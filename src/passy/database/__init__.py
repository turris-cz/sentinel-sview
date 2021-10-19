from peewee import DatabaseProxy, PostgresqlDatabase, SqliteDatabase
from passy.utils import conform_arguments

# provides option to switch `db` object on the run
# works great with flask testing
# http://docs.peewee-orm.com/en/latest/peewee/database.html?highlight=DatabaseProxy#dynamically-defining-a-database
db = DatabaseProxy()


def load_postgres(**settings):
    """Links proxy to local database, provide path, or not"""
    db.initialize(PostgresqlDatabase(**conform_arguments(settings)))
