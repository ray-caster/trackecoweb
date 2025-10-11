# TrackEco - New Features Documentation

## Overview
This document describes the new multi-page architecture and modern UI effects implemented for the TrackEco website.

## New Pages Created

### 1. Latest News Page (`/news`)
A dynamic news page featuring:
- **Glassmorphism Effects**: Modern glass-like cards with backdrop blur
- **Featured News Section**: Hero-style featured article with parallax background
- **Category Filtering**: Filter news by Partnership, Events, Impact, and Innovation
- **Magnetic Effects**: Interactive cards that respond to mouse movement
- **Newsletter Subscription**: Email signup with glass effect design
- **Responsive Grid Layout**: Adapts to all screen sizes

**Features:**
- News cards with hover animations
- Category badges with color coding
- Read time estimates
- Smooth filtering transitions
- Glass morphism design throughout

### 2. Interactive Timeline Page (`/timeline`)
An immersive timeline showcasing TrackEco's journey:
- **Parallax Scrolling**: Background elements move at different speeds
- **Animated Timeline**: Progress bar that fills as you scroll
- **Glass Cards**: Milestone cards with glassmorphism effects
- **Magnetic Timeline Dots**: Interactive dots that pulse on hover
- **Statistics Display**: Impact metrics for each milestone
- **Floating Parallax Shapes**: Decorative elements that respond to mouse movement
- **Year Markers**: Visual separation of different time periods

**Features:**
- Alternating left/right layout
- Scroll-triggered animations
- Interactive hover effects
- Real-time progress tracking
- Stats overview section with animated counters

### 3. Impact Calculator Page (`/calculator`)
A comprehensive calculator with multiple modes:
- **Four Calculation Modes**:
  1. **Plastic Recycling**: Calculate by weight (kg)
  2. **Bottle Count**: Calculate by number of bottles
  3. **Time-Based**: Calculate over time periods
  4. **Community Impact**: Calculate collective impact

**Features:**
- Real-time calculation engine
- Multiple input methods (text fields, sliders, dropdowns)
- Interactive mode selector cards
- Dynamic results display with glass effects
- Impact breakdown (CO2, Water, Energy)
- Real-world comparisons (trees, car km, LED bulbs)
- Responsive design for all devices

**Calculations:**
- CO2 Savings: 1.5 kg per kg of plastic
- Water Conservation: 11 liters per kg
- Energy Savings: 5.7 kWh per kg

## Modular Architecture

### Shared Components

#### `templates/shared/base.html`
Base template that provides:
- Common HTML structure
- Meta tags for SEO
- Font and icon loading
- CSS and JS imports
- Language management system
- Smooth scrolling
- Mobile menu functionality

#### `templates/shared/navbar.html`
Modern navigation bar with:
- Glassmorphism background
- Sticky positioning
- Scroll-based opacity changes
- Mobile-responsive menu
- Language switcher (EN/ID)
- Magnetic logo effect
- Smooth underline animations

#### `templates/shared/footer.html`
Footer component featuring:
- Three-column layout
- Social media links
- Quick navigation
- Contact information
- Magnetic hover effects
- Gradient separator line

## Modern UI Effects

### 1. Glassmorphism (iPhone Glass Effect)
**File**: `static/css/effects.css`

Classes available:
- `.glass` - Standard glass effect
- `.glass-dark` - Dark glass with more blur
- `.glass-light` - Light glass effect
- `.glass-card` - Complete glass card with hover

**Properties:**
- Semi-transparent background
- Backdrop blur filter
- Subtle border
- Soft shadows
- Smooth transitions

### 2. Magnetic Elements
**File**: `static/js/magnetic.js`

Three types of magnetic effects:
1. **Standard Magnetic** (`.magnetic`): Subtle attraction to cursor
2. **Strong Magnetic** (`.magnetic-strong`): Stronger effect with 3D rotation
3. **Text Magnetic** (`.magnetic-text`): Individual character movement

**Usage:**
```html
<button class="magnetic">Standard Button</button>
<button class="magnetic-strong">Strong Effect Button</button>
<h1 class="magnetic-text">Magnetic Text</h1>
```

### 3. Parallax Effects
**File**: `static/js/parallax.js`

Four parallax implementations:
1. **ParallaxScroll**: Scroll-based parallax
2. **ParallaxMouse**: Mouse movement parallax
3. **SmoothParallax**: Interpolated smooth parallax
4. **ScrollReveal**: Scroll-triggered animations

**Usage:**
```html
<!-- Scroll parallax -->
<div data-parallax="0.5">Content</div>

<!-- Mouse parallax -->
<div class="parallax-container">
  <div class="parallax-layer" data-depth="0.2">Layer 1</div>
  <div class="parallax-layer" data-depth="0.5">Layer 2</div>
</div>

<!-- Scroll reveal -->
<div class="scroll-reveal">Content fades in on scroll</div>
```

