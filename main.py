#!/usr/bin/env	python3
from lib import *

FTP_ADDR = '192.168.1.50'
LOGIN = 'esp'
PASSW = 'esp'
DEBUG_LVL = 1
FOLDER_NAME = 'backup'
FILE_NAME = 'folders_list'

folders_list = get_dirnames_from_file(FILE_NAME)


if not os.path.exists(FOLDER_NAME):
    os.mkdir(FOLDER_NAME)
    os.chdir(FOLDER_NAME)
else:
    os.chdir(FOLDER_NAME)

ftp1 = init_ftp(FTP_ADDR, LOGIN, PASSW, DEBUG_LVL)
make_copy(ftp1, folders_list)
