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

def pad(data: bytes) -> bytes:
    bit_len = (len(data) * 8) & 0xFFFFFFFF  # kiek bitų turėjo pradinis tekstas
    padded = data + b'\x80'                 # pridedam 0x80
    while len(padded) % 4 != 0:             # pildom nuliais, kol ilgis % 4 == 0
        padded += b'\x00'
    padded += struct.pack('<I', bit_len)    # gale pridedam 4 baitus su ilgiu
    return padded
