'use strict';

angular.module('app').controller('DashCtrl', function (
    $scope,
    $rootScope,
    uiGmapGoogleMapApi,
    Config,
    Api) {

    $scope.init = function() {
        $scope.devices = Api.device.list();
        $scope.showAddDevice = true;

        $scope.map = {
            center: {latitude: -37.219053, longitude: 144.404418 },
            zoom: 4,
            options: {scrollwheel: false}
        };

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
    $scope.uiGmapGoogleMapApi = uiGmapGoogleMapApi;
    uiGmapGoogleMapApi.then(function(maps) {
        console.log('map ready');
        console.log(maps);
    });

    $scope.init();

  });
