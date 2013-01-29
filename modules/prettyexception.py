#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
 Plugin PRETTYHTTP
 Copyright (c) 2011 Mulone, Pablo Martin (http://martin.tecnodoc.com.ar/)
 License: MIT
"""

"""
 ABOUT PRETTYHTTP:
"""

from gluon.globals import current
from gluon.http import HTTP
from gluon.html import IMG, A, URL


class ErrorHTTP(BaseException):
    """ PRETTYHTTP """

    def __init__(
        self,
        status,
        body='',
        **headers
        ):
        self.status = status
        self.body = body
        self.headers = headers

        body = self.render()

        raise HTTP(status, body, **headers)

    def render(self):
        """ Render """

        response = current.response
        T = current.T

        return '''
	<html><head><title>Error 404: doughnut not found!</title>
	</head><body>
	<center>
	<table width="90%" height="100%">
	<tbody><tr>
	<td width="100%">
	<center><h1><u> %(title)s </u></h1><br>
	%(message)s
	<br><br>
	<font face="Arial">You have reach this page because the requested
	doughnut does not exists on this server. Please check that the URL
	is correct or inform the webmaster of the website of an incorrect
	link.<br><br>
	%(index)s
	</font><br><br><br></center></td></tr>
	</tbody></table>
	</center>
	</body></html>
        ''' % {'title': self.status,
               'message':self.body,
               'index':A(T('Go to website home page'), _href=URL('default','index')).xml()}
