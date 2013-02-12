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



if settings.login_method == 'local' or settings.login_method == 'ldap':
	
	auth = Auth(db)

elif settings.login_method == 'ldap':


	from gluon.contrib.login_methods.ldap_auth import ldap_auth
	auth.settings.login_methods=[(ldap_auth(
	mode=settings.ldap_mode, 
	secure=settings.ldap_secure, 
	server=settings.ldap_server, port=settings.ldap_port, 
	base_dn=settings.ldap_base_dn, 
	allowed_groups = settings.ldap_allowed_groups,
	group_dn = settings.ldap_group_dn,
	group_name_attrib = settings.ldap_group_name_attrib,
	group_member_attrib = settings.ldap_group_member_attrib,
	group_filterstr = settings.ldap_group_filterstr

	))]


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

if settings.login_method == 'CAS' or settings.login_method == 'ldap':
	auth.settings.actions_disabled.append('register')
	auth.settings.actions_disabled.append('change_password')

auth.settings.actions_disabled.append('request_reset_password')
auth.settings.actions_disabled.append('retrieve_username')


##########################################################################
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
##########################################################################

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
    Field('f_path_rrd', notnull=True,  type='string', label=T('Path Rrd')),
    Field('f_time_zone', notnull=True, type="list:string", label=T('Time Zone')),
    format='%(f_name)s',
    migrate=settings.migrate)

db.define_table('t_server_archive',db.t_server,Field('current_record','reference t_server',readable=False,writable=False))

group_time_sone = [('GMT-14'),('GMT-13'),('GMT-12'),('GMT-11'),('GMT-10'),('GMT-9'),('GMT-8'),('GMT-7'),('GMT-6'),('GMT-5'),('GMT-4'),('GMT-3'),('GMT-2'), ('GMT-1'),('GMT0'),('GMT+1'),('GMT+2'),('GMT+3'),('GMT+4'),('GMT+5'),('GMT+6'),('GMT+7'),('GMT+8'),('GMT+9'),('GMT+10'),('GMT+11'),('GMT+12')]
db.t_server.f_time_zone.requires = IS_IN_SET(group_time_sone, multiple=False)

####################### This code is fo rthe register page #########################################
if settings.check_if_user and settings.login_method == 'local' and request.args(0) != 'register':
	check_if_empty = db(db.auth_user.id>0).select()
    	if not check_if_empty:
		redirect(URL(c='default', f='user', args='register'))
	else:
		auth.settings.actions_disabled.append('register')
	

if not settings.check_if_user:
	auth.settings.actions_disabled.append('register')
####################### This code is fo rthe register page #########################################
	
