// sessions are used to track the reactive variables for the pending deletion table.
Session.setDefault("deletionChecked", false); // see if any items are checked in the deletion table
Session.setDefault("completionChecked", false);
Session.setDefault("rejectOrApproveDeletions", 0); // reject or approve selected deletions
Session.setDefault("rejectOrApproveDeletionsCompletions", 0);

Template.allNotifications.helpers({

	singleProject: function() {
		return Projects.find({manager: Meteor.user().username}).fetch();
	},

	created: function() { // find only notifications related to task creation
		return Notifications.find({type: "task creation", projectId: this._id}).fetch();
	},

	deleted: function() { 
		return Notifications.find({type: "task deletion pending", projectId: this._id}).fetch();
	},

	completed: function() {
		return Notifications.find({type: "task completion pending", projectId: this._id}).fetch();
	},

	notificationsPresent: function() { // see if there are notifications from any of these categories.
		var hasCreatedNotifications = Notifications.find({type: "task creation", projectId: this._id}).fetch();
		var createdNotifsExist = hasCreatedNotifications.length > 0;
		var hasDeletedNotifications = Notifications.find({type: "task deletion pending", projectId: this._id}).fetch();
		var deletedNotifsExist = hasDeletedNotifications.length > 0;
		var hasCompletedNotifications = Notifications.find({type: "task completion pending", projectId: this._id}).fetch()
		var completedNotifsExist = hasCompletedNotifications.length > 0;
		return createdNotifsExist || deletedNotifsExist || completedNotifsExist;
	},

	// link to the specific path--since these tags are all made on the back-end
	// no need to error check.
	notificationPostPath: function() {
	    typeArray = this.type.split(" ");
	    if (typeArray[0] == "task") {
	      if ((typeArray[1] == "creation") || (typeArray[1] == "deletion" && typeArray.length > 2) 
	        || (typeArray[1] == "comment")) {
	        return Router.routes.taskView.path({_id: this.taskId, project: this.projectId});
	      }
	    } else if (typeArray[0] == "post") {
	      if (typeArray[1] == "new" || typeArray[1] == "comment") {
	        return Router.routes.postPage.path({_id: this.postId});
	      }
	    
	    }
  	},

  	deleteOptionButton: function() {
  		return (Session.get("deletionChecked"));
  	},

  	completeOptionButton: function() {
  		return (Session.get("completionChecked"));
  	},

  	approveOrRejectDeletions: function() {
  		return (Session.get("rejectOrApproveDeletions") == 1 || Session.get("rejectOrApproveDeletions") == -1);
  	},

  	approveOrRejectCompletions: function() {
  		return (Session.get("rejectOrApproveCompletions") == 1 || Session.get("rejectOrApproveCompletions") == -1);
  	}
});

Template.allNotifications.rendered = function() {
	$(".categories").each(function() {
		$(this).slideUp();
	});
}

