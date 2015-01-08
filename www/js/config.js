angular.module('app').service('Config', function() {
    this.api_base_url = 'http://10.0.1.10:5000';

    this.icon_device_online = 'img/car-black.png';
    this.icon_device_offline = 'img/car-grey.png';
    this.icon_device_active = 'img/car-blue.png';
});
