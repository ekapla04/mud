var me = {};
me.avatar = "";

var you = {};
you.avatar = "";

var websocket = "";
var commands = ["say", "look", "map", "move", "login"];

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

function verifyInput(text){
    str = text.trim();
    strs = str.split(" ");
    console.log(str.slice(0,4));
    if ((strs.length > 1 && commands.includes(strs[0])) || commands.includes(str.slice(0,4))){
        // console.log(strs);
        return true
        
    }else {
        return false
    }
}

$(".mytext").on("keydown", function(e){
        if (e.which == 13){
            var text = $(this).val();
            console.log("And we should send it: ", text);
            if (verifyInput(text)){
                insertChat("me", text);
                $(this).val('');
                websocket.send(text);
            }else{
                insertChat("you", "Invalid commad: " + text);
                $(this).val('');
            }
        }
    });

$('body > div > div > div:nth-child(2) > span').click(function(){
    $(".mytext").trigger({type: 'keydown', which: 13, keyCode: 13});
})

//-- Clear Chat
// resetChat();

window.addEventListener("DOMContentLoaded", () => {
    
    insertChat("you", "Basic commands: <br> &nbsp;&nbsp;&nbsp;&nbsp;say,<br> \
        &nbsp;&nbsp;&nbsp;&nbsp; look <br> &nbsp;&nbsp;&nbsp;&nbsp; map,<br>\
        &nbsp;&nbsp;&nbsp;&nbsp; move <br> <br> Use: commad message: eg: \
        say hello everyone!" ); 

    // Connect to the server
    websocket = new WebSocket("ws://localhost:8001/");
    
    function receive_message(msg){
        console.log("Message received: ", msg)
        // identify whether it's msg, map, or error
        // 
        var data = JSON.parse(msg["data"]);
        console.log(data)
        // outlog.append(`<p class='from_server'>${data["text"]}</p>`)
        if (data["type"] === "msg"){
            if (data["text"] !== "Enter login string:"){
                insertChat("you", data["text"], 3);
            }
            
        } else if (data["type"] === "map"){
            console.log("Display map", data["texts"]);
        } else {
            console.log("Error: ", data["text"]);
        }
    }


    websocket.onmessage = receive_message;

    var loginUsername = localStorage.getItem("logName");
    var loginPass = localStorage.getItem("logPass");
    var logCommand = "login//" + loginUsername + "//" + loginPass
    console.log("input ", logCommand);

    // log user
    websocket.onopen = () => websocket.send(logCommand);
  });

