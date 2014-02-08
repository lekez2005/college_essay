'''
Created on Aug 9, 2013

@author: Ola
'''
import webapp2, jinja2, os
from google.appengine.ext import db
from google.appengine.ext import blobstore
from google.appengine.api import users
import ndb_json
from models.pad import Pad, logging
from py_etherpad import EtherpadLiteClient
import ast

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader('static/templates'),
    extensions=['jinja2.ext.autoescape'])

JINJA_ENVIRONMENT.filters['ndb_json'] = ndb_json.encode
 
        
class ViewPads(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if user:
            template = JINJA_ENVIRONMENT.get_template('view_pads.html')
            pads = Pad.query(Pad.owner==user.email())
            self.response.write(template.render(title = 'My Pads', pads=pads))
        else:
            self.redirect(users.create_login_url(self.request.uri))
            
class Update(webapp2.RequestHandler):
    def post(self):
        user = users.get_current_user()
        
        
        if user:
            pad_id = self.request.get('padId')
            try:
                pad = Pad.query(Pad.pad_id==pad_id).fetch()[0]
            except:
                self.redirect('/mypads')
            editors = self.request.get('editors')
            editors = ast.literal_eval(editors)
            title = self.request.get('padName')
            pad.editors = editors
            pad.title = title
            pad.put()
            self.redirect('/mypads')
            
        else:
            self.redirect(users.create_login_url('/mypads'))

