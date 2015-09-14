# Copyright (c) 2015, Paul R. Tagliamonte <paultag@opensource.org>
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
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import json
import sys

from collections import defaultdict


def audit_identifiers(licenses):
    total = len(licenses)
    schemes = defaultdict(lambda: 0)
    for license in licenses:
        for identifier in license.get('identifiers', []):
            schemes[identifier['scheme']] += 1

    return [{"scheme": scheme, "count": count, "percent": count/total}
            for (scheme, count) in schemes.items()]


def audit_names(licenses):
    def check_name(license):
        if 'version' in license['name']:
            yield "contains 'version', use 'Version'"

        if license['name'] == license['name'].upper():
            yield "all uppercase"

        # lname = license['name'].lower()
        # if lname.startswith("the"):
        #     yield "Name starts with 'The'"

    return list(filter(
        lambda x: x['problems'] != [],
        [{"id": x['id'], "name": x['name'], "problems": list(check_name(x))}
         for x in licenses]))


def audit(path):
    with open(path, 'r') as fd:
        licenses = json.load(fd)
    report = {"identifiers": audit_identifiers(licenses),
              "names": audit_names(licenses)}
    json.dump(report, sys.stdout, indent=4, sort_keys=True)


audit(*sys.argv[1:])
