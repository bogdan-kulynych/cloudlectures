"""
App Engine datastore models
~~~~~~~~~~~~~~~~~~~~~~~~~~~

"""


from google.appengine.ext import ndb


# Utils

def get_course_by_name(name):
    course = Course.query(Course.name == name)
    return course


def get_course_by_link(alias):
    course = Course.query(Course.link == link)
    return course


# Models

class Course(ndb.Model):
    """Example Model"""
    name = ndb.StringProperty(required=True)
    desc = ndb.TextProperty(required=True)
    univ = ndb.TextProperty(required=True)
    link = ndb.StringProperty(required=True)

    tags = ndb.StringProperty(repeated=True)
    content = ndb.JsonProperty()
