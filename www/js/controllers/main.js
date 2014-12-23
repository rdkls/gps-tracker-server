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
            'password':'nick'
        }
        $scope.login_user = {
            'email': 'nick@nick.com',
            'password':'nick'
        }
    };

    $scope.login = function() {
        User.login(Api, $scope.login_user.email, $scope.login_user.password)
        .then(function(data) {
            $location.url('/dash');
        });
    }
    $scope.clickLogin = function() {
        $scope.showRegister = false;
    }
    $scope.clickRegister = function() {
        $scope.showRegister = true;
    }

    $scope.register = function() {
        User.register(Api, $scope.register_user.email, $scope.register_user.password)
        .then(function(data) {
            $location.url('/dash');
        });
    };

    $scope.init();
  });
