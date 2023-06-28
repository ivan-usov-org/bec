import ctypes
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


def timeout(timeout_time: float):
    """Decorator to raise a TimeoutError if the decorated function does
    not finish within the specified time.

    Args:
        timeout_time (float): Timeout time in seconds.

    Raises:
        TimeoutError: Raised if the elapsed time > timeout

    """
    threadpool = SingletonThreadpool(max_workers=50)

    def Inner(fcn):
        def wrapper(*args, **kwargs):
            try:
                fcn_future = threadpool.executor.submit(fcn, *args, **kwargs)
                return fcn_future.result(timeout=timeout_time)
            finally:
                if fcn_future.running():
                    fcn_future.cancel()

        return wrapper

    return Inner


set_async_exc = ctypes.pythonapi.PyThreadState_SetAsyncExc


def killthread(thread, exc=KeyboardInterrupt):
    if not thread.is_alive():
        return

    ident = ctypes.c_long(thread.ident)
    exc = ctypes.py_object(exc)

    res = set_async_exc(ident, exc)
    if res == 0:
        raise ValueError(f"thread {thread} does not exist")
    elif res > 1:
        # if return value is greater than one, you are in trouble.
        # you should call it again with exc=NULL to revert the effect.
        set_async_exc(ident, None)
        raise SystemError(
            f"PyThreadState_SetAsyncExc on thread {thread} failed with return value {res}"
        )
