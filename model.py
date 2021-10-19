from peewee import *

database = PostgresqlDatabase('hapi', **{'host': '127.0.0.1', 'user': 'hapi_user', 'password': 'hapi-secret'})

class UnknownField(object):
    def __init__(self, *_, **__): pass

class BaseModel(Model):
    class Meta:
        database = database

class Passwords(BaseModel):
    count = BigIntegerField(null=True)
    id = BigAutoField()
    password_hash = TextField()
    password_source = UnknownField(null=True)  # ARRAY

    class Meta:
        table_name = 'passwords'

