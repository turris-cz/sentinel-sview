from peewee import Model, AutoField, CharField, IntegerField, TimestampField
from . import db


class BaseModel(Model):
    """Base database model"""

    id = AutoField()

    class Meta:
        database = db


class Password(BaseModel):
    """id is included from `BaseModel`"""

    password = CharField(null=False)
    count = IntegerField(null=False)

    class Meta:
        table_name = "passwords"


class AnonymousUser(BaseModel):
    last_used = TimestampField(null=False)  # in case of retention (you don't need to hold it forever)
    pub_key = CharField(null=False)

    class Meta:
        table_name = "anonymous_users"
