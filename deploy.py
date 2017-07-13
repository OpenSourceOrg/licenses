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

import os
import sys

import boto
from boto.s3.key import Key
from boto.s3.connection import OrdinaryCallingFormat


def upload(s3_bucket, s3_path, filename):
    s3_url = 'http://%s/%s' % (s3_bucket, s3_path)
    s3conn = boto.connect_s3(os.environ.get("S3_ACCESS_KEY", ""),
                             os.environ.get("S3_SECRET_KEY", ""),
                             calling_format=OrdinaryCallingFormat())
    bucket = s3conn.create_bucket(s3_bucket)
    k = Key(bucket)
    k.key = s3_path

    k.set_contents_from_filename(filename)
    k.set_acl('public-read')


if __name__ == "__main__":
    print("Uploading to licenses/licenses.json...")
    upload("api.opensource.org", "licenses/licenses.json", *sys.argv[1:])
