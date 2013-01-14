"""
Forms
~~~~~

Based on WTForms

Docs: http://flask.pocoo.org/docs/patterns/wtforms/
      http://wtforms.simplecodes.com/

"""

from flask import g as state
from flask.ext.wtf import Form
from wtforms import validators, ValidationError
from wtforms.fields import TextField, TextAreaField, HiddenField

import models


# Validators

class ValidLink:
    def __init__(self, message=None):
        if not message:
            message = "These alias is already taken"
        self.message = message

    def __call__(self, form, field):
        link = field.data.lower()
        course = models.get_course_by_link(link)
        if course is not None and course.key.urlsafe() != \
            state.current_course_key:
            raise ValidationError(self.message)


# Forms

class CourseBasic(Form):
    name = TextField(
            'Name',
            validators=[
                validators.Required(),
                validators.Length(max=500, \
                    message="It's too long"
                ),
            ]
        )

    desc = TextAreaField(
            'Short description',
            validators=[
                validators.Required(),
                validators.Length(max=500, \
                    message="It's too long"
                )
            ],
            description="Twitter-style short. No markup allowed"
        )

    univ = TextField(
            'University name',
            validators=[
                validators.Required(),
                validators.Length(max=500, \
                    message="It's too long"
                )
            ]
        )

    link = TextField(
            'Custom URL',
            validators=[
                validators.Length(max=100, \
                    message="It's too long"
                ),
                validators.Regexp(r'[A-z0-9\-_]*',
                    message=("Only latin characters, numbers, dash and "
                             "underscore allowed")
                ),
                ValidLink(
                    message="Sorry, this alias is already taken"
                )
            ],
            description=("Course's url will look like <br />"
                         "<span class=\"monospaced\">"
                         "http://.../courses/&lt;your alias></span>")
        )

    # tags = TextField(
    #         'Tags',
    #         validators=[
    #             validators.Regexp(r'(?:(?:[^,]+,\s*)*[^,])?', \
    #                 message=("Bad format. Give a list of tags, separated by"
    #                          "commas")
    #         )],
    #         description="Separated by commas"
    #     )


class CourseContents(Form):
    json_data = HiddenField(None, validators=[validators.Optional()])


class CoursePublish(Form):
    pass
