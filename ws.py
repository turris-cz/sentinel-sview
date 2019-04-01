#!/usr/bin/env python3

import websockets
import asyncio
import json

from sview import create_app
from sview.extensions import rq

USERS = ()


def main():
    server = websockets.serve(ws_server, '127.0.0.1', 9000)
    asyncio.ensure_future(server)
    asyncio.get_event_loop().run_forever()


async def ws_server(websocket, path):
    register_user(websocket)

    try:
        app = create_app()
        with app.app_context():
            req = await websocket.recv()
            print(req)
    #job_id = request.form.get(post_name)
    #job = rq.get_queue().fetch_job(job_id)

    except websockets.exceptions.ConnectionClosed:
        pass

    finally:
        unregister_user(websocket)


def register_user(websocket):
    USERS.add(websocket)


def unregister_user(websocket):
    USERS.remove(websocket)


if __name__ == "__main__":
    main()
