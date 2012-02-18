==========
Quickstart
==========

1.- Get the source code cloning/forking the repository:

  git clone https://github.com/PyBossa/app-flickrperson/

Or download the ZIP file from this URL:

  https://github.com/PyBossa/app-flickrperson/zipball/master

2.- Then, you will only have to access the folder that will have three files:

  * flickrperson.html This is the view for your application, what the volunteer will see and interact with.
  * js/flickrperson.js This file will get the tasks from pybossa, show to the user and record the answer from the volunteer back in PyBossa
  * flickperson.py This is the script that will allow you to create the application in PyBossa and several tasks for the user.
     
3.- Create an account in http://pybossa.ep.io (check the Register option!)
4.- Check your profile, your user name in blue in the top bar, to get your API-KEY
5.- Copy and Paste the API-KEY so you can create the application and the tasks (modify the name if you want for the application) using the flickrperson.py script.
6.- Run the command python flickrperson.py -u http://pybossa.ep.io/api -k API-KEY

.. note:

  Sometimes Flickr will fail, so you will have to re-run the flickrperson.py script

7.- Load flickrpserson.html in your browser, so you should be able to see the tasks that your application has created.
