function checklogin() {

    const usernameInput = document.getElementById("email");
    const passwordInput = document.getElementById("password");
    const errorMail = document.getElementById("errorMail");
    const errorPass = document.getElementById("errorPass");

    const username = usernameInput.value;
    const password = passwordInput.value;
    // um Fehler zu Entfernen aber das Code hier ist nur für einmal fehler:
    /* usernameInput.addEventListener('input',function (){
          if(usernameInput.checkValidity()){
              errorMail.style.display = 'none';
          }
          else{
              errorMail.style.display ='block';
          }
      }); */
    function showError(errorMail) {
   /*     Ich versuchte hier bei neuen Anfang zu schreiben,dass rotes Fehler entfernt aber habe ich andere Methode danach erstellt
            while (errorMail.firstChild) {
            errorMail.removeChild(errorMail.firstChild);
        } */
        //Neuen Fehler erstellen und anzeigen
        const errorElement = document.createElement('errorMail');
        errorElement.textContent = errorMail;
        errorElement.style.color = 'red';
        errorMail.appendChild(errorElement);
    }

    if(username === 'GruppeB@SEP.de'){
        errorMail.innerHTML = "    ";
        if(password == '12345') {
            window.location.href = '2FA.html'
        }
        else{
            errorPass.innerHTML = "Password ist falsch";
            errorPass.style.color = "red";
        }
    }
    else{
        //   alert('Ihre E-Mail ist uns nicht bekannt, oder angegebenes Passwort ist falsch. Überprüfen Sie Ihre Angaben und versuchen Sie es erneut.');
        errorMail.innerHTML = "Ihre E-Mail ist uns nicht bekannt. Überprüfen Sie Ihre Angaben und versuchen Sie es erneut."
        errorMail.style.color = "red";
    }
}


