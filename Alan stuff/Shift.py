import datetime
from google.appengine.ext import db
from google.appengine.api import users

class Shift(db.model):
	idNum = IntegerProperty()
	starttime = TimeProperty(required=True)
	startAMPM = db.StringProperty(required=True)
	endtime = TimeProperty(required=True)
	endAMPM = db.StringProperty(required=True)
	shiftName = db.StringProperty(required=True)
	mo = db.StringProperty(required=True)
	tu = db.StringProperty(required=True)
	we = db.StringProperty(required=True)
	th = db.StringProperty(required=True)
	fr = db.StringProperty(required=True)
	sa = db.StringProperty(required=True)
	su = db.StringProperty(required=True)
	staffNum = db.IntegerProperty(required=True)
	staffAss = db.IntegerProperty()
#
