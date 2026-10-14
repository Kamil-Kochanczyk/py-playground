import asyncio
import math
import random
import time
from collections.abc import AsyncGenerator, Awaitable, Callable, Coroutine
from dataclasses import dataclass
from functools import wraps
from http import HTTPStatus
from types import TracebackType
from typing import Any, ClassVar, Literal, NamedTuple, ParamSpec, Self, TypedDict, TypeVar

import aiohttp

# region Example 0 - Introduction


async def hello() -> None:
    print("Hello async world")


async def countdown(seconds: int) -> None:
    for i in range(seconds, 0, -1):
        print(i)
        await asyncio.sleep(1)
    print("Done!")


# endregion


# region Examples 1, 2


async def worker(name: str, delay: int) -> None:
    print(f"{name} started")
    await asyncio.sleep(delay)
    print(f"{name} finished")


async def bad_worker(name: str, delay: int) -> None:
    print(f"{name} started")
    time.sleep(delay)
    print(f"{name} finished")


# endregion


# region Examples 3.1, 3.2, 3.3


async def calculate_square(number: int) -> int:
    await asyncio.sleep(3)
    return number**2


async def fetch_weather() -> str:
    await asyncio.sleep(2)
    return "Sunny"


async def fetch_news() -> list[str]:
    await asyncio.sleep(3)
    # return ["News 1", "News 2"]
    raise RuntimeError("News service unavailable")  # uncomment to see what happens when one independent service fails


async def fetch_currency() -> float:
    await asyncio.sleep(1)
    return 4.25


# endregion


# region Examples 4.1, 4.2, 4.3


async def bad_fetch_service(name: str, delay: int) -> str:
    print(f"{name}: bad service started")
    await asyncio.sleep(delay)
    print(f"{name}: bad service finished")
    return f"{name}: bad service result"


async def good_fetch_service(name: str, delay: int, my_timeout: int) -> str:
    try:
        async with asyncio.timeout(my_timeout):
            return await bad_fetch_service(name, delay)
    except TimeoutError:
        return f"{name} timed out after {my_timeout}s"


# endregion


# region Example 5 - Task cancellation


async def long_operation() -> None:
    try:
        my_counter = 0
        while True:
            print(f"{my_counter}: Long operation working...")
            my_counter += 1
            await asyncio.sleep(1)
    except asyncio.CancelledError:
        print("Long operation cancelled...")
        raise  # CancelledError should be propagated up because asyncio components might misbehave if it's swallowed
    finally:
        print("Long operation cleanup...")


# endregion


# region Example 6 - More complicated example


P = ParamSpec("P")
T = TypeVar("T")


@dataclass(frozen=True)
class ServiceSuccess[T]:
    value: T
    attempts: int


class MaxAttemptsExceededError(Exception):
    def __init__(self, name: str, attempts: int, last_error: Exception) -> None:
        self.name = name
        self.attempts = attempts
        self.last_error = last_error
        super().__init__(f"Service {name} exceeded max attempts ({attempts}), last error was {last_error!r}")


def safe_service(
    my_timeout: float,
    max_attempts: int,
    attempts_delay: float,
    name: str,
    retry_on: tuple[type[Exception], ...] = (TimeoutError, RuntimeError),
) -> Callable[[Callable[P, Awaitable[T]]], Callable[P, Coroutine[Any, Any, ServiceSuccess[T]]]]:

    if my_timeout <= 0 or max_attempts < 1 or attempts_delay < 0:
        raise ValueError("allowed values: my_timeout positive, max_attempts at least 1, attempts_delay non-negative")

    def actual_decorator(
        unsafe_service: Callable[P, Awaitable[T]],
    ) -> Callable[P, Coroutine[Any, Any, ServiceSuccess[T]]]:

        # wraps preserves the original function's metadata (name, docstring, etc.) in the decorated function
        @wraps(unsafe_service)
        async def wrapper(*args: P.args, **kwargs: P.kwargs) -> ServiceSuccess[T]:

            last_error: Exception | None = None

            for attempt in range(1, max_attempts + 1):
                try:
                    async with asyncio.timeout(my_timeout):
                        unsafe_service_res = await unsafe_service(*args, **kwargs)
                        print(f"{name}, attempt {attempt}: fetch completed")
                        return ServiceSuccess(value=unsafe_service_res, attempts=attempt)
                except asyncio.CancelledError:
                    print(f"{name}, attempt {attempt}: cancellation detected (raising it)")
                    raise
                except retry_on as exc:
                    print(f"{name}, attempt {attempt}: unexcepted error occurred")
                    last_error = exc
                finally:
                    print(f"{name}, attempt {attempt}: Cleanup...")

                if attempt < max_attempts:
                    print(f"{name}, attempt {attempt}: retrying in {attempts_delay}s")
                    await asyncio.sleep(attempts_delay)  # this could also be exponential backoff

            if last_error is None:
                raise AssertionError("Retry loop failed without catching retrayable errors")

            raise MaxAttemptsExceededError(name=name, attempts=max_attempts, last_error=last_error) from last_error

        return wrapper

    return actual_decorator


