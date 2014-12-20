angular.module('app').service('User', function(
    $location,
    $rootScope
    ) {

        this.init = function() {
            this._user = JSON.parse(localStorage.getItem('user'));
            if(this._user) {
                this.api_key = this._user.api_key;
                this.email = this._user.email;
                $rootScope.user = this;
            }
        };

        /* Api passed in here to avoid circular dependencies
        */
        this.login = function(Api, email, password) {
            Api.user.login(
                {'email': email, 'password': password},
                function(resp) {
                    localStorage.setItem('user', JSON.stringify(resp));
                    this._user = JSON.parse(localStorage.getItem('user'));
                    this.api_key = this._user.api_key;
                    this.email = this._user.email;
                    $rootScope.user = this;
                    $location.url('/dash');
                }
            );
        };

        this.logout = function() {
            this._user = null;
            $rootScope.user = null;
            localStorage.clear();
            $location.url('/');
        };

        this.init();
    }
);
