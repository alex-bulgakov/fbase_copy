import os
from datetime import datetime
import ftplib
import zipfile
from ftplib import FTP
import shutil

log_list = []

def _get_files(ftp, dirname):
    try:
        ftp.cwd(dirname)
        for i in ftp.mlsd():
            handle = open(i[0], 'wb')
            ftp.retrbinary('RETR %s' % i[0], handle.write)
            handle.close()
        ftp.cwd('/')
    except ftplib.error_perm:
        log("can't copy " + dirname)


def get_dirnames_from_file(filename):
    result = []
    raw_list = open(filename, 'r').readlines()
    for i in raw_list:
        result.append(i.rstrip('\n'))
    return result


def _gen_dir_name():
    return datetime.today().strftime("%Y%m%d_%H%M%S")


def init_ftp(address, login, password, debug_lvl):
    ftp = FTP(address, login, password)
    ftp.set_debuglevel(debug_lvl)
    return ftp


def _zipdir(path, ziph):
    # ziph is zipfile handle
    for root, dirs, files in os.walk(path):
        for file in files:
            ziph.write(os.path.join(root, file),
                       os.path.relpath(os.path.join(root, file),
                                       os.path.join(path, '..')))


def zipdir(path, ziph):
    # ziph is zipfile handle
    for root, dirs, files in os.walk(path):
        for file in files:
            ziph.write(os.path.join(root, file),
                       os.path.relpath(os.path.join(root, file),
                                       os.path.join(path, '..')))


def _send_to_ftp(address, login, password, filename):
    ftp = FTP(address, login, password)
    ftp.set_debuglevel(1)
    file = open(filename, 'rb')
    ftp.storbinary('STOR ' + filename, file)
    ftp.close()


def make_copy(ftp, dirnames):
    log('=' * 100)
    log('start copy ' + datetime.today().strftime("%Y-%m-%d_%H:%M:%S"))
    folder_name = _gen_dir_name()
    os.mkdir(folder_name)
    os.chdir(folder_name)
    for i in dirnames:
        os.mkdir(i)
        os.chdir(i)
        _get_files(ftp, i)
        os.chdir('../')
    os.chdir('../')
    zipf = zipfile.ZipFile(folder_name + '.zip', 'w', zipfile.ZIP_DEFLATED)
    _zipdir(folder_name, zipf)
    zipf.close()
    shutil.rmtree(folder_name)
    _send_to_ftp('mrb2005.beget.tech', 'mrb2005_backup', 'A7DwQk%*', folder_name + '.zip')




def log(text):
    with open('/log.txt', 'a') as log_file:
        log_file.write(text + '\n')
    log_file.close()

