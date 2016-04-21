// check that the userId specified owns the documents
ownsDocument = function(userId, doc) {
  return doc && doc.userId === userId;
}

ownsNotification = function(userId, doc) {
	return doc && (doc.sendToUsers.indexOf(userId) != -1);
}
// check that a user is a member of a project
memberInProject = function(userId, pm, projectUsers) {
	return (_.contains(projectUsers, userId) || userId == pm);
}