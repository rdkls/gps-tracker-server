angular.module('app').service('Api', function(
    $resource,
    $http,
    User,
    Config) {

        this.user = $resource(Config.api_base_url + '/user/:id', {}, {
            register: {
                method  : 'POST',
                url     : Config.api_base_url + '/user/register'
            },
            login: {
                method  : 'POST',
                url     : Config.api_base_url + '/login'
            },
            get: {
                method  : 'GET',
                headers : {'X-API-KEY': User.api_key},
            },
            list: {
                method  : 'GET',
                headers : {'X-API-KEY': User.api_key},
                isArray : true
            }
        });

        this.device = $resource(Config.api_base_url + '/device/:id', {}, {
            list: {
                method  : 'GET',
                headers : {'X-API-KEY': User.api_key},
                isArray : true,
                transformResponse   : function(resp) {
                    data = JSON.parse(resp);
                    data_changed = [];
                    for(var i=0;i<data.length;i++) {
                        d = data[i];
                        d.icon = d.is_online ? 'img/car-black.png' : 'img/car-grey.png'
                        data_changed.push(d);
                    }
                    return data_changed;
                },
            },
            remove: {
                method  : 'DELETE',
                headers : {'X-API-KEY': User.api_key},
            },
            post: {
                method  : 'POST',
                headers : {'X-API-KEY': User.api_key},
            }
        });

    })
