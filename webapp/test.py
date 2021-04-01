import smtplib
server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
server.login('testing.deepak.sharma@gmail.com', 'Deepaktesting@123')
# msg = """ Subject:Your Account Status \n Hi, <br> Your account has been  """
msg = 'Rejected'
server.sendmail('testing.deepak.sharma@gmail.com','deepakinfoweb1@gmail.com','Subject:Your Account Status\nHi,\nYour account has been updated. '+msg+'  ')

# import smtplib
# sender=’thesender@gmail.com’
# receiver=’whicheverreceiver@gmail.com’
# password=’<put your password here>’
# smtpserver=smtplib.SMTP(“smtp.gmail.com”,587)
# smtpserver.ehlo()
# smtpserver.starttls()
# smtpserver.ehlo
# smtpserver.login(sender,password)
# msg=’Subject:Demo\nThis is a demo
# smtpserver.sendmail(sender,receiver,msg)
# print(‘Sent’)
# smtpserver.close()