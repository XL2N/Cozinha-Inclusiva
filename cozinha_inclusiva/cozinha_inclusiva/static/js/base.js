// Controla abertura/fechamento do menu mobile
document.addEventListener('DOMContentLoaded', function() {
    const navbarToggler = document.querySelector('.navbar-toggler');
    const navCollapse = document.getElementById('navbarContent');
    
    // Verifica se os elementos existem (podem não existir em páginas de login/cadastro)
    if (!navbarToggler || !navCollapse) {
        return;
    }
    
    const navLinks = document.querySelectorAll('.navbar-collapse .nav-link, .navbar-collapse .btn-login, .navbar-collapse .btn-logout');
    
    // Fecha o menu ao clicar em links de navegação
    if (navLinks.length > 0) {
        navLinks.forEach(function(link) {
            link.addEventListener('click', function(e) {
                if (window.innerWidth < 1200 && navCollapse.classList.contains('show')) {
                    // Usa o método nativo do Bootstrap para fechar
                    const bsCollapse = bootstrap.Collapse.getInstance(navCollapse);
                    if (bsCollapse) {
                        bsCollapse.hide();
                    }
                }
            });
        });
    }
    
    // Fecha o menu ao clicar fora dele
    document.addEventListener('click', function(event) {
        if (window.innerWidth < 1200 && navCollapse.classList.contains('show')) {
            const isClickInsideNav = navCollapse.contains(event.target);
            const isClickOnToggler = navbarToggler.contains(event.target);
            const isClickOnNavbarBrand = event.target.closest('.navbar-brand');
            
            // Fecha apenas se clicou fora do menu, do toggler e da logo
            if (!isClickInsideNav && !isClickOnToggler && !isClickOnNavbarBrand) {
                const bsCollapse = bootstrap.Collapse.getInstance(navCollapse);
                if (bsCollapse) {
                    bsCollapse.hide();
                }
            }
        }
    });
    
    // Fecha o menu ao pressionar ESC
    document.addEventListener('keydown', function(event) {
        if (event.key === 'Escape' && window.innerWidth < 1200 && navCollapse.classList.contains('show')) {
            const bsCollapse = bootstrap.Collapse.getInstance(navCollapse);
            if (bsCollapse) {
                bsCollapse.hide();
            }
        }
    });
});
