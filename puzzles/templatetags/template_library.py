import django.template
import django.utils.safestring

register = django.template.Library()

@register.inclusion_tag('puzzle_listings.html')
def show_puzzles(puzzles):
  return {'puzzles':puzzles}

