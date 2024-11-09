function change_status(ticket_id) {

    const ticket = document.getElementById("ticket-" + ticket_id);
    var status = ticket.value;
    var new_status;

    if (status === "In Bearbeitung") {
        new_status = "Erledigt";
        ticket.classList.remove("red-button");
        ticket.classList.add("green-button");
        ticket.value = new_status;
        ticket.innerText = new_status;
    }

    else {
        new_status = "In Bearbeitung";
        ticket.classList.remove("green-button");
        ticket.classList.add("red-button");
        ticket.value = new_status;
        ticket.innerText = new_status;
    }

    fetch('/tickets/bearbeiten?ticket=' + ticket_id + "&status=" + new_status, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          credentials: 'include',
        })
          .then(response => response.json())
          .then(data => console.log(data))
          .catch(error => console.error(error));
}