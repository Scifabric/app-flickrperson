# Image Pattern Recognition Demo project for PyBossa

The aim of this demo project is to show how you can solve an image pattern
recognition problem using [PyBossa](http://pybossa.com) technology.

This demo uses Flickr as the backend for storing the photos, but you can use
any other web server or service that gives you public access to the photos.

The project has five main files:

* **project.json**: a JSON file that describes the project.
* **long_description.md**: a Markdown file with a long description of the
  project.
* **get_images.py**: to query Flickr and write a file with the photo links.
* **template.html**: the task presenter where the user/volunteer will do the image
  pattern recognition.
* **tutorial.html**: a simple tutorial that explains how to do the image pattern
  recognition.

![alt screenshot](http://i.imgur.com/Isj4rJQ.png)

# Testing the project

You need to install the pybossa-pbs. If you don't have a virtual environment,
we recommend you to create one, and activate it:

```bash
    $ virtualenv env
    $ source env/bin/activate
```

Then, you can install pybossa-pbs:

```bash
    $ pip install pybossa-pbs
```

Or if you prefer:

```bash
    $ pip install -r requirements.txt
```

**NOTE**: Use this template with a PyBossa server version >=1.0.0.

## Creating an account in a PyBossa server
Now that you've all the requirements installed in your system, you need
a PyBossa account:

*  Create an account in your PyBossa server (use [Crowdcrafting](http://crowdcrafting.org) if you want).
*  Copy your API-KEY (you can find it in your profile page).

## Configure pybossa-pbs command line

PyBossa-pbs command line tool can be configured with a config file in order to
avoid typing the API-KEY and the server every time you want to take an action
on your project. For this reason, we recommend you to actually create the
config file. For creating the file, follow the next steps:

```bash
    $ cd ~
    $ editorofyourchoice .pybossa.cfg
```

That will create a file. Now paste the following:

```ini
[default]
server: http://yourpybossaserver.com
apikey: yourapikey
```

Save the file, and you are done! From now on, pybossa-pbs will always use the
default section to run your commands.

## Create the project

Now that we've everything in place, creating the project is as simple as
running this command:

```bash
    $ pbs create_project
```

## Adding some tasks

Now we can add some tasks. The project comes with two samples that you can use:

 * flickr_tasks.csv: a CSV file with some tasks
 * get_images.py: a script that will contact Flickr to create a JSON file with
   links to images

### Using a CSV file for adding tasks

This is very simple too, thanks to pbs:

```bash
    $ pbs add_tasks --tasks-file flickr_tasks.csv
```
You'll get a progress bar with the tasks being uploaded. Now your project has
some tasks in the server to be processed by the volunteers.

### Using a JSON file for adding tasks

Instead of giving you a JSON file, we wanted to show you how you can use a web
service like Flickr to query it and get the images that want to do image
pattern recognition. For this reason, we've created the script
**get_images.py**.

When you run this script, it will contact Flickr, get the last 20 published
photos in the web services, get its links, and write a file in JSON format
named: **flickr_tasks.json**. We'll use this file to add some extra tasks to
our project:

```bash
    $ python get_images.py
    $ pbs add_tasks --tasks-file flickr_tasks.json
```

Again, as before, you will see a progess bar as the tasks are being added to
your project. You can modify get_images.py to adapt it for your needs ;-)

## Finally, add the task presenter, tutorial and long description

Now that we've some data to process, let's add to our project the required
templates to show a better description of our project, to present the tasks to
our users, and a small tutorial for the volunteers:

```bash
    $ pbs update_project
```

Done! Now you can do image pattern recognition problems in the PyBossa server.

**NOTE**: we provide templates also for Bootstrap v2 in case your PyBossa
server is using Bootstrap2 instead of Bootstrap3. See the rest of the files.

Documentation
=============

We recommend that you read the section: [Build with PyBossa](http://docs.pybossa.com/en/latest/build_with_pybossa.html), follow the [step by step tutorial](http://docs.pybossa.com/en/latest/user/tutorial.html) and read the [PyBossa pbs documentation](https://github.com/PyBossa/pbs).

**NOTE**: This project uses the [pybossa-pbs](https://pypi.python.org/pypi/pybossa-pbs) library in order to simplify the development of the project and its usage. Check the [documentation](https://github.com/PyBossa/pbs).


LICENSE
=======

Copyright (C) 2015 [SciFabric LTD](http://scifabric.com)

Please, see the COPYING file.


Acknowledgments
===============
The thumbnail has been created using a [photo](http://www.flickr.com/photos/mcgraths/3289448299/) from Sean McGrath (license CC BY 2.0). 


**Note**: You can see the results of the Crowdcrafting app [here](http://dev.pybossa.com/app-flickrperson/results.html)
