from __future__ import annotations

import ctypes
import datetime as dt
import logging
import math
import multiprocessing
import os
import random
import time
from concurrent.futures import ProcessPoolExecutor, as_completed
from contextlib import AbstractContextManager
from multiprocessing import Queue as MPQueue
from multiprocessing import shared_memory
from multiprocessing.connection import Connection
from multiprocessing.managers import DictProxy, ListProxy
from multiprocessing.sharedctypes import Synchronized
from multiprocessing.synchronize import BoundedSemaphore as MPBSem
from typing import Any, Literal, NamedTuple, TypedDict

import numpy as np
from pydantic import BaseModel, ValidationError

logging.basicConfig(format="%(asctime)s | %(levelname)s | %(name)s | %(message)s", datefmt="%H:%M:%S")
logger = logging.getLogger(f"PID {os.getpid()}")
logger.setLevel(logging.INFO)


# region Golden Rules

# 0. Miscellaneous
# - use multiprocessing when you need parallel calculations for CPU-bound work
# - each process gets its own GIL and thus many processes can run simultaneously on different CPU cores
# - Python can start a new process using either spawn(), fork() or fork_server() (all of them provide separate GILs for new processes)
# - spawn():
# -- usually default on Windows and macOS and available on Linux
# -- starts a new child Python process from scratch (doesn't clone the parent)
# -- tries to immediately load the module and call the desired callable
# - fork():
# -- usually default on Linux and available only on Linux
# -- clones the parent so that the child is identical
# -- uses copy-on-write method
# -- doesn't copy parent's threads which can cause subtle bugs
# -- for example, a lock owned in the parent by a thread will become locked in the child and no thread will be able to release it
# -- this can cause deadlocks
# -- fork() also clones open file descriptors which is also problematic
# - fork_server():
# -- clones the parent process, then trims it so that it's basically a fresh Python process
# -- it's then used to create child processes on demand by forking and running the desired callable
# -- safe but not well documented
# 1. Main guard
# - use the pattern with "main()" and "if __name__ == "__main__"" when spawning new processes
# - otherwise the spawning can become recursive
# - if using spawn(), Python starts a fresh interpreter for a child process and that interpreter imports the module containing your worker function
# - without the main guard, top-level code that creates more processes can run again in the child, potentially causing recursive process creation
# 2. Top-level workers
# - make sure the workers aren't lambdas or nested functions but rather top-level functions easy to import from your modules
# 3. Keep data simple
# - processes don't share data
# - use primitive types, lists, dictionaries, etc., when data needs to be passed between processes without any additional mechanisms (like pipes or queues)
# - otherwise Python might have problems serializing and deserializing your complex data (it uses pickle.dumps() and pickle.loads() for that)
# - e.g. locks, connections, file handles, or sockets shouldn't be used when executing future.result() in a pool

# endregion


# region Example 1


def ex_1_calcualte_squares(limit: int) -> None:
    if limit < 1:
        raise ValueError("limit should be no smaller than one")
    pid = os.getpid()
    res = sum(x**2 for x in range(1, limit + 1))
    logger.info("PID %d: %d", pid, res)


def ex_1() -> None:
    workers = [multiprocessing.Process(target=ex_1_calcualte_squares, args=(i,)) for i in [100, 1000]]
    for w in workers:
        w.start()
    for w in workers:
        w.join()
        logger.info("Child PID %d exited with exit code %d", w.pid, w.exitcode)


# endregion


# region Example 2


def ex_2_process_asset(name: str) -> str:
    logger.info("Processing %s...", name)
    time.sleep(0.1 * len(name))
    if "broken" in name.lower():
        msg = f"Broken asset {name}"
        raise ValueError(msg)
    logger.info("Finished processing %s", name)
    return f"{name} processed by PID {os.getpid()}"


