var button1 = document.getElementById('mainButton1');

var openForm1 = function() {
	button1.className = 'active';
};

var checkInput1 = function(input) {
	if (input.value.length > 0) {
		input.className = 'active';
	} else {
		input.className = '';
	}
};

var closeForm1 = function() {
	button1.className = '';
};

document.addEventListener("keyup", function(e) {
	if (e.keyCode == 27 || e.keyCode == 13) {
		closeForm();
	}
});