$(document).ready(function() {
		$.ajax({
			url: "http://127.0.0.1:5000/surgery/0",
			type: "GET",
			dataType: "json",
			contentType: "application/json",
			success: function(result) {
				console.log("hello world");
				console.log(result);
				/*var table = $("#table").dataTable();
				for(var i = 0; i < result.length; i++) {
					table.fnAddData([ s[i][0], s[i][1], s[i][2], s[i][3], s[i][4] ]);
				} */
			}
		});
});


