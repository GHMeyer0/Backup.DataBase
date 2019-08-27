from email.message import Message
import smtplib, os
import json
import requests

from configuration import notification as config

def send_logs(subject,log, msg = ""):
  msg = msg + "\nOcorreu um erro ao executar o Backup, Favor Verificar! \n"
  msg = msg + "Segue abaixo os logs do Backup \n \n"
  msg = msg + open(log, 'r').read()
  send_message(subject, msg, "#fc0303" )

def send_message(subject, msg, color = '#764FA5', notification_channel = config.channel):
  try:
    if notification_channel == 'web-hook':
      slack_data = {
        'attachments': [
          {
            'title': subject,
            'text': msg,
            'color': color
          }
        ]
      }
      requests.post(
        config.webhook_url, data=json.dumps(slack_data),
        headers={'Content-Type': 'application/json'}
      )
      
    else:
      mail_form = Message()
      mail_form['Subject'] = subject
      mail_form['From'] = config.fromaddr
      mail_form['To'] = config.toaddrs
      mail_form.set_payload(msg)
      
      serv=smtplib.SMTP(config.smtpserver,config.smtpport)
      serv.login(config.mailuser, config.mailpass)
      serv.sendmail(mail_form['From'], mail_form['To'], mail_form.as_string())
      serv.quit()
    
  except Exception as e:
    print("Erro " , e)
