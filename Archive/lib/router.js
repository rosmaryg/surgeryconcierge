// this page is used for routing all the URLs in our web app

// default layout and loading templates
Router.configure({
  layoutTemplate: "layout",
  loadingTemplate: "loading",
  notFoundTemplate: "notFound",
  waitOn: function() { 
    return [Meteor.subscribe("ownNotificationsUnread")]
  }
});

// basic views, note that the "waitOn" just makes sure that we have
// all the info from the database before the page loads, 
// and the "data" just passes in the necessary pieces of data
// to a template so we can reduce load time (by not just passing in
// EVERYTHING every single time.)

Router.route("/", {
  name: "loginPage",
}); 

Router.route("/project/:_id", {
  name: "projectView",
  waitOn: function() {
    if (Meteor.userId()) {
      return [
        Meteor.subscribe("singleProject", this.params._id),
        Meteor.subscribe("allUsers"),
        Meteor.subscribe("tasks"), 
        Meteor.subscribe("sprintsInProject", this.params._id) //can remove
        ];
    }
  },
  data: function() { return Projects.findOne(this.params._id); }
});

// note: changed task url so it"s just about the project.
// this makes it a lot easier to get some data for notifications.
Router.route("/project/:project/:_id/view", { 
  name: "taskView",
  waitOn: function() {
    return [
      Meteor.subscribe("singleTask", this.params._id),
      Meteor.subscribe("singleProject", this.params.project) 
      ];
  },
  data: function() { return Tasks.findOne(this.params._id); }
});

Router.route("/project/:project/:_id/edit", {
  name: "editTask",
  waitOn: function() {
    return [
      Meteor.subscribe("singleTask", this.params._id),
      Meteor.subscribe("singleProject", this.params.project),
      Meteor.subscribe("sprintsInProject", this.params.project)
    ];
  },
  data: function() { return Tasks.findOne(this.params._id); }
});


Router.route("/project/:_id/create", {
  name: "createNewTask",
  waitOn: function() {
    if (Meteor.userId()) {
      return [
        Meteor.subscribe("singleProject", this.params._id),
        Meteor.subscribe("sprintsInProject", this.params._id)
      ];
    }
  },
  data: function() { return Projects.findOne(this.params._id); }
});

Router.route("/project/:_id/log", {
  name: "activityLog", 
  waitOn: function() {
    return [
      Meteor.subscribe("projectLog", this.params._id)
    ];
  },
  data: function() {
    return Logs.findOne({projectId: this.params._id});
  }
});

Router.route("/project/:_id/sprints", {
  name: "allSprints",
  waitOn: function() {
    return [
      Meteor.subscribe("sprintsInProject", this.params._id), 
      Meteor.subscribe("taskInProject", this.params._id),
      Meteor.subscribe("singleProject", this.params._id)
    ];
  },
  data: function() {
    return Projects.findOne(this.params._id); 
  }
});

Router.route("/project/:_id/sprints/create", {
  name: "createNewSprint",
  waitOn: function() {
    return [
      Meteor.subscribe('singleProject', this.params._id)
    ];
  }
});

Router.route("/submit/project", {
    name: "projectSubmit",
    waitOn: function() {
      if (Meteor.userId()) {
        return [
          Meteor.subscribe("userManagedProjects"),
          Meteor.subscribe("userJoinedProjects"),
          Meteor.subscribe("sprints"),
          Meteor.subscribe("allPosts"),
          Meteor.subscribe("tasks")
        ];
      }
  }
});

Router.route("/notifications/", {
  name: "allNotifications",
  waitOn: function() {
    return [
      Meteor.subscribe("ownNotificationsUndeleted"),
      Meteor.subscribe("userManagedProjects")
    ];
  },
  data: function() {
    var taskNotifsData = {
      //completed: Notifications.find({type: "task completion"}),
      created: Notifications.find({type: "task creation"}),
      deleted: Notifications.find({type: "task deletion"})
    };
    return taskNotifsData;
  }
});

/* BELOW: These links are currently from the example base we drew from.
NOT our code [will be removed by the final demo--just keeping it so we can 
use it as a reference as people learn how to use the framework], 
so ignore the routing here. */


// microscope app"s post links

Router.route("/submit/post/:_id", 
    {name: "postSubmit",
    waitOn: function() {
        return [
            Meteor.subscribe("projects")
        ];
    }
    });

Router.route("/announcements/:postsLimit?", {
  name: "newPosts",
  waitOn: function() {
        return [
            Meteor.subscribe("projects")
        ];
    }
});

Router.route("/calendar", {
    name: "calendar",
    waitOn: function() {
      if (Meteor.userId()) {
        return [
          Meteor.subscribe("tasks")
        ];
      }
  }
});



Router.route("/posts/:_id", {
  name: "postPage",
  waitOn: function() {
    return [
      Meteor.subscribe("singlePost", this.params._id),
      Meteor.subscribe("comments", this.params._id),
      Meteor.subscribe("projects")

    ];
  },
  data: function() { return Posts.findOne(this.params._id); }
});

Router.route("/posts/:_id/edit", {
  name: "postEdit",
  waitOn: function() { 
    return [
    Meteor.subscribe("singlePost", this.params._id),
    ];
  },
  data: function() { return Posts.findOne(this.params._id); }
});

PostsListController = RouteController.extend({
  template: "postsList",
  increment: 5, 
  postsLimit: function() {
    return parseInt(this.params.postsLimit || this.increment); 
  },
  findOptions: function() {
    return {sort: this.sort, limit: this.postsLimit()};
  },
  subscriptions: function() {
    this.postsSub = Meteor.subscribe("posts", this.findOptions());
  },
  posts: function() {
    return Posts.find({}, this.findOptions());
  },
  data: function() {
    var self = this;
    return {
      posts: self.posts(),
      ready: self.postsSub.ready,
      nextPath: function() {
        var posts = self.posts().fetch();
        var numVisPosts = 0;
        _.each(posts, function(post) {
            var project = Projects.findOne({name:post.projectName});
            if(project) {
                _.each(project.users, function(user) {
                    if(Meteor.user() && Meteor.user().username === user)
                        numVisPosts++;
                });
            }
        });
          if (numVisPosts === self.postsLimit()){
            return self.nextPath();
          }
      }
    };
  }
});

NewPostsController = PostsListController.extend({
  sort: {submitted: -1, _id: -1},
  nextPath: function() {
    return Router.routes.newPosts.path({postsLimit: this.postsLimit() + this.increment})
  }
});

var requireLogin = function() {
  if (! Meteor.user()) {
    if (Meteor.loggingIn()) {
      this.render(this.loadingTemplate);
    } else {
      this.render("accessDenied");
    }
  } else {
    this.next();
  }
}

Router.onBeforeAction("dataNotFound", {only: "postPage"});
Router.onBeforeAction(function() {
    if (!Meteor.user() && this.ready()) {
        return this.redirect("/");
    } else {
      this.next();
    }
}, {except: ["loginPage"]}); 
Router.onBeforeAction(requireLogin, 
  {only: ["postSubmit", "userProjectsList", "project", "calendar", "task"]});
