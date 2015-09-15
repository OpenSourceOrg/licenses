#!/usr/bin/env python
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

import os
import sys
import json

from collections import defaultdict


def audit_tags(licenses):
    total = len(licenses)
    tags = defaultdict(lambda: 0)
    for license in licenses:
        for tag in license.get('tags', []):
            tags[tag] += 1

    return [{"tag": tag, "count": count, "percent": count/total*100,
             "fatal": False} for (tag, count) in tags.items()]


def audit_identifiers(licenses):
    total = len(licenses)
    schemes = defaultdict(lambda: 0)
    for license in licenses:
        for identifier in license.get('identifiers', []):
            schemes[identifier['scheme']] += 1

    return [{"scheme": scheme, "count": count, "percent": count/total*100,
             "fatal": False} for (scheme, count) in schemes.items()]


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
        [{"id": x['id'], "name": x['name'], "problems": list(check_name(x)),
          "fatal": True} for x in licenses]))


def audit_full_text(licenses):
    def missing(licenses):
        for license in licenses:
            if not os.path.exists("texts/plain/{id}".format(**license)):
                yield license

    return [{"id": license['id'],
             "fatal": True} for license in missing(licenses)]


def has_error(report):
    for class_, elements in report.items():
        for element in elements:
            if element['fatal']:
                return True
    return False


def audit(path='licenses.json', exit=True):
    with open(path, 'r') as fd:
        licenses = json.load(fd)
    report = {"identifiers": audit_identifiers(licenses),
              "tags": audit_tags(licenses),
              "names": audit_names(licenses),
              "full_text": audit_full_text(licenses)}
    if exit and has_error(report):
        json.dump(report, sys.stdout, indent=4, sort_keys=True)
        sys.exit(1)
    return report


if __name__ == "__main__":
    audit(*sys.argv[1:])
