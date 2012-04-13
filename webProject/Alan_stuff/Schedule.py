import datetime
from google.appengine.ext import db
from google.appengine.api import users

class Schedule(db.model):
	key = db.TextProperty(required=True)
	isComplete = BooleanProperty()
	entry = db.LinkProperty()
	results	= db.TextProperty()
	coord = db.TextProperty()   # coordinator's name
	email = db.EmailProperty(required=True)
#
