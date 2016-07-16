licenses
========

This repo contains machine readable information regarding OSI's licenses.

The top level `compile.py` script will produce the merged and verified
list of licenses.

**Note:** the `compile.py` script is written in Python 3, and will result
in a Python 2.x syntax error being thrown, due to it not having the
`yield from` keyword yet. When you run `compile.py`, be sure you're using
Python 3, or you might see obscure errors.

The [latest version of the .json can be found here](https://api.opensource.org.s3.amazonaws.com/licenses/licenses.json)


Is this authoritative?
======================

Not yet. Hopefully soon.


Licensing
=========

Software is GPL-3.0+, data is CC0. See LICENSE for more information.
