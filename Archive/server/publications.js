// publications are tied to the router--so they selectively
// publish certain parts of the database, and then a template
// can "subscribe" to these publications to get this data

// filters for projects a user is associated with
Meteor.publish("userCreatedProjects", function() {
  if (this.userId) {
    var username = Meteor.users.findOne({_id: this.userId}, {fields: {"username": 1}}).username;
    return Projects.find({createdBy: username});
  } else {
    this.ready(); 
  }
});

Meteor.publish("userManagedProjects", function() {
  if (this.userId) {
    var username = Meteor.users.findOne({_id: this.userId}, {fields: {"username": 1}}).username;
    return Projects.find({manager: username});
  } else {
    this.ready();
  }
});

Meteor.publish("userJoinedProjects", function() {
  if (this.userId) {
    var username = Meteor.users.findOne({_id: this.userId}, {fields: {"username": 1}}).username;
    return Projects.find({users: { $in: [username]}});
  } else {
    this.ready(); 
  }
});

// publishing project related information
Meteor.publish("projects", function() {
  return Projects.find({});
});

Meteor.publish("projectLog", function(projectId) {
  check(projectId, String);
  return Logs.find({projectId: projectId});
});

Meteor.publish("singleProject", function(id) {
  check(id, String);
  return Projects.find(id);
});

Meteor.publish("tasks", function() {
  return Tasks.find({});
});

Meteor.publish("singleTask", function(taskId) {
  check(taskId, String);
  return Tasks.find({_id: taskId});
});

Meteor.publish("taskInProject", function(projectId) {
  check(projectId, String); 
  return Tasks.find({projectID: projectId}); 
}); 

Meteor.publish("sprintsInProject", function(projectId) {
  check(projectId, String); 
  return Sprints.find({projectId: projectId}); 
}); 

Meteor.publish("sprints", function() {
    return Sprints.find({});
});

// notifications
Meteor.publish("ownNotificationsUnread", function() {
  return Notifications.find({sendToUsers: {$in: [this.userId]}, read: false});
});

Meteor.publish("ownNotificationsUndeleted", function() {
  return Notifications.find({sendToUsers: {$in: [this.userId]}, deleted: false});
});

Meteor.publish("allPosts", function() {
    return Posts.find({});
});

Meteor.publish("posts", function(options) {
  check(options, {
    sort: Object,
    limit: Number
  });
  return Posts.find({}, options);
});

Meteor.publish("singlePost", function(id) {
  check(id, String);
  return Posts.find(id);
});

Meteor.publish("comments", function(postId) {
  check(postId, String);
  return Comments.find({postId: postId});
});

Meteor.publish("allUsers", function () {
    return Meteor.users.find({}, {fields: {"username": 1}});
});
