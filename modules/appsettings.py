from gluon.storage import Storage
from gluon import current
from prettyexception import ErrorHTTP
settings = Storage()


#Check if user on the startup. Set to False if you have user on the system
settings.check_if_user=True

#mysql or sqlite
settings.database='sqlite'

##To connect to a Mysql Databse
settings.database_name='MY_DATABASE_NAME' #First: create database MY_DATABASE_NAME CHARACTER SET utf8 COLLATE utf8_general_ci;
settings.database_user='MY_DATABASE_USER'
settings.database_pass='MY_DATABASE_PASS'
settings.database_uri='MY_DATABASE_URI'
settings.migrate = True
settings.title = 'Monitor'
settings.subtitle = 'powered by web2py'
settings.author = 'Jose de Soto'
settings.author_email = 'josedesoto@gmail.com'
settings.keywords = 'monitor, statistics, server'
settings.description = 'Web application that allows to view rrd datacollections that have been created by collectd.'
settings.security_key = 'd110e72d-83fb-40bc-bb1c-a62e324c80bc'
settings.login_method = 'local' #local, ldap or CAS
settings.login_config = ''
settings.plugins = []

#########################################
#if LDAP configuration:			#
#########################################
settings.ldap_server = ''
settings.ldap_port = ''
settings.ldap_mode = 'uid_r' #uid, cn, dominio
settings.ldap_secure = True #Maybe you need openssl
settings.ldap_cert_path = ''
settings.ldap_cert_file = ''
settings.ldap_base_dn =  ''
settings.ldap_allowed_groups = [""]
settings.ldap_group_dn = ''
settings.ldap_group_name_attrib = 'cn'
settings.ldap_group_member_attrib = 'memberUid'
settings.ldap_group_filterstr = 'objectClass=*'

##################################################################################
#	 #Example Apache LDAP#
#
#	 AuthType Basic
#        AuthBasicProvider ldap
#        AuthName "GG LDAP authentication"
#        AuthLDAPURL ldaps://ldap.mydomain.com/ou=people,dc=mydomain,dc=com?uid
#        AuthLDAPGroupAttribute memberUid
#        AuthLDAPGroupAttributeIsDN off
#        AuthzLDAPAuthoritative on
#        Require ldap-group cn=Monitor,cn=groups,dc=mydomain,dc=com
#
#	#The same LDAP aut in MONITOR web application
#	
#	settings.ldap_server = 'ldap.mydomain.com'
#	settings.ldap_port = '636'
#	settings.ldap_mode = 'uid_r' #uid, cn, dominio
#	settings.ldap_secure = True #Maybe you need openssl
#	settings.ldap_cert_path = ''
#	settings.ldap_cert_file = ''
#	settings.ldap_base_dn =  'ou=people,dc=mydomain,dc=com'
#	settings.ldap_allowed_groups = ["Monitor"]
#	settings.ldap_group_dn = 'cn=groups,dc=mydomain,dc=com'
#	settings.ldap_group_name_attrib = 'cn'
#	settings.ldap_group_member_attrib = 'memberUid'
#	settings.ldap_group_filterstr = 'objectClass=*'
#	
####################################################################################


#########################################
#if CAS configuration:			#
#########################################
settings.cas_provider='https://mydomain.com/cas/default/user/cas'
#by default, change if needed
settings.cas_actions_login='login'
settings.cas_actions_validate='validate'
settings.cas_actions_logout='logout'


#########################################
# PATH TO PERL FILE COMMAND		#
# by default: /usr/bin/perl  		#
#########################################
settings.perl_file="/usr/bin/perl"
##########################################################################
# PATH TO collection.cgi FILE COMMAND					 #
# by dafault: ...applications/monitor/private/scripts/perl/collection.cg #
##########################################################################
settings.collection_file=current.request.folder+"private/scripts/perl/collection.cgi"





if settings.database=='sqlite':

	#To connect a SQLITE database. No extra configuration need to be done
	settings.database_uri = 'sqlite://storage.sqlite'

elif settings.database=='mysql':
	
	settings.database_uri = 'mysql://'+settings.database_user+':'+settings.database_pass+'@'+settings.database_uri+'/'+settings.database_name



#We check if we have defined perl and colelction

class check_config:

    @staticmethod
    def get_config_status():
    
        import os.path
        result=''

        
        if not os.path.exists(settings.perl_file):
            result="Miss configuration in settings.perl_file"
  
        if not os.path.exists(settings.collection_file):
            result+="Miss configuration in settings.collection_file"
            
        if result=='':
            return "The configuration looks fine"
        else:
            raise PRETTYHTTP(500, 'ERROR in the configuration!!!'\
            +result)

            
