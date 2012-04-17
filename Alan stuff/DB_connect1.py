# This set of functions merely creates and recalls shifts, schedules, or employees. nothing more
# Note that names are used as keys, so they must be unique
# There is also a function to clean out the datastore of test information.

import datetime
from google.appengine.ext import db
import Shift.py
import Employee.py
import Schedule.py

def make_shift(starttime, startAMPM, endtime, endAMPM, shiftName, mo, tu, we, th, fr, sa, su, staffNum ):
	shift = Shift(key_name=shiftName)
	shift.starttime = starttime
	shift.startAMPM = startAMPM
	shift.endtime = endtime
	shift.endAMPM = endAMPM
	shift.shiftName = shiftName
	shift.mo = mo
	shift.tu = tu
	shift.we = we
	shift.th = th
	shift.fr = fr
	shift.sa = sa
	shift.su = su
	shift.staffNum = staffNum
	shift.put()
#

def make_employee(name, email):
	employee = Employee(key_name=name)
	employee.name = name
	employee.email = email
	employee.put()
#

def make_schedule(coord, email):
	sched = Schedule()
	sched.coord = coord
	sched.email = email
	sched.put()
#

def find_shift(input_str):
	query = GqlQuery("SELECT * FROM Shift WHERE starttime = :1", input_str)
	for shift in query:
		print shift.name shift.starttime shift.endtime
	#
	
	query = GqlQuery("SELECT * FROM Shift WHERE endtime = :1", input_str)
	for shift in query:
		print shift.name shift.starttime shift.endtime
	#
	
	query = GqlQuery("SELECT * FROM Shift WHERE shiftname = :1", input_str)
	for shift in query:
		print shift.name shift.starttime shift.endtime
#

def find_employee(input_str):
	query = GqlQuery("SELECT * FROM Employee WHERE name = :1", input_str)
	for emp in query:
		print emp.name emp.email
	#
	
	query = GqlQuery("SELECT * FROM Employee WHERE email = :1", input_str)
	for emp in query:
		print emp.name emp.email
	#	
#

def find_schedule(input_str):
	query = GqlQuery("SELECT * FROM Schedule WHERE coord = :1", input_str)
	for sched in query:
		print sched.coord sched.email
	#

	query = GqlQuery("SELECT * FROM Schedule WHERE email = :1", input_str)
	for sched in query:
		print sched.coord sched.email
	#
#

def clear_store():
	query = GqlQuery("SELECT __key__ FROM Employee")
	for emp in query
		db.delete(emp)
	#
	
	query = GqlQuery("SELECT __key__ FROM Shift")
	for shift in query
		db.delete(shift)
	#
	
	query = GqlQuery("SELECT __key__ FROM Schedule")
	for sched in query
		db.delete(sched)
	#
#