Template.notifications.helpers({
  notifications: function() {
    return Notifications.find({sendToUsers: {$in: [Meteor.userId()]}, read: false, deleted: false}, {sort: {timestamp: -1}, limit: 5});
  },

  notificationCount: function() {
    return Notifications.find({sendToUsers: {$in: [Meteor.userId()]}, read: false, deleted: false}).count();
  },

  isManager: function() {
    return Projects.find({manager: Meteor.user().username}).fetch();
  }
});

Template.notifications.events({
  "click .notification.dropdown-menu": function(e) {
    e.stopPropagation();
  }
});

Template.notificationItem.helpers({
  notificationPostPath: function() {
    typeArray = this.type.split(" ");
    if (typeArray[0] == "task") {
      if ((typeArray[1] == "creation") || (typeArray[1] == "deletion" && 
        typeArray.length > 2 && typeArray[2] == "pending") 
        || (typeArray[1] == "comment") || (typeArray[1] == "completion")) {
        return Router.routes.taskView.path({_id: this.taskId, project: this.projectId});
      }
    } else if (typeArray[0] == "post") {
      if (typeArray[1] == "new" || typeArray[1] == "comment") {
        return Router.routes.postPage.path({_id: this.postId});
      }
    
    }
  },

  taskUpdate: function() {
    var typeArray = this.type.split(" ");
    return (typeArray[0] == "task");
  },

  postUpdate: function() {
    var typeArray = this.type.split(" ");
    return (typeArray[0] == "post");
  },

  notificationMessage: function() {
    var typeArray = this.type.split(" ");
    if (typeArray[0] == "task") {
      if (typeArray[1] == "creation") {
        var message = this.actionByUser + " created task ";
        return message;
      } else if (typeArray[1] == "deletion") {
        if (typeArray.length > 2) {
          if (typeArray[2] == "pending") {
            var message = "pending deletion for " + this.actionByUser + "'s task ";
          } else {
            var message = "deletion request was rejected for ";
          }
        } else {
          var message = this.actionByUser + " deleted task ";
        }
        return message;
      } else if (typeArray[1] == "comment") {
        var message = this.actionByUser + " commented on task ";
        return message;
      } else if (typeArray[1] == "completion") {
        if (typeArray.length > 2) {
          if (typeArray[2] == "pending") {
            var message = "pending completion for " + this.actionByUser + "'s task ";
          } else {
            var message = "completion request was rejected for ";
          }
        } else {
          var message = this.actionByUser + " approved your completed task ";
        }
        return message;
      }
    } else if (typeArray[0] == "post") {
      var message;
      if (typeArray[1] == "new") {
        message = "posted in " + this.projectName + ": ";
      } else if (typeArray[1] == "comment") {
        message = "commented on your post "
      }
      return message;
    }

  }
});

Template.notificationItem.events({
  "click .notification-message": function(e) {
    Notifications.update(this._id, {$set: {read: true, deleted: true}});
  },

  "click .ack-notification": function(e) {
    e.preventDefault();
    e.stopPropagation();
    Notifications.update(this._id, {$set: {read: true}});
  },

  "click .del-notification": function(e) {
    e.preventDefault();
    e.stopPropagation();
    Notifications.update(this._id, {$set: {read: true, deleted: true}});
  }

})