# -*- coding: utf-8 -*-

#########################################################################
## This scaffolding model makes your app work on Google App Engine too
## File is released under public domain and you can use without limitations
#########################################################################

## if SSL/HTTPS is properly configured and you want all HTTP requests to
## be redirected to HTTPS, uncomment the line below:
# request.requires_https()



from appsettings import settings
db = DAL(settings.database_uri)


## by default give a view/generic.extension to all actions from localhost
## none otherwise. a pattern can be 'controller/function.extension'
#response.generic_patterns = ['*'] if request.is_local else []

response.generic_patterns = ['*.json'] if request.is_local else []

## (optional) optimize handling of static files
# response.optimize_css = 'concat,minify,inline'
# response.optimize_js = 'concat,minify,inline'

#########################################################################
## Here is sample code if you need for
## - email capabilities
## - authentication (registration, login, logout, ... )
## - authorization (role based authorization)
## - services (xml, csv, json, xmlrpc, jsonrpc, amf, rss)
## - old style crud actions
## (more options discussed in gluon/tools.py)
#########################################################################

from gluon.tools import Auth, Crud, Service, PluginManager, prettydate



if settings.login_method == 'local':
	auth = Auth(db)

elif settings.login_method == 'ldap':

	print "not yet"


elif settings.login_method == 'CAS':

	auth = Auth(db,cas_provider = settings.cas_provider)
	auth.settings.cas_actions['login']=settings.cas_actions_login
	auth.settings.cas_actions['validate']=settings.cas_actions_validate
	auth.settings.cas_actions['logout']=settings.cas_actions_logout


crud, service, plugins = Crud(db), Service(), PluginManager()

## create all tables needed by auth if not custom tables
auth.define_tables(username=True, signature=False)

#We dont create a group for each user
auth.settings.create_user_groups=False

## configure auth policy
auth.settings.registration_requires_verification = False
auth.settings.registration_requires_approval = False
auth.settings.reset_password_requires_verification = False
auth.settings.actions_disabled=['register','change_password','request_reset_password','retrieve_username']



#########################################################################
## Define your tables below (or better in another model file) for example
##
## >>> db.define_table('mytable',Field('myfield','string'))
##
## Fields can be 'string','text','password','integer','double','boolean'
##       'date','time','datetime','blob','upload', 'reference TABLENAME'
## There is an implicit 'id integer autoincrement' field
## Consult manual for more options, validators, etc.
##
## More API examples for controllers:
##
## >>> db.mytable.insert(myfield='value')
## >>> rows=db(db.mytable.myfield=='value').select(db.mytable.ALL)
## >>> for row in rows: print row.id, row.myfield
#########################################################################

## after defining tables, uncomment below to enable auditing
# auth.enable_record_versioning(db)


########################################
db.define_table('t_project',
    Field('f_name', notnull=True, type='string', label=T('Name')),
    Field('f_description', type='text', label=T('Description')),
    format='%(f_name)s',
    migrate=settings.migrate)

db.define_table('t_project_archive',db.t_project,Field('current_record','reference t_project',readable=False,writable=False))

########################################
db.define_table('t_server',
    Field('f_name', notnull=True, type='string', label=T('Name')),
    Field('f_project', notnull=True, type='reference t_project', label=T('Project')),
    Field('f_path_rrd',notnull=True,  type='string', label=T('Path Rrd')),
    Field('f_time_zone',notnull=True,  type='string', label=T('Time Zone')),
    format='%(f_name)s',
    migrate=settings.migrate)

db.define_table('t_server_archive',db.t_server,Field('current_record','reference t_server',readable=False,writable=False))
