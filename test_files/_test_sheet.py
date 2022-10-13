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


def initialise_columns():
    print(f"{datetime.now().strftime('%H:%M:%S')}\tLoading spreadsheet.")
    sheet = pd.ExcelFile(FILE_PATH).parse(0)

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


def main():
    initialise_columns()
    for i in ID_COL:
        print(i)


if __name__ == "__main__":
    main()