class SimpleServiceManager:
    runtime_error_chance: ClassVar[float] = 0.66

    @staticmethod
    @safe_service(my_timeout=3, max_attempts=3, attempts_delay=1, name="weather")
    async def service_weather() -> str:
        await asyncio.sleep(1)
        if random.random() < SimpleServiceManager.runtime_error_chance:
            raise RuntimeError("Weather service unavailable")
        return "Rainy"

    @staticmethod
    @safe_service(my_timeout=3, max_attempts=3, attempts_delay=1, name="news")
    async def service_news() -> list[str]:
        await asyncio.sleep(2)
        if random.random() < SimpleServiceManager.runtime_error_chance:
            raise RuntimeError("News service unavailable")
        return ["Hot news 1", "Hot news 2"]

    @staticmethod
    @safe_service(my_timeout=3, max_attempts=3, attempts_delay=1, name="currency")
    async def service_currency() -> float:
        await asyncio.sleep(1)
        if random.random() < SimpleServiceManager.runtime_error_chance:
            raise RuntimeError("Currency service unavailable")
        return 3.84

    @staticmethod
    @safe_service(my_timeout=3, max_attempts=3, attempts_delay=1, name="stock market")
    async def service_stock_market() -> int:
        await asyncio.sleep(4)
        if random.random() < SimpleServiceManager.runtime_error_chance:
            raise RuntimeError("Stock market service unavailable")
        return 0

    @staticmethod
    @safe_service(my_timeout=3, max_attempts=3, attempts_delay=1, name="traffic")
    async def service_traffic() -> list[int]:
        await asyncio.sleep(6)
        if random.random() < SimpleServiceManager.runtime_error_chance:
            raise RuntimeError("Traffic service unavailable")
        return [0, 1, 2]


# endregion


# region Example 7 - Semaphore


async def process_file(file_id: int, sem: asyncio.Semaphore) -> None:
    async with sem:
        print(f"Start processing file {file_id}")
        await asyncio.sleep(2)
        print(f"End processing file {file_id}")


# endregion


# region Example 8.1 - Queue 1 (workers working on a pre-made queue)


JOB_FAILURE_CHANCE = 0.5


async def process_job(job_id: int, job_time: float) -> None:
    print(f"Start processing job {job_id}")
    await asyncio.sleep(job_time)
    if random.random() < JOB_FAILURE_CHANCE:
        error_message = f"Job {job_id} failed"
        raise RuntimeError(error_message)
    print(f"End processing job {job_id}, it took {job_time:.2f}s")


async def worker_job(worker_id: int, queue: asyncio.Queue[tuple[int, float]]) -> None:
    while True:
        try:
            job_id, job_time = await queue.get()  # for each get() there must be the corresponding task_done()
            try:
                print(f"Worker {worker_id} starts processing job {job_id}, expected processing time is {job_time:.2f}s")
                await process_job(job_id, job_time)
                print(f"Worker {worker_id} finished processing job {job_id}")
            except RuntimeError as exc:
                print(f"Worker {worker_id} failed job {job_id}, message is '{exc!r}'")
            finally:
                queue.task_done()  # acknowledge every item removed, including failed jobs
        except asyncio.CancelledError:
            print(f"Worker {worker_id} is scheduled to cancellation")
            raise
        finally:
            print(f"Worker {worker_id} cleans up...")


# endregion


# region Example 8.2 - Queue 2 (producers + consumers)


type Total = Literal["total"]


class LockSharedState[T](NamedTuple):
    lock: asyncio.Lock
    shared_state: dict[Total, T]


