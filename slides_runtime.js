// Slide presentation runtime
let currentSlide = 0;

// Add CSS for content transitions
function addTransitionStyles() {
  const style = document.createElement('style');
  style.textContent = `
    .slide-content {
      opacity: 0;
      transform: translateY(20px);
      transition: opacity 0.8s ease-out, transform 0.8s ease-out;
      transition-delay: 0s;
    }
    
    .slide.active .slide-content {
      opacity: 1;
      transform: translateY(0);
      transition-delay: 1.5s; /* Longer delay for word box */
    }
    
    .slide-content h1,
    .slide-content h2,
    .slide-content ul,
    .slide-content p,
    .slide-content .icon-row {
      opacity: 0;
      transform: translateY(15px);
      transition: opacity 0.6s ease-out, transform 0.6s ease-out;
    }
    
    .slide.active .slide-content h1 {
      opacity: 1;
      transform: translateY(0);
      transition-delay: 1.8s;
    }
    
    .slide.active .slide-content h2 {
      opacity: 1;
      transform: translateY(0);
      transition-delay: 2.0s;
    }
    
    .slide.active .slide-content ul,
    .slide.active .slide-content p {
      opacity: 1;
      transform: translateY(0);
      transition-delay: 2.2s;
    }
    
    .slide.active .slide-content .icon-row {
      opacity: 1;
      transform: translateY(0);
      transition-delay: 2.4s;
    }
  `;
  document.head.appendChild(style);
}

// Navigation functions
function showSlide(n) {
  const slides = document.querySelectorAll('.slide');
  if (n >= slides.length) currentSlide = 0;
  if (n < 0) currentSlide = slides.length - 1;
  
  // Remove active class from all slides first
  slides.forEach(slide => slide.classList.remove('active'));
  
  // Add a small delay before showing the new slide to ensure clean transitions
  setTimeout(() => {
    if (slides[currentSlide]) {
      slides[currentSlide].classList.add('active');
    }
  }, 50);
}

function nextSlide() {
  currentSlide++;
  showSlide(currentSlide);
}

function prevSlide() {
  currentSlide--;
  showSlide(currentSlide);
}

// Generate slide HTML
function generateSlides(slidesData) {
  console.log('Generating slides:', slidesData.length);
  const deck = document.getElementById('deck');
  
  slidesData.forEach((slide, index) => {
    console.log(`Creating slide ${index}:`, slide.title);
    const slideEl = document.createElement('div');
    slideEl.className = `slide ${slide.layout || ''}`;
    if (index === 0) slideEl.classList.add('active');
    
    let html = '';
    
    // Background image
    if (slide.bg) {
      console.log(`Adding background: assets/${slide.bg}`);
      html += `<img src="assets/${slide.bg}" class="bg" alt="">`;
    }
    
    // Overlay images
    if (slide.overlays) {
      slide.overlays.forEach(overlay => {
        console.log(`Adding overlay: assets/${overlay.src}`);
        html += `<img src="assets/${overlay.src}" class="overlay" style="${overlay.style || ''}" alt="">`;
      });
    }
    
    // Wrap content in a container for animations
    html += '<div class="slide-content">';
    
    // Content
    if (slide.title) {
      html += `<h1>${slide.title}</h1>`;
    }
    
    if (slide.subtitle) {
      html += `<h2>${slide.subtitle}</h2>`;
    }
    
    if (slide.bullets) {
      html += '<ul>';
      slide.bullets.forEach(bullet => {
        html += `<li>${bullet}</li>`;
      });
      html += '</ul>';
    }
    
    if (slide.text) {
      html += `<p class="${slide.textClass || ''}">${slide.text}</p>`;
    }
    
    // Icon row
    if (slide.icons) {
      html += '<div class="icon-row">';
      slide.icons.forEach(icon => {
        html += `<img src="assets/${icon}" alt="">`;
      });
      html += '</div>';
    }
    
    html += '</div>'; // Close slide-content wrapper
    
    slideEl.innerHTML = html;
    deck.appendChild(slideEl);
  });
}

// Keyboard navigation
document.addEventListener('keydown', (e) => {
  switch(e.key) {
    case 'ArrowRight':
    case ' ':
      nextSlide();
      break;
    case 'ArrowLeft':
      prevSlide();
      break;
    case 'Home':
      currentSlide = 0;
      showSlide(currentSlide);
      break;
    case 'End':
      currentSlide = slidesData.length - 1;
      showSlide(currentSlide);
      break;
  }
});

// Navigation will be set up after DOM loads

// Load slides data and initialize presentation
async function loadSlides() {
  console.log('Loading slides...');
  try {
    const response = await fetch('slides.json');
    console.log('Fetch response:', response.status);
    const slides = await response.json();
    console.log('Loaded slides:', slides.length);
    generateSlides(slides);
  } catch (error) {
    console.error('Error loading slides:', error);
  }
}

// Initialize presentation
console.log('Script loaded');
document.addEventListener('DOMContentLoaded', () => {
  console.log('DOM loaded, starting presentation');
  
  // Add transition styles
  addTransitionStyles();
  
  // Set up navigation
  document.getElementById('next').addEventListener('click', nextSlide);
  document.getElementById('prev').addEventListener('click', prevSlide);
  document.getElementById('edge-r').addEventListener('click', nextSlide);
  document.getElementById('edge-l').addEventListener('click', prevSlide);
  
  loadSlides();
});