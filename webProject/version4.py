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
import re
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
                        <input type="text" size="20" id="1" maxlength="20" name="newName" value="Schedule Name" onclick="erase(id)"></input>
                        <input type="submit" value="Make New Schedule"></input>
                    </form>
                    <form action="/enterSiteOld" method="post">
                        <input type="text" size="20" id="2" maxlength="20" name="oldName" value="Old Key" onclick="erase(id)"></input>
                        <input type="submit" value="Get Old Schedule From Key"></input>
                    </form>
                    <form action="/enterSiteRand" method="post">
                        <input type="submit" value="Make Anonymous Schedule"></input>
                    </form>
                </center>
                </body>
                </html>
                """)

class enterSiteNew(webapp2.RequestHandler):
    def post(self):
	name = self.request.get("newName")
	randKey = "".join(random.sample(string.letters+string.digits, 8))
        alreadyHere = db.GqlQuery("SELECT * from Schedule WHERE schedKey = :1", randKey)
        while alreadyHere.count() is not 0:
            randKey = "".join(random.sample(string.letters+string.digits, 8))
            alreadyHere = db.GqlQuery("SELECT * from Schedule WHERE schedKey = :1", randKey)
        sched = Schedule(schedKey=randKey, schedName=name)
        sched.put()

        self.redirect("/shiftAddPage?schedId=" + sched.schedKey)

class parseDigits(webapp2.RequestHandler):
    def post(self):
        digits = self.request.get("schedId")
	query = db.GqlQuery("SELECT * FROM * WHERE id=:1", digits)
	self.response.headers["Content-Type"] = "text/html"
        self.response.out.write("""
		<html>
            <head>
				<title>""" + stuff + """</title>
            </head> 
		</html>""")
		
class enterSiteOld(webapp2.RequestHandler):
    def post(self):
        oldKey = self.request.get("oldName")
        alreadyHere = db.GqlQuery("SELECT * from Schedule WHERE schedKey = :1", oldKey)
        if alreadyHere.count(1) is 0:
            self.redirect('/scheduleConflict?' + str(alreadyHere.count(1)))
        else:
            self.redirect('/shiftAddPage?schedId=' + oldKey)

class enterSiteRand(webapp2.RequestHandler):
    def post(self):
	randKey = "".join(random.sample(string.letters+string.digits, 8))
        alreadyHere = db.GqlQuery("SELECT * from Schedule WHERE schedKey = :1", randKey)
        while alreadyHere.count() is True:
            randKey = "".join(random.sample(string.letters+string.digits, 8))
            alreadyHere = db.GqlQuery("SELECT * from Schedule WHERE schedKey = :1", randKey)
        sched = Schedule(schedKey=randKey, schedName=randKey)
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
                            <input type="submit" id="2" value="Back"></input>
                        </form>
                    </body>
                    </html>
                    """)

