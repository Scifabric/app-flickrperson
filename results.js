// Flickr Person Finder results page
// Copyright (C) 2012 Daniel Lombraña González
// 
// This program is free software: you can redistribute it and/or modify
// it under the terms of the GNU General Public License as published by
// the Free Software Foundation, either version 3 of the License, or
// (at your option) any later version.
// 
// This program is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// GNU General Public License for more details.
// 
// You should have received a copy of the GNU General Public License
// along with this program.  If not, see <http://www.gnu.org/licenses/>.

var lt = []; // List of Task array: circular buffer with an index:
var index = 0; // index for the buffer, it will show the next task
var url = "http://crowdcrafting.org/api/" // URL to query the PyBossa API
var xhr = $.getJSON(url + "app?short_name=flickrperson"); // In this case Flickr Person
var app_id;

// Get the application ID for loading the submitted tasks and results
xhr.done( function( data ){
    app_id = data[0].id;
    var tasks = $.getJSON(url + "task?app_id=" + app_id + "&limit=400");
    // Once all the tasks for this application have been loaded, create the
    // circular buffer
    tasks.done( function(data){
        for (i = 0; i < data.length; i++) {
            lt.push([app_id, data[i].id]);
        }
    // Load the pie chart for the first task in the circular buffer 
    create_arcs();
    });
});

// Initialization for the arc pie
var data = [2,2];

// Some code comes from 
// http://bl.ocks.org/1346410
// by mbostock

// Size, colors, etc. for the pie
var w = 470,
    h = 400,
    r = Math.min(w, h) / 2,
    outerRadius = r,
    innerRadius = r *.6,
    //color = d3.scale.category20(),
    color = d3.interpolateRgb("#729fcf", "#ad7fa7"),
    donut = d3.layout.pie().sort(null),
    arc = d3.svg.arc().innerRadius(r * .4).outerRadius(r);

// We only want a half pie, not a full circle
donut.startAngle([-Math.PI/2]);
donut.endAngle([Math.PI/2]);

// Create the SVG and the arc
var svg = d3.select("#arcs").append("svg:svg")
    .attr("width", w)
    .attr("height", h)
  .append("svg:g")
    .attr("transform", "translate(" + w / 2 + "," + h / 2 + ")");

// Load the data with the donut facility (it computes for us the startin and
// ending degrees for the arcs
var arcs = svg.selectAll("path")
    .data(donut(data));

// Store the arcs info for making the nice transitions
arcs.enter().append("svg:path")
    .attr("fill", function(d, i) { return color(i); })
    .each(function(d) {this._current = d;})
    .attr("d", arc);

// Include a description for the task that has been loaded
var title = svg.append("text")
     .attr("class", "title")
     .attr("dx", "-2em")
     .attr("class", "badge badge-warning")
     .text("Task ID: ");

// Include a description about the number of Yes votes
var yes = svg.append("text")
     .attr("class", "title")
     .attr("dx", "-4em")
     .attr("dy", "3em")
     .attr("fill", color(0))
     .text("Number of Yes votes: ");

// Include a description about the number of No votes
var no = svg.append("text")
     .attr("class", "title")
     .attr("dx", "-4em")
     .attr("dy", "4em")
     .attr("fill", color(1))
     .text("Number of No votes: ");

// Function to populate the arcs with data from Flickr Person App
function create_arcs(formTaskId) {
    // Be sure that the index has not reached the end of the buffer, otherwise
    // set it to zero again
    if (index >= lt.length) { index = 0;}
    // Set the appId and taskId variables for requesting the data 
    var taskId = lt[index][1];
    var appId = lt[index][0];
    // If the user has asked for the data of a specific task, load that task
    if (formTaskId != undefined) { taskId = parseInt(formTaskId); }
    // Populate the skeleton with the data
    title.text("Task ID: " + taskId);
    // Get the Task Image URL for comparing the answer of the volunteers and
    // the real photo
    var img = $.getJSON(url + "task/" + taskId);
    img.done(function(data){
        // Load the _b size and not the _m size from Flickr
        //var url = data.info.url_m.replace("_m.jpg","_b.jpg");
        $("#flickr").attr("src",data.info.url_b);
    });

    // Get the answers for the task
    var answers = $.getJSON(url + "taskrun?app_id=" + appId + "&task_id=" + taskId +"&limit=100");

    // When all the data have been retrieved, populate the chart
    answers.done( function ( data ){
        // Update the index to load the next task with the blue button
        index = index + 1;
        // Feedback for the user
        $("#next").text("Check task: " + lt[index][1]);

        // Initialize some variables
        var length = data.length;
        var tmp = [0,0]

        // Compute the number of answers of Yes and No for the given task
        for (i=0;i<length;i++) {
            if (data[i].info === "Yes") {
                tmp[0] = tmp[0] + 1;
            }
            else {
                tmp[1] = tmp[1] + 1;
            }
        }
        
        arcs = arcs.data(donut(tmp)); //update the data
        //arcs.attr("d", arc); // redraw the arcs without an animation
        no.text("Number of No votes: " + tmp[1]);
        yes.text("Number of Yes votes: " + tmp[0]);
        // Redraw the arcs with an animation
        arcs.transition().duration(750).attrTween("d", arcTween);
        });
}

// Function to load the data of a specific task
function create_arcs_for() {
    create_arcs($("#taskId").val());
};

// The following code comes from 
// http://bl.ocks.org/1346410
// by mbostock
// Store the currently-displayed angles in this._current.
// Then, interpolate from this._current to the new angles.
function arcTween(a) {
  var i = d3.interpolate(this._current, a);
  this._current = i(0);
  return function(t) {
    return arc(i(t));
  };
}
