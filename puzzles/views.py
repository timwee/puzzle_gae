from google.appengine.api import users
from google.appengine.ext import db
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.db import djangoforms

from django import forms
from django.http import Http404
from django.http import HttpResponse, HttpResponseRedirect
from django.http import HttpResponseForbidden, HttpResponseNotFound
from django.shortcuts import render_to_response
import django.template
from django.utils import simplejson
from django.utils.safestring import mark_safe
# Local imports
from puzzles.models import *
from puzzles.utils import *


### Form classes ###
class PuzzleForm(djangoforms.ModelForm):
  class Meta:
    model = Puzzle
    exclude = ['created', 'published']

### Views ###
def all_puzzles(request):
  q = Puzzle.all()
  q.order('-published')
  puzzles = q.fetch(limit=10)
  return render_to_response("all_puzzles.html", { 'puzzles' : puzzles })



# @login_required
def create_puzzle(request):
  if request.method != 'POST':
    form = PuzzleForm()
    return render_to_response("puzzle_form.html", {'form' : form })
  else:
    form = PuzzleForm(request.POST)
    errors = form.errors
    if not errors:
      try:
        puzzle = form.save()
        return HttpResponseRedirect('/puzzle/view/%i' % puzzle.key().id())
      except ValueError, err:
        errors['__all__'] = unicode(err)
    if errors:
      return render_to_response("puzzle_form.html", {'form' : form })


def edit_puzzle(request, puzzle_id):
  puzzle = get_object_or_404(Puzzle, puzzle_id)
  if request.method != 'POST':
    form = PuzzleForm(instance=puzzle)
    return render_to_response("puzzle_form.html", {'form' : form })
  else:
    form = PuzzleForm(request.POST)
    errors = form.errors
    if not errors:
      try:
        puzzle = form.save()
        return HttpResponseRedirect('/puzzle/view/%i' % puzzle.key().id())
      except ValueError, err:
        errors['__all__'] = unicode(err)
    if errors:
      return render_to_response("puzzle_form.html", {'form' : form })



def view_puzzle(request, puzzle_id):
  puzzle = get_object_or_404(Puzzle, puzzle_id)
  return render_to_response("puzzle_detail.html", {'puzzle' : puzzle })

def get_object_or_404(model_kls, id):
  result = model_kls.get_by_id(int(id))
  if not result:
    raise Http404
  return result






