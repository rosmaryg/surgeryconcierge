Template.loginPage.helpers({
	//If user is logged in, route to the main projects page 
	redirectToProjectSubmit: function() {
		Router.go("/submit/project");
	}
});
