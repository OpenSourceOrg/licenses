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
import os.path
import sys
import json
import validictory

if sys.version_info < (3,):
    print("This program is Python 3 only")
    sys.exit(0)


def load_file(path):
    """
    Load a JSON file and yield out all top level elements from the JSON
    list in the file.
    """
    with open(path) as fd:
        yield from json.load(fd)


def merge_into(root, new):
    lists = ["identifiers", "links", "other_names", "tags"]
    id_ = new.pop('id')
    for key, value in new.items():
        if key in lists:
            if key not in root:
                root[key] = value
                continue
            root[key] += new[key]
            continue
        if key in root:
            raise ValueError("Fatal error: Key \"{}\" present on multiple "
                             "documents ({})".format(key, id_))
        root[key] = value
    return root


def merge_stream(stream):
    merged = {}
    for el in stream:
        id_ = el['id']
        root = merged.get(id_, {"id": id_})
        if 'name' in root and 'name' in el:
            raise ValueError("`name` given on two objects")
        merged[id_] = merge_into(root, el)
    return merged.values()


def validate(stream):
    with open("schema/license.validictory", 'r') as fd:
        schema = json.load(fd)

    def valid_schema(obj):
        validictory.validate(obj, schema)

    seen = set()
    for el in stream:
        valid_schema(el)

        if el['id'] in seen:
            raise ValueError("Duplicate ID in stream")
        seen.add(el['id'])
        if 'name' not in el:
            raise ValueError("Object {id} missing a name attribute".format(**el))
        yield el


def stream_licenses(path="."):
    """
    Given a path, walk all the JSON in the directory, and yield back all the
    license data blobs from each.
    """
    for dirpath, _, filenames in os.walk(path):
        for filename in filenames:
            if not filename.endswith(".json"):
                continue
            yield from load_file(os.path.join(dirpath, filename))


def load_licenses(path=".", output="licenses.json"):
    if os.path.exists(output):
        if os.stat(output).st_mtime < os.stat(__file__).st_mtime:
            os.unlink(output)
        else:
            print("Output file already exists, doing nothing")
            sys.exit(0)

    licenses = stream_licenses(path=path)
    data = list(validate(merge_stream(licenses)))

    with open(output, 'w') as fd:
        json.dump(data, fd)
    json.dump(data, sys.stdout, sort_keys=True, indent=4)


if __name__ == "__main__":
    load_licenses(*sys.argv[1:])
