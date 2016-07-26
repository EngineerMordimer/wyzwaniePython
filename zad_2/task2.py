# -*- coding: utf-8 -*-
import sys
import os


def get_extension(file):
    """
    Return extension o file (to 5 charts). If extension is longer, last char is *.
    """
    extension = os.path.splitext(file)[1][1:]
    if len(extension) <= 5:
        return extension[:5]
    else:
        return extension[:4] + '*'


def get_size(file, path):
    """
    Return size of file in path
    """
    return os.stat(path + "/" + file).st_size


def scan_dir(path, main_data):
    """
    Scan directory for data about files, if search dir, execute recursive this method.
    Return list of data (extension, sum of size, count) and count of all files.
    """
    for element in os.listdir(path):
        # print("path: " + path + ", element: " + element)
        if os.path.isfile(path + "/" + element):
            main_data["count_files"] += 1
            file = next((file for file in main_data["list"] if file["extension"] == get_extension(element)), None)
            if file:
                file["count"] += 1
                file["size"] += get_size(element, path)
            else:
                main_data["list"].append({"extension": get_extension(element), "count": 1, "size": get_size(element, path)})
        else:
            new_path = path + "/" + element
            main_data = scan_dir(new_path, main_data)
    return main_data


localPath = (sys.argv[1] if len(sys.argv) > 1 else os.getcwd())
listData = []
mainData = {"list": listData, "count_files": 0}
mainData = scan_dir(localPath, mainData)
mainData["list"] = sorted(mainData["list"], key=lambda k: k["count"], reverse=True)
allElements = mainData["count_files"]
writeFile = ''
if len(sys.argv) > 2:
    print("Saving file: " + sys.argv[2])
    writeFile = open(sys.argv[2], 'w+')
    writeFile.write("#####***************%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%\n")
else:
    print("#####***************%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
for fileType in mainData["list"]:
    histogram = '#' * round((50 * (fileType["count"] / allElements)))
    text = fileType["extension"].rjust(5, ' ') + (str(fileType["size"]) + 'B').rjust(15, ' ') + histogram.rjust(60, ' ')
    if len(sys.argv) > 2:
        writeFile.write(text + '\n')
    else:
        print(text)
