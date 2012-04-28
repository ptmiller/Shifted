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
