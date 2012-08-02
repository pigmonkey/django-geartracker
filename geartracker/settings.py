"""
These settings should not be edited directly.
Instead, overwrite them in the main project's setting file.
"""
from django.conf import settings

# How many items should appear on a single page.
GEARTRACKER_PAGINATE_BY = getattr(settings, 'GEARTRACKER_PAGINATE_BY', 12)
