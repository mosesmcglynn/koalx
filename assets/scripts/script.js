var toggleNav = document.getElementById("toggleNav");
var menu = document.getElementById("menu");
var nav = document.getElementById("topnav");

toggleNav.addEventListener("click", function() {
    menu.classList.toggle("open");
    toggleNav.classList.toggle("open");
});

document.addEventListener("scroll", function(e) {
    if (window.scrollY > 100) {
        nav.classList.add("scrolled");
    }else{
        nav.classList.remove("scrolled");
    }
});
