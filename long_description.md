Flickr Person is a **demo application** for PyBossa that shows how you can
crowdsourcing an image classification problem.

This application uses the Flickr web service as the source of the data. By
using Flickr, we have the possibility of using its API to refine the searches,
and looking for specific tags or descriptions that match a specific criteria,
i.e. houses of 1920 or tsunami.

In this demo application, we use a very simple approach by polling the latest
20 published photos in the public Flickr feed.

The feed provides the direct link to the photo. This link is used to show the
image to the users, and ask them the following question: **Do you see a human
in this photo?**

The application provides three simple answers as action buttons:

  * Yes
  * No and
  * I don't know

![](http://farm7.staticflickr.com/6109/6286728068_2f3c6912b8_q.jpg)

Based on the answer of the users, we will be able to classify the photos,
distributing the tasks (thanks to PyBossa) to different users and volunteers.

__ Note If you want to learn more about how to use this application as a
template, check the:

  * [source code](http://github.com/PyBossa/app-flickrperson)
  * [ Google Spreadsheet Task Template](https://docs.google.com/spreadsheet/ccc?key=0AsNlt0WgPAHwdHFEN29mZUF0czJWMUhIejF6dWZXdkE&usp=sharing#gid=0)
  * [the official documentation of PyBossa](http://docs.pybossa.com/) and 
  * [the step by step tutorial.](http://docs.pybossa.com/en/latest/user/tutorial.html)

* * *

