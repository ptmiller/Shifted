from google.appengine.ext import db

class Shift(db.Model):
    user = db.StringProperty(required=True)
    idNum = db.StringProperty()
    starttime = db.StringProperty(required=True)
    startAMPM = db.StringProperty(required=True)
    endtime = db.StringProperty(required=True)
    endAMPM = db.StringProperty(required=True)
    shiftName = db.StringProperty(required=True)  
    assigned = db.StringListProperty()  
    day = db.StringProperty()
    staffNum = db.IntegerProperty() 

    def __str__(self):
        string = """
            %s: %s %s%s - %s%s""" % (self.shiftName, self.day, self.starttime, self.startAMPM, self.endtime, self.endAMPM)
        string = string + """<br>
            Number of Staff: %s""" % (self.staffNum)
        return string
