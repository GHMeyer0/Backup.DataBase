import os
from datetime import datetime
import utilities.notification as mail
import zipfile

try:
    import zlib
    compression = zipfile.ZIP_DEFLATED
except:
    compression = zipfile.ZIP_STORED

def create_folder(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)
        write_log_file("Create folder "+ directory,directory)

def write_log_file(log_message,directory):  
    logfile = open(directory + "log.txt","a+")
    logfile.write(get_hour_now() + "- " + log_message +"\n")
    logfile.close()

def get_hour_now():
    return "["+str(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))+"]"

def compact_file(backup_directory, backup_filename):
    write_log_file("Start Compact file: " + backup_directory + backup_filename, backup_directory)
    zf = zipfile.ZipFile(backup_directory + backup_filename.replace('.bak','.zip'), mode='w')
    if os.path.isfile(backup_directory + backup_filename):
        try:
            zf.write(backup_directory + backup_filename, compress_type=compression)
        except:
            write_log_file("Falha ao compactar " + backup_directory + backup_filename, backup_directory)
            mail.send_logs("Falha ao Compactar o Backup! Favor Verificar!", backup_directory + "log.txt")
            exit()
        finally:
            write_log_file("Ended Compact file: " + backup_directory + backup_filename, backup_directory)
            zf.close()
        #delete the file
        try:
            write_log_file("Deleting " + backup_directory + backup_filename, backup_directory)
            os.remove(backup_directory + backup_filename)
        except:
            write_log_file("Fail to Delete " + backup_directory + backup_filename, backup_directory)
        finally:
            write_log_file(backup_directory + backup_filename + "Deleted", backup_directory)
    else:
        write_log_file("File " + backup_directory + " not exists", backup_directory)
        mail.send_logs("Arquivo de Backup Não Encontrado! Favor Verificar!",backup_directory + "backup.log")
