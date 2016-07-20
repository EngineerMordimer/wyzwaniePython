import sys
import os
import re
import time
import shutil
import collections


def is_proper_file(ele, path ):
    """This method test element if
    1. it is NOT a element with '.py' at end of name
    2. it is NOT a element with '.' at start of name
    3. ele is a file in path
    """
    return not (re.match('(.*).py', ele) or re.match('\.(.*)', ele)) and os.path.isfile(path + '/' + ele)


def get_modification_time(ele):
    """Return modification time of file in
        (tm_year, tm_mon, tm_mday, tm_hour, tm_min, tm_sec, tm_wday, tm_yday, tm_isdst)"""
    return time.gmtime(os.path.getmtime(ele))


localPath = sys.argv[1] if len(sys.argv) > 1 else os.getcwd()
FileElements = collections.namedtuple('FileElements', 'fileName modDate')
files = [FileElements(ele, get_modification_time(ele)) for ele in os.listdir(localPath) if is_proper_file(ele, localPath)]
for file in files:
    fileName = file.fileName
    yearMod, monthMod = time.strftime('%Y', file.modDate), time.strftime('%m', file.modDate)
    newFileDirectory = '{localPath}/{yearMod}/{monthMod}/'.format(**vars())
    newFilePath = '{newFileDirectory}/{fileName}'.format(**vars())
    oldFilePath = '{localPath}/{fileName}'.format(**vars())
    os.makedirs(newFileDirectory, mode=0o755, exist_ok=True)
    shutil.copy2(oldFilePath, newFilePath)

print(len(files), ' files copied')
