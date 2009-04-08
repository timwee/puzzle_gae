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

### Helper Functions ###
def respond(request, template, params=None):
  if params is None:
    params = {}
  if request.user is not None:
    account = Account.current_user_account

  params['request'] = request
  params['user'] = request.user
  params['is_admin'] = request.user_is_admin
  full_path = request.get_full_path().encode('utf-8')
  if request.user is None:
    params['sign_in'] = users.create_login_url(full_path)
  else:
    params['sign_out'] = users.create_logout_url(full_path)
  try:
    return render_to_response(template, params)
  except AssertionError:
    logging.exception('AssertionError')
    return HttpResponse('AssertionError')


### Form classes ###
class PuzzleForm(djangoforms.ModelForm):
  class Meta:
    model = Puzzle
    exclude = ['created', 'published']

class SolutionForm(forms.Form):
  #author = forms.UserProperty(required=True)
  #language = db.ReferenceProperty(Prog_Language)
  language = forms.ChoiceField(choices=Prog_Language.SYNTAX)
  title = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'size': 60}))
  code = forms.CharField(widget=forms.Textarea(attrs={'cols': 60}))
  puzzle = forms.IntegerField(widget=forms.HiddenInput())

### Views ###
def all_puzzles(request):
  q = Puzzle.all()
  q.order('-published')
  puzzles = q.fetch(limit=10)
  return respond(request,"all_puzzles.html", { 'puzzles' : puzzles })



@login_required
def create_puzzle(request):
  if request.method != 'POST':
    form = PuzzleForm()
    return respond(request,"puzzle_form.html", {'puzzle_form' : form })
  else:
    form = PuzzleForm(request.POST)
    errors = form.errors
    if not errors:
      try:
        puzzle = form.save()
        return HttpResponseRedirect(puzzle.get_absolute_url())
      except ValueError, err:
        errors['__all__'] = unicode(err)
    if errors:
      return respond(request,"puzzle_form.html", {'puzzle_form' : form })

@login_required
def edit_puzzle(request, puzzle_id):
  puzzle = get_object_or_404(Puzzle, puzzle_id)
  if request.method != 'POST':
    form = PuzzleForm(instance=puzzle)
    return respond(request,"puzzle_form.html", {'puzzle_form' : form })
  else:
    form = PuzzleForm(request.POST)
    errors = form.errors
    if not errors:
      try:
        puzzle = form.save()
        return HttpResponseRedirect(puzzle.get_absolute_url())
      except ValueError, err:
        errors['__all__'] = unicode(err)
    if errors:
      return respond(request,"puzzle_form.html", {'puzzle_form' : form })

def view_puzzle(request, puzzle_id):
  puzzle = get_object_or_404(Puzzle, puzzle_id)
  return respond(request,"puzzle_detail.html", {'puzzle' : puzzle })

@login_required
def create_solution(request, puzzle_id):
  puzzle = get_object_or_404(Puzzle, puzzle_id)
  if request.method != 'POST':
    form = SolutionForm(initial={ 'puzzle' : puzzle_id })
    return respond(request, "solution_form.html", {'solution_form' : form, 'puzzle' : puzzle })
  else:
    form = SolutionForm(request.POST)
    if not form.is_valid():
      return respond(request, "solution_form.html", {'solution_form' : form, 'puzzle' : puzzle })

    sol = Solution(author=users.get_current_user(),
                   puzzle=puzzle,
                   title=form.cleaned_data['title'],
                   language=form.cleaned_data['language'],
                   code=form.cleaned_data['code'])
    sol.put()
    return HttpResponseRedirect(sol.get_absolute_url())

def view_solution(request, puzzle_id, solution_id):
  puzzle = get_object_or_404(Puzzle, puzzle_id)
  solution = get_object_or_404(Solution, solution_id)
  return respond(request,"solution_detail.html", {'puzzle' : puzzle, 'solution':solution })

@login_required
def edit_solution(request, puzzle_id, solution_id):
  puzzle = get_object_or_404(Puzzle, puzzle_id)
  solution = get_object_or_404(Solution, solution_id)

  if request.method != 'POST':
    form = SolutionForm(initial={ 'puzzle' : puzzle_id, 'title':solution.title, 'code':solution.code })
    return respond(request,"solution_form.html", {'solution_form' : form, 'puzzle' : puzzle })
  else:
    form = SolutionForm(request.POST)
    errors = form.errors
    if not errors:
      try:
        solution = form.save()
        return HttpResponseRedirect(solution.get_absolute_url())
      except ValueError, err:
        errors['__all__'] = unicode(err)
    if errors:
      return respond(request,"solution_form.html", {'solution_form' : form, 'puzzle' : puzzle })

def get_object_or_404(model_kls, id):
  result = model_kls.get_by_id(int(id))
  if not result:
    raise Http404
  return result






