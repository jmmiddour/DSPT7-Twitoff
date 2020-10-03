'''Entry point to Twitoff app.'''
from .app import create_app

# Initializes the core app.
APP = create_app()