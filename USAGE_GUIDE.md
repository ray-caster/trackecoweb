# TrackEco - Quick Usage Guide

## Getting Started

### Running the Application

```bash
# Navigate to project directory
cd trackecoweb

# Run the Flask application
python main.py

# Visit in browser
http://localhost:5000
```

## Quick Effect Examples

### 1. Adding Glassmorphism

```html
<!-- Basic glass card -->
<div class="glass-card">
    <h3>Card Title</h3>
    <p>Card content with glassmorphism effect</p>
</div>

<!-- Dark glass variant -->
<div class="glass-dark" style="padding: 2rem; border-radius: 20px;">
    <p style="color: white;">Dark glass content</p>
</div>

<!-- Light glass variant -->
<div class="glass-light" style="padding: 2rem; border-radius: 20px;">
    <p>Light glass content</p>
</div>
```

### 2. Adding Magnetic Effects

```html
<!-- Standard magnetic button -->
<button class="btn-modern magnetic">
    Click Me
</button>

<!-- Strong magnetic with 3D rotation -->
<button class="btn-modern magnetic-strong">
    Strong Effect
</button>

<!-- Magnetic text (each character moves) -->
<h1 class="magnetic-text">Interactive Title</h1>

<!-- Magnetic card -->
<div class="modern-card magnetic" style="padding: 2rem;">
    <h3>Card Title</h3>
    <p>This entire card follows your mouse</p>
</div>
```

### 3. Adding Parallax Effects

```html
<!-- Scroll-based parallax -->
<div class="parallax-layer" data-parallax="0.5">
    <!-- Content moves at 50% of scroll speed -->
    <img src="background.jpg" alt="Background">
</div>

<!-- Mouse-based parallax container -->
<div class="parallax-container" style="position: relative; height: 400px;">
    <div class="parallax-layer" data-depth="0.2">
        <img src="layer1.jpg" alt="Layer 1">
    </div>
    <div class="parallax-layer" data-depth="0.5">
        <img src="layer2.jpg" alt="Layer 2">
    </div>
</div>
```

### 4. Adding Scroll Animations

```html
<!-- Fade in on scroll -->
<div class="scroll-reveal">
    <h2>This fades in when you scroll to it</h2>
</div>

<!-- Pre-built animation classes -->
<div class="animate-fade-in">Fades in immediately</div>
<div class="animate-slide-in-left animate-delay-1">Slides from left with delay</div>
<div class="animate-slide-in-right animate-delay-2">Slides from right with delay</div>
<div class="animate-scale-in animate-delay-3">Scales in with delay</div>
```

### 5. Creating a Modern Button

```html
<!-- Basic modern button -->
<button class="btn-modern" style="background: var(--accent-color); color: white;">
    Click Me
</button>

<!-- Glass button -->
<button class="btn-glass btn-modern">
    Glass Button
</button>

<!-- Magnetic glass button (combines effects) -->
<button class="btn-glass btn-modern magnetic-strong">
    <i class="fas fa-rocket"></i> Launch
</button>
```

### 6. Creating Modern Cards

```html
<!-- Basic modern card -->
<div class="modern-card" style="padding: 2rem;">
    <h3>Card Title</h3>
    <p>Card content with hover effect</p>
</div>

<!-- Glass card with magnetic effect -->
<div class="glass-card magnetic">
    <h3>Interactive Glass Card</h3>
    <p>Hovers and follows mouse</p>
</div>
```

## Creating a New Page

### Template Structure

```html
{% extends "shared/base.html" %}

{% block title %}Your Page Title - TrackEco{% endblock %}
{% block description %}Page description for SEO{% endblock %}

{% block extra_css %}
<style>
    /* Your custom CSS here */
    .custom-section {
        padding: 5rem 0;
    }
</style>
{% endblock %}

{% block content %}
<section class="custom-section">
    <div class="container">
        <h1 class="magnetic-text">Your Title</h1>
        
        <!-- Your content -->
        <div class="glass-card magnetic scroll-reveal">
            <p>Content here</p>
        </div>
    </div>
</section>
{% endblock %}

{% block extra_js %}
<script>
    // Your custom JavaScript here
    document.addEventListener('DOMContentLoaded', () => {
        console.log('Page loaded!');
    });
</script>
{% endblock %}
```

### Adding Route in main.py

```python
@app.route("/your-page")
def your_page():
    return render_template("your_page.html")
```

## Common Patterns

### Hero Section with Parallax

