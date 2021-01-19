/**
 * Created by 孙振凯 on 2017/3/2.
 * for requirejs
 */

requirejs.config({
    baseUrl: 'static/js/lib',
    paths: {
        bootstrap: 'bootstrap.min-3.3.5',
        material: 'material.min',
        tether: 'tether-module',
        jquery: 'jquery-1.12.4.min',
        ripples: 'ripples'
    },
    shim: {
        tether: {
            deps: ['jquery']
        },
        bootstrap: {
            deps: ['jquery']
        },
        ripples : {
            deps: ['jquery']
        },
        material: {
            deps : ['jquery', 'ripples', 'bootstrap']
        }
    }
});

requirejs(['material'], function (Material) {
    $.material.init();
});