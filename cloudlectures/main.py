"""
Views
~~~~~

"""

import json

from flask import render_template, \
                  flash,           \
                  url_for,         \
                  redirect,        \
                  request,         \
                  abort,           \
                  g as state       \

from . import app
from utils import admin_required

import models
import forms


@app.route('/')
def home():
    courses = models.get_published_courses()
    return render_template('home.html', courses=courses)


@app.route('/course/add', methods=['GET', 'POST'])
@admin_required
def add_course():
    form = forms.CourseBasic(request.form)

    if form.validate_on_submit():
        course = models.Course()

        course.name = form.name.data
        course.desc = form.desc.data
        course.univ = form.univ.data
        course.link = form.link.data.lower()

        key = course.put()

        if not course.link:
            course.link = key.urlsafe()
            course.put()

        flash('Course added', 'success')
        return redirect(url_for('edit_course_content', alias=course.link))

    return render_template('course-add.html',
                            form=form)


@app.route('/courses/<alias>', methods=['GET', 'POST'])
def course_page(alias):
    course = models.get_course_by_link(alias)
    if course is None:
        abort(404)

    if not course.published:
        return redirect(url_for('edit_course_content', alias=alias))

    form = forms.CoursePublish(request.form)

    if form.validate_on_submit():
        course.published = False
        course.put()

        flash('Course is moved to drafts', 'warning')
        return redirect(url_for('course_preview', alias=alias))

    return render_template('course-page.html', form=form, course=course)


@app.route('/courses/<alias>/edit/basic', methods=['GET', 'POST'])
@admin_required
def edit_course_basic(alias):
    course = models.get_course_by_link(alias)
    if course is None:
        abort(404)

    state.current_course_key = course.key.urlsafe()

    form = forms.CourseBasic(request.form, obj=course)

    if form.validate_on_submit():
        course.name = form.name.data
        course.desc = form.desc.data
        course.univ = form.univ.data
        course.link = form.link.data

        if not course.link:
            course.link = course.key.urlsafe()

        course.put()

        flash('New course basic data saved', 'success')
        return redirect(url_for('edit_course_basic', alias=course.link))

    return render_template('course-edit-basic.html',
                            course=course,
                            form=form)


@app.route('/courses/<alias>/edit/content', methods=['GET', 'POST'])
@admin_required
def edit_course_content(alias):
    course = models.get_course_by_link(alias)
    if course is None:
        abort(404)

    form = forms.CourseContents(request.form)
    json_data = course.content

    if form.validate_on_submit():
        try:
            content = json.loads(form.json_data.data)
        except ValueError:
            abort(400)

        json_data = content

        if models.validate_content(content):
            course.content = content
            course.put()

            flash('Content successfully updated', 'success')
            return redirect(url_for('course_preview', alias=course.link))

        else:
            flash('There were problems with your input', 'error')
            return redirect(url_for('course_edit_content', alias=course.link))

    json_data = json.dumps(json_data)
    return render_template('course-edit-content.html',
                            course=course,
                            json_data=json_data,
                            form=form)


@app.route('/courses/<alias>/preview', methods=['GET', 'POST'])
@admin_required
def course_preview(alias):
    course = models.get_course_by_link(alias)
    if course is None:
        abort(404)

    if course.published:
        return redirect(url_for('course_page', alias=alias))

    form = forms.CoursePublish(request.form)

    if form.validate_on_submit():
        course.published = True
        course.put()

        flash('Course is published', 'success')
        return redirect(url_for('course_page', alias=alias))

    return render_template('course-page.html', form=form, course=course)


@app.route('/drafts')
def drafts():
    courses = models.get_drafts()
    return render_template('drafts.html', courses=courses)


@app.route('/admin')
@admin_required
def admin():
    return redirect('/')


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
