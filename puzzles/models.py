# AppEngine imports
from google.appengine.ext import db
from google.appengine.api import memcache

from django.db import models

class Puzzle(db.Model):
  """ represents a puzzle """
  title = db.StringProperty(required=True)
  #tags = db.ListProperty(db.Category)
  description = db.TextProperty()
  created = db.DateTimeProperty(auto_now_add=True)
  published = db.DateTimeProperty(auto_now=True)

  @models.permalink
  def get_absolute_url(self):
    return ('puzzles.views.view_puzzle', [str(self.key().id())])