def ex_2() -> None:
    assets = [
        "player.png",
        "forest.png",
        "broken_shader",
        "music.ogg",
        "enemy.png",
        "broken_model",
    ]
    max_workers = 3
    successes = 0

    # note that pool transfers data between different processes
    with ProcessPoolExecutor(max_workers=max_workers) as ppe:
        futures = {ppe.submit(ex_2_process_asset, asset): asset for asset in assets}

        for future in as_completed(futures):
            asset = futures[future]

            try:
                res = future.result(timeout=5)
            except ValueError:
                logger.exception("An error accurred while processing the asset %s", asset)
            else:
                successes += 1
                logger.info("Asset successfully processed, returned: %s", res)

    logger.info("Successes: %d, Failures: %d", successes, len(assets) - successes)


# endregion


# region Example 3


type Quality = Literal["low", "medium", "high"]


class Ex3Config(TypedDict):
    quality: Quality


# each process gets its own "local" but still global config variable
ex_3_config: Ex3Config | None = None


def ex_3_initializer(config: Ex3Config) -> None:
    global ex_3_config
    ex_3_config = config
    logger.info("Config quality set to %s", ex_3_config["quality"])


def ex_3_process_asset(name: str) -> tuple[str, Quality | None]:
    logger.info("Processing %s...", name)
    time.sleep(0.1 * len(name))
    # if "broken" in name.lower():
    #     msg = f"Broken asset {name}"
    #     raise ValueError(msg)
    logger.info("Finished processing %s", name)
    return f"{name} processed by PID {os.getpid()}", ex_3_config["quality"] if ex_3_config is not None else None


def ex_3() -> None:
    assets = [
        "player.png",
        "forest.png",
        "broken_shader",
        "music.ogg",
        "enemy.png",
        "broken_model",
    ]
    quality_settings: Ex3Config = {"quality": "high"}
    max_workers = 2

    with ProcessPoolExecutor(
        max_workers=max_workers, initializer=ex_3_initializer, initargs=(quality_settings,)
    ) as ppe:
        results = list(ppe.map(ex_3_process_asset, assets))
        for res, asset in zip(results, assets, strict=True):
            try:
                logger.info("Asset %s processed successfully, %s", asset, res)
            except ValueError:
                logger.exception("Error occurred while processing asset %s", asset)


# endregion


# region Example 4.1 (Pipe)

# a FIFO communication channel for two processes
# for bidirectional (duplex) pipes the data can flow in and out on both endpoints
# for unidirectional pipes the data flows in at one endpoint and flows out at another endpoint
# it's recommended for each process to close the endpoint which isn't going to be used in that process
# it's also recommended to have a strict convention about which endpoint is for what
# leaving unnecessary endpoints opened can prevent another process from observing that the connection has ended


class Ex4WorkerIn(BaseModel):
    data: str | None


class Ex4WorkerOut(BaseModel):
    processed: str
    word_count: int


class Ex4WorkerOutDict(TypedDict):
    processed: str
    word_count: int


def ex_4_1_worker(parent_endpoint: Connection, child_endpoint: Connection) -> None:
    logger.info("Child worker starts...")

    parent_endpoint.close()  # child won't use the parent endpoint

    data_to_send: Ex4WorkerOutDict | None = None

    try:
        while True:
            try:
                worker_input = Ex4WorkerIn(data=child_endpoint.recv())

                if worker_input.data is None:
                    logger.info("Child worker received sentinel value and shuts down...")
                    break

                time.sleep(1)
                new_msg = worker_input.data.strip().upper()
                word_count = len(new_msg.split())
                data_to_send = {"processed": new_msg, "word_count": word_count}
                child_endpoint.send(data_to_send)
            except ValidationError:
                logger.exception("Child worker received unexpected data format, returning default results...")
                data_to_send = {"processed": "", "word_count": 0}
                child_endpoint.send(data_to_send)
            except EOFError:
                logger.exception("Pipe was unexpectedly closed by the parent, child worker quits...")
                break
    finally:
        child_endpoint.close()


