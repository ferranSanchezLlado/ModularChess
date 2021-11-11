import datetime
import threading
from itertools import zip_longest
from typing import Callable, Any, Optional, List

from ModularChess.utils.Exceptions import TimerError


class Timer:

    def __init__(self, time_control: datetime.timedelta, increment: datetime.timedelta, end_call: Callable[..., Any],
                 *args, **kwargs):
        def extend_end_call():
            self.finish_time.append(datetime.datetime.now())
            end_call(*args, **kwargs)

        self.time_control = time_control
        self.increment = increment
        self.end_call = extend_end_call
        self.stopped = False

        self.start_time: List[datetime.datetime] = []
        self.expected_finish_time: List[datetime.datetime] = []
        self.timer: Optional[threading.Timer] = None
        self.finish_time: List[datetime.datetime] = []  # Time when timer was stopped or ended

    def start(self) -> None:
        if self.has_started():
            self.stop()
        self.start_time = [datetime.datetime.now()]
        self.expected_finish_time = [self.start_time[0] + self.time_control]

        self.timer = threading.Timer(self.time_control.total_seconds(), self.end_call)
        self.timer.start()

    def add_increment(self) -> None:
        if not self.has_started():
            raise TimerError("Not Started")
        elif not self.has_stopped():
            assert self.timer is not None
            self.timer.cancel()
            self.expected_finish_time[-1] += self.increment

            self.timer = threading.Timer(self.remaining_time().total_seconds(), self.end_call)
            self.timer.start()

    def move(self) -> None:
        if not self.has_started():
            raise TimerError("Not Started")
        elif not self.has_stopped():
            assert self.timer is not None
            self.timer.cancel()
            self.expected_finish_time[-1] += self.increment
            self.finish_time.append(datetime.datetime.now())
            self.stopped = True

    def stop(self) -> None:
        if not self.has_started():
            raise TimerError("Not Started")
        elif not self.has_stopped():
            assert self.timer is not None
            self.timer.cancel()
            self.finish_time.append(datetime.datetime.now())
            self.stopped = True

    def resume(self) -> None:
        if not self.has_started():
            raise TimerError("Not Started")
        if not self.stopped:
            raise TimerError("Not Stopped")
        remaining_time = self.remaining_time()

        self.start_time.append(datetime.datetime.now())
        self.expected_finish_time.append(self.start_time[-1] + remaining_time)

        self.timer = threading.Timer(remaining_time.total_seconds(), self.end_call)
        self.timer.start()
        self.stopped = False

    def has_finished(self) -> bool:
        return self.has_stopped() and not self.stopped

    def has_stopped(self) -> bool:
        return self.has_started() and len(self.finish_time) == len(self.start_time)

    def has_started(self) -> bool:
        return self.timer is not None and len(self.start_time) > 0 and len(self.expected_finish_time) > 0

    def elapsed_time(self) -> datetime.timedelta:
        if not self.has_started():
            return datetime.timedelta()

        return sum(((finish_time or datetime.datetime.now()) - start_time
                    for start_time, finish_time in zip_longest(self.start_time, self.finish_time, fillvalue=None)),
                   datetime.timedelta())

    def remaining_time(self) -> datetime.timedelta:
        if not self.has_started():
            return self.time_control
        if self.has_finished():
            return datetime.timedelta(seconds=0)

        return self.expected_finish_time[-1] - (self.finish_time[-1] if self.has_stopped() else datetime.datetime.now())

    def __str__(self) -> str:
        hours, minutes, seconds = int(self.remaining_time().total_seconds() // 3600), \
                                  int(self.remaining_time().total_seconds() // 60 % 60), \
                                  self.remaining_time().total_seconds() % 60
        return f"{hours}:{minutes:02d}:{seconds:05.2f}s"
