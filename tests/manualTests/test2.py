import time
from datetime import timedelta

from ModularChess.controller.Timer import Timer


def print_timer(extra, local_timer: Timer):
    print(f"[{str(extra)}] str: {str(local_timer)} | Remaining Time: {local_timer.remaining_time()} | Elapsed Time: \
    {local_timer.elapsed_time()}")


def end_call():
    global func_is_called
    print("------------ END ------------")
    func_is_called = True


def test2():
    timer = Timer(timedelta(minutes=3), timedelta(seconds=1), end_call)
    timer.start()

    i = 0
    while not timer.has_finished():
        timer.add_increment()
        print_timer(i := i + 1, timer)
        time.sleep(5)

        if i % 20 == 0:
            timer.stop()
            print_timer("STOPPED", timer)
            time.sleep(10)
            timer.resume()
            print_timer("RESUMED", timer)
    print_timer("END", timer)
    assert func_is_called


if __name__ == "__main__":
    func_is_called = False
    test2()
