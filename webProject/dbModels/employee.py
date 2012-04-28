from google.appengine.ext import db

class Employee(db.Model):
    user = db.StringProperty(required=True)
    keyy = db.StringProperty(required=True)
    email = db.StringProperty(required=True)
    choices = db.StringListProperty()
    assignments = db.StringListProperty()
    rating = db.StringProperty()

    def __str__(self):
		return "%s (%s): %s <b>%s</b>" % (self.email, self.keyy, self.choices, self.rating)

