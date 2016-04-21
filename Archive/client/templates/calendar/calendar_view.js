// Calendar rendering handling -- what to show as header and how to handle multiple events
Template.calendar.rendered = function() {
    var tasks = Tasks.find({taskOwner: Meteor.user().username}).fetch();
    var calEvents = [];
    _.each(tasks, function(task) {
        calEvents.push({title: task.projectName + ": " + task.taskName, start: task.taskStartDate, end: task.taskDueDate});
    });
    $("#calendar").fullCalendar({
    header: {
      left: "prev",
      right: "next",
      center: "title"
    },
    defaultDate: new Date(),
    editable: false,
    eventLimit: true, // allow "more" link when too many events
    events: calEvents
  });
};


