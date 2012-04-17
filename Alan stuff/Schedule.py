import datetime
import Shift.py
import Employee.py
from google.appengine.ext import db
from google.appengine.api import users

class Schedule(db.model):
	key = db.TextProperty(required=True)
	isComplete = BooleanProperty()
	entry = db.LinkProperty()
	results	= {} # db.TextProperty()
	coord = db.TextProperty(required=True)   # coordinator's name
	email = db.EmailProperty(required=True)
	shifts = []
	emps = []

	#--------Optimizer code---------------------------------
	def optimize(self)
	
#

