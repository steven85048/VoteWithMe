var name = document.getElementById('name');
var email = document.getElementById('email');
var ccnumber = document.getElementById('ccnumber');
var cvc = document.getElementById('cvc');
var expmonth = document.getElementById('expmonth');
var expyear = document.getElementById('expyear');
var zip = document.getElementById('zip');
var password = document.getElementById('password');

var globalCounter = 0;
var findThis = document.getElementById('cardparent');

window.onload = function() {
	console.log("STARTING");
	loadDoc(url1, callback1);
}

var url1 = "http://10.101.39.17:5000/getBillsSortedId";
var url2 = "http://10.101.39.17:5000/getBillById"

var callback2 = function(json_object, billid){
	console.log(JSON.stringify(json_object));
	if(globalCounter % 3 == 0)
	{
		var div1 = document.createElement('div');
		div1.className = 'card-container';
		findThis.appendChild(div1)
	}

	var div2 = document.createElement('div');
	div2.className = 'card-inner';
	var div3 = document.createElement('div');
	div3.className = 'card-header';
	var div4 = document.createElement('div');
	div4.className = 'card-body';
	var header = billid;
	div3.innerHTML = header;
	var title = json_object.results[0].title;
	div4.innerHTML = title;
	div2.appendChild(div3);
	div2.appendChild(div4);
	div1.appendChild(div2);
	globalCounter++;
	$('#example li:last').append(div1);
};

var callback1 = function (callback2){
	var dataArr = [];

	var initialList = obj._embedded.events;
	console.log(initialList);
	for (var i = 0 ; i < initialList.length; i++){
		var currItem = eventList[i];
		console.log(currItem);

		var bill_id = currItem.bill_id;

		// add that to your first view 

		loadDoc(url2 + bill_id, callback2);

		var JSONOBject = loadDoc();

		callback2(JSONObject, bill_id);
	}
	fillBill(JSONOBject);
}

function loadDoc(url, callback) {
  var xhttp = new XMLHttpRequest();
  console.log('hello');
  xhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
     	callback(JSON.parse(xhttp.responseText));
    }
  };

  xhttp.open("GET", url, true);
  xhttp.send();
}

function fillBill(obj){
	var billArr = [];

	var billList = obj._embedded.events;
	for(var j = 0; j < billList.length; j++){
		var billJSON = billList[j];
		var billData = { billID: billJSON.bill_id,
						billDescription: billJSON.title};
		billArr.push(billData);
		return billArr;
	}

}