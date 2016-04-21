Template.postEdit.created = function() {
  Session.set('postEditErrors', {});
}

Template.postEdit.helpers({
  errorMessage: function(field) {
    return Session.get('postEditErrors')[field];
  },
  errorClass: function (field) {
    return !!Session.get('postEditErrors')[field] ? 'has-error' : '';
  }
});

Template.postEdit.events({
  'submit form': function(e) {
    e.preventDefault();
    var currentPostId = this._id;
    var postProperties = {
      title: $(e.target).find('[name=title]').val(),
      message: $(e.target).find('[name=message]').val()
    }
    
    var errors = validateEdit(postProperties);
    if (errors.title || errors.message) {
      console.log("Hitting post errors");
      return Session.set('postEditErrors', errors);
    }
    
    Posts.update(currentPostId, {$set: postProperties}, function(error) {
      if (error) {
        // display the error to the user
        throwError(error.reason);
      } else {
        Router.go('postPage', {_id: currentPostId});
      }
    });
  }
});
