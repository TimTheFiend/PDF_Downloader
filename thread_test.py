from concurrent.futures import process, thread
from pickle import FALSE
import threading
from time import time as process_time, sleep as time_sleep
import itertools
import sys

from constants import IN_PROGRESS

IN_PROGRESS : bool


def loading_thread():
    for c in itertools.cycle(['|', '/', '-', '\\']):
        if IN_PROGRESS == False:
            break
        sys.stdout.write('\rloading ' + c)
        sys.stdout.flush()
        time_sleep(0.1)
    sys.stdout.write('\rDone!     ')


def foobar(sleep : float):
    start_time = process_time()
    print("START TIME: " + str(sleep) + "s")
    time_sleep(sleep)
    print(f"Time{sleep} - {process_time() - start_time}")




def main() -> None:
    global IN_PROGRESS

    start_time = process_time()
    t1 = threading.Thread(target=foobar, args=(8.5,))
    t2 = threading.Thread(target=foobar, args=(2.5,))
    t3 = threading.Thread(target=foobar, args=(3.5,))
    threads = [t1, t2, t3]

    loading = threading.Thread(target=loading_thread)
    loading.start()
    # print("START THREADS")
    for thread in threads:
        thread.start()

    # print("JOIN THREADS")
    for thread in threads:
        thread.join()
    IN_PROGRESS = False

    # print("FUNCTION END")

    # print(f"TOTAL TIME: {process_time() - start_time}")


if __name__ == "__main__":
    main()