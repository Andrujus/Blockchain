def rotl32(x, r):
    return ((x << r) & 0xFFFFFFFF) | (x >> (32 - r))