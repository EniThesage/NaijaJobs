let toggle = document.querySelector('#toggleBtn');
let body = document.body;
let icon = document.querySelector('#themeIcon');

let darkMode = localStorage.getItem('darkTheme');

if (darkMode === 'true') {
    body.classList.add('dark-theme');
    icon.className = 'fa-solid fa-sun';
} else {
    icon.className = 'fa-solid fa-moon';
}

if (toggle) {
    toggle.addEventListener('click', () => {
        body.classList.toggle('dark-theme');

        let isDark = body.classList.contains('dark-theme');

        localStorage.setItem('darkTheme', isDark);

        if (isDark) {
            icon.className = 'fa-solid fa-sun';
        } else {
            icon.className = 'fa-solid fa-moon';
        }
    });
}


let hamburgerBtn = document.querySelector('#hamburgerBtn');
let navMenu = document.querySelector('#navMenu');
let hamburgerIcon = hamburgerBtn ? hamburgerBtn.querySelector('i') : null;

function closeNavMenu() {
    navMenu.classList.remove('active');
    hamburgerBtn.classList.remove('active');
    hamburgerBtn.setAttribute('aria-expanded', 'false');
    hamburgerIcon.className = 'fa-solid fa-bars';
}

if (hamburgerBtn && navMenu && hamburgerIcon) {
    hamburgerBtn.addEventListener('click', (event) => {
        event.stopPropagation();

        let isOpen = navMenu.classList.toggle('active');

        hamburgerBtn.classList.toggle('active', isOpen);
        hamburgerBtn.setAttribute('aria-expanded', isOpen);
        hamburgerIcon.className = isOpen ? 'fa-solid fa-xmark' : 'fa-solid fa-bars';
    });

    navMenu.querySelectorAll('a').forEach((link) => {
        link.addEventListener('click', closeNavMenu);
    });

    document.addEventListener('click', (event) => {
        let clickedInsideMenu = navMenu.contains(event.target) || hamburgerBtn.contains(event.target);

        if (!clickedInsideMenu && navMenu.classList.contains('active')) {
            closeNavMenu();
        }
    });
}

let errorMessages = document.getElementById('msg');

if (errorMessages && errorMessages.innerText.trim() !== '') {
    setTimeout(() => {
        errorMessages.style.opacity = '0';

        setTimeout(() => {
            errorMessages.style.display = 'none';
        }, 500);

    }, 3000);
}