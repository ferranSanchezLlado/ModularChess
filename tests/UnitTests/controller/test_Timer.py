import time
import unittest
from datetime import timedelta

from ModularChess.controller.Timer import Timer
from ModularChess.utils.Exceptions import TimerError


class TestTimer(unittest.TestCase):

    def setUp(self):
        def end_call():
            self.finished = True

        self.end_call = end_call
        self.time = timedelta(seconds=1)
        self.increment = timedelta(milliseconds=1)
        self.finished = False
        self.timer = Timer(self.time, self.increment, self.end_call)

    def test_not_started(self):
        self.assertEqual(self.time, self.timer.remaining_time())
        self.assertEqual(timedelta(seconds=0), self.timer.elapsed_time())
        self.assertFalse(self.timer.has_started())
        self.assertFalse(self.timer.has_finished())
        self.assertFalse(self.timer.has_stopped())
        self.assertFalse(self.finished)

    def test_started(self):
        self.timer.start()
        time.sleep(0.01)

        self.assertGreater(self.time, self.timer.remaining_time())
        self.assertLess(timedelta(seconds=0), self.timer.elapsed_time())
        self.assertTrue(self.timer.has_started())
        self.assertFalse(self.timer.has_finished())
        self.assertFalse(self.timer.has_stopped())
        self.assertFalse(self.finished)

        self.timer.stop()

    def test_started_and_stopped(self):
        self.timer.start()
        time.sleep(0.01)
        self.timer.stop()

        self.assertGreater(self.time, self.timer.remaining_time())
        self.assertLess(timedelta(seconds=0), self.timer.elapsed_time())
        self.assertTrue(self.timer.has_started())
        self.assertFalse(self.timer.has_finished())
        self.assertTrue(self.timer.has_stopped())
        self.assertFalse(self.finished)

    def test_finished(self):
        self.timer.start()
        time.sleep(1.25 * self.time.total_seconds())

        self.assertEqual(timedelta(seconds=0), self.timer.remaining_time())
        self.assertEqual(self.time.seconds, self.timer.elapsed_time().seconds)  # Precision error in finish time
        self.assertTrue(self.timer.has_started())
        self.assertTrue(self.timer.has_finished())
        self.assertTrue(self.timer.has_stopped())
        self.assertTrue(self.finished)

    def test_increment(self):
        self.timer.start()
        self.timer.add_increment()
        time.sleep(1.25 * self.time.total_seconds())

        self.assertEqual(timedelta(seconds=0), self.timer.remaining_time())
        self.assertEqual(self.time.seconds, self.timer.elapsed_time().seconds)  # Precision error in finish time
        self.assertTrue(self.timer.has_started())
        self.assertTrue(self.timer.has_finished())
        self.assertTrue(self.timer.has_stopped())
        self.assertTrue(self.finished)

    def test_increment_stop(self):
        self.timer.start()
        self.timer.add_increment()
        self.timer.stop()

        self.assertEqual(self.time + self.increment, self.timer.remaining_time() + self.timer.elapsed_time())
        self.assertTrue(self.timer.has_started())
        self.assertFalse(self.timer.has_finished())
        self.assertTrue(self.timer.has_stopped())
        self.assertFalse(self.finished)

    def test_move(self):
        self.timer.start()
        self.timer.move()

        self.assertEqual(self.time + self.increment, self.timer.remaining_time() + self.timer.elapsed_time())
        self.assertTrue(self.timer.has_started())
        self.assertFalse(self.timer.has_finished())
        self.assertTrue(self.timer.has_stopped())
        self.assertFalse(self.finished)

    def test_exceptions(self):
        self.assertRaises(TimerError, self.timer.add_increment)
        self.assertRaises(TimerError, self.timer.stop)
        self.assertRaises(TimerError, self.timer.resume)

        self.timer.start()
        self.assertRaises(TimerError, self.timer.resume)

    def test_resume(self):
        self.timer.start()
        self.timer.stop()
        self.timer.resume()
        time.sleep(1.25 * self.time.total_seconds())

        self.assertEqual(timedelta(seconds=0), self.timer.remaining_time())
        self.assertEqual(self.time.seconds, self.timer.elapsed_time().seconds)  # Precision error in finish time
        self.assertTrue(self.timer.has_started())
        self.assertTrue(self.timer.has_finished())
        self.assertTrue(self.timer.has_stopped())
        self.assertTrue(self.finished)

    def test_str(self):
        hours, minutes, seconds = int(self.timer.remaining_time().total_seconds() // 3600), \
                                  int(self.timer.remaining_time().total_seconds() // 60 % 60), \
                                  self.timer.remaining_time().total_seconds() % 60

        self.assertEqual(f"{hours}:{minutes:02d}:{seconds:05.2f}s", str(self.timer))


if __name__ == '__main__':
    unittest.main()
