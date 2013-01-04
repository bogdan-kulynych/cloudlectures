from google.appengine.api import users
from google.appengine.runtime.apiproxy_errors import CapabilityDisabledError

from flask import render_template, flash, url_for, redirect

from . import app
from decorators import login_required, admin_required

@app.route('/')
def main():
    return 'Fukin works'

# Administration page
@app.route('/admin')
@admin_required
def admin():
    return 'Super-seekrit admin page.'

# Custom 404 page
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

# Custom 500 page
@app.errorhandler(500)
def server_error(e):
    return render_template('500.html'), 500

# App Engine warm up handler
# See http://code.google.com/appengine/docs/python/config/appconfig.html#Warming_Requests
@app.route('/_ah/warmup')
def warmup():
    """App Engine warmup handler
    See http://code.google.com/appengine/docs/python/config/appconfig.html#Warming_Requests

    """
    return ''