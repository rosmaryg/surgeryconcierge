AWS.config.update({accessKeyId: 'AKIAIEZXTTUAHGFBCKZQ',
	    secretAccessKey: '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'});

var dynamoDB = new AWS.DynamoDB({endpoint: "https://dynamodb.us-east-1.amazonaws.com", region:"us-east-1"});
$('.dropdown-toggle').dropdown()
// var params = {
//   TableName : 'surgery-concierge-templates',
//   Key: {
//     'template_name': { "S": "blah" }
//   }
// };

// dynamoDB.deleteItem(params, function(err, data) {
//   if (err) console.log(err, err.stack); // an error occurred
//   else     console.log(data);           // successful response
// });
var existing_template_names = [];
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
			    existing_template_names.push(info);
			}
	    }
	    menu.innerHTML = putIn;
		
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
	    }
	}
    }
}

function createNewTemplate() {
    var table = document.getElementById("myTable");
    var row = table.insertRow(-1);
    var cell1 = row.insertCell(0);
    var cell2 = row.insertCell(1);
    var cell3 = row.insertCell(2);
    var cell4 = row.insertCell(3);
    cell1.innerHTML = "<input type='checkbox'/>";
    cell2.innerHTML = "<input type='text' placeholder='e.g. takes Aspirin regularly'/>";
    cell3.innerHTML = "<input type='text' placeholder='e.g. stop taking Aspirin'/>";
    cell4.innerHTML = "<input style='width:20%' type='number' min='0'/><select name='time_unit'><option value='days'>days</option><option value='weeks'>weeks</option></select>";
    return false;
}

function onSubmitForm() {
	var addItem = true;
    var n = document.getElementById("template-name").value.trim();
	if (n === "") {
		addItem = false;
		alert("Please enter a name for your template")
	} else if (existing_template_names.indexOf(n) != -1) {
		addItem = false;
		alert(n + " is an existing template; please retitle your new template")
	}
    var o = {};
    o["title"] = n;
    var idx = 0;
    var table = document.getElementById("myTable");
    for(var i = 1; i < table.rows.length; i++) {
		if (table.rows[i].cells[0].firstChild.checked) {
			if (table.rows[i].cells[1].firstChild.value === "" | table.rows[i].cells[2].firstChild.value === "" | table.rows[i].cells[3].children[0].value === "") {
				addItem = false;
				alert("Please enter a condition, instruction, and time for all instructions that you have checked off as part of the template")
			}
		    var toAdd = [{"cond": table.rows[i].cells[1].firstChild.value},
				 {"insn": table.rows[i].cells[2].firstChild.value},
				 {"time": table.rows[i].cells[3].children[0].value},
				 {"time_unit": table.rows[i].cells[3].children[1].value}];
		    o[idx++] = toAdd;
		}
    }
    if (addItem) {
    	var params = {
			TableName: 'surgery-concierge-templates',
			Item: {
			    'template_name' : { "S": n },
			    'insns' : { "S": JSON.stringify(o) }
			}
	    }
	    addToDB(params, n)
    }
}

function addToDB(params, name) {
	var form = document.getElementById("the-form");
	dynamoDB.putItem(params, function(err, data) {
        if (err) {
		    console.log("Unable to put item. Error JSON:", JSON.stringify(err, null, 2));
		    alert("Error adding template. Please try again.");
		} else {
		    console.log("PutItem succeeded:", JSON.stringify(data, null, 2));
		    form.reset();
		    alert(name +  " has been added.");
		}
    });
}

function displayContents(info) {
    var idx = 1;
    for (var k in info) {
		if (k == "title") continue;
		var table = document.getElementById("myTable");
		var row = table.insertRow(idx++);
		var cell1 = row.insertCell(0);
		var cell2 = row.insertCell(1);
		var cell3 = row.insertCell(2);
		var cell4 = row.insertCell(3);
		var plural = "";
		var timeUnit = "<select name='time_unit'><option value='days'>days</option><option value='weeks'>weeks</option></select>";
		cell1.innerHTML = "<input type='checkbox' checked/>";
		cell2.innerHTML = "<input type='text' value='" + info[k][0].cond + "'/>";
		cell3.innerHTML = "<input type='text' value='" + info[k][1].insn + "'/>";
		cell4.innerHTML = "<input id='time_entry' style='width:60px' type='number' min='0' value='" + info[k][2].time + "'/> " + timeUnit;
		cell4.children[1].value = info[k][3].time_unit;
    }
}