def ex_4_1_pipe() -> None:
    parent_conn, child_conn = multiprocessing.Pipe(duplex=True)

    worker = multiprocessing.Process(
        target=ex_4_1_worker,
        args=(parent_conn, child_conn),
    )

    worker.start()

    child_conn.close()  # parent won't use the child endpoint

    data_to_send = ["   Inter Process Communication   ", " pipe", "bello! (appfff)              "]

    try:
        for i, data in enumerate(data_to_send):
            logger.info("Parent sends data to the child worker...")
            parent_conn.send(data)

            try:
                logger.info("Parent waits for data from the child worker...")
                res = Ex4WorkerOut(**parent_conn.recv())
                logger.info("Processed: %s, Word Count: %d", res.processed, res.word_count)
            except ValidationError:
                logger.exception("Parent received unexpected data format from the child worker")
            except EOFError:
                logger.exception("Pipe was unexpectedly closed by the child worker, parent quits...")
                break

            if i == len(data_to_send) - 1:
                parent_conn.send(None)
    finally:
        parent_conn.close()
        worker.join()

    logger.info("Parent shuts down...")


# endregion


# region Example 4.2 (Queue)

# another FIFO communication channel for multiple processes
# under the hood it's a thread-safe and process-safe Pipe with additional mechanisms
# when objects are sent into the Queue they are first serialized (pickled)
# once they are received from the Queue they must be deserialized (unpickled)
# this creates overhead and means that changes made to objects after sending them into the queue aren't reflected when they're received


class Ex4QueueItem(BaseModel):
    item_id: int
    data: int


class Ex4QueueItemDict(TypedDict):
    item_id: int
    data: int


def ex_4_2_consumer(
    task_queue: MPQueue[Ex4QueueItemDict | None],
    result_queue: MPQueue[Ex4QueueItemDict | None],
) -> None:
    while True:
        task = task_queue.get()

        if task is None:
            break

        try:
            item = Ex4QueueItem(**task)
            item.data = -10 * item.data

            time.sleep(1)

            result_queue.put({"item_id": item.item_id, "data": item.data})

        except ValidationError:
            logger.exception("Consumer got unexpected data format to consume, sending None...")
            result_queue.put(None)


def ex_4_2_queue() -> None:
    # max_size = 5
    task_q: MPQueue[Ex4QueueItemDict | None] = MPQueue()
    result_q: MPQueue[Ex4QueueItemDict | None] = MPQueue()

    num_workers = 3
    workers = [multiprocessing.Process(target=ex_4_2_consumer, args=(task_q, result_q)) for _ in range(num_workers)]
    for worker in workers:
        worker.start()

    num_jobs = 10
    for i in range(num_jobs):
        random_data = random.randrange(-10, 10, 1)
        task_q.put({"item_id": i, "data": random_data})
        logger.info("PUT item_id=%d, data=%d", i, random_data)

    for _ in workers:
        task_q.put(None)

    try:
        for _ in range(num_jobs):
            result = result_q.get()

            if result is None:
                logger.info("Consumer sent None, something must have gone wrong")
                continue

            try:
                item = Ex4QueueItem(**result)
                logger.info("GET item_id=%d, data=%d", item.item_id, item.data)

            except ValidationError:
                logger.exception("Producer got unexpected data format from consumer, skipping...")

        for worker in workers:
            worker.join()

    finally:
        task_q.close()
        result_q.close()


# endregion


# region Example 4.3 (Manager)

# used to safely access objects shared between multiple processes
# Manager spawns a separate, dedicated server process that hosts Python objects (like lists, dictionaries, or custom classes)
# other processes interact with these objects via proxy objects using local RPC (Remote Procedure Calls) over a socket or pipe
# the manager process handles some synch and state updates automatically although compound operations such dict["key"]+=1 aren't atomic and require a lock
# Manager is a pretty slow mechanism
# it may not work for nested mutable objects (re-assignment required) (a managed container doesn't automatically make every object nested inside it a managed object)

# Remote Procedure Call (RPC) is a communication protocol that allows a computer program to run a function or procedure on another computer in a network
# as if it were a local function call, without needing to understand the underlying network details
# 1. the client program invokes a local stub function, passing parameters just like a normal function call
# 2. the client stub packages and converts (serializes) those parameters into a network-friendly message format (marshalling)
# 3. the message is sent across the network from the client to the server
# 4. the server-side stub receives the message, unpacks (deserializes) the parameters (unmarshalling), and executes the actual procedure
# 5. the server sends the return value back through the network, where the client stub extracts the result and returns it to the client program


