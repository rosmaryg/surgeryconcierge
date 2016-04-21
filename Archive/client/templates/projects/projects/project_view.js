Template.projectView.helpers({
	// Get user sort type, then return projects in sorted order
    taskList: function() {
		var name = Session.get('projectName');
		var sortOption = Session.get('currentSortOption');
		switch(sortOption)
		{
			case 0:
				return Tasks.find({projectName: name}, {sort: {normalizedName: 1}});
			case 1:
				return Tasks.find({projectName: name}, {sort: {normalizedName: -1}});
			case 2:
				return Tasks.find({projectName: name}, {sort: {taskDifficulty: 1}});
			case 3:
				return Tasks.find({projectName: name}, {sort: {taskDifficulty: -1}});
			case 4:
				return Tasks.find({projectName: name}, {sort: {taskDueDate: 1}});
			case 5: 
				return Tasks.find({projectName: name}, {sort: {taskDueDate: -1}});
			case 6:
				return Tasks.find({projectName: name}, {sort: {taskOwner: 1}});
			default:
				return Tasks.find({projectName: name}, {sort: {normalizedName: 1}});
		}
	},
	// for a PM, check if a task is pending deletion
	pendingDeletion: function() {
		return (this.status == -1);
	},
	// for a PM, check if a task is pending completion
	pendingCompletion: function() {
		return (this.status == 1);
	},
	// Returns tasks with project name, and 'Pending Completion' status
	viewPendingCompletion: function() {
		var manager = Projects.findOne({_id: Router.current().params._id}, {fields: {manager: 1}});
		return (Meteor.user().username === manager.manager || Meteor.user().username === this.taskOwner)
			&& this.status == 1;
	},
	// Returns tasks with project name, and 'Pending  Deletion' status
	viewPendingDeletion: function() {
		var manager = Projects.findOne({_id: Router.current().params._id}, {fields: {manager: 1}});
		return (Meteor.user().username === manager.manager || Meteor.user().username === this.taskOwner)
			&& this.status == -1;
	},

	//return all currently active sprints for this project WILL BE REMOVED
	activeSprintsList: function() {
		var name = Session.get('projectName');
		return Sprints.find({projectName: name, sprintIsActive: true}).fetch();
	},
    // Return task id associated with project name
	taskId: function(taskName) {
		check(taskName, String);
		return Tasks.findOne({projectName: taskName}).id;
	},
    // Returns tasks with project name, and 'To Do' status 
	toDoTasks: function() {
		var name = Session.get('projectName');
		return Tasks.find({projectName: name, taskStatus: 'To Do'}, {sort: {normalizedName: 1}});
	},
    // Returns tasks with project name, and 'In Progress' status
	inProgressTasks: function() {
		var name = Session.get('projectName');
		return Tasks.find({projectName: name, taskStatus: 'In Progress'}, {sort: {normalizedName: 1}});
	},
    // Returns tasks with project name, and 'Completed' status
	completedTasks: function() {
		var name = Session.get('projectName');
		return Tasks.find({projectName: name, taskStatus: 'Completed'}, {sort: {normalizedName: 1}});	
	},
	// Returns tasks with project name, and 'Pending' status
	pendingTasks: function() {
		var name = Session.get('projectName');
		return Tasks.find({projectName: name, taskStatus: {$in: ['Pending Completed', 'Pending Deletion']}}, {sort: {normalizedName: 1}});
	},
	// Returns whether the current user is the manager of the project
	isManager: function() {
		var manager = Projects.findOne({_id: Router.current().params._id}, {fields: {manager: 1}});
		return (Meteor.user().username === manager.manager);
	},

	notSelf: function() {
		return (this != Meteor.user().username);
	},

	hasTasks: function() {
		var tasksInProject = Tasks.find({projectID: Router.current().params._id}).fetch();
		return tasksInProject.length > 0; 
	}

});

