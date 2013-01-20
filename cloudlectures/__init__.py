"""
Initialization and Configuration
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""

from flask import Flask
from werkzeug import DebuggedApplication

import secrets


# Initializing application
app = Flask('cloudlectures')

# Configuration
app.config.update(
    DEBUG            = False,
    CSRF_ENABLED     = True,
    SECRET_KEY       = secrets.CSRF,
    CSRF_SESSION_KEY = secrets.SESSION
)


# Debugger
app.wsgi_app = DebuggedApplication(app.wsgi_app, True)


# Everything else
import main
