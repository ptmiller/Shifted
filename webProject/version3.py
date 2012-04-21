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

import webapp2
import os
import string
import random
from google.appengine.ext import db
from google.appengine.api import rdbms
from google.appengine.api import users
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app
from dbModels.shift import *
from dbModels.employee import *
from dbModels.schedule import *

class makeNewSchedulePage(webapp2.RequestHandler):
    def get(self):
        self.response.headers["Content-Type"] = "text/html"
        self.response.out.write("""
                <html>
                    <head>
                        <title>Shifted</title>
                        <link rel="stylesheet" type="text/css" media="screen" href="beginLayout.css"/>
                        <script type="text/javascript">
                            function erase(id)
                            {
                                document.getElementById(id).select();
                            }
                        </script>
                    </head>                
                <body>
                <center><img align="center" src="Logo1.png"/>
                    <form action="/enterSiteNew" method="post">
                        <input type="text" size="20" id="1" maxlength="20" name="newName" value="Schedule Name" onclick="erase(id)"/>
                        <input type="submit" value="Make New Schedule"></input>
                    </form>
        e            <form action="/enterSiteOld" method="post">
                        <input type="text" size="20" id="2" maxlength="20" name="oldName" value="Old Key" onclick="erase(id)"/>
                        <input type="submit" value="Get Old Schedule From Key">
                    </form>
                    <form action="/enterSiteRand" method="post">
                        <input type="submit" value="Make Anonymous Schedule">
                    </form>
                </center>
                </body>
                </html>
                """)

class enterSiteNew(webapp2.RequestHandler):
    def post(self):
        name = self.request.get("newName")
		randKey = "".join(random.sample(string.letters+string.digits, 8))
        alreadyHere = db.GqlQuery("SELECT * from Schedule WHERE user = :1", randKey)
        while alreadyHere.count(1) is not 0:
            randKey = "".join(random.sample(string.letters+string.digits, 8))
        else:
            sched = Schedule(schedKey=randKey, schedName=name)
            sched.put()
            self.redirect("/shiftAddPage?schedId=" + newKey)

class enterSiteOld(webapp2.RequestHandler):
    def post(self):
        oldKey = self.request.get("oldName")
        alreadyHere = db.GqlQuery("SELECT * from Schedule WHERE user = :1", oldKey)
        if alreadyHere.count(1) is 0:
            self.redirect('/scheduleConflict')
        else:
            self.redirect('/shiftAddPage?schedId=' + oldKey)

class enterSiteRand(webapp2.RequestHandler):
    def post(self):
        randKey = "".join(random.sample(string.letters+string.digits, 8))
        alreadyHere = db.GqlQuery("SELECT * from Schedule WHERE user = :1", randKey)
        while alreadyHere.count(1) is not 0:
            randKey = "".join(random.sample(string.letters+string.digits, 8))
        sched = Schedule(schedKey=randKey)
        sched.put()
        self.redirect('/shiftAddPage?schedId=' + randKey)

class scheduleConflict(webapp2.RequestHandler):
    def get(self):
        self.response.headers["Content-Type"] = "text/html"
        self.response.out.write("""
                    <html>
                        <head>
                            <title>Shifted</title>
                        </head>                
                    <body>
                        The schedule or schedule name you requested<br>
                        is either not in our database or has already<br>
                        been taken by another user<br><br>
                        Please go back and try again.
                        <form action="/">
                            <input type="submit" id="2" value="Back">
                        </form>
                    </body>
                    </html>
                    """)

