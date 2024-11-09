
function admin_reg() {
    const birthdateWrapper = document.getElementById("Birthdate");
    const profilepicWrapper = document.querySelector('#ProfilePic').parentNode;
    const loginButton = document.getElementById("login");
    const isAdmin1 = document.querySelector('input[type="checkbox"]').checked;
    if (!isAdmin1) {
        birthdateInput.setAttribute("required", true);
    } else {
        birthdateInput.removeAttribute("required");
    }
    if (document.querySelector('input[type="checkbox"]').checked) {
        birthdateWrapper.style.display = "none"
        birthdateWrapper.classList = "fadeIn first"
        birthdateWrapper.style.marginLeft = "33px";
        profilepicWrapper.style.display = "none"
        profilepicWrapper.classList = "fadeIn second"
        loginButton.value = "admin";
    } else {
        birthdateWrapper.style.display = "block"
        profilepicWrapper.style.display = "block"
        loginButton.value = "user";
    }

}




function naechsteSeite(){
    const vorName = document.getElementById('Firstname').value;
    const nachName = document.getElementById('Lastname').value;
    const email = document.getElementById('email').value;
    const pass = document.getElementById('psw').value;
    const isAdmin = document.querySelector('input[type="checkbox"]').checked;
    if (isAdmin) {
        if (vorName.length > 0 && nachName.length > 0 && email.length > 0 && pass.length > 0) {
            return true;
        } else {
            return false;
        }
    } else {
        const geburstDatum = document.getElementById('Birthdate').value;
        if (vorName.length > 0 && nachName.length > 0 && geburstDatum.length > 0 && email.length > 0 && pass.length > 0) {
            return true;
        } else {
            return false;
        }
    }

        }
