import os
import time
import threading

from constants import *


import requests
import pandas as pd



# FILE_PATH = r'C:\repos\PDF_Downloader\_files\GRI_2017_2020 (1).xlsx'
# OUTPUT_PATH = r'C:\repos\PDF_Downloader\output_dir'

# ID_COL_NAME = 'BRnum'
# URL_COL_NAME = 'Pdf_URL'
# URL_BACKUP_COL_NAME = 'Report Html Address'

ID_COL = None
URL_COL = None
URL_BACKUP = None
RESULTS = dict[bool, list[str]]



def get_pdfs(start : int, end : int) -> None:
    for i in range(start, end):
        URL = URL_COL[i]
        if type(URL) != str:
            continue
        if str(URL).lower().startswith('http') == False:
            continue

        pdf = requests.get(url=URL, allow_redirects=True)
        # pdf = requests.get(url_col[i], allow_redirects=True)
        if pdf.status_code == 200:
            RESULTS[True].append(ID_COL[i])
            continue
            open(os.path.join(OUTPUT_PATH, f"{ID_COL[i]}.pdf"), 'wb').write(pdf.content)
        RESULTS[False].append(ID_COL[i])


def _get_pdfs(start : int, end = int) -> None:
    for i in range(start, end):
        URL = URL_COL[i]
        if type(URL) != str:
            continue
        if str(URL).lower().startswith('http') == False:
            continue

        pdf = requests.get(url=URL, allow_redirects=True)
        # pdf = requests.get(url_col[i], allow_redirects=True)
        if pdf.status_code == 200:
            open(os.path.join(OUTPUT_PATH, f"{ID_COL[i]}.pdf"), 'wb').write(pdf.content)



def main() -> None:
    sheet = pd.ExcelFile(FILE_PATH).parse(0)
    # Columns
    global ID_COL
    global URL_COL
    global URL_BACKUP
    ID_COL = sheet[ID_COL_NAME]
    URL_COL = sheet[URL_COL_NAME]
    URL_BACKUP = sheet[URL_BACKUP_COL_NAME]
    # Dictionary
    global RESULTS
    RESULTS[True] = []
    RESULTS[False] = []


    #Test we got data
    assert type(ID_COL) == pd.core.series.Series
    assert type(URL_COL) == pd.core.series.Series
    assert type(URL_BACKUP) == pd.core.series.Series

    t1 = threading.Thread(target=get_pdfs, args=(0, 19,))
    t2 = threading.Thread(target=get_pdfs, args=(20, 39,))

    t1.start()
    t2.start()

    t1.join()
    t2.join()

    for succ in RESULTS[True]:
        print(succ)

    for fail in RESULTS[False]:
        print("\t" + succ)



def pandas_main() -> None:
    print("Time starts now!")
    tim = time.process_time()

    xls = pd.ExcelFile(FILE_PATH)
    sheet = xls.parse(0)
    print(f"Excel loaded:\t{time.process_time() - tim}")

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
            open(os.path.join(OUTPUT_PATH, f"{id_col[i]}.pdf"), 'wb').write(pdf.content)
            print(f"print {i + 1}:\t{time.process_time() - tim}")




def clean_output() -> None:
    for x in os.listdir(OUTPUT_PATH):
        # print(os.path.join(OUTPUT_PATH, x))
        os.remove(os.path.join(OUTPUT_PATH, x))
        # os.remove(x)



if __name__ == "__main__":
    clean_output()
    main()

# # Overwrites existing text
# # w = Write
# output_file = open("hello.txt", "w")
# output_file.writelines("I thought what I'd do was, I'd pretend to be one of those deaf-mutes.\n\t- J. D. Salinger\n\n")

# lines_to_write = [
#     "Veni, vidi, vici",
#     "\nI came",
#     "\nI saw",
#     "\nI conquered"
# ]
# output_file.writelines(lines_to_write)

# output_file.close()

# # a = Appends
# output_file = open("hello.txt", "a")
# output_file.writelines("\n\t- Some Dork")
# output_file.close()