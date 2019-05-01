"""
Copyright 2017 Glen Harmon

All of this is taken from the python library passlib
https://passlib.readthedocs.io/en/stable/

Thank you for great software!
"""
import functools
from hashlib import md5
import time

from ..exceptions import InvalidPassword
from .common_passwords import _COMMON_PASSWORDS

_ASCII_COMMON_PASSWORDS = [pw.encode('ascii') for pw in _COMMON_PASSWORDS]


_HASH64_CHARS = u"./0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
_c_digest_offsets = (
    (0, 3), (5, 1), (5, 3), (1, 2), (5, 1), (5, 3), (1, 3),
    (4, 1), (5, 3), (1, 3), (5, 0), (5, 3), (1, 3), (5, 1),
    (4, 3), (1, 3), (5, 1), (5, 2), (1, 3), (5, 1), (5, 3),
)

_transpose_map = (12, 6, 0, 13, 7, 1, 14, 8, 2, 15, 9, 3, 5, 10, 4, 11)

_BNULL = b"\x00"
_MD5_MAGIC = b"$1$"
_APR_MAGIC = b"$apr1$"

class _Base64Engine(object):
    def __init__(self, charmap, big=False):
        # validate charmap, generate encode64/decode64 helper functions.
        if isinstance(charmap, str):
            charmap = charmap.encode("latin-1")
        if len(charmap) != 64:
            raise ValueError("charmap must be 64 characters in length")
        if len(set(charmap)) != 64:
            raise ValueError("charmap must not contain duplicate characters")
        self.bytemap = charmap
        self._encode64 = charmap.__getitem__
        lookup = dict((value, idx) for idx, value in enumerate(charmap))
        self._decode64 = lookup.__getitem__

        self.big = big
        if big:
            self._encode_bytes = self._encode_bytes_big
            self._decode_bytes = self._decode_bytes_big
        else:
            self._encode_bytes = self._encode_bytes_little
            self._decode_bytes = self._decode_bytes_little

    def encode_bytes(self, source):
        """encode bytes to base64 string.

        :arg source: byte string to encode.
        :returns: byte string containing encoded data.
        """
        if not isinstance(source, bytes):
            raise TypeError("source must be bytes, not %s" % (type(source),))
        chunks, tail = divmod(len(source), 3)
        next_value = iter(source).__next__
        gen = self._encode_bytes(next_value, chunks, tail)
        out = bytes(map(self._encode64, gen))
        ##if tail:
        ##    padding = self.padding
        ##    if padding:
        ##        out += padding * (3-tail)
        return out

    def _encode_bytes_little(self, next_value, chunks, tail):
        """helper used by encode_bytes() to handle little-endian encoding"""
        #
        # output bit layout:
        #
        # first byte:   v1 543210
        #
        # second byte:  v1 ....76
        #              +v2 3210..
        #
        # third byte:   v2 ..7654
        #              +v3 10....
        #
        # fourth byte:  v3 765432
        #
        idx = 0
        while idx < chunks:
            v1 = next_value()
            v2 = next_value()
            v3 = next_value()
            yield v1 & 0x3f
            yield ((v2 & 0x0f)<<2)|(v1>>6)
            yield ((v3 & 0x03)<<4)|(v2>>4)
            yield v3>>2
            idx += 1
        if tail:
            v1 = next_value()
            if tail == 1:
                # note: 4 msb of last byte are padding
                yield v1 & 0x3f
                yield v1>>6
            else:
                assert tail == 2
                # note: 2 msb of last byte are padding
                v2 = next_value()
                yield v1 & 0x3f
                yield ((v2 & 0x0f)<<2)|(v1>>6)
                yield v2>>4


    def _decode_bytes_little(self, next_value, chunks, tail):
        """helper used by decode_bytes() to handle little-endian encoding"""
        #
        # input bit layout:
        #
        # first byte:   v1 ..543210
        #              +v2 10......
        #
        # second byte:  v2 ....5432
        #              +v3 3210....
        #
        # third byte:   v3 ......54
        #              +v4 543210..
        #
        idx = 0
        while idx < chunks:
            v1 = next_value()
            v2 = next_value()
            v3 = next_value()
            v4 = next_value()
            yield v1 | ((v2 & 0x3) << 6)
            yield (v2>>2) | ((v3 & 0xF) << 4)
            yield (v3>>4) | (v4<<2)
            idx += 1
        if tail:
            # tail is 2 or 3
            v1 = next_value()
            v2 = next_value()
            yield v1 | ((v2 & 0x3) << 6)
            # NOTE: if tail == 2, 4 msb of v2 are ignored (should be 0)
            if tail == 3:
                # NOTE: 2 msb of v3 are ignored (should be 0)
                v3 = next_value()
                yield (v2>>2) | ((v3 & 0xF) << 4)


    #===================================================================
    # transposed encoding/decoding
    #===================================================================
    def encode_transposed_bytes(self, source, offsets):
        """encode byte string, first transposing source using offset list"""
        if not isinstance(source, bytes):
            raise TypeError("source must be bytes, not %s" % (type(source),))
        tmp = bytes(source[off] for off in offsets)
        return self.encode_bytes(tmp)





