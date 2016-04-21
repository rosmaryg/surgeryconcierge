AWS.config.update({accessKeyId: 'AKIAJUJB7DVFDSGOBNOQ',
	    secretAccessKey: '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'});

var dynamoDB = new AWS.DynamoDB({endpoint: "https://dynamodb.us-east-1.amazonaws.com", region:"us-east-1"});
$('.dropdown-toggle').dropdown()

// dynamoDB.listTables({}, function(err, data) {
// 	if (err) console.log(err, err.stack);
// 	else     console.log(data);
//     });
// toDelete = ["Dw2iOJ6DEH"]
// for (var i = 0; i < toDelete.length; i++) {
// 	var params = {
// 	  TableName : 'surgery-concierge-surgeries',
// 	  Key: {
// 	    'access_key': { "S": toDelete[i] }
// 	  }
// 	};

// 	dynamoDB.deleteItem(params, function(err, data) {
// 	  if (err) console.log(err, err.stack); // an error occurred
// 	  else     console.log(data);           // successful response
// 	});
// }


dynamoDB.scan({ TableName: 'surgery-concierge-templates' }, function(err, data) {
	if (err) console.log(err, err.stack);
	else {
	    console.log(data);
	    var putIn = "<a href='#'><i>No templates found</i></a>";
	    var menu = document.getElementById("myDropdown");
	    if (data.Items.length > 0) {
	        putIn = "";
			for (var i = 0; i < data.Items.length; i++) {
			    var info = data.Items[i].template_name['S'];
			    putIn += "<a href='javascript:displayContents(" + data.Items[i].insns['S'] + ")'>" + info + "</a>";
			}
	    }
	    menu.innerHTML = putIn;
	}                                                        
});

var existing_access_keys = [];

dynamoDB.scan({ TableName: 'surgery-concierge-surgeries' }, function(err, data) {
	if (err) console.log(err, err.stack);
	else {
		console.log(data)
		for (var i = 0; i < data.Items.length; i++) {
			existing_access_keys.push(data.Items[i].access_key['S'])
		}
	}
});

function myFunction() {
    document.getElementById("myDropdown").classList.toggle("show");
}

window.onclick = function(event) {
    if (!event.target.matches('.dropbtn')) {
	var dropdowns = document.getElementsByClassName("dropdown-content");
	var i;
	for (i = 0; i < dropdowns.length; i++) {
	    var openDropdown = dropdowns[i];
	    if (openDropdown.classList.contains('show')) {
		openDropdown.classList.remove('show');
    		document.getElementById("sect").innerHTML = event.target.innerHTML; 
	    }
	}
    }
}


function onSubmitForm() {
    var o = {};
    var idx = 0;
    var tbody = document.getElementById("myTable").children[1];
    for(var i = 0; i < tbody.rows.length; i++) {
		if (tbody.rows[i].cells[0].firstChild.checked) {
		    var toAdd = [{'insn': tbody.rows[i].cells[3].firstChild.value},
				 {'time': tbody.rows[i].cells[4].firstChild.value},
				 {'time_unit': tbody.rows[i].cells[5].firstChild.value}];
		    o[idx++] = toAdd;
		}
    }
    var key = "";
    var possible = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";
    while (key == "" | existing_access_keys.indexOf(key) != -1) {
	key = "";
    	for ( var i=0; i < 10; i++ ) {
    		key += possible.charAt(Math.floor(Math.random() * possible.length));
    	}
    }
    
	var params = {
	  TableName : 'surgery-concierge-surgeries',
	  Item: {
	    'access_key': { "S": key },
	    'insns': { "S": JSON.stringify(o) },
	    'date': { "S": document.getElementsByName("date")[0].value }
		}
	};
	dynamoDB.putItem(params, function(err, data) {
        if (err) {
		    console.log("Unable to put item. Error JSON:", JSON.stringify(err, null, 2));
		    alert("Error adding template. Please try again.");
		} else {
		    console.log("PutItem succeeded:", JSON.stringify(data, null, 2));
			var h = document.getElementById("key");
			var t = document.createTextNode(key);
			h.appendChild(t); 
			var w = window.open();
		  	var head = $("#toNewWindowHead").html();
		    $(w.document.head).html(head);
		  	var body = $("#toNewWindowBody").html();
		    $(w.document.body).html(body);
		    location.reload();
		}
    });
}

function displayContents(info) {
	var table = document.getElementById("myTable");
	document.getElementById("insn-table").style.display = "inline";
	var new_tbody = document.createElement('tbody');
	table.replaceChild(new_tbody, table.children[1])
    var idx = -1;
    for (var k in info) {
		if (k == "title") continue;
		var row = new_tbody.insertRow(idx++);
		var cell1 = row.insertCell(0);
		var cell2 = row.insertCell(1);
		var cell3 = row.insertCell(2);
		var cell4 = row.insertCell(3);
		var cell5 = row.insertCell(4);
		var cell6 = row.insertCell(5);
		cell4.style.display = "none";
		cell5.style.display = "none";
		cell6.style.display = "none";
		var plural = "";
		if (info[k][2].time > 1) {
			plural = "s";
		}
		cell1.innerHTML = "<input type='checkbox' checked/>";
		cell2.innerHTML = info[k][0].cond;
		cell3.innerHTML = info[k][1].insn + " " + info[k][2].time + " " + info[k][3].time_unit.slice(0, -1) + plural + " before the surgery";
		cell4.innerHTML = "<input type='text' value='" + info[k][1].insn + "'/>";
		cell5.innerHTML = "<input type='text' value='" + info[k][2].time + "'/>";
		cell6.innerHTML = "<input type='text' value='" + info[k][3].time_unit + "'/>";
    }
}
