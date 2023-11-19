var toggleNav = document.getElementById("toggleNav");
var menu = document.getElementById("menu");
var nav = document.getElementById("topnav");

toggleNav.addEventListener("click", function() {
    menu.classList.toggle("open");
    toggleNav.classList.toggle("open");
});

document.addEventListener("scroll", function() {
    window.scrollY > 50 ? nav.classList.add("scrolled") : nav.classList.remove("scrolled");
});
