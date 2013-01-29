#!/usr/bin/env python
# -*- coding: utf-8 -*-


from gluon.html import *
from gluon.sqlhtml import *
from gluon.validators import *


class Server:
	@staticmethod
	def get_pathrdd_server(server_id, db):
    		path_rrd=db(db.t_server.id==server_id).select(db.t_server.f_path_rrd).first()

    		return path_rrd.f_path_rrd

	@staticmethod
	def get_pathrdd_timezone_server(server_id, db):
    		result=db(db.t_server.id==server_id).select(db.t_server.f_path_rrd, db.t_server.f_time_zone).first()
    
    		return result
	
	@staticmethod
	def get_servers(db):
		return db().select(db.t_server.ALL)

