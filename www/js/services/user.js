angular.module('app').service('User', function(
    $location
    ) {
        var self = this;

        // Used in API resource headers
        // Defined as function (as opposed to accessing value directly)
        // means it'll be evaluated at time of request and will contain current
        // logged-in user
        this.get_api_key = function() {
            console.log('get_api_key: ' + self.api_key);
            return self.api_key;
        }

        this.init = function() {
            self._user = JSON.parse(localStorage.getItem('user'));
            if(self._user) {
                self.api_key = this._user.api_key;
                self.email = this._user.email;
            }
        };

        /* Api passed in here to avoid circular dependencies
        */
        this.login = function(Api, email, password) {
            return Api.user.login({'email': email, 'password': password})
                .$promise.then(function(resp) {
                    self['api_key'] = resp.api_key;
                    self['email'] = resp.email;
                    localStorage.setItem('user', JSON.stringify(resp));
                })
            ;
        };

        /* Api passed in here to avoid circular dependencies
        */
        this.register = function(Api, email, password) {
            return Api.user.register({'email': email, 'password': password})
                .$promise.then(function(resp) {
                    self['api_key'] = resp.api_key;
                    self['email'] = resp.email;
                    localStorage.setItem('user', JSON.stringify(resp));
                    return resp;
            });
        };

        this.logout = function() {
            this.api_key = null;
            this.email = null;
            this._user = null;
            localStorage.setItem('user', null);
            localStorage.clear();
            $location.url('/');
        };

        this.init();
    }
);
