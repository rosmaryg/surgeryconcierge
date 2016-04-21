Posts = new Mongo.Collection("posts");

// Allow a user to update and remove from the Posts collection if they provide a userId and the post
Posts.allow({
  update: function(userId, post) { return ownsDocument(userId, post); },
  remove: function(userId, post) { return ownsDocument(userId, post); },
});

// Do not allow the user to modify the Posts collection otherwise
Posts.deny({
  update: function(userId, post, fieldNames) {
    // may only edit the following fields:
    return (_.without(fieldNames, "title", "message", "projectName").length > 0);
  }
});

// Checks to make sure the post has all valid fields filled
validatePost = function (post) {
  var errors = {};

  if (!post.title)
    errors.title = "Please fill in a headline";
      
  if (!post.message)
    errors.message = "Please fill in a message";

  if (!post.projectName)
    errors.message = "Unable to locate the project name";

  return errors;
}

// Checks to make sure that the post has all valid fields filled.
validateEdit = function (post) {
  var errors = {};

  if (!post.title)
    errors.title = "Please fill in a headline";
  
  if (!post.message)
    errors.message = "Please fill in a message";

  return errors;
}


// Insertion
Meteor.methods({
  postInsert: function(postAttributes) {
    check(this.userId, String);
    check(postAttributes, {
      title: String,
      message: String,
      projectName: String
    });
    
    var errors = validatePost(postAttributes);
    if (errors.title || errors.message || errors.projectName)
      throw new Meteor.Error("invalid-post", "You must set a title and message for your post");
        
    var user = Meteor.user();
    var post = _.extend(postAttributes, {
      userId: user._id, 
      author: user.username, 
      submitted: new Date(),
      commentsCount: 0,
      upvoters: [], 
      votes: 0
    });
    
    var postId = Posts.insert(post);
    post._id = postId;

    createAnnouncementNotification(post);

    var projectInfo = Projects.findOne({name: postAttributes.projectName});
    var projectId = projectInfo._id;
    var logEntryDescription = "Announcement posted: " + postAttributes.title;
    Meteor.call("updateLog", projectId, 
      {
        description: logEntryDescription,
        color: "pink",
        link: "posts/" + postId,
        tag: "project note"
      }
    );

    return {
      _id: postId
    };
  },

  // Upvote for announcement handler
  upvote: function(postId) {
    check(this.userId, String);
    check(postId, String);
    
    var affected = Posts.update({
      _id: postId, 
      upvoters: {$ne: this.userId}
    }, {
      $addToSet: {upvoters: this.userId},
      $inc: {votes: 1}
    });
    
    if (! affected)
      throw new Meteor.Error("invalid", "You weren't able to upvote that post");
  }
});
