import os
import threading
import time
import queue

from constants import *

import pandas as pd
import requests


ID_COL = None
URL_COL = None
URL_BACKUP = None


def pandas_main() -> None:
    xls = pd.ExcelFile(EXCEL_FILEPATH)
    sheet = xls.parse(0)

    id_col = sheet[ID_COL_NAME]
    url_col = sheet[URL_COL_NAME]
    url_backup = sheet[URL_BACKUP_COL_NAME]



    for i in range(20):
        URL = url_col[i]
        if str(URL).lower().startswith('http') == False:
            continue

        pdf = requests.get(url=URL, allow_redirects=True)
        # pdf = requests.get(url_col[i], allow_redirects=True)
        if pdf.status_code == 200:
            open(os.path.join(OUTPUT_DIR, f"{id_col[i]}.pdf"), 'wb').write(pdf.content)
