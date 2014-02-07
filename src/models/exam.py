'''
Created on Jan 9, 2014

@author: Ola
'''
from endpoints_proto_datastore.ndb import EndpointsModel, EndpointsDateProperty
from endpoints_proto_datastore.ndb import  EndpointsDateTimeProperty
from google.appengine.api.datastore_errors import BadValueError
from google.appengine.ext import ndb
from models.subject import Subject
from models.examiner import Examiner
import logging


class Document(EndpointsModel):
    comment = ndb.TextProperty()
    file = ndb.BlobKeyProperty(required=True)
    created = EndpointsDateTimeProperty(auto_now_add=True)
    complete = ndb.BooleanProperty(default=True)
    uploader = ndb.UserProperty(auto_current_user_add=True)
    
class RawText(EndpointsModel): # latex drafts etc
    content = ndb.TextProperty()
    created = EndpointsDateTimeProperty(auto_now_add=True)
    comment = ndb.TextProperty()
    uploader = ndb.UserProperty(auto_current_user_add=True)
    
class Issue(EndpointsModel):
    text = ndb.TextProperty(required=True)
    user = ndb.UserProperty(auto_current_user_add=True)
    
class Instruction(EndpointsModel):
    text = ndb.TextProperty(required=True)
    file = ndb.BlobKeyProperty()
    begin_num = ndb.IntegerProperty(required = True)
    end_num = ndb.IntegerProperty(required=True)
    
    @classmethod
    def _pre_delete_hook(cls, key):
        logging.info(key)

class Exam(EndpointsModel):
    
    def validate_no_choices(self, value):
        if value > 6 or value < 0:
            raise BadValueError
        
    
    name = ndb.StringProperty(required = True)
    date = EndpointsDateProperty(required=True)
    subject = ndb.KeyProperty(kind='Subject', required = True)
    examiner = ndb.KeyProperty(kind='Examiner', required = True)
    duration = ndb.IntegerProperty(required=True)
    objective = ndb.BooleanProperty(required=True)
    issues = ndb.StructuredProperty(Issue, repeated=True)
    scanned_pdf = ndb.StructuredProperty(Document)
    question_pdf = ndb.StructuredProperty(Document)
    solution_pdf = ndb.StructuredProperty(Document)
    tags = ndb.StringProperty(repeated=True)
    no_choices = ndb.IntegerProperty(default=0, validator=validate_no_choices)
    instructions = ndb.StructuredProperty(Instruction, repeated=True)
    _message_fields_schema = ('date', 'duration', 'entityKey', 'examiner', 'id', 'instructions', 
                              'issues', 'name', 'no_choices', 'objective', 'subject', 'tags')
    
    
    @property
    def compute_url(self):
        return str(self.id) + "_url"
        
    
    
        
        
    