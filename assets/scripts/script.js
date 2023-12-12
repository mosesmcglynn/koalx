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

// gallery

var gallery = document.querySelectorAll('.gallery .galleryimg'),
    galleryslider = document.querySelector('.gallery-slider'),
    images = document.querySelectorAll('.gallery-slider .galleryimg'),
    prevbtn = document.querySelector('.nav-button.prev'),
    nextbtn = document.querySelector('.nav-button.next'),
    exitbtn = document.querySelector('.exit');

var currentIndex = 0;

function updateButtons(currentIndex) {
    prevbtn.style.visibility = currentIndex > 0 ? 'visible' : 'hidden';
    nextbtn.style.visibility = currentIndex < images.length - 1 ? 'visible' : 'hidden';
}

gallery.forEach(function(img, index) {
    img.addEventListener('click', function() {
        galleryslider.classList.toggle('open');
        images[index].classList.add('active');
        currentIndex = index;
        updateButtons(currentIndex);
    });
});
    
images[currentIndex].classList.add('active');

prevbtn.addEventListener('click', function() {
    images[currentIndex].classList.remove('active');
    currentIndex = (currentIndex - 1 + images.length) % images.length;
    updateButtons(currentIndex);
    images[currentIndex].classList.add('active');
});

nextbtn.addEventListener('click', function() {
    images[currentIndex].classList.remove('active');
    currentIndex = (currentIndex + 1) % images.length;
    updateButtons(currentIndex);
    images[currentIndex].classList.add('active');
});

exitbtn.addEventListener('click', function() {
    document.querySelector('.gallery-slider').classList.toggle('open');
    images[currentIndex].classList.remove('active');
});

updateButtons(currentIndex);