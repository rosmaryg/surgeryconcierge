Template.taskView.helpers({
	printDueDate: function() {
		var projectId = Router.current().params.project; 
		var task = Tasks.findOne({projectID: projectId}); 
		if (task.taskDueDate == null) {
			return "Unassigned"; 
		} else {
			return moment.utc(task.taskDueDate).format("MMMM Do, YYYY"); 
		}
	},

	printStartDate: function() {
		var projectId = Router.current().params.project; 
		var task = Tasks.findOne({projectID: projectId}); 
		if (task.taskStartDate == null) {
			return "Unassigned"; 
		} else {
			return moment.utc(task.taskStartDate).format('MMMM Do, YYYY'); 
		}
	},

	pendingDeletionByManager: function() {
		var projectCorrespToTask = Projects.findOne({_id: this.projectID});
		return (Meteor.user().username === projectCorrespToTask.manager && this.status == -1);
	},

	pendingCompletionByManager: function() {
		var projectCorrespToTask = Projects.findOne({_id: this.projectID});
		return (Meteor.user().username === projectCorrespToTask.manager && this.status == 1);
	}
}); 

Template.taskView.events({
    // Reroute when click on edit task
    "click .edit-task": function() {
    	var projectId = Router.current().params.project; 
		Router.go("editTask", {_id: this._id, project: projectId}); 
	},
	// Delete task and reroute
	"click .delete-task": function(e, t) {
		e.preventDefault();
		var project = Router.current().params.project;
		var projectCorrespToTask = Projects.findOne({_id: project});
		if (projectCorrespToTask) {
			if (Meteor.user().username === projectCorrespToTask.manager) {
				var x = confirm("Are you sure you want to permanantly delete this task?");
                		if(x) {
                        		Meteor.call("taskDelete", this._id);
					Router.go("projectView", {_id: project});}
			} else if (Meteor.user().username === this.taskCreator) {
				var x = confirm("Are you sure you want to pend deletion from the project manager for this task?");
                		if(x) {
					Meteor.call("updateTaskPendingDeletion", this._id);}
			} else {
				throwError("You cannot delete another user's task.");
			}
	}},

	"click .complete-task": function(e, t) {
		console.log(this._id);
		Meteor.call("taskCompleteApprove", this._id, function(error, id) {
			if (error) {
				return throwError(error.reason);
			}
		});
	},

	"click .mark-resolved-del": function(e, t) {
		console.log(this._id);
		Meteor.call("taskDeleteReject", this._id, function(error, id) {
			if (error) {
				return throwError(error.reason);
			}
		});
	},

	"click .mark-resolved-compl": function(e, t) {
		Meteor.call("taskCompleteReject", this._id, function(err, id) {
			if (error) {
				return throwError(error.reason);
			}
		});
	},
    // Move task, to be completed
	"change .moveDropDown": function(e, t) {
		Session.set("nextMoveOption", e.target.selectedOptions[0].label);
	},
    // Add Note, to be completed
	"submit form": function(e, t){
		if(e.target.id == "moveForm")
		{
			var option2 = Session.get("nextMoveOption");
			Session.set("currentMoveOption", option2);

			var task = this;
			var newStatus = option2;
			var projInfo = Projects.findOne({_id: this.projectID}, {fields: {manager: 1}});
			var isManager = Meteor.user().username === projInfo.manager;
			if(newStatus == "Completed")
			{
				if (isManager) {
					Meteor.call("taskCompleteApprove", this._id, function(error, id) {
						if (error) {
							return throwError(error.reason);
						}
					});
				} else {
					Meteor.call("updateTaskPendingCompletion", this._id, function(error, id) {
						if (error) {
							return throwError(error.reason);
						}
					});
				}
			} else {
				Tasks.update({_id: task._id}, {$set: {taskStatus: newStatus}});
			}
		}
		else
		{
			var now = new Date();
			var inputtedNote = e.target.taskNoteInput.value;
			inputtedNote += " \n -Posted by "
			inputtedNote += Meteor.user().username;
			inputtedNote += " at "
			inputtedNote += moment(now).format("LLLL");
			var msgForLog = Meteor.user().username + " added a note to task " + t.data.taskName;
			Meteor.call("taskAddNote", this._id, t.data.projectID, 
					inputtedNote, msgForLog, function(error, result) {
					if (error) {
						return throwError(error.reason);
					} else {
					}
				}
			);
			Router.go("taskView", {"_id": t.data._id, "project": t.data.projectID});
		}
	}
});

