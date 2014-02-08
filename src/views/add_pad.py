'''
Created on Aug 9, 2013

@author: Ola
'''
import webapp2, jinja2, os
from google.appengine.ext import db
from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers
from google.appengine.api import users
import zipfile
from lxml import etree
import json, logging
import random, string
from docx import getdocumenttext
from models.pad import Pad
from py_etherpad import EtherpadLiteClient

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader('static/templates'),
    extensions=['jinja2.ext.autoescape'])

        
def opendocx(file):
    '''Open a docx file, return a document XML tree'''
    mydoc = zipfile.ZipFile(file)
    xmlcontent = mydoc.read('word/document.xml')
    document = etree.fromstring(xmlcontent)
    return document

def doc_to_text(document):
    # Fetch all the text out of the document we just created
    paratextlist = getdocumenttext(document)

    # Make explicit unicode version
    newparatextlist = []
    for paratext in paratextlist:
        newparatextlist.append(paratext.encode("utf-8"))

    # Print out text of document with two newlines under each paragraph
    return '\n\n'.join(newparatextlist)

def id_generator(size=8, chars=string.letters + string.digits):
    return ''.join(random.choice(chars) for x in range(size))
        
class Add(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if user:
            template = JINJA_ENVIRONMENT.get_template('add_pad.html')
            post_url = blobstore.create_upload_url('/add/upload')
            self.response.write(template.render(title = 'Add Pad', post_url=post_url))
        else:
            self.redirect(users.create_login_url(self.request.uri))
    
class Upload(blobstore_handlers.BlobstoreUploadHandler):
    def post(self):
        user = users.get_current_user()
        if user:
            try:
                uploaded_file = (self.get_uploads('file'))[0]
            except:
                uploaded_file = None
            origin = self.request.get('create_from')
            if origin == 'textarea':
                pad_text = self.request.get('pad_text').strip()
            else:
                if uploaded_file is None:
                    pad_text = ''
                else:
                    blob_reader = blobstore.BlobReader(uploaded_file)
                    document = opendocx(blob_reader)
                    pad_text = doc_to_text(document)
            pad_name = self.request.get('padName')
            
            myPad = EtherpadLiteClient()
            pad_id = id_generator()
            pad = myPad.createPad(padID = pad_id, text=pad_text)
            pad = Pad(owner = user.email(), name=pad_name, pad_id = pad_id, master='')
            pad.put()
        
        else:
            self.error(404)
        if uploaded_file:
            uploaded_file.delete()
            
        self.redirect('/mypads')