Template.projectView.events({
	'click .project-user-add': function(e, t) {
		user = Meteor.users.find({_id: this._id}).fetch();
        // Call projectAddUser if we can find a valid username
        if (user.length > 0) {
			Meteor.call('projectAddUser', t.data._id, user[0]['username'], function(error, result) {
				if (error) {
					return throwError(error.reason);
				} else {
				}
			}); 
		}
        // Auto complete user names
		var instance = EasySearch.getComponentInstance(
		  { id : 'user-search-bar', index : 'searchUsers' }
		);

		instance.clear();
		$('#user-search-bar').val('');
	},
	
    // Handling for when user clicks to remove user from project
	'click .remove-user': function(e, t) {
		Meteor.call('projectRemoveUser', t.data._id, e.target.id, function(error, result) {
			if (error) {
				return throwError(error.reason);
			}
		});
	},
    // Handlers for drop down lists
	'change .sortDropDown': function(e, t) {
		Session.set('nextSortOption', e.target.options.selectedIndex);
	},
	'change .tasksDropDown': function(e, t) {
		Session.set('nextTaskOption', e.target.selectedOptions[0].label);
	},
	'change .moveDropDown': function(e, t) {
		Session.set('nextMoveOption', e.target.selectedOptions[0].label);
	},
    // Handler for when forms submitted
	'submit form': function(e, t) {
		e.preventDefault();
		if (e.target.id == 'moveForm')
		{
			if(Session.get('nextTaskOption') == undefined)
			{
				var option1 = e.target[1][0].label;
			}
			else
			{
				var option1 = Session.get('nextTaskOption');
			}
			if(Session.get('nextMoveOption') == undefined)
			{
				var option2 = e.target[2][0].label;
			}
			else
			{
				var option2 = Session.get('nextMoveOption');
			}
			Session.set('currentTaskOption', option1);
			Session.set('currentMoveOption', option2);

			var task = Tasks.findOne({taskName: option1});
			var newStatus = option2;
			var projInfo = Projects.findOne({_id: Router.current().params._id}, {fields: {manager: 1}});
			var isManager = Meteor.user().username === projInfo.manager;
		
			if (newStatus == 'Completed' && !isManager)
			{
				newStatus = 'Pending Completed';
				sendTaskNotification(task, 'deletion completion', Meteor.user().username);
					
			}
			Tasks.update({_id: task._id}, {$set: {taskStatus: newStatus}});
		}
		else
		{
			var option = Session.get('nextSortOption');
			Session.set('currentSortOption', option);
		}
	},
    // Drag handlers
	'dragstart .projectTasks': function(e, t) {
		Session.set('dragging', 1);
		Session.set('possibleDraggedTask', e.target.id);
	},

	'mousedown .projectTasks': function(e, t) {
		Session.set('possibleDraggedTask', e.target.id);
		Session.set('dragging', 1);
		//update categories' locations
		var cat1 = $('#cat1');
	    var cat2 = $('#cat2');
	    var cat3 = $('#cat3');
	    var cat4 = $('#cat4');

	    var offset = cat1.offset();
	    Session.set('cat1', offset.top);
	    offset = cat2.offset();
	    Session.set('cat2', offset.top);
	    offset = cat3.offset();
	    Session.set('cat3', offset.top);
	    offset = cat4.offset();
	    Session.set('cat4', offset.top);
	},

	'mouseup': function(e, t) {
		Session.set('dragEndX', e.originalEvent.clientX);
		Session.set('dragEndY', e.originalEvent.clientY);
		var name = Session.get('possibleDraggedTask');
		var pName = Session.get('projectName');
		var taskDetails = Tasks.findOne({taskName: name, projectName: pName});
		if (taskDetails) {
			var taskId = taskDetails._id;
			var projInfo = Projects.findOne({_id: Router.current().params._id}, {fields: {manager: 1}});
			var isManager = Meteor.user().username === projInfo.manager;
			if (Session.get('dragging') == 1)
			{
				if(e.originalEvent.clientY > Session.get('cat3') && e.originalEvent.clientY < Session.get('cat4'))
				{
					if (isManager) {
						Tasks.update({_id: taskId}, {$set: {taskStatus: 'Completed'}});
					} else {
						Meteor.call('updateTaskPendingCompletion', taskId, function(error, id) {
							if (error) {
								return throwError(error.reason);
							}
						});
					}
				}
				else if(e.originalEvent.clientY > Session.get('cat2') && e.originalEvent.clientY < Session.get('cat3'))
				{
					Tasks.update({_id: taskId}, {$set: {taskStatus: 'In Progress'}});
				}
				else if(e.originalEvent.clientY > Session.get('cat1') && e.originalEvent.clientY < Session.get('cat2'))
				{
					Tasks.update({_id: taskId}, {$set: {taskStatus: 'To Do'}});
				}
			}
			Session.set('dragging', 0);
		}
	},

	'dragend .projectTasks': function(e, t) {
		Session.set('dragging', 0);
		Session.set('dragEndX', e.originalEvent.clientX);
		Session.set('dragEndY', e.originalEvent.clientY);
		var name = Session.get('possibleDraggedTask');
		var pName = Session.get('projectName');
		var id = Tasks.findOne({taskName: name, projectName: pName})._id;
		if(Session.get('dragging') == 1)
		{
			if(e.originalEvent.clientY > Session.get('cat3') && e.originalEvent.clientY < Session.get('cat4'))
			{
				Tasks.update({_id: id}, {$set: {taskStatus: 'Completed'}});
			}
			else if(e.originalEvent.clientY > Session.get('cat2') && e.originalEvent.clientY < Session.get('cat3'))
			{
				Tasks.update({_id: id}, {$set: {taskStatus: 'In Progress'}});
			}
			else if(e.originalEvent.clientY > Session.get('cat1') && e.originalEvent.clientY < Session.get('cat2'))
			{
				Tasks.update({_id: id}, {$set: {taskStatus: 'To Do'}});
			}
		}
		Session.set('dragging', 0);
	},

	// quick delete handler
	'click .quick-delete':  function(e, t) {
		e.preventDefault();
		Meteor.call('taskDelete', this._id, function(error, id) {
			if (error) {
				return throwError(error.reason);
			} 
		});
	},
	// quick approve handler
	'click .quick-approve':  function(e, t) {
		e.preventDefault();
		Meteor.call('taskCompleteApprove', this._id, function(error, id) {
			if (error) {
				return throwError(error.reason);
			} 
		});
	},

    // handling for when user wants to create a new task
	'click .create-task': function(e, t) {
		Router.go('createNewTask', {_id: this._id});
	},
    // click handler for project logging
	'click .project-log-btn': function() {
		Session.set('currentActionsListed', null);
		Router.go('activityLog', {_id: this._id});
	}, 
	// click hanndler for viewing sprints
	'click .see-all-sprints': function() {
		Router.go('allSprints', {_id: this._id}); 
	}
});

Template.projectView.created = function () {
	Session.set('projectName', this.data.name);
	Session.set('currentSortOption', -1);
	Session.set('nextSortOption', 0);

  var instance = EasySearch.getComponentInstance(
    { id : 'user-search-bar', index : 'searchUsers' }
  );

  instance.on('currentValue', function (val) {
  });
}


