import datetime
from google.appengine.ext import db

class Schedule(db.Model):
	schedKey = db.TextProperty(required=True)
	schedName = db.TextProperty()
	isComplete = db.BooleanProperty()
	entry = db.LinkProperty()
	results	= db.TextProperty()
	coord = db.TextProperty()   # coordinator's name
	email = db.EmailProperty()
        assigned = db.StringListProperty()
#
