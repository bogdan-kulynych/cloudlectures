"""
Models for Datastore and JSON data
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

"""

from google.appengine.ext import ndb
from flask import flash
from validictory import validate, ValidationError


# Utils

def get_course_by_name(name):
    course = Course.query(Course.name == name).get()
    return course


def get_course_by_link(link):
    course = Course.query(Course.link == link).get()
    return course


def get_courses_by_university(univ):
    courses = Course.query(Course.univ == univ).fetch()
    return courses


def get_published_courses():
    courses = Course.query(Course.published == True).fetch()
    return courses


def get_drafts():
    courses = Course.query(Course.published == False).fetch()
    return courses


def get_universities():
    courses = Course.all()
    return courses


# Models


class Course(ndb.Model):
    """
    Metadata and course contents
    """
    name = ndb.StringProperty(required=True)
    desc = ndb.TextProperty(required=True)
    univ = ndb.TextProperty(required=True)

    link = ndb.StringProperty()
    content = ndb.JsonProperty()

    published = ndb.BooleanProperty(default=False)

    data = ndb.DateTimeProperty(auto_now_add=True)
    edit = ndb.DateTimeProperty(auto_now=True)


# Content JSON schema
content_schema = {
    "type": "object",
    "$schema": "http://json-schema.org/draft-03/schema",
    "id": "#",
    "required": False,
    "properties": {
        "units": {
            "type": "array",
            "id": "units",
            "required": False,
            "maxItems": 255,
            "items":
                {
                    "type": "object",
                    "id": "0",
                    "required": False,
                    "properties": {
                        "description": {
                            "type": "string",
                            "id": "description",
                            "required": False,
                            "blank": True,
                            "maxLength": 500,
                        },
                        "lectures": {
                            "type": "array",
                            "id": "lectures",
                            "required": False,
                            "maxItems": 255,
                            "items":
                                {
                                    "type": "object",
                                    "id": "0",
                                    "required": False,
                                    "properties": {
                                        "description": {
                                            "type": "string",
                                            "id": "description",
                                            "required": False,
                                            "blank": True,
                                            "maxLength": 500,
                                        },
                                        "link": {
                                            "type": "string",
                                            "id": "link",
                                            "required": False,
                                            "blank": True,
                                            "maxLength": 500,
                                        },
                                        "title": {
                                            "type": "string",
                                            "id": "title",
                                            "required": True,
                                            "maxLength": 500,
                                        }
                                    }
                                }
                        },
                        "title": {
                            "type": "string",
                            "id": "title",
                            "required": True,
                            "maxLength": 500,
                        }
                    }
                }
        }
    }
}


def validate_content(content):
    """
    content - JSON object
    """
    try:
        validate(content, content_schema)
        return True
    except ValidationError, error:
        flash(error, 'error')
        return False
