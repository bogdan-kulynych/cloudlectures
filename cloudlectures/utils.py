"""
Utility things
~~~~~~~~~~~~~~
"""

from functools import wraps
# from google.appengine.api import users
# from flask import redirect, request

from . import app


def admin_required(func):
    """Requires App Engine admin credentials"""
    @wraps(func)
    def decorated_view(*args, **kwargs):
        app.jinja_env.globals['admin'] = "admin"
        return func(*args, **kwargs)
    return decorated_view
