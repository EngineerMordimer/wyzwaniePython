import sys
import os
import re
import time
import shutil


def is_proper_file(ele, path ):
    """This method test element if
    1. it is NOT a element with '.py' at end of name
    2. it is NOT a element with '.' at start of name
    3. ele is a file in path
    """
    if not (re.match('(.*).py', ele) or re.match('\.(.*)', ele)) and os.path.isfile(path + '/' + ele):
        return 1
    else:
        return None
try:
    localPath = sys.argv[1]
except IndexError:
    localPath = os.getcwd()
files = [[ele, time.gmtime(os.path.getmtime(ele))] for ele in os.listdir(localPath) if is_proper_file(ele, localPath)]
for file in files:
    fileName = file[0]
    yearMod = time.strftime('%Y', file[1])
    monthMod = time.strftime('%m', file[1])
    newFileDirectory = '{localPath}/{year}/{month}/'.format(localPath=localPath, year=yearMod, month=monthMod)
    newFilePath = '{newFileDirectory}/{fileName}'.format(newFileDirectory=newFileDirectory, fileName=fileName)
    oldFilePath = '{localPath}/{fileName}'.format(localPath=localPath, fileName=fileName)
    os.makedirs(newFileDirectory, mode=0o755, exist_ok=True)
    shutil.copy2(oldFilePath, newFilePath)

print(str(len(files)) + ' files copied')
