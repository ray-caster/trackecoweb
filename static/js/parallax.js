/**
 * Parallax Effect
 * Creates depth and motion based on scroll and mouse movement
 */

class ParallaxScroll {
    constructor(selector = '.parallax-layer', speed = 0.5) {
        this.elements = document.querySelectorAll(selector);
        this.speed = speed;
        this.ticking = false;
        this.init();
    }

    init() {
        window.addEventListener('scroll', () => this.handleScroll());
        this.handleScroll(); // Initial position
    }

    handleScroll() {
        if (!this.ticking) {
            window.requestAnimationFrame(() => {
                this.update();
                this.ticking = false;
            });
            this.ticking = true;
        }
    }

    update() {
        const scrollY = window.pageYOffset;
        
        this.elements.forEach(element => {
            const speed = element.dataset.speed || this.speed;
            const yPos = -(scrollY * speed);
            element.style.transform = `translate3d(0, ${yPos}px, 0)`;
        });
    }

    destroy() {
        window.removeEventListener('scroll', this.handleScroll);
    }
}

class ParallaxMouse {
    constructor(containerSelector = '.parallax-container') {
        this.containers = document.querySelectorAll(containerSelector);
        this.ticking = false;
        this.init();
    }

    init() {
        this.containers.forEach(container => {
            container.addEventListener('mousemove', (e) => this.handleMouseMove(e, container));
            container.addEventListener('mouseleave', () => this.handleMouseLeave(container));
        });
    }

    handleMouseMove(e, container) {
        if (!this.ticking) {
            window.requestAnimationFrame(() => {
                this.update(e, container);
                this.ticking = false;
            });
            this.ticking = true;
        }
    }

    update(e, container) {
        const rect = container.getBoundingClientRect();
        const x = (e.clientX - rect.left) / rect.width - 0.5;
        const y = (e.clientY - rect.top) / rect.height - 0.5;
        
        const layers = container.querySelectorAll('.parallax-layer');
        
        layers.forEach((layer, index) => {
            const depth = layer.dataset.depth || (index + 1) * 0.1;
            const moveX = x * depth * 100;
            const moveY = y * depth * 100;
            
            layer.style.transform = `translate3d(${moveX}px, ${moveY}px, 0)`;
        });
    }

    handleMouseLeave(container) {
        const layers = container.querySelectorAll('.parallax-layer');
        layers.forEach(layer => {
            layer.style.transform = 'translate3d(0, 0, 0)';
        });
    }

    destroy() {
        this.containers.forEach(container => {
            const layers = container.querySelectorAll('.parallax-layer');
            layers.forEach(layer => {
                layer.style.transform = '';
            });
        });
    }
}

// Advanced parallax with smooth interpolation
class SmoothParallax {
    constructor(selector = '[data-parallax]') {
        this.elements = document.querySelectorAll(selector);
        this.scrollY = window.pageYOffset;
        this.targetY = this.scrollY;
        this.ease = 0.1;
        this.isRunning = false;
        this.init();
    }

    init() {
        window.addEventListener('scroll', () => {
            this.targetY = window.pageYOffset;
            if (!this.isRunning) {
                this.isRunning = true;
                this.animate();
            }
        });
        
        // Set initial positions
        this.update();
    }

    animate() {
        this.scrollY += (this.targetY - this.scrollY) * this.ease;
        
        if (Math.abs(this.targetY - this.scrollY) > 0.5) {
            this.update();
            requestAnimationFrame(() => this.animate());
        } else {
            this.scrollY = this.targetY;
            this.update();
            this.isRunning = false;
        }
    }

    update() {
        this.elements.forEach(element => {
            const speed = parseFloat(element.dataset.parallax) || 0.5;
            const rect = element.getBoundingClientRect();
            const elementTop = rect.top + this.scrollY;
            const elementHeight = rect.height;
            const windowHeight = window.innerHeight;
            
            // Only apply parallax if element is in viewport
            if (elementTop < this.scrollY + windowHeight && elementTop + elementHeight > this.scrollY) {
                const progress = (this.scrollY - elementTop + windowHeight) / (windowHeight + elementHeight);
                const translateY = (progress - 0.5) * speed * 100;
                
                element.style.transform = `translate3d(0, ${translateY}px, 0)`;
            }
        });
    }

    destroy() {
        this.elements.forEach(element => {
            element.style.transform = '';
        });
    }
}

// Scroll reveal animation
class ScrollReveal {
    constructor(selector = '.scroll-reveal', options = {}) {
        this.elements = Array.from(document.querySelectorAll(selector));
        this.options = {
            threshold: options.threshold || 0.15,
            rootMargin: options.rootMargin || '0px',
            ...options
        };
        this.init();
    }

    init() {
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('revealed');
                    if (this.options.once !== false) {
                        observer.unobserve(entry.target);
                    }
                }
            });
        }, this.options);

        this.elements.forEach(element => observer.observe(element));
    }
}

// Initialize on DOM load
if (typeof window !== 'undefined') {
    window.parallaxScroll = null;
    window.parallaxMouse = null;
    window.smoothParallax = null;
    window.scrollReveal = null;

    document.addEventListener('DOMContentLoaded', () => {
        window.parallaxScroll = new ParallaxScroll();
        window.parallaxMouse = new ParallaxMouse();
        window.smoothParallax = new SmoothParallax();
        window.scrollReveal = new ScrollReveal();
    });
}

// Export for module usage
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { ParallaxScroll, ParallaxMouse, SmoothParallax, ScrollReveal };
}

