from django.conf.urls.defaults import *

from views import *

urlpatterns = patterns('django.views.generic.simple',
    (r'^$', 'direct_to_template', {'template' : 'index.html'}),
  )

urlpatterns += patterns('puzzles.views',
  (r'^puzzles$', 'all_puzzles'),
  (r'^puzzle/create', 'create_puzzle'),
  (r'^puzzle/(?P<puzzle_id>\d+)/view$', 'view_puzzle'),
  (r'^puzzle/(?P<puzzle_id>\d+)/edit$', 'edit_puzzle'),
  (r'^puzzle/(?P<puzzle_id>\d+)/solutions/date$', 'solutions_by_date'),
  (r'^puzzle/(?P<puzzle_id>\d+)/solutions/language/(?P<language>\w+)/', 'solutions_by_lang'),
  (r'^puzzle/(?P<puzzle_id>\d+)/solution/create$', 'create_solution'),
  (r'^puzzle/(?P<puzzle_id>\d+)/solution/(?P<solution_id>\d+)/edit$', 'edit_solution'),
  (r'^puzzle/(?P<puzzle_id>\d+)/solution/(?P<solution_id>\d+)/view$', 'view_solution'),
  )
