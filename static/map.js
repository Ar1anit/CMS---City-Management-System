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

