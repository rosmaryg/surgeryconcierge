Comments = new Mongo.Collection("comments");

Meteor.methods({
  // Check for userId, postId, and content before continuing
  commentInsert: function(commentAttributes) {
    check(this.userId, String);
    check(commentAttributes, {
      postId: String,
      body: String
    });
    // Define the user and retrieve the post that this comment will attach to
    var user = Meteor.user();
    var post = Posts.findOne(commentAttributes.postId);

    // If a parent post can't be found, throw an error.
    if (!post)
      throw new Meteor.Error("invalid-comment", "You must comment on a post");
    // Find the project that the comment + post are about
    var project = Projects.findOne({name: post.projectName});
    var projectId = project._id;
    comment = _.extend(commentAttributes, {
      userId: user._id,
      author: user.username,
      submitted: new Date()
    });
    
    // update the post with the number of comments
    Posts.update(comment.postId, {$inc: {commentsCount: 1}});
    
    // create the comment, save the id
    comment._id = Comments.insert(comment);
    
    // now create a notification, informing the user that there's been a comment
    createPostCommentNotification(comment);


    var logEntryDescription = Meteor.user().username + " commented on " + post.title;
    Meteor.call("updateLog", projectId, 
      {
        description: logEntryDescription,
        color: "pink",
        link: "posts/" + commentAttributes.postId,
        tag: "project note comment"
      }
    );
    
    return comment._id;
  }
});
