from tinyec import registry
import secrets
import hashlib


_CURVE = registry.get_curve("brainpoolP256r1")


def _compress(key):
    return hex(key.x) + hex(key.y % 2)[2:]


def ecc_point_to_256_bit_key(point):
    sha = hashlib.sha256(int.to_bytes(point.x, 32, "big"))
    sha.update(int.to_bytes(point.y, 32, "big"))
    return sha.digest()


class ECC:
    def __init__(self) -> None:
        self.secret = secrets.randbelow(_CURVE.field.n)
        self.public = self.secret * _CURVE.g
        self.shared = None

    def generate_common(self, foreign):
        self.shared = self.secret * foreign

    def get_public(self):
        return _compress(self.public)
