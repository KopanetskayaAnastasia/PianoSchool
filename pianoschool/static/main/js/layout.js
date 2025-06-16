(function(){
    const burgerBtn = document.getElementById('burgerBtn');
    const menuDropdown = document.getElementById('menuDropdown');
    const burgerMenu = document.getElementById('burgerMenu');
    burgerBtn.addEventListener('click', function(e){
        e.stopPropagation();
        const isOpen = menuDropdown.classList.toggle('open');
        burgerBtn.setAttribute('aria-expanded', isOpen ? 'true' : 'false');
    });
    // Закрытие по клику вне меню
    document.addEventListener('click', function(e){
        if (!burgerMenu.contains(e.target)) {
            menuDropdown.classList.remove('open');
            burgerBtn.setAttribute('aria-expanded', 'false');
        }
    });
    // Закрытие по Esc
    document.addEventListener('keydown', function(e){
        if (e.key === "Escape") {
            menuDropdown.classList.remove('open');
            burgerBtn.setAttribute('aria-expanded', 'false');
        }
    });
})();