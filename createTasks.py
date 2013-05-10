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

import json
from optparse import OptionParser
import pbclient
from get_images import get_flickr_photos


def contents(filename):
    return file(filename).read()

def handle_arguments():
    # Arguments for the application
    usage = "usage: %prog [options]"
    parser = OptionParser(usage)
    # URL where PyBossa listens
    parser.add_option("-s", "--server", dest="api_url",
                      help="PyBossa URL http://domain.com/", metavar="URL",
                      default="http://localhost:5000/")
    # API-KEY
    parser.add_option("-k", "--api-key", dest="api_key",
                      help="PyBossa User API-KEY to interact with PyBossa",
                      metavar="API-KEY")
    # Create App
    parser.add_option("-c", "--create-app", action="store_true",
                      dest="create_app",
                      help="Create the application",
                      metavar="CREATE-APP")
    # Update template for tasks and long_description for app
    parser.add_option("-t", "--update-template", action="store_true",
                      dest="update_template",
                      help="Update Tasks template",
                      metavar="UPDATE-TEMPLATE")

    # Update tasks question
    parser.add_option("-q", "--update-tasks",
                      type="int",
                      dest="update_tasks",
                      help="Update Tasks n_answers",
                      metavar="UPDATE-TASKS")

    parser.add_option("-x", "--extra-task", action="store_true",
                      dest="add_more_tasks",
                      help="Add more tasks",
                      metavar="ADD-MORE-TASKS")

    # Modify the number of TaskRuns per Task
    # (default 30)
    parser.add_option("-n", "--number-answers",
                      type="int",
                      dest="n_answers",
                      help="Number of answers per task",
                      metavar="N-ANSWERS",
                      default=30)

    parser.add_option("-a", "--application-config",
                      dest="app_config",
                      help="Application config file",
                      metavar="APP-CONFIG",
                      default="app.json")

    parser.add_option("-v", "--verbose", action="store_true", dest="verbose")
    (options, args) = parser.parse_args()

    if not options.create_app and not options.update_template\
            and not options.add_more_tasks and not options.update_tasks:
        parser.error("Please check --help or -h for the available options")

    if not options.api_key:
        parser.error("You must supply an API-KEY to create an \
                      application and tasks in PyBossa")

    return options

def get_configuration():
    options = handle_arguments()

    # Load app details
    try:
        with file(options.app_config) as app_json:
            app_config = json.load(app_json)
    except IOError as e:
        print "application config file is missing! Please create a new one"
        exit(1)

    return (app_config, options)

def run(app_config, options):
    def find_app_by_short_name():
        return pbclient.find_app(short_name=app_config['short_name'])[0]

    def setup_app():
        app = find_app_by_short_name()
        app.long_description = contents('long_description.html')
        app.info['task_presenter'] = contents('template.html')
        app.info['thumbnail'] = app_config['thumbnail']
        app.info['tutorial'] = contents('tutorial.html')

        pbclient.update_app(app)
        return app

    def create_photo_task(app, photo, question):
        # Data for the tasks
        task_info = dict(question=question,
                         n_answers=options.n_answers,
                         link=photo['link'],
                         url_m=photo['url_m'],
                         url_b=photo['url_b'])
        pbclient.create_task(app.id, task_info)

    def add_photo_tasks(app):
        # First of all we get the URL photos
        # Then, we have to create a set of tasks for the application
        # For this, we get first the photo URLs from Flickr
        photos = get_flickr_photos()
        question = app_config['question']
        [create_photo_task(app, p, question) for p in photos]

    pbclient.set('api_key', options.api_key)
    pbclient.set('endpoint', options.api_url)

    if options.verbose:
        print('Running against PyBosssa instance at: %s' % options.api_url)
        print('Using API-KEY: %s' % options.api_key)

    if options.create_app or options.add_more_tasks:
        if options.create_app:
            pbclient.create_app(app_config['name'],
                                app_config['short_name'],
                                app_config['description'])

            app = setup_app()
        else:
            app = find_app_by_short_name()
        add_photo_tasks(app)

    if options.update_template:
        print "Updating app template"
        # discard return value
        setup_app()

    if options.update_tasks:
        def tasks(app): 
            offset = 0
            limit = 100
            while True:
                tasks = pbclient.get_tasks(app.id, offset=offset, limit=limit)
                if len(tasks) == 0:
                    break
                for task in tasks:
                    yield task
                offset += len(tasks)

        def update_task(task, count):
            print "Updating task: %s" % task.id
            if 'n_answers' in task.info:
                del(task.info['n_answers'])
            task.n_answers = options.update_tasks
            pbclient.update_task(task)
            count[0] += 1

        print "Updating task n_answers"
        app = find_app_by_short_name()

        n_tasks = [0]
        [update_task(t, n_tasks) for t in tasks(app)]
        print "%s Tasks have been updated!" % n_tasks[0]

if __name__ == "__main__":
    app_config, options = get_configuration()
    run(app_config, options)
