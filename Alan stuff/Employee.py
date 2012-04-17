import datetime
from google.appengine.ext import db
from google.appengine.api import users

class Employee(db.model):
	name = db.TextPropety(required=True)
	email = db.EmailProperty(required=True)
	choices = db.TextProperty()
	prefs = [] #convert choices to list
	rating = db.RatingProperty()
	shifts_assigned = db.IntegerProperty()
#
