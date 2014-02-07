'''
Created on Jan 9, 2014

@author: Ola
'''
from google.appengine.ext import ndb
from models.question import Objective, Essay
import webapp2, jinja2

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader('static/templates/admin'),
    extensions=['jinja2.ext.autoescape'])

JINJA_ENVIRONMENT.filters['webapp2'] = webapp2

class Add(webapp2.RequestHandler):
    def get(self):
        template = JINJA_ENVIRONMENT.get_template(
           'add_question.html')
        self.response.write(template.render())
        
class Edit(webapp2.RequestHandler):
    def get(self, questionKey):
        template = JINJA_ENVIRONMENT.get_template(
           'add_question_by_id.html')
        try:
            question = ndb.Key(urlsafe=questionKey).get()
        except:
            self.abort(404)
        self.response.write(template.render(question = question))
