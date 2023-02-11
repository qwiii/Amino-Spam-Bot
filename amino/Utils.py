from hmac import new
from hashlib import sha1
from base64 import b64encode
from random import randbytes


class Utils:

    @staticmethod
    def generate_signature(string: str):
        return b64encode(bytes.fromhex("19") + new(bytes.fromhex("DFA5ED192DDA6E88A12FE12130DC6206B1251E44"),
                                                   string.encode("utf-8"),
                                                   sha1).digest()).decode("utf-8")

    @staticmethod
    def generate_deviceid():
        ident = bytes.fromhex("19") + randbytes(20)
        hmac = new(bytes.fromhex("E7309ECC0953C6FA60005B2765F99DBBC965C8E9"),
                   ident,
                   sha1)
        return "{0}{1}".format(ident.hex(), hmac.hexdigest())
