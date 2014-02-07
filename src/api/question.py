'''
Created on Jan 8, 2014

@author: Ola
'''

import endpoints
from protorpc import remote

from models.question import Objective, Essay
from google.appengine.api import users

@endpoints.api(name='objective', version='v1', description='objective api')
class ObjectiveApi(remote.Service):
    
    @Objective.method(path='objective', http_method='POST', name='objective.insert')
    def ObjectiveInsert(self, objective):
        user = users.get_current_user()
        ADMINS = ['test@example.com']
        if user.email() in ADMINS:
            objective.put()
            return objective
        else:
            raise endpoints.UnauthorizedException('You are not an admin')
        
    
    @Objective.query_method(query_fields=('exam','order')
                             ,path='objectives', name='objective.list_by_exam')
    def ObjectiveList(self, query):
        return query
    
    @Objective.method(request_fields=('id',),
                      path='objectives/{id}', http_method='GET', name='objective.get')
    def ObjectiveGet(self, entity):
        if not entity.from_datastore:
            raise endpoints.NotFoundException('Question not found.')
        return entity
    
    
@endpoints.api(name='essay', version='v1', description='essay api')
class EssayApi(remote.Service):
    
    @Essay.method(path='essay', http_method='POST', name='essay.insert')
    def EssayInsert(self, essay):
        user = users.get_current_user()
        ADMINS = ['test@example.com']
        if user.email() in ADMINS:
            essay.put()
            return essay
        else:
            raise endpoints.UnauthorizedException('You are not an admin')
        
    
    @Essay.query_method(query_fields=('exam','order')
                             ,path='essays', name='essay.list_by_exam')
    def EssayList(self, query):
        return query
    
    @Essay.method(request_fields=('id',),
                      path='essay/{id}', http_method='GET', name='essay.get')
    def EssayGet(self, entity):
        if not entity.from_datastore:
            raise endpoints.NotFoundException('Question not found.')
        return entity
    
    
