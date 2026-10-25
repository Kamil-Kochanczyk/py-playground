import queue
import random
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import TypedDict

# region Example 1


ex_1_completed_tasks = 0


def ex_1_process_task(n_tasks: int, lock: threading.Lock) -> None:
    print(f"{threading.current_thread().name}: start")
    global ex_1_completed_tasks

    # slower version:
    # for _ in range(n_tasks):
    #     with lock:
    #         completed_tasks += 1

    # faster version:
    completed = 0
    for _ in range(n_tasks):
        completed += 1
    with lock:
        ex_1_completed_tasks += completed

    print(f"{threading.current_thread().name}: end")


def ex_1_task_counter() -> None:
    num_workers = 4
    num_tasks = 50_000
    completed_tasks_lock = (
        threading.Lock()
    )  # lock adds overhead (use as rarely as possible and envelop the smallest code blocks possible)
    workers = [
        threading.Thread(target=ex_1_process_task, args=(num_tasks, completed_tasks_lock), name=f"THR{i}")
        for i in range(num_workers)
    ]
    start = time.perf_counter()
    for worker in workers:
        worker.start()  # OS schedules the threads independently (execution order never guaranteed)
    print("MAIN THR: time to wait for workers...")
    for worker in workers:
        worker.join()
    elapsed = time.perf_counter() - start
    print(f"{elapsed:.2f} s")
    print(ex_1_completed_tasks)
    # note that start() is a non-blocking call (it doesn't halt the main thread but returns immediately)
    # only join() halts the main thread
    # but due to GIL only one thread can execute at any instant
    # so if multiple threads are created, then they must run concurrently on one core
    # Python must switch quickly between them to advance them all (time slicing)


# endregion


# region Example 2


def ex_2_process_asset(asset_name: str) -> str:
    print(f"{threading.current_thread().name}: start processing {asset_name}")
    time.sleep(0.1 * len(asset_name))
    if asset_name == "broken_shader":
        raise ValueError("Broken shader cannot be processed")
    return f"{threading.current_thread().name}: end processing {asset_name}"


def ex_2_thread_pool_executor() -> None:
    assets = [
        "texture",
        "model",
        "audio",
        "shader",
        "broken_shader",
    ]
    num_workers = 3

    # with ThreadPoolExecutor(max_workers=num_workers, thread_name_prefix="TPE") as tpe:
    #     futures = [tpe.submit(ex_2_process_asset, asset) for asset in assets]  # non-blocking call
    #     results = [
    #         future.result() for future in futures
    #     ]  # blocking call (results match the submission order but the completion order is independent of the submission order)
    #     print(results)

    with ThreadPoolExecutor(max_workers=num_workers, thread_name_prefix="TPE") as tpe:
        futures = {tpe.submit(ex_2_process_asset, asset): asset for asset in assets}  # non-blocking call
        succeeded = 0
        for future in as_completed(futures):  # yields futures as they complete (not according to submission order)
            try:
                res = future.result()  # excpetion stored in future is raised only after calling result()
            except ValueError as ve:
                print(f"(ERROR, {futures[future]}) {ve!r}")
            else:
                print(f"(SUCCESS, {futures[future]}) {res}")
                succeeded += 1

    # with block ensures that the executor shuts down and waits for the submitted tasks to finish before printing summary
    print(f"Succeded: {succeeded}\nFailed: {len(assets) - succeeded}")


# endregion


# region Example 3


# experimenting with queues and events


EX3_ERROR_CHANCE = 0.5
EX3_WAIT_TIMEOUT = 0.1


def ex_3_process_job(job: str) -> None:
    print(f"{threading.current_thread().name}: processing job {job}")

    time.sleep(random.uniform(0.5, 2.0))
    if random.random() < EX3_ERROR_CHANCE:
        raise ValueError("Random error")


