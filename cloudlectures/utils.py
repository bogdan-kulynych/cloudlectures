"""
Utility things
~~~~~~~~~~~~~~
"""

from functools import wraps
from google.appengine.api import users, urlfetch
from flask import redirect, request, Markup

from . import app


def admin_required(func):
    """Requires App Engine admin credentials"""
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if users.get_current_user():
            if not users.is_current_user_admin():
                del app.jinja_env.globals['admin']
                return redirect(users.create_logout_url(request.url))
            else:
                app.jinja_env.globals['admin'] = \
                    users.get_current_user()
                app.jinja_env.globals['logout'] = \
                    users.create_logout_url(request.url)

            return func(*args, **kwargs)
        return redirect(users.create_login_url(request.url))
    return decorated_view


def oembed(link):
    url = 'http://youtube.com/oembed?url={0}&format=json'
    result = urlfetch.fetch(url.format(link))
    if result.status_code == 200:
        return Markup(result['html'])
