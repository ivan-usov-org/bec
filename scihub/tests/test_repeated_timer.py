import time

import pytest

from scihub.repeated_timer import RepeatedTimer


class Counter:
    def __init__(self):
        self.count = 0

    def increment(self):
        self.count += 1


@pytest.fixture
def counter():
    return Counter()


@pytest.fixture
def timer(counter):
    return RepeatedTimer(0.1, counter.increment)


def test_start_and_stop(timer, counter):
    timer.start()
    time.sleep(2)
    timer.stop()
    assert counter.count == 19
