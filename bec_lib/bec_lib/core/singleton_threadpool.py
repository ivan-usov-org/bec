import asyncio
import ctypes
import functools
import threading
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import TimeoutError as CFTimeoutError
from typing import Callable


# pylint: disable=too-few-public-methods
class SingletonThreadpool:
    """Singleton class for handling threadpools: Instantiating a new class instance
    is idempotent and will return the already existing class. However, the number of
    workers can be increased by instantiating a new class instance.

    >>> pool = SingleThreadpool(max_workers=100)
    # number of max_workers of pool == 100
    >>> pool2 = SingletonThreadpool(max_workers=110)
    # number of max_workers pool and pool2 == 110
    """

    DEFAULT_MAX_WORKER = 100
    executor = None

    def __init__(self, max_workers=DEFAULT_MAX_WORKER) -> None:
        if self.executor is None:
            self.executor = ThreadPoolExecutor(max_workers=max_workers)
        if max_workers > self.executor._max_workers:
            self.executor._max_workers = max_workers

    def __new__(cls, max_workers=DEFAULT_MAX_WORKER):
        if not hasattr(cls, "_threadpool"):
            cls._threadpool = super(SingletonThreadpool, cls).__new__(cls)
        return cls._threadpool


def run_with_timeout(timeout_time: float):
    """Decorator to run a function in a while loop and
    raise a TimeoutError if the decorated function does
    not finish within the specified time. It is done by using
    asyncio. The decorated function must be a coroutine.

    Args:
        timeout_time (float): Timeout time in seconds.

    Raises:
        TimeoutError: Raised if the elapsed time > timeout

    """

    def decorator(func: Callable):
        # check if the function is a coroutine
        if not asyncio.iscoroutinefunction(func):
            raise TypeError("Function must be a coroutine.")

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # get the event loop and create a new one if there is none
            try:
                loop = asyncio.get_event_loop()
            except RuntimeError:
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
            # create a future and run the coroutine
            try:
                future = asyncio.run_coroutine_threadsafe(func(*args, **kwargs), loop)
                # get the result of the coroutine
                result = future.result(timeout=timeout_time)
                return result
            except asyncio.TimeoutError:
                raise TimeoutError(
                    f"Function {func.__name__} did not finish within {timeout_time} seconds."
                )

        return wrapper

    return decorator
