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
from google.appengine.ext import db
from google.appengine.api import rdbms
from google.appengine.api import users
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app

class Shift(db.Model):
    user = db.StringProperty(required=True)
    idNum = db.StringProperty()
    starttime = db.StringProperty(required=True)
    startAMPM = db.StringProperty(required=True)
    endtime = db.StringProperty(required=True)
    endAMPM = db.StringProperty(required=True)
    shiftName = db.StringProperty(required=True)    
    mo = db.StringProperty()
    tu = db.StringProperty()
    we = db.StringProperty()
    th = db.StringProperty()
    fr = db.StringProperty()
    sa = db.StringProperty()
    su = db.StringProperty()
    staffNum = db.StringProperty() 

    def __str__(self):
        string = """Calender Owner:  %s<br>
                Shift ID Number: %s<br>
                Shift Name:      %s<br>
                Time:            %s%s - %s%s<br>
                Days of Week:    """ % (self.user, self.idNum, self.shiftName, self.starttime, self.startAMPM, self.endtime, self.endAMPM)
        if self.mo:
            string = string + "Mo "
        if self.tu:
            string = string + "Tu "
        if self.we:
            string = string + "We "
        if self.th:
            string = string + "Th "
        if self.fr:
            string = string + "Fr "
        if self.sa:
            string = string + "Sa "
        if self.su:
            string = string + "Su "
        string = string + """<br>
            Number of Staff: %s""" % (self.staffNum)
        return string

class EmployeeM(db.Model):
    user = db.StringProperty(required=True)
    keyy = db.StringProperty(required=True)
    email = db.StringProperty(required=True)
    choices = db.StringProperty()
    rating = db.StringProperty()

    def __str__(self):
	return "%s (%s): %s <b>%s</b>" % (self.email, self.keyy, self.choices, self.rating)
    
class MainHandler(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if user is None:
            self.redirect(users.create_login_url(self.request.uri))
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
		    <h1>Welcome to <i>SHIFTED</i></h1>
                    </div>
                    <div id="calender-block">
                """)
            shifts = db.GqlQuery("SELECT * from Shift ORDER BY starttime").fetch(20)
            shifts.reverse()
            
            for s in shifts:
                self.response.out.write("<p>%s</p>" % s)
            self.response.out.write("""
                </div>
                <div id="entry-block">
                <form action="/talk" method="post">
		<h1>Enter New Shift:</h1>
			
		<b>Shift Name</b>
		<input type="text" size="17" maxlength="20" name="shiftNameInput" value="name"/>
		<br><br>

		<b>ID Number</b>
		<input type="text" size="17" maxlength="20" name="idNum" value="000"/>
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
		<form action="/addPersonel">
		<input type="submit" value="Done Adding Shifts"></input>
		</form>
		</div>
                </body>
                </html>
                """)

class addShift(webapp2.RequestHandler):
    def post(self):
        thing1 = users.get_current_user()
        if thing1 is None:
            self.redirect(users.create_login_url(self.request.uri))
        else:
            user1 = thing1.nickname()
            idn = self.request.get("idNum")
            st = self.request.get("startTimeInput")
            stap = self.request.get("stc")
            et = self.request.get("endTimeInput")
            etap = self.request.get("etc")
            sn = self.request.get("shiftNameInput")
            mon = self.request.get("mon")
            tue = self.request.get("tue")
            wed = self.request.get("wed")
            thu = self.request.get("thu")
            fri = self.request.get("fri")
            sat = self.request.get("sat")
            sun = self.request.get("sun")
            stfn = self.request.get("staffNumberInput")
            shft = Shift(user=user1, idNum=idn, starttime=st, startAMPM=stap, endtime=et, endAMPM=etap, shiftName=sn, mo=mon, tu=tue, we=wed, th=thu, fr=fri, sa=sat, su=sun, staffNum=stfn)
            shft.put()
            self.redirect('/')

class newEmployee(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if user is None:
            self.redirect(users.create_login_url(self.request.uri))
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
		    <h1>Add Employee Page</h1>
                    </div>
                    <div id="calender-block">
                """)
            employees = db.GqlQuery("SELECT * from EmployeeM ORDER BY email").fetch(20)
            
            for e in employees:
                self.response.out.write("<p>%s</p>" % e)
            self.response.out.write("""
                </div>
                <div id="entry-block">
                <form action="/addPerson" method="post">
		<h1>Add New Employee:</h1>
			
		<b>Key</b>
		<input type="text" size="17" maxlength="20" name="ekey" value="ABC"/>
		<br><br>

		<b>Email</b>
		<input type="text" size="17" maxlength="20" name="eemail" value="jdoe@fake.com"/>
		<br><br>

		<b>Choices</b>
		<input type="text" size="10" maxlength="100" name="ch" value="Choices"/>
		<br>

		<b>Rating </b>
		<input type="text" size="10" maxlength="3" name="rtn" value="000"/>	
		<br>
		<input type="submit" value="Add Employee"></input>
		</form>
		</div>
                </body>
                </html>
                """)

class addEmployee(webapp2.RequestHandler):
    def post(self):
        user2 = users.get_current_user()
        if user2 is None:
            self.redirect(users.create_login_url(self.request.uri))
        else:
            user1 = user2.nickname()
            key1 = self.request.get("ekey")
            email1 = self.request.get("eemail")
            choices1 = self.request.get("ch")
            rating1 = self.request.get("rtn")
            emp = EmployeeM(user=user1, keyy=key1, email=email1, choices=choices1, rating=rating1)
            emp.put()
            self.redirect('/addPersonel')


app = webapp2.WSGIApplication([('/', MainHandler),
                               ('/talk', addShift),
                               ('/addPersonel', newEmployee),
                               ('/addPerson', addEmployee)],
                              debug=True)

def main():
    run_wsgi_app(app)

if __name__ == "__main__":
    main()
