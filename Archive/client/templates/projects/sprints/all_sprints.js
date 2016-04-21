// callback function launched when template is loaded
Template.allSprints.rendered = function() {
	// get all the sprints under the current project
	var sprintsCursor = Sprints.find({}); 
	// get current time to check whether sprints are expired
	var currentTime = new Date(); 
	currentTime.setHours(0,0,0,0); 

	// iterate through each sprint to check if expired
	sprintsCursor.forEach(function(sprint) { 
		// check sprint end date against current time
		var hasExpired = sprint.sprintEndDate < currentTime; 
		// update sprints "sprintIsActive" field
		Meteor.call("sprintUpdateStatus", sprint._id, !hasExpired, 
			function(error, result) {
				if (error) {
					console.log("sprint's 'isActive' status is not updated properly."); 
				}
			}
		); 
	}); 
}; 


Template.allSprints.helpers({
	projectId: function() { 
		return Router.current().params._id; 
	}, 
	
	// for displaying name on top of page
	projectName: function() {
		var project = Projects.find(); 
		return this.projectName; 
	},

	// return list of sprints that are active
	activeSprintsList: function() {
		return Sprints.find({sprintIsActive: true}); 
	}, 

	expiredSprintsList: function() {
		return Sprints.find({sprintIsActive: false}); 
	},

	// return a list of tasks assigned to this sprint
	sprintTasks: function(sprintId) {
		check(sprintId, String); 
		var output = Tasks.find({taskSprintId: sprintId}); 
		return output;
	}, 

	// for displaying sprint dates in the correct format
	sprintDate: function(date) {
		check(date, Date); 
		//Parse date in UTC format 
		return moment.utc(date).format("MMMM Do, YYYY");
	}
}); 

Template.allSprints.events({
	// route the app to the Create New Sprint page upon click
	"click .create-sprint": function(e, t) {
		var projectId = Router.current().params._id; 
		Router.go("createNewSprint", {_id: projectId});
	},

	//callback function when the user clicks delete button
	"click .delete-sprint-btn": function(e, t) {
		// create pop-up window with warning
		var result = confirm("Are you sure you want to delete this sprint?"); 
		// if user confirms on sprint deletion
		if (result) {
			// first removes all tasks currently under the sprint (update tasks" attributes)
			Meteor.call("removeTasksFromSprint", this._id, function(error, result) {
				if (error) {
					return throwError(error.reason); 
				}
			}); 
			// then delete the sprint from the database
			Meteor.call("sprintDelete", this._id, function(error,result) {
				if (error) {
					return throwError(error.reason); 
				} 
			});
			var i; 
			
		}
	}
})