'''
Created on Jan 9, 2014

@author: Ola
'''
import webapp2
from webapp2_extras.routes import RedirectRoute as Route

application = webapp2.WSGIApplication([
    # admin page
    Route(r'/admin', handler = 'views.admin.admin.Admin',  name='admin_page',
          strict_slash = True),
    # questions
    Route(r'/admin/add/question', handler = 'views.admin.add_question.Add',
          name = 'add_question'),
    Route(r'/admin/edit/question/images/<questionKey>', handler = 'views.admin.add_question_image.Add',
          name = 'add_question_image'),
    Route(r'/admin/edit/question/<questionKey>', handler = 'views.admin.add_question.Edit', 
          name = 'edit_question_by_id'),
    Route(r'/admin/add/question/images/<questionKey>/upload', handler = 'views.admin.add_question_image.Upload',
          name = 'upload_question_image'),   
    # exams
    Route(r'/admin/add/exam', handler = 'views.admin.add_exam.Add', name = 'add_exam', 
          strict_slash = True),
    Route(r'/admin/edit/exam/<examId>', handler = 'views.admin.add_exam.Edit', name = 'edit_exam'),
    Route(r'/admin/edit/exam/<examId>/instructions/post', handler = 'views.admin.add_exam.AddInstruction',
          name = 'add_exam_instruction', strict_slash = True),
    Route(r'/admin/edit/exam/<examId>/instructions', handler = 'views.admin.add_exam.EditInstructions',
          name = 'edit_exam_instructions', strict_slash = True),
    Route(r'/admin/edit/exam/<examId>/instructions/update', handler = 'views.admin.add_exam.UpdateInstruction',
          name = 'update_exam_instruction', strict_slash = True),
    Route(r'/admin/edit/exam/<examId>/documents', handler='views.admin.add_exam.EditDocuments', 
          name = 'edit_exam_documents', strict_slash = True),
    Route(r'/admin/edit/exam/<examId>/documents/upload', handler='views.admin.add_exam.UploadDocuments', 
          name = 'upload_exam_documents', strict_slash = True)                                       
                                       
    ], debug=True)