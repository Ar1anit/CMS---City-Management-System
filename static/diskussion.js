function showCreateDiskussion() {
    const create_ticket_container = document.getElementById("create-ticket-container");
    const support_heading = document.getElementById("support-heading");

    // Clear every input field (We dont want values in them)!
    const text_inputs = document.querySelectorAll(".text-input");
    for (let i = 0; i < text_inputs.length; i++) {
      text_inputs[i].value = "";
    }

    switch (create_ticket_container.style.display) {

        case "block":
            support_heading.innerHTML = "Diskussionen";
            create_ticket_container.classList.remove('visible');
            create_ticket_container.classList.add('hidden');

            create_ticket_container.style.display = "none";
            break;

        case "none":
            create_ticket_container.style.display = "block";
            support_heading.innerHTML = "Erstelle eine neue Diskussion";

            create_ticket_container.classList.remove('hidden');
            create_ticket_container.classList.add('visible');
            break;

    }
}

function postDiscussion() {
    // Get the input values
    const title = document.getElementById('ticket-name').value;
    const category = document.getElementById('ticket-short-desc').value;
    const text = document.getElementById('ticket-desc').value;

    // Validate the input
    if (!title || !category || !text) {
        // Here you could show an error message to the user
        console.error('All fields must be filled out');
        return;
    }

    // Create the data object
    const data = {
        title: title,
        text: text,
        category: category,
    };

    // Send the AJAX request
    fetch('/create_discussion', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        credentials: 'include', // This is required to include the cookies
        body: JSON.stringify(data)
    }).then(response => {
        if (response.ok) {
            // If the response was successful, reload the page
            location.reload();
        } else {
            // If there was an error, log it to the console
            console.error('Error:', response.statusText);
        }
    }).catch(error => {
        console.error('Error:', error);
    });
}


function postReply(postId) {
    // Get the input value
    const text = document.getElementById('reply-text').value;

    // Create the data object
    const data = {
        text: text
    };

    // Send the AJAX request
    fetch('/post_reply/' + postId, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    }).then(response => {
        location.reload();
    }).catch(error => {
        console.error('Error:', error);
    });
}

