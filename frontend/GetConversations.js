function loadConversations() {
    var uid = firebase.auth().currentUser.uid;
    conversationIDs = []
    var conversations = firebase.database().ref("Users/" + uid + "/Conversations");
    conversations.once("value", function (snapshot) {
        let data = snapshot.val()
        for (let k in data) {
            console.log(data[k])
            if (data[k] != 0) {
                conversationIDs.push(data[k]);
            }
        }
    }).then(() => {

        conversationNames = []
        for (let i = 0; i < 5; i++) {
            if (i < conversationIDs.length) {
                var conversationRef = firebase.database().ref("Conversations/" + conversationIDs[i]);
                conversationRef.once("value", function (snapshot) {
                    conversationNames.push(snapshot.val()['name']);
                }).then(() => {
                    $("#button-" + (i + 1)).html(conversationNames[i]);
                });
            } else {
                $("#button-" + (i + 1)).remove();
            }
        }
    });
}
