#!/usr/bin/env python 
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
import json
import re
import string
import datetime
from optparse import OptionParser

def delete_app(api_url, api_key, id):
    """
    Deletes the Flickr Person Finder application.

    :arg integer id: The ID of the application
    :returns: True if the application has been deleted
    :rtype: boolean
    """
    request = urllib2.Request(api_url + '/api/app/' + str(id) + '?api_key=' + api_key)
    request.get_method = lambda: 'DELETE'

    if (urllib2.urlopen(request).getcode() == 204): 
        return True
    else:
        return False

def update_app(api_url , api_key, id, name = None):
    """
    Updates the name of the Flickr PErson Finder application
    
    :arg integer id: The ID of the application
    :arg string name: The new name for the application
    :returns: True if the application has been updated
    :rtype: boolean
    """
    data = dict(id = id, name = name)
    data = json.dumps(data)
    request = urllib2.Request(api_url + '/api/app/' + str(id) + '?api_key=' + api_key)
    request.add_data(data)
    request.add_header('Content-type', 'application/json')
    request.get_method = lambda: 'PUT'

    if (urllib2.urlopen(request).getcode() == 200): 
        return True
    else:
        return False

def create_app(api_url , api_key, name=None, short_name=None, description=None):
    """
    Creates the Flickr Person Finder application. 

    :arg string name: The application name.
    :arg string short_name: The slug application name.
    :arg string description: A short description of the application. 

    :returns: Application ID or 0 in case of error.
    :rtype: integer
    """
    print('Creating app')
    name = u'Flickr Person PHinder' # Name with a typo
    short_name = u'flickrperson'
    description = u'Do you see a human in this photo?'
    # JSON Blob to present the tasks for this app to the users
    # First we read the template:
    file = open('template.html')
    text = file.read()
    file.close()
    info = dict (thumbnail = "http://img37.imageshack.us/img37/156/flickrpersonthumbnail.png", task_presenter = text)
    data = dict(name = name, short_name = short_name, description = description,
               hidden = 0, info = info)
    data = json.dumps(data)

    # Checking which apps have been already registered in the DB
    apps = json.loads(urllib2.urlopen(api_url + '/api/app' + '?api_key=' + api_key).read())
    for app in apps:
        if app['short_name'] == short_name: 
            print('{app_name} app is already registered in the DB'.format(app_name = name))
            print('Deleting it!')
            if (delete_app(api_url, api_key, app['id'])): print "Application deleted!"
    print("The application is not registered in PyBOSSA. Creating it...")
    # Setting the POST action
    request = urllib2.Request(api_url + '/api/app?api_key=' + api_key )
    request.add_data(data)
    request.add_header('Content-type', 'application/json')

    # Create the app in PyBOSSA
    output = json.loads(urllib2.urlopen(request).read())
    if (output['id'] != None):
        print("Done!")
        print("Ooooops! the name of the application has a typo!")
        print("Updating it!")
        if (update_app(api_url, api_key, output['id'], "Flickr Person Finder")): 
            print "Application name fixed!"
            return output['id']
        else:
            print "An error has occurred"
    else:
        print("Error creating the application")
        return 0

def create_task(api_url , api_key, app_id, photo):
    """
    Creates tasks for the application

    :arg integer app_id: Application ID in PyBossa.
    :returns: Task ID in PyBossa.
    :rtype: integer
    """
    # Data for the tasks
    info = dict (link = photo['link'], url = photo['url'])
    data = dict (app_id = app_id, state = 0, info = info, calibration = 0, priority_0 = 0)
    data = json.dumps(data)

    # Setting the POST action
    request = urllib2.Request(api_url + '/api/task' + '?api_key=' + api_key)
    request.add_data(data)
    request.add_header('Content-type', 'application/json')

    # Create the task
    output = json.loads(urllib2.urlopen(request).read())
    if (output['id'] != None):
        return True
    else:
        return False

def get_flickr_photos(size="big"):
    """
    Gets public photos from Flickr feeds
    
    :arg string size: Size of the image that should be obtained from Flickr feed. 
    :returns: A list of photos.
    :rtype: list
    """
    # Get the ID of the photos and load it in the output var
    print('Contacting Flickr for photos')
    url = "http://api.flickr.com/services/feeds/photos_public.gne"
    values = {
        'nojsoncallback': 1,
        'format': "json",
        #'ids':'25053835@N03'
        }
    query = url + "?" + urllib.urlencode(values)
    urlobj = urllib2.urlopen(query)
    data = urlobj.read()
    urlobj.close()
    # The returned JSON object by Flickr is not correctly escaped, so we have to fix it
    # see http://stackoverflow.com/questions/9312196/how-to-convert-this-string-into-json-format-using-json-loads
    regex = re.compile(r'\\(?![/u"])')
    fixed = regex.sub(r"\\\\", data)
    output = json.loads(fixed)
    print('Data retrieved from Flickr')

    # For each photo ID create its direct URL according to its size: big, medium, small
    # (or thumbnail) + Flickr page hosting the photo
    photos = []
    for idx, photo in enumerate(output['items']):
        print 'Retrieved photo: %s' % idx
        imgUrl = string.replace(photo["media"]["m"],"_m.jpg","_b.jpg")
        photos.append({'link': photo["link"], 'url':  imgUrl})
    return photos


import sys
if __name__ == "__main__":
    # Arguments for the application
    usage = "usage: %prog [options]"
    parser = OptionParser(usage)
    
    parser.add_option("-u", "--url", dest="api_url", help="PyBossa URL http://domain.com/", metavar="URL")
    parser.add_option("-k", "--api-key", dest="api_key", help="PyBossa User API-KEY to interact with PyBossa", metavar="API-KEY")
    parser.add_option("-v", "--verbose", action="store_true", dest="verbose")
    
    (options, args) = parser.parse_args()

    if not options.api_url:
        options.api_url = 'http://localhost:5000/'

    if not options.api_key:
        parser.error("You must supply an API-KEY to create an applicationa and tasks in PyBossa")

    if (options.verbose):
       print('Running against PyBosssa instance at: %s' % options.api_url)
       print('Using API-KEY: %s' % options.api_key)

    app_id = create_app(options.api_url, options.api_key)
    # First of all we get the URL photos
    # WARNING: Sometimes the flickr feed returns a wrong escape character, so it may
    # fail at this step
    photos = get_flickr_photos()
    # Finally, we have to create a set of tasks for the application
    # For this, we get first the photo URLs from Flickr
    for photo in photos:
        create_task(options.api_url, options.api_key, app_id, photo)

