'''
Created on Jan 10, 2014

@author: Ola
'''
import endpoints

from protorpc import remote

from models.examiner import Examiner


@endpoints.api(name='examiner', version='v1', description='examiners api')
class ExaminerApi(remote.Service):
    
    @Examiner.query_method(collection_fields=('name', 'id', 'entityKey' ),
                            path='examiners', name='examiner.list')
    def ExaminerList(self, query):
        return query