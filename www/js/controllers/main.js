'use strict';

angular.module('app').controller('MainCtrl', function (
    $scope,
    $rootScope,
    $location,
    Config,
    Api) {
    $scope.email = 'nick@nick.com';
    $scope.password = 'nick';

    $scope.login = function() {
        // TODO validation
        Api.user.login(
            {'email': $scope.email, 'password': $scope.password},
            function(resp) {
                $rootScope.user = resp;
                localStorage.setItem('user', JSON.stringify(resp));
                $location.url('/dash');
            }
        );
    };

    $scope.register = function() {
        // TODO validation
        Api.user.register(
            {'email': $scope.email, 'password': $scope.password},
            function(resp) {
                $rootScope.user = resp;
                localStorage.setItem('user', JSON.stringify(resp));
                $location.url('/dash');
            }
        );
    };
  });
