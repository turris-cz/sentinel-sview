#!/usr/bin/env python3
from logging import getLogger, DEBUG
from geoip2.errors import AddressNotFoundError

import os
import tempfile
import argparse
import urllib.request
import geoip2.database
import json
import asyncio

import zmq
import zmq.auth
import zmq.asyncio
import websockets

import sn

TMP_CERT_LOCATION = os.path.join(tempfile.gettempdir(), "vizapp_certificates")
DOWNLOADED_SERVER_KEY_PATH = os.path.join(
    tempfile.gettempdir(), "vizapp_certificates", "server.pub"
)

_LOGGER = getLogger("dynfw")

USERS = set()


def get_arg_parser():
    def readable_file(path):
        if not os.path.exists(path):
            raise argparse.ArgumentTypeError("GeoIP database file not found")
        return path

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--server",
        "-s",
        metavar="URL",
        required=False,
        default="sentinel.turris.cz",
        help="URL of Sentinel DynFW publisher",
    )
    parser.add_argument(
        "--listen-addr",
        "-l",
        required=False,
        default="127.0.0.1",
        help="vizapp listen address",
    )
    parser.add_argument(
        "--port",
        "-p",
        required=False,
        default=7087,
        type=int,
        help="Port to connect to",
    )
    cert_def = parser.add_mutually_exclusive_group()
    cert_def.add_argument(
        "--cert-file",
        "-c",
        metavar="PATH",
        required=False,
        help="Path to server's certificate",
    )
    cert_def.add_argument(
        "--download-cert",
        "-d",
        metavar="URL",
        required=False,
        default="https://repo.turris.cz/sentinel/dynfw.pub",
        help="URL of published certificate",
    )
    parser.add_argument(
        "--geoip-db",
        "-g",
        metavar="PATH",
        required=True,
        type=readable_file,
        help="Path to geoip database",
    )
    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="provide debug INFO to logger destination",
        default=False,
    )

    return parser


def main():
    args = get_arg_parser().parse_args()

    if args.verbose:
        _LOGGER.setLevel(DEBUG)

    prepare_tmp_dir()

    if args.cert_file:
        server_key_file = args.cert_file
    else:
        download_certificate(args.download_cert)
        server_key_file = DOWNLOADED_SERVER_KEY_PATH

    ctx = zmq.asyncio.Context()
    sub = prepare_socket(ctx, args.server, args.port, server_key_file)

    reader = geoip2.database.Reader(args.geoip_db)

    server = websockets.serve(vizapp_server, args.listen_addr, 9000)

    asyncio.ensure_future(server)
    asyncio.ensure_future(dynfw_reader(reader, sub))

    asyncio.get_event_loop().run_forever()


def prepare_tmp_dir():
    if not os.path.exists(TMP_CERT_LOCATION):
        os.mkdir(TMP_CERT_LOCATION, mode=0o700)
        _LOGGER.info(f"created temporary file {TMP_CERT_LOCATION}")


def download_certificate(url):
    response = urllib.request.urlopen(url)
    with open(DOWNLOADED_SERVER_KEY_PATH, "wb") as f:
        f.write(response.read())
        _LOGGER.info(f"downloaded server key {DOWNLOADED_SERVER_KEY_PATH}")


def prepare_socket(ctx, addr, port, keyfile):
    sub = ctx.socket(zmq.SUB)
    sub.ipv6 = True

    client_public, client_secret = prepare_certificates()
    server_public = load_server_key(keyfile)

    sub.curve_secretkey = client_secret
    sub.curve_publickey = client_public
    sub.curve_serverkey = server_public
    sub.connect("tcp://{}:{}".format(addr, port))

    # I want to subscribe to all messages
    sub.setsockopt(zmq.SUBSCRIBE, b"dynfw/")

    return sub


def prepare_certificates():
    key_path = os.path.join(TMP_CERT_LOCATION, "client.key_secret")
    if not os.path.exists(key_path):
        public, secret = zmq.auth.create_certificates(TMP_CERT_LOCATION, "client")
        assert public
        assert secret

    client_public, client_secret = zmq.auth.load_certificate(key_path)

    return client_public, client_secret


def load_server_key(keyfile):
    public, _ = zmq.auth.load_certificate(keyfile)

    return public


def enrich_message(reader, payload):
    try:
        res = reader.country(payload["ip"])
        if res and res.country:
            payload["geo"] = res.country.iso_code
    except AddressNotFoundError:
        _LOGGER.info(f"Encountered `ip` that does not translate '{payload['ip']}'")


# ######################
# Websockets server code
# ######################
async def vizapp_server(websocket, path):
    register_user(websocket)
    try:
        await welcome_user(websocket)

        while True:
            await websocket.recv()

    except websockets.exceptions.ConnectionClosed:
        pass

    finally:
        unregister_user(websocket)


async def dynfw_reader(reader, socket):
    while True:
        _LOGGER.debug("awaiting mesage from dynfw..")
        msg = await socket.recv_multipart()
        _LOGGER.debug("message received!")

        mtype, payload = sn.parse_msg(msg)

        _LOGGER.debug(f'mtype="{mtype}", contents=""{payload}')

        if mtype == "dynfw/delta":
            await notify_users("dynfw delta", payload)
            _LOGGER.debug(f"users notified: `{mtype}` with payload: {payload}")

        elif mtype == "dynfw/list":
            await notify_users("dynfw list", payload)
            _LOGGER.debug(f"users notified with greylist ip addresses")

        elif mtype == "dynfw/event":
            enrich_message(reader, payload)
            await notify_users("dynfw event", payload)
            _LOGGER.debug(f"users notified: `{mtype}` with payload: {payload}")


def register_user(websocket):
    USERS.add(websocket)
    _LOGGER.info(f"added user {websocket.id}")


def unregister_user(websocket):
    USERS.remove(websocket)
    _LOGGER.info(f"removed user {websocket.id}")


async def welcome_user(websocket):
    await notify_user(websocket, "info", {"msg": "Connected"})


async def notify_users(msg_type, payload):
    if USERS:
        message = {
            "msgtype": msg_type,
            "payload": payload,
        }
        await asyncio.wait([asyncio.create_task(user.send(json.dumps(message))) for user in USERS if user])


async def notify_user(user, msg_type, payload):
    message = {
        "msgtype": msg_type,
        "payload": payload,
    }
    if user:
        await user.send(json.dumps(message))
        _LOGGER.info(
            f"user notified with message `{msg_type}` having payload: {payload}"
        )


if __name__ == "__main__":
    main()
