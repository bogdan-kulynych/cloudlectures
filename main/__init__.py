from flask import Flask
from flaskext.gae_mini_profiler import GAEMiniProfiler

import secrets


app = Flask('cloudlectures')


# Configuration
app.config.update(
    DEBUG            = False,
    CSRF_ENABLED     = True,
    SECRET_KEY       = secrets.CSRF,
    CSRF_SESSION_KEY = secrets.SESSION
)


# Extensions

# Enable profiler (enabled in non-production environ only)
GAEMiniProfiler(app)


# Everything else
import main