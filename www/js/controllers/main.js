'use strict';

angular.module('app').controller('MainCtrl', function (
    $scope,
    $rootScope,
    $location,
    $q,
    Config,
    User,
    Api) {

    $scope.init = function() {
        $scope.showRegister = true;
        $scope.register_user = {
            'email': 'nick-' + Math.random() + '@nick.com',
            'password':'nick',
            'password_again':'nick'
        }
        $scope.login_user = {
            'email': 'nick@nick.com',
            'password':'nick'
        }
    };

    $scope.clickLogin = function() {
        $scope.showRegister = false;
    }
    $scope.clickRegister = function() {
        $scope.showRegister = true;
    }

    $scope.login = function() {
        if(!$scope.login_user.email.match(/^[^@]+@\w+\.\w+$/)) {
            alert("That's not a valid email");
            return;
        }
        // Api ref is passed in here to avoid circular dependencies between User-Api
        User.login(Api, $scope.login_user.email, $scope.login_user.password)
        .then(function(data) {
            $location.url('/dash');
        });
    }

    $scope.register = function() {
        if(!$scope.register_user.email.match(/^[^@]+@\w+\.\w+$/)) {
            alert("That's not a valid email");
            return;
        }
        if($scope.register_user.password != $scope.register_user.password_again) {
            alert('Passwords must match');
        }
        else {
            User.register(Api, $scope.register_user.email, $scope.register_user.password)
            .then(
                function(data) {
                    $location.url('/dash');
                },
                function(data) {
                    alert("Sorry, there was a problem registering that email. Perhaps youre' already registered; try logging in.");
                }
            );
        }
    };

    $scope.init();
  });
