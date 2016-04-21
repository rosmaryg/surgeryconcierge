// Initialize a projectSubmitErrors hash
Template.projectSubmit.created = function() {
  Session.set("projectSubmitErrors", {});
}
// Hanlders for submitting a project
Template.projectSubmit.helpers({
    hideCompleted: function() {
        return Session.get("hideCompleted");
    },
    incompleteCount: function() {
        return Projects.find({checked: {$ne: true}}).count();
    },
    errorMessage: function(field) {
        return Session.get("projectSubmitErrors")[field];
    },
    errorClass: function (field) {
        return !!Session.get("projectSubmitErrors")[field] ? "has-error" : "";
    }
});

Template.projectSubmit.events({
   "change .hide-completed input": function(event) {
        Session.set("hideCompleted", event.target.checked);
    },
    "submit form": function(e) {
         // Sample Spring Insertion
        var sprintName = $(e.target).find("[name=project-name]").val();
        if (sprintName === "overDue") {
            var sprint = {
                sprintNumber: 1,
                projectName: sprintName,
                projectId: "test1",
                sprintDescription: "Over due sprint!",
                sprintStartDate: new Date("April 20, 2015"),
                sprintEndDate: new Date("April 21, 2015"),
                sprintIsActive: true
            };
            Meteor.call("sprintInsert", sprint, function(error, result) {
                // display the error to the user and abort
                if (error) {
                    return throwError(error.reason);
                }                 
                });
        }
        else if (sprintName === "almostDue") {
            var sprint = {
                sprintNumber: 2,
                projectName: sprintName,
                projectId: "test2",
                sprintDescription: "Almost due sprint!",
                sprintStartDate: new Date("April 20, 2015"),
                sprintEndDate: new Date("April 22, 2015"),
                sprintIsActive: true
            };
            Meteor.call("sprintInsert", sprint, function(error, result) {
                // display the error to the user and abort
                if (error) {
                    return throwError(error.reason);
                }                 
                });
        }
        
        e.preventDefault();
        
        var project = {
          name: $(e.target).find("[name=project-name]").val(),
          users: [Meteor.user().username]
        };
        var errors = validateProject(project);
        if (errors.name)
          return Session.set("projectSubmitErrors", errors);
        
        // later on, might want to change the created by and manager to a name instead of username
        projectAttr = _.extend(project, {
          checked:false,
          createdBy: Meteor.user().username,
          manager: Meteor.user().username,
          createdDate: new Date()
        });


  /*
  // Add sample task to project
    var sample = {
  projectName: $(e.target).find("[name=project-name]").val(),
  taskName: "Sample User Story",
  taskDescription: "This is a sample user story. Here you will write the actual user story for this specific task",
  taskDifficulty: 555,
  taskLength: "20 hours",
  taskSprint: "Unassigned",
  taskDueDate: new Date(45,12,12,0,0,0,0),
  taskOwner: "He who shall not be named",
  taskStatus: "To Do",
  }; 
  Meteor.call("taskInsert", sample);
    var sample2 = {
  projectName: $(e.target).find("[name=project-name]").val(),
  taskName: "Ample User Story",
  taskDescription: "This is a sample user story. Here you will write the actual user story for this specific task",
  taskDifficulty: 444,
  taskLength: "20 hours",
  taskSprint: "Unassigned",
  taskDueDate: new Date(45,12,12,0,0,0,0),
  taskOwner: "He who shall not be named",
  taskStatus: "To Do",
  }; 
  Meteor.call("taskInsert", sample2);
    var sample3 = {
  projectName: $(e.target).find("[name=project-name]").val(),
  taskName: "Maple User Story",
  taskDescription: "This is a sample user story. Here you will write the actual user story for this specific task",
  taskDifficulty: 999,
  taskLength: "20 hours",
  taskSprint: "Unassigned",
  taskDueDate: new Date(45,12,12,0,0,0,0),
  taskOwner: "He who shall not be named",
  taskStatus: "To Do",
  }; 
  Meteor.call("taskInsert", sample3);
  */
    

        Meteor.call("projectInsert", project, function(error, result) {
          // display the error to the user and abort
          if (error) {
            return throwError(error.reason);
          } else {

            Router.go("projectView", {_id: result._id});  
          }
          // show this result but route anyway
          /*
          if (result.projectExists) {
            throwError("This project has already been created");
          }
          */
        });
    }
    
});
