'use strict';

angular.module('app').controller('MainCtrl', function (
    $scope,
    $rootScope,
    Config,
    Api) {
    $scope.email = 'nick@nick.com';
    $scope.password = 'nick';

    $scope.login = function() {
        Api.user.login(
            {"email":$scope.email, "password":$scope.password},
            function(data) {
                $scope.api_key=data.api_key;
                localStorage.setItem('api_key', data.api_key);
            }
        );
    };
  });
