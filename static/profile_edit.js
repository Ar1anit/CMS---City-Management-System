
function setFriendListVisibility() {

    const sliderInput = document.getElementById('friendList');
    let visibility = sliderInput.checked ? "public" : "private";

    fetch('/friend/visibility/set?visibility=' + visibility, {
        method: 'GET',
        credentials: 'include',
    })
}

function getFriendListVisibility() {
    fetch('/friend/visibility/get', {
        method: 'GET',
        credentials: 'include',
    })
    .then(response => {
            return response.json();
    })
    .then(data => {
        const sliderInput = document.getElementById('friendList');
        console.log(data[0])
        console.log(data[0] === "public");
        sliderInput.checked = data[0] === "public";
    })
}


getFriendListVisibility();

//
// Zyklus 3
//

function saveChanges() {
    const profile_visibility = document.getElementById("profile-visibility");
    const visibility = profile_visibility.checked ? "public" : "private";

    const firstname = document.getElementById('firstname').value;
    const lastname = document.getElementById('lastname').value;
    const password = document.getElementById('password').value;
    const profilinfo = document.getElementById('profilinfo').value;

    let changes = {
        'firstname': firstname,
        'lastname': lastname,
        'password': password,
        'profilinfo': profilinfo
    }

    fetch('/update_profile', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        credentials: 'include',
        body: JSON.stringify(changes)
    })


    fetch('/profile/visibility/set?visibility=' + visibility, {
        method: 'GET',
        credentials: 'include',
    })

    //window.location.reload();
}

function getProfilVisibility() {
    fetch('/profile/visibility/get', {
        method: 'GET',
        credentials: 'include',
    })
    .then(response => {
            return response.json();
    })
    .then(data => {
        const sliderInput = document.getElementById('profile-visibility');
        console.log(data[0])
        console.log(data[0] === "public");
        sliderInput.checked = data[0] === "public";
    })
}

getProfilVisibility()