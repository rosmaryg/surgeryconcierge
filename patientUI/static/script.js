$(function () {
  $('[data-toggle="tooltip"]').tooltip()
})

AWS.config.update({accessKeyId: 'AKIAIRI6C6H53B2DJWKA',
 secretAccessKey: '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'});

var dynamoDB = new AWS.DynamoDB({endpoint: "https://dynamodb.us-east-1.amazonaws.com", region:"us-east-1"});

function getPatientInsns() {
	dynamoDB.scan({ TableName: 'surgery-concierge-surgeries' }, function(err, data) {
		if (err) console.log(err, err.stack);
		else {
			var key_found = false;
			var patient_object;
			var key_entered = document.getElementById("accessKey").value;
			var returned_items = data.Items;
			for (var key in returned_items) {
				if (key_entered === returned_items[key].access_key.S) {
					key_found = true;
					patient_object = returned_items[key];
					console.log(patient_object);
					document.getElementById("insns_ics").value = patient_object.insns.S;
					document.getElementById("insns_pdf").value = patient_object.insns.S;
					document.getElementById("insns_text").value = patient_object.insns.S;
					break;
				}
			}
			if (!key_found) {
				window.alert("The access key you entered was not found. Please check that you entered the correct access key and contact your doctor's office if your access key does not work.")
				return;
			} else {
				document.getElementById("notifs-buttons").style.display = "inline";
				document.getElementById("insn-block").style.display = "none";
			}
		}
	});
}

function getIcs() {
	console.log(document.getElementById("insns_ics").value);
}

function getPdf() {
	console.log(document.getElementById("insns_pdf").value);
}

function getTexts() {
	console.log(document.getElementById("insns_text").value);
}


// var params = {
//   TableName : 'surgery-concierge-surgeries',
//   Item: {
//     'access_key': { "S": "test" },
//     'ics': { "S": "blah1" },
//     'pdf' :{ "S": "blah2"},
//     'texts' :{ "S": "blah3"}
//   }
// };

// dynamoDB.putItem(params, function(err, data) {
//   if (err) console.log(err, err.stack); // an error occurred
//   else     console.log(data);           // successful response
// });

// var params = {
//   TableName : 'surgery-concierge-surgeries',
//   Key: {
//     'access_key': { "S": "test" }
//   }
// };

// dynamoDB.deleteItem(params, function(err, data) {
//   if (err) console.log(err, err.stack); // an error occurred
//   else     console.log(data);           // successful response
// });

// dynamoDB.listTables({}, function(err, data) {
//   if (err) console.log(err, err.stack); // an error occurred
//   else     console.log(data);           // successful response
// });


// var params_scan = {
//   TableName : 'surgery-concierge-surgeries'
// }

// dynamoDB.scan(params_scan, function(err, data) {
//   if (err) console.log(err, err.stack); // an error occurred
//   else     console.log(data);           // successful response
// });