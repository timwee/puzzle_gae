#!/usr/bin/env python
#
#

# Standard Python imports.
import os
import sys
import logging

# Log a message each time this module get loaded.
logging.info('Loading %s, app version = %s',
             __name__, os.getenv('CURRENT_VERSION_ID'))

# Delete the preloaded copy of Django.
for key in [key for key in sys.modules if key.startswith('django') or key.startswith('pygments')]:
  del sys.modules[key]

# Force sys.path to have our own directory first, so we can import from it.
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

# Import Django from a zipfile.
sys.path.insert(0, os.path.abspath('django.zip'))
sys.path.insert(0, os.path.abspath('pygments.zip'))

# Fail early if we can't import Django.  Log identifying information.
import django
logging.info('django.__file__ = %r, django.VERSION = %r',
             django.__file__, django.VERSION)
assert django.VERSION[0] >= 1, "This Django version is too old"

# AppEngine imports.
from google.appengine.ext.webapp import util


# Helper to enter the debugger.  This passes in __stdin__ and
# __stdout__, because stdin and stdout are connected to the request
# and response streams.  You must import this from __main__ to use it.
# (I tried to make it universally available via __builtin__, but that
# doesn't seem to work for some reason.)
def BREAKPOINT():
  import pdb
  p = pdb.Pdb(None, sys.__stdin__, sys.__stdout__)
  p.set_trace()


# Custom Django configuration.
#from django.conf import settings
#settings._target = None
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

# Import various parts of Django.
import django.core.handlers.wsgi
import django.core.signals
import django.db
import django.dispatch.dispatcher
import django.forms

# Work-around to avoid warning about django.newforms in djangoforms.
django.newforms = django.forms


def log_exception(*args, **kwds):
  """Django signal handler to log an exception."""
  cls, err = sys.exc_info()[:2]
  logging.exception('Exception in request: %s: %s', cls.__name__, err)


# Log all exceptions detected by Django.
django.core.signals.got_request_exception.connect(log_exception)

# Unregister Django's default rollback event handler.
django.core.signals.got_request_exception.disconnect(
    django.db._rollback_on_exception)


def real_main():
  """Main program."""
  # Create a Django application for WSGI.
  application = django.core.handlers.wsgi.WSGIHandler()
  # Run the WSGI CGI handler with that application.
  util.run_wsgi_app(application)


def profile_main():
  """Main program for profiling."""
  import cProfile
  import pstats
  import StringIO

  prof = cProfile.Profile()
  prof = prof.runctx('real_main()', globals(), locals())
  stream = StringIO.StringIO()
  stats = pstats.Stats(prof, stream=stream)
  # stats.strip_dirs()  # Don't; too many modules are named __init__.py.
  stats.sort_stats('time')  # 'time', 'cumulative' or 'calls'
  stats.print_stats()  # Optional arg: how many to print
  # The rest is optional.
  # stats.print_callees()
  # stats.print_callers()
  print '\n<hr>'
  print '<h1>Profile</h1>'
  print '<pre>'
  print stream.getvalue()[:1000000]
  print '</pre>'

# Set this to profile_main to enable profiling.
main = real_main


if __name__ == '__main__':
  main()

