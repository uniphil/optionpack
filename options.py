#!/usr/bin/env python3

import json
import base64


def quit():
    from sys import argv
    print("""\
usage: {} (pack|unpack) OBJ

where
    OBJ is a JSON string to be packed or unpacked

The result will be printed to stdout.
""".format(argv[0] if len(argv) > 0 else "python options.py"))
    raise SystemExit(1)


def bits_to_bytes(bits):
    bytes = bytearray()
    byte_so_far = 0
    bits_so_far = 0
    for bit in bits:
        byte_so_far += int(bit)  # 1 or 0
        bits_so_far += 1
        if bits_so_far == 8:
            bytes.append(byte_so_far)
            byte_so_far = 0
            bits_so_far = 0
        else:
            byte_so_far <<= 1
    if bits_so_far > 0:
        last_byte = byte_so_far << (7 - bits_so_far)  # right-pad with zeros
        bytes.append(last_byte)
    return bytes


def bytes_to_bits(bytes):
    bits = []
    for byte in bytes:
        bits.extend(bool(int(b)) for b in '{:08b}'.format(byte))
    return bits


def pack(obj, packs):
    options = packs['packs'][packs['current']]['options']
    bits = (bool(obj.get(opt)) for opt in options)
    encoded = base64.urlsafe_b64encode(bits_to_bytes(bits))
    return json.dumps({ packs['current']: encoded.decode() })  # .decode bytes->str


def unpack(obj, packs):
    opt_version, encoded = list(obj.items())[0]
    options_then = packs['packs'][opt_version]['options']
    options_now = packs['packs'][packs['current']]['options']
    bits = bytes_to_bits(base64.urlsafe_b64decode(encoded.encode()))
    result_then = {opt: bit for opt, bit in zip(options_then, bits)}
    return json.dumps({opt: result_then.get(opt) or False for opt in options_now})


if __name__ == '__main__':
    from sys import argv
    if not 2 < len(argv) < 4:
        quit()

    mode, payload = argv[1:3]
    if mode not in ('pack', 'unpack'):
        print('Valid modes are "pack" and "unpack"')
        quit()

    packs = json.load(open('options.packed.json'))
    try:
        obj = json.loads(payload)
    except ValueError:
        print('Could not decode JSON')
        quit()

    if mode == 'pack':
        print(pack(obj, packs))
    else:
        print(unpack(obj, packs))


