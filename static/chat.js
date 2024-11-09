document.addEventListener("keydown", function(event) {

  if (event.key === "Enter") {
    send_message();
  }
});


var socket = io();
var currentChatUser = null;
var chatHistory = {};
let message_sender = document.getElementById("message-sender").innerHTML;
let is_group_chat = false;

let prev_msg_sender = "";

function startChat(username) {
   currentChatUser = username;
   is_group_chat = false;
   renderChatHistory();

   var json_message = {
        "user": message_sender,
        "current_chat": currentChatUser,
    }
    socket.emit('chat-message', json_message);
}
/*function startGroupChat() {
    currentChatUser = "Gruppenchat";
    if (!("Gruppenchat" in chatHistory)) {
        chatHistory["Gruppenchat"] = [];
    }
    renderChatHistory();
}*/
function renderChatHistory() {
    document.getElementById("chatbot-chat-content").innerHTML = '';
     document.querySelector(".chat-header-container").innerText = "Chat mit " + currentChatUser;
}

socket.on("chat-hist-message", function(messages) {
    const chat_message_container = document.getElementById("chatbot-chat-content");

    console.log(messages);

    if (!is_group_chat) {
        for (const message in messages) {
            console.log(messages[message][1])
            if (messages[message][1] !== message_sender) {
                const htmlObject = document.createElement('div');
                htmlObject.className = "message-container fade-in-chat-text-box";
                htmlObject.innerHTML = `<div id="chat-messages"></div><div class="recv-text-bubble">` + messages[message][0] + `</div>`;
                chat_message_container.appendChild(htmlObject);
            } else {
                var htmlObject = document.createElement('div');
                htmlObject.className = "message-container fade-in-chat-text-box";
                htmlObject.innerHTML = `
                                        <div class="send-text-bubble" oncontextmenu="showContextMenu(this, ` + messages[message][3] + `)">` + messages[message][0] + `</div>
                                          <div id="chat-messages"></div>`;

                if (messages[message][2] === "unread") {
                    console.log("unread");
                    htmlObject.innerHTML +=
                        `<div class="message-actions" style="display: none;">
                            <button class="chat-edit-button" onclick="edit_message(this.parentNode.parentNode, ` + messages[message][3] + `);">Bearbeiten</button>
                            <button class="chat-delete-button" onclick="delete_message(this.parentNode.parentNode, null, ` + messages[message][4] + `);">Löschen</button>
                        </div>`;
                }

                chat_message_container.appendChild(htmlObject);
            }
        }
    }
    chat_message_container.scrollTop = chat_message_container.scrollHeight;
});

// Get chat message from other user
socket.on('chat-message', function(message) {
    // ToDo: Hier message box mit Nachricht und timestamp generieren und ins DOM einfügen
    console.log(message);

    const chat_message_container = document.getElementById("chatbot-chat-content");

    const htmlObject = document.createElement('div');
    htmlObject.className = "message-container fade-in-chat-text-box";

    console.log(message.group)
    console.log(currentChatUser)

    if (!is_group_chat && message.receiver === message.group) {

        console.log("GEHT WEITER");

        htmlObject.innerHTML = `<div class="recv-text-bubble">` + message.content + `</div>`;
        chat_message_container.appendChild(htmlObject);

        const message_options = document.querySelectorAll(".message-actions");

        message_options.forEach(function (option) {
            option.style.display = "none";
        });
    }

    else if (currentChatUser === message.group)
    {

        if (prev_msg_sender !== message.sender) {
            htmlObject.innerHTML = `<a class="link-to-profile" style="color: #333333; text-decoration: none; margin-left: 5px;" href="/profile/` + message.sender + `">` + message.sender + `<div class="recv-text-bubble">` + `</a><br>` + message.content + `</div>`;
        } else {
            htmlObject.innerHTML = `<div class="recv-text-bubble">` + message.content + `</div>`;
        }

        chat_message_container.appendChild(htmlObject);

    }

    prev_msg_sender = message.sender;
    chat_message_container.scrollTop = chat_message_container.scrollHeight;

});
function send_message() {
    const chat_message_container = document.getElementById("chatbot-chat-content");
    var message = document.getElementById('chat-message-input').value;
    var json_message = {
        "sender": message_sender,
        "receiver": currentChatUser,
        "message": message
    }

    if (!is_group_chat) {
        socket.emit('chat-message', json_message);
        const unixTimestamp = Math.floor(Date.now() / 1000);
        document.getElementById('chat-message-input').value = '';

        var htmlObject = document.createElement('div');
        htmlObject.className = "message-container fade-in-chat-text-box";
        htmlObject.innerHTML = `
             <div class="send-text-bubble" oncontextmenu="showContextMenu(this, ` + unixTimestamp + `)">` + message + `</div>
             <div id="chat-messages"></div>
             <div class="message-actions" style="display: none;">
            <button class="chat-edit-button" onclick="edit_message(this.parentNode.parentNode, ` + unixTimestamp + `);">Bearbeiten</button>
            <button class="chat-delete-button" onclick="delete_message(this.parentNode.parentNode, ` + unixTimestamp + `);">Löschen</button>
        </div>`;

        chat_message_container.appendChild(htmlObject);
        chat_message_container.scrollTop = chat_message_container.scrollHeight;
    } else {

        console.log("SENDING TO A GROUP")
        console.log(json_message);

        socket.emit('group-chat-message', json_message);
        document.getElementById('chat-message-input').value = '';

        var htmlObject = document.createElement('div');
        htmlObject.className = "message-container fade-in-chat-text-box";
        htmlObject.innerHTML = `
             <div class="send-text-bubble">` + message + `</div>
             <div id="chat-messages"></div>`;

        chat_message_container.appendChild(htmlObject);
        chat_message_container.scrollTop = chat_message_container.scrollHeight;
    }
}