class _LazyBase64Engine(_Base64Engine):
    """Base64Engine which delays initialization until it's accessed"""
    _lazy_opts = None

    def __init__(self, *args, **kwds):
        self._lazy_opts = (args, kwds)

    def _lazy_init(self):
        args, kwds = self._lazy_opts
        super(_LazyBase64Engine, self).__init__(*args, **kwds)
        del self._lazy_opts
        self.__class__ = _Base64Engine

    def __getattribute__(self, attr):
        if not attr.startswith("_"):
            self._lazy_init()
        return object.__getattribute__(self, attr)


def _repeat_string(source, size):
    """repeat or truncate <source> string, so it has length <size>"""
    cur = len(source)
    if size > cur:
        mult = (size+cur-1)//cur
        return (source*mult)[:size]
    else:
        return source[:size]


def _decode(pwd, salt, use_apr=False):
    assert isinstance(pwd, bytes), "pwd not unicode or bytes"
    pwd_len = len(pwd)

    salt = salt.encode("ascii")
    assert len(salt) < 9, "salt too large"

    if use_apr:
        magic = _APR_MAGIC
    else:
        magic = _MD5_MAGIC

    #===================================================================
    # digest B - used as subinput to digest A
    #===================================================================
    db = md5(pwd + salt + pwd).digest()

    #===================================================================
    # digest A - used to initialize first round of digest C
    #===================================================================
    # start out with pwd + magic + salt
    a_ctx = md5(pwd + magic + salt)
    a_ctx_update = a_ctx.update

    # add pwd_len bytes of b, repeating b as many times as needed.
    a_ctx_update(_repeat_string(db, pwd_len))

    i = pwd_len
    evenchar = pwd[:1]
    while i:
        a_ctx_update(_BNULL if i & 1 else evenchar)
        i >>= 1

    # finish A
    da = a_ctx.digest()

    pwd_pwd = pwd+pwd
    pwd_salt = pwd+salt
    perms = [pwd, pwd_pwd, pwd_salt, pwd_salt+pwd, salt+pwd, salt+pwd_pwd]

    # build up list of even-round & odd-round constants,
    # and store in 21-element list as (even,odd) pairs.
    data = [ (perms[even], perms[odd]) for even, odd in _c_digest_offsets]

    # perform 23 blocks of 42 rounds each (for a total of 966 rounds)
    dc = da
    blocks = 23
    while blocks:
        for even, odd in data:
            dc = md5(odd + md5(dc + even).digest()).digest()
        blocks -= 1

    # perform 17 more pairs of rounds (34 more rounds, for a total of 1000)
    for even, odd in data[:17]:
        dc = md5(odd + md5(dc + even).digest()).digest()

    #===================================================================
    # encode digest using appropriate transpose map
    #===================================================================
    return _LazyBase64Engine(_HASH64_CHARS).encode_transposed_bytes(dc, _transpose_map).decode("ascii")


def chunks(full_list, number_of_chunks):
    for chunk in range(0, len(full_list), number_of_chunks):
        yield full_list[chunk: chunk + number_of_chunks]


def _brute_force_password(salt, password_hash, known_passwords):

    for bad_password in known_passwords:
        bad_password_hash = _decode(bad_password, salt)
        if bad_password_hash == password_hash:
            return bad_password
    return None    


@functools.lru_cache(maxsize=128)
def decode(type_5_password):
    try:
        _1, _2, salt, password_hash = type_5_password.split('$')
    except ValueError:
        raise InvalidPassword('Invalid Type 5 Password: {}'.format(type_5_password))

    start = time.time()
    password = _brute_force_password(salt, password_hash, _ASCII_COMMON_PASSWORDS)
    elapsed = time.time() - start
    return password
