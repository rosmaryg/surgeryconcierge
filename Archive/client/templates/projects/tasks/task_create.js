Template.createNewTask.events({
    // Create of new task
    "submit form": function(event){
      event.preventDefault();
      // the menu object in the html form
      var sprintsMenu = event.target.taskSprint; 
      // get the sprint number from the item selected in the sprints menu 
      var selectedSprintNumber = sprintsMenu.options[sprintsMenu.selectedIndex].value; 
      
      var task = {
    		projectName: this.name,
		    projectID: this._id,
        taskOwner: Meteor.user().username,
    		taskName: event.target.taskName.value,
    		taskDescription: event.target.taskDescription.value,
    		taskDifficulty: parseInt(event.target.taskDifficulty.value),
    		taskLength: event.target.taskLength.value,
		    taskSprintNumber: selectedSprintNumber,
		    taskStatus: "To Do",
		    taskNotes: []
    	};

      Meteor.call("taskInsert", task, function(error, result) {
          // display the error to the user and abort
          if (error) {
            return throwError(error.reason);
          } else {
            // if the user assigns the task to an existing sprint
            if (selectedSprintNumber != "Unassigned") {
              // getting sprintId based on the selected item in the dropdown menu
              var sprintId = sprintsMenu.options[sprintsMenu.selectedIndex].id; 
              // add the task to the sprint by updating attributes in the task
              Meteor.call("taskAddToSprint", result._id, sprintId, function(error, result) {
                  if(error) {
                    return throwError(error.reason); 
                  }
                }
              ); 
            } 
            // route to task view page
	          Router.go("taskView", {project: Router.current().params._id, _id: result._id});
          }

        });
    }
    
});

Template.createNewTask.helpers({
  // find all active sprints in the project
  activeSprints: function() {
    return Sprints.find({projectId: Router.current().params._id, sprintIsActive: true}); 
  }
}); 

