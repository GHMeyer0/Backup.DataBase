import sys
import subprocess
import os
import threading
from datetime import datetime

import utilities.system as system
import utilities.notification as notifications
import utilities.aws as aws
import configuration.sql_server as sql_config

def backup_mmsql(database):
    now = datetime.now()
    try:
        backup_directory = sql_config.BASE_DIRECTORY +'/'+ database +'/'+ str(now.year) +'/'+ str(now.month) +'/'
        backup_filename = database + '-' + str(now.day) + '-'+ str(now.hour) + str(now.strftime("%M")) + '.bak'
        aws_s3_object =  database +'/'+ str(now.year) +'/'+ str(now.month) +'/' + backup_filename.replace('.bak','.zip')
        system.create_folder(
            backup_directory
        )
        create_sql_file(
            database, 
            backup_directory, 
            backup_filename
        )
        run_backup(
            backup_directory, 
            backup_filename,
            database
        )
        system.compact_file(
            backup_directory, 
            backup_filename,
            database
        )
        aws.upload_file_to_s3(
            backup_directory, 
            backup_filename.replace('.bak','.zip'), 
            sql_config.AWS_BUCKET, 
            aws_s3_object,
            database
        )
        end_time = datetime.now() - now
        tamanho_backup = os.path.getsize(backup_directory + backup_filename.replace('.bak', '.zip'))
        notifications.send_message(
            "Backup da base "+ database, 
            "Backup da base " + database + " no servidor " + sql_config.DATABASE_SERVER + " foi realizado." + 
            "\n Duração: " + str(end_time) +
            "\n Tamanho: " "{0:.2f}".format(tamanho_backup/(1024*1024*1024)) + " GB",
            '#03fc1c'
        )
    except Exception as e:
        notifications.send_logs(
            "Falha no Backup! Favor Verificar!", 
            backup_directory + database +".txt", 
            "Error: %s" % e
        )

def create_sql_file(database_name, backup_directory, backup_filename):
    file = open(
        backup_directory + 
        database_name + "bkp.sql", "w+"
    )
    file.write("use " + database_name + "\n")
    file.write("BACKUP DATABASE " + database_name + " TO DISK='" + backup_directory + backup_filename + "' \n")
    #file.write("DBCC Shrinkfile('Teste_Log',1)")
    file.close()
    system.write_log_file(
        "Create SQL file for Backup on: " + backup_directory + database_name + "bkp.sql",
        backup_directory,
        database_name
    )

def run_backup(backup_directory, backup_filename, database):
    system.write_log_file(
        "Start backup: " + backup_directory + backup_filename, 
        backup_directory, database
    )
    output = subprocess.call('sqlcmd -S ' + sql_config.DATABASE_SERVER + ' -U ' + sql_config.USERNAME + ' -P ' + sql_config.PASSWORD + ' -i "' + backup_directory + database + 'bkp.sql"')
    if output == 0:
        system.write_log_file("End backup: " + backup_directory + backup_filename, backup_directory, database)
    else:
        system.write_log_file("Backup failed: " + backup_directory + backup_filename, backup_directory, database)
        notifications.send_logs("Falha no Backup! Favor Verificar!", backup_directory + database + ".txt")
        exit()


system.deletar_backups_antigos(sql_config.BASE_DIRECTORY, sql_config.DIAS_RETER_BACKUP)
aws.deletar_backup_antigo_S3(sql_config.AWS_BUCKET, sql_config.DIAS_RETER_BACKUP)


backups = []
try:
    for database in sql_config.DATABASES:
        backups.append(threading.Thread(target=backup_mmsql, args=(database,)))
except Exception as e:
        notifications.send_logs(
            "Falha no Backup! Favor Verificar!", 
            0, 
            "Error: %s" % e
        )
for backup in backups:
    backup.start()
    
for backup in backups:
    backup.join()
