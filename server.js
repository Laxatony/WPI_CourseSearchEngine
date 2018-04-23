var PythonShell = require('python-shell');

var Server = require('ws').Server;
var port = 1111;
var ws = new Server({port: port});

ws.on('connection', function(w){
    w.on('message', function(msg){
        var receieveObj = JSON.parse(msg);

        console.log('1Receive object from client: ' + receieveObj.func);

        if(receieveObj.func == "search_courses") {
            var options = {
                args: [msg]
            };
            console.log('2Receive object from client: ' + receieveObj.func);

            PythonShell.run('pythonFiles/main.py', options, function (err, results) {
                console.log('3Receive object from client: ' + receieveObj.func);
  
                var data = JSON.parse(results); //string to json
                //data = JSON.stringify(data);
                console.log('4Receive object from client: ' + receieveObj.func);
  
                var res = {
                    'func': receieveObj.func,
                    'data': data
                }
                console.log('5Receive object from client: ' + receieveObj.func);
  
                var res = JSON.stringify(res); // json to string
                console.log('ready to send');
                if(!(w.readyState === w.CLOSED))
                    w.send(res); // sent json string back to client
            });
        }
    });
  
    w.on('close', function() {
        console.log('closing connection');
    });
});