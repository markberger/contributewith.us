contributewith.us
=================

Github doesn't allow users to search for repositories with open issues. ContributeWith.Us tries to fix this.

The site is run with Flask and AngularJS on Heroku. Repositories and cached from Github into a MongoDB database since there is a limited number of API calls per hour and no way to filter all repositories using issues. In order for a repository to be cached in the database it must have at least ten open isuses.