async def job_producer(
    producer_id: int,
    queue: asyncio.Queue[tuple[int | None, float | None]],
    num_jobs: int,
    lss_job_ids: LockSharedState[int],
    lss_job_times: LockSharedState[float],
) -> None:
    for i in range(1, num_jobs + 1):
        print(f"Producer {producer_id} started producing its job number {i}")
        async with lss_job_ids.lock:
            new_job_id = lss_job_ids.shared_state["total"] + 1
            lss_job_ids.shared_state["total"] = new_job_id
        new_job_time = random.uniform(0.5, 2.0)
        async with lss_job_times.lock:
            lss_job_times.shared_state["total"] += new_job_time
        print(f"Producer {producer_id} finished producing its job number {i}")
        await queue.put((new_job_id, new_job_time))
        print(f"Producer {producer_id} put job {new_job_id} into the queue, job time is {new_job_time:.2f}s")
        if i < num_jobs:
            print(f"Producer {producer_id} is waiting for another job to produce")
            await asyncio.sleep(0.2)
    print(f"Producer {producer_id} produced all its jobs and quits")


async def job_consumer(consumer_id: int, queue: asyncio.Queue[tuple[int | None, float | None]]) -> None:
    while True:
        try:
            job_id, job_time = await queue.get()
            try:
                print(f"Consumer {consumer_id} starts working on job {job_id}, expected job time is {job_time:.2f}s")
                await process_job(job_id, job_time)  # type: ignore[]
                print(f"Consumer {consumer_id} finished working on job {job_id}")
            except RuntimeError as exc:
                print(f"Consumer {consumer_id} failed job {job_id}, message is '{exc!r}'")
            finally:
                queue.task_done()
        except asyncio.CancelledError:
            print(f"Consumer {consumer_id} is scheduled to cancellation")
            raise
        finally:
            print(f"Consumer {consumer_id} cleans up...")


# alternative version where instead of cancellation sentinel values are used to terminate the consumers
# async def job_consumer(consumer_id: int, queue: asyncio.Queue[tuple[int | None, float | None]]) -> None:
#     while True:
#         job_id, job_time = await queue.get()

#         try:
#             if job_id is None and job_time is None:
#                 print(f"Consumer {consumer_id} got a sentinel value, breaking...")
#                 break

#             print(f"Consumer {consumer_id} starts working on job {job_id}, expected job time is {job_time:.2f}s")
#             await process_job(job_id, job_time)  # type: ignore[]
#             print(f"Consumer {consumer_id} finished working on job {job_id}")
#         except RuntimeError as exc:
#             print(f"Consumer {consumer_id} failed job {job_id}, message is '{exc!r}'")
#         finally:
#             queue.task_done()


# endregion


# region Example 9 - async iterables and async iterators


async def async_logs_generator(total_logs: int) -> AsyncGenerator[dict[str, object]]:
    for i in range(1, total_logs + 1):
        await asyncio.sleep(random.uniform(0.05, 0.5))
        yield {"id": i, "temp": random.uniform(15.0, 35.0), "status": random.choice(["OK", "ERROR"])}


async def async_logs_error_filter(
    logs_generator: AsyncGenerator[dict[str, object]],
) -> AsyncGenerator[dict[str, object]]:
    # at every step of the loop Python implicitly performs await for the log
    # this way the loop advances only when the next log is ready
    # when the loop waits for the log, it gives the control back to the event loop
    async for log in logs_generator:
        if log["status"] == "ERROR":
            yield log


# endregion


# region Example 10 - async http requests (aiohttp)


class TodoPaginationParams(TypedDict):
    _page: int
    _limit: int


class Todo(TypedDict):
    user_id: int
    id: int
    title: str
    completed: bool


@dataclass(frozen=True)
class TodoFetchFailure:
    todo_id: int
    error: Exception


async def fetch_todo_1() -> None:
    async with (
        aiohttp.ClientSession() as session,
        session.get("https://jsonplaceholder.typicode.com/todos/1") as response,
    ):
        res = await response.json()
        print(f"Fetched: {res}")


async def fetch_todo_n(session: aiohttp.ClientSession, sem: asyncio.Semaphore, n: int) -> Todo:
    # context managers' inner workings:
    # - resemble stack data structure
    # - for example "async with A as a, B as b":
    # -- entering order: first A, then B
    # -- exiting order: first B, then A
    # therefore correct order is: sem before session in the context manager
    async with sem, session.get(f"https://jsonplaceholder.typicode.com/todos/{n}") as response:
        res: Todo = await response.json()
        return res


