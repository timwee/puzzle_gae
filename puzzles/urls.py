from django.conf.urls.defaults import *

from views import *

urlpatterns = patterns('puzzles.views',
  (r'^$', 'all_puzzles'),
  (r'^puzzles$', 'all_puzzles'),
  (r'^puzzle/create', 'create_puzzle'),
  (r'^puzzle/(?P<puzzle_id>\d+)/view$', 'view_puzzle'),
  (r'^puzzle/(?P<puzzle_id>\d+)/edit$', 'edit_puzzle'),
  (r'^puzzle/(?P<puzzle_id>\d+)/solutions/date$', 'solutions_by_date'),
  (r'^puzzle/(?P<puzzle_id>\d+)/solutions/votes$', 'solutions_by_votes'),
  (r'^puzzle/(?P<puzzle_id>\d+)/solutions/language/(?P<language>\w+)/', 'solutions_by_lang'),
  (r'^puzzle/(?P<puzzle_id>\d+)/solution/create$', 'create_solution'),
  (r'^puzzle/(?P<puzzle_id>\d+)/solution/(?P<solution_id>\d+)/edit$', 'edit_solution'),
  (r'^puzzle/(?P<puzzle_id>\d+)/solution/(?P<solution_id>\d+)/view$', 'view_solution'),
  (r'^solution/(?P<solution_id>\d+)/voteup$', 'voteup_solution'),
  (r'^solution/(?P<solution_id>\d+)/votedown$', 'votedown_solution'),
  )
