var app = angular.module('myApp', []);

app.factory('repos', function() {
    var list = [];
    var language = "";
    var numRepos = 0;
    reposService = {};

    reposService.setList = function(new_repos) {
    	list = new_repos;
    };

    reposService.getList = function () {
    	return list;
    };

    reposService.setLanguage = function(new_language) {
    	language = new_language;
    };

    reposService.getLanguage = function() {
    	return language;
    };

    reposService.setNumRepos = function(num) {
    	numRepos = num;
    };

    reposService.getNumRepos = function() {
    	return numRepos;
    };

    return reposService;
});


function RepoCtrl($scope, $http, repos) {
	$scope.language = "";

	$scope.doSearch = function() {
		var url = encodeURIComponent("/issues/" + $scope.language)
		$http.get(url).
		success(function(data, status, headers, config) {
			repos.setList(data['issues']);
			repos.setNumRepos(data['count']);
			repos.setLanguage($scope.language)
		})
	}
}

function RepoDisplayCtrl($scope, repos) {
	$scope.language = repos.getLanguage
	$scope.repos = repos.getList;
	$scope.numRepos = repos.getNumRepos;
}