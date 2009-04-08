# AppEngine imports
from google.appengine.ext import db
from google.appengine.api import memcache

from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter

from django.db import models

class Prog_Language(object):
  SYNTAX = (
		('scala','Scala'),
		('java','Java'),
		('scheme','Scheme'),
		('fortran','Fortran'),
		('cpp','C++'),
		('c','C'),
		('python','Python'),
		('smalltalk','Smalltalk'),
		('ocaml','OCaml'),
		('actionscript','ActionScript'),
		('ruby','Ruby'),
		('io','io'),
		('haskell','Haskell'),
		('lua','Lua'),
		('erlang','Erlang'),
		('clojure','Clojure'),
		('tcl','tcl'),
		('perl','perl'),
		('c#','C#'),
		('objective-c','objective-c'),
		('javascript','javascript'),
		('cl','Common Lisp'),
		('php','PHP')
  )

from google.appengine.ext import db

class HookedModel(db.Model):
  """A subclass of model that provides hooks for extra checks."""

  def pre_write(self):
    """Called before a model is written to the store."""
    pass

  def post_read(self):
    """Called after a model is read from the store."""
    pass

  def _populate_internal_entity(self, *args, **kwds):
    """Introduces hooks into the entity storing process."""
    self.pre_write()
    return db.Model._populate_internal_entity(self, *args, **kwds)



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


class Solution(HookedModel):
  author = db.UserProperty(required=True, auto_current_user_add=True)
  puzzle = db.ReferenceProperty(Puzzle, required=True)
  posted = db.DateTimeProperty(auto_now=True)
  language = db.StringProperty(required=True)
  title = db.StringProperty(required=True)
  code = db.TextProperty(required=True)
  formatted_code = db.TextProperty()

  def format_code(self):
    if not self.formatted_code:
      self.formatted_code = self.create_formatted_code()
    return self.formatted_code

  def create_formatted_code(self):
    if not self.code or not self.language:
      return ''
    lexer = get_lexer_by_name(self.language, stripall=True)
    formatter = HtmlFormatter(linenos=True, cssclass="source")
    return highlight(self.code, lexer, formatter)

  def pre_write(self):
    self.formatted_code = self.create_formatted_code()

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


