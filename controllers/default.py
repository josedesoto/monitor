# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## This is a samples controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
## - call exposes all registered services (none by default)
#########################################################################

from collection import Collection
from server import Server  



def index():
    """
    example action using the internationalization operator T and flash
    rendered by views/default/index.html or views/generic.html

    if you need a simple wiki simple replace the two lines below with:
    return auth.wiki()
    """

    if request.env.http_x_forwarded_host:
	http_host = request.env.http_x_forwarded_host.split(':',1)[0]
    else:
	http_host = request.env.http_host    
	   
    #link_check_config='href=http://'+http_host+'/'+request.application+'/'+request.controller+'/check_config'    

    return dict(message='')


def check_config():
    from appsettings import check_config
    return check_config.get_config_status()


def project_manage():
    form = SQLFORM.grid(db.t_project,csv=False,user_signature = False, searchable=False)

    return locals()
  
def server_manage():
    form = SQLFORM.grid(db.t_server,csv=False,user_signature = False, searchable=False)
    return locals()


def show_servers():
    return dict(result=Server.get_servers(db))


def show_graph():

    server_id=request.get_vars.server_id
    action=request.get_vars.action
    plugin=request.get_vars.plugin
    typegraph=request.get_vars.type
    plugin_instance=request.get_vars.plugin_instance
    host=request.get_vars.host
    timespan=request.get_vars.timespan
    start=request.get_vars.start
    end=request.get_vars.end

    result=Server.get_pathrdd_timezone_server(server_id,db)
    path_rrd=result.f_path_rrd
    time_zone=result.f_time_zone
  
    response.headers['Content-Type']="image/png" 
    return response.stream(Collection.get_graph(action, plugin, typegraph, host,\
                                                timespan, path_rrd, time_zone, start,\
                                                end, plugin_instance))


def show_plugin():
    result=''
    
    server_id=request.get_vars.host
    action=request.get_vars.action
    timespan=request.get_vars.timespan
    plugin=request.get_vars.plugin

    result=Collection.action_collection(Server.get_pathrdd_server(server_id,db),plugin,\
                                        timespan, action)
                                        
    
    return dict(result=result)


def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    """
    return dict(form=auth())


def show_plugins():
    result=''
    server_id=request.args(0)
    result=Collection.get_plugins(Server.get_pathrdd_server(server_id, db))
    
    return dict(result=result)


def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)



def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()


@auth.requires_signature()
def data():
    """
    http://..../[app]/default/data/tables
    http://..../[app]/default/data/create/[table]
    http://..../[app]/default/data/read/[table]/[id]
    http://..../[app]/default/data/update/[table]/[id]
    http://..../[app]/default/data/delete/[table]/[id]
    http://..../[app]/default/data/select/[table]
    http://..../[app]/default/data/search/[table]
    but URLs must be signed, i.e. linked with
      A('table',_href=URL('data/tables',user_signature=True))
    or with the signed load operator
      LOAD('default','data.load',args='tables',ajax=True,user_signature=True)
    """
    return dict(form=crud())
