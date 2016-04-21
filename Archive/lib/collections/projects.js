// collection to store all of the projects
Projects = new Mongo.Collection("projects");

// function to make sure that the one required field--
// the project name--is present
validateProject = function (post) {
  var errors = {};

  if (!post.name)
    errors.name = "Please name your project.";

  return errors;
};

// the EasySearch is the package we use to search for users
// in the projectView template.
EasySearch.createSearchIndex("searchUsers", {
  "collection": Meteor.users, // instanceof Meteor.Collection
  "field": ["username"], // array of fields to be searchable
  "limit": 100,
  "use" : "mongo-db",
  "convertNumbers": true,
  "props": {
    "filteredCategory": "All",
    "sortBy": "username"
  },
  "sort": function() {
    if (this.props.sortBy === "username") {
      return { "username": 1 };
    }  
  },

  "query": function(searchString, opts) {
    // Default query that will be used for the mongo-db selector
    var easySearcher = EasySearch.getSearcher(this.use);
    var query = easySearcher.defaultQuery(this, searchString);

    // filter for categories if set
    if (this.props.filteredCategory.toLowerCase() !== "all") {
      query.category = this.props.filteredCategory;
    }
    
    return query;
  }
});

// this is how the users actually show up below the search bar
// -- just reactive searching.
EasySearch.createSearchIndex("usersAutosuggest", {
  "collection": Meteor.users, 
  "use" : "mongo-db",
  "field": ["username"],
  "convertNumbers": true
});


if (Meteor.isServer) {
  Meteor.methods({
    projectDelete: function(projectName) {
      // check() function just makes sure that
      // what you"re inputting is type-safe
      check(this.userId, String);
      check(projectName, String);

      // remove the tasks related to this project.
      Tasks.remove({projectName: projectName});

      return Projects.remove({name : projectName});    
    },

    // Insert project after verifying well-formed input
    projectInsert: function(projectAttributes) {
      check(this.userId, String);
      check(projectAttributes, {
        checked: Boolean,
        createdBy: String,
        manager: String,
        name: String,
        createdDate: Date, 
        users: [Match.Any]
      });
      
      projectAttributes = _.extend(projectAttributes, {
        sprintCount: 0
      }); 

       // check for duplicate project--PROBLEM: currently case-sensitive.
      var projects = Projects.find({name: projectAttributes.name}, {sort: {createdDate: -1}}).fetch();
      if (projects.length > 0) {
        var timeToday = new Date();
        var mostRecentDuplicate = projects[0];
        var projDate = mostRecentDuplicate.createdDate;
        if (projDate.getYear() == timeToday.getYear() && projDate.getMonth() == timeToday.getMonth()) {
          throw new Meteor.Error("duplicate-project", "Project name has already been used this semester.");
          return {
              projectExists: true,
              _id: project._id
          };
        
        }
      }
      // Actual project insertion line 
      projectAttributes._id = Projects.insert(projectAttributes);

      // any time a project is created, a log is created as well.
      var projectLog  = {
        projectId: projectAttributes._id,
        projectName: projectAttributes.name,
        log: []
      }

      check(projectLog, {
        projectId: String,
        projectName: String,
        log: [Match.Any]
      });

      projectLog._id = Logs.insert(projectLog);

      var fstLogEntryDescription = projectAttributes.createdBy + " created project " + projectAttributes.name;
      // add your first log item
      Meteor.call("updateLog", projectAttributes._id, 
        {
          description: fstLogEntryDescription,
          color: "white",
          link: "",
          tag: "project create"
        });

      return { _id: projectAttributes._id,
              logId: projectLog._id };
    },
    // Used to hit project if a project is completed
    projectHide: function(projectId, checking) {
        check(this.userId, String);
        check(projectId, String);
        check(checking, Match.Any);
        return Projects.update(projectId, checking);
    },     

    projectAddUser: function(projectId, userId) {
      check(projectId, String);
      check(userId, String);
      // this is our permissions check to make sure the person adding a user is a PM. 
      var userIsManager = Projects.findOne({_id: projectId, manager: Meteor.user().username});
      if (userIsManager) {
        var logEntryDescription = Meteor.user().username + " added " + userId + "."; 
        Meteor.call("updateLog", projectId, 
          {
            description: logEntryDescription,
            color: "white",
            link: "",
            tag: "user add"
          });

        return Projects.update(projectId, {$addToSet: {users: userId}});
      } else {
        throw new Meteor.Error("project-permissions", "Only a project manager can add users.");
      }
    },

    projectRemoveUser: function(projectId, userId) {
      check(projectId, String);
      check(userId, String);
      var userIsManager = Projects.findOne({_id: projectId, manager: Meteor.user().username});
      if (userIsManager) {
        var logEntryDescription = Meteor.user().username + " removed " + userId + ".";
        Meteor.call("updateLog", projectId, 
          {
            description: logEntryDescription,
            color: "white",
            link: "",
            tag: "user remove"
          });
        return Projects.update({_id: projectId}, {$pull: {users: userId}});
      } else {
        throw new Meteor.Error("project-permissions", "Only a project manager can remove users.");  
      }
    }, 

    projectIncrementSprintCount: function(projectId) {
      check(projectId, String); 
      var project = Projects.findOne(projectId); 
      var count = project.sprintCount + 1; 
      return Projects.update({_id: projectId}, {$set: {sprintCount: count}}); 
    }

  });
}
