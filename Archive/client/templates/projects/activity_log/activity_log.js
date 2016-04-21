// activity log template: 

// session variables are reactive--they update based on the user actions and
// change based on the events below.
Session.setDefault("currentActionsListed", null);
Session.setDefault("fullLog", null);
Session.setDefault("filtering", 0);


Template.activityLog.helpers({
	// this displays the individal items in the log, returns an array
	logItems: function() {
		if (Session.get("currentActionsListed") == null) {
			var logArray = this.log;
			logArray = _.map(logArray, function(action) {
				var timestamp = action.submitted;
				var formattedSubmitDate = timestamp.getMonth() + "/" + timestamp.getDay() + "/" + timestamp.getFullYear() 
					+ " " + timestamp.toLocaleTimeString();
				var stringOfTags = action.tag;
				action.tagArray = stringOfTags.split(" ");
				action.submitted = formattedSubmitDate;
				return action;
			});
			logArray = logArray.reverse();
			Session.set("fullLog", logArray);
			Session.set("currentActionsListed", logArray);
		}
		return Session.get("currentActionsListed");
	},

	// if currently filtering, it will return true.
	filtering: function() {
		return (Session.get("filtering") != 0);
	},

	// be able to only view your own activities--if this is true,
	// the button is displayed (because this implies that we are not already
	// using this filter)
	notMyActivitiesView: function() {
		return (Session.get("filtering") != 2);
	}
});

Template.activityLog.events({
	// once a tag has been clicked, filter based on it.
	"click .tag": function(e, t) {
		e.preventDefault();
		var classToFilterBy = e.target.className;
		var fullLog = Session.get("fullLog");
		var filteredLog = _.filter(fullLog, function(action) {
			var stringOfTags = action.tag;
			return (stringOfTags.indexOf(classToFilterBy) != -1);
		});
		Session.set("filtering", 1);
		Session.set("currentActionsListed", filteredLog);
	},

	// if currently in a filtered view, can click this to return 
	// to the default log view.
	"click .default-log": function(e, t) {
		e.preventDefault();
		var fullLog = Session.get("fullLog");
		Session.set("filtering", 0);
		Session.set("currentActionsListed", fullLog);
	},

	// go to the page corresponding to the activity if possible.
	"click .description-link": function(e, t) {
		e.preventDefault();
		var url = e.target.id;
		Router.go("/" + url);
	},

	// this filters it so that only your activities are shown. 
	"click .my-activities": function(e, t) {
		e.preventDefault();
		var userToFilterBy = Meteor.user().username;
		var fullLog = Session.get("fullLog");
		var filteredLog = _.filter(fullLog, function(action) {
			return (action.user == userToFilterBy);
		});
		Session.set("filtering", 2);

		Session.set("currentActionsListed", filteredLog);
	}
});