#!/usr/bin/env python

import subprocess
import cStringIO
import urllib, os
from HTMLParser import HTMLParser
from gluon import current
from appsettings import settings


class Collection:
    
    @staticmethod
    def get_graph(action, plugin, typegraph, host, timespan, path_rrd, time_zone, start, end, plugin_instance=None):
	
	action=str(action)
	plugin=str(plugin)
	typegraph=str(typegraph)
	host=str(host)
	timespan=str(timespan)
	path_rrd=os.path.split(path_rrd)[0]
	start=str(start)
	end=str(end)
	time_zone=str(time_zone)
	PERL=settings.perl_file
	COLLECTION=settings.collection_file	
	
	    
	if plugin_instance==None:
	    plugin_instance = None
	else:
	    plugin_instance = str(plugin_instance)
      
	p=None
	if plugin_instance==None:
	    p=subprocess.Popen(["env", "TZ="+time_zone, PERL, COLLECTION,\
		                "action="+action,\
		                "plugin="+plugin,\
		                "type="+typegraph,\
		                "host="+host,\
		                "timespan="+timespan,\
		                "start="+start,\
		                "end="+end,\
		                "path_rrd="+path_rrd]\
		                ,stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	else:
	    p=subprocess.Popen(["env", "TZ="+time_zone, PERL, COLLECTION,\
		                "action="+action,\
		                "plugin="+plugin,\
		                "type="+typegraph,\
		                "plugin_instance="+plugin_instance,\
		                "host="+host,\
		                "timespan="+timespan,\
		                "start="+start,\
		                "end="+end,
		                "path_rrd="+path_rrd]\
		                ,stdout=subprocess.PIPE, stderr=subprocess.PIPE)
     
     
	#Shell=False
	
	
	stdout, stderr=p.communicate()
	status = p.poll()

    
	return cStringIO.StringIO(stdout)



    @staticmethod
    def get_plugins(path_rrd):
	    
	path_rrd=path_rrd
	r=[]
	d=urllib.unquote(path_rrd)
	#regex = re.compile(expression)
	file_listing=os.listdir(d)
	for f in file_listing:
	    ff=os.path.join(d,f)
	    if os.path.isdir(ff):
		r.append(f.split('-')[0])
	
	result=list(set(r))
	result.sort()
	return result


    @staticmethod
    def action_collection(path_rrd, plugin, timespan, action):


	host=os.path.split(path_rrd)[1]
	plugin=plugin
	timespan=timespan
	action=action
	PERL=settings.perl_file
	COLLECTION=settings.collection_file	

	p=subprocess.Popen([PERL, COLLECTION,\
	        "action="+action,\
	        "plugin="+plugin,\
	        "host="+host,\
	        "timespan="+timespan,
	        "path_rrd="+os.path.split(path_rrd)[0]]\
	        ,stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	
	stdout, stderr=p.communicate()
	status = p.poll()
	
	class ImgParse(HTMLParser):
	    def __init__(self):
		    HTMLParser.__init__(self)
		    self.result = []
	
	    def handle_starttag(self, tag, attrs):
		if tag=="img":
		    self.result.append((dict(attrs)["src"]))
	
	
	parse=ImgParse()
	parse.feed(stdout)
	return parse.result
               
    

