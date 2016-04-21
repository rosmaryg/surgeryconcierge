$(document).ready(function() {
		$.ajax({
			url: "http://127.0.0.1:5000/patient/7",
			type: "GET",
			dataType: "jsonp",
			contentType: "application/json",
			success: function(result) {
				var table = $("#table tbody");
				$.each(result, function(idx, elem) {
					table.append("<tr><td>"
					+elem.pdf_link+"</td><td>"
					+elem.cal_link+"</td><td></tr>");
				});
			}
		});
});