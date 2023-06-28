import concurrent
import time

import pytest
from bec_lib.core.timeout import SingletonThreadpool, timeout


@pytest.mark.parametrize("timeout_time,sleep_time", [(0.1, 0.5), (0.5, 0.1), (None, 0.1)])
def test_timeout(timeout_time, sleep_time):
    @timeout(timeout_time)
    def run_dummy(val):
        time.sleep(val)

    if timeout_time is not None and timeout_time < sleep_time:
        with pytest.raises(concurrent.futures.TimeoutError):
            run_dummy(sleep_time)
    else:
        run_dummy(sleep_time)


def test_singleton_threadpool():
    threadpool = SingletonThreadpool()
    assert threadpool.executor._max_workers == SingletonThreadpool.DEFAULT_MAX_WORKER
    executor_id = id(threadpool.executor)
    new_threadpool = SingletonThreadpool()
    assert threadpool.executor._max_workers == SingletonThreadpool.DEFAULT_MAX_WORKER
    assert executor_id == id(new_threadpool.executor)
    new_threadpool = SingletonThreadpool(max_workers=SingletonThreadpool.DEFAULT_MAX_WORKER + 10)
    assert threadpool.executor._max_workers == SingletonThreadpool.DEFAULT_MAX_WORKER + 10
