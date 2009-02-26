"""Top-level URL mappings for puzzles."""

# NOTE: Must import *, since Django looks for things here, e.g. handler500.
from django.conf.urls.defaults import *

urlpatterns = patterns(
    '',
    url(r'', include('puzzles.urls')),
    )

