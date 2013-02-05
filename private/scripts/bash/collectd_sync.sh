#!/bin/bash
#
# Scrtipt to sync the xhtml or rrd data. XHTML if 32bit platform, RRD if 64bits platform
# Need to have install apt-get  install rrdtool
# by Jose de Soto
#
# Version 1.0
#
# On the crontab as for example:
## #Scrtip to send the data from collectd to ggeuweb301
## */30 * * * * PATH_TO_SCRIPT/collectd_sync.sh >> /dev/null

##CLIENT DATA
 #Values can be: 32 or 64
 PLATFORM="64" 

 #To update the RRD to 64bits. Only for 32 client server. Soon will be obsolete: YES=1 or NO=0
 UPDATE_TO_64="0"
 SCRIPT_TO_UPDATE_64="/opt/app/scripts/rrd32to64.sh"

 #Yes=1 or No=0
 SEND_DATA_COMPRESS="1"

 #Path where collectd generate the RRD. For example /opt/collectd/var not /opt/collectd/var/
 PATH_TO_DATA="/opt/collectd/var/lib/collectd"

 DOMAIN=`hostname -d`
 if [ "$DOMAIN" != "" ];
 then
 	HOSTNAME=`hostname`.$DOMAIN
 else
	HOSTNAME=`hostname`
 fi
 

#SERVER DATA
 #Default root
 SSH_USER="serverstatus"
 #Server IP where to sync the data. ggeuweb301=92.243.21.211
 SERVER="92.243.21.211"
 #Path where to keep the data into the server, example /srv/ggeuint301_data/server-statistics
 PATH_TO_KEEP_DATA="/srv/ggeuint301_data/server-statistics"
 LOCK_FILE=/var/lock/collectd_sync.lock

if [ -e "$LOCK_FILE" ]
then
	echo "THE PROCESS IS LOCK"
	exit 0
fi


if test ! -d "$PATH_TO_DATA";
then
	echo "$PATH_TO_DATA does not exist"
	exit 1
fi

if [ "$PLATFORM" != "64" ] && [ "$PLATFORM" != "32" ];
then

	echo "PLATFORM value have to be 32 or 64"
	exit 1
fi

echo "START:" `date`

touch $LOCK_FILE

if [ "$PLATFORM" == "64" ];
then

	if [ "$SEND_DATA_COMPRESS" == "1" ];
	then
		cd $PATH_TO_DATA
		tar -zcf $HOSTNAME.tar.gz $HOSTNAME
		rsync -rah --stats $PATH_TO_DATA/$HOSTNAME.tar.gz $SSH_USER@$SERVER:$PATH_TO_KEEP_DATA/
		rm $HOSTNAME.tar.gz
		ssh $SSH_USER@$SERVER "cd $PATH_TO_KEEP_DATA;tar xzf $HOSTNAME.tar.gz;rm $HOSTNAME.tar.gz"
	else
		rsync -rah --stats $PATH_TO_DATA/$HOSTNAME $SSH_USER@$SERVER:$PATH_TO_KEEP_DATA/

	fi
fi

if [ "$PLATFORM" == "32" ];
then

	if [ "$SEND_DATA_COMPRESS" == "1" ];
	then

		cd $PATH_TO_DATA
		for i in `find -name "*.rrd"`; do rrdtool dump $i > $i.xml; done
		#Interesante: --remove-files
		# To show the tar content: tar -ztvf edeuweb200.tar.gz
		tar -zcf $HOSTNAME.tar.gz --exclude='*.rrd' $HOSTNAME
		rsync -rah --stats $PATH_TO_DATA/$HOSTNAME.tar.gz $SSH_USER@$SERVER:$PATH_TO_KEEP_DATA/
		rm $HOSTNAME.tar.gz
		ssh $SSH_USER@$SERVER "cd $PATH_TO_KEEP_DATA;tar xzf $HOSTNAME.tar.gz;rm $HOSTNAME.tar.gz"
	else

		rsync -rah --stats --exclude=*.rrd $PATH_TO_DATA/$HOSTNAME $SSH_USER@$SERVER:$PATH_TO_KEEP_DATA/

	fi 


	if [ "$UPDATE_TO_64" == "1" ];
	then

		#Execute one remote scrtipt to update the RRD
		ssh $SSH_USER@$SERVER "$SCRIPT_TO_UPDATE_64 $PATH_TO_KEEP_DATA/$HOSTNAME"
		

		
	fi 
fi

echo "FINISH:" `date`

rm $LOCK_FILE
