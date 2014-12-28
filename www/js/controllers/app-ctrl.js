'use strict';

angular.module('app').controller('AppCtrl', function (
    $scope,
    $rootScope,
    Config,
    User,
    Api) {

    $scope.user = User;

  });