class TodoClient:
    BASE_URL: ClassVar[str] = "https://jsonplaceholder.typicode.com/todos"
    MAX_ATTEMPTS: ClassVar[int] = 3
    ERROR_CHANCE: ClassVar[float] = 0.5

    def __init__(self, concurrency: int = 10, timeout: int = 3) -> None:
        self.sem = asyncio.Semaphore(concurrency)
        self.timeout = aiohttp.ClientTimeout(total=timeout)
        self.session: aiohttp.ClientSession
        self.curr_fetch_many_tasks: list[asyncio.Task[Todo | TodoFetchFailure]]

    async def __aenter__(self) -> Self:
        self.session = aiohttp.ClientSession(timeout=self.timeout)
        return self

    async def __aexit__(
        self, exc_type: type[BaseException] | None, exc: BaseException | None, tb: TracebackType | None
    ) -> None:
        await self.session.close()

    async def fetch_todo_n(self, n: int) -> Todo:
        last_error: Exception | None = None

        for attempt in range(1, self.MAX_ATTEMPTS + 1):
            try:
                async with self.sem, self.session.get(f"{TodoClient.BASE_URL}/{n}") as response:
                    response.raise_for_status()  # checks for errors, instead of silently failing
                    res: Todo = await response.json()

                    # simulate some random errors to test the retry mechanism
                    if random.random() < TodoClient.ERROR_CHANCE:
                        raise aiohttp.ClientResponseError(
                            request_info=response.request_info,
                            history=response.history,
                            status=HTTPStatus.INTERNAL_SERVER_ERROR,
                            message="Simulated server error",
                        )

                    print(f"Todo {n}, attempt {attempt}: fetch completed")
                    return res
            except asyncio.CancelledError:
                raise
            except aiohttp.ClientResponseError as exc:
                if exc.status != HTTPStatus.TOO_MANY_REQUESTS and exc.status < HTTPStatus.INTERNAL_SERVER_ERROR:
                    raise
                last_error = exc
            except (aiohttp.ClientConnectionError, TimeoutError) as exc:
                last_error = exc

            if attempt < self.MAX_ATTEMPTS:
                delay = 2 ** (attempt - 1)
                print(f"Todo {n}, attempt {attempt}: retrying in {delay}s")
                await asyncio.sleep(delay)

        if last_error is None:
            raise AssertionError("Retry loop failed without catching retryable errors")

        raise MaxAttemptsExceededError(
            name=f"Todo {n}", attempts=self.MAX_ATTEMPTS, last_error=last_error
        ) from last_error

    async def fetch_many_todos(self, ns: list[int]) -> list[Todo | TodoFetchFailure | BaseException]:
        async def fetch_one_todo(n: int) -> Todo | TodoFetchFailure:
            try:
                return await self.fetch_todo_n(n)
            except (
                MaxAttemptsExceededError,
                TimeoutError,
                aiohttp.ClientConnectionError,
                aiohttp.ClientResponseError,
            ) as exc:
                return TodoFetchFailure(todo_id=n, error=exc)
            except asyncio.CancelledError:
                raise

        self.curr_fetch_many_tasks = [asyncio.create_task(fetch_one_todo(n)) for n in ns]

        task_to_cancel = random.choice(ns)
        print(f"Cancelling todo {task_to_cancel}...")
        loop = asyncio.get_running_loop()
        loop.call_later(0.1, self.curr_fetch_many_tasks[ns.index(task_to_cancel)].cancel)

        return await asyncio.gather(*self.curr_fetch_many_tasks, return_exceptions=True)

    async def fetch_todos_page(
        self, params: TodoPaginationParams, *, simulate_error: bool = False
    ) -> tuple[list[Todo], int | None]:
        last_error: Exception | None = None

        for attempt in range(1, self.MAX_ATTEMPTS + 1):
            try:
                async with self.session.get(
                    self.BASE_URL,
                    params={"_page": params["_page"], "_limit": params["_limit"]},
                ) as response:
                    response.raise_for_status()
                    todos: list[Todo] = await response.json()

                    if simulate_error and random.random() < self.ERROR_CHANCE:
                        raise aiohttp.ClientResponseError(
                            request_info=response.request_info,
                            history=response.history,
                            status=HTTPStatus.INTERNAL_SERVER_ERROR,
                            message="Simulated server error",
                        )

                    total_count = response.headers.get("X-Total-Count")
                    return todos, int(total_count) if total_count is not None else None
            except asyncio.CancelledError:
                raise
            except aiohttp.ClientResponseError as exc:
                if exc.status != HTTPStatus.TOO_MANY_REQUESTS and exc.status < HTTPStatus.INTERNAL_SERVER_ERROR:
                    raise
                last_error = exc
            except (aiohttp.ClientConnectionError, TimeoutError) as exc:
                last_error = exc

            if attempt < self.MAX_ATTEMPTS:
                delay = 2 ** (attempt - 1)
                print(f"Todo page {params['_page']}, attempt {attempt}: retrying in {delay}s")
                await asyncio.sleep(delay)

        if last_error is None:
            raise AssertionError("Retry loop failed without catching retryable errors")

        raise MaxAttemptsExceededError(
            name=f"Todo page {params['_page']}", attempts=self.MAX_ATTEMPTS, last_error=last_error
        ) from last_error

    async def fetch_all_todos(
        self, per_page: int
    ) -> AsyncGenerator[
        tuple[
            int,
            list[Todo]
            | list[
                MaxAttemptsExceededError | TimeoutError | aiohttp.ClientConnectionError | aiohttp.ClientResponseError
            ],
        ]
    ]:
        first_page_params: TodoPaginationParams = {"_page": 1, "_limit": 10}
        _, total_count = await self.fetch_todos_page(first_page_params)
        total_items = (
            total_count or 0
        )  # if total_count is truthy, return total_count, else provide fallback falsy value, i.e. 0, to not break math
        total_pages = math.ceil(total_items / per_page)
        print(f"fetch_all_todos: {total_items} total items to fetch, {total_pages} pages in total")

        for page in range(1, total_pages + 1):
            pagination_params: TodoPaginationParams = {"_page": page, "_limit": per_page}

            try:
                todos, _ = await self.fetch_todos_page(pagination_params, simulate_error=True)
            except asyncio.CancelledError:
                raise
            except (
                MaxAttemptsExceededError,
                TimeoutError,
                aiohttp.ClientConnectionError,
                aiohttp.ClientResponseError,
            ) as exc:
                yield page, [exc]
                continue

            yield page, todos


