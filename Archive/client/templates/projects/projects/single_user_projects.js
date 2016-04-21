// Event handling for when user clicks a done check box
Template.singleProjectStub.events({
    // Switch states between checked / not checked
    "click .toggle-checked": function() {
        Meteor.call("projectHide", this._id, {$set: {checked: ! this.checked}});
    }
});

// Event handling for when to display a red/yellow !
Template.singleProjectStub.helpers({
    // red exclamation pt check
    late: function() {
      var name = $(this)[0].name;
      var project = Projects.findOne({name: name});
      var currSprint = Sprints.find({projectId: project._id, sprintIsActive: true}).fetch();
      var possLate = false;
      _.each(currSprint, function(curr) {
            var endDate = curr.sprintEndDate;
            var timeDiff = (new Date() - endDate)/(1000*60*60*24);
            if(timeDiff >= 0) {
                possLate = true;
            }
      }); 
      return possLate;  
    },
    // yellow exclamation pt check
    upcoming: function() {
      var name = $(this)[0].name;
      var project = Projects.findOne({name: name});
      var currSprint = Sprints.find({projectId: project._id, sprintIsActive: true}).fetch();
      var possUpcoming = false;
      _.each(currSprint, function(curr) {
            var endDate = curr.sprintEndDate;
            var timeDiff = (endDate - new Date())/(1000*60*60*24);
            if(timeDiff < 1 && timeDiff > 0) {
                possUpcoming = true;
            }
      });
      return possUpcoming;  
    },
});
Template.userProjectsList.helpers({
	// Displays list of projects user manages
    managed: function() {
      //if (this.userId) {
    		var username = Meteor.user().username;
            // If we enabled hide finished projts, only get the non-checked off projs
            if (Session.get("hideCompleted")) {
                return Projects.find( {checked: {$ne: true}, manager: username}, {sort: {createdDate: -1}} );
            }
            // Otherwise just return all projects we are managers of
            else {
                return Projects.find({manager:username}, {sort: {createdDate: -1}});
            }
      //}
    },
  
    // Displays list of projects user is a member of
  	member: function() {
    	//if (this.userId) {
      	var username = Meteor.user().username;
            var userInProjects;
            // If enabled hide finished projects, only get non-checked off projs
            if (Session.get("hideCompleted")) {
                userInProjects = Projects.find({users: { $in: [username]}, checked: {$ne: true}}, 
                    {sort: {createdDate: -1}}).fetch();
            }
            // Otherwise just return all projects we are members of
            else {
                userInProjects = Projects.find({users: { $in: [username]}}, {sort: {createdDate: -1}}).fetch();
            }
    		var filterOutManagedProjects = [];
    		_.each(userInProjects, function(project) {
    			if (project.manager != username) {
    				filterOutManagedProjects.push(project);
    			}
    		});
    		return filterOutManagedProjects;
    	//}
    }
});
