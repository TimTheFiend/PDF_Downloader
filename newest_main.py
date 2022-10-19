#!/usr/bin/env python3
import os
import time
from datetime import datetime
from multiprocessing.pool import ThreadPool

import pandas as pd
import PyPDF2
import requests

from constants import *

ID_COL = None
URL_COL = None
URL_BACKUP = None

ALREADY_DOWNLOADED = None

def main() -> None:
    validate_file_paths()
    initialise_columns()
    get_pdfs_in_output()

    #Time related
    s = time.perf_counter()
    print(f"{datetime.now().strftime('%H:%M:%S')}\tStarting...")

    # STARTS DOWNLOADING
    process_get_pdf()

    #Time related
    elapsed = time.perf_counter() - s
    print(f"{datetime.now().strftime('%H:%M:%S')}\tExecuted in {elapsed / 60:0.2f}min.")


def validate_file_paths() -> None:
    """Kinda very much unneccessary I feel."""
    if not os.path.exists(EXCEL_FILEPATH):
        raise Exception("`constants\\EXCEL_FILEPATH` does not exist.")
    if not os.path.splitext(EXCEL_FILEPATH)[1].lower() == ".xlsx":
        raise Exception("`constants\\EXCEL_FILEPATH` is not an Excel-file (.xlsx).")
    if not os.path.exists(OUTPUT_DIR):
        raise Exception("`constants\\OUTPUT_DIR` does not exist.")


#region Initialise global variables
def initialise_columns() -> None:
    """Reads the input-file, and loads in the necessary columns into global variables."""
    print(f"{datetime.now().strftime('%H:%M:%S')}\tLoading spreadsheet.")
    sheet = pd.ExcelFile(EXCEL_FILEPATH).parse(0)

    global ID_COL
    ID_COL = sheet[ID_COL_NAME]
    global URL_COL
    URL_COL = sheet[URL_COL_NAME]
    global URL_BACKUP
    URL_BACKUP = sheet[URL_BACKUP_COL_NAME]

    print(f"{datetime.now().strftime('%H:%M:%S')}\tFinished loading spreadsheet.")


def get_pdfs_in_output() -> None:
    """Sets `ALREADY_DOWNLOADED` as a global variable, and sets it value to be the contents of `OUTPUT_DIR`"""
    global ALREADY_DOWNLOADED
    ALREADY_DOWNLOADED = os.listdir(OUTPUT_DIR)
#endregion Initialise global variables


#region ThreadPool & Thread function
def process_get_pdf():
    """In charge of threads. After all threads are finished, it prints an .xlsx based on the results of `get_pdf`."""
    results = []
    #region Threads
    pool = ThreadPool(processes=NUMBER_OF_THREADS)
    for i in range(ID_COL.size):
        if f"{ID_COL[i]}.pdf" in ALREADY_DOWNLOADED:
            continue
        results.append(pool.apply_async(get_pdf, (ID_COL[i], URL_COL[i], URL_BACKUP[i])))

    pool.close()
    pool.join()
    #endregion Threads

    #region Printing to Excel
    id_col = []
    is_dwn_col = []
    for r in results:
        _id, _dwn = r.get()
        id_col.append(_id)
        is_dwn_col.append(_dwn)

    df = pd.DataFrame({RESULT_EXCEL_ID_COL_NAME: id_col, RESULT_EXCEL_DOWNLOAD_COL_NAME: is_dwn_col})
    df.to_excel(FILE_STATUS_EXCEL_FILEPATH, sheet_name=FILE_STATUS_EXCEL_SHEETNAME, index=False)
    #endregion Printing to Excel

    cleanup_output_dir(id_col=id_col, is_dwn=is_dwn_col)


def get_pdf(id : str, url_1st : str, url_2nd : str) -> list[str, bool]:
    # Return True if the file is already downloaded.
    # if f"{id}.pdf" in ALREADY_DOWNLOADED:
    #     return [id, True]

    for url in [url_1st, url_2nd]:
        # Check (superficially) if string is a valid URL
        if not str(url).lower().startswith('http'):
            continue

        try:
            # Attempt to reach the PDF
            pdf = requests.get(url=url, allow_redirects=True, timeout=TIMEOUT_REQUEST_MAX)
            pdf.raise_for_status()

            if pdf.status_code == 200:
                file_path = os.path.join(OUTPUT_DIR, f"{id}.pdf")
                open(file_path, 'wb').write(pdf.content)
                # Try and read the file as a PDF, if it fails it goes into except.
                PyPDF2.PdfFileReader(open(file_path, 'rb'), strict=False)
                return [id, True]
        except:
            continue

    #Failed to download
    return [id, False]
#endregion ThreadPool & Thread function


def cleanup_output_dir(id_col : list[str], is_dwn : list[bool]) -> None:
    """Based on the content of the result.xlsx, removes the files that are in `OUTPUT_DIR` that aren't noted as downloaded."""
    files_in_output = os.listdir(OUTPUT_DIR)
    for i in range(len(id_col)):
        if is_dwn[i] == False and f"{id_col[i]}.pdf" in files_in_output:
            os.remove(os.path.join(OUTPUT_DIR, f"{id_col[i]}.pdf"))


if __name__ == "__main__":
    main()
