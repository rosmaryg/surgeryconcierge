$(function () {
  $('[data-toggle="tooltip"]').tooltip()
})

function OnSubmitForm() {
	if (document.getElementById("phone-number").value === "+1 ") {
		window.alert("Please enter your phone number!");
		return false;
	}

	var mystring = document.getElementById("insn10").value;
	var newchar = '('
	document.getElementById("insn10").value = mystring.split('[').join(newchar);

	var mystring = document.getElementById("insn10").value;
	var newchar = ')'
	document.getElementById("insn10").value = mystring.split(']').join(newchar);

	if (document.pressed == 'Get PDF') {
		document.myform.action ="generate-pdf"; 
	} else if (document.pressed == 'Get ICS') {
		document.myform.action ="generate-ics";
	} else if (document.pressed == 'Get Calendar') {
		document.myform.action ="generate-calendar";
	} else if(document.pressed == 'Get Texts') {
		document.myform.action ="generate-text";
	}
	return true;
}