class shiftAddPage(webapp2.RequestHandler):
    def get(self):
        currentSchedule = self.request.get("schedId")
        if currentSchedule is "":
            self.redirect('/scheduleConflict')
        else:
            link = "http://zshiftedz.appspot.com/employeePreferencesPage?schedId=" + currentSchedule
            self.response.headers["Content-Type"] = "text/html"
            self.response.out.write("""
                <html>
                    <head>
                        <title>Shifted</title>
                        <link rel="stylesheet" type="text/css" media="screen" href="layout.css"/>
                        <script type="text/javascript">
                            function isInt()
                            {
                                var input = document.getElementById("3");
                                var intPatt = /^\d+$/;
                                intPatt.compile(intPatt);
                                if (intPatt.test(input.value) == false) {
                                    input.value = "0";
                                    document.getElementById(3).select();
                                    alert("Please enter a valid integer.");
                                }
                            }
                        </script>
                        <script type="text/javascript">
                            functon checkTime(id)
                            {
                                alert("What the hell!!??!!?");
                                var time = document.getElementById(id);

                                var timePatt = /(1[0-2])|(0?[1-9]):[0-5][0-9]/;
                                timePatt.compile(timePatt);

                                if (timePatt.test(time.value) == false) {
                                    alert("please input correct time values\nformat: 01 - 12 : 00 - 59");
                                    sTc.value = "12:00";
                                }
                            }
                        </script>
                    </head>                
					<body>
						<div id="header-block">
							<h1>Welcome to <i>SHIFTED</i><br>
								<font size="3">Current Schedule: %s</font><br>
								<font size="3">Send following link to employees/participants: %s</font></h1>
						</div>
						<div id="calender-block">
							""" % (currentSchedule, link))
            shifts = db.GqlQuery("SELECT * from Shift WHERE user = :1 ORDER BY starttime", currentSchedule).fetch(20)
            
            for s in shifts:
                self.response.out.write("""<p class="shiftcolor">%s
                        <form action="/deleteShift" method="post">
                            <input type="hidden" name="doomedShift" value=%s></input>
                            <input type="hidden" name="schedId" value=%s></input>
                            <input type="submit" value="delete"></input>
                        </form>
                    </p>""" % (s, s.idNum, s.user))
           
	    self.response.out.write("""
			</div>
			<div id="entry-block">
				<form action="/addShift? method="post">
					<h1>Enter New Shift:</h1>
					<input type="hidden" name="schedId" value="%s"></input>
					<b>Shift Name</b>
					<input type="text" size="17" maxlength="20" name="shiftNameInput" value="name"></input>
					<br><br>
					<b>Start Time</b>
					<input type="text" size="10" maxlength="5" name="startTimeInput" value="12:00" id="4" onblur="checkTime(id)"></input>
					<select name="stc">
						<option value="AM">AM</option>
						<option value="PM">PM</option>
					</select>
					<br>
					<b>End Time </b>
					<input type="text" size="10" maxlength="5" name="endTimeInput" value="12:00" id="5" onblur="checkTime(id)"></input>
					<select name="etc">
						<option value="AM">AM</option>
						<option value="PM">PM</option>
					</select>
					<br><br>
					<b>Days of the Week</b><br>
						Mon<input type="checkbox" name="mon" value="off"></input>
						Tue<input type="checkbox" name="tue" value="off"></input>
						Wed<input type="checkbox" name="wed" value="off"></input>
						Thu<input type="checkbox" name="thu" value="off"></input>
						Fri<input type="checkbox" name="fri" value="off"></input>
						Sat<input type="checkbox" name="sat" value="off"></input>
						Sun<input type="checkbox" name="sun" value="off"></input>
					<br><br>
						<b>Number of Staff</b>
					<input id="3" type="text" size="10" maxlength="3" name="staffNumberInput" value="0" onkeyup="isInt()"></input>
					<br>
						<input type="submit" value="Add Shift"></input>
				</form>
                               <form action="/results" method="post"> 
									<input type="hidden" value="%s" name="schedId"></input>
									<input type="submit" value="Done Adding Shifts"></input> 
								</form>			</div>
			</body>
                   </html>
            """ % (currentSchedule,currentSchedule))
        
class addShift(webapp2.RequestHandler):
    def get(self):
        sched = self.request.get("schedId")
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
        stfN = int(stfn)
        if mon:
            shft = Shift(user=sched, idNum="".join(random.sample(string.letters+string.digits, 5)), starttime=st, startAMPM=stap, endtime=et, endAMPM=etap, shiftName=sn, day="Mon", staffNum=stfN)
            shft.put()
        if tue:
            shft = Shift(user=sched, idNum="".join(random.sample(string.letters+string.digits, 5)), starttime=st, startAMPM=stap, endtime=et, endAMPM=etap, shiftName=sn, day="Tue", staffNum=stfN)
            shft.put()
        if wed:
            shft = Shift(user=sched, idNum="".join(random.sample(string.letters+string.digits, 5)), starttime=st, startAMPM=stap, endtime=et, endAMPM=etap, shiftName=sn, day="Wed", staffNum=stfN)
            shft.put()
        if thu:
            shft = Shift(user=sched, idNum="".join(random.sample(string.letters+string.digits, 5)), starttime=st, startAMPM=stap, endtime=et, endAMPM=etap, shiftName=sn, day="Thu", staffNum=stfN)
            shft.put()
        if fri:
            shft = Shift(user=sched, idNum="".join(random.sample(string.letters+string.digits, 5)), starttime=st, startAMPM=stap, endtime=et, endAMPM=etap, shiftName=sn, day="Fri", staffNum=stfN)
            shft.put()
        if sat:
            shft = Shift(user=sched, idNum="".join(random.sample(string.letters+string.digits, 5)), starttime=st, startAMPM=stap, endtime=et, endAMPM=etap, shiftName=sn, day="Sat", staffNum=stfN)
            shft.put()
        if sun:
            shft = Shift(user=sched, idNum="".join(random.sample(string.letters+string.digits, 5)), starttime=st, startAMPM=stap, endtime=et, endAMPM=etap, shiftName=sn, day="Sun", staffNum=stfN)
            shft.put()
        self.redirect('/shiftAddPage?schedId=' + sched)
		
