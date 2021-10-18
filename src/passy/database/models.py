from peewee import IntegerField, Model, TextField
import playhouse.postgres_ext as pg

from . import db


class BaseModel(Model):
    class Meta:
        database = db

class Password(BaseModel):
    count = pg.BigIntegerField(null=True)
    id = pg.BigAutoField()
    password_hash = pg.TextField()
    password_source = pg.ArrayField(pg.TextField) # ARRAY

    class Meta:
        table_name = 'passwords'
