var dynamoDB = new AWS.DynamoDB({endpoint: "https://dynamodb.us-east-1.amazonaws.com", region:"us-east-1"});
var params = {
  TableName : 'test-table',
  Item: {
    'username': { "S": "Tadas" },
    'last_name': { "S": "A" }
  }
};

var params2 = {
  TableName : 'test-table',
  Key: {
    'username': { "S": "Tadas" },
    'last_name': { "S": "A" }
  }
};

dynamoDB.listTables({}, function(err, data) {
  if (err) console.log(err, err.stack); // an error occurred
  else     console.log(data);           // successful response
});

dynamoDB.putItem(params, function(err, data) {
  if (err) console.log(err, err.stack); // an error occurred
  else     console.log(data);           // successful response
});

var params_scan = {
  TableName : 'test-table'
}

dynamoDB.scan(params_scan, function(err, data) {
  if (err) console.log(err, err.stack); // an error occurred
  else     console.log(data);           // successful response
});


dynamoDB.getItem(params2,function(err, data) {
  if (err) console.log(err);
  else console.log(data);
});