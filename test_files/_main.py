import os
from datetime import datetime
import threading
import time
import sys

import requests as req
import PyPDF2
import pandas as pd

import remove_files
from constants import *

ID_COL = None
URL_COL = None
URL_BACKUP = None
DONE = False


def on_start_up():
    _output = open(OUTPUT_FILE, 'w')
    _output.close()

    if CLEAN_OUTPUT:
        clean_output()


def report_result(id : str, file_name : str) -> None:
    def success():
        with open(OUTPUT_FILE, 'a') as myfile:
            myfile.write(id + "\n")
    try:
        PyPDF2.PdfFileReader(open(file_name, 'rb'), strict=False)
        success()
    except:
        os.remove(file_name)
        return

def loading_animation():
    import itertools

    for c in itertools.cycle(['|', '/', '-', '\\']):
        if DONE:
            break
        sys.stdout.write('\rloading ' + c)
        sys.stdout.flush()
        time.sleep(0.1)
    sys.stdout.write('\rDone!     ')


def get_names(_start: int, _end: int, _id: int):
    def is_not_url(url_str : str) -> bool:
        return not url_str.lower().startswith('http')

    def on_success(pdf) -> None:
        if DOWNLOAD_FILES:
            file_name = os.path.join(OUTPUT_DIR, f"{id}.pdf")
            try:
                open(file_name, 'wb').write(pdf.content)
            except:
                os.remove(file_name)
                return
            finally:
                report_result(id, file_name)

    midway_point = int((_end - _start) / 2) + _start

    for i in range(_start, _end):
        if i == midway_point:
            print(f"{_id} halfway there")
            sys.stdout.flush()

        url = str(URL_COL[i])
        url_backup = str(URL_BACKUP[i])
        id = ID_COL[i]

        # Check if valid URL address.
        for item in [url, url_backup]:
            if is_not_url(item):
                continue
            try:
                pdf = req.get(url=url, allow_redirects=True, timeout=TIMEOUT_REQUEST_MAX, stream=True)
                pdf.raise_for_status()
                if pdf.status_code == 200:
                    on_success(pdf)
                    break
            except:
                pass




def main():
    #loading
    loading = threading.Thread(target=loading_animation)
    loading.start()

    sheet = pd.ExcelFile(EXCEL_FILEPATH).parse(0)
    print("EXCEL HAS BEEN LOADED")

    s = time.perf_counter()
    # Columns
    global ID_COL
    global URL_COL
    global URL_BACKUP
    global DONE
    ID_COL = sheet[ID_COL_NAME]
    URL_COL = sheet[URL_COL_NAME]
    URL_BACKUP = sheet[URL_BACKUP_COL_NAME]

    assert type(ID_COL) == pd.core.series.Series
    assert type(URL_COL) == pd.core.series.Series
    assert type(URL_BACKUP) == pd.core.series.Series


    total_row_count = int(ID_COL.size / CAP_TOTAL_AMOUNT_OF_ROWS)
    amount = int(total_row_count / NUMBER_OF_THREADS)

    # print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Estimated time: {(((total_row_count / NUMBER_OF_THREADS) * TIMEOUT_REQUEST_MAX) / 60) * 2.5:0.2f}min")

    threads = []

    for x in range(NUMBER_OF_THREADS):
        start_value = x * amount
        end_value = amount * (x + 1)
        if x == NUMBER_OF_THREADS - 1:
            end_value += 1

        t = threading.Thread(
            target=get_names,
            name=f"T{x + 1}",
            args=(start_value, end_value, x,))
        threads.append(t)

    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()

    elapsed = time.perf_counter() - s
    DONE = True
    print(f"Executed in {elapsed / 60:0.2f}min.")


def clean_output() -> None:
    for x in os.listdir(OUTPUT_DIR):
        os.remove(os.path.join(OUTPUT_DIR, x))


if __name__ == "__main__":
    on_start_up()
    print(f"START:\t{datetime.now().strftime('%H:%M:%S')}")
    # print(f"START:\t{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    main()
    remove_files.remove_invalid_files()
    print(f"END:\t{datetime.now().strftime('%H:%M:%S')}")
    # print(f"END:\t{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
