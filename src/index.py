'''
Created on Aug 9, 2013

@author: Ola
'''
import webapp2, jinja2, os
from google.appengine.ext import db
import json


JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__) + "/static/templates"),
    extensions=['jinja2.ext.autoescape'])

        
        
class Index(webapp2.RequestHandler):
    def get(self):
        template = JINJA_ENVIRONMENT.get_template('index.html')
        self.response.write(template.render(title = 'College Essays'))
    