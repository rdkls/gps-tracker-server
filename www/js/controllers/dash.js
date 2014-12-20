'use strict';

angular.module('app').controller('DashCtrl', function (
    $scope,
    $rootScope,
    Config,
    Api) {

    $scope.init = function() {
        $scope.devices = Api.device.list();
        $scope.showAddDevice = true;
    };
    $scope.viewDevice = function(imei) {
        console.log('viewDevice ' + imei);
    };
    $scope.addDevice = function() {
        Api.device.post(
            {'imei'  : $scope.newImei},
            function(resp) {
                $scope.devices = Api.device.list();
            }
        );
        $scope.newImei = null;
    };
    $scope.removeDevice = function(device_id) {
        Api.device.remove(
            {'id': device_id},
            function(resp) {
                $scope.devices = Api.device.list();
            }
        );
    };

    $scope.init();

  });
