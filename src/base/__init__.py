from peewee import DatabaseProxy, PostgresqlDatabase, SqliteDatabase

db = DatabaseProxy()


def populate_database(file):
    """Actually just for testing purpose
    as the db is poulated by users in prod"""
    with open(file, "r") as f:
        commands = f.readlines()

    for command in commands:
        db.execute_sql(command)


def create_testing(file) -> None:
    """Links the DatabaseProxy object `db` to memory"""
    db.initialize(SqliteDatabase(":memory:"))
    populate_database(file)


def load_production(path: str, user: str, host: str) -> None:
    """Links proxy to live database"""
    db.initialize(PostgresqlDatabase(path, user, host))


def load_dev():
    """Links proxy to local database"""
    db.initialize(SqliteDatabase("base.db"))
