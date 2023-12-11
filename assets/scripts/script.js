var toggleNav = document.getElementById("toggleNav"),
    menu = document.getElementById("menu"),
    nav = document.getElementById("topnav");

toggleNav.addEventListener("click", function() {
    menu.classList.toggle("open");
    toggleNav.classList.toggle("open");
});

document.addEventListener("scroll", function() {
    window.scrollY > 50 ? nav.classList.add("scrolled") : nav.classList.remove("scrolled");
});

var cards = document.querySelectorAll(".cards");

cards.forEach(function(card) {
    card.addEventListener("mouseover", function() {
        var p = card.querySelector("p");
        p.classList.add("open");
    });
    card.addEventListener("mouseout", function() {
        var p = card.querySelector("p");
        p.classList.remove("open");
    });
});