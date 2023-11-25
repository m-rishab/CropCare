/* ---------------- PRELOADER ---------------- */
let loader = document.querySelector('.preloader');

window.addEventListener('load', function() {
    loader.style.display = 'none';
})
/* ---------------- SCROLL TO TOP BUTTON CHANGE ---------------- */
function showScrollToTopBtn() {
    if (document.body.scrollTop > 400 || document.documentElement.scrollTop > 400) {
        document.getElementById('scrollTop').style.opacity = '1';
        document.getElementById('scrollTop').style.visibility = 'visible';
    } else {
        document.getElementById('scrollTop').style.opacity = '0';
        document.getElementById('scrollTop').style.visibility = 'hidden';
    }
}

window.addEventListener('scroll', showScrollToTopBtn);
/* ---------------- CHANGE HEADER ON SCROLL ---------------- */
let nav = document.querySelector('nav');

function changeHeader() {
    if (document.body.scrollTop > 150) {
        nav.classList.add('change-header');
    } else if (document.documentElement.scrollTop > 150) {
        nav.classList.add('change-header');
    } else {
        nav.classList.remove('change-header');
    }
}

window.addEventListener('scroll', changeHeader);

/* ---------------- TOGGLE NAVIGATION ---------------- */
let navigation = document.querySelector('nav');
let navMenu = document.querySelector('.nav-menu');
let navToggle = document.getElementById('nav-toggle');
let navClose = document.getElementById('nav-close');

function showNav() {
    navMenu.style.display = 'flex';
    navigation.style.height = '200px';
    navToggle.style.display = "none";
    navClose.style.display = 'block';
}
function hideNav() {
    navMenu.style.display = 'none';
    navigation.style.height = '80px';
    navToggle.style.display = "block";
    navClose.style.display = 'none';
}

/* HIDE NAV WHEN GO TO SECTION FOR SMALLER DEVICES */
let navLinks = document.querySelectorAll('.pages')
function removeNav() {
    if ($(window).width() < 880) {
        navMenu.style.display = 'none';
        navigation.style.height = '80px';
        navToggle.style.display = "block";
        navClose.style.display = 'none';
    }
}
navLinks.forEach(link => {
    link.addEventListener('click', removeNav);
})

/* ---------------- SWIPER ---------------- */
var swiper = new Swiper(".swiper", {
    loop: true,
    centeredSlides: 'true',
    slidesPerView: 3,
    spaceBetween: 20,
    pagination: {
      el: ".swiper-pagination",
      clickable: true,
      type: 'bullets',
    },
    navigation: {
        nextEl: '.swiper-button-next',
        prevEl: '.swiper-button-prev',
    }
    
});


/* ---------------- SCROLL TO ---------------- */
function scrollToTop() {
    window.scrollTo(0,0);
}
function scrollToAbout() {
    let about = document.getElementById('about');
    about.scrollIntoView()
}
/* ---------------- SCROLL REVEAL ---------------- */
const inViewport = (entries, observer) => {
    entries.forEach(entry => {
        entry.target.classList.toggle('is-inViewport', entry.isIntersecting);
    })
}

const Obs = new IntersectionObserver(inViewport);
const obsOptions = {};

const ELs_inViewport = document.querySelectorAll('[data-inViewport]');
ELs_inViewport.forEach(EL => {
    Obs.observe(EL, obsOptions);
});

      
/* ---------------- TOGGLE DAY/NIGHT MODE ---------------- */
let moon = document.getElementById('moon');
let sun = document.getElementById('sun');
let root = document.querySelector(':root');

function changeToDark() {
    moon.style.visibility = 'hidden';
    moon.style.opacity = '0';
    sun.style.visibility = 'visible';
    sun.style.opacity = '1';

    // CHANGE VALUES
    root.style.setProperty('--text-color', '#fff');
    root.style.setProperty('--bg-color', '#631413');
    root.style.setProperty('--dark-color', '#fea398');
    root.style.setProperty('--header-change-color', '#bd3c3ad7');
    root.style.setProperty('--hover-color', '#54cc25');
    root.style.setProperty('--bg-color-header', '#bd3c3ad3');
}


function changeToLight() {
    moon.style.visibility = 'visible';
    moon.style.opacity = '1';
    sun.style.visibility = 'hidden';
    sun.style.opacity = '0';

    // REVERT VALUES
    root.style.setProperty('--text-color', '#000');
    root.style.setProperty('--bg-color', '#b3ffa2');
    root.style.setProperty('--dark-color', '#095000');
    root.style.setProperty('--header-change-color', '#b8eba6d7');
    root.style.setProperty('--hover-color', '#bb3333');
    root.style.setProperty('--bg-color-header', '#b3ffa2d3');
}