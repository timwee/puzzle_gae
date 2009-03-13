import django.template
import django.utils.safestring

register = django.template.Library()

@register.inclusion_tag('puzzle_listings.html')
def show_puzzles(puzzles):
  return {'puzzles':puzzles}

@register.inclusion_tag('solution_listings.html')
def show_solutions(puzzle):
  solutions = puzzle.solution_set
  return {'solutions': solutions, 'puzzle_id':puzzle.key().id() }

