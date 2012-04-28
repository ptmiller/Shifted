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

class deleteShift(webapp2.RequestHandler):
    def post(self):
        currentShift = self.request.get("doomedShift")
        currentSchedule = self.request.get("schedId")
        shift = db.GqlQuery("SELECT * from Shift WHERE user = :1 and idNum = :2", currentSchedule, currentShift)
        db.delete(shift)
        self.redirect('/shiftAddPage?schedId=' + currentSchedule)
		
class addEmployee(webapp2.RequestHandler):
    def get(self):
	nkeyy = "".join(random.sample(string.letters+string.digits, 5))
	nEmp = Employee(user=self.request.get("schedId"), keyy=nkeyy, email=self.request.get("email"))
	nEmp.put()
	self.redirect('/empThanksPage?schedId=' + schedId + '&empId=' + nkeyy)

class deleteEmployee(webapp2.RequestHandler):
	def post(self):
		currentEmp = self.request.get("doomedEmployee")
		currentSchedule = self.request.get("schedId")
		emp = db.GqlQuery("SELECT * from Employee WHERE user = :1 and keyy = :2", currentSchedule, currentEmp)
		db.delete(emp)
		self.redirect('/')