Template.allNotifications.events({
	"click .project": function(e, t) {
		$(e.target).find("i").toggleClass("fa-plus-square-o fa-minus-square-o");
		
		$(".categories").not($(e.target).next()).each(function() {
			$(this).slideUp();
		});
		
		$(e.target).next().animate({
			height: "toggle",
      		opacity: "toggle",
		});

	},

	// change css based on whether you select "reject" or "approve" requests
	"click .select-req-del": function(e, t) {
		e.preventDefault();
		e.stopPropagation();
		$(".select-req").not($(e.target)).each(function() {
			$(this).removeClass("btn-warning");
			$(this).addClass("btn-default");
		});
		if ($(e.target).hasClass("btn-warning")) {
			$(e.target).removeClass("btn-warning");
			$(e.target).addClass("btn-default");
			Session.set("rejectOrApproveDeletions", 0);
		} else {
			$(e.target).removeClass("btn-default");
			$(e.target).addClass("btn-warning");
			var acceptOrReject = e.target.id;
			if (acceptOrReject === "select-req-approve") {
				Session.set("rejectOrApproveDeletions", 1);
			} else {
				Session.set("rejectOrApproveDeletions", -1);
			}
		}

	},

	"click .select-req-compl": function(e, t) {
		e.preventDefault();
		e.stopPropagation();
		$(".select-req").not($(e.target)).each(function() {
			$(this).removeClass("btn-warning");
			$(this).addClass("btn-default");
		});
		if ($(e.target).hasClass("btn-warning")) {
			$(e.target).removeClass("btn-warning");
			$(e.target).addClass("btn-default");
			Session.set("rejectOrApproveCompletions", 0);
		} else {
			$(e.target).removeClass("btn-default");
			$(e.target).addClass("btn-warning");
			var acceptOrReject = e.target.id;
			if (acceptOrReject === "select-req-approve") {
				Session.set("rejectOrApproveCompletions", 1);
			} else {
				Session.set("rejectOrApproveCompletions", -1);
			}
		}

	},

	"click .select-all-del": function(e, t) {
		e.stopPropagation();
		if ($(e.target)[0].checked) { // check select status
            $(".single-check-del").each(function() { //loop through each checkbox
                this.checked = true;  // select all checkboxes         
                Session.set("deletionChecked", true);       
            });
        } else {
            $(".single-check-del").each(function() { //loop through each checkbox
                this.checked = false; // deselect all checkboxes
                Session.set("deletionChecked", false);                        
            });         
        }

	},

	"click .single-check-del": function(e, t) {
		e.stopPropagation();
		if ($(e.target)[0].checked) {

			Session.set("deletionChecked", true);
		} else {
			Session.set("deletionChecked", false);
		}
	},

	"click .mark-read": function(e, t) {
		e.preventDefault();
		e.stopPropagation();
		var createdNotifs = Notifications.find({type: "task creation", projectId: this._id}).fetch();
		_.each(createdNotifs, function(notif) {
			Notifications.update(notif._id, {$set: {read: true, deleted: true}});
		});
	},

	"click .single-check-compl": function(e, t) {
		e.stopPropagation();
		if ($(e.target)[0].checked) {

			Session.set("completionChecked", true);
		} else {
			Session.set("completionChecked", false);
		}
	},

	"click .select-all-compl": function(e, t) {
		e.stopPropagation();
		if ($(e.target)[0].checked) { // check select status
            $(".single-check-compl").each(function() { //loop through each checkbox
                this.checked = true;  // select all checkboxes         
                Session.set("completionChecked", true);       
            });
        } else {
            $(".single-check-compl").each(function() { //loop through each checkbox
                this.checked = false; // deselect all checkboxes
                Session.set("completionChecked", false);                        
            });         
        }

	},

	"click .notification-message": function(e, t) {
		Notifications.update(this._id, {$set: {read: true}});
	},

	"click .notif-read": function(e, t) {
	    e.preventDefault();
	    e.stopPropagation();
	    Notifications.update(this._id, {$set: {read: true, deleted: true}});
	},

	"click .delete-req-update": function(e, t) {
		e.preventDefault();
		e.stopPropagation();
		var approveStatus = Session.get("rejectOrApproveDeletions") == 1;
		if (approveStatus) {
			$(".single-check-del").each(function() { //loop through each checkbox
				Meteor.call("taskDelete", this.id, function(error, id) {
                	if (error) {
                		return throwError(error.reason);
                	} else {
						
                	}
                });
				Notifications.update(this.value, {$set: {read: true, deleted: true}});
            });
		} else {
			$(".single-check-del").each(function() { //loop through each checkbox
				Meteor.call("taskDeleteReject", this.id, function(error, id) {
                	if (error) {
                		return throwError(error.reason);
                	} else {
                	}
                });
				Notifications.update(this.value, {$set: {read: true, deleted: true}});
            });
		}
		Session.set("rejectOrApproveDeletions", 0);
	},

	"click .complete-req-update": function(e, t) {
		e.preventDefault();
		e.stopPropagation();
		var approveStatus = Session.get("rejectOrApproveCompletions") == 1;
		if (approveStatus) {
			$(".single-check-compl").each(function() { //loop through each checkbox
				Meteor.call("taskCompleteApprove", this.id, function(error, id) {
                	if (error) {
                		return throwError(error.reason);
                	} else {
						
                	}
                });
				Notifications.update(this.value, {$set: {read: true, deleted: true}});
            });
		} else {
			$(".single-check-compl").each(function() { //loop through each checkbox
				Meteor.call("taskCompleteReject", this.id, function(error, id) {
                	if (error) {
                		return throwError(error.reason);
                	} else {
                	}
                });
				Notifications.update(this.value, {$set: {read: true, deleted: true}});
            });
		}
		Session.set("rejectOrApproveCompletions", 0);
	}
})