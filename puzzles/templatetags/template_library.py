import django.template
from google.appengine.api import users
import django.utils.safestring
from puzzles.models import *

register = django.template.Library()

@register.inclusion_tag('puzzle_listings.html')
def show_puzzles(puzzles):
  return {'puzzles':puzzles}

@register.inclusion_tag('solution_listings.html')
def show_solutions(puzzle):
  solutions = puzzle.solution_set
  return {'solutions': solutions}

@register.inclusion_tag('vote_widget.html')
def vote_widget(solution):
  user = users.get_current_user()
  most_recent_vote = solution.get_votes_by(user, limit=1)
  voted_up = False
  voted_down = False
  if most_recent_vote and most_recent_vote[0]:

    most_recent_vote = most_recent_vote[0]
    #print(most_recent_vote.weight)
    if most_recent_vote.weight > 0:
      voted_up = True
    else:
      voted_down = True

  votes = solution.votes
  if votes < 0:
    votes = 0
  return {'solution':solution, 'voted_up':voted_up, 'voted_down':voted_down, 'votes':votes}

