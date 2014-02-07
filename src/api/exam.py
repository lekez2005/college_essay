'''
Created on Jan 10, 2014

@author: Ola
'''
import endpoints
from endpoints_proto_datastore.ndb import EndpointsAliasProperty

from protorpc import remote

from models.exam import Exam
from models.examiner import Examiner
from models.subject import Subject

@endpoints.api(name='exam', version='v1', description='exam api')
class ExamApi(remote.Service):
    
    @Exam.query_method(path='exams', name='exam.list_by_examiner_sub',
                            query_fields=('examiner', 'subject', 'order'),
                            collection_fields = ('name', 'id', 'entityKey',
                                                 'objective','no_choices'))
    def ExamList(self, query):
        return query
    
    # Get by key
    @Exam.method(request_fields=('entityKey',),
                      path='exams/{entityKey}', http_method='GET', name='exam.get')
    def ExamGet(self, entity):
        if not entity.from_datastore:
            raise endpoints.NotFoundException('Exam not found.')
        return entity
    
    # Get by Id
    @Exam.method(request_fields=('id',),
                      path='get/{id}', http_method='GET', name='exam.get_by_id')
    def ExamGetById(self, entity):
        if not entity.from_datastore:
            raise endpoints.NotFoundException('Exam not found.')
        return entity
    
    @Exam.method(path='exam', http_method='POST', name='exam.insert')
    def ObjectiveInsert(self, exam):
        exam.put()
        return exam