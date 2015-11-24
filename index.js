$(document).ready(function() {
		$.ajax({
			url: "http://127.0.0.1:5000/surgery/0",
			type: "GET",
			dataType: "json",
			contentType: "application/json",
			success: function(result) {
				console.log("hello world");
				console.log(result);
				var table = $("#table tbody");
				$.each(result, function(idx, elem) {
					table.append("<tr><td>"
					+elem.surgery_name+"</td><td>"
					+elem.month+"</td><td>"
					+elem.day+"</td><td>"
					+elem.year+"</td></tr>");
				});
			}
		});
});


