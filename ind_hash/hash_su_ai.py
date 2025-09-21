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

def mix_once(st):
    for i in range(8):
        a = st[i]
        b = st[(i+1) % 8]
        # čia pagrindinis maišymas
        c = ((a ^ rotl32(b, (i+1) % 31)) * 0x85ebca6b) & 0xFFFFFFFF
        st[i] = ((st[i] + c) ^ rotl32(st[(i+3) % 8], (i*7) % 31)) & 0xFFFFFFFF
    # dar pamaišom sukeisdami vietomis
    st[0], st[2], st[4], st[6] = st[2], st[4], st[6], st[0]