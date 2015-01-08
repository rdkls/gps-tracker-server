'use strict';

angular.module('app').controller('DashCtrl', function (
    $scope,
    $rootScope,
    uiGmapGoogleMapApi,
    Config,
    User,
    Api) {

    $scope.init = function() {
        $scope.devices = Api.device.list();
        $scope.showAddDevice = true;

        $scope.map = {
            center  : {latitude: "-37.77", longitude: "144.97"},
            zoom    : 12,
            options : {}
        };

    };
    $scope.viewDevice = function(id) {
        // Also allow us to pass in marker object (from marker click event)
        if('object'==typeof(id)) {
            id = id.idKey;
        }
        for(var i=0; i<$scope.devices.length; i++) {
            $scope.devices[i].viewing = null;
            $scope.devices[i].icon = $scope.devices[i].is_online ? Config.icon_device_online : Config.icon_device_offline;
        }
        $scope.devices.filter(function(d) {return d.id==id})[0]['icon'] = Config.icon_device_active;
        $scope.devices.filter(function(d) {return d.id==id})[0]['viewing'] = true;
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
    });

    $scope.init();

  });
