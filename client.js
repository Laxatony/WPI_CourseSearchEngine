//Global Variables
var gCourses = [];

// var connection = new WebSocket('ws://ec2-52-23-176-195.compute-1.amazonaws.com:1111');
var connection = new WebSocket('ws://localhost:1111');
connection.onopen = function () {};

// Log errors
connection.onerror = function (error) {
    console.error('WebSocket Error ' + error);
};

// Get messages from the server and do further job
connection.onmessage = function (e) {
    var res = JSON.parse(e.data);

    if(res['func'] == 'retrieveTimeStamp') {
        var resultString = 'Timestamp is ' + res['time'];

        document.getElementById("demo").innerHTML = resultString;
    }
    else if(res['func'] == 'sum2') {
        var x = 0;
        var resultString = res['data']['num1'] + ' + ' + res['data']['num2'] + ' is ' + res['data']['result'][x];

        document.getElementById("demo").innerHTML = resultString;
    }
    else if(res['func'] == 'search_courses') {
        gCourses = res['data'];
        update_courseList();
    }
};
// ====================================================================
// function for passing message to server

// Send query to Server
function search_courses() {
    var text = document.getElementById('queryBox').value;
    var data = {
        func: 'search_courses',
        query: text
    };
    connection.send(JSON.stringify(data));
}

function update_courseList() {

    //Get target div and clean it
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
        stringBuf += course['title']
        stringBuf += "<br>"
        stringBuf += '____________________<br>'
        stringBuf += 'Term: ' + course['term'] + '<br>'
        stringBuf += 'Subject: ' + course['subject'] + '<br>'
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

    stringBuf += "<p>";
    stringBuf += course['description'];
    stringBuf += "</p>"


    targetDIV.innerHTML = stringBuf;
}