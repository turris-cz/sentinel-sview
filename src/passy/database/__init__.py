from peewee import DatabaseProxy, PostgresqlDatabase, SqliteDatabase
from passy.utils import conform_arguments

# provides option to switch `db` object on the run
# works great with flask testing
# http://docs.peewee-orm.com/en/latest/peewee/database.html?highlight=DatabaseProxy#dynamically-defining-a-database
db = DatabaseProxy()


# def populate_database(file):
#     """Actually just for testing purpose
#     as the db is poulated by users in prod"""
#     with open(file, "r") as f:
#         commands = f.readlines()  # sqlite is only able run one command at the time

#     for command in commands:
#         db.execute_sql(command)  # each command is also commited


# def create_testing(file) -> None:
#     """Links proxy to database in memory"""
#     db.initialize(SqliteDatabase(":memory:"))
#     populate_database(file)


# def load_postgres(path: str, user: str, host: str) -> None:
#     """Links proxy to live database"""
#     db.initialize(PostgresqlDatabase(path, user, host))


def load_postgres(**settings):
    """Links proxy to local database, provide path, or not"""
    db.initialize(PostgresqlDatabase(**conform_arguments(**settings)))
