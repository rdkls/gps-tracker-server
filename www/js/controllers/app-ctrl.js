'use strict';

angular.module('app').controller('AppCtrl', function (
    $scope,
    $rootScope,
    Config,
    User,
    Api) {

    $scope.logout = function() {
        User.logout();
    };

  });
