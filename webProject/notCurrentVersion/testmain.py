import webapp2
import os
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app

class Page(webapp2.RequestHandler):
    def get(self):

app = webapp2.WSGIApplication([('/', Page)],
                              debug=True)

def main():
    run_wsgi_app(app)

if __name__ == "__main__":
    main()
