// Complete Main JavaScript for AI Affiliate Hub with Sliding Sections

document.addEventListener('DOMContentLoaded', function() {
    // Initialize all functionality
    initializeSearch();
    initializeFormValidation();
    initializeTooltips();
    initializeLoadingStates();
    initializeImageLazyLoading();
    initializeAnalytics();
    initializeSectionsSlider(); // New sliding sections functionality
});

// Search functionality
function initializeSearch() {
    const searchForm = document.querySelector('form[action*="search"]');
    if (searchForm) {
        const searchInput = searchForm.querySelector('input[name="q"]');
        
        // Add search suggestions (simple implementation)
        searchInput.addEventListener('input', function() {
            const query = this.value.toLowerCase();
            if (query.length > 2) {
                // Could implement autocomplete here
                console.log('Searching for:', query);
            }
        });
        
        // Prevent empty searches
        searchForm.addEventListener('submit', function(e) {
            const query = searchInput.value.trim();
            if (!query) {
                e.preventDefault();
                searchInput.focus();
                showAlert('Please enter a search term', 'warning');
            }
        });
    }
}

// Form validation and enhancement
function initializeFormValidation() {
    const forms = document.querySelectorAll('form');
    
    forms.forEach(form => {
        // Add Bootstrap validation classes
        form.addEventListener('submit', function(e) {
            if (!form.checkValidity()) {
                e.preventDefault();
                e.stopPropagation();
            } else {
                // Show loading state for submit buttons
                const submitBtn = form.querySelector('button[type="submit"]');
                if (submitBtn) {
                    submitBtn.classList.add('loading');
                    submitBtn.disabled = true;
                }
            }
            form.classList.add('was-validated');
        });
        
        // Real-time validation for required fields
        const requiredFields = form.querySelectorAll('[required]');
        requiredFields.forEach(field => {
            field.addEventListener('blur', function() {
                if (this.value.trim() === '') {
                    this.classList.add('is-invalid');
                } else {
                    this.classList.remove('is-invalid');
                    this.classList.add('is-valid');
                }
            });
        });
        
        // URL validation for affiliate links
        const urlFields = form.querySelectorAll('input[type="url"]');
        urlFields.forEach(field => {
            field.addEventListener('blur', function() {
                if (this.value && !isValidUrl(this.value)) {
                    this.classList.add('is-invalid');
                    showAlert('Please enter a valid URL', 'warning');
                } else if (this.value) {
                    this.classList.remove('is-invalid');
                    this.classList.add('is-valid');
                }
            });
        });
    });
}

// Initialize tooltips
function initializeTooltips() {
    // Add tooltips to affiliate links
    const affiliateLinks = document.querySelectorAll('a[target="_blank"][rel*="nofollow"]');
    affiliateLinks.forEach(link => {
        link.setAttribute('title', 'Affiliate link - opens in new tab');
        link.setAttribute('data-bs-toggle', 'tooltip');
    });
    
    // Initialize Bootstrap tooltips if available
    if (typeof bootstrap !== 'undefined' && bootstrap.Tooltip) {
        const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
        tooltipTriggerList.map(function (tooltipTriggerEl) {
            return new bootstrap.Tooltip(tooltipTriggerEl);
        });
    }
}

// Loading states for buttons and forms
function initializeLoadingStates() {
    // Add loading states to CTA buttons
    const ctaButtons = document.querySelectorAll('.btn-primary[href*="http"]');
    ctaButtons.forEach(button => {
        button.addEventListener('click', function() {
            this.classList.add('loading');
            setTimeout(() => {
                this.classList.remove('loading');
            }, 2000);
        });
    });
}

// Lazy loading for images
function initializeImageLazyLoading() {
    const images = document.querySelectorAll('img[src]');
    
    if ('IntersectionObserver' in window) {
        const imageObserver = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    img.classList.add('fade-in');
                    observer.unobserve(img);
                }
            });
        });
        
        images.forEach(img => {
            imageObserver.observe(img);
        });
    }
}

