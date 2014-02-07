'''
Created on Jan 10, 2014

@author: Ola
'''

import endpoints

from protorpc import remote

from models.subject import Subject


@endpoints.api(name='subject', version='v1', description='subjects api')
class SubjectApi(remote.Service):
    
    @Subject.query_method(collection_fields=('name', 'id', 'entityKey' ),
                           path='subjects', name='subject.list')
    def SubjectList(self, query):
        return query
    
    