# Python script for create a microservice to retrieve data from ftp server and send to queue on RabbitMQ
# Author: Edinor Junior
# Version: 1.0.1

# Import Libraries
import os, sys
import pika
import pysftp
from datetime import datetime, date
from time import sleep

# Date and timestamp variables
today = date.today()
now = datetime.now()

# Convert date from a brazilian format
now = now.strftime('%d/%m/%Y')

# Time to wait until try again
delay_time = 60


# function to connect on ftp
def conect_ftp(remoteFilePath, localFilePath, nameQueue):
    cnopts = pysftp.CnOpts()
    cnopts.hostkeys = None
    sftp = pysftp.Connection(host='0.0.0.0', username='userftp', password='passwordftp', cnopts=cnopts)
    print('Connection succesfully stablished ...')
    remoteFilePath = remoteFilePath
    localFilePath = localFilePath
    sftp.get(remoteFilePath, localFilePath)
    sftp.close()

    check_date(remoteFilePath, nameQueue)


################# start of function to check date ###############################
def check_date(file, queue):
    # format data and build file
    file = file
    modify = datetime.fromtimestamp(os.path.getmtime(file))
    alter_date = []
    create_date = modify.strftime('%d/%m/%Y')
    x = modify.strftime('%d/%m/%Y').split('/')
    for i in x:
        alter_date.append(i)
    path = file
    y = path.split('/')
    destination = []
    for i in y:
        destination.append(i)
    name = len(destination) - 1
    # broker connection
    connection = pika.BlockingConnection(
        pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    # queue declaration
    channel.queue_declare(queue=queue)
    # file validation
    if create_date == now:
        try:
            with open('/home/user/{0}_{1}'.format(queue, destination[name]), 'r'):
                print(" File exist")
                connection.close()
        except Exception:
            log = open('/home/user/{0}_{1}'.format(queue, destination[name]), 'a')
            log.write('\nThe file {0} is new'.format(destination[name]))
            log.close()
            # send file to broker server
            channel.basic_publish(exchange='',
                                  routing_key=queue,
                                  body=file)
            print(" [x] Sent Files.csv")
            # closed connection
            connection.close()
    else:
        log = open('/home/user/{0}'.format(destination[name]), 'a')
        log.write('\nThe file {0} is old'.format(destination[name]))
        log.close()
        print('file not sent')
        connection.close()


################# end of function to check date ###############################

def main():
    while True:
        try:
            conect_ftp('/FTP/ADDRESS/file.csv', '/home/user/file.csv', 'queue')
            conect_ftp('/FTP/ADDRESS/file.csv', '/home/user/file.csv', 'queue')
            sleep(delay_time)

            check_date('/FTP/ADDRESS/file.csv', 'queue')
            check_date('/FTP/ADDRESS/file.csv', 'queue')
            sleep(delay_time)

        except Exception:
            print("Connection is not possible, try again in:", delay_time / 60, "minute(s).")
            sleep(delay_time)


if __name__ == '__main__':
    main()
