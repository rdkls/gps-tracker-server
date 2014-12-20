'use strict';

angular.module('app').controller('MainCtrl', function (
    $scope,
    $rootScope,
    $location,
    Config,
    User,
    Api) {

    $scope.init = function() {
        //$scope.showRegister = true;
        $scope.login_user = {
            'email': 'nick@nick.com',
            'password':'nick'
        }
        $scope.register_user = {};
    };

    $scope.login = function() {
        User.login(Api, $scope.login_user.email, $scope.login_user.password);
    }
    $scope.clickRegister = function() {
        $scope.showRegister = true;
    }

    $scope.register = function() {
        Api.user.register(
            {   
                'email'     : $scope.register_user.email,
                'password'  : $scope.register_user.password
            },
            function(resp) {
                $rootScope.user = resp;
                localStorage.setItem('user', JSON.stringify(resp));
                $location.url('/dash');
            }
        );
    };

    $scope.init();
  });
