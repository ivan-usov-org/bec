from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import TimeoutError as CFTimeoutError


# pylint: disable=too-few-public-methods
class SingletonThreadpool:
    """Singleton class for handling threadpools: Instantiating a new class instance
    is indempotent and will return the already existing class. However, the number of
    workers can be increased by instantiating a new class instance.

    >>> pool = SingleThreadpool(max_workers=100)
    # number of max_workers of pool == 100
    >>> pool2 = SingletonThreadpool(max_workers=110)
    # number of max_workers pool and pool2 == 110
    """

    DEFAULT_MAX_WORKER = 100

    def __init__(self, max_workers=DEFAULT_MAX_WORKER) -> None:
        if not hasattr(self, "_initialized"):
            self._initialized = True
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
            fcn_future = threadpool.executor.submit(fcn, *args, **kwargs)
            try:
                return fcn_future.result(timeout=timeout_time)
            except CFTimeoutError as error:
                raise TimeoutError from error

        return wrapper

    return Inner
