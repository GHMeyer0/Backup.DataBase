import os
import datetime
import zipfile
try:
    import zlib
    compression = zipfile.ZIP_DEFLATED
except:
    compression = zipfile.ZIP_STORED

def create_folder(directory,log):
  if not os.path.exists(directory):
      os.makedirs(directory)
      write_log_file("create folder "+directory+"- "+get_hour_now()+"\n",log)

def write_log_file(log_msg,path):
  logfile = open(path+"/log","wa+")
  logfile.write(log_msg + "\n")
  logfile.close()

def get_hour_now():
  return "hour["+str(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))+"]"

def compact_file(disk,log):
  print('Start Compact file: '+disk)
  log+="Start Compact file: "+disk+" - "+get_hour_now()+"\n"
  zf = zipfile.ZipFile(disk.replace('.bak','.zip'), mode='w')
  if os.path.isfile(disk):
      try:
          zf.write(disk, compress_type=compression)
      finally:
          print('closing compress')
          log+="Ended Compact file: "+disk+" - "+get_hour_now()+"\n"
          zf.close()

      #delete the file
      print('Deleting '+disk)
      log+="Deleting "+disk+" - "+get_hour_now()+"\n"
      os.remove(disk)
  else:
      print('File not exists')
      log+="File "+disk+" not exists - "+get_hour_now()+"\n"

  print("Log: "+log)
