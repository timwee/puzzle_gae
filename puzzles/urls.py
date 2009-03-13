from django.conf.urls.defaults import *

from views import *

urlpatterns = patterns('puzzles.views',
  (r'^puzzles$', 'all_puzzles'),
  (r'^puzzle/create', 'create_puzzle'),
  (r'^puzzle/(?P<puzzle_id>\d+)/view$', 'view_puzzle'),
  (r'^puzzle/(?P<puzzle_id>\d+)/edit$', 'edit_puzzle'),
  (r'^puzzle/(?P<puzzle_id>\d+)/solution/create$', 'create_solution'),
  (r'^puzzle/(?P<puzzle_id>\d+)/solution/(?P<solution_id>\d+)/edit$', 'edit_solution'),
  (r'^puzzle/(?P<puzzle_id>\d+)/solution/(?P<solution_id>\d+)/view$', 'view_solution'),
  )
