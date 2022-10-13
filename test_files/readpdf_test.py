import PyPDF2

PDF_FAIL = r"C:\repos\PDF_Downloader\output_dir\BR50155.pdf"
PDF_SUCC = r"C:\repos\PDF_Downloader\output_dir\BR50408.pdf"

def main():
    try:
        # PyPDF2.PdfFileReader(open(PDF_SUCC, 'rb'), strict=False)
        PyPDF2.PdfFileReader(open(PDF_FAIL, 'rb'), strict=False)
        print("lmao")
    except:
        print("lol")


if __name__ == "__main__":
    main()