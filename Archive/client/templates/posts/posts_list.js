Template.postsList.helpers({
    // Determine which projects to show
    myProj: function() {
        var proj = Projects.findOne({name: this.projectName});
        var mine = false;
        if(proj) {

            _.each(proj.users, function(user) {
                if(Meteor.user()) {
                    mine = mine || (Meteor.user().username === user);
                }
            }); 
        }
        return mine;    
    },
    // Determine if no posts are shown
    notShown: function() {
        if(!Meteor.user()) {
            return false;
        }
        updateLists();
        var posts = Posts.find({}).fetch();
        var visibility = false;
        _.each(posts, function(post) {
            var project = Projects.findOne({name:post.projectName});
            if(project) {      
                _.each(project.users, function(user) {
                    visibility = visibility || (Meteor.user().username === user);
                });
            }
        });
        return !visibility;
    }
});
var updateLists = function() {
        var allPostNodes = document.getElementsByClassName("collapsibleList");
        var i;
       for(i=0; i<allPostNodes.length; i++) {
           var currNode = allPostNodes.item(i);
           var collapsibleList =  currNode.getElementsByClassName("collapsibleListClosed");
           // Already collapsible, don't apply again
           if(collapsibleList.length > 0) {
               continue;
           }
           else {
               CollapsibleLists.applyTo(allPostNodes.item(i)); 
           }
       }
};

Template.postsList.rendered = function () {
    updateLists();
    this.find('.wrapper')._uihooks = {
    insertElement: function (node, next) {
      $(node)
        .hide()
        .insertBefore(next)
        .fadeIn();
    },
    moveElement: function (node, next) {
      var $node = $(node), $next = $(next);
      var oldTop = $node.offset().top;
      var height = $(node).outerHeight(true);
      
      // find all the elements between next and node
      var $inBetween = $(next).nextUntil(node);
      if ($inBetween.length === 0)
        $inBetween = $(node).nextUntil(next);
      
      // now put node in place
      $(node).insertBefore(next);
      
      // measure new top
      var newTop = $(node).offset().top;
      
      // move node *back* to where it was before
      $(node)
        .removeClass('animate')
        .css('top', oldTop - newTop);
      
      // push every other element down (or up) to put them back
      $inBetween
        .removeClass('animate')
        .css('top', oldTop < newTop ? height : -1 * height)
        
      
      // force a redraw
      $(node).offset();
      
      // reset everything to 0, animated
      $(node).addClass('animate').css('top', 0);
      $inBetween.addClass('animate').css('top', 0);
    },
    removeElement: function(node) {
      $(node).fadeOut(function() {
        $(this).remove();
      });
    }
  }
}
