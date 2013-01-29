## Description: 
monitor is a web application that allows to view rrd datacollections that have been created by collectd.

1- Monitor allow you to create group of server by projects.
2- Monitor allow to have different time zone for each server.


## How to install in Linux, windows or Mac:


1- Download web2py:

        #cd /opt
        #wget http://www.web2py.com/examples/static/web2py_src.zip

2- Desscompres:

        #unzip web2py_src.zip

3 - Download Stream log client into web2py:

        #cd /opt/web2py/applications
        #git clone https://github.com/josedesoto/monitor.git

4- Run web2py:

        #python /opt/web2py/web2py.py

5 - Open the URL: http://localhost:8000/monitor


## Dependecies:

	In debian 6 or ubuntu 11:
	#apt-get install perl libjson-perl librrds-perl libhtml-entities-numbered-perl libhtml-element-extended-perl


## How to check the installations:

	In your browser type:
	#http://localhost:8000/monitor/default/check_config



