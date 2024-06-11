document.addEventListener('DOMContentLoaded', function () {
    const menuToggle = document.getElementById('menu-toggle');
    const navMenu = document.getElementById('nav-menu');
    const empresaButtons = document.querySelectorAll('.empresa-button');
    const empresaInfo = document.querySelector('.empresa-info p');

    menuToggle.addEventListener('click', function () {
        navMenu.classList.toggle('active');
    });

    empresaButtons.forEach(button => {
        button.addEventListener('click', function () {
            empresaInfo.textContent = button.getAttribute('data-text');
        });
    });
});
