# STARTUP INSTRUCTIONS: 

Before you can run this project, you will need to install Meteor with Autoparts, and install Meteorite with NPM.

Run the following commands in the Terminal below:

1. `cd pm-tool-tmp`
2. `parts install meteor` (IF YOU HAVEN'T INSTALLED METEOR ALREADY.)
3. `npm install -g meteorite` (If this doesn't work, you may need to do `sudo npm install -g meteorite`)
4. `mrt update`
5. `meteor add momentjs:moment` (Library used in 09-PMTool project to tack time)
5. `meteor` (Again, if you used sudo before, do `sudo meteor`)

# Mongodb database instructions:

You can view your local mongodb database by running `meteor mongo` (if you used sudo before, this is `sudo meteor mongo`) in a new tab. Note that this only works if the app is already running in a separate tab/window. 

This database's contents are saved locally on your laptop. It won't get updated when you push/pull from git, but it will persist whenever you start up your local application. 

See the mongodb and Meteor documentation whenever you need to remove, find, etc. anything in the collections. 

## Examples: 
- If I run `show collections` I can see what collections (this is the same thing as tables in MySQL) are in my mongodb database. 
- If I run `db.users.find()` any existing users will show up. 
- These collections are created in the `lib/collections` folder in our application.  

# Relevant files:
There are a number of folders/pages that we aren't actually using for this iteration--they are present because this base was pulled from the Meteor example Microscope app (built in the Discover Meteor tutorial). Below is a list of relevant folders for the iteration 1; please note that many of these pages only show up on the running application when a user is logged in, so create an account to test the links.

## Top-level Directories: 
### Client
	Templates: 
	1. The `application` folder contains the wrapper, the `{{> yield}}` handlebar just makes sure that the header (stored in `includes` folder) stays fixed when all the other pages change. Click through the links in the header to see this behavior. 
	2. The `projects` folder is the only new thing that I've added for iteration 1. Inside are a number of templates that pertain to views after a user has created a project. 
	3. Links to some of the projects templates are added in the `header.html` file (see in `includes` folder).


### Lib
	1. The `router.js` is the most important part for linking a newly created template to your application. You can't see your template if it's not linked inside the router. If you don't know how this works, please read the documentation, find a tutorial, or shoot me a message. 
	2. The `collections` folder is how all the mongodb collections are made. Each one also contains server-side methods that will allow you to add, delete, update, etc. an item in your collection. A lot of these have a `check()` function in them--look at the Meteor documentation for `check()` (it's basically just to ensure your inputs are correctly typed).

### Server
	1. `fixtures.js` is just some temporary data that came with the Microscope application. Don't worry about this, but it's good if you feel like adding test data. 
	2. `publications.js` is used in relation to the `waitOn` attribute in all the `Router.route` objects. We need to subscribe to certain fields in a collection rather than subscribing to everything all the time because we need to limit client access. 

### (Takeaways: if none of this makes sense, there's a ton of documentation, so please Google!!)

# Microscope

Microscope is a simple social news app that lets you share links, comment, and vote on them.

It was built with [Meteor](http://meteor.com) as a companion app to [The Meteor Book](http://themeteorbook.com), and is the "little brother" of [Telescope](http://telesc.pe), the (much more complex) open-source social news app that was the inspiration for the book.

Microscope itself is free and open-source, and is a good example of common Meteor app patterns such as:

- Routing
- User Accounts
- Notifications
- Errors
- Publications/Subscriptions
- Permissions

## This Repository

The commits to this repository are organized in a very linear fashion, corresponding to progress throughout the book. Commits are tagged in the format `chapterX-Y`, indicating the `Y`th commit of chapter `X`.

Also, note that as the book focuses on _development_, all CSS is committed in a single commit early on.

### Branches

There are 2 branches in this repository which correspond to advanced code that is covered in sidebars of the book, and outside of the main code progression. They are tagged `sidebarX-Y`, corresponding to the sidebar number in the book.

### Developing on Nitrous.IO

Start hacking on this app on
[Nitrous.IO](https://www.nitrous.io/?utm_source=github.com&utm_campaign=Microscope&utm_medium=hackonnitrous)
in seconds:

[![Hack DiscoverMeteor/Microscope on
Nitrous.IO](https://d3o0mnbgv6k92a.cloudfront.net/assets/hack-l-v1-3cc067e71372f6045e1949af9d96095b.png)](https://www.nitrous.io/hack_button?source=embed&runtime=nodejs&repo=DiscoverMeteor%2FMicroscope&file_to_open=README.nitrous.md)

