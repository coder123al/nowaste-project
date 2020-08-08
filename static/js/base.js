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

//nav-responsive
const navSlide = () => {
  const burger = document.querySelector(".burger");
  const nav = document.querySelector(".nav-links");
  burger.addEventListener('click',()=>{
      nav.classList.toggle('nav-active');
      burger.classList.toggle('toggle');
      nav.classList.toggle('toggle');
  });
}

navSlide();

//back to top
var btt=document.getElementById("footer-text"),
    body=document.body,
    docElem=document.documentElement;
btt.addEventListener("click", function(event){
    event.preventDefault();
    docElem.scrollTop=0;
});