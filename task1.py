import sys
import os
import re
import time
import shutil

try:
    localPath = sys.argv[1]
except IndexError:
    localPath = os.getcwd()
Files = [[ele, time.gmtime(os.path.getmtime(ele))] for ele in os.listdir(localPath) if (not (re.match('(.*).py', ele) or re.match('\.(.*)', ele)) and os.path.isfile(localPath + '/' + ele))]
i = 0
for file in Files:
    fileName = file[0]
    newFilePath = localPath + '/' + time.strftime('%Y', file[1]) + '/' + time.strftime('%m', file[1]) + '/'
    os.makedirs(newFilePath, mode=0o755, exist_ok=True)
    shutil.copy2(localPath + '/' + fileName, newFilePath + fileName)
    i += 1
print(str(i) + ' files copied')
