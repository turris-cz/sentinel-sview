from enum import unique
from peewee import Index, Model, AutoField, CharField, IntegerField, TimestampField
from . import db


class BaseModel(Model):
    """Base database model"""

    id = AutoField() # enable id for every child Model

    class Meta:
        database = db


class Password(BaseModel):
    """id is included from `BaseModel`"""

    password = CharField(null=False)
    count = IntegerField(null=False)

    class Meta:
        table_name = "passwords"


class PasswordWithHash(BaseModel):
    """Testing purposes"""

    password = CharField(null=False, unique=True)
    count = IntegerField(null=False)
    _hash = CharField(column_name="hash", null=False, index=True)

    class Meta:
        table_name = "passwords_with_hash"
