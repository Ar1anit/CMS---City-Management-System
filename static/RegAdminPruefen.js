function emailPruefen() {
    var email = document.getElementById("email").value;
    var pass = document.getElementById('psw').value;

    if(email.length===0) {
        alert("Sie haben keine E-Mail eingegeben");
        return;
    }
    if(pass.length===0){
        alert("Füllen Sie alle Fenster aus")

    }
    if (email.includes('@')) {
        if(pruefen(pass) === false){
            alert("Passwort ist weniger als 8 Symbole");
            return;
        }
        else if (naechsteSeite()==true){
            alert("Daten werden gespeichert");
            window.location.href = 'Login.html';
        }
        else if (naechsteSeite()==false){
            alert("Sie haben nicht alle felder ausgefüllt");
        }
    }
    else {
        alert("E-mails Format ist falsch, überprüfen Sie, ob Ihr Email (@) beinhaltet und versuchen es erneut")
    }
}
function pruefen(passwordein) {
    if (passwordein.length >= 8) {
        return true;
    }
    return false;
}

function naechsteSeite(){
    const vorName = document.getElementById('Firstname').value;
    const nachName = document.getElementById('Lastname').value;
    if(vorName.length > 0  && nachName.length > 0){
        return true;
    }
    else{
        return false;
    }
}
