from webapp2 import WSGIApplication, Route


application = WSGIApplication([
    Route(r'/', handler='index.Index', name='index'),
    ]
    , debug=True)
