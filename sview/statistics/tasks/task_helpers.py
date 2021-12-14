import math
import re

IP_REGEX = re.compile(
    "^((25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9][0-9]|[0-9])\.){3}"
    "(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9][0-9]|[0-9])$"
)
TOKEN_HASH_REGEX = re.compile("^[a-z0-9]*$")
TOKEN_HASH_LENGTH = 10


def is_token_hash(string):
    return len(string) == TOKEN_HASH_LENGTH and TOKEN_HASH_REGEX.match(string)


def is_ip(string):
    return bool(IP_REGEX.match(string))


def human_readable_bytes(size):
    _suffixes = ["bytes", "KiB", "MiB", "GiB", "TiB", "PiB", "EiB", "ZiB", "YiB"]
    order = int(math.log2(size) / 10) if size else 0
    return "{:.4g} {}".format(size / (1 << (order * 10)), _suffixes[order])
