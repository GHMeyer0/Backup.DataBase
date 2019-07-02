from email.message import Message

from Configuration import Mail as config

def send_mail(subject,msg):
  try:
    msg1 = Message()
    msg1['Subject'] = subject
    msg1['From'] = config.fromaddr
    msg1['To'] = config.toaddrs
    msg1.set_payload(msg)
    print('Enviando Mensagem...\n')
    print(msg1)
    serv=smtplib.SMTP(config.smtpserver,config.smtpport)
    #serv.ehlo()
    #serv.starttls()
    serv.login(config.mailuser, config.mailpass)
    serv.sendmail(msg1['From'], msg1['To'], msg1.as_string())
    serv.quit()
  except Exception as e:
    print("Erro " , e)
  else:
    print("Enviado!")  