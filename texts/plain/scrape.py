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
import requests
import lxml.html


def lxmlize(url):
    page = lxml.html.fromstring(requests.get(url).text)
    page.make_links_absolute(url)
    return page


def do_scrape(id_):
    text ,= lxmlize("http://opensource.org/licenses/{}".format(id_)).xpath(
        "//div[@class='content clearfix']"
    )
    return text.text_content()


def scrape():
    for id_ in [x['id'] for x in json.load(open(sys.argv[1]))]:
        if os.path.exists(id_):
            continue
        print(id_)
        text = do_scrape(id_)
        with open(id_, 'w') as fd:
            fd.write(text)

scrape()