function showContextMenu(element, timestamp) {
    let message = element.innerText;
    check_message_read_status(message, timestamp)
        .then(data => {
            console.log(data)

          if (!data) {
              let messageActions = element.nextElementSibling.nextElementSibling;
              console.log(element);
              console.log(messageActions);

              if (messageActions.style.display === "none") {
                  messageActions.style.display = "block";
              } else {
                  messageActions.style.display = "none";
              }
        }
      });
}

function edit_message(messageContainer, timestamp) {
    const messageTextElement = messageContainer.querySelector(".send-text-bubble");
    const editedMessageInput = document.getElementById("edited-message-input");
    editedMessageInput.value = messageTextElement.textContent;

    const update_timestamp_field = document.getElementById("update-timestamp-hidden");
    update_timestamp_field.value = timestamp;
    const update_message_field = document.getElementById("update-message-hidden");
    update_message_field.value = messageTextElement.textContent;

    // Fügen Sie der Nachrichtencontainer-Div die Klasse "editing" hinzu
    messageContainer.classList.add("editing");

    // Öffnen des Popup-Fensters
    const editMessagePopup = document.getElementById("edit-message-popup");
    editMessagePopup.style.display = "block";
}

function updateMessage() {
    const editedMessageInput = document.getElementById("edited-message-input");
    const editedText = editedMessageInput.value;

    // Aktualisieren der Nachricht
    const messageContainer = document.querySelector(".message-container.editing");
    const messageTextElement = messageContainer.querySelector(".send-text-bubble");
    messageTextElement.textContent = editedText;

    fetch('/edit-message?message=' + document.getElementById("update-message-hidden").value + '&timestamp=' + document.getElementById("update-timestamp-hidden").value + "&new_message=" + editedText, {
            method: 'GET',
            credentials: 'include',
        })
            .then(response => {
                return response.json();
            })
            .then(data => {
                console.log(data);
                let status = data === true? "bearbeitet" : "fehler";
                console.log(status);
                if (status === "bearbeitet") {
                    messageTextElement.style.backgroundColor = "yellow";
                }
                else if (status === "fehler") {
                    messageTextElement.style.backgroundColor = "green";
                }
            });


    closeEditMessagePopup();
}
function closeEditMessagePopup() {
    const editMessagePopup = document.getElementById("edit-message-popup");
    editMessagePopup.style.display = "none";
}

