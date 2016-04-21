$(document).ready(function() {
		$.ajax({
			url: "http://127.0.0.1:5000/surgery/0",
			type: "GET",
			dataType: "json",
			contentType: "application/json",
			success: function(result) {
				var table = $("#table tbody");
				$.each(result, function(idx, elem) {
					table.append("<tr><td>"
					+elem.surgery_name+"</td><td>"
					+elem.month+"</td><td>"
					+elem.day+"</td><td>"
					+elem.year+"</td><td>"
					+"<button onclick='myFunction(" + elem.id + ")'>Generate</button></td></tr>");
				});
			}
		});
});
function myFunction(id) {
	$.ajax({
			url: "http://127.0.0.1:5000/pdf/" + id,
			type: "GET",
			success: function(result) {
				console.log(result);
			}
		});

}