class shiftAddPage(webapp2.RequestHandler):
    def get(self):
        currentSchedule = self.request.get("schedId")
        if currentSchedule is None:
            self.redirect('/nope')
        else:
            self.response.headers["Content-Type"] = "text/html"
            self.response.out.write("""
                <html>
                    <head>
                        <title>Shifted</title>
                        <link rel="stylesheet" type="text/css" media="screen" href="layout.css"/>
                    </head>                
                <body>
                    <div id="header-block">
		    <h1>Welcome to <i>SHIFTED</i><br>
                        Current Schedule: %s</h1>
                    </div>
                    <div id="calender-block">
                """ % currentSchedule)
            shifts = db.GqlQuery("SELECT * from Shift WHERE user = :1 ORDER BY starttime", currentSchedule).fetch(20)
            
            for s in shifts:
                self.response.out.write("""<p class="shiftcolor">%s</p>""" % s)
            self.response.out.write("""
                </div>
                <div id="entry-block">
                <form action="/addShift? method="post">
		<h1>Enter New Shift:</h1>
		<input type="hidden" name="schedId" value="%s"/>
		<b>Shift Name</b>
		<input type="text" size="17" maxlength="20" name="shiftNameInput" value="name"/>
		<br><br>

		<b>Start Time</b>
		<input type="text" size="10" maxlength="5" name="startTimeInput" value="12:00"/>
		<select name="stc">
			<option value="AM">AM</option>
			<option value="PM">PM</option>
		</select>
		<br>

		<b>End Time </b>
		<input type="text" size="10" maxlength="5" name="endTimeInput" value="12:00"/>
		<select name="etc">
			<option value="AM">AM</option>
			<option value="PM">PM</option>
		</select>
		<br>
		<br>
		<b>Days of the Week</b><br>
			Mon<input type="checkbox" name="mon" value="off"/>
			Tue<input type="checkbox" name="tue" value="off"/>
			Wed<input type="checkbox" name="wed" value="off"/>
			Thu<input type="checkbox" name="thu" value="off"/>
			Fri<input type="checkbox" name="fri" value="off"/>
			Sat<input type="checkbox" name="sat" value="off"/>
			Sun<input type="checkbox" name="sun" value="off"/>
		<br>
		<br>

		<b>Number of Staff</b>
		<input type="text" size="10" maxlength="3" name="staffNumberInput" value="0"/>
			
		<br>
		<input type="submit" value="Add Shift"></input>
		</form>
		</div>
                </body>
                </html>
                """ % currentSchedule)
        
class addShift(webapp2.RequestHandler):
    def get(self):
        self.redirect('/')
        
        
class employeePreferencesPage(webapp2.RequestHandler):
    def get(self):
        self.redirect('/')
		# self.response.headers["Content-Type"] = "text/html"
        # self.response.out.write("""
            # <html>
				# <head>
					# <title>Shifted</title>
					# <link rel="stylesheet" type="text/css" media="screen" href="layout.css"/>
					# <script type="text/javascript">
					
		# The PLAN!!!!!!!!!
		# Step 1: Get the framing of a webpage up and running
		# Step 2: get the skeleton pieces in place without code behind them
		# Step 3: Wire Skeleton pieces together to make at least a user interface
		# Step 4: Wire user interface and results to datastore
		# Step 5: run through to make sure all moving parts have proper clearance
		# Step 6: ???
		# Step 7: PROFIT!!!

class addEmployee(webapp2.RequestHandler):
    def get(self):
        self.redirect('/')



app = webapp2.WSGIApplication([('/', makeNewSchedulePage),
                               ('/scheduleConflict', scheduleConflict),
                               ('/enterSiteNew', enterSiteNew),
                               ('/enterSiteOld', enterSiteOld),
                               ('/enterSiteRand', enterSiteRand),
                               ('/shiftAddPage', shiftAddPage),
                               ('/addShift', addShift),
                               ('/employeePreferencesPage', employeePreferencesPage),
                               ('/addPerson', addEmployee)],
                              debug=True)
								# NOTE. these are all regexps, so for our 8 digit stuff,
								# '(/(.)(.)(.)(.)(.)(.)(.)(.))+/*', parseDigits
								#
								# REGEXP above should match any positive number of 8 digit strings
								# preceded by a '/' with an optional one at the end
def main():
    run_wsgi_app(app)

if __name__ == "__main__":
    main()
