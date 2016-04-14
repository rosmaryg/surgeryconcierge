AWS.config.update({accessKeyId: 'AKIAIRI6C6H53B2DJWKA',
 secretAccessKey: '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'});

var dynamoDB = new AWS.DynamoDB({endpoint: "https://dynamodb.us-east-1.amazonaws.com", region:"us-east-1"});

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