EX_4_3_ERROR_CHANCE = 0.5


type Ex4SharedState = Literal["ok", "fail"]


def ex_4_3_tasker(task: str) -> None:
    if random.random() < EX_4_3_ERROR_CHANCE:
        msg = f"Unknown error occurred for task {task}"
        raise ValueError(msg)


def ex_4_3_worker(
    lock: AbstractContextManager[Any],
    shared_dict: DictProxy[Ex4SharedState, int],
    shared_list: ListProxy[str],
    worker_id: int,
    tasks: list[str],
) -> None:
    for task in tasks:
        shared_list.append(f"Worker {worker_id}: start task {task}")

        try:
            time.sleep(1)
            ex_4_3_tasker(task)
            with lock:
                shared_dict["ok"] += 1
                shared_list.append(f"Worker {worker_id}: SUCCESS, finished task {task}")

        except ValueError:
            with lock:
                shared_list.append(f"Worker {worker_id}: FAILURE, abort task {task}")
                shared_dict["fail"] += 1


def ex_4_3_manager() -> None:
    with multiprocessing.Manager() as manager:
        lock = manager.Lock()
        shared_state: DictProxy[Ex4SharedState, int] = manager.dict({"ok": 0, "fail": 0})
        shared_logs: ListProxy[str] = manager.list()

        task_sets = [
            ["page_1", "page_2", "page_3"],
            ["page_4", "page_5"],
            ["page_6", "page_7", "page_8", "page_9"],
        ]

        workers = [
            multiprocessing.Process(target=ex_4_3_worker, args=(lock, shared_state, shared_logs, i, task_set))
            for i, task_set in enumerate(task_sets)
        ]

        for worker in workers:
            worker.start()

        for worker in workers:
            worker.join()

        if any(worker.exitcode != 0 for worker in workers):
            raise RuntimeError("Worker exited with non-zero exit code")

        logger.info("ok = %d, fail = %d", shared_state["ok"], shared_state["fail"])

        for item in list(shared_logs):
            logger.info(item)


# endregion


# region Example 4.4 (shared_memory)

# shared_memory provides direct access to a block of raw, unmanaged physical RAM
# multiple independent processes map this exact same block of memory directly into their own virtual address spaces
# no serialization involved
# useful for large datasets
# doesn't contain built-in mechanisms for preventing race conditions (you have to do it manually or make sure processes use disjoint regions of the shared buffer)


class Ex4ChangeSpec(NamedTuple):
    start_idx: int  # inclusive
    end_idx: int  # exclusive
    scale_factor: int


def ex_4_4_worker(
    shared_memory_name: str, array_shape: tuple[int], array_dtype: np.dtype[np.int64], change_spec: Ex4ChangeSpec
) -> None:
    if change_spec.start_idx < change_spec.end_idx:
        existing_shm = shared_memory.SharedMemory(name=shared_memory_name, create=False)
        my_ints = np.ndarray(shape=array_shape, dtype=array_dtype, buffer=existing_shm.buf)

        my_ints[change_spec.start_idx : change_spec.end_idx] *= change_spec.scale_factor

        existing_shm.close()


