'''
Created on Aug 9, 2013

@author: Ola
'''
import webapp2, jinja2, os
from google.appengine.ext import db
import lib.subprocess as subprocess 
import os  
import uuid  


JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__) + "/static/templates"),
    extensions=['jinja2.ext.autoescape'])

        
def document_to_html(file_path):  
    print subprocess.__file__
    tmp = "/tmp"  
    guid = str(uuid.uuid1())  
    # convert the file, using a temporary file w/ a random name  
    command = "abiword -t %(tmp)s/%(guid)s.html %(file_path)s; cat %(tmp)s/%(guid)s.html" % locals()      
    p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, cwd=os.path.join(settings.PROJECT_DIR, "website/templates"))  
    error = p.stderr.readlines()      
    if error:  
        raise Exception("".join(error))  
    html = p.stdout.readlines()  
    return "".join(html)  

class App(webapp2.RequestHandler):
    def get(self):
        file_path = os.path.dirname(__file__) + "/static/test_document.docx"
        output = document_to_html(file_path)
        template = JINJA_ENVIRONMENT.get_template('files.html')
        #output = "This is output"
        self.response.write(template.render(title = 'College Essays', output=output))
    