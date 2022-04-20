var me = {};
me.avatar = "";

var you = {};
you.avatar = "";

var websocket = "";

function formatAMPM(date) {
    var hours = date.getHours();
    var minutes = date.getMinutes();
    var ampm = hours >= 12 ? 'PM' : 'AM';
    hours = hours % 12;
    hours = hours ? hours : 12; // the hour '0' should be '12'
    minutes = minutes < 10 ? '0'+minutes : minutes;
    var strTime = hours + ':' + minutes + ' ' + ampm;
    return strTime;
}            

//-- No use time. It is a javaScript effect.
function insertChat(who, text, time){
    // console.log("InsertChat");
    if (time === undefined){
        time = 0;
    }
    var control = "";
    var date = formatAMPM(new Date());
    
    if (who == "me"){
        control = '<li style="width:100%">' +
                        '<div class="msj macro">' +
                        '<div class="avatar"><img class="img-circle" style="width:100%;" src="'+ me.avatar +'" /></div>' +
                            '<div class="text text-l">' +
                                '<p>'+ text +'</p>' +
                                '<p><small>'+date+'</small></p>' +
                            '</div>' +
                        '</div>' +
                    '</li>';                    
    }else{
        control = '<li style="width:100%;">' +
                        '<div class="msj-rta macro">' +
                            '<div class="text text-r">' +
                                '<p>'+text+'</p>' +
                                '<p><small>'+date+'</small></p>' +
                            '</div>' +
                        '<div class="avatar" style="padding:0px 0px 0px 10px !important"><img class="img-circle" style="width:100%;" src="'+you.avatar+'" /></div>' +                                
                  '</li>';
    }
    setTimeout(
        function(){                        
            $("ul").append(control).scrollTop($("ul").prop('scrollHeight'));
        }, time);
    
}

function resetChat(){
    $("ul").empty();
}

$(".mytext").on("keydown", function(e){
        if (e.which == 13){
            var text = $(this).val();
            console.log("And we should send it: ", text);
            if (text !== ""){
                insertChat("me", text);
                $(this).val('');
                websocket.send(text);
            }
        }
    });

$('body > div > div > div:nth-child(2) > span').click(function(){
    $(".mytext").trigger({type: 'keydown', which: 13, keyCode: 13});
})

//-- Clear Chat
// resetChat();

window.addEventListener("DOMContentLoaded", () => {
    insertChat("you", "Hello, to connect to server type: login//YOURUSERNAME//PASSWORD", 0);
    insertChat("you", "Basic commands: <br> say, \n look, \n map, \n move"); 
    // insertChat("you", "Hi, Pablo", 1500);
    // insertChat("me", "What would you like to talk about today?", 3500);
    // insertChat("you", "Tell me a joke",7000);
    // insertChat("me", "Spaceman: Computer! Computer! Do we bring battery?!", 9500);
    // insertChat("you", "LOL", 12000);


    websocket = new WebSocket("ws://localhost:8001/");


    function receive_message(msg){
        console.log("Message received: ", msg)
        // identify whether it's msg, map, or error
        // 
        var data = JSON.parse(msg["data"]);
        console.log(data)
        // outlog.append(`<p class='from_server'>${data["text"]}</p>`)
        insertChat("you", data["text"], 3);
    }





    websocket.onmessage = receive_message;

  });




//-- NOTE: No use time on insertChat.