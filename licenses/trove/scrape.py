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




def stream():
    classifiers = requests.get("https://pypi.python.org/pypi?%3Aaction=list_classifiers").text
    for line in classifiers.splitlines():
        if not line.startswith("License :: OSI Approved :: "):
            continue
        yield {
            "id": "",
            "identifiers": [
                {"identifier": line,
                 "scheme": "Trove"}
            ]
        }


def scrape():
    json.dump(list(stream()), sys.stdout, sort_keys=True, indent=4)

scrape()
