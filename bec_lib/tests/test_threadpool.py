from bec_lib.core.singleton_threadpool import SingletonThreadpool


def test_singleton_threadpool():
    threadpool = SingletonThreadpool()
    assert threadpool.executor._max_workers == SingletonThreadpool.DEFAULT_MAX_WORKER
    executor_id = id(threadpool.executor)
    new_threadpool = SingletonThreadpool()
    assert threadpool.executor._max_workers == SingletonThreadpool.DEFAULT_MAX_WORKER
    assert executor_id == id(new_threadpool.executor)
    new_threadpool = SingletonThreadpool(max_workers=SingletonThreadpool.DEFAULT_MAX_WORKER + 10)
    assert threadpool.executor._max_workers == SingletonThreadpool.DEFAULT_MAX_WORKER + 10
