/**
 * Magnetic Elements Effect
 * Elements with .magnetic class will be attracted to cursor
 */

class MagneticEffect {
    constructor(selector = '.magnetic', strength = 0.15) {
        this.elements = document.querySelectorAll(selector);
        this.strength = strength;
        this.init();
    }

    init() {
        this.elements.forEach(element => {
            element.addEventListener('mousemove', (e) => this.handleMouseMove(e, element));
            element.addEventListener('mouseleave', () => this.handleMouseLeave(element));
        });
    }

    handleMouseMove(e, element) {
        const rect = element.getBoundingClientRect();
        const centerX = rect.left + rect.width / 2;
        const centerY = rect.top + rect.height / 2;
        
        const deltaX = (e.clientX - centerX) * this.strength;
        const deltaY = (e.clientY - centerY) * this.strength;
        
        element.style.transform = `translate(${deltaX}px, ${deltaY}px) scale(1.02)`;
    }

    handleMouseLeave(element) {
        element.style.transform = 'translate(0, 0) scale(1)';
    }

    updateStrength(newStrength) {
        this.strength = newStrength;
    }

    destroy() {
        this.elements.forEach(element => {
            element.style.transform = '';
        });
    }
}

// Strong magnetic effect for buttons and interactive elements
class StrongMagneticEffect extends MagneticEffect {
    constructor(selector = '.magnetic-strong') {
        super(selector, 0.25);
    }

    handleMouseMove(e, element) {
        const rect = element.getBoundingClientRect();
        const centerX = rect.left + rect.width / 2;
        const centerY = rect.top + rect.height / 2;
        
        const deltaX = (e.clientX - centerX) * this.strength;
        const deltaY = (e.clientY - centerY) * this.strength;
        
        // Add rotation for more dynamic effect
        const rotateX = ((e.clientY - centerY) / rect.height) * 5;
        const rotateY = ((e.clientX - centerX) / rect.width) * 5;
        
        element.style.transform = `
            translate(${deltaX}px, ${deltaY}px) 
            rotateX(${-rotateX}deg) 
            rotateY(${rotateY}deg) 
            scale(1.03)
        `;
    }

    handleMouseLeave(element) {
        element.style.transform = 'translate(0, 0) rotateX(0) rotateY(0) scale(1)';
    }
}

// Text magnetic effect - characters follow cursor
class TextMagneticEffect {
    constructor(selector = '.magnetic-text') {
        this.elements = document.querySelectorAll(selector);
        this.init();
    }

    init() {
        this.elements.forEach(element => {
            const text = element.textContent;
            element.innerHTML = '';
            
            text.split('').forEach(char => {
                const span = document.createElement('span');
                span.textContent = char === ' ' ? '\u00A0' : char;
                span.style.display = 'inline-block';
                span.style.transition = 'transform 0.2s ease';
                element.appendChild(span);
            });
            
            element.addEventListener('mousemove', (e) => this.handleMouseMove(e, element));
            element.addEventListener('mouseleave', () => this.handleMouseLeave(element));
        });
    }

    handleMouseMove(e, element) {
        const spans = element.querySelectorAll('span');
        const rect = element.getBoundingClientRect();
        
        spans.forEach(span => {
            const spanRect = span.getBoundingClientRect();
            const spanCenterX = spanRect.left + spanRect.width / 2;
            const spanCenterY = spanRect.top + spanRect.height / 2;
            
            const deltaX = (e.clientX - spanCenterX) * 0.05;
            const deltaY = (e.clientY - spanCenterY) * 0.05;
            
            span.style.transform = `translate(${deltaX}px, ${deltaY}px)`;
        });
    }

    handleMouseLeave(element) {
        const spans = element.querySelectorAll('span');
        spans.forEach(span => {
            span.style.transform = 'translate(0, 0)';
        });
    }
}

// Initialize on DOM load
if (typeof window !== 'undefined') {
    window.magneticEffect = null;
    window.strongMagneticEffect = null;
    window.textMagneticEffect = null;

    document.addEventListener('DOMContentLoaded', () => {
        window.magneticEffect = new MagneticEffect();
        window.strongMagneticEffect = new StrongMagneticEffect();
        window.textMagneticEffect = new TextMagneticEffect();
    });
}

// Export for module usage
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { MagneticEffect, StrongMagneticEffect, TextMagneticEffect };
}

