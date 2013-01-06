"""
Views
~~~~~

"""

from flask import render_template, flash, url_for, redirect, request

from . import app
from decorators import admin_required

import models
import forms


@app.route('/')
def main():


@app.route('/course/add', methods=['GET', 'POST'])
@admin_required
def create_course()
    form = forms.CourseBasic(request.form)

    if request.method == 'POST' and form.validate():
        course = models.Course(
            name=form.name.data,
            desc=form.desc.data,
            tags=[form.tags.data],
            univ=form.univ.data
        )
        course.put()

        flash('Course added')
        return redirect('/')

    return render_template('course_basic_edit.html', form=form, legend="New lecture")


# Custom 404 page
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


# Custom 500 page
@app.errorhandler(500)
def server_error(e):
    return render_template('500.html'), 500


# App Engine warm up handler
# http://code.google.com/appengine/docs/python/config/appconfig.html#Warming_Requests
@app.route('/_ah/warmup')
def warmup():
    return ''