from webapp2 import WSGIApplication, Route


application = WSGIApplication([
    Route(r'/', handler='index.Index', name='index'),
    Route(r'/add_file', handler='import_file.App'),
    ]
    , debug=True)
