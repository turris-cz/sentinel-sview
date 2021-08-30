#!/usr/bin/env python3

import argparse
import datetime
import numpy
import random

import influxdb_client
import configparser

PASSWORDS = [
    "heslo", "pass", "password", "123", "00000", "123456", "passw0rd", "tajneheslo",
    "this is very secret", "super long and very secret password", "jetojedno",
    "it's one", "Can I use these: #$@;'?", "I can't  think of any more"
    ]
USERNAMES = [
    "Michal", "Karel", "Vojta", "Robin", "Pepe", "Alex", "Martin", "Mirek", "Filip",
    "Marek", "user", "someuser", "myself", "admin", "ubnt", "root"
]
COUNTRIES = ["CZ", "DE", "SK", "US", "GB", "TW", "PL"]
DEVICE_TOKENS = ["a"*64, "b"*64, "c"*64, "d"*64, "e"*64, "f"*64, "g"*64]
MONTH = 30 * 24 * 60 * 60  # seconds


class InfluxStorage():
    def __init__(self, url, token, org):
        client = influxdb_client.InfluxDBClient(url=url, token=token)
        self.write_api = client.write_api(write_options=influxdb_client.client.write_api.SYNCHRONOUS)
        self.org = org

    @classmethod
    def from_dict(cls, dct):
        try:
            return cls(dct["url"], dct["token"], dct["org"])
        except KeyError as exc:
            raise Exception(f"InfluxDB {exc} not provided in configuration.") from exc

    def _store_password(self, ts, password, username):
            self._write_point(
                "password_count",
                password,
                1,
                ts,
                username=username  # tag
            )

    def _store_port(self, ts, port, proto):
            self._write_point(
                "port_count",
                port,
                1,
                ts,
                protocol=proto  # tag
            )

    def _store_general_incident(self, ts, source, action):
            self._write_point(
                "incident_count",
                source,
                1,
                ts,
                action=action  # tag
            )

    def _store_attacker_incident(self, ts, src_addr, country):
            self._write_point(
                "attacker_incident_count",
                src_addr,
                1,
                ts,
                country=country  # tag
            )

    def _store_user_incident(self, ts, device_token, country, source):
            self._write_point(
                "user_incident_count",
                device_token,
                1,
                ts,
                country=country,  # tag
                source=source  # tag
            )

    def _populate_ports(self, ts, port_count):
        for i in range(port_count):
            self._store_port(ts, random.randint(0, 100), random.choice(["TCP", "UDP"]))

    def populate(self, count):
        for i in range(count):
            print(f"Populating {i}/{count}")
            timedelta = datetime.timedelta(seconds=abs(numpy.random.normal()) * MONTH)
            ts = datetime.datetime.utcnow() - timedelta
            source = random.choice([
                "minipot_telnet", "minipot_smtp", "minipot_ftp", "fwlogs"
            ])
            action = random.choice(["login", "connect"])
            address = f"192.0.2.{random.randint(1, 254)}"
            country = random.choice(COUNTRIES)

            self._store_general_incident(ts, source, action)
            self._store_attacker_incident(ts, address, country)
            self._store_user_incident(ts, random.choice(DEVICE_TOKENS), country, source)
            if action == "login":
                self._store_password(ts, random.choice(PASSWORDS), random.choice(USERNAMES))
            if source == "fwlogs":
                self._populate_ports(ts, random.randint(10, 100))

    def _write_point(self, measurement, field, value, ts, **tags):
        """Write data point to InfluxDB with precision in seconds"""
        point = influxdb_client.Point(measurement).field(field, value)
        point = point.time(ts, influxdb_client.WritePrecision.NS)

        for tag_name, tag_value in tags.items():
            point = point.tag(tag_name, tag_value)

        for bucket in ["sentinel-base", "sentinel-minutely", "sentinel-hourly", "sentinel-daily"]:
            self.write_api.write(bucket, self.org, point)


def add_parser_args(parser):
    parser.add_argument(
        "-c",
        "--config",
        default="dumper.ini",
        help="Path to configuration file"
    )
    parser.add_argument(
        "-t",
        "--token",
        help="InfluxDB access token. Overwrites value defined in config file."
    )
    parser.add_argument(
        "-u",
        "--url",
        help="InfluxDB URL. Overwrites value defined in config file."
    )
    parser.add_argument(
        "-m",
        "--measurements",
        default=200,
        type=int,
        help="Number of measurements to create."
    )


def prepare_config():
    conf = configparser.ConfigParser()

    conf.add_section("influx")
    conf["influx"].update({
        "url": "http://127.0.0.1:8086",
        "org": "myorganization",
        "token": "some-secret-token",
    })

    return conf


def config(args):
    conf = prepare_config()
    conf.read(args.config)

    if args.token:
        conf["influx"]["token"] = args.token

    if args.url:
        conf["influx"]["url"] = args.url

    return conf


def main():
    parser = argparse.ArgumentParser(
        description="Populate InfluxDB with random Sentinel data"
    )
    add_parser_args(parser)
    args = parser.parse_args()
    conf = config(args)
    storage = InfluxStorage.from_dict(conf["influx"])
    storage.populate(args.measurements)


if __name__ == "__main__":
    main()
