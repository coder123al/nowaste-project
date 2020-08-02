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

//back to top
var btt=document.getElementById("footer-text"),
    body=document.body,
    docElem=document.documentElement;
btt.addEventListener("click", function(event){
    event.preventDefault();
    docElem.scrollTop=0;
});