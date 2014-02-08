'''
Created on Aug 9, 2013

@author: Ola
'''
import webapp2, jinja2, os
from google.appengine.ext import db
from google.appengine.ext import blobstore
from google.appengine.api import users
import zipfile

from models.pad import Pad
from py_etherpad import EtherpadLiteClient

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader('static/templates'),
    extensions=['jinja2.ext.autoescape'])

 
        
class ViewPads(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if user:
            template = JINJA_ENVIRONMENT.get_template('view_pads.html')
            pads = Pad.query(Pad.owner==user.email())
            self.response.write(template.render(title = 'My Pads', pads=pads))
        else:
            self.redirect(users.create_login_url(self.request.uri))
