// ===== HAMBURGER MENU FUNCTIONALITY =====

document.addEventListener('DOMContentLoaded', function() {
    // Get DOM elements
    const hamburger = document.getElementById('hamburger');
    const mobileMenu = document.getElementById('mobileMenu');
    const overlay = document.getElementById('overlay');
    const closeBtn = document.getElementById('closeBtn');
    const body = document.body;
    const mobileNavLinks = document.querySelectorAll('.mobile-nav-link');

    // Check if elements exist
    if (!hamburger || !mobileMenu || !overlay || !closeBtn) {
        console.warn('Hamburger menu elements not found');
        return;
    }

    // Function to open mobile menu
    function openMobileMenu() {
        hamburger.classList.add('active');
        mobileMenu.classList.add('active');
        overlay.classList.add('active');
        body.classList.add('menu-open');
        
        // Add animation delay for menu items
        mobileNavLinks.forEach((link, index) => {
            link.style.transitionDelay = `${index * 0.1}s`;
        });
    }

    // Function to close mobile menu
    function closeMobileMenu() {
        hamburger.classList.remove('active');
        mobileMenu.classList.remove('active');
        overlay.classList.remove('active');
        body.classList.remove('menu-open');
        
        // Reset transition delays
        mobileNavLinks.forEach(link => {
            link.style.transitionDelay = '0s';
        });
    }

    // Function to toggle mobile menu
    function toggleMobileMenu() {
        if (mobileMenu.classList.contains('active')) {
            closeMobileMenu();
        } else {
            openMobileMenu();
        }
    }

    // Event Listeners
    hamburger.addEventListener('click', function(e) {
        e.preventDefault();
        e.stopPropagation();
        toggleMobileMenu();
    });

    closeBtn.addEventListener('click', function(e) {
        e.preventDefault();
        e.stopPropagation();
        closeMobileMenu();
    });

    overlay.addEventListener('click', function(e) {
        e.preventDefault();
        closeMobileMenu();
    });

    // Close menu when clicking on nav links
    mobileNavLinks.forEach(link => {
        link.addEventListener('click', function() {
            // Add small delay for better UX
            setTimeout(() => {
                closeMobileMenu();
            }, 200);
        });
    });

    // Close menu on ESC key
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape' && mobileMenu.classList.contains('active')) {
            closeMobileMenu();
        }
    });

    // Handle window resize
    window.addEventListener('resize', function() {
        // Close mobile menu if window becomes wide enough
        if (window.innerWidth > 768 && mobileMenu.classList.contains('active')) {
            closeMobileMenu();
        }
    });

    // Prevent menu from closing when clicking inside it
    mobileMenu.addEventListener('click', function(e) {
        e.stopPropagation();
    });

    // Add touch support for better mobile experience
    let touchStartX = 0;
    let touchEndX = 0;

    mobileMenu.addEventListener('touchstart', function(e) {
        touchStartX = e.changedTouches[0].screenX;
    });

    mobileMenu.addEventListener('touchend', function(e) {
        touchEndX = e.changedTouches[0].screenX;
        handleSwipeGesture();
    });

    function handleSwipeGesture() {
        const swipeThreshold = 50;
        const swipeDistance = touchEndX - touchStartX;
        
        // Swipe right to close menu
        if (swipeDistance > swipeThreshold) {
            closeMobileMenu();
        }
    }

    // Add loading animation
    function addLoadingEffect() {
        const navLinks = document.querySelectorAll('.mobile-nav-link');
        navLinks.forEach((link, index) => {
            link.style.opacity = '0';
            link.style.transform = 'translateX(20px)';
            
            setTimeout(() => {
                link.style.transition = 'all 0.3s ease';
                link.style.opacity = '1';
                link.style.transform = 'translateX(0)';
            }, index * 100);
        });
    }

    // Add smooth scroll to top when clicking logo in mobile menu
    const logoLinks = document.querySelectorAll('a[href*="halaman_utama"]');
    logoLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            if (window.location.pathname === '/') {
                e.preventDefault();
                window.scrollTo({
                    top: 0,
                    behavior: 'smooth'
                });
                if (mobileMenu.classList.contains('active')) {
                    closeMobileMenu();
                }
            }
        });
    });

    console.log('🍔 Hamburger menu initialized successfully!');
});