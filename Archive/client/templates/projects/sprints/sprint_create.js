Template.createNewSprint.helpers({
  // get the current project id 
  "projectId": function() {
    return Router.current().params._id; 
  }, 
  "projectName": function() {
    var project = Projects.findOne(Router.current().params._id); 
    return project.name; 
  }
}); 

Template.createNewSprint.events({
    // Create of new sprint
    "submit form": function(event){
      event.preventDefault();
      var routeProjectId = Router.current().params._id; 
      var inputStartDate = event.target.startDate.value; 
      var inputEndDate = event.target.endDate.value; 
      var startDate = new Date(inputStartDate);
      var endDate = new Date(inputEndDate); 
      
      // adjust dates for timezone difference
      startDate.setHours(startDate.getHours() + 4); 
      endDate.setHours(endDate.getHours() + 4); 

      // create new object based on user inputs
      var sprint = {
        projectId: routeProjectId,
        sprintDescription: event.target.description.value,       
        sprintStartDate: startDate,
        sprintEndDate: endDate
      }; 
      // inserting new sprint into the database collection
      Meteor.call("sprintInsert", sprint, function(error, result) {
          // display the error to the user and abort
          if (error) {
            console.log("error with new sprint creation."); 
            return throwError(error.reason);
          } 
          else {
            // reroute the app back to Sprints page
            Router.go("allSprints", {_id: routeProjectId});
          }
        });
    }
    
  });

