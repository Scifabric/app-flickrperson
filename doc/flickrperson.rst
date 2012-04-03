===================================
Application Tutorial: Flickr Person
===================================

This tutorial is based in the demo application **Flickr Person** provided with
PyBossa. This demo application is a simple microtasking app where users have to
answer the following question: Do you see a human in this photo? The possible
answers are: Yes, No and I don't know.

The demo application Flickr Person has two main components:

  * **Task Creator**: Python script to generate the tasks in PyBossa, and the
  * **Task Presenter**: HTML + Javascript to show the tasks to the users.

Both items use the PyBossa API.

Setting Things Up
=================

In order to run the tutorial, you will need to create an account in a PyBossa. 
The PyBossa server could be running in your computer or in a third party
server.

.. note:

   You can use http://pybossa.com for testing. 

When you create the account, you will have to access your profile, and copy the
API-KEY that has been generated for you. This API-KEY allows you to create the
application in PyBossa (only authenticated users can create applications and
tasks, while everyone can collaborate solving the tasks).

Creating the Application
========================

There two possible ways for creating an application:

  * Using the **web interface**: the top menu bar has a section called
    Applications, that will have an option for creating an application.
  * Using the **RestFUL API**: you can check the source code of the
    createTasks.py script for more details about creating an application using
    the API.

For this tutorial we are going to use the second option, the RestFUL API via
the createTasks.py script. The script will require a URL and an API-KEY to
authenticate you in the PyBossa server. The following section gives more
details about how to use the script.

Creating the Tasks and Application
==================================

The createTasks.py script has a full example about how it is possible to create
an application, and several tasks for the application. PyBossa will deliver the
tasks for the users (authenticated and anonymous) and store the submitted
results in the PyBossa data base.

The script gets the latest 20 published photos in the Flickr public feed and
save the *link* the Flickr web page that publishes the photo, and the *direct url* 
of the image.

For example:

  * **Link**: http://www.flickr.com/photos/teleyinex/2945647308/
  * **URL**: http://farm4.staticflickr.com/3208/2945647308_f048cc1633_m.jpg

Those two variables (Link and URL) will be stored in a JSON object::

  { 'link': 'http://www.flickr.com/photos/teleyinex/2945647308/',
    'url': 'http://farm4.staticflickr.com/3208/2945647308_f048cc1633_m.jpg' }

And saved into the task field **info** of the task model. As Flickr only
publishes the latest 20 uploaded photos in their public feed, the script will
create 20 tasks in PyBossa.

.. note::

  Sometimes the script fails because Flickr does not provide a sane JSON object,
  so you will have to re-run it until you get a successful run.

In order to create the application and its tasks, run the following script::

  python createTasks.py -u http://PYBOSSA-SERVER -k API-KEY

Here is a list of all the Python methods that use the PyBossa API:

.. automodule:: createTasks 
   :members: create_app, update_app, delete_app

Presenting the Tasks to the user
================================

In order to present the tasks to the user, you have to create an HTML template.
The template has only the skeleton for loading the tasks data (the photos
images) and the questions and answers that users can provide for the given
task.

In this tutorial, Flickr Person uses a basic HTML skeleton and the PyBossa.JS
library to load the data of the tasks into the HTML template, and take actions
based on the users's answers.

.. note::
  When a task is submitted by an authenticated user, the task will save his
  user_id. For anonymous users the submitted task will only have the user IP
  address.

1. The HTML Skeleton
--------------------

The file_ **template.html** has the skeleton to show the tasks. The file has three 
sections or <div>:

  * **<div> for the warnings actions**. When the user saves an answer, a success
    feedback message is shown to the user. There is also an error one for
    the failures.
  * **<div> for the Flickr image**. This div will be populated with the task
    photo URL and LINK data.
  * **<div> for the Questions & Answer buttons**. There are three buttons with the possible
    answers: *Yes*, *No*, and *I don't know*.

At the end of the skeleton we load the Javascript: 

 * the PyBossa.JS library: <script src="/static/js/pybossa/pybossa.js" type="text/javascript"></script>
 * and the script to load the data, request new tasks, etc.: <script></script>

.. _file: https://github.com/PyBossa/app-flickrperson/blob/master/app-flickrperson/template.html