function delete_message(element, unixtime=null, id=null) {
    if (unixtime != null) {
        fetch('/delete-message?find-id=true&message=' + element.querySelector(".send-text-bubble").innerText + '&timestamp=' + unixtime, {
            method: 'GET',
            credentials: 'include',
        })
            .then(response => {
                return response.json();
            })
            .then(data => {
                let status = data === true? "gelöscht" : "fehler"
                if (status === "gelöscht") {
                    element.querySelector('.send-text-bubble').style.backgroundColor = "red";
                }
                else if (status === "fehler") {
                    element.querySelector('.send-text-bubble').style.backgroundColor = "yellow";
                }
            });
    }
    else {
         fetch('/delete-message?message-id=' + id, {
            method: 'GET',
            credentials: 'include',
        })
            .then(response => {
                return response.json();
            })
            .then(data => {
                let status = data === true? "gelöscht" : "fehler"
                if (status === "gelöscht") {
                    element.querySelector('.send-text-bubble').style.backgroundColor = "red";
                }
                else if (status === "fehler") {
                    element.querySelector('.send-text-bubble').style.backgroundColor = "yellow";
                }
            });
    }
}

function check_message_read_status(message, timestamp) {
    return fetch('/read-message-status?message=' + message + '&timestamp=' + timestamp, {
        method: 'GET',
        credentials: 'include',
    })
        .then(response => {
            return response.json();
        })
        .then(data => {
            return data;
        });

}

/*
        This part is specifically for the group chat actions
 */

function openCreateGroupPopup() {
    document.getElementById("create-group-popup").style.display = "block";
    document.getElementById("user-list-popup").style.display = "block";
}
function closeCreateGroupPopup() {
    document.getElementById("create-group-popup").style.display = "none";
    document.getElementById("user-list-popup").style.display = "none";
    document.getElementById("group-members-input").value = "";
    document.getElementById("group-name-input").value = "";
}

function createGroup() {
    openCreateGroupPopup()
    var groupNameInput = document.getElementById("group-name-input");
    var groupName = groupNameInput.value;
    const groupMembers = document.getElementById("group-members-input").value.split(",");

    if (groupName && groupMembers.length > 0) {

        let json_payload = {
            'group_name': groupName,
            'members': groupMembers
        }

        fetch('create_group_chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            credentials: 'include',
            body: JSON.stringify(json_payload)
        });

        var chatsContainer = document.querySelector('.chats-container');
        var groupButton = document.createElement('button');
        groupButton.className = 'chats-single-chat';
        groupButton.innerHTML = `
        <div class="chat-profile-picture"></div>
        <div class="chats-single-chat-name">${groupName}</div>
    `;
        groupButton.addEventListener('click', function () {
            openGroupChat(groupName);
        });

        chatsContainer.appendChild(groupButton);

        closeCreateGroupPopup();
    }

}

function openGroupChat(group) {
     currentChatUser = group;
     is_group_chat = true;

     var json_message = {
        "sender": message_sender,
        "receiver": group
    }

     socket.emit('group-changed-message', json_message);
     renderChatHistory();

     const chat_message_container = document.getElementById("chatbot-chat-content");

     fetch('/load_group_message_hist', {
            method: 'GET',
            credentials: 'include',
        })
            .then(response => {
                return response.json();
            })
            .then(data => {
                console.log(data);
                let prev_sender = "";

                for (let message in data) {

                    console.log(data[message]['message']);
                    let htmlObject = document.createElement('div');

                    if (data[message]['sender'] === 'you') {

                        htmlObject.className = "message-container fade-in-chat-text-box";
                        htmlObject.innerHTML = `<div class="send-text-bubble">` + data[message]['message'] + `</div>
                                                <div id="chat-messages"></div>`;
                    } else {
                        if (prev_sender !== data[message]['sender']) {
                            htmlObject.innerHTML = `<a class="link-to-profile" style="color: #333333; text-decoration: none; margin-left: 5px;" href="/profile/` + data[message]['sender'] + `">` + data[message]['sender'] + `<div class="recv-text-bubble">` + `</a><br>` + data[message]['message'] + `</div>`;
                        } else {
                            htmlObject.innerHTML = `<div class="recv-text-bubble">` + data[message]['message'] + `</div>`;
                        }
                    }
                    prev_sender = data[message]['sender'];
                    chat_message_container.appendChild(htmlObject);

                }

                chat_message_container.scrollTop = chat_message_container.scrollHeight;

            });
}
function add_user_to_group_chat(username) {

    let members = document.getElementById("group-members-input");

    // User can only be added once
    if (members.value === "") {
        members.value = username
    }
    else {
        const groupMembers = document.getElementById("group-members-input").value.split(",");
        console.log(groupMembers.includes(username))
        if (!groupMembers.includes(username)) {
            members.value += ', ' + username;
        }
    }
}