def ex_3_producer(stop_event: threading.Event, queue: queue.Queue[str | None], asset_type: str, num_jobs: int) -> None:
    thread_name = threading.current_thread().name

    print(f"{thread_name}: start producing {num_jobs} jobs for {asset_type.capitalize()}")

    for i in range(1, num_jobs + 1):
        if stop_event.wait(timeout=EX3_WAIT_TIMEOUT):
            print(f"{thread_name}: shutting down gracefully")
            break

        print(f"{thread_name}: try to put job {i} for {asset_type.capitalize()} into the queue")

        queue.put(f"{asset_type.capitalize()}{i}")

        print(f"{thread_name}: job {i} for {asset_type.capitalize()} has been put into the queue")

        time.sleep(random.uniform(0.5, 2.0))

    print(f"{thread_name}: finished")


def ex_3_consumer(queue: queue.Queue[str | None]) -> None:
    thread_name = threading.current_thread().name

    print(f"{thread_name}: start consuming jobs")

    while True:
        try:
            job = queue.get()

            if job is None:
                break

            ex_3_process_job(job)
        except ValueError as e:
            print(f"{thread_name}: error consuming job {job}: {e!r} (moving on to the next job)")
        else:
            print(f"{thread_name}: successfully consumed job {job}")
        finally:
            queue.task_done()

    print(f"{thread_name}: finished")


def ex_3_producer_consumer() -> None:
    stop_event = threading.Event()
    assets_queue: queue.Queue[str | None] = queue.Queue(maxsize=3)  # this queue is already thread-safe!
    asset_types_num_jobs = [("music", 3), ("ui", 2), ("player", 4)]
    num_cons = 2

    producers = [
        threading.Thread(target=ex_3_producer, args=(stop_event, assets_queue, at, nj), name=f"PROD{i}")
        for i, (at, nj) in enumerate(asset_types_num_jobs)
    ]
    consumers = [
        threading.Thread(
            target=ex_3_consumer,
            args=(assets_queue,),
            name=f"CONS{i}",
        )
        for i in range(num_cons)
    ]

    for cons in consumers:
        cons.start()

    for prod in producers:
        prod.start()

    if random.random() < EX3_ERROR_CHANCE:
        time.sleep(random.random())
        stop_event.set()

    # make sure all jobs have been generated before waiting for the queue
    for prod in producers:
        prod.join()

    print("MAIN THR: producers finished all jobs and quit!")

    assets_queue.join()

    print("MAIN THR: consumers finished all jobs!")

    for cons in consumers:
        if cons.is_alive():
            assets_queue.put(None)

    assets_queue.join()

    print("MAIN THR: consumers acknowledged their sentinel values!")

    for cons in consumers:
        cons.join()

    print("MAIN THR: consumers quit!")

    print("MAIN THR: the end!")


# endregion


# region Example 4


# example of a deadlock caused by recursive acquisition of a non-reentrant lock
# the thread waits for the lock but this thread is the only one who can release the lock
# so it cannot proceed
# lock = threading.Lock()
# def inner():
#     with lock:
#         print("Inside inner")
# def outer():
#     with lock:
#         inner()
# outer()
# a reentrant lock allows the thread that already owns the lock to acquire it again
# the only change needed is "lock = threading.RLock()" instead of "lock = threading.Lock()"
# RLock tracks its owning thread and the number of times that thread has acquired it
# the owning thread must release it the same number of times before another thread can acquire it

# tip: in general: lock = umbrella-term, mutex = "who has restrictive access?", semaphore = "how many threads have access?"
# tip: in Python: lock = mutex
# tip: use consistent lock ordering to prevent deadlocks (e.g. always acquire lock_a before acquiring lock_b)

# BoundedSemaphore raises ValueError if releasing it would increase the counter above its initial value
# this can help detect accidental over-releases

# Event can handle a simple one-time signal
# Condition is more suitable when threads need to inspect shared state and wait for that state to change before continuing

# wait():
# - puts the current thread to sleep
# - it automatically releases the underlying lock when it goes to sleep allowing other thread to do work
# - when it gets woken up (via a notification), it automatically tries to reacquire the lock before returning
# - not recommended due to spurious wakeups
# - spurious wakeup occurs when a thread wakes up from a waiting state on a condition variable even though no other thread notified it
# - because of this, the condition it was waiting for might still be false
# - it's essentially a "false alarm" for no apparent reason
# - spurious wakeups happen because of how OS handles threading and synchronization

