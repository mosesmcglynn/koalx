var nav = document.getElementById('topnav');
var navToggle = document.getElementById('toggle');

navToggle.addEventListener('click', function() {
    if (nav.className === 'navclose') {
        navToggle.className = 'open-nav-toggle';
        nav.className = 'navopen';

    } else {
        navToggle.className = 'close-nav-toggle';
        nav.className = 'navclose';
    }
})
