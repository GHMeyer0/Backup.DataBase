import utilities.system as system
import sys
import utilities.notification as mail
# import utilities.aws as aws
import configuration.sql_server as sql_config
import subprocess

from datetime import datetime
import os




def backup_mmsql():
    now = datetime.now()

    for database in sql_config.DATABASES:
        try:
            backup_directory = sql_config.BASE_DIRECTORY +'/'+ database +'/'+ str(now.year) +'/'+ str(now.month) +'/'+ str(now.day) +'/'
            backup_filename = database+'-' + str(now.hour) + str(now.strftime("%M")) + '.bak'
            # aws_s3_object =  database +'/'+ str(now.year) +'/'+ str(now.month) +'/'+ str(now.day) +'/' + backup_filename.replace('.bak','.zip')
            
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
                backup_filename
            )
            system.compact_file(
                backup_directory, 
                backup_filename
            )
            # aws.upload_file_to_s3(
            #     backup_directory, 
            #     backup_filename.replace('.bak','.zip'), 
            #     sql_config.AWS_BUCKET, 
            #     aws_s3_object
            # )
            
            mail.send_message(
                "Backup da base "+ database, 
                "Backup da base " + database + " no servidor " + sql_config.DATABASE_SERVER + " foi realizado.", 
                '#03fc1c'
            )
        except Exception as e:
            mail.send_logs(
                "Falha no Backup! Favor Verificar!", 
                backup_directory + "log.txt", 
                "Error: %s" % e
            )


def create_sql_file(database_name, backup_directory, backup_filename):
    file = open(
        backup_directory + 
        "dbbkp.sql","w+"
    )
    file.write("use " + database_name + "\n")
    file.write("BACKUP DATABASE " + database_name + " TO DISK='" + backup_directory + backup_filename + "' \n")
    #file.write("DBCC Shrinkfile('Teste_Log',1)")
    file.close()
    system.write_log_file(
        "Create SQL file for Backup on: " + backup_directory + "dbbkp.sql", 
        backup_directory
    )

def run_backup(backup_directory, backup_filename):
    system.write_log_file(
        "Start backup: " + backup_directory + backup_filename, 
        backup_directory
    )
    output = subprocess.call('sqlcmd -S ' + sql_config.DATABASE_SERVER + ' -U ' + sql_config.USERNAME + ' -P ' + sql_config.PASSWORD + ' -i "' + backup_directory + 'dbbkp.sql"')
    if output == 0:
        system.write_log_file("End backup: " + backup_directory + backup_filename, backup_directory)
    else:
        system.write_log_file("Backup failed: " + backup_directory + backup_filename, backup_directory)
        mail.send_logs("Falha no Backup! Favor Verificar!", backup_directory + "backup.log")
        exit()

backup_mmsql()