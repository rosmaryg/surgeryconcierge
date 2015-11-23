$(document).ready(function() {
		$.ajax({
			url: "http://127.0.0.1:5000/surgeries",
			type: "POST",
			
			success: function(result) {
				var table = $("#table tbody");
				$.each(data, 
			}
		});
	}
});


