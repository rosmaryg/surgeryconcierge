// Code for creation of Sprints database; needs to be worked on
Sprints = new Mongo.Collection("sprints");
if(Meteor.isServer) {
Meteor.methods({
	sprintInsert: function(sprintAttributes) {
		// get current time to compare to sprint start and end dates later 
		var currentTime = new Date(); 
		currentTime.setDate(currentTime.getDate()); 
		currentTime.setHours(0,0,0,0); 

		// check that inputs are type-safe
		check(this.userId, String); 
		check(sprintAttributes, {
			projectId: String, 
			sprintDescription: String,
			sprintStartDate: Date,
			sprintEndDate: Date,
		}); 

		// find the project that the sprint will be in
		var project = Projects.findOne(sprintAttributes.projectId); 
		// sprint number of new sprint reflects updated projectSprintCount
		var sprintNum = project.sprintCount + 1; 
		sprintAttributes = _.extend(sprintAttributes, {
			sprintIsActive: true, 
			sprintNumber: sprintNum
		});
		// check whether a sprint with following attributes already exists
		var sprint = Sprints.findOne({
			projectId: sprintAttributes.projectId,
			sprintNumber: sprintAttributes.sprintNumber,
			sprintStartDate: sprintAttributes.sprintStartDate, 
			sprintEndDate: sprintAttributes.sprintEndDate
		}); 
		// if the sprint already exists, throw error 
		if (sprint) {
			throw new Meteor.Error("duplicate-sprint", "Duplicate Sprint Number.");
			return {
			_id: sprint._id
			};  
		} 
		
		// check if sprint start and end dates have already expired
		else if (sprintAttributes.sprintStartDate < currentTime ||
			sprintAttributes.sprintEndDate <= currentTime) {
			throw new Meteor.Error("sprint-date", "Sprint dates have already expired.");

		}
		
		
		// check if the end date is before the start date
		else if (sprintAttributes.sprintStartDate > sprintAttributes.sprintEndDate) {
			throw new Meteor.Error("sprint-date", "Sprint start date must be earlier than end date.");
		}
		// get the objectId of the newly inserted sprint
		sprintAttributes._id = Sprints.insert(sprintAttributes); 
		
		// update the activity log when the sprint has been successfully inserted
		var logEntryDescription = "Created new sprint " + sprintAttributes.sprintNumber;
		Meteor.call("updateLog", sprintAttributes.projectId, 
          {
            description: logEntryDescription,
            color: "white",
            link: "project/" + sprintAttributes.projectId + "/sprints",
            tag: "project create sprint"
          });

		// update the project's sprintCount after new sprint is added
		Meteor.call("projectIncrementSprintCount", sprintAttributes.projectId, 
			function(error, result) {
				console.log("updating project sprint count"); 
				if (error) {
					console.log("project sprint count not incremented successfully. "); 
				}
			} 
		); 
		return { _id: sprintAttributes._id }; 
	},

	sprintDelete: function(sprintId) {
		// check that inputs are type-safe
		check(this.userId, String);
		check(sprintId, String);  
		// remove said sprint from database
		return Sprints.remove({_id: sprintId}); 
	}, 

	sprintUpdateStatus: function(sprintId, isActive) {
		check(sprintId, String); 
		check(isActive, Boolean); 
		return Sprints.update(sprintId, {$set: {sprintIsActive: isActive}}); 
	}
}); 
}

