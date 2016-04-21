// collection for our activity logs

Logs = new Mongo.Collection("logs");

if (Meteor.isServer) {
	Meteor.methods({
		// each one corresponds to a project, so we 
		// always associate a log with the unique project id
		insertLog: function(logAttributes) {
			check(this.userId, String);
			check(logAttributes, {
				projectId: String,
		        projectName: String,
		        log: [Match.Any]
			});
			return Logs.insert(projectLog);
		},

		// every log item has the attributes listed in this function; 
		// the update will just append a new activity each time.
		updateLog: function(projectId, addActivity) {
			check(projectId, String);
			check(this.userId, String);
			check(addActivity, {
				description: String,
				color: String,
				link: String,
				tag: String
			});
			addActivity.user = Meteor.user().username;
			addActivity.submitted = new Date();
		
			return Logs.update({projectId: projectId}, {$push: {log: addActivity}});
		}
	});
}