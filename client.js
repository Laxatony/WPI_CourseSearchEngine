//Global Variables
var gCourses = [];

var connection = new WebSocket('ws://localhost:1111');
connection.onopen = function () {};

// Log errors
connection.onerror = function (error) {
    console.error('WebSocket Error ' + error);
};

// Get messages from the server and do further job
connection.onmessage = function (e) {
    var res = JSON.parse(e.data);

    if(res['func'] == 'search_courses') {
        gCourses = res['data'];
        update_courseList();
    }
};
// ====================================================================
// function for passing message to server

// Send query to Server
function search_courses() {
	clean_all_display();
    var text = document.getElementById('queryBox').value;
    var data = {
        func: 'search_courses',
        query: text
    };
    connection.send(JSON.stringify(data));
}

function clean_all_display() {
    document.getElementById("course_list").innerHTML = "";
    document.getElementById("course_description").innerHTML = "";
}

function update_courseList() {

    if(gCourses.length == 0) {
        document.getElementById("course_list").innerHTML = "No Result";
        document.getElementById("course_description").innerHTML = "No Result";
        return;
    }

    var targetDIV = document.getElementById("course_list");
    targetDIV.innerHTML = "";
    
    //Create DIV for each course(in gCourses) for display
    for(var index=0 ; index<gCourses.length ; index++) {
        var course = gCourses[index]
        
        //New an element for insert
        var element = document.createElement("div");

        //Assign attributes to the element.
        element.setAttribute("role", "button");
        element.setAttribute("class", "course_bref");
        element.setAttribute("tabindex", index);
        element.setAttribute("title", course['cid']);
        
        //Edit content in list blocks
        stringBuf = ""
        stringBuf += (index+1) + ". "
        stringBuf += course['title']
        stringBuf += "<br>"
        stringBuf += '____________________<br>'
        stringBuf += 'Term: ' + course['term'] + ',  '
        stringBuf += 'CRN: ' + course['reference'] + '<br>'
        stringBuf += 'Subject: ' + course['subject'] + '<br>'
        stringBuf += 'Index: ' + course['course_index']
        element.innerHTML = stringBuf
        
        //Binding description
        element.addEventListener('click', function(){show_description(this.title);});
        
        //Insert into div
        targetDIV.appendChild(element);
    }
}

// Show details based on given ele
function show_description(cid) {

    // Find course object using title(cid)
    var index = 0;
    for(;index<gCourses.length;index++) {
        if(gCourses[index]['cid'] === cid) {
            break;
        }
    }
    var course = gCourses[index];

    // Show details in DIV: course_description
    
    //Get target div and clean it
    var targetDIV = document.getElementById("course_description");
    targetDIV.innerHTML = "";

    //Insert into div
    stringBuf = ""
    stringBuf += "<p>";
    stringBuf += "<strong>"
    stringBuf += course['title'];
    stringBuf += "</strong>"
    stringBuf += "</p>"

    //Insert informations
	stringBuf += "<font size='2'>"
    stringBuf += "<table id='course_details' border='1'>"

    stringBuf += "<tr>"
    stringBuf += "<th>Term</th><th>CRN</th><th>Subject</th><th>Course</th>"
    stringBuf += "<th>Section</th><th>Campus</th><th>Days</th><th>Time</th><th>Capacity</th>"
    stringBuf += "<th>Registerd</th><th>Remaining</th><th>Instructor</th><th>Date</th><th>Location</th>"
    stringBuf += "</tr>"

    stringBuf += "<tr>"
    stringBuf += "<td>" + course['term'] + "</td>"
    stringBuf += "<td>" + course['reference'] + "</td>"
    stringBuf += "<td>" + course['subject'] + "</td>"
    stringBuf += "<td>" + course['course_index'] + "</td>"
    stringBuf += "<td>" + course['section'] + "</td>"
    stringBuf += "<td>" + course['campus'] + "</td>"
    stringBuf += "<td>" + course['days'] + "</td>"
    stringBuf += "<td>" + course['time'] + "</td>"
    stringBuf += "<td>" + course['capacity'] + "</td>"
    stringBuf += "<td>" + course['registered'] + "</td>"
    stringBuf += "<td>" + course['remaining'] + "</td>"
    stringBuf += "<td>" + course['instructor'] + "</td>"
    stringBuf += "<td>" + course['date'] + "</td>"
    stringBuf += "<td>" + course['location'] + "</td>"
    stringBuf += "</tr>"

    stringBuf += "</table>"
	stringBuf += "</font>"

    stringBuf += "<br>";
	
	stringBuf += "<font size='2'>"
    stringBuf += "<p>";
    stringBuf += course['description'];
    stringBuf += "</p>"
	stringBuf += "</font>"


    targetDIV.innerHTML = stringBuf;
}

// Support search with pressing [Enter] key
function inputKeyPress(e) {
    e=e||window.event;
    var key = e.keyCode;
    if(key==13) //Enter
    {
        document.getElementById("queryBox").blur();
        search_courses();
        return false; //return true to submit, false to do nothing
    }
  }