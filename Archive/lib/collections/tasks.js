Tasks = new Mongo.Collection('tasks');

if(Meteor.isServer) {
  Meteor.methods({
  taskDelete: function(taskId) {
    check(this.userId, String);
    check(taskId, String);

    // get some task information so it can be added to the activity log. 
    var getTaskInformationForLog = Tasks.find({_id: taskId}, {fields: {taskName: 1, projectID: 1, 
      projectName: 1, taskCreator: 1}}).fetch();
    if (getTaskInformationForLog.length != 0) {
      
      var taskName = getTaskInformationForLog[0].taskName;
      var projectId = getTaskInformationForLog[0].projectID;
      var logEntryDescription = Meteor.user().username + ' deleted the task ' + taskName;
      Meteor.call('updateLog', projectId, 
        {
          description: logEntryDescription,
          color: 'red',
          link: '',
          tag: 'task delete'
        }
      );

      // send a notification to the user who owned the task.
      sendTaskNotification(getTaskInformationForLog[0], 'deletion', Meteor.user().username);
    }
    
    return Tasks.remove({_id: taskId});    
  },

  taskDeleteReject: function(taskId) {
    check(taskId, String);
    var taskDetails = Tasks.findOne({_id: taskId});
    sendRejectNotification(taskDetails, 'deletion');
    Tasks.update({_id: taskId}, {$set: {status: 0}});
  },

  updateTaskPendingDeletion: function(taskId) {
    check(this.userId, String);
    check(taskId, String);
    Tasks.update({_id: taskId}, {$set: {status: -1, taskStatus: 'Pending Deletion'}});
    var getTaskInformation = Tasks.find({_id: taskId}, {fields: {taskName: 1, projectID: 1, 
      projectName: 1, taskCreator: 1}}).fetch();
    
    // send a notification to the PM.
    sendTaskNotification(getTaskInformation[0], 'deletion pending', Meteor.user().username);
  },

  updateTaskPendingCompletion: function(taskId) {
    check(this.userId, String);
    check(taskId, String);
    Tasks.update({_id: taskId}, {$set: {status: 1, taskStatus: 'Pending Completion'}});
    var getTaskInformation = Tasks.find({_id: taskId}, {fields: {taskName: 1, projectID: 1, 
      projectName: 1, taskCreator: 1}}).fetch();
    
    // send a notification to the PM.
    sendTaskNotification(getTaskInformation[0], 'completion pending', Meteor.user().username);
  },

  taskCompleteApprove: function(taskId) {
    check(this.userId, String);
    check(taskId, String);
    Tasks.update({_id: taskId}, {$set: {status: 0, taskStatus: 'Completed'}});
    var getTaskInformation = Tasks.find({_id: taskId}, {fields: {taskName: 1, projectID: 1, 
      projectName: 1, taskCreator: 1}}).fetch();
    
    // send a notification to the task owner.
    sendTaskNotification(getTaskInformation[0], 'completion', Meteor.user().username);
  },

  taskCompleteReject: function(taskId) {
    check(taskId, String);
    var taskDetails = Tasks.findOne({_id: taskId});
    sendRejectNotification(taskDetails, 'completion');

    Tasks.update({_id: taskId}, {$set: {status: 0, taskStatus: 'In Progress'}});
  },

  taskInsert: function(taskAttributes) {
    check(this.userId, String);
    check(taskAttributes, {
      projectName: String,
      projectID: String,
      taskName: String,
      taskSprintNumber: String,
      taskStatus: String,
      taskDescription: String,
      taskDifficulty: Number,
      taskLength: String,
      taskOwner: String,
      taskStatus: String,
      taskNotes: [String]
    });
    
    var user = Meteor.user();
    var task = Tasks.findOne({
      projectName: taskAttributes.projectName,
      taskName: taskAttributes.taskName
    });

    if (task)
      throw new Meteor.Error('Duplicate Task Name - This Task already exists in your project.');
    var createDate = new Date(); 
    var defaultDueDate = new Date(createDate); 
    // default due date is set to 14 days after task creation if task not assigned to a sprint
    defaultDueDate.setDate(defaultDueDate.getDate() + 14); 
    task = _.extend(taskAttributes, {
      taskStartDate: createDate,
      taskCreator: user.username,
      taskOwner: user.username,
      normalizedName: taskAttributes.taskName.toLowerCase(),
      taskCreateDate: createDate,
      taskDueDate: defaultDueDate, 
      status: 0 // assign -1 to pending deletion, +1 to pending completion. 
    });
    task._id = Tasks.insert(task);
    
    // added to the activity log. 
    var logEntryDescription = Meteor.user().username + ' created a new task ' + taskAttributes.taskName;
    Meteor.call('updateLog', taskAttributes.projectID, 
      {
        description: logEntryDescription,
        color: 'green',
        link: 'project/' + taskAttributes.projectID + '/' + task._id + '/view',
        tag: 'task create'
      }
    );

    // send a notification to the PM.
    sendTaskNotification(task, 'creation', task.taskCreator);
        
    return {_id: task._id};
  },

  taskAddNote: function(taskId, projectId, input, msgForLog) {
    check(taskId, String);
    check(projectId, String);
    check(input, String);
    check(msgForLog, String);
  	var eachCommentWord = input.split(' ');
    var commenterUsername = eachCommentWord[eachCommentWord.length - 8];
    createTaskCommentNotification(taskId, commenterUsername);
    Meteor.call('updateLog', projectId, 
      {
        description: msgForLog,
        color: 'pink',
        link: 'project/' + projectId + '/' + taskId + '/view',
        tag: 'task note'
      }
    );
    return Tasks.update(taskId, {$addToSet: {taskNotes: input}});
  },

  taskAddToSprint: function(taskId, sprintId) {
    check(taskId, String); 
    check(sprintId, String); 
    var sprint = Sprints.findOne({_id: sprintId}); 
    //return Tasks.update({taskSprintNumber: sprintNumber}); 
    return Tasks.update(taskId, {$set: 
      {taskSprintId: sprintId, 
       taskDueDate: sprint.sprintEndDate, 
       taskStartDate: sprint.sprintStartDate
      }
     }); 
  }, 

  removeTasksFromSprint: function(sprintId) {
    check(sprintId, String); 
    var tasksCursor = Tasks.find({taskSprintId:sprintId}); 
    tasksCursor.forEach(function(task) {
      var id = task._id; 
      Tasks.update(id, {
      $unset: {taskSprintId:'', taskDueDate:'', taskStartDate:''}, 
      $set: {taskSprintNumber: 'Unassigned'}}); 
    }); 
  }
  });
}

// need to actually set permissions for this 
Tasks.allow({
  update: function() { return true; },
});
