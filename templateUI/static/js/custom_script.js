AWS.config.update({accessKeyId: 'AKIAIEZXTTUAHGFBCKZQ',
	    secretAccessKey: '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'});

var dynamoDB = new AWS.DynamoDB({endpoint: "https://dynamodb.us-east-1.amazonaws.com", region:"us-east-1"});


dynamoDB.listTables({}, function(err, data) {
	if (err) console.log(err, err.stack);
	else     console.log(data);
    });


dynamoDB.scan({ TableName: 'surgery-concierge-templates' }, function(err, data) {
	if (err) console.log(err, err.stack);
	else {
	    console.log(data);
	    var putIn = "<a href='#'><i>No templates found</i></a>";
	    var menu = document.getElementById("myDropdown");
	    if (data.Items.length > 0) {
	        putIn = "";
		for (var i = 0; i < data.Items.length; i++) {
		    var info = JSON.parse(data.Items[i].template_name['S']);
		    putIn += "<a href='javascript:displayContents(" + data.Items[i].template_name['S'] + ")'>" + info['title'] + "</a>";
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
    cell2.innerHTML = "<input type='text'/>";
    cell3.innerHTML = "<input type='text'/>";
    cell4.innerHTML = "<input style='width:20%' type='number' min='0'/><select name='time_unit'><option value='days'>days</option><option value='weeks'>weeks</option></select>";
    return false;
}

function onSubmitForm() {
    var n = document.getElementById("template-name").value;
    var o = {};
    o["title"] = n;
    var idx = 0;
    var table = document.getElementById("myTable");
    for(var i = 1; i < table.rows.length; i++) {
	if (table.rows[i].cells[0].firstChild.checked) {
	    var toAdd = [{"cond": table.rows[i].cells[1].firstChild.value},
			 {"insn": table.rows[i].cells[2].firstChild.value},
			 {"time": table.rows[i].cells[3].children[0].value},
			 {"time_unit": table.rows[i].cells[3].children[1].value}];
	    o[idx++] = toAdd;
	}
    }
    var params = {
	TableName: 'surgery-concierge-templates',
	Item: {
	    'template_name' : { "S": JSON.stringify(o) }
	}
    }
    
    dynamoDB.scan({ TableName: 'surgery-concierge-templates' }, function(err, data) {
	    if (err) console.log(err, err.stack);
	    else {
		for (var i = 0; i < data.Items.length; i++) {
		    var info = JSON.parse(data.Items[i].template_name['S']);
		    console.log(n);
		    console.log(info['title']);
		    if (info['title'] == n) {
			console.log(n + " is an existing template; please retitle your new template.");
			return;
		    }
		}
	    }
	});

    dynamoDB.putItem(params, function(err, data) {
        if (err) {
	    console.log("Unable to put item. Error JSON:", JSON.stringify(err, null, 2));
	    alert("Error adding template. Please try again.");
	} else {
	    console.log("PutItem succeeded:", JSON.stringify(data, null, 2));
	    document.getElementByID("the-form").reset();
	    alert(n +  " has been added.");
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
	cell1.innerHTML = "<input type='checkbox' checked/>";
	cell2.innerHTML = "<input type='text' value='" + info[k][0].cond + "'/>";
	cell3.innerHTML = "<input type='text' value='" + info[k][1].insn + "'/>";
	cell4.innerHTML = "<input type='text' value='" + info[k][2].time + "'/>";
	console.log(info[k][0].cond);
    }
}