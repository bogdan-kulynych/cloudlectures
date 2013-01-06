"""
Forms
~~~~~

Based upond WTForms

Docs: http://flask.pocoo.org/docs/patterns/wtforms/
      http://wtforms.simplecodes.com/

"""

from flask.ext.wtf import Form
from wtforms import validators, ValidationError
from wtforms.fields import TextField, TextAreaField

import models


# Validators

class ValidCourseName:
    def __init__(self, message=None):
        if not message:
            message = "There already exists a course with this name"
        self.message = message

    def __call__(self, form, field):
        if models.get_course_by_name(field.data) is not None:
            raise ValidationError(self.message)


# Forms

class CourseBasic(Form):
    name = TextField(
            'Name',
            validators=[
                validators.Required(), validators.Length(max=500, \
                    message="This shouldn't be longer than 500"
                ),
                ValidCourseName(
                    message="Oops, there already exists a course with this name"
                )
            ]
        )

    desc = TextAreaField(
            'Short description',
            validators=[
                validators.Required(),
                validators.length(max=500, \
                    message="This shouldn't be longer than 500"
                )
            ],
            description="Twitter-style short. No markup allowed"
        )

    tags = TextField(
            'Tags',
            validators=[
                validators.Regexp(r'(?:(?:[^,]+,\s*)*[^,])?', \
                    message=("Bad format. Give a list of tags, separated by"
                             "commas")
            )],
            description="Separate by commas"
        )

    univ = TextField(
            'University name'
        )
