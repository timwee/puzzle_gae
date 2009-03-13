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

class Prog_Language(db.Model):
  name = db.StringProperty(required=True)
  homepage = db.LinkProperty()

class Solution(db.Model):
  author = db.UserProperty(required=True, auto_current_user_add=True)
  puzzle = db.ReferenceProperty(Puzzle)
  posted = db.DateTimeProperty(auto_now=True)
  #language = db.ReferenceProperty(Prog_Language)
  title = db.StringProperty(required=True)
  detail = db.TextProperty(required=True)

  @models.permalink
  def get_absolute_url(self):
    return ('puzzles.views.view_solution', (), {
            'puzzle_id' : str(self.puzzle.key().id()),
            'solution_id' : str(self.key().id()), })


class Account(db.Model):
  user = db.UserProperty(auto_current_user_add=True, required=True)
  email = db.EmailProperty(required=True)  # key == <email>
  created = db.DateTimeProperty(auto_now_add=True)
  modified = db.DateTimeProperty(auto_now=True)
  nickname = db.StringProperty(required=True)

  # Current user's Account.  Updated by middleware.AddUserToRequestMiddleware.
  current_user_account = None

  @classmethod
  def get_account_for_user(cls, user):
    """Get the Account for a user, creating a default one if needed."""
    email = user.email()
    assert email
    key = '<%s>' % email
    # Since usually the account already exists, first try getting it
    # without the transaction implied by get_or_insert().
    account = cls.get_by_key_name(key)
    if account is not None:
      return account
    nickname = user.nickname()
    if '@' in nickname:
      nickname = nickname.split('@', 1)[0]
    assert nickname

    return cls.get_or_insert(key, user=user, email=email, nickname=nickname)


