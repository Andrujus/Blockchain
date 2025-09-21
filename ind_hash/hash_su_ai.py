import struct

def rotl32(x, r):
    return ((x << r) & 0xFFFFFFFF) | (x >> (32 - r))

print(hex(rotl32(0b1011, 1)))

def u32_le(b, i):
    # paimame 4 baitus nuo pozicijos i
    chunk = b[i:i+4]
    if len(chunk) < 4:
        # jei trūksta baitų – pridedam nuliais
        chunk = chunk + b'\x00' * (4 - len(chunk))
    # paverčiam į 32 bitų skaičių (little-endian)
    return struct.unpack('<I', chunk)[0]