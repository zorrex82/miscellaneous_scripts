#!/bin/sh
# Author: Edinor Santos da Cunha Júnior
# Email: edinorscjr@gmail.com
# Script to retrieve IP Address

NETADDRESS="http://www.meuip.com.br" # Brazilian website to discover public IP address on clients without fixed IP

# Variables with ADM email address, the client name and path to log file
ADM="user@email.com"
CLIENT="Client Name "
LOG=/tmp/myip.log

# Checking the log file for a change in the IP address.
[ -f "${LOG}" ] && IPADDR=`cat /tmp/myip.log` || IPADDR=0
CURRENT_IPADDR=`lynx -dump ${NETADDRESS} | sed -e 's/ //g' | grep -e "^[0-9]\+\.[0-9]\+\.[0-9]\+\.[0-9]\+$"`

# Generating and sending the email with the IP data and which client to Sys Admin
if [ ${IPADDR}: != ${CURRENT_IPADDR}: ]; then
  echo ${CURRENT_IPADDR} > ${LOG}
  mailx -s "Client IP ${CLIENT}" ${ADM} < ${LOG}
fi