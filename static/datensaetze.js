//animation for like-Button is from: https://codepen.io/abaicus/pen/gNXdQP/
let buttons = document.querySelectorAll(".like-button");

buttons.forEach(function(button) {
  button.addEventListener("click", function(e) {
    //e.preventDefault();
    this.classList.toggle("active");
    this.classList.add("animated");
    generateClones(this);
  });

});



function generateClones(button) {
  let clones = randomInt(2, 4);
  for (let it = 1; it <= clones; it++) {
    let clone = button.querySelector("svg").cloneNode(true),
      size = randomInt(5, 16);
    button.appendChild(clone);
    clone.setAttribute("width", size);
    clone.setAttribute("height", size);
    clone.style.position = "absolute";
    clone.style.transition =
      "transform 0.5s cubic-bezier(0.12, 0.74, 0.58, 0.99) 0.3s, opacity 1s ease-out .5s";
    let animTimeout = setTimeout(function() {
      clearTimeout(animTimeout);
      clone.style.transform =
        "translate3d(" +
        (plusOrMinus() * randomInt(10, 25)) +
        "px," +
        (plusOrMinus() * randomInt(10, 25)) +
        "px,0)";
      clone.style.opacity = 0;
    }, 1);
    let removeNodeTimeout = setTimeout(function() {
      clone.parentNode.removeChild(clone);
      clearTimeout(removeNodeTimeout);
    }, 900);
    let removeClassTimeout = setTimeout(function() {
      button.classList.remove("animated");
    }, 600);
  }
}

function randomInt(min, max) {
  return Math.floor(Math.random() * (max - min + 1)) + min;
}

function plusOrMinus() {
  return Math.random() < 0.5 ? -1 : 1;
}


// ToDO: This will implement an advanced search

function contains_string(string_1, string_2) {

    for (let i = 0; i < string_2.length; i++) {

        if (string_1[i] !== string_2[i]) return false;

    }

    return true;
}


/* Search Anfrage*/
const searchForm = document.querySelector('form');
const searchInput = document.getElementById('suche');
const yearFilter = searchForm.querySelector('#yearFilter');
const nameFilter = searchForm.querySelector('#nameFilter');

// Retrieve information about every container
const everyDSContainer = document.querySelectorAll(".container-lg");
const everyDSText = document.querySelectorAll(".card-text");

// Doing this in the frontend is way faster
searchForm.addEventListener('input', function(event) {
    event.preventDefault();


    if (yearFilter.checked) {
        everyDSContainer.forEach(DSContainer => {
            const year = DSContainer.querySelector(".card-text");
            console.log(year.innerHTML)
            if (!contains_string(year.innerHTML, searchInput.value)) {
                console.log(year.value)
                DSContainer.style.opacity = 0;
                DSContainer.addEventListener('transitionend', function() {
                    DSContainer.style.display = "none";
                }, {once: true});
            }
            else if (contains_string(year.innerHTML, searchInput.value)) {
                DSContainer.style.display = "block";
                DSContainer.style.opacity = 1;
                DSContainer.style.transition = "opacity 0.5s";
            }
        });

    } else if (nameFilter.checked) {
        // Suche nach Name
         everyDSContainer.forEach(DSContainer => {
            if (!contains_string(DSContainer.id, searchInput.value)) {
                DSContainer.style.opacity = 0;
                DSContainer.addEventListener('transitionend', function() {
                    DSContainer.style.display = "none";
                    // Add event listener to set display to none after transition ends
                }, {once: true});
            }
            else if (contains_string(DSContainer.id, searchInput.value)) {
                DSContainer.style.display = "block";
                DSContainer.style.opacity = 1;
                DSContainer.style.transition = "opacity 0.5s";
            }
        });
    }

    if (searchInput.value === "") {
        everyDSContainer.forEach(DSContainer => {
            DSContainer.style.display = "block";
            DSContainer.style.opacity = 1;
            DSContainer.style.transition = "opacity 0.5s";
        });
    }
});

    // remove Datensatz
    let btn = document.getElementById("deleteBtn");

    //btn.addEventListener("click", function () {
        //rowElement.remove();
    //}
//);

// update Pop Up
let headers = document.querySelectorAll(".update-headers");
let rows = [];
function openFormForUpdate(row) {
    row = row.substring(4, row.length - 2);
    row = row.split(",");
    let i = 0;
    for (const value in row) {
        headers[i].value = removeNonAlphaNumericChars(row[i]);
        rows[i] = removeNonAlphaNumericChars(row[i]);
        i += 1;
    }
    document.getElementById("popupFormupdate").style.display = "block";
}

function updateDataset() {
    const current_file_name = document.getElementById("current-file-name");

    let headers = document.querySelectorAll(".update-headers");

    let json_obj = {};
    for (let i = 0; i < headers.length; i++) {
        const [key, value] = [headers[i].id, headers[i].value];
        json_obj[key] = value;
    }

    fetch('/dataset-single?dataset=' + current_file_name.innerHTML + '&update=true', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      credentials: 'include',
      body: JSON.stringify(json_obj)
    })
      .then(response => response.json())
      .then(data => console.log(data))
      .catch(error => console.error(error));

    closeFormForUpdate();
}

