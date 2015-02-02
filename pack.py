#!/usr/bin/env python3

import json
from hashlib import sha1
from datetime import datetime


def quit():
    from sys import argv
    print("""\
usage: {} FILE

where
    FILE: is the filename of your options to pack in JSON form
""".format(argv[0] if len(argv) > 0 else "python pack.py"))
    raise SystemExit(1)


def get_machine_name(pack_filename):
    return '{}.packed.{}'.format(*pack_filename.rsplit('.', 1)) 


def get_packs(pack_filename):
    with open(pack_filename) as options_file:
        new_options = json.load(options_file)
    try:
        with open(get_machine_name(pack_filename)) as pack_file:
            machine_packed = json.load(pack_file)
    except FileNotFoundError:
        machine_packed = {'packs': {}}
    return new_options, machine_packed


def next_machine_pack(old, options):
    new_packs = old['packs'].copy()
    hashed = sha1(",".join(options).encode()).hexdigest()[:7]
    if hashed not in new_packs:
        new_packs[hashed] = {
            'packed': datetime.now().timestamp(),
            'options': options
        }
    return {
        'current': hashed,
        'packs': new_packs
    }


def write_machine_pack(pack_filename, new_packed):
    with open(pack_filename, 'w') as packed:
        json.dump(new_packed, packed, indent=2)


if __name__ == '__main__':
    from sys import argv
    if not 1 < len(argv) < 3:
        quit()
    options_fname = argv[1]

    try:
        new_options, machine_packed = get_packs(options_fname)
    except FileNotFoundError:
        print('file not found: "{}"'.format(options_fname))
        quit()

    new_packed = next_machine_pack(machine_packed, new_options)

    try:
        write_machine_pack(get_machine_name(options_fname), new_packed)
    except IOError as e:
        print('IOError, Could not write new pack :(\n{}'.format(e))
        quit()

    print('success')
