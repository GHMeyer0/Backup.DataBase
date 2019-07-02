from Utilities import System as sys
import Utilities.Mail as mail
from Configuration import SqlServer as config
import subprocess

from datetime import datetime
import os

def backup_mmsql():
  now = datetime.now()
  databases = config.databases
  
  for x in config.databases:
    bkp_directory = config.backup_base_dir+str(now.year)+'/'+str(now.month)+'/'+str(now.day)+'/'
    bkp_filename = database+'-'+str(now.year)+str(now.month)+str(now.day)+'.bak'
    bkp_fullpath = bkp_directory+bkp_filename
    log = bkp_directory
    sys.create_bkp_folders(bkp_directory,log)
    create_sql_file(database,bkp_fullpath)
    sys.run_backup(bkp_fullpath)

    sys.compact_file(bkp_directory)
    msg = 'Backup da base '+ database +' no servidor '+ config.dbserver+' foi realizado.'
    msg += 'Saida do programa: '+str(log)
    mail.send_mail(dataconfig['subject'],msg)

def create_sql_file(dbname,bkp_fullpath):
  sys.create_folder(os.path.realpath(__file__)+"/sql")
  file = open(os.path.dirname(os.path.realpath(__file__))+"/sql/dbbkp.sql","w+")
  file.write("use "+dbname+"\n")
  file.write("BACKUP DATABASE "+dbname+" TO DISK='"+bkp_fullpath+"' \n")
  #file.write("DBCC Shrinkfile('Teste_Log',1)")
  file.close()

def run_backup(bkp_fullpath,log):
  print('Start backup')
  sys.write_log_file("Start backup: "+bkp_fullpath+" - "+sys.get_hour_now()+"\n")
  output = subprocess.call('sqlcmd -S '+ config.dbserver +' -U '+ config.u +' -P '+ config.p + ' -i "'+os.path.dirname(os.path.realpath(__file__))+'/sql/dbbkp.sql"')
  sys.write_log_file(output,log) 
  sys.write_log_file("End backup: "+bkp_fullpath+" - "+sys.get_hour_now()+"\n",log)

backup_mmsql()