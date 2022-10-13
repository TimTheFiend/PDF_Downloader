from datetime import datetime
from multiprocessing.pool import ThreadPool
import time
import os

from constants import *

import requests
import PyPDF2
import pandas as pd


ID_COL = None
URL_COL = None
URL_BACKUP = None


def remove_invalid_files():
    file_list = []
    with open(OUTPUT_FILE, 'r') as myfile:
        while True:
            line = myfile.readline()[:-1]
            if line == "":
                break
            if line == "\n":
                continue
            file_list.append(line)

    for x in os.listdir(OUTPUT_PATH):
        file, ext = os.path.splitext(x)
        if file not in file_list:
            os.remove(os.path.join(OUTPUT_PATH, x))


def report_result(id : str, file_name : str) -> None:
    def success():
        with open(OUTPUT_FILE, 'a') as myfile:
            myfile.write(id + "\n")
    def failure():
        with open(OUTPUT_FILE, 'a') as myfile:
            myfile.write(f"\t{id} \n")

    try:
        PyPDF2.PdfFileReader(open(file_name, 'rb'), strict=False)
        success()
    except:
        os.remove(file_name)
        return


def get_pdf(row_id: int) -> None:
    def is_not_url(url_str : str) -> bool:
        return not url_str.lower().startswith('http')

    def on_success(pdf) -> None:
        if DOWNLOAD_FILES:
            file_name = os.path.join(OUTPUT_PATH, f"{id}.pdf")
            try:
                open(file_name, 'wb').write(pdf.content)
            except:
                os.remove(file_name)
                return
            finally:
                report_result(id, file_name)


    url = str(URL_COL[row_id])
    url_backup = str(URL_BACKUP[row_id])
    id = ID_COL[row_id]


    if is_not_url(url):
        return
    pdf = requests.get(url=url, allow_redirects=True, timeout=TIMEOUT_REQUEST_MAX)
    pdf.raise_for_status()

    # attempt_status = False
    if pdf.status_code == 200:
        on_success(pdf)


def process_get_pdf(row_count : int) -> None:
    pool = ThreadPool(processes=NUMBER_OF_THREADS)
    results = []
    for row in range(row_count):
        results.append(pool.apply_async(get_pdf, (row, )))

    pool.close()
    pool.join()


def main():
    sheet = pd.ExcelFile(FILE_PATH).parse(0)
    print(f"{datetime.now().strftime('%H:%M:%S')}\tEXCEL HAS BEEN LOADED")

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
    print(total_row_count)
    # print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{datetime.now().strftime('%H:%M:%S')}\tEstimated time: {(((total_row_count / NUMBER_OF_THREADS) * TIMEOUT_REQUEST_MAX) / 60) * 2.5:0.2f}min")

    process_get_pdf(total_row_count)
    elapsed = time.perf_counter() - s
    print(f"{datetime.now().strftime('%H:%M:%S')}\tExecuted in {elapsed / 60:0.2f}min.")


if __name__ == "__main__":
    _output = open(OUTPUT_FILE, 'w')
    _output.close()
    main()
    remove_invalid_files()