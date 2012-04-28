parseDigits(webapp2.RequestHandler):
	digits = self.request.get
	query = db.GqlQuery("SELECT * FROM * WHERE id=:1", digits)
	self.response.headers["Content-Type"] = "text/html"
    self.response.out.write("""
		<html>
            <head>
				<title>""" + digits + """</title>
            </head> 
		</html>""")
	#
#