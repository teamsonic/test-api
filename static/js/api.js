var app = angular.module('api', []);

app.factory('NewPerson', function(){
    return{
        'newPerson': function(){
            return {
                'id': null,
                'name': null,
                'age': null,
            };
        },
    };
});

app.controller('ApiController', function($scope, $http, NewPerson){
    var ctrl = this;
    
    ctrl.getCollection = function(){
        $http.get('api/getcollection').success(function(response){
            ctrl.people = response;
        });
    };


    ctrl.createPerson = function(){
        var new_person = NewPerson.newPerson();
        $http.put('api/getone/').success(function(response){
            new_person.id = response;
            ctrl.people.push(new_person);
        });
    };


    ctrl.savePerson = function(person){
        ctrl.post = true;
        $http.post('api/getone/' + person.id, person).success(function(response){
            ctrl.post = false;
        });
    };


    ctrl.deletePerson = function(person){
        ctrl.post = true;
        $http.delete('api/getone/' + person.id).success(function(response){
            ctrl.people.splice(ctrl.people.indexOf(person), 1);
            ctrl.post = false;
        });
    };
            

    ctrl.getCollection();
});
