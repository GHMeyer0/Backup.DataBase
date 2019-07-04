import Utilities.System as sys
import Utilities.Mail as mail
import Utilities.Aws_s3 as s3
from Configuration import SqlServer as config
import subprocess

from datetime import datetime
import os

def backup_mmsql():
  now = datetime.now()
  for database in config.databases:
    try:
      bkp_directory = config.backup_base_dir +'/'+ database +'/'+ str(now.year) +'/'+ str(now.month) +'/'+ str(now.day) +'/'
      aws_directory = database +'/'+ str(now.year) +'/'+ str(now.month) +'/'+ str(now.day) +'/'
      bkp_filename = database+'-' + str(now.hour) + str(now.minute) + '.bak'
      log_dir = bkp_directory
      sys.create_folder(bkp_directory,log_dir)
      create_sql_file(database,bkp_directory + bkp_filename,log_dir)
      run_backup(bkp_directory+bkp_filename,log_dir)
      sys.compact_file(bkp_directory+bkp_filename,log_dir)
      s3.upload_file(bkp_directory+bkp_filename,config.aws_bucket, aws_directory + bkp_filename, log_dir)
      msg = "Backup da base " + database + " no servidor " + config.dbserver + " foi realizado."
      mail.send_mail("Backup da base "+ database, msg)
    except:
      mail.send_logs("Falha no Backup! Favor Verificar!",log_dir + "backup.log")
    

def create_sql_file(dbname,bkp_fullpath,log):
    #sys.create_folder(os.path.dirname(__file__) + "/sql",log)
    file = open(log + "dbbkp.sql","w+")
    file.write("use " + dbname + "\n")
    file.write("BACKUP DATABASE " + dbname + " TO DISK='" + bkp_fullpath + "' \n")
    #file.write("DBCC Shrinkfile('Teste_Log',1)")
    file.close()
    sys.write_log_file("Create SQL file for Backup on: " + log + "dbbkp.sql",log)

def run_backup(bkp_fullpath,log):
  sys.write_log_file("Start backup: " + bkp_fullpath ,log)
  output = subprocess.call('sqlcmd -S ' + config.dbserver + ' -U ' + config.u + ' -P ' + config.p + ' -i "' + log + 'dbbkp.sql"')
  if output == 0:
    sys.write_log_file("End backup: " + bkp_fullpath, log)
  else:
    sys.write_log_file("Backup failed: " + bkp_fullpath ,log)
    mail.send_logs("Falha no Backup! Favor Verificar!",log + "backup.log")
    exit()

backup_mmsql()