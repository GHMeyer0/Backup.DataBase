import os
from datetime import datetime
import time
import utilities.notification as mail
import zipfile

try:
    import zlib
    compression = zipfile.ZIP_DEFLATED
except:
    compression = zipfile.ZIP_STORED


def deletar_backups_antigos(directory, dias_reter_backup):
    tempo_em_segundos = time.time() - (dias_reter_backup * 24 * 60 * 60)
    for root, dirs, files in os.walk(directory, topdown=False):
        for file_ in files:
            full_path = os.path.join(root, file_)
            stat = os.stat(full_path)

            if stat.st_mtime <= tempo_em_segundos:
                os.remove(full_path)
        if not os.listdir(root):
            os.remove(root)
def create_folder(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)
def write_log_file(log_message,directory, arquivo_log):  
    logfile = open(directory + arquivo_log + ".txt","a+")
    logfile.write(get_hour_now() + "- " + log_message +"\n")
    logfile.close()

def get_hour_now():
    return "["+str(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))+"]"

def compact_file(backup_directory, backup_filename, database):
    write_log_file("Start Compact file: " + backup_directory + backup_filename, backup_directory,database)
    zf = zipfile.ZipFile(backup_directory + backup_filename.replace('.bak','.zip'), mode='w')
    if os.path.isfile(backup_directory + backup_filename):
        try:
            zf.write(backup_directory + backup_filename, compress_type=compression)
        except:
            write_log_file("Falha ao compactar " + backup_directory + backup_filename, backup_directory, database)
            mail.send_logs("Falha ao Compactar o Backup! Favor Verificar!", backup_directory + database +".txt")
            exit()
        finally:
            write_log_file("Ended Compact file: " + backup_directory + backup_filename, backup_directory,database)
            zf.close()
        #delete the file
        try:
            write_log_file("Deleting " + backup_directory + backup_filename, backup_directory, database)
            os.remove(backup_directory + backup_filename)
        except:
            write_log_file("Fail to Delete " + backup_directory + backup_filename, backup_directory, database)
        finally:
            write_log_file(backup_directory + backup_filename + "Deleted", backup_directory, database)
    else:
        write_log_file("File " + backup_directory + " not exists", backup_directory,database)
        mail.send_logs("Arquivo de Backup Não Encontrado! Favor Verificar!",backup_directory+ database + ".txt")
