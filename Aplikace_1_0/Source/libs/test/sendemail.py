'''
Created on 31. 12. 2015

@author: Meloun
'''
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText

msg = MIMEMultipart()
msg['From'] = 'lubos.melichar@gmail.com'
msg['To'] = 'lubos.melichar@gmail.com'
msg['Subject'] = 'simple email in python'
message = 'a'
msg.attach(MIMEText(message))

mailserver = smtplib.SMTP('smtp.gmail.com:587')
# identify ourselves to smtp gmail client
mailserver.ehlo()
# secure our email with tls encryption
mailserver.starttls()
# re-identify ourselves as an encrypted connection
mailserver.ehlo()
mailserver.login('lubos.melichar', 'fbkdagpxfpkysgtx')

mailserver.sendmail('lubos.melichar@gmail.com','lubos.melichar@gmail.com',msg.as_string())

mailserver.quit()