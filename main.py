#!/usr/bin/env python3
import os
import time
from datetime import datetime
from multiprocessing.pool import ThreadPool
from urllib.error import HTTPError

import pandas as pd
import PyPDF2
import requests

from constants import *

"""Columns from the spreadsheet"""
ID_COL = None
URL_COL = None
URL_BACKUP = None

FILES_IN_OUTPUT_DIR = None

TEMP_LIST = None

def main():
    create_result_files()
    initialise_columns()
    #Time related
    s = time.perf_counter()
    print(f"{datetime.now().strftime('%H:%M:%S')}\tEstimated time: {(((MAX_ROWS / NUMBER_OF_THREADS) * TIMEOUT_REQUEST_MAX) / 60):0.2f}min")

    # STARTS DOWNLOADING
    process_get_pdf()

    #Time related
    elapsed = time.perf_counter() - s
    print(f"{datetime.now().strftime('%H:%M:%S')}\tExecuted in {elapsed / 60:0.2f}min.")
    #Cleanup
    remove_invalid_files()
    write_to_excel()


###
def report_success(id: str, file_name: str) -> None:
    def success():
        with open(OUTPUT_FILE_SUCCESS, 'a') as myfile:
            myfile.write(id + "\n")

    try:
        PyPDF2.PdfFileReader(open(file_name, 'rb'), strict=False)
        success()
        TEMP_LIST.append(id)
        return
    except:
        os.remove(file_name)


def get_files_in_output():
    return os.listdir(OUTPUT_DIR)

def initialise_columns():
    global TEMP_LIST
    TEMP_LIST = []


    print(f"{datetime.now().strftime('%H:%M:%S')}\tLoading spreadsheet.")
    sheet = pd.ExcelFile(EXCEL_FILEPATH).parse(0)

    #region Global Variables
    global ID_COL
    global URL_COL
    global URL_BACKUP

    ID_COL = sheet[ID_COL_NAME]
    URL_COL = sheet[URL_COL_NAME]
    URL_BACKUP = sheet[URL_BACKUP_COL_NAME]

    global MAX_ROWS
    MAX_ROWS = int(ID_COL.size)

    global FILES_IN_OUTPUT_DIR
    FILES_IN_OUTPUT_DIR = get_files_in_output()
    # FILES_IN_OUTPUT = os.listdir(OUTPUT_PATH)
    #endregion Global Variables

    print(f"{datetime.now().strftime('%H:%M:%S')}\tFinished loading spreadsheet.")


def get_pdf(id : str, url_primary : str, url_secondary : str) -> None:
    #region Internal functions
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

    def check_if_skip(id: str) -> bool:
        return f"{id}.pdf" in FILES_IN_OUTPUT_DIR
    #endregion Internal functions


    if check_if_skip(id):
        return

    for url in [url_primary, url_secondary]:
        if is_not_url(url):
            continue
        try:
            pdf = requests.get(url=url, allow_redirects=True, timeout=TIMEOUT_REQUEST_MAX)
            pdf.raise_for_status()

            # attempt_status = False
            if pdf.status_code == 200:
                on_success(pdf)
                return
        except HTTPError:
            return




def process_get_pdf():
    pool = ThreadPool(processes=NUMBER_OF_THREADS)
    for i in range(ID_COL.size):
        pool.apply_async(get_pdf, (ID_COL[i], URL_COL[i], URL_BACKUP[i], ))

    pool.close()
    pool.join()


#Create .txt-files that contains the result of the
def create_result_files():
    global TEMP_LIST
    TEMP_LIST = os.listdir(OUTPUT_DIR)



    #If there are no files in ´output_dir´ then create a new ´report_Success.txt´
    if not len(os.listdir(OUTPUT_DIR)) > 0:
        foo = open(OUTPUT_FILE_SUCCESS, 'w')
        foo.close()


# Removes files that aren't actually PDF.
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
        # file, ext = os.path.splitext(x)
        file = os.path.splitext(x)[0]
        if file not in file_list:
            os.remove(os.path.join(OUTPUT_DIR, x))

def write_to_excel():
    FILES_IN_OUTPUT = get_files_in_output()
    id_list = []
    is_downloaded_list = []
    for id in ID_COL:
        is_download = False
        if f"{id}.pdf" in FILES_IN_OUTPUT:
            is_download = True
        id_list.append(id)
        is_downloaded_list.append(is_download)

    df = pd.DataFrame({'ID': id_list, 'Is downloaded': is_downloaded_list})
    df.to_excel(FILE_STATUS_EXCEL_FILEPATH, sheet_name=FILE_STATUS_EXCEL_SHEETNAME, index=False)


if __name__ == "__main__":
    main()
    print()
    for x in TEMP_LIST:
        if not str(x).startswith('B'):
            print(str(x))
    print()
    # initialise_columns()
    # write_to_excel()