class addEmployee(webapp2.RequestHandler):
    def get(self):
	nkeyy = "".join(random.sample(string.letters+string.digits, 5))
	choiceString = self.request.get("choices")
	choices = string.split(choiceString, ",")
	nEmp = Employee(user=self.request.get("schedId"), keyy=nkeyy, email=self.request.get("email"))
	nEmp.put()
	self.redirect('/empThanksPage?schedId=' + schedId + '&empId=' + nkeyy)

class empThanksPage(webapp2.RequestHandler):
    def get(self):
	sched = self.request.get("schedId")
	emp = self.request.get("empId")
	urlS = "http://zshiftedz.appspot.com/employeePreferencesPage?schedId=" + sched + "&empId" + emp
	self.response.out.write("""
        <html>
            <head>
                <title>Shifted</title>
            </head>
            <body>
                <h1>Thank you for your response !</hi><br clear="both />
                <p>Keep the following url to update your preferences at any time:</P><br>
                <a href=%s>%s
            </body>
        </html>""" % (urlS,urlS))
#
        
class employeePreferencesPage(webapp2.RequestHandler):
    def get(self):
        currentSchedule = self.request.get("schedId")
	currentEmployee = self.request.get("empId")
        if currentSchedule is None:
            self.redirect('/nope')
        else:
            self.response.headers["Content-Type"] = "text/html"
            self.response.out.write("""
				<!DOCTYPE html>
				<html lang="en">
					<head>
						<meta charset="utf-8">
						<title>Shifted:: Enter your shift preferences</title>
						<link rel="stylesheet" href="./jQuery/development-bundle/themes/base/jquery.ui.all.css">
						<script src="./jQuery/development-bundle/jquery-1.7.2.js"></script>
						<script src="./jQuery/development-bundle/ui/jquery.ui.core.js"></script>
						<script src="./jQuery/development-bundle/ui/jquery.ui.widget.js"></script>
						<script src="./jQuery/development-bundle/ui/jquery.ui.mouse.js"></script>
						<script src="./jQuery/development-bundle/ui/jquery.ui.sortable.js"></script>
						<link rel="stylesheet" href="./jQuery/development-bundle/demos.css">
						<style>
						.column { width: 270px; float: left; padding-bottom: 100px; }
						.hhh {width: 270px; float: left; }
						.portlet { margin: 0 0.5em 0.5em 0; }
						.portlet-header { margin: 0.3em; padding-bottom: 4px; padding-left: 0.2em; }
						.portlet-header .ui-icon { float: right; }
						.portlet-content { padding: 0.4em; }
						.ui-sortable-placeholder { border: 1px dotted black; visibility: visible !important; height: 50px !important; }
						.ui-sortable-placeholder * { visibility: hidden; }	</style>
						<script>
						$(function() {
							$( ".column" ).sortable({
								connectWith: ".column"
							});

							$( ".portlet" ).addClass( "ui-widget ui-widget-content ui-helper-clearfix ui-corner-all" )
								.find( ".portlet-header" )
									.addClass( "ui-widget-header ui-corner-all" )
									.prepend( "<span class='ui-icon ui-icon-plusthick'></span>")
									.end()
								.find( ".portlet-content" ).toggle();
								
							$( ".portlet-header .ui-icon" ).click(function() {
								$( this ).toggleClass( "ui-icon-minusthick" ).toggleClass( "ui-icon-plusthick" );
								$( this ).parents( ".portlet:first" ).find( ".portlet-content" ).toggle();
							});

							$( ".column" ).disableSelection();
						});
						function button_click() {
							var input = document.getElementById("List2");
							var email = document.getElementById("1");
							var name = document.getElementById("2");
							var schedId = document.getElementById("sc")
							var result = $('#List2').sortable("toArray"); 
							<!-- alert("Shifts: " + result.toString() + "\nE-mail: " + email.value + "\nName: " + name.value); -->
							window.location("http://zshiftedz.appspot.com/addEmployee?schedId=" + schedId + "&email=" + email + "&choices=" + result.toString())
							<!-- if sched id is given in url, make a new employee. -->
							<!-- addEmployee(schedId, result, email.value, name.value) -->
							
							<!-- if employee id is given, update -->
							<!-- enter shifts into employee by id -->
							<!-- enter name into employee -->
							<!-- enter email into employee -->
							<!-- redirect to thank-you page with link to update these prefs -->
						}
						function erase(id) {
							document.getElementById(id).select();
						}
						</script>
					</head>
					<body>
						<div id="header-block">
							<h1>Welcome to <i>SHIFTED</i><br clear="both" /></h1>
						</div>
						<div id="columns">
							<div class="hhh" id="header1">
								<h2>All Shifts</h2>
							</div>
							<div class="hhh" id="header2">
								<h2>Desired Shifts</h2>
							</div>
							<br clear="both" />
							<div class="column" id="List1">
								<!-- if an employee id is given, use the employee. if a schedule id is given, use sched -->""")

            schedQ = db.GqlQuery("SELECT * FROM Schedule WHERE schedKey=:1", currentSchedule)
            schedK = 0
            #shiftQ = None
            for sc in schedQ:
                schedK = sc.schedKey
                shiftQ = db.GqlQuery("SELECT * FROM Shift WHERE user=:1", schedK)
            if (currentEmployee == ""):
                for sh in shiftQ:
                    self.response.out.write("""<div class="portlet" id="%s">\n""" % sh.idNum)
                    self.response.out.write("""<div class="portlet-header">%s</div>\n""" % sh.shiftName)
                    self.response.out.write("""<div class="portlet-content">This feature has not yet been implemented</div>\n""")
                    self.response.out.write("""</div>
						</div>
						<div class="column" id="List2"></div>
							</div>
							<div id="user_info">
								<form>
									<input type="text" size="20" id="1" maxlength="50" name="email_field" value="Enter your e-mail" onclick="erase(id)"/>
									<br>
									<input type="text" size="20" id="2" maxlength="50" name="name_field" value="Enter your name" onclick="erase(id)"/>
									<br>
									<input type="hidden" value="%s" name="schedId"></input>
									<button type="button" onclick="button_click()">Submit</button>
								</form>
							</div>
						</body>
					</html>""" % currentSchedule)
				#
            else:
		empQ = db.GqlQuery("SELECT * FROM Employee WHERE keyy=:1", currentEmployee)
		for e in empQ:
		    skip = False
                    for sh in shiftQ: 
			for ds in e.choices:
			    if (sh.idNum == ds):
				skip = True
                            #
			#
                        if (skip == False):
			    self.response.out.write("""<div class="portlet" id="%s">\n""" % sh.idNum)
                            self.response.out.write("""<div class="portlet-header">%s</div>\n""" % sh.shiftName)
                            self.response.out.write("""<div class="portlet-content">This feature has not yet been implemented</div>\n""")
                            self.response.out.write("""</div>\n""")
                        #
                    self.response.out.write("""</div>\n<div class="column" id="List2">""")
		    for ds in e.choices:
                        shQ = db.GqlQuery("SELECT * FROM Shift WHERE idNum=:1", ds)
                        for s in shQ:
                            self.response.out.write("""<div class="portlet" id="%s">\n""" % s.idNum)
                            self.response.out.write("""<div class="portlet-header">%s</div>\n""" % s.shiftName)
			    self.response.out.write("""<div class="portlet-content">This feature has not yet been implemented</div>\n""")
			    self.response.out.write("""</div>\n""")
                        #
		    #
		    self.response.out.write("""
									</div>
								</div>
								<div id="user_info">
									<form>
										<input type="text" size="20" id="1" maxlength="50" name="email_field" value=%s onclick="erase(id)"/>
										<br>""" % e.email)
		    self.response.out.write("""<input type="text" size="20" id="2" maxlength="50" name="name_field" value="Enter your name" onclick="erase(id)"/>
										<br>
										<input type="hidden" value="%s" name="schedId" id="sc"></input>
                                                                                <button type="button" onclick="button_click()">Submit</button>
									</form>
								</div>
							</body>
						</html>""" % currentSchedule)
					#
				#
			#
		#
	#
