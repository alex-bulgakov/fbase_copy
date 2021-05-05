import os
import pathlib
import shutil
from datetime import datetime, timedelta


def remove(path):
    try:
        if os.path.isdir(path):
            shutil.rmtree(path)
        else:
            os.remove(path)
    except:
        pass



path = "backup"
check_date = datetime.today() - timedelta(days=10)
for i in os.listdir(path):
    try:
        fname = pathlib.Path(path + '/' + i)
        file_date = datetime.fromtimestamp(fname.stat().st_mtime)
        if file_date < check_date:
            print('REMOVE: ' + str(file_date) + ' ' + i)
            remove(fname)
    except FileNotFoundError:
        print("can't find file " + i)