```html
<div class="hero-section parallax-container" style="height: 60vh; position: relative;">
    <!-- Background with parallax -->
    <div class="parallax-layer" data-parallax="0.5" 
         style="background: url('hero.jpg'); background-size: cover;">
    </div>
    
    <!-- Overlay -->
    <div style="position: absolute; inset: 0; background: rgba(0,0,0,0.5);"></div>
    
    <!-- Content -->
    <div style="position: relative; z-index: 2; color: white; text-align: center; padding: 4rem 2rem;">
        <h1 class="magnetic-text animate-fade-in">Hero Title</h1>
        <p class="animate-fade-in animate-delay-1">Hero subtitle</p>
        <button class="btn-glass btn-modern magnetic-strong animate-delay-2">
            Get Started
        </button>
    </div>
</div>
```

### Grid of Cards

```html
<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 2rem;">
    <div class="glass-card magnetic scroll-reveal">
        <h3>Card 1</h3>
        <p>Content</p>
    </div>
    <div class="glass-card magnetic scroll-reveal">
        <h3>Card 2</h3>
        <p>Content</p>
    </div>
    <div class="glass-card magnetic scroll-reveal">
        <h3>Card 3</h3>
        <p>Content</p>
    </div>
</div>
```

### Statistics Section

```html
<section style="background: linear-gradient(135deg, var(--primary-color), var(--ecoBlue-color)); padding: 5rem 2rem; border-radius: 32px;">
    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 2rem;">
        <div class="glass-card magnetic" style="text-align: center; color: white;">
            <div style="font-size: 3rem; font-weight: 800; color: var(--accent-color);">
                1000+
            </div>
            <div>Items Collected</div>
        </div>
        <!-- More stat cards -->
    </div>
</section>
```

## Tips & Best Practices

### Performance
1. **Limit parallax elements**: Use 2-3 per section maximum
2. **Use magnetic effects sparingly**: Only on key interactive elements
3. **Lazy load images**: Add `loading="lazy"` to images
4. **Debounce scroll events**: Already handled in parallax.js

### Design
1. **Contrast for glass**: Use glass effects on contrasting backgrounds
2. **Consistency**: Stick to 2-3 effect types per page
3. **Hierarchy**: Use stronger effects for more important elements
4. **Spacing**: Give elements room to breathe (generous margins/padding)

### Accessibility
1. **Always include ARIA labels**: For screen readers
2. **Keyboard navigation**: Test with Tab key
3. **Color contrast**: Ensure text is readable
4. **Reduced motion**: Effects automatically respect user preferences

### Mobile
1. **Test on actual devices**: Not just browser resize
2. **Touch targets**: Minimum 44x44px for buttons
3. **Simplify on mobile**: Some effects auto-disable on mobile
4. **Test orientation**: Both portrait and landscape

## Troubleshooting

### Effects not working?

**Check:**
1. Is `effects.css` loaded?
   ```html
   <link rel="stylesheet" href="/static/css/effects.css">
   ```

2. Are JS files loaded?
   ```html
   <script src="/static/js/magnetic.js" defer></script>
   <script src="/static/js/parallax.js" defer></script>
   ```

3. Is the element visible on page?
4. Check browser console for errors (F12)

### Magnetic effect not working?

**Solutions:**
1. Ensure class is spelled correctly: `.magnetic`
2. Element must be visible and in viewport
3. Try `.magnetic-strong` for stronger effect
4. Check that element has some size (width/height)

### Parallax not smooth?

**Solutions:**
1. Keep data-parallax values between 0.1-0.8
2. Reduce number of parallax elements
3. Use CSS `will-change: transform` for performance
4. Check if images are too large (optimize them)

### Glass effect not showing?

**Solutions:**
1. Background must have content behind glass
2. Browser must support backdrop-filter (most modern browsers do)
3. Try different glass variants (`.glass-dark`, `.glass-light`)
4. Check element has padding/content

## CSS Variables

Available CSS variables you can use:

```css
:root {
    --primary-color: #231842;
    --accent-color: #F2C14E;
    --secondary-color: #E07A5F;
    --ecoGreen-color: #2e7d32;
    --ecoBlue-color: #1565c0;
    --white-color: #ffffff;
    --gray-800-color: #1f2937;
    --gray-700-color: #374151;
    --gray-400-color: #9ca3af;
}
```

**Usage:**
```css
.my-element {
    background: var(--accent-color);
    color: var(--primary-color);
}
```

## Advanced: Custom Magnetic Effect

```javascript
// Create custom magnetic strength
const customMagnetic = new MagneticEffect('.my-class', 0.7);

// Update strength dynamically
customMagnetic.updateStrength(0.5);

// Destroy effect
customMagnetic.destroy();
```

## Advanced: Custom Parallax

```javascript
// Create custom parallax
const customParallax = new SmoothParallax('[data-custom-parallax]');

// Clean up
customParallax.destroy();
```

## Need Help?

1. Check FEATURES.md for detailed documentation
2. Look at existing pages (news.html, timeline.html, calculator.html) for examples
3. Contact: hello@trackeco.org

---

Happy coding! 🚀

