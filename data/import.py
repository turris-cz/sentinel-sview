import argparse
import csv
import getpass
import hashlib

import psycopg2
import psycopg2.sql


def main():
    args = parse_args()
    password = getpass.getpass() if args.password else None

    reader = csv.DictReader(args.csv_file)
    connection = psycopg2.connect(
        host=args.host,
        port=args.port,
        dbname=args.dbname,
        user=args.username,
        password=password,
    )
    cursor = connection.cursor()

    import_data(reader, cursor)

    connection.commit()
    cursor.close()
    connection.close()


def import_data(reader, cursor):
    for row in reader:
        password_hash = hash_password(row["password"])
        count = row["count"]
        password_source = row["sources"].split(",")
        import_row(cursor, password_hash, count, password_source)


def hash_password(password):
    hash_object = hashlib.sha1(password.encode())
    return hash_object.hexdigest()


def import_row(cursor, password_hash, count, password_source):
    cursor.execute(
        """
            INSERT INTO passwords(password_hash, count, password_source)
            VALUES (%s, %s, %s::data_source[])
        """,
        (password_hash, count, password_source),
    )


def parse_args():
    parser = argparse.ArgumentParser(
        description="Hash and import common passwords data into the database",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    parser.add_argument(
        "-H",
        "--host",
        required=False,
        default=None,
        help="database server host or socket directory",
    )
    parser.add_argument(
        "-p", "--port", required=False, default=5432, help="database server port"
    )
    parser.add_argument(
        "-d",
        "--dbname",
        required=False,
        default=None,
        help="database name to connect to",
    )
    parser.add_argument(
        "-u", "--username", required=False, default=None, help="database user name"
    )
    parser.add_argument(
        "-W", "--password", action="store_true", help="force password prompt"
    )

    parser.add_argument(
        "csv_file",
        type=open,
        help="list of occurence count, passwords and data sources in CSV format",
    )

    return parser.parse_args()


if __name__ == "__main__":
    main()
