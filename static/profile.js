function toggleMenu() {
    const container = document.querySelector('.bell-container');
    container.classList.toggle('open');

    const menu = document.querySelector('.menu');
    menu.style.display = container.classList.contains('open') ? 'block' : 'none';

    if (!container.classList.contains('open')) {
        var friendRequestContainer = document.querySelector(".menu");
        var friendRequests = friendRequestContainer.querySelectorAll(".friend-request");

        friendRequests.forEach(function (element) {
            element.remove();
        });
    }
    first_load = false;
}

const menu = document.querySelector('.menu');
menu.addEventListener('click', function (event) {
    event.stopPropagation();
});

const friendRequests = document.querySelectorAll('.friend-request');
const bellIcon = document.querySelector('.bell-icon');

if (friendRequests.length > 0) {
    bellIcon.classList.add('animate');
} else {
    bellIcon.classList.remove('animate');
}


function acceptFriend(friendName) {

    console.log('Nutzer akzeptiert:', friendName);
    accept_Friend(friendName);
    document.getElementById("friend-request-" + friendName).remove();
}

function ignoreFriend(friendName) {

    console.log('Nutzer ignoriert:', friendName);

    fetch('/friend-requests?action=decline&user=' + friendName, {
        method: 'GET',
        credentials: 'include',
    });
}

function searchFriends() {
    var input = document.getElementById('search-friends');
    var filter = input.value.toUpperCase();
    var friendList = document.getElementById('friend-list');
    var friendItems = friendList.getElementsByClassName('friend-item');

    // Durchlaufe alle Freundenelemente und verstecke diejenigen, die nicht der Suche entsprechen
    for (var i = 0; i < friendItems.length; i++) {
        var friendName = friendItems[i].getElementsByClassName('friends-name')[0];
        if (friendName.innerHTML.toUpperCase().indexOf(filter) > -1) {
            friendItems[i].style.display = '';
        } else {
            friendItems[i].style.display = 'none';
        }
    }
}

// Ereignislistener für die Eingabe in das Suchfeld
var searchInput = document.getElementById('search-friends');
searchInput.addEventListener('input', function () {
    searchFriends();
});


function searchUsers() {
    var input = document.getElementById('search-users');
    var filter = input.value.toUpperCase();
    var userList = document.getElementById('user-list');
    var userItems = userList.getElementsByClassName('user-item');

    // Durchlaufe alle Nutzerelemente und verstecke diejenigen, die nicht der Suche entsprechen
    for (var i = 0; i < userItems.length; i++) {
        var userName = userItems[i].getElementsByClassName('user-name')[0];
        if (userName.innerHTML.toUpperCase().indexOf(filter) > -1) {
            userItems[i].style.display = '';
        } else {
            userItems[i].style.display = 'none';
        }
    }
}

// Ereignislistener für die Eingabe in das Suchfeld
var searchInput = document.getElementById('search-users');
searchInput.addEventListener('input', function () {
    searchUsers();
});


function removeFriend(friend_id) {
    const friendItem = document.querySelector(`.friend-item[data-name="${friend_id}"]`);

    fetch('/friend-requests?action=remove&friend=' + friend_id, {
        method: 'GET',
        credentials: 'include',
    })
        .then(response => {
            //Erfolgreich entfernt
        })
        .catch(error => {
            console.error('Error:', error);
        });

    getFreunde();
}

function addFriend(friend_id) {
    fetch('/friend-requests?action=add&friend=' + friend_id, {
        method: 'GET',
        credentials: 'include',
    });

    document.getElementById("addFriend-" + friend_id).innerText = "Anfrage gesendet";
}

function accept_Friend(friend_id) {
    fetch('/friend-requests?action=accept&friend=' + friend_id, {
        method: 'GET',
        credentials: 'include',
    });
}

function getFriendRequests() {

    var friend_request_container = document.querySelector(".menu");
    document.querySelector(".menu").querySelectorAll(".friend-request").forEach(elem => {
        elem.innerHTML = '';
    })

    fetch('/friend-requests?action=get', {
        method: 'GET',
        credentials: 'include',
    })
        .then(response => {
            return response.json();
        })
        .then(data => {
            // Here, `data` represents the JSON response
            console.log(data);
            var friend_request_container = document.querySelector(".menu");
            var friendRequestHTML = `
        <div class="friend-request" id="friend-request-` + data[0].username + `">
            <p><img class="friend-pb" src="./static/images/uploads/` + data[0].profilbild + `" alt="Profilbild"></p>
            <p class="friends-name">` + data[0].username + `</p>
            <button type="submit" class="friend-add" onclick='acceptFriend("` + data[0].username + `")'>Akzeptieren</button>
            <button type="submit" class="friend-decline" onclick='ignoreFriend("` + data[0].username + `")'>Ignorieren</button>
        </div>
        `;
            friend_request_container.innerHTML += friendRequestHTML;
            const bellIcon = document.querySelector('.bell-icon');

            if (friend_request_container.querySelectorAll('.friend-request')) {
                bellIcon.classList.add('animate');
            } else {
                bellIcon.classList.remove('animate');
            }

        })
        .catch(error => {
            console.error('Error:', error);
        });

}

var first_load = true;
getFriendRequests();


function getFreunde(freund) {
    const freunde_container = document.getElementById('friend-list');
    let friends = freunde_container.querySelectorAll(".friend-item");

    friends.forEach(function (element) {
        element.remove();
    });

    console.log("Freunde werden gesucht")

    fetch('/friend-requests?action=get_friends&friend=' + freund, {
        method: 'GET',
        credentials: 'include',
    })
        .then(response => {
            return response.json();
        })
        .then(data => {
            for (let i = 0; i < data.length; i++) {
                console.log(data[i]);
                let friendsHTML = `<div class="friend-item">
                                            <p><img class="friend-pb" src="../static/images/uploads/` + data[i].profilbild + `" alt="Profilbild"></p>
                                            <p class="friends-name">` + data[i].username + `</p>
                                            <button class="btn friend-delete" onclick='removeFriend("` + data[i].username + `")'>Entfernen</button>
                                        </div>`

                freunde_container.innerHTML += friendsHTML;
            }

        })
        .catch(error => {
                console.error('Error:', error);
            }
        );
}