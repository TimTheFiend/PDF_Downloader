import asyncio
import time
from datetime import datetime
import sys

import requests as req
import pandas as pd

from constants import *

ID_COL = None
URL_COL = None
URL_BACKUP = None
SUCCESS_LIST = []
FAILED_LIST = []


async def get_names(start: int, end: int, _id: int):
    output_file = open(f"output{_id}.txt", 'w')

    for i in range(start, end):
        url = str(URL_COL[i])
        id = ID_COL[i]

        if url.lower().startswith('http') == False:
            #fail
            output_file.write(
                f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ({i})- fail\n")
            continue

        try:
            pdf = req.get(url=url, allow_redirects=False, timeout=0.5, )
            if pdf.status_code == 200:
                #succ
                output_file.write(
                    f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ({i})- succ\n")
                continue
            else:
                #fail
                output_file.write(
                    f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ({i})- fail\n")
                continue
        except:
            pass
        output_file.write(
            f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ({i})- fail\n")
        #fail
    output_file.close()


async def main() -> None:
    sheet = pd.ExcelFile(EXCEL_FILEPATH).parse(0)
    print("EXCEL HAS BEEN LOADED")
    # Columns
    global ID_COL
    global URL_COL
    global URL_BACKUP
    ID_COL = sheet[ID_COL_NAME]
    URL_COL = sheet[URL_COL_NAME]
    URL_BACKUP = sheet[URL_BACKUP_COL_NAME]

    global SUCCESS_LIST
    global FAILED_LIST

    assert type(ID_COL) == pd.core.series.Series
    assert type(URL_COL) == pd.core.series.Series
    assert type(URL_BACKUP) == pd.core.series.Series

    await asyncio.gather(get_names(0, 19, 1), get_names(20, 39, 2), get_names(40, 59, 3))

    for x in SUCCESS_LIST:
        print(x)
    for x in FAILED_LIST:
        print("\t" + x)


if __name__ == "__main__":
    s = time.perf_counter()

    asyncio.run(main())
    elapsed = time.perf_counter() - s

    print(f"Executed in {elapsed:0.2f} seconds")
