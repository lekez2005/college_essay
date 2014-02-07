from webapp2 import WSGIApplication, Route


application = WSGIApplication([
    Route(r'/', handler='index.Index', name='index'),
    Route(r'/question', handler='index.Question', name='index'),
    Route(r'/<examtype:(wassce|jamb)>/<subject:[^/]+/?>/<exam:[^/]+/?>/<number:[0-9]{1,2}>', handler='display.question.Question', name='question'),
    Route(r'/<examtype:(wassce|jamb)>/<subject:[^/]+/?>/<exam:[^/]+/?>', handler='display.exam.Exam', name='exam'),
    Route(r'/<examtype:(wassce|jamb)>/<subject:[^/]+/?>', handler='display.subject.Subject', name='subject'),
    Route(r'/<examtype:(wassce|jamb)/?>', handler='display.exam_type.ExamType', name='exam_type')
    ]
    , debug=True)
