#!/usr/bin/env python3
# Script to update the imported Trove license data.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
#
# Intended to be run in order to update trove.json with new Trove license
# identifiers, e.g. like this:
#
#     ./scrape.py > trove-new.json
#     ./update.py > trove-updated.json
#     diff -u trove.json trove-updated.json
#
#     # Now manually merge content from trove-updated.json into trove.json;
#     # _might_ even execute this (at some time in future):
#     #mv trove-updates.json trove.json

import json
from sys import stdout

def update():
    with open('trove.json', 'r') as fc, open('trove-new.json', 'r') as fn:
        trove_cur = json.load(fc)
        trove_new = json.load(fn)

    # keep it simple and just assume 1:1 mapping
    id_mapping = {}
    for lic in trove_cur:
        osi_id = lic['id']
        for id_ in lic['identifiers']:
            if id_['scheme'] == 'Trove':
                trove_id = id_['identifier']
                id_mapping[trove_id] = osi_id

    for lic in trove_new:
        for id_ in lic['identifiers']:
            if id_['scheme'] == 'Trove':
                trove_id = id_['identifier']
                if id_mapping.__contains__(trove_id):
                    lic['id'] = id_mapping[trove_id]

    json.dump(trove_new, stdout, indent=4, sort_keys=True)

update()