#

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
        

class deleteShift(webapp2.RequestHandler):
    def post(self):
        currentShift = self.request.get("doomedShift")
        currentSchedule = self.request.get("schedId")
        shift = db.GqlQuery("SELECT * from Shift WHERE user = :1 and idNum = :2", currentSchedule, currentShift)
        db.delete(shift)
        self.redirect('/shiftAddPage?schedId=' + currentSchedule)

class thankYouPage(webapp2.RequestHandler):
    def get(self):
        self.redirect('/')

class Optimize(webapp2.RequestHandler):
    def post(self):
		currentSchedule = self.request.get("schedId")
		if currentSchedule is None:
			self.redirect('/nope')
		shifts = db.GqlQuery("SELECT * from Shift WHERE user = :1 ORDER BY starttime", currentSchedule).fetch(1000)
		for s in shifts:
			self.response.out.write("""<p> %s </p>""" % s)
		emps = db.GqlQuery("SELECT * from Employee WHERE user = :1 ORDER BY keyy", currentSchedule).fetch(1000)
		for e in emps: 
			self.response.out.write("""<p> %s </p>""" % e)
		self.response.out.write(len(emps))
		
		# begin the draconian optimization algorithm
		# these keep track of data that is collected at the start and gradually discarded
		matrix_haters = [[10000]*len(shifts) for i in range(len(emps))]
		shifts_to_fill = [0]*len(shifts)
		shift_prefs_remaining = [0]*len(emps)
		
		# these keep track of data during the run-throughs
		choice_employee = [0]*len(shifts)
		badness = [10000]*len(shifts)
		
		#fill out the matrix and the lists
		for i in range(len(shifts)):
			shifts_to_fill[i] = shifts[i].staffNum
			for j in range(len(emps)):
				pref = 1000
				# check through the employee's preferences to see whether the shift is contained
				for k in range(len(emps[j].choices)):
					if emps[j].choices[k] == shifts[i].idNum:
						pref = k
					#
				matrix_haters[i][j] = pref
				shift_prefs_remaining[j] = len(emps[j].choices)
			#
		#
		
		# The main loop; every time through, one shift-employee pair will be assigned
		while True:
			# determine which shift-employee pair to assign
			
			# find the "best" badness for every shift
			for i in range(len(shifts)):
				if shifts_to_fill[i] == 0:
					# cannot fill shift, because it is already full
					badness[i] = 0
					continue
				# find the employee with the "best" badness rating, for this particular shift
				best = 1000
				for j in range(len(emps)):
					bad = matrix_haters[i][j]
					# find the best other shift available
					best2 = 1000
					for k in range(len(shifts)):
						if k == i:
							continue
						if matrix_haters[k][j] < best2:
							best2 = matrix_haters[k][j]
						# badness = preference level * 2 - best other option preference
						# level + number of shifts remaining to fill on this shift
					bad = bad * 2 - best2 + shifts_to_fill[i] 
					if bad < best:
						best = bad
						choice_employee[i] = j
					#
				if best >= 1000:
					# cannot fill shift, because no one wants it
					shifts_to_fill[i] = 0
					badness[i] = 0
					continue
				#
			# find the shift with the "worst best" badness
			worst = 0
			shift_choice = 0
			for i in range(len(shifts)):
				if badness[i] > worst:
					worst = badness[i]
					shift_choice = i
				#
			if worst == 0:
				# no shifts could be filled
				break
			# assign the shift to its choice employee, both know whom they own
			shifts[shift_choice].assigned.append(emps[choice_employee[shift_choice]].keyy)
			emps[choice_employee[shift_choice]].assignments.append(shifts[shift_choice].idNum)
			
			# clear information that has been used
			# clear the specific employee preference for this shift
			matrix_haters[shift_choice][choice_employee[shift_choice]] = 10000
			# decrement number of shifts to fill for this shift
			shifts_to_fill[shift_choice] = shifts_to_fill[shift_choice] - 1
			# decrement number of preferred shifts remaining for this employee
			shift_prefs_remaining[choice_employee[shift_choice]] = shift_prefs_remaining[choice_employee[shift_choice]] - 1
			if shifts_to_fill[shift_choice] <= 0:
				# shift has been completely filled, remove preferences among employees
				for i in range(len(emps)):
					matrix_haters[shift_choice][i] = 10000
				#
			#
		# all shifts have been assigned; that's all folks


app = webapp2.WSGIApplication([('/', makeNewSchedulePage),
                               ('/scheduleConflict', scheduleConflict),
                               ('/enterSiteNew', enterSiteNew),
                               ('/enterSiteOld', enterSiteOld),
                               ('/enterSiteRand', enterSiteRand),
                               ('/shiftAddPage', shiftAddPage),
                               ('/addShift', addShift),
                               ('/employeePreferencesPage', employeePreferencesPage),
                               ('/deleteShift', deleteShift),
                               ('/thankYouPage', thankYouPage),
                               ('/Optimize', Optimize),
                               ('/results', results),
                               ('/empThanksPage', empThanksPage),
                               ('/parseDigits', parseDigits)],
                               debug=True)

def main():
    run_wsgi_app(app)

if __name__ == "__main__":
    main()