def ex_4_4_shared_memory() -> None:
    array_size = 10
    template = np.array([i * 10 for i in range(array_size)])
    logger.info("shape: %s, type: %s, bytes: %d", str(template.shape), str(template.dtype), template.nbytes)

    shm_name = "_".join(f"MYINTS {dt.datetime.now(tz=dt.UTC)}".split())
    logger.info(shm_name)

    try:
        shm = shared_memory.SharedMemory(name=shm_name, create=True, size=template.nbytes)

        # create a numpy array view of the shared memory buffer
        my_ints = np.ndarray(shape=template.shape, dtype=template.dtype, buffer=shm.buf)

        # copy the template values into the actual array
        my_ints[:] = template[:]

        logger.info(my_ints)

        # calcualte disjoint regions of shared memory for each child process
        # this is more efficient that using locks but creates the risk of race conditions
        # note that when the array size is smaller than the number of workers
        # then some workers will be unnecessary
        num_workers = 3
        elems_per_worker = math.ceil(array_size / num_workers)
        change_specs: list[Ex4ChangeSpec] = []
        for i in range(num_workers):
            start = i * elems_per_worker  # inclusive
            end = min((i + 1) * elems_per_worker, array_size)  # exclusive
            scale = random.choice([-3, -2, 2, 3])
            change_specs.append(Ex4ChangeSpec(start_idx=start, end_idx=end, scale_factor=scale))

        for spec in change_specs:
            logger.info("%d, %d, %d", spec.start_idx, spec.end_idx, spec.scale_factor)

        workers = [
            multiprocessing.Process(
                target=ex_4_4_worker, args=(shm_name, template.shape, template.dtype, change_specs[i])
            )
            for i in range(num_workers)
        ]

        for worker in workers:
            worker.start()

        for worker in workers:
            worker.join()

        if any(worker.exitcode != 0 for worker in workers):
            raise RuntimeError("Worker exited with non-zero exit code")

        # changes made in child processed should be reflected in the parent process
        logger.info(my_ints)
    finally:
        shm.close()
        shm.unlink()


# endregion


# region Example 5


# multiprocessing has similar concepts to multithreading
# for example: Lock, RLock, Semaphore, BoundedSemaphore, Event, Condition


def ex_5_worker(counter: Synchronized[ctypes.c_int], gpu_semaphore: MPBSem, num_assets: int) -> None:
    for _ in range(num_assets):
        with gpu_semaphore:
            time.sleep(0.0001)

        with counter.get_lock():
            counter.value += 1  # type: ignore[]


def ex_5() -> None:
    shared_counter = multiprocessing.Value("i", 0)  # integer initialized to zero

    b_sem = multiprocessing.BoundedSemaphore(2)

    num_tasks = 5000
    num_workers = 6

    workers = [
        multiprocessing.Process(target=ex_5_worker, args=(shared_counter, b_sem, num_tasks)) for _ in range(num_workers)
    ]

    for worker in workers:
        worker.start()

    for worker in workers:
        worker.join()

    logger.info(shared_counter.value)


# endregion


# region Bytes


