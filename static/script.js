//sticky nav-bar
window.onscroll = function() {myFunction()};

var navbar = document.getElementById("nav");
var sticky = navbar.offsetTop;

function myFunction() {
  if (window.pageYOffset >= sticky) {
    navbar.classList.add("sticky")
  } else {
    navbar.classList.remove("sticky");
  }
}

//fade ins
var element = $("#first-container-text-container");
element.hide();
element.delay( 300 ).fadeIn( 1000 );

var element2 = $("#first-container-image");
element2.hide();
element2.delay( 500 ).fadeIn( 1500 );