# wait_for(predicate):
# - a safe wrapper around wait()
# - it automatically handles spurious wakeups by checking the desired condition in the while loop on every wake up
# - it loops on every wake up until the condition is satisfied

# notify(n=1):
# - wakes up n threads (by default, just 1) that are currently sleeping in a wait() state on the given condition variable
# - the woken thread doesn't resume instantly, though
# - it has to wait until the thread that called notify() releases the lock

# notify_all():
# - wakes up all threads that are currently waiting on this condition variable


ex_4_resource_users = 0


class Ex4SharedState(TypedDict):
    initialized: bool


def ex_4_worker(
    bounded_semaphore: threading.BoundedSemaphore, res: str, lock: threading.Lock, max_resource_users: int
) -> None:
    global ex_4_resource_users
    thread_name = threading.current_thread().name

    with bounded_semaphore:
        print(f"{thread_name}: processing resource {res}")

        with lock:
            ex_4_resource_users += 1
            if ex_4_resource_users > max_resource_users:
                raise AssertionError("Max resource users exceeded maximum allowed value")

        try:
            time.sleep(1)
        finally:
            with lock:
                ex_4_resource_users -= 1
                if ex_4_resource_users < 0:
                    raise AssertionError("Max resource users fell below zero")

        print(f"{thread_name}: finished processing resource {res}")


def ex_4_renderer(condition: threading.Condition, shared_state: Ex4SharedState) -> None:
    thread_name = threading.current_thread().name
    with condition:
        print(f"{thread_name}: waiting for the condition to be true...")
        condition.wait_for(lambda: shared_state["initialized"])
        print(f"{thread_name}: waiting done (moving on to rendering)")
    print(f"{thread_name}: rendering in progress...")


def ex_4_initializer(condition: threading.Condition, shared_state: Ex4SharedState) -> None:
    thread_name = threading.current_thread().name
    print(f"{thread_name}: initializing (no lock acquired)")
    time.sleep(2)
    print(f"{thread_name}: initializing done")
    with condition:
        print(f"{thread_name}: notifying (lock acquired)")
        shared_state["initialized"] = True
        condition.notify_all()
        print(f"{thread_name}: notifying done")


def ex_4_sem_and_cond() -> None:
    max_res_usr_lock = threading.Lock()
    max_res_usr = 3
    bnd_sem = threading.BoundedSemaphore(max_res_usr)
    workers = [
        threading.Thread(
            target=ex_4_worker, args=(bnd_sem, f"RES{i}", max_res_usr_lock, max_res_usr), name=f"WORKER{i}"
        )
        for i in range(6)
    ]
    for worker in workers:
        worker.start()
    for worker in workers:
        worker.join()

    cond_var = threading.Condition()
    shared: Ex4SharedState = {"initialized": False}

    initiliazer = threading.Thread(target=ex_4_initializer, args=(cond_var, shared), name="INIT")
    renderers = [threading.Thread(target=ex_4_renderer, args=(cond_var, shared), name=f"REND{i}") for i in range(4)]

    initiliazer.start()

    for r in renderers:
        r.start()

    initiliazer.join()

    for r in renderers:
        r.join()

    print("Main thread: finished")


# endregion


def background_check() -> None:
    thread_name = threading.current_thread().name
    while True:
        print(f"{thread_name}: check if main is alive...")
        time.sleep(1)


def main() -> None:
    daemon = threading.Thread(target=background_check, daemon=True, name="DAEMON")
    daemon.start()

    # schedule a new function on another thread
    prompt = threading.Timer(interval=2.0, function=lambda: print("Enter Q or I'll turn off this program >:D"))
    prompt.start()

    # barrier can be used to ensure all threads are initialized before moving on
    num_players = 3
    barrier = threading.Barrier(parties=num_players, action=lambda: print("Barrier released!"), timeout=5)
    players = [threading.Timer(interval=i, function=barrier.wait) for i in range(num_players)]
    for player in players:
        player.start()

    # ex_1_task_counter()
    # ex_2_thread_pool_executor()
    # ex_3_producer_consumer()
    ex_4_sem_and_cond()

    # demon killed automatically (it doesn't stop the main thread)


if __name__ == "__main__":
    main()
