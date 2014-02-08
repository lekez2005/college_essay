from webapp2 import WSGIApplication, Route


application = WSGIApplication([
    Route(r'/', handler='index.Index', name='index'),
    Route(r'/add_file', handler='import_file.App'),
    Route(r'/add/pad', handler='views.add_pad.Add'),
    Route(r'/add/upload', handler='views.add_pad.Upload'),
    Route(r'/mypads', handler='views.viewPads.ViewPads'),
    Route(r'/update_pad', handler='views.viewPads.Update')
    ]
    , debug=True)
