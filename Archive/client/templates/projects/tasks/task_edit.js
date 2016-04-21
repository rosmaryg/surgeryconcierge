Template.editTask.events({
    // Form submission handler
    "submit form": function(event){
      event.preventDefault();
      var sprintsMenu = event.target.taskSprint; 
      var selectedSprintNumber = sprintsMenu.options[sprintsMenu.selectedIndex].value; 
      // Populate task
      var task = {
    		projectName: this.projectName,
		    projectID: this.projectID,
		    taskOwner: this.taskOwner,
    		taskName: event.target.taskName.value,
    		taskDescription: event.target.taskDescription.value,
    		taskDifficulty: parseInt(event.target.taskDifficulty.value),
    		taskLength: event.target.taskLength.value,
		    taskSprintNumber: selectedSprintNumber,
		    taskStatus: this.taskStatus,
		    taskNotes: this.taskNotes
    	}; 
		// Get rid of old task with id, create a new one
  	  Meteor.call("taskDelete", this._id);
  	  Meteor.call("taskInsert", task, function(error, result) {
          // display the error to the user and abort
          if (error) {
            return throwError(error.reason);
          } else {
            // if the user assigns the task to an existing sprint
            if(selectedSprintNumber!="Unassigned") {
              var sprintId = sprintsMenu.options[sprintsMenu.selectedIndex].id; 
              // add the task to the sprint by updating task attributes in database
              Meteor.call("taskAddToSprint", result._id, sprintId, function(error, result) {
                  if(error) {
                    return throwError(error.reason); 
                  }
                }
              ); 
              
            } else {

            }
      	    Router.go("taskView", {_id:result._id, project: Router.current().params.project});
          }
      });
    }
    
});

Template.editTask.helpers({
  activeSprints: function() {
    return Sprints.find({projectId: Router.current().params.project, sprintIsActive: true}); 
  }
}); 

