Template.postItem.helpers({
  findProj: function() {
    var projName = this.projectName;
    var proj = Projects.findOne({name: projName});
    return proj._id;
  },
  ownPost: function() {
    return this.userId == Meteor.userId();
  },
  upvotedClass: function() {
    var userId = Meteor.userId();
    if (userId && !_.include(this.upvoters, userId)) {
      return "btn-primary upvotable";
    } else {
      return "disabled";
    }
  }
});

Template.postItem.events({
  "click .upvotable": function(e) {
    e.preventDefault();
    Meteor.call("upvote", this._id);
  },
  "click .discuss": function(e) {
    e.preventDefault();
    if (confirm("Delete this post?")) {
        var currentPostId = this._id;
        Posts.remove(currentPostId);
        Router.go('newPosts');
    }
  }
});
