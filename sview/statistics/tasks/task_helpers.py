import base64
import binascii
import math
import re

IP_REGEX = re.compile(
    "^((25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9][0-9]|[0-9])\.){3}"
    "(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9][0-9]|[0-9])$"
)


def is_ip(string):
    return bool(IP_REGEX.match(string))


def human_readable_bytes(size):
    _suffixes = ["bytes", "KiB", "MiB", "GiB", "TiB", "PiB", "EiB", "ZiB", "YiB"]
    order = int(math.log2(size) / 10) if size else 0
    return "{:.4g} {}".format(size / (1 << (order * 10)), _suffixes[order])


def base64_encode(string):
    return base64.b64encode(bytes(string, "UTF-8")).decode()


def base64_decode(string):
    try:
        return str(base64.b64decode(string), "UTF-8")
    except (binascii.Error, UnicodeDecodeError):
        return None
