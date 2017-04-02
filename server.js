var express = require('express');
var app = express();
var path = require('path');

app.set('view engine', 'html');
app.use(express.static(__dirname + '/'));

app.get('/', function(req,res){
	res.sendFile(path.join(__dirname+'/index.html'));
});

app.listen(3000, function(){
	console.log("hello");
});