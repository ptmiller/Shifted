import datetime
from google.appengine.ext import db

class Schedule(db.Model):
	schedKey = db.StringProperty(required=True)
	schedName = db.StringProperty()
	isComplete = db.BooleanProperty()
	coord = db.StringProperty()   # coordinator's name
	email = db.EmailProperty()
#

	def __str__(self):
                string = "Key = %s, Name = %s" % (self.schedKey, self.schedName)
                return string
