Contributing
============

Hey, thanks for considering contributing to the OSI master license list!

If you're unsure about anything, just ask! Feel free to submit and issue
or pull request, even if you're not sure!

OSI License List
================

New datasets can be super useful - stuff like adding metadata to existing
licenses (like Wikipedia pages, or SPDX identifiers) comes in quite handy.

Compiling the master list
-------------------------

Run the `compile.py` script, which will import all the JSON, merge documents
on the `id` key (merging lists, and only allowing each non-list key to be set
once), and print the resulting data to stdout.

Please run the `compile.py` script before sending in any patches.
