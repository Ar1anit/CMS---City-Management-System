function chatbot_open() {
    const chat_container = document.getElementById("chat-bot-container");
    const open_chat_button_arrow = document.getElementById("open-chat-button-arrow");

    if (chat_container.classList.contains("small")) {
        chat_container.classList.remove("small");
        chat_container.classList.add("big");
        open_chat_button_arrow.classList.remove("closed");
        open_chat_button_arrow.classList.add("opened");
    }
    else {
        chat_container.classList.remove("big");
        chat_container.classList.add("small");
        open_chat_button_arrow.classList.remove("opened");
        open_chat_button_arrow.classList.add("closed");
    }

}

var socket = io();
socket.on('bot-message', function(message) {
    console.log(message);
    const chatbot_message_container = document.getElementById("chatbot-chat-content");
    var htmlObject = document.createElement('div');
        htmlObject.innerHTML = `<div class="message-container fade-in-chat-text-box">
            <div class="recv-text-bubble">` + message + `</div>
        </div>`;

    chatbot_message_container.appendChild(htmlObject);
    chatbot_message_container.scrollTop = chatbot_message_container.scrollHeight;
});

function send_message() {
    const chatbot_message_container = document.getElementById("chatbot-chat-content");
    var message = document.getElementById('chat-message-input').value;
    socket.emit('bot-message', message);
    document.getElementById('chat-message-input').value = '';

    var htmlObject = document.createElement('div');
        htmlObject.innerHTML = `<div class="message-container fade-in-chat-text-box">
            <div class="send-text-bubble">` + message + `</div>
        </div>`;

    chatbot_message_container.appendChild(htmlObject);
}
