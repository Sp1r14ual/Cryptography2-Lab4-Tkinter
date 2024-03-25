from Crypto.Cipher import DES
import os
import struct
import time

def ANSI_X9_17(p1, p2):
    seed = os.urandom(8)
    key = os.urandom(8)

    des = DES.new(key, DES.MODE_ECB)

    while True:
        dt = struct.pack('d', time.time())

        xor_result = int.from_bytes(des.encrypt(
            dt), 'big') ^ int.from_bytes(seed, 'big')
        seed = des.encrypt(xor_result.to_bytes(8, 'big'))
        yield struct.unpack('Q', seed)[0]