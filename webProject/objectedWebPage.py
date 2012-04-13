#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
import os
import cgi
import datetime
import urllib
import wsgiref.handlers

from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db
from google.appengine.api import users
from google.appengine.ext import webapp

class calenderPage(object):
    """A Shifted App Page"""

    calenders{}

    def __init__(self, name):
        self.name = name
        self.staff = []
        self.shifts = []
        calenderPage.calenders[name] = self

    def 

class userShift(db.Model):
    user = db.StringProperty(required=True)
    shiftName = db.StringProperty(required=True)
    sTime = db.StringProperty(required=True)
    sTc = db.StringProperty(required=True)
    eTime = db.StringProperty(required=True)
    eTc = db.StringProperty(required=True)
    mo = db.StringProperty(required=True)
    tu = db.StringProperty(required=True)
    we = db.StringProperty(required=True)
    th = db.StringProperty(required=True)
    fr = db.StringProperty(required=True)
    sa = db.StringProperty(required=True)
    su = db.StringProperty(required=True)
    staffNum = db.IntegerProperty(required=True)
    
    
        

class MainHandler(webapp2.RequestHandler):
    def get(self):
        template_values = {}
        self.response.headers["Content-Type"] = "text/html"
        path = os.path.join(os.path.dirname(__file__), 'calenderPage.html')
        page = template.render(path, template_values)
        self.response.out.write(page)


app = webapp2.WSGIApplication([('/', MainHandler)],
                              debug=True)