// Basic analytics tracking
function initializeAnalytics() {
    // Track affiliate link clicks
    const affiliateLinks = document.querySelectorAll('a[href*="amazon"], a[href*="flipkart"], a[target="_blank"][rel*="nofollow"]');
    affiliateLinks.forEach(link => {
        link.addEventListener('click', function() {
            const productName = document.querySelector('h1')?.textContent || 'Unknown Product';
            console.log('Affiliate link clicked:', {
                product: productName,
                url: this.href,
                timestamp: new Date().toISOString()
            });
            
            // Could send to analytics service here
            // Example: gtag('event', 'affiliate_click', { product_name: productName });
        });
    });
    
    // Track search queries
    const searchForms = document.querySelectorAll('form[action*="search"]');
    searchForms.forEach(form => {
        form.addEventListener('submit', function() {
            const query = form.querySelector('input[name="q"]')?.value;
            if (query) {
                console.log('Search performed:', {
                    query: query,
                    timestamp: new Date().toISOString()
                });
            }
        });
    });
}

// NEW: Sections Sliding Bar JavaScript
function initializeSectionsSlider() {
    const sectionsContainer = document.getElementById('sectionsContainer');
    const scrollLeftBtn = document.querySelector('.scroll-left');
    const scrollRightBtn = document.querySelector('.scroll-right');
    
    if (!sectionsContainer) return;
    
    const scrollAmount = 200; // pixels to scroll
    let isScrolling = false;
    
    // Function to update button visibility
    function updateButtonVisibility() {
        const container = sectionsContainer;
        const maxScrollLeft = container.scrollWidth - container.clientWidth;
        
        // Show/hide left button
        if (container.scrollLeft <= 0) {
            if (scrollLeftBtn) scrollLeftBtn.style.display = 'none';
        } else {
            if (scrollLeftBtn) scrollLeftBtn.style.display = 'flex';
        }
        
        // Show/hide right button
        if (container.scrollLeft >= maxScrollLeft) {
            if (scrollRightBtn) scrollRightBtn.style.display = 'none';
        } else {
            if (scrollRightBtn) scrollRightBtn.style.display = 'flex';
        }
        
        // If no scrolling is needed, hide both buttons
        if (maxScrollLeft <= 0) {
            if (scrollLeftBtn) scrollLeftBtn.style.display = 'none';
            if (scrollRightBtn) scrollRightBtn.style.display = 'none';
        }
    }
    
    // Smooth scroll function
    function smoothScroll(element, target, duration) {
        const start = element.scrollLeft;
        const change = target - start;
        const startTime = performance.now();
        
        function animateScroll(currentTime) {
            const elapsed = currentTime - startTime;
            const progress = Math.min(elapsed / duration, 1);
            
            // Easing function (ease-out)
            const easing = 1 - Math.pow(1 - progress, 3);
            element.scrollLeft = start + (change * easing);
            
            if (progress < 1) {
                requestAnimationFrame(animateScroll);
            } else {
                isScrolling = false;
                updateButtonVisibility();
            }
        }
        
        isScrolling = true;
        requestAnimationFrame(animateScroll);
    }
    
    // Scroll left button click
    if (scrollLeftBtn) {
        scrollLeftBtn.addEventListener('click', function() {
            if (isScrolling) return;
            
            const newScrollLeft = Math.max(0, sectionsContainer.scrollLeft - scrollAmount);
            smoothScroll(sectionsContainer, newScrollLeft, 300);
            
            // Add click animation
            this.style.transform = 'scale(0.9)';
            setTimeout(() => {
                this.style.transform = '';
            }, 150);
        });
    }
    
    // Scroll right button click
    if (scrollRightBtn) {
        scrollRightBtn.addEventListener('click', function() {
            if (isScrolling) return;
            
            const maxScrollLeft = sectionsContainer.scrollWidth - sectionsContainer.clientWidth;
            const newScrollLeft = Math.min(maxScrollLeft, sectionsContainer.scrollLeft + scrollAmount);
            smoothScroll(sectionsContainer, newScrollLeft, 300);
            
            // Add click animation
            this.style.transform = 'scale(0.9)';
            setTimeout(() => {
                this.style.transform = '';
            }, 150);
        });
    }
    
    // Handle scroll events to update button visibility
    sectionsContainer.addEventListener('scroll', function() {
        if (!isScrolling) {
            updateButtonVisibility();
        }
    });
    
    // Handle window resize
    window.addEventListener('resize', function() {
        updateButtonVisibility();
    });
    
    // Handle mouse wheel scrolling on sections container
    sectionsContainer.addEventListener('wheel', function(e) {
        if (Math.abs(e.deltaX) > Math.abs(e.deltaY)) {
            // Horizontal scrolling
            return;
        }
        
        // Convert vertical scroll to horizontal
        if (e.deltaY !== 0) {
            e.preventDefault();
            const scrollDirection = e.deltaY > 0 ? 1 : -1;
            const newScrollLeft = this.scrollLeft + (scrollDirection * 100);
            
            smoothScroll(this, Math.max(0, Math.min(this.scrollWidth - this.clientWidth, newScrollLeft)), 200);
        }
    }, { passive: false });
    
    // Touch/swipe support for mobile
    let startX = 0;
    let startScrollLeft = 0;
    let isDragging = false;
    
    sectionsContainer.addEventListener('touchstart', function(e) {
        startX = e.touches[0].clientX;
        startScrollLeft = this.scrollLeft;
        isDragging = true;
    }, { passive: true });
    
    sectionsContainer.addEventListener('touchmove', function(e) {
        if (!isDragging) return;
        
        const currentX = e.touches[0].clientX;
        const diffX = startX - currentX;
        this.scrollLeft = startScrollLeft + diffX;
    }, { passive: true });
    
    sectionsContainer.addEventListener('touchend', function() {
        isDragging = false;
        updateButtonVisibility();
    }, { passive: true });
    
    // Keyboard navigation for sections
    document.addEventListener('keydown', function(e) {
        if (document.activeElement.classList.contains('section-link')) {
            if (e.key === 'ArrowLeft' || e.key === 'ArrowRight') {
                e.preventDefault();
                
                const currentLink = document.activeElement;
                const allLinks = Array.from(document.querySelectorAll('.section-link'));
                const currentIndex = allLinks.indexOf(currentLink);
                
                let nextIndex;
                if (e.key === 'ArrowLeft') {
                    nextIndex = currentIndex > 0 ? currentIndex - 1 : allLinks.length - 1;
                } else {
                    nextIndex = currentIndex < allLinks.length - 1 ? currentIndex + 1 : 0;
                }
                
                const nextLink = allLinks[nextIndex];
                nextLink.focus();
                
                // Scroll to make the focused link visible
                const linkRect = nextLink.getBoundingClientRect();
                const containerRect = sectionsContainer.getBoundingClientRect();
                
                if (linkRect.left < containerRect.left) {
                    const scrollTarget = sectionsContainer.scrollLeft - (containerRect.left - linkRect.left) - 20;
                    smoothScroll(sectionsContainer, Math.max(0, scrollTarget), 200);
                } else if (linkRect.right > containerRect.right) {
                    const scrollTarget = sectionsContainer.scrollLeft + (linkRect.right - containerRect.right) + 20;
                    smoothScroll(sectionsContainer, scrollTarget, 200);
                }
            }
        }
    });
    
    // Auto-scroll to active section on page load
    function scrollToActiveSection() {
        const activeSection = document.querySelector('.section-link.active');
        if (activeSection) {
            setTimeout(() => {
                const linkRect = activeSection.getBoundingClientRect();
                const containerRect = sectionsContainer.getBoundingClientRect();
                
                // Calculate scroll position to center the active section
                const linkCenter = activeSection.offsetLeft + (activeSection.offsetWidth / 2);
                const containerCenter = sectionsContainer.clientWidth / 2;
                const scrollTarget = linkCenter - containerCenter;
                
                smoothScroll(sectionsContainer, Math.max(0, scrollTarget), 500);
            }, 100);
        }
    }
    
    // Initial setup
    updateButtonVisibility();
    scrollToActiveSection();
    
    // Add loading animation to section links
    const sectionLinks = document.querySelectorAll('.section-link');
    sectionLinks.forEach((link, index) => {
        link.style.animationDelay = `${index * 0.1}s`;
        
        // Add hover effects
        link.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-2px) scale(1.02)';
        });
        
        link.addEventListener('mouseleave', function() {
            this.style.transform = '';
        });
    });
}

