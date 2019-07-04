import os
from datetime import datetime
import Utilities.Mail as mail
import zipfile

try:
    import zlib
    compression = zipfile.ZIP_DEFLATED
except:
    compression = zipfile.ZIP_STORED

def create_folder(directory,log_dir = "./"):
    if not os.path.exists(directory):
        os.makedirs(directory)
        write_log_file("Create folder "+directory,log_dir)

def write_log_file(log_msg,log_dir = "./"):  
    logfile = open(log_dir + "backup.log","a+")
    logfile.write(get_hour_now() + "- " + log_msg +"\n")
    logfile.close()

def get_hour_now():
    return "["+str(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))+"]"

def compact_file(bkp_fullpath,log_dir = "./"):
    write_log_file("Start Compact file: " + bkp_fullpath, log_dir)
    zf = zipfile.ZipFile(bkp_fullpath.replace('.bak','.zip'), mode='w')
    if os.path.isfile(bkp_fullpath):
        try:
            zf.write(bkp_fullpath, compress_type=compression)
        except:
            write_log_file("Falha ao compactar " + bkp_fullpath,log_dir)
            mail.send_logs("Falha ao Compactar o Backup! Favor Verificar!",log_dir + "backup.log")
            exit()
        finally:
            write_log_file("Ended Compact file: " + bkp_fullpath,log_dir)
            zf.close()
      #delete the file
        write_log_file("Deleting "+bkp_fullpath,log_dir)
        os.remove(bkp_fullpath)
    else:
        write_log_file("File " + bkp_fullpath + " not exists",log_dir)
        mail.send_logs("Arquivo de Backup Não Encontrado! Favor Verificar!",log_dir + "backup.log")
