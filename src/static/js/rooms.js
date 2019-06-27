$( document ).ready(function() {

    load_data("/api/rooms/", function(json) {
        for(var i = 0; i < json.length; i++) {
            $("#rooms").append("<li><a href='/rooms/"+ json[i].url + "/'>" + json[i].name +"</a></li>");
        }
    });

    // Submit post on submit
    $('#room-form').on('submit', function(event){
        event.preventDefault();
        console.log("form submitted!")  // sanity check
        
        var url = "/api/rooms/";
        var data = { 
            name : $('#name').val()
        };
        var success = function(json) {
            console.log(json); // log the returned json to the console
            $("#room-form")[0].reset();
            var content = "<li><a href='/rooms/"+ json.url + "/'>" + json.name +"</a></li>";
            $("#rooms").append(content);
            console.log("success"); // another sanity check
        };
        create(url, data, success);
    });


});