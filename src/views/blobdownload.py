'''
Created on Jan 18, 2014

@author: Ola
'''

from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers
import webapp2

class Download(blobstore_handlers.BlobstoreDownloadHandler):
    def get(self, blobKey):
        if not blobstore.get(blobKey):
            self.error(404)
        else:
            self.send_blob(blobKey)


application = webapp2.WSGIApplication([
            webapp2.Route(r'/files/<blobKey>', handler = Download, 
                          name = 'download_blob'),
            ], debug=True)