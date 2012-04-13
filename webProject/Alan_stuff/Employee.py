import datetime
from google.appengine.ext import db
from google.appengine.api import users

class Employee(db.model):
	key = db.TextPropety(required=True)
	email = db.EmailProperty(required=True)
	choices = db.TextProperty()
	rating = db.RatingProperty()
#
