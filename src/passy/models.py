from peewee import SqliteDatabase, Model

database = SqliteDatabase('base.db')

class BaseModel(Model):
    class Meta:
        database = database

