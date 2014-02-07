'''
Created on Aug 9, 2013

@author: Ola
'''
import webapp2, jinja2, os
from google.appengine.ext import db
import json


JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__) + "/assets/templates"),
    extensions=['jinja2.ext.autoescape'])
class Question(webapp2.RequestHandler):
    def get(self):
        question = db.GqlQuery("SELECT * FROM Objective").fetch(1)[0]
        self.response.headers['Content-Type'] = 'application/json'
        obj = {'question': question.question,
               'answer': question.question}
        self.response.out.write(json.dumps(obj))
        
        
class Index(webapp2.RequestHandler):
    def get(self):
        #self.initialize_database()
        template = JINJA_ENVIRONMENT.get_template('index.html')
        #questions = db.GqlQuery("SELECT * from  Objective")
        #self.response.write(template.render({'questions':questions}))
        self.response.write(template.render(title = 'Past Questions'))
    