// Main JavaScript for AI Affiliate Hub

document.addEventListener('DOMContentLoaded', function() {
    // Initialize all functionality
    initializeSearch();
    initializeFormValidation();
    initializeTooltips();
    initializeLoadingStates();
    initializeImageLazyLoading();
    initializeAnalytics();
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
            bootstrap.Dropdown.getInstance(dropdown.previousElementSibling)?.hide();
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

console.log('AI Affiliate Hub - JavaScript initialized successfully! 🚀');
