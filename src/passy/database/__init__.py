from peewee import DatabaseProxy, PostgresqlDatabase, SqliteDatabase

# provides option to switch `db` object on the run
# works great with flask testing
# http://docs.peewee-orm.com/en/latest/peewee/database.html?highlight=DatabaseProxy#dynamically-defining-a-database
db = DatabaseProxy()


def populate_database(file):
    """Actually just for testing purpose
    as the db is poulated by users in prod"""
    with open(file, "r") as f:
        commands = f.readlines()  # sqlite is only able run one command at the time

    for command in commands:
        db.execute_sql(command)  # each command is also commited


def create_testing(file) -> None:
    """Links proxy to database in memory"""
    db.initialize(SqliteDatabase(":memory:"))
    populate_database(file)


def load_production(path: str, user: str, host: str) -> None:
    """Links proxy to live database"""
    db.initialize(PostgresqlDatabase(path, user, host))


def load_dev(path=None, **settings):
    """Links proxy to local database, provide path, or not"""
    if not settings:
        db.initialize(SqliteDatabase(path or "/tmp/base.db"))
    else:
        db.initialize(
            PostgresqlDatabase(
                host=settings['DB_HOSTNAME'],
                database=settings['DB_NAME'],
                user=settings['DB_USERNAME'],
                password=settings['DB_PASSWORD']
            )
        )

