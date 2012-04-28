import webapp2
import os
import string
import random
import re
from google.appengine.ext import db
from google.appengine.api import rdbms
from google.appengine.api import users
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app
from dbModels.shift import *
from dbModels.employee import *
from dbModels.schedule import *

class results(webapp2.RequestHandler):
    def post(self):
        currentSchedule = self.request.get("schedId")
        self.response.out.write("""
        <html>
            <head>
                <link rel="stylesheet" type="text/css" media="screen" href="resultsPage.css"/>
            </head>
            <body>""")

        shifts = db.GqlQuery("SELECT * from Shift WHERE user = :1 ORDER BY starttime", currentSchedule).fetch(1000)
	for s in shifts:
            self.response.out.write("""<p class="color"> %s </p>""" % s)
        emps = db.GqlQuery("SELECT * from Employee WHERE user = :1 ORDER BY keyy", currentSchedule).fetch(1000)
	for e in emps: 
            self.response.out.write("""<p class="color"> %s </p>""" % e)

        self.response.out.write("""
                <form action="/Optimize" method="post">
                <input type="hidden" value="%s" name="schedId"></input>
                <input type="submit" value="Optimize"></input>
                </form>
            </body>
        </html>
        """ % currentSchedule)