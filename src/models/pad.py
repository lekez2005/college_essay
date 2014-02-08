'''
Created on Jan 9, 2014

@author: Ola
'''

from google.appengine.ext import ndb
import logging


class Pad(ndb.Model):
    owner = ndb.StringProperty(required=True)
    name = ndb.StringProperty()
    editors = ndb.StringProperty(repeated=True)
    pad_id = ndb.StringProperty(required=True)
    master = ndb.StringProperty(default='')
    

    
    
        
        
    