This template file will be used by the **createTasks.py** script to send the
template as part of the JSON object that will create the tasks. In PyBossa
every application has a **presenter** endpoint:

 * http://PYBOSSA-SERVER/app/SLUG/presenter

.. note::
   The **slug** is the short name for the application, in this case **flickrperson**. 

The presenter will load the skeleton and JavaScript for the application task.
The header and footer will be provided by PyBossa, so the template only has to
define the structure to load the data from the tasks and the action buttons to
retrieve and save the answer from the volunteers.

2. Loading the Task data
------------------------

All the action takes place in the file_
**template.html** script section, after the pybossa.js library.

The script is very simple, it uses the PyBossa.JS library to get a new task and
to submit and save the answer in the server.

PyBossa.JS provides a method to get the data for a task that needs to be solved
by the volunteer:

  * pybossa.newTask( applicationName )

In this case, applicationName will be "flickrperson". The library will get
a task for the application and return a JSON object with the following format::

  { question: application.description,
    task: { 
            id: value,
            ...,
            info: { 
                    url: 
                    link:
                   } 
          } 
  }

Therefore, if we want to load the data into the skeleton, we will only have to
do something like this::

  $("#question h1").text(data.question);
  $("#task-id").text(data.task.id);
  $("#photo-link").attr("href", data.task.info.link);
  $("#photo").attr("src",data.task.info.url);

and wrap it in the pybossa.newTask method::

  pybossa.newTask( "flickrperson").done(
    function( data ) {
      $("#question h1").text(data.question);
      $("#task-id").text(data.task.id);
      $("#photo-link").attr("href", data.task.info.link);
      $("#photo").attr("src",data.task.info.url);
    };
  );

Every time that we want to load a new task, we will have to call the above
function, so it will be better if we create a specific function for this
purpose (check the loadData function in the script).

Once the data have been loaded, it is time to bind the action buttons to
actions that will save the answer from the user.

3. Saving the answer
--------------------

Once the task has been presented, the users can click on the answer buttons: **Yes**, **No** or **I don't know**.
*Yes* and *No* save the answer in the DB (check **/api/taskrun**) with information about the task and the answer,
while the button *I don't know* simply loads another task as sometimes the
image is not available (the Flickr user has delete it) or it is not clear if
there is a human or not in the image (you only see one hand and nothing else). 

In order to submit and save the answer from the user, we will use again the
PyBossa.JS library. In this case::

  pybossa.saveTask( taskid, answer )

The **pybossa.saveTask** method saves an answer for a given task. In the
previous section we saved in the DOM the task-id that we have loaded, so we can
retrieve this value and use it for saving the volunteer's answer.

The method allows us to give a successful pop-up feedback for the user, so we
will use the following structure to warn the user and tell him that his answer
has been saved, and load a new Task::

  pybossa.saveTask( taskid, answer ).done(
    function( data ) {
        // Show the feedback div
        $("#success").fadeIn(); 
        // Fade out the pop-up after a 1000 miliseconds
        setTimeout(function() { $("#success").fadeOut() }, 1000);
        // Finally, load a new task
        pybossa.newTask("flickrperson").done( function( data ){ loadData( data ) });
    };
  );

Now we only have to bind the action of the Yes and No buttons to call the above
snippet. In order to bind it, we will use the onclick event to call a new and
simple function for both buttons:

 * <button class="btn btn-success" onclick="submitTask('Yes')">Yes</button>
 * <button class="btn btn-info" onclick="submitTask('No')">No</button>

The function submitTask will get the task-id from the DOM, and the answer is
the string 'Yes' or 'No' depending on which button the user has clicked. The
only missing button is the "I don't know" which will use the same event,
onclick, to request a new task using the pybossa.newTask function:

 * <button class="btn" onclick="pybossa.newTask('flickrperson').done( function( data ) { loadData( data ) });">I don't know</button>

For more details about the code, please, check the `template file
<https://github.com/PyBossa/app-flickrperson/blob/master/app-flickrperson/template.html>`_
for more details about all the steps.

4. Test the task presenter
--------------------------

In order to test the application task presenter, go to the following URL:

 * http://PYBOSSA-SERVER/app/SLUG/presenter

The presenter will load one task, and you will be able to submit and save one
answer for one task.
