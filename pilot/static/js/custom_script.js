$(function () {
  $('[data-toggle="tooltip"]').tooltip()
})

function OnSubmitForm() {
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