# endregion


async def amain() -> None:
    # ============ Example 0 - Introduction ============
    await hello()
    await countdown(3)

    # ============ Example 1 - Sequential ============
    # await worker("A", 2)  # gives control to the worker and pauses until it finishes
    # await worker("B", 1)  # doesn't schedule the task on the event loop

    # ============ Example 2 - Concurrent ============
    # start = time.perf_counter()
    # task_a = asyncio.create_task(worker("A", 2))  # change to bad_worker to see how it blocks the event loop thread
    # task_b = asyncio.create_task(worker("B", 1))  # immediately schedules the task concurrently on the event loop
    # print("Waiting for A and B")
    # await task_a  # pauses and gives control back to the event loop
    # await task_b  # event loop starts task_a but it also pauses and gives control back to the event loop so task_b can also be immediately started
    # print("Waiting done")
    # elapsed = time.perf_counter() - start
    # print(f"Elapsed time: {elapsed:.2f}s")

    # ============ Example 3.1 - Retrieving result from a task ============
    # square_1 = await calculate_square(1)
    # print(square_1)

    # ============ Example 3.2 - Retrieving results from a group of concurrent tasks (TaskGroup) ============
    # async with asyncio.TaskGroup() as tg:
    #     task_square_2 = tg.create_task(calculate_square(2))
    #     task_square_3 = tg.create_task(calculate_square(3))
    #     task_square_4 = tg.create_task(calculate_square(4))
    #     task_square_5 = tg.create_task(calculate_square(5))
    # print("Squares 2, 3, 4, 5 calculated")
    # print(task_square_2.result(), task_square_3.result(), task_square_4.result(), task_square_5.result())

    # ============ Example 3.3 - Retrieving results from a group of concurrent tasks (gather) ============
    # tasks = [asyncio.create_task(calculate_square(i)) for i in range(12, 16)]
    # results = await asyncio.gather(*tasks)
    # print("Squared 12, 13, 14, 15 calculated")
    # print(results)
    # fetch_tasks = [fetch_weather(), fetch_news(), fetch_currency()]
    # weather, news, currency = await asyncio.gather(*fetch_tasks, return_exceptions=True)
    # print(f"Weather: {weather}")
    # print(f"News: {news}")
    # print(f"EUR/PLN: {currency}")

    # ============ Example 4.1 - Handling slow, timed out services (case: sequential + unhandled exception) ============
    # timeout_ex_4_1 = 3
    # async with asyncio.timeout(timeout_ex_4_1):
    #     res = await bad_fetch_service("Service 1s", 1)
    #     print(res)
    # async with asyncio.timeout(timeout_ex_4_1):
    #     res = await bad_fetch_service("Service 2s", 2)
    #     print(res)
    # async with asyncio.timeout(timeout_ex_4_1):
    #     res = await bad_fetch_service("Service 5s", 5)
    #     print(res)

    # ============ Example 4.2 - Handling slow, timed out services (case: sequential + handled exception) ============
    # timeout_ex_4_2 = 3
    # try:
    #     async with asyncio.timeout(timeout_ex_4_2):
    #         res = await bad_fetch_service("Service 1s", 1)
    #         print(res)
    # except TimeoutError:
    #     print("Skipping Service 1s due to timeout")
    # try:
    #     async with asyncio.timeout(timeout_ex_4_2):
    #         res = await bad_fetch_service("Service 2s", 2)
    #         print(res)
    # except TimeoutError:
    #     print("Skipping Service 2s due to timeout")
    # try:
    #     async with asyncio.timeout(timeout_ex_4_2):
    #         res = await bad_fetch_service("Service 5s", 5)
    #         print(res)
    # except TimeoutError:
    #     print("Skipping Service 5s due to timeout")

    # ============ Example 4.3 - Handling slow, timed out services (case: proper way of doing this) ============
    # my_timeout = 3
    # good_fetch_tasks = [
    #     good_fetch_service("Service 1s", 1, my_timeout),
    #     good_fetch_service("Service 2s", 2, my_timeout),
    #     good_fetch_service("Service 5s", 5, my_timeout),
    # ]
    # fetch_1s, fetch_2s, fetch_5s = await asyncio.gather(*good_fetch_tasks)
    # print(fetch_1s)
    # print(fetch_2s)
    # print(fetch_5s)

    # ============ Example 5 - Task cancellation ============
    # cancellation != "immediate termination", it just sets a flag that the task should be cancelled at the next await point
    # long_task = asyncio.create_task(long_operation())
    # await asyncio.sleep(3)
    # print(long_task.cancel())
    # try:
    #     await long_task
    # except asyncio.CancelledError:
    #     print("Long task cancelled")

    # ============ Example 6 - More complicated example ============
    # print("====================================")

    # ss_names = ["weather", "news", "currency", "stock market", "traffic"]
    # ss_services = [
    #     SimpleServiceManager.service_weather(),
    #     SimpleServiceManager.service_news(),
    #     SimpleServiceManager.service_currency(),
    #     SimpleServiceManager.service_stock_market(),
    #     SimpleServiceManager.service_traffic(),
    # ]
    # ss_tasks = [asyncio.create_task(ss) for ss in ss_services]

    # loop = asyncio.get_running_loop()
    # ss_random_int = random.randint(0, len(ss_tasks) - 1)
    # print(f"Task to be cancelled: {ss_names[ss_random_int]}")
    # loop.call_later(5, ss_tasks[ss_random_int].cancel)

    # start = time.perf_counter()
    # ss_weather, ss_news, ss_currency, ss_stock_market, ss_traffic = await asyncio.gather(
    #     *ss_tasks, return_exceptions=True
    # )
    # elapsed = time.perf_counter() - start
    # # expected time = (my_timeout + attempts_delay) * (max_attempts - 1) + my_timeout = (3 + 1) * 2 + 3 ~ 11s
    # print("====================================")
    # print(f"Elapsed: {elapsed:.2f}s")
    # print("====================================")

    # ss_results = [ss_weather, ss_news, ss_currency, ss_stock_market, ss_traffic]

    # for name, result in zip(ss_names, ss_results, strict=True):
    #     if isinstance(result, ServiceSuccess):
    #         print(f"(SUCCESS) {name}: {result.value}, {result.attempts} attempts")
    #     elif isinstance(result, asyncio.CancelledError):
    #         print(f"(CANCELLED) {name}: {result!r}")
    #     elif isinstance(result, MaxAttemptsExceededError):
    #         print(f"(MAX ATTEMPTS FAILURE) {name}: {result!r}")
    #     else:
    #         print("This should never print")

    # print("====================================")

    # ============ Example 7 - Semaphore ============
    # sem = asyncio.Semaphore(3)
    # start = time.perf_counter()
    # async with asyncio.TaskGroup() as tg:
    #     file_tasks = [tg.create_task(process_file(i, sem)) for i in range(10)]
    # elapsed = time.perf_counter() - start
    # print(f"Elapsed: {elapsed:.2f}s")
    # for file_task in file_tasks:
    #     print(file_task.result())

    # ============ Example 8.1 - Queue 1 (workers working on a pre-made queue) ============

    # jobs = list(range(1, 21))
    # jobs_times = [random.uniform(0.5, 2.0) for _ in jobs]

    # # FIFO queue managed by one thread
    # # which constantly switches between tasks and yields (awaits)
    # # to see whether it can enqueue, dequeue or process an item in the queue
    # # this queue also stores _unfinished_tasks which can be used to mark when the work on the queue is done
    # queue_ex_8_1: asyncio.Queue[tuple[int, float]] = asyncio.Queue()

    # for job, job_time in zip(jobs, jobs_times, strict=True):
    #     # put_nowait (as well as get_nowait) is a normal function, not a coroutine
    #     # putting items increases _unfinished_tasks in the queue
    #     queue_ex_8_1.put_nowait((job, job_time))

    # # print(queue_ex_8_1.qsize())
    # # print(queue_ex_8_1.get_nowait())  # this returns job 1 because this is FIFO
    # # print(queue_ex_8_1.qsize())

    # num_workers = 4
    # jobs_tasks = [asyncio.create_task(worker_job(i, queue_ex_8_1)) for i in range(1, num_workers + 1)]

    # # wait for workers to finish all jobs in the queue
    # # this happens when _unfinished_tasks equals 0
    # start = time.perf_counter()
    # await queue_ex_8_1.join()
    # elapsed = time.perf_counter() - start
    # print(f"Elapsed: {elapsed:.2f}s\nExpected (naive): {sum(jobs_times):.2f}s")

    # # schedule the workers to cancellation
    # for job_task in jobs_tasks:
    #     job_task.cancel()

    # # hold until all workers are cancelled
    # jobs_cancellations = await asyncio.gather(*jobs_tasks, return_exceptions=True)
    # print(all(isinstance(res, asyncio.CancelledError) for res in jobs_cancellations))

    # ============ Example 8.2 - Queue 2 (producers + consumers) ============

    # test different cases, e.g. too slow producers or too slow consumers
    # note that in those cases the thread can become idle for pretty long times
    # it's best to find the balance so that the thread doesn't become idle for too long

    total_str: Total = "total"

    # used by producers to determine the id of a job based on the total number of dynamically generated jobs
    lock_job_ids = asyncio.Lock()
    shared_state_job_ids = {total_str: 0}

    # used to aggregate total job times as they are generated dynamically by producers
    lock_job_times = asyncio.Lock()

    # floats are immutable so passing floats to other functions creates a local copy
    # encapsulating a float with an object allows modyfying the float inside other functions
    shared_state_job_times = {total_str: 0.0}

    # prevent producers from putting too much work into the queue (backpressure threshold)
    queue: asyncio.Queue[tuple[int | None, float | None]] = asyncio.Queue(maxsize=5)

    num_producers = 4
    producer_tasks = [
        asyncio.create_task(
            job_producer(
                i,
                queue,
                5,
                LockSharedState(lock=lock_job_ids, shared_state=shared_state_job_ids),
                LockSharedState(lock=lock_job_times, shared_state=shared_state_job_times),
            )
        )
        for i in range(1, num_producers + 1)
    ]

    num_consumers = 3
    consumer_tasks = [asyncio.create_task(job_consumer(i, queue)) for i in range(1, num_consumers + 1)]

    # make sure you wait for the producers to finish producing all jobs
    # before waiting for all jobs to be done
    # otherwise queue might notify that all jobs have been done and quit while some producer is in the middle of creating another job
    await asyncio.gather(*producer_tasks)

    # even though you waited for the producers, the consumers weren't idle
    # they were working concurrently with the producers
    # but now, after all job is put into the queue, the consumers surely won't skip any remaining jobs
    await queue.join()

    for consumer_task in consumer_tasks:
        consumer_task.cancel()

    consumer_cancellations = await asyncio.gather(*consumer_tasks, return_exceptions=True)
    print(all(isinstance(res, asyncio.CancelledError) for res in consumer_cancellations))

    # alternative version where sentinel values are passed into the queue to terminate consumers
    # for _ in consumer_tasks:
    #     await queue.put((None, None))
    # await queue.join()
    # await asyncio.gather(*consumer_tasks)

    print(f"Total jobs: {shared_state_job_ids['total']}")
    print(f"Total expected jobs time (naive): {shared_state_job_times['total']:.2f}s")

    # ============ Example 9 - async iterables and async iterators ============

    # # 1. Get the async iterator
    # async_iter = async_iterable.__aiter__()

    # while True:
    #     try:
    #         # 2. Await the next item from __anext__()
    #         item = await async_iter.__anext__()
    #         print(item)
    #     except StopAsyncIteration:
    #         # 3. Stop when StopAsyncIteration is raised
    #         break

    # num_error_logs = 0
    # async for error_log in async_logs_error_filter(async_logs_generator(20)):
    #     print(error_log)
    #     num_error_logs += 1
    # print(f"Number of error logs: {num_error_logs}")
    # print([log["temp"] async for log in async_logs_generator(10)])

    # ============ Example 10 - async http requests (aiohttp) ============

    # print("fetch_todo_1:")
    # await fetch_todo_1()

    # print("fetch_todo_n:")
    # start = time.perf_counter()
    # todo_sem = asyncio.Semaphore(10)
    # async with aiohttp.ClientSession() as session, asyncio.TaskGroup() as tg:
    #     todo_tasks = [tg.create_task(fetch_todo_n(session, todo_sem, n)) for n in range(1, 101)]
    # for task in todo_tasks:
    #     print(task.result())
    # elapsed = time.perf_counter() - start
    # print(f"Elapsed: {elapsed:.2f}s")

    # print("TodoClient:")

    # async with TodoClient(concurrency=10, timeout=3) as tc:
    #     try:
    #         todo_69 = await tc.fetch_todo_n(69)
    #         print(todo_69)
    #     except (
    #         MaxAttemptsExceededError,
    #         TimeoutError,
    #         aiohttp.ClientConnectionError,
    #         aiohttp.ClientResponseError,
    #     ) as exc:
    #         print(f"Failed to fetch todo 69: {exc}")
    #     except asyncio.CancelledError:
    #         print("Fetching todo 69 was cancelled")

    #     todos_1_68 = await tc.fetch_many_todos(list(range(1, 69)))
    #     for todo in todos_1_68:
    #         if isinstance(todo, TodoFetchFailure):
    #             print(f"Failed to fetch todo {todo.todo_id}: {todo.error}")
    #         elif isinstance(todo, asyncio.CancelledError):
    #             print(f"Fetching this todo has been cancelled: {todo!r}")
    #         else:
    #             print(f"Fetched todo: {todo}")

    #     print("Fetching all todos...")

    #     # current_main_task = asyncio.current_task()
    #     # if current_main_task is not None:
    #     #     asyncio.get_running_loop().call_later(8, current_main_task.cancel)

    #     try:
    #         async for page, todos in tc.fetch_all_todos(12):
    #             if len(todos) == 1 and isinstance(
    #                 todos[0],
    #                 (
    #                     MaxAttemptsExceededError,
    #                     TimeoutError,
    #                     aiohttp.ClientConnectionError,
    #                     aiohttp.ClientResponseError,
    #                 ),
    #             ):
    #                 print(f"Todos on page {page} could not be retrieved: {todos!r}")
    #             else:
    #                 print(f"Todos on page {page}:")
    #                 for todo in todos:
    #                     print(todo)
    #     except asyncio.CancelledError:
    #         print("Fetching all todos cancelled")


def main() -> None:
    asyncio.run(amain())


if __name__ == "__main__":
    main()
