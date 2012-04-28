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
