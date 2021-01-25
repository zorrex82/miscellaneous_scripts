#!/bin/bash
#
#  Hardware Inventory Bash Script
#
# Author     : Edinor Junior
#
#  -------------------------------------------------------------
#   This program makes a file with machine name and timestamp, attach all data collect about configuration proprierties
#  -------------------------------------------------------------
#
# Versions:
#
#    v1.0.0 2019-04-02: Edinor Junior
#    v1.0.1 2021-01-25: Edinor Junior
#
#
# License: GPL
#

if [ $(id -u) != 0 ] ; then
	echo "You need to be root with you want to run the script"
	exit 1 ;
fi


function interfacesNetwork(){
	interfacesNetwork=`ifconfig | cut -d" " -f1 | cut -d":" -f1 | grep -v "lo"`
	number=1
	for interfacesName in $interfacesNetwork
	do
		echo "2.$((number++))""-Network Informations ($interfacesName):"										>> $BD
		echo "     ""- IPv4 Address: "`ifconfig $interfacesName | grep 'inet ' | awk '{print $2}'`							>> $BD
		echo "     ""- MAC Address:  "`ifconfig $interfacesName | grep 'ether' | cut -d" " -f10 `							>> $BD
		echo ""																		>> $BD
	done
}

function partitions(){
	partitions=`fdisk -l | grep /dev/sda2 | grep -v Drive | grep $1 | cut -d" " -f1 | cut -d"/" -f3`
	number=1
    for partition in $partitions
    do
		echo "     ""     ""- Nome : " $partition													>> $BD
		capacity=`parted /dev/$partition print 2>/dev/null | grep $partition | cut -d" " -f3`
		type=`parted /dev/$partition print 2>/dev/null | grep -v File | grep -v  Disk | grep -v model | grep -v Sector | grep -v Partition | grep -v model | cut -d" " -f14`
		echo "     ""     ""- Size : " $capacity													>> $BD
		if [ -z $type ]; then type="Not Formated or Unknown"; fi
		echo "     ""     ""- Type : " $type									 					>> $BD
		echo "     "																	>> $BD
	done
}


function drive(){
	drives=`fdisk -l | grep Drive | grep /dev/sda | cut -d" " -f2 | cut -d"/" -f3| sed 's/://g'| grep -v ram`
	number=1
	for drive in $drives
	do
		echo "3.3.$((number++))""- Drive $drive "													>> $BD
		capacity=`fdisk -l | grep Drive | grep -e $drive | cut -d" " -f3`										>> $BD
		escale=`fdisk -l | grep Drive | grep -e $drive | cut -d" " -f4 | sed 's/,//g'`									>> $BD
		echo "     ""- Size : "$capacity $escale													>> $BD
		echo "     ""- Partition Table  : "`parted /dev/$drive print | grep "Partition Table" | cut -d" " -f3`					>> $BD
		echo "	   ""Partitions:"															>> $BD
		echo "	   "																	>> $BD
		partitions $drive
	done
}

	BD=`hostname`.$(date +%d-%m-%Y-%H:%M).log
	echo ""                              													     		>> $BD
	echo "========================================================="											>> $BD
	echo "=  Inventory Timestamp - `date +'%d/%m/%Y %H:%M'` ="											>> $BD
	echo "========================================================="									 		>> $BD
	echo ""						 													>> $BD
	echo " Hostname: `hostname`"								     							>> $BD
	echo ""															     				>> $BD
	echo "1 - SYSTEM"																	>> $BD
	echo ""																			>> $BD
	echo "1.1 Operation System Info:"										     				>> $BD
	echo "     ""- Architecture: "`uname -m`															>> $BD
	echo "     ""- Kernel Version: "`uname -r`														>> $BD
	echo ""																	     		>> $BD
	echo "1.2 Distro Info:"												     			>> $BD
	echo "     ""- Distro: "`lsb_release -i | cut -d: -f2`												>> $BD
	echo "     ""- Version: "`lsb_release -r | cut -d: -f2` 													>> $BD
	echo "     ""- Codename: "`lsb_release -c | cut -d: -f2`							 					>> $BD
	echo "" 																		>> $BD
	echo "2 - Network"																		>> $BD
	echo ""																				>> $BD
	interfacesNetwork
	echo ""																				>> $BD
	echo "3 - HARDWARE"																	>> $BD
	echo ""																	             	>> $BD
	echo "3.1 Processor" 																     	>> $BD
	echo "     ""- Manufacture: "`cat /proc/cpuinfo | head -n 31 | grep 'model name'  | cut -d : -f2`				  			>> $BD
	echo "     ""- Model: "`cat /proc/cpuinfo | head -n 31 | grep 'model name'  | cut -d : -f2`				  				>> $BD
	echo "     ""- Velocity (MHz):" `cat /proc/cpuinfo | head -n 31 | grep 'cpu MHz' | cut -d : -f2 | cut -d . -f1`"MHz" 					>> $BD
	echo "     ""- Cache: "`cat /proc/cpuinfo | head -n 31 | grep 'cache size' | cut -d : -f2`								>> $BD
	echo ""																			>> $BD
	echo "3.2 Memory" 																	>> $BD
	echo "     ""- Maximum Capacity: "`dmidecode -t memory | grep 'Maximum Capacity'| cut -d : -f2`								>> $BD
	echo "     ""- Number of Slot(s): "`dmidecode -t memory |  grep 'Number Of Devices:' | cut -d : -f2`							>> $BD
	echo "     ""- Quantity Installed:  "`free -m | grep 'Mem:' | awk '{print $2}'`"MB"	    								>> $BD
	echo "     ""- Slot(s) in Use: "`dmidecode -t memory | grep 'Size' | grep -v "No Module Installed" | cut -d" "  -f2`		>> $BD
	echo ""											     								>> $BD
	echo "3.3 Hard drives"																	>> $BD
	echo ""																			>> $BD
	drive
	echo ""
	echo "Generate Inventory $BD"
	sleep 2
	cat $BD