function deleteRow(entry_uid) {
    const current_file_name = document.getElementById("current-file-name");

    fetch('/dataset-single?dataset=' + current_file_name.innerHTML + '&update=delete&entry_uid=' + entry_uid, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      credentials: 'include'
    })
      .then(response => response.json())
      .then(data => console.log(data))
      .catch(error => console.error(error));
}

function removeNonAlphaNumericChars(input) {
  const pattern = /[^a-zA-Z0-9äöü_]/g;
  return input.replace(pattern, '');
}

function closeFormForUpdate() {
    document.getElementById("popupFormupdate").style.display = "none";
}

function showCreateTicket() {
    const create_ticket_container = document.getElementById("create-ticket-container");
    const support_heading = document.getElementById("support-heading");

    // Clear every input field (We dont want values in them)!
    const text_inputs = document.querySelectorAll(".text-input");
    for (let i = 0; i < text_inputs.length; i++) {
      text_inputs[i].value = "";
    }

    switch (create_ticket_container.style.display) {

        case "block":
            support_heading.innerHTML = "Deine Supporttickets";
            create_ticket_container.classList.remove('visible');
            create_ticket_container.classList.add('hidden');

            create_ticket_container.style.display = "none";
            break;

        case "none":
            create_ticket_container.style.display = "block";
            support_heading.innerHTML = "Erstelle ein neues Ticket";

            create_ticket_container.classList.remove('hidden');
            create_ticket_container.classList.add('visible');
            break;

    }
}

function postTicket() {
    const ticket_name = document.getElementById("ticket-name").value;
    const ticket_short_desc = document.getElementById("ticket-short-desc").value;
    const ticket_desc = document.getElementById("ticket-desc").value;

    let ticketData = {
      "ticket-name": ticket_name,
      "ticket-short-desc": ticket_short_desc,
      "ticket-desc": ticket_desc
    };

    fetch('/tickets?ticket=open-new-ticket', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      credentials: 'include',
      body: JSON.stringify(ticketData)
    })
      .then(response => response.json())
      .then(data => console.log(data))
      .catch(error => console.error(error));

    try {
        document.getElementById("zero-elems").remove();
    }
    catch {
        // Hehe
    }

    showCreateTicket();

    // Add that thing
    var top_pos = document.getElementById("create-ticket-container");
    var new_data_box = '<div class="container-lg table-design">' +
    '<div class="row row-cols-1">' +
    '<div class="card shadow-sm p-3 mb-5 bg-white rounded">' +
    '<div class="card-header">' +
    '<img style="width: 22px; height: 22px;" src="../static/images/dataset.png" alt="icon">' +
    'Support' +
    '</div>' +
    '<div class="card-body">' +
    '<div class="status-container">' +
    '<h3 style="float: left;">Supportticket - ' + ticket_name + '</h3>' +
    '<button class="status-button red-button">In Bearbeitung</button>' +
    '</div>' +
    '<div>' +
    '<p style="font-size: 20px;">' + ticket_short_desc + '</p>' +
    '</div>' +
    '</div>' +
    '</div>' +
    '</div>' +
    '</div>';

    top_pos.insertAdjacentHTML("afterend", new_data_box);
}

let anzahl_spalten = 0;
var build_chart_link = "&spalte"
var chart_link = ""
function handle_add_spalte() {
    const spalten_select = document.getElementById("spalten-select");
    const spalten = document.getElementById("selector-for_spalten")

    if (anzahl_spalten < 2) {
        let new_spalte = '<div class="item"><p>' + spalten_select.value + '</p></div>';
        spalten.innerHTML += new_spalte;
        anzahl_spalten += 1;
        chart_link += build_chart_link + anzahl_spalten + '=' + spalten_select.value;
    }
}

function handle_add_pie_spalte() {
    const spalten_select = document.getElementById("pie-spalten-select");
    const spalten = document.getElementById("selector-for_pie-spalten")

    if (anzahl_spalten < 2) {
        let new_spalte = '<div class="item"><p>' + spalten_select.value + '</p></div>';
        spalten.innerHTML += new_spalte;
        anzahl_spalten += 1;
        chart_link += build_chart_link + anzahl_spalten + '=' + spalten_select.value;
    }
}

function HinzufügenAbbrechen() {
    const add_ds_container = document.getElementById("add-ds-container");

    //   Lösche alle Eingabefelder
    const text_inputs = document.getElementById("add-ds-container").querySelectorAll(".text-input");
    for (let i = 0; i < text_inputs.length; i++) {
      text_inputs[i].value = "";
    }


    switch (add_ds_container.style.display) {

        case "block":
            add_ds_container.classList.remove('visible');
            add_ds_container.classList.add('hidden');
            add_ds_container.style.display = "none";
            break;

        case "none":
            add_ds_container.style.display = "block";
            add_ds_container.classList.remove('hidden');
            add_ds_container.classList.add('visible');
            break;

    }
}

// Hinzufügen

function add_dataset() {
    let url = document.getElementById("ds-url").value;
    let desc = document.getElementById("ds-desc").value;

     fetch('/add_dataset', {
         method: 'POST',
         headers: {
             'Content-Type': 'application/json'
         },
         credentials: 'include',
         body: JSON.stringify({"url": url, "desc": desc})
     })
      .then(response => response.json())
      .then(data => console.log(data))
      .catch(error => console.error(error));

     HinzufügenAbbrechen();
}