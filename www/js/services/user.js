angular.module('app').service('User', function(
    ) {
        this._user = JSON.parse(localStorage.getItem('user'));
        this.api_key = this._user.api_key;
        this.email = this._user.email;
    }
);
