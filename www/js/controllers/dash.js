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
            center  : {latitude: 0, longitude: 0},
            zoom    : 1,
            options : {}
        };

    };
    $scope.viewDevice = function(id) {
        // Zoom map to device
        var d = $scope.devices.filter(function(d) {return d.id==id})[0];
        $scope.map.center = d.coords;
        $scope.map.zoom = 12;

        // Also allow us to pass in marker object (from marker click event)
        if('object'==typeof(id)) {
            id = id.key;
            // Referring to 'idKey' needed if using repeated ui-gmap-marker
            // Otherwise, when using one -markers it's just "key"
            //id = id.idKey;
        }
        for(var i=0; i<$scope.devices.length; i++) {
            $scope.devices[i].viewing = null;
            $scope.devices[i].icon = $scope.devices[i].is_online ? Config.icon_device_online : Config.icon_device_offline;
        }
        $scope.devices.filter(function(d) {return d.id==id})[0]['icon'] = Config.icon_device_active;
        $scope.devices.filter(function(d) {return d.id==id})[0]['viewing'] = true;
    };
    $scope.addDevice = function() {
        if($scope.newImei.match(/\d{15}/)) {
            var p = Api.device.post({'imei'  : $scope.newImei});
            p.$promise.then(
                function(resp_succ) {
                    $scope.devices = Api.device.list();
                    $scope.newImei = null;
                },
                function(resp_err) {
                    // Intentionally uninformative; perhaps device already registered by another user
                    alert("Sorry, can't add that device");
                }
            );
        }
        else {
            alert('IMEI should be 15 digits');
        }
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
