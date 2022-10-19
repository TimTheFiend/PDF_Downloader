from os.path import join as join_path

# FILE/DIRECTORY INFORMATION
EXCEL_FILEPATH = r'C:\repos\PDF_Downloader\_files\GRI_2017_2020 (1).xlsx'
OUTPUT_DIR = r'C:\repos\PDF_Downloader\output_dir'
FILE_STATUS_EXCEL_FILEPATH = 'results.xlsx'
FILE_STATUS_EXCEL_SHEETNAME = '0'

# SPREADSHEET -> COLUMN INFORMATION
ID_COL_NAME = 'BRnum'
URL_COL_NAME = 'Pdf_URL'
URL_BACKUP_COL_NAME = 'Report Html Address'

# SETTINGS
NUMBER_OF_THREADS = 10
TIMEOUT_REQUEST_MAX = 0.25


# DEBUG VALUES
CLEAN_OUTPUT = False
DOWNLOAD_FILES = True
IN_PROGRESS = True
SKIP_IF_IN_RESULT_REPORT = True
CAP_TOTAL_AMOUNT_OF_ROWS = 1
OUTPUT_FILE_FAIL = "report_Failure.txt"
OUTPUT_FILE_SUCCESS = join_path(OUTPUT_DIR, "report_Success.txt")