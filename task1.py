import os
import re
import time
import shutil

print('START')
localPath = os.getcwd()
Files = [[ele, time.gmtime(os.path.getmtime(ele))] for ele in os.listdir(localPath) if (not (re.match('(.*).py', ele) or re.match('\.(.*)', ele)) and os.path.isfile(localPath + '/' + ele))]
i = 0
for file in Files:
    fileName = file[0]
    newFilePath = localPath + '/' + time.strftime('%Y', file[1]) + '/' + time.strftime('%m', file[1]) + '/'
    i += 1
    try:
        original_umask = os.umask(0)
        os.makedirs(newFilePath, mode=0o777, exist_ok=True)
    finally:
        os.umask(original_umask)
    shutil.copy2(localPath + '/' + fileName, newFilePath + fileName)
print(str(i) + ' files copied')
