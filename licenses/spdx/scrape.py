#!/usr/bin/env python3
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

import sys
import json
import requests

def stream(known):
    request = requests.get("https://spdx.org/licenses/licenses.json")
    spdx_json = request.json()
    licenses = sorted(spdx_json["licenses"], key=lambda x: x["licenseId"])
    for license in licenses:
        if license["isOsiApproved"] and not license["isDeprecatedLicenseId"]:
            if license["licenseId"] not in known:
                sys.stderr.write("Unknown license: {}\n".format(license["licenseId"]))
                sys.stderr.flush()
                continue

            yield {
                "id": license["licenseId"],
                "identifiers": [
                    {"scheme": "SPDX",
                     "identifier": license["licenseId"]},
                ]
            }


def scrape():
    known = [x['id'] for x in json.load(open(sys.argv[1]))]
    json.dump(list(stream(known)), sys.stdout, sort_keys=True, indent=4)

scrape()
