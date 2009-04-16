import django.template
import django.utils.safestring
from puzzles.models import *

register = django.template.Library()

@register.inclusion_tag('puzzle_listings.html')
def show_puzzles(puzzles):
  return {'puzzles':puzzles}

@register.inclusion_tag('solution_listings.html')
def show_solutions(puzzle):
  solutions = puzzle.solution_set
  puzzle_langs = set([Prog_Language.SYNTAX_MAP[solution.language] for solution in solutions])
  return {'solutions': solutions, 'puzzle_id':puzzle.key().id(), 'puzzle_langs':puzzle_langs }

