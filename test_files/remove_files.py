from constants import OUTPUT_FILE, OUTPUT_DIR
import os

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

    for x in os.listdir(OUTPUT_DIR):
        file, ext = os.path.splitext(x)
        if file not in file_list:
            os.remove(os.path.join(OUTPUT_DIR, x))


remove_invalid_files()