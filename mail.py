# Libraries to create connection and send mail
import smtplib
from email.mime.text import MIMEText

# create connection with google
smtp_ssl_host = 'smtp.gmail.com'
smtp_ssl_port = 465
# username or email and password
username = 'user@gmail.com'
password = 'senha'

# Variables for origin and destination mail
from_addr = 'user@gmail.com'
to_addrs = ['destination@domain']

# the email library has several templates
# for different message formats
# in this case we will use MIMEText to send
# text only
message = MIMEText('Hello World')
message['subject'] = 'Hello'
message['from'] = from_addr
message['to'] = ', '.join(to_addrs)

# we will connect securely using SSL
server = smtplib.SMTP_SSL(smtp_ssl_host, smtp_ssl_port)
# to interact with an external server we will need
# sign in to it
server.login(username, password)
server.sendmail(from_addr, to_addrs, message.as_string())
server.quit()
