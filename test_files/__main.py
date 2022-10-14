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

MAX_ROWS = None
ROWS_DONE = None

def remove_invalid_files():
    file_list = []
    with open(OUTPUT_FILE_SUCCESS, 'r') as myfile:
        while True:
            line = myfile.readline()[:-1]

            if line == "":
                break
            if line == "\n":
                continue
            file_list.append(line)

    for x in os.listdir(OUTPUT_DIR):
        file, ext = os.path.splitext(x)
        if file not in file_list:
            os.remove(os.path.join(OUTPUT_DIR, x))


def check_if_skip(id: str) -> bool:
    return f"{id}.pdf" in os.listdir(OUTPUT_DIR)



def report_success(id : str, file_name : str) -> None:
    def success():
        with open(OUTPUT_FILE_SUCCESS, 'a') as myfile:
            myfile.write(id + "\n")

    try:
        PyPDF2.PdfFileReader(open(file_name, 'rb'), strict=False)
        success()
    except:
        #Not sure this does anything.
        report_failure(id)
        os.remove(file_name)
        return

def report_failure(id : str) -> None:
    with open(OUTPUT_FILE_FAIL, 'a') as myfile:
        myfile.write(f"\t{id} \n")


def initialise_columns():
    print(f"{datetime.now().strftime('%H:%M:%S')}\tLoading spreadsheet.")
    sheet = pd.ExcelFile(EXCEL_FILEPATH).parse(0)

    # Columns
    global ID_COL
    global URL_COL
    global URL_BACKUP

    ID_COL = sheet[ID_COL_NAME]
    URL_COL = sheet[URL_COL_NAME]
    URL_BACKUP = sheet[URL_BACKUP_COL_NAME]

    global MAX_ROWS
    MAX_ROWS = int(ID_COL.size)
    print(f"{datetime.now().strftime('%H:%M:%S')}\tFinished loading spreadsheet.")


def get_pdf(row_id: int) -> None:
    def is_not_url(url_str: str) -> bool:
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
                report_success(id, file_name)

    url = str(URL_COL[row_id])
    url_backup = str(URL_BACKUP[row_id])
    id = ID_COL[row_id]

    if check_if_skip(id):
        return

    for _url in [url, url_backup]:
        if is_not_url(_url):
            return
        pdf = requests.get(url=_url, allow_redirects=True,
                        timeout=TIMEOUT_REQUEST_MAX)
        pdf.raise_for_status()

        # attempt_status = False
        if pdf.status_code == 200:
            on_success(pdf)
            return



def process_get_pdf():
    pool = ThreadPool(processes=NUMBER_OF_THREADS)
    # _tasks = []
    # for index, row in enumerate(ID_COL):
    #     _tasks.append(pool.apply_async(get_pdf, args=(row, URL_COL[index], URL_BACKUP[index], )))

    for i in range(MAX_ROWS):
        pool.apply_async(get_pdf, (i, ))

    pool.close()
    pool.join()

def clean_output() -> None:
    for x in os.listdir(OUTPUT_DIR):
        os.remove(os.path.join(OUTPUT_DIR, x))

def create_result_files():
    if not len(os.listdir(OUTPUT_DIR)) > 0:
        foo = open(OUTPUT_FILE_SUCCESS, 'w')
        foo.close()
    _output = open(OUTPUT_FILE_FAIL, 'w')
    _output.close()


def main():
    create_result_files()

    initialise_columns()
    if CLEAN_OUTPUT:
        clean_output()

    s = time.perf_counter()
    print(f"{datetime.now().strftime('%H:%M:%S')}\tEstimated time: {(((MAX_ROWS / NUMBER_OF_THREADS) * TIMEOUT_REQUEST_MAX) / 60):0.2f}min")

    process_get_pdf()

    elapsed = time.perf_counter() - s
    print(f"{datetime.now().strftime('%H:%M:%S')}\tExecuted in {elapsed / 60:0.2f}min.")

    remove_invalid_files()



if __name__ == "__main__":
    main()