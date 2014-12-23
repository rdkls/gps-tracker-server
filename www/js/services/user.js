angular.module('app').service('User', function(
    $location,
    $rootScope
    ) {

        this.init = function() {
            console.log('user init');
            this._user = JSON.parse(localStorage.getItem('user'));
            console.log(this._user);
            if(this._user) {
                this.api_key = this._user.api_key;
                this.email = this._user.email;
                $rootScope.user = this;
            }
        };

        /* Api passed in here to avoid circular dependencies
        */
        this.login = function(Api, email, password) {
            return Api.user.login({'email': email, 'password': password})
                .$promise.then(function(resp) {
                    localStorage.setItem('user', JSON.stringify(resp));
                    this._user = JSON.parse(localStorage.getItem('user'));
                    this.api_key = this._user.api_key;
                    this.email = this._user.email;
                    $rootScope.user = this;
                    return resp;
            });
        };

        /* Api passed in here to avoid circular dependencies
        */
        this.register = function(Api, email, password) {
            return Api.user.register({'email': email, 'password': password})
                .$promise.then(function(resp) {
                    localStorage.setItem('user', JSON.stringify(resp));
                    this._user = JSON.parse(localStorage.getItem('user'));
                    this.api_key = this._user.api_key;
                    this.email = this._user.email;
                    $rootScope.user = this;
                    return resp;
            });
        };

        this.logout = function() {
            this.api_key = null;
            this.email = null;
            this._user = null;
            localStorage.setItem('user', null);
            $rootScope.user = null;
            localStorage.clear();
            $location.url('/');
        };

        this.init();
    }
);
