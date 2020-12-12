⚠️ Not recommended ⚠️
---------------------

The design here is not super well thought-out. I don't know if a perfect alternative for the original goals exist, but something like [msgpack](https://msgpack.org/) is probably closer than this.

Incomplete list of someother better options in no particular order:

- [protocol buffers](https://en.wikipedia.org/wiki/Protocol_Buffers)
- [cap'n'proto](https://capnproto.org/)
- [thrift](https://thrift.apache.org/)? maybe?
- [asn.1](https://en.wikipedia.org/wiki/ASN.1), even


optionpack
==========

A simple protocol for serializing and deserializing a list of options.

optionpack strives to be:

  1. **Correct**: optionpack should never fail silently with the wrong results.

  2. **Simple**: as easy as possible to get it right for library users and implementers. Avoid third-party dependencies and use standard tools like base64 and JSON.

  3. **Safe**: bugs in implementations should not lead to XSS vulnerabilities

  4. **Backwards-compatible**: when the list of options changes, old packed options should still work.

  5. **Efficient**: the option choices should be packed as binary so that in most realistic use-cases, it can fit in a URL suitable for sharing.


optionpack does not strive to be:

 1. **Complete**: It's just for option lists. You might be interested in [tamper](http://nytimes.github.io/tamper/) or [protocol buffers](https://developers.google.com/protocol-buffers/) if you need more.

 2. **Optimal**: The bar is naiive JSON including the option keys. It's a low bar.


Usage
-----

### Maintaining the options

  1. Create an options array in JSON format

    example: [options.json](./options.json). It's an array of keys, like `["option1", "option2" ,...]`

  2. Generate or update an options pack from the options array

    example: `$ `[`./pack.py`](./pack.py)` options.json`. This will create (or update) [`options.packed.json`](./options.packed.json). It knows: the current options list, and all previous options lists.


### Packing

  1. Generate a JSON object representing the options state, like `{"option1": true, "option2": false,...}`

  2. Call `pack`. The python reference works on the command line like this:

    ```bash
    $ ./options.py pack '{"approved": true, "rejected": false, "proposed": true, "dropped": false}'
    ```
    which should yield `{"1e959d5": "oA=="}`. That's your pack!

### Unpacking

  1. Call `unpack` with the pack and get JSON back. With the python reference:

    ```bash
    $ ./options.py unpack '{"1e959d5": "oA=="}'
    ```
    which yields
    ```json
    {"rejected": false, "proposed": true, "approved": true, "dropped": false}
    ```

    woo hoo!


Example Use-case
----------------

A dashboard with shareable links that serialize the state of a filter with 500+ checkbox-type options.


Failure Modes
-------------

**Unpack with a reference to an options list that does not exist**

The library should raise an exception or otherwise indicate failure

**Unpack old options that have been removed in the current options list**

The removed options are silently dropped. The list of options returned must always be valid for the current options list.

**Unpack old options after new options have been added to the current options list**

The library must always include the full current set of options. Options missing from old packs must be false-y. It is acceptable for a library to use `null` in this case.

**Renaming option keys**

optionpack does not support this directly. Anyway, don't even do this :). If you must, do it in your application code around `unpack`.


Reference Implementation
------------------------

This repo contains a reference implementation written in python.

