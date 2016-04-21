Notifications = new Mongo.Collection("notifications");

// only the user who is sent the notification can update the 
// read or delete statuses
Notifications.allow({
  update: function(userId, doc, fieldNames) {
    return ownsNotification(userId, doc) && 
      fieldNames.length < 3 && 
        (fieldNames.indexOf("read") != -1 || fieldNames.indexOf("deleted") != -1);
  }
});

// all notifications have these attributes.
notificationSkeleton = function() {
  var notificationSkeleton = {
    timestamp: new Date(),
    read: false,
    deleted: false
  }
  return notificationSkeleton;
};

// notifications include: creating a task, deleting a task, 
// commenting on a task. 
sendTaskNotification = function(task, type, actionByUser) {
  var project = Projects.findOne(task.projectID);
  var taskNotification = notificationSkeleton();
    
  _.extend(taskNotification, {
      type: "task " + type,
      actionByUser: actionByUser,
      taskId: task._id,
      taskName: task.taskName,
      projectName: task.projectName,
      projectId: task.projectID
    });
  // project manager must be notified if a task status changed by a generic user.
  if (project.manager !== actionByUser) {
    var projectManagerId = Meteor.users.findOne({username: project.manager})._id;
    _.extend(taskNotification, {
      sendToUsers: [projectManagerId]
    });
  // user who owns the task must be notified if a task status changed by the PM.
  } else {
    var genericUserId = Meteor.users.findOne({username: task.taskCreator})._id;
    if (task.taskCreator !== actionByUser) {
      _.extend(taskNotification, {
        sendToUsers: [genericUserId]
      });
    }
  }
  Notifications.insert(taskNotification);
};

// if the PM rejects the user"s request, the user is notified.
sendRejectNotification = function(taskDetails, type) {
  var taskCreator = taskDetails.taskCreator;
  var creatorUserId = Meteor.users.findOne({username: taskCreator})._id;
  
  var taskNotification = notificationSkeleton();
    
  _.extend(taskNotification, {
      type: "task " + type + " reject",
      actionByUser: Meteor.user().username,
      taskId: taskDetails._id,
      taskName: taskDetails.taskName,
      projectName: taskDetails.projectName,
      projectId: taskDetails.projectID,
      sendToUsers: [creatorUserId]
  });
  Notifications.insert(taskNotification);
};

// when someone makes a note on a task, the following parties are notified:
// the task owner, the PM, and anyone else who might have already posted a note
// on this task.
createTaskCommentNotification = function(taskId, commenter) {
  var taskDetails = Tasks.findOne({_id: taskId});
  var taskOwner = taskDetails.taskOwner,
      taskName = taskDetails.taskName,
      projectName = taskDetails.projectName,
      projectId = taskDetails.projectID;
  var project = Projects.findOne({_id: projectId}, {fields: {manager: 1}});
  var manager = project.manager;

  var notifyTheseUsers = [];

  var taskOwnerNotified = false;
  var managerNotified = false;

  var taskNotesArray = taskDetails.taskNotes;
  
  // go through the previous notes associated with the task
  _.each(taskNotesArray, function(note) {
    var eachCommentWord = note.split(" ");
    // find the last word in each note--this is the username.
    var username = eachCommentWord[eachCommentWord.length - 8];
    // if username isn"t the one who commented and the user isn"t already in the array
    if (commenter != username && notifyTheseUsers.indexOf(username) == -1) {
      var foundUserId = Meteor.users.findOne({username: username}, {fields: {username: 1}});
      notifyTheseUsers.push(foundUserId._id);
    }

    if (username == project.manager) {
      managerNotified = true;
    }

    if (username == taskOwner) {
      taskOwnerNotified = true;
    }

  });

  // if owner is not the commenter and has not previously commented.
  if (!taskOwnerNotified && taskOwner != commenter) {
    var ownerId = Meteor.users.findOne({username: taskOwner}, {fields: {username: 1}})._id;
    notifyTheseUsers.push(ownerId);
  }

  // if PM is not the commenter and has not previously commented.
  if (!managerNotified && manager != commenter) {
    var managerId = Meteor.users.findOne({username: manager}, {fields: {username: 1}})._id;
    notifyTheseUsers.push(managerId);
  }

  var taskCommentNotif = notificationSkeleton();
  _.extend(taskCommentNotif, {
    type: "task comment",
    sendToUsers: notifyTheseUsers,
    taskId: taskId,
    projectId: projectId,
    projectName: projectName,
    actionByUser: commenter
  });
  Notifications.insert(taskCommentNotif);
  
};

// when someone makes an announcement, every user in the group is notified.
createAnnouncementNotification = function(announcement) {
  var projectMembers = Projects.findOne({name: announcement.projectName}, {fields: {users: 1}}).users;
  projectMembers = _.without(projectMembers, _.findWhere(projectMembers, announcement.author));
  var memberIds = [];
  _.each(projectMembers, function(username) {
    var foundUser = Meteor.users.find({username: username}, {fields: {username: 1}}).fetch();
    if (foundUser.length > 0) {
      memberIds.push(foundUser[0]._id);
    }
  });
  if (memberIds.length > 0) {
    var announcementNotif = notificationSkeleton();
    _.extend(announcementNotif, {
      type: "post new",
      sendToUsers: memberIds,
      postId: announcement._id,
      postTitle: announcement.title,
      projectName: announcement.projectName,
      actionByUser: announcement.author
    });
    Notifications.insert(announcementNotif);
  } 
};

// if someone comments on an announcement, should be seen by the announcement creator.
createPostCommentNotification = function(comment) {
  var post = Posts.findOne(comment.postId);
  if (comment.userId !== post.userId) {
    var commentNotification = notificationSkeleton();
    _.extend(commentNotification, {
      type: "post comment",
      sendToUsers: [post.userId],
      postId: post._id,
      commentId: comment._id,
      actionByUser: comment.author
    });
    Notifications.insert(commentNotification);
  }
};



