'use strict';

angular
  .module('app', [
    'ngResource',
    'ngRoute',
    'uiGmapgoogle-maps'
  ])
  .config(function (
    $routeProvider,
    uiGmapGoogleMapApiProvider
  ) {
    $routeProvider
      .when('/', {
        templateUrl: 'views/main.html',
        controller: 'MainCtrl'
      })
      .when('/dash', {
        templateUrl: 'views/dash.html',
        controller: 'DashCtrl'
      })
      .otherwise({
        redirectTo: '/'
      });
    uiGmapGoogleMapApiProvider.configure({
      key : 'AIzaSyDMLTl_mCtvP038xgjDvgwUhXjV0Ch-ofk',
      v   : '3.17'
    });
  });
