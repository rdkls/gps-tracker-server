angular.module('app').service('Api', function(
    $resource,
    $http,
    Config) {

        this.user = $resource('', {}, {
            login: {
                method  : 'POST',
                url     : Config.api_base_url + '/login',
            }
        });

    })
