from email.message import Message
import smtplib, os

from Configuration import Mail as config

def send_logs(subject,log):
  msg = ""
  msg = msg + "Ocorreu um erro ao executar o Backup, Favor Verificar! \n"
  msg = msg + "Segue abaixo os logs do Backup \n \n"
  msg = msg + open(log, 'r').read()
  send_mail(subject, msg)

def send_mail(subject,msg):
  try:
    msg1 = Message()
    msg1['Subject'] = subject
    msg1['From'] = config.fromaddr
    msg1['To'] = config.toaddrs
    msg1.set_payload(msg)
    serv=smtplib.SMTP(config.smtpserver,config.smtpport)
    serv.login(config.mailuser, config.mailpass)
    serv.sendmail(msg1['From'], msg1['To'], msg1.as_string())
    serv.quit()
  except Exception as e:
    print("Erro " , e)