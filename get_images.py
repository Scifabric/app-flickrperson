# -*- coding: utf-8 -*-

# This file is part of PyBOSSA.
#
# PyBOSSA is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# PyBOSSA is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with PyBOSSA.  If not, see <http://www.gnu.org/licenses/>.

import urllib
import urllib2
import re
import json
import string


def get_flickr_photos(size="big"):
    """
    Gets public photos from Flickr feeds
    :arg string size: Size of the image from Flickr feed.
    :returns: A list of photos.
    :rtype: list
    """
    # Get the ID of the photos and load it in the output var
    # add the 'ids': '25053835@N03' to the values dict if you want to
    # specify a Flickr Person ID
    print('Contacting Flickr for photos')
    url = "http://api.flickr.com/services/feeds/photos_public.gne"
    values = {'nojsoncallback': 1,
              'format': "json"}

    query = url + "?" + urllib.urlencode(values)
    urlobj = urllib2.urlopen(query)
    data = urlobj.read()
    urlobj.close()
    # The returned JSON object by Flickr is not correctly escaped,
    # so we have to fix it see
    # http://goo.gl/A9VNo
    regex = re.compile(r'\\(?![/u"])')
    fixed = regex.sub(r"\\\\", data)
    output = json.loads(fixed)
    print('Data retrieved from Flickr')

    # For each photo ID create its direct URL according to its size:
    # big, medium, small (or thumbnail) + Flickr page hosting the photo
    photos = []
    for idx, photo in enumerate(output['items']):
        print 'Retrieved photo: %s' % idx
        imgUrl_m = photo["media"]["m"]
        imgUrl_b = string.replace(photo["media"]["m"], "_m.jpg", "_b.jpg")
        photos.append({'link': photo["link"], 'url_m':  imgUrl_m,
                       'url_b': imgUrl_b})
    return photos

if __name__ == '__main__':
    file = open('flickr_tasks.json', 'w')
    photos = get_flickr_photos()
    file.write(json.dumps(photos))
    file.close()