def about_bytes() -> None:
    # ASCII:
    # - mapping between characters and numbers (each character is represented as a number)
    # Unicode:
    # - modern extension of ASCII, assigns a unique number (code point) to every abstract character, e.g. character, symbol, emoji, etc.
    # UTF-8:
    # - set of rules how to represent Unicode's code points inside computer memory, some code points use 1 byte, some 2 bytes, some 3 bytes and some 4 bytes
    # UTF-16, UTF-32:
    # - alternative sets of rules, they differ in how many bytes are used for code points to represent them in computer memory
    #
    # strings vs bytes:
    # - strings can be converted to raw bytes and raw bytes can be converted to strings and they're not the same thing
    # - strings in Python are sets of Unicode's abstract characters represented by Unicode's code points
    # - raw bytes are sequences of bytes, i.e. sequences of 8-bit integers
    # - the mapping between them is done using UTF-8 (or sometimes using other UTFs, like UTF-16 or UTF-32)
    # - for example:
    # --- we have the letter "A" followed by the symbol "€"
    # --- "A€" = string, i.e. abstract characters U+0041 and U+20AC
    # --- b"A\xe2\x82\xac" = bytes, i.e. sequence of integers which represent U+0041 and U+20AC in computer memory (here: [65, 226, 130, 172])
    # --- note that if Python finds an ASCII printable character in a sequence of bytes, like a letter, it displays it in a human-friendly format
    # - strings:
    # --- when Python sees a string, it operates on abstract characters
    # --- for example, len("€") = 1 even though "€" is represented with 3 bytes, not with 1 byte
    # --- Python is smart enough to display those 3 bytes as "€" because it knows Unicode
    # --- inside computer memory, those 3 bytes are treated by Python as a whole, so Python sees one number (8364)
    # --- used for human-friendly text manipulation
    # - bytes:
    # --- represented in Python with b"XXXXX", where X is either an ASCII character or a hex number representing a byte
    # --- a hex number inside b"" is represented as \xYY where Y is a hex digit (0-9, A-F)
    # --- when Python sees a byte sequence, it treats them as a list of ints, each one from 0 to 255
    # --- for example, len(b"\xe2\x83\xac") = 3, where "\xe2\x83\xac" represent "€"
    # --- inside computer memory, those 3 bytes are treated by Python as separate, so Python chops 8364 into 3 separate numbers ([226, 130, 172])
    # --- used for data transmission to files, network sockets, etc.
    #
    # Unicode defines the mapping between numbers and abstract characters like letters, symbols and emojis
    # in Python, if you don't have a Unicode abstract character to copy-paste directly into editor
    # you can use those Unicode numbers to print abstract characters
    # for example:
    # - assuming UTF-8 for representing Unicode abstract characters...
    # - 2-byte Unicode numbers are represented with \uXXXX, where X represents a hex digit (0-9, A-F)
    # - symbol '✓' has the code point U+2713 so it will be "\u2713"
    # - 4-byte Unicode numbers are represented with \UXXXXXXXX, where X represents a hex digit (0-9, A-F) (leading zeros need to be added if necessary)
    # - the snake emoji '🐍' has the code point U+1F40D so it will be "\U0001F40D"
    # - alternatively you can use the name of the Unicode abstract character, e.g. "\N{SPARKLES}"
    #
    # a related concept is serialization (and deserialization)
    # complex Python structures, e.g. dictionaries, can consist of many data types, memory pointers, addresses, etc.
    # sending such a structure over a network cable is impossible because the network cable doesn't understand what is a memory pointer, etc.
    # the network cable only understands sequences of raw bytes, i.e. one 8-bit integer going through it after another
    # how this sequence is interpreted is the problem of a computer program, it's not the problem of the network cable
    # programs must then convert complex structures into flat sequences of bytes which can be easily interpreted by other programs when they receive such flat sequences from the network
    # this requires a standard format for transferring data as a sequence of flat bytes
    # one such format is JSON, which is one flat string representing the entire complex structure of an object
    # this string can't be arbitrary, it must have some rules, e.g. an opening brace "{" must have a matching closing brace "}" later in the string
    # if you manage to convert a complex Python structure into a flat JSON string in your program, you can easily send it to another program across the network
    # one way to do this is to define how a Python structure is represented as a dictionary, because dictionaries can be easily converted into flat JSON strings
    # the workflow is:
    # - serialization: Python object -> Python dictionary -> flat JSON string -> sequence of bytes -> network cable
    # - deserialization: network cable -> sequence of bytes -> flat JSON string -> Python dictionary -> Python object
    # note that "JSON string -> sequence of bytes" is the convertion from string to bytes (there is also the opposite conversion in the workflow)

    smile_str = "\U0001f600"
    smile_bytes = smile_str.encode("utf-8")
    logger.info(smile_str)
    logger.info(len(smile_str))
    logger.info(smile_bytes)
    logger.info(list(smile_bytes))
    logger.info(len(list(smile_bytes)))
    logger.info(smile_bytes.decode("utf-8"))


# endregion


def main() -> None:
    about_bytes()

    logger.info("Logical CPU threads is %d", os.cpu_count())
    logger.info("Default start method is %s", multiprocessing.get_start_method())

    # ex_1()
    # ex_2()
    # ex_3()
    # ex_4_1_pipe()
    # ex_4_2_queue()
    # ex_4_3_manager()
    # ex_4_4_shared_memory()
    # ex_5()

    # note: waiting vs cancellation vs termination
    # - waiting with timeout doesn't mean that the process which didn't produce the result on time will be killed
    # - cancellation request doesn't mean that the termination of the running process will actually happen (cancellation works on processes that haven't started yet)


if __name__ == "__main__":
    main()
