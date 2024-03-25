from Crypto.Cipher import DES
# import os
import struct
import time

# import monobit_test as test1
# import runs_test as test2
# import random_excursion_variant_test as test3

def ANSI_X9_17(seed, key):
    des = DES.new(key, DES.MODE_ECB)

    while True:
        dt = struct.pack('d', time.time())

        xor_result = int.from_bytes(des.encrypt(
            dt), 'big') ^ int.from_bytes(seed, 'big')
        seed = des.encrypt(xor_result.to_bytes(8, 'big'))
        yield struct.unpack('Q', seed)[0]

# seed = os.urandom(8)
# key = os.urandom(8)

seed = '10101010101010101010'

generator = ANSI_X9_17(seed, key)

for _ in range(10):
    seq = next(generator)
    print(seq)
    print(test1.test(bin(seq)[2:]))
    print(test2.test(bin(seq)[2:]))
    print(test3.test(bin(seq)[2:]))