// Utility functions
function isValidUrl(string) {
    try {
        new URL(string);
        return true;
    } catch (_) {
        return false;
    }
}

function showAlert(message, type = 'info') {
    // Create and show a Bootstrap alert
    const alertContainer = document.querySelector('.container');
    if (alertContainer) {
        const alertElement = document.createElement('div');
        alertElement.className = `alert alert-${type} alert-dismissible fade show mt-3`;
        alertElement.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;
        
        alertContainer.insertBefore(alertElement, alertContainer.firstChild);
        
        // Auto-dismiss after 5 seconds
        setTimeout(() => {
            if (alertElement.parentNode) {
                alertElement.remove();
            }
        }, 5000);
    }
}

// Smooth scrolling for anchor links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});

// Back to top functionality
function addBackToTop() {
    const backToTopButton = document.createElement('button');
    backToTopButton.innerHTML = '<i data-feather="arrow-up"></i>';
    backToTopButton.className = 'btn btn-primary position-fixed';
    backToTopButton.style.cssText = 'bottom: 20px; right: 20px; z-index: 1000; border-radius: 50%; width: 50px; height: 50px; display: none;';
    backToTopButton.setAttribute('aria-label', 'Back to top');
    
    document.body.appendChild(backToTopButton);
    
    // Show/hide button based on scroll position
    window.addEventListener('scroll', function() {
        if (window.pageYOffset > 300) {
            backToTopButton.style.display = 'block';
        } else {
            backToTopButton.style.display = 'none';
        }
    });
    
    // Scroll to top when clicked
    backToTopButton.addEventListener('click', function() {
        window.scrollTo({
            top: 0,
            behavior: 'smooth'
        });
    });
    
    // Reinitialize Feather icons for the new button
    if (typeof feather !== 'undefined') {
        feather.replace();
    }
}

