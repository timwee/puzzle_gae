from django.conf.urls.defaults import *

from views import *

urlpatterns = patterns('puzzles.views',
  (r'^puzzles$', 'all_puzzles'),
  (r'^puzzle/create', 'create_puzzle'),
  (r'^puzzle/view/(?P<puzzle_id>\d+)$', 'view_puzzle'),
  (r'^puzzle/edit/(?P<puzzle_id>\d+)$', 'edit_puzzle'),
  )