### 4. Animation Classes
Pre-built animation classes:
- `.animate-fade-in` - Fade in from bottom
- `.animate-slide-in-left` - Slide from left
- `.animate-slide-in-right` - Slide from right
- `.animate-scale-in` - Scale up effect
- `.animate-float` - Floating animation
- `.animate-delay-1` through `.animate-delay-5` - Staggered delays

### 5. Modern Buttons
- `.btn-modern` - Base modern button with shine effect
- `.btn-glass` - Glass button with hover states
- `.btn-modern:hover` - Animated shine sweep

### 6. Modern Cards
- `.modern-card` - Advanced card with gradient border
- Hover effects with scale and lift
- Smooth cubic-bezier transitions

## Technical Implementation

### Routes (main.py)
```python
@app.route("/")          # Homepage
@app.route("/news")      # News page
@app.route("/timeline")  # Timeline page
@app.route("/calculator") # Calculator page
```

### CSS Architecture
```
static/css/
└── effects.css (Modern effects library)
    ├── Glassmorphism
    ├── Parallax utilities
    ├── Magnetic element styles
    ├── Animation keyframes
    ├── Button styles
    ├── Card styles
    └── Responsive utilities
```

### JavaScript Modules
```
static/js/
├── magnetic.js (Magnetic effects engine)
│   ├── MagneticEffect class
│   ├── StrongMagneticEffect class
│   └── TextMagneticEffect class
└── parallax.js (Parallax engine)
    ├── ParallaxScroll class
    ├── ParallaxMouse class
    ├── SmoothParallax class
    └── ScrollReveal class
```

## Responsive Design

All pages are fully responsive with breakpoints:
- Mobile: < 768px
- Tablet: 768px - 1024px
- Desktop: > 1024px

Mobile-specific features:
- Hamburger menu
- Stacked layouts
- Touch-optimized interactions
- Reduced animation complexity
- Simplified navigation

## Browser Compatibility

- Chrome/Edge: Full support
- Firefox: Full support
- Safari: Full support (with -webkit prefixes)
- Mobile browsers: Optimized for touch

## Performance Optimizations

1. **Lazy Loading**: Images load as needed
2. **Deferred JavaScript**: Non-critical JS loads after page
3. **RequestAnimationFrame**: Smooth 60fps animations
4. **Debounced Events**: Optimized scroll handlers
5. **CSS Hardware Acceleration**: GPU-accelerated transforms
6. **Backdrop Filter**: Native browser blur (where supported)

## Accessibility

- Keyboard navigation support
- Focus-visible indicators
- ARIA labels on interactive elements
- Reduced motion support for users with preferences
- Semantic HTML structure
- Alt text on all images
- Screen reader friendly

## Language Support

All pages support:
- English (EN)
- Indonesian (ID)

Language switching:
- Persistent across pages (localStorage)
- Browser language detection
- Smooth content switching without reload

## Future Enhancements

Potential additions:
1. News article detail pages
2. Timeline filtering by category
3. Export calculator results as PDF
4. Share impact on social media
5. Animation preloading
6. Service worker for offline support
7. Dark mode toggle
8. More calculation modes
9. Interactive data visualizations
10. Real-time impact dashboard

## Best Practices

### Using Glass Effects
```html
<!-- Good: Use on contrasting backgrounds -->
<div style="background: url('image.jpg')">
  <div class="glass-card">Content</div>
</div>

<!-- Better: Combine with gradient -->
<div style="background: linear-gradient(135deg, #231842, #2e7d32)">
  <div class="glass-card">Content</div>
</div>
```

### Using Magnetic Effects
```html
<!-- Use sparingly on key interactive elements -->
<button class="btn-modern magnetic-strong">Call to Action</button>

<!-- Use standard magnetic on cards -->
<div class="card magnetic">Card Content</div>

<!-- Use text magnetic on hero titles -->
<h1 class="magnetic-text">Hero Title</h1>
```

### Using Parallax
```html
<!-- Keep data-parallax values between 0.1 and 0.8 -->
<div data-parallax="0.3">Subtle movement</div>
<div data-parallax="0.6">More noticeable</div>

<!-- Don't overuse - 2-3 parallax elements per section -->
```

## Testing

To test the new features:

1. **Start the server:**
   ```bash
   python main.py
   ```

2. **Visit pages:**
   - Homepage: `http://localhost:5000/`
   - News: `http://localhost:5000/news`
   - Timeline: `http://localhost:5000/timeline`
   - Calculator: `http://localhost:5000/calculator`

3. **Test features:**
   - Hover over magnetic elements
   - Scroll to see parallax effects
   - Try different calculator modes
   - Filter news articles
   - Switch languages
   - Test on mobile (resize browser)

## Support

For questions or issues:
- Email: hello@trackeco.org
- Instagram: @trackeco_org

## Credits

Built with:
- Flask (Python web framework)
- Vanilla JavaScript (No framework dependencies)
- CSS3 (Modern effects)
- Font Awesome (Icons)
- Inter Font (Typography)

---

**Version**: 2.0  
**Last Updated**: October 2024  
**Author**: TrackEco Development Team