// Initialize back to top button
addBackToTop();

// Performance optimization: Debounce function
function debounce(func, wait, immediate) {
    let timeout;
    return function executedFunction() {
        const context = this;
        const args = arguments;
        const later = function() {
            timeout = null;
            if (!immediate) func.apply(context, args);
        };
        const callNow = immediate && !timeout;
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
        if (callNow) func.apply(context, args);
    };
}

// Optimize scroll events
const optimizedScrollHandler = debounce(function() {
    // Any scroll-based functionality can go here
}, 100);

window.addEventListener('scroll', optimizedScrollHandler);

// Handle offline/online status
window.addEventListener('online', function() {
    showAlert('Connection restored!', 'success');
});

window.addEventListener('offline', function() {
    showAlert('You are currently offline. Some features may not work.', 'warning');
});

// Keyboard navigation improvements
document.addEventListener('keydown', function(e) {
    // ESC key to close modals/dropdowns
    if (e.key === 'Escape') {
        const openDropdowns = document.querySelectorAll('.dropdown-menu.show');
        openDropdowns.forEach(dropdown => {
            if (typeof bootstrap !== 'undefined' && bootstrap.Dropdown) {
                bootstrap.Dropdown.getInstance(dropdown.previousElementSibling)?.hide();
            }
        });
    }
    
    // Ctrl/Cmd + K to focus search
    if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
        e.preventDefault();
        const searchInput = document.querySelector('input[name="q"]');
        if (searchInput) {
            searchInput.focus();
        }
    }
});

// Optimized resize handler for sections slider
window.addEventListener('resize', debounce(function() {
    const sectionsContainer = document.getElementById('sectionsContainer');
    if (sectionsContainer) {
        // Re-initialize sections slider visibility if needed
        setTimeout(() => {
            const scrollLeftBtn = document.querySelector('.scroll-left');
            const scrollRightBtn = document.querySelector('.scroll-right');
            
            if (scrollLeftBtn && scrollRightBtn) {
                // Update button visibility
                const maxScrollLeft = sectionsContainer.scrollWidth - sectionsContainer.clientWidth;
                
                if (sectionsContainer.scrollLeft <= 0) {
                    scrollLeftBtn.style.display = 'none';
                } else {
                    scrollLeftBtn.style.display = 'flex';
                }
                
                if (sectionsContainer.scrollLeft >= maxScrollLeft || maxScrollLeft <= 0) {
                    scrollRightBtn.style.display = 'none';
                } else {
                    scrollRightBtn.style.display = 'flex';
                }
            }
        }, 100);
    }
}, 250));

console.log('AI Affiliate Hub - Complete JavaScript initialized successfully! 🚀');