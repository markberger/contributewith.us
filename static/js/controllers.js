var app = angular.module('myApp', []);

app.factory('repos', function() {
    var list = [];
    var language = "";
    var numRepos = 0;
    var pageNum = 0;
    reposService = {};

    reposService.setList = function(new_repos) {
    	pageNum = 0;
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

    reposService.getPageNum = function() {
        return pageNum;
    };

    reposService.nextPage = function() {
        pageNum++;
    };

    reposService.prevPage = function() {
        pageNum--;
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
	};
}

function RepoDisplayCtrl($scope, repos) {
	$scope.language = repos.getLanguage
	$scope.repos = repos.getList;
	$scope.numRepos = repos.getNumRepos;
    $scope.reposPerPage = 20;
    $scope.pageNum = repos.getPageNum;
    $scope.nextPage = repos.nextPage;
    $scope.prevPage = repos.prevPage;
    $scope.showRepos = function() {
        pageNum = $scope.pageNum();
        reposPerPage = $scope.reposPerPage;
        start = pageNum * reposPerPage;
        return $scope.repos().slice(start, start+reposPerPage);
    };
}