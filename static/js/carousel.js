// Testimonials Carousel Handler
class TestimonialsCarousel {
  constructor() {
    this.currentIndex = 0;
    this.testimonials = document.querySelectorAll('.testimonial-card');
    this.totalTestimonials = this.testimonials.length;
    this.autoRotateInterval = null;
    this.autoRotateDelay = 4000; // 4 seconds

    this.init();
  }

  init() {
    if (this.totalTestimonials === 0) return;

    const prevBtn = document.querySelector('.carousel-nav-btn.prev-btn');
    const nextBtn = document.querySelector('.carousel-nav-btn.next-btn');
    const dots = document.querySelectorAll('.carousel-dot');

    if (prevBtn) prevBtn.addEventListener('click', () => this.prev());
    if (nextBtn) nextBtn.addEventListener('click', () => this.next());

    dots.forEach((dot, index) => {
      dot.addEventListener('click', () => this.goTo(index));
    });

    const testimonialsSection = document.getElementById('testimonials');
    if (testimonialsSection) {
      testimonialsSection.addEventListener('mouseenter', () => this.pause());
      testimonialsSection.addEventListener('mouseleave', () => this.resume());
    }

    this.showTestimonial(0);
    this.resume();
  }

  showTestimonial(index) {
    this.currentIndex = (index + this.totalTestimonials) % this.totalTestimonials;

    this.testimonials.forEach((card, i) => {
      if (i === this.currentIndex) {
        card.style.opacity = '1';
        card.style.transform = 'translateY(0)';
        card.style.zIndex = '10';
        card.style.pointerEvents = 'auto';
      } else {
        card.style.opacity = '0';
        card.style.transform = 'translateY(20px)';
        card.style.zIndex = '0';
        card.style.pointerEvents = 'none';
      }
    });

    const dots = document.querySelectorAll('.carousel-dot');
    dots.forEach((dot, i) => {
      dot.style.backgroundColor = i === this.currentIndex ? 'var(--accent)' : '#cbd5e1';
    });

    // Update right-side testimonial image (if present)
    try {
      const displayImg = document.getElementById('testimonial-display-image');
      if (displayImg) {
        const activeCard = this.testimonials[this.currentIndex];
        const img = activeCard.querySelector('img');
        if (img) {
          displayImg.src = img.src || img.getAttribute('data-src') || displayImg.src;
          displayImg.alt = img.alt || displayImg.alt;
        }
      }
    } catch (e) {
      // fail silently
    }
  }

  next() {
    this.showTestimonial(this.currentIndex + 1);
  }

  prev() {
    this.showTestimonial(this.currentIndex - 1);
  }

  goTo(index) {
    this.showTestimonial(index);
  }

  pause() {
    if (this.autoRotateInterval) {
      clearInterval(this.autoRotateInterval);
      this.autoRotateInterval = null;
    }
  }

  resume() {
    this.pause();
    this.autoRotateInterval = setInterval(() => {
      this.next();
    }, this.autoRotateDelay);
  }
}

class HorizontalSlider {
  constructor(wrapper) {
    this.wrapper = wrapper;
    this.slider = wrapper.querySelector('.horizontal-card-slider');
    this.dots = wrapper.querySelector('.carousel-dots');
    this.cards = this.slider ? Array.from(this.slider.children) : [];
    this.activeIndex = 0;
    this.isDragging = false;
    this.startX = 0;
    this.scrollStart = 0;

    this.init();
  }

  init() {
    if (!this.slider || this.cards.length === 0) return;

    this.cards.forEach((card, index) => {
      const dot = document.createElement('button');
      dot.type = 'button';
      dot.className = 'carousel-dot';
      dot.addEventListener('click', () => this.goTo(index));
      if (this.dots) this.dots.appendChild(dot);
    });

    this.slider.addEventListener('scroll', this.onScroll.bind(this), { passive: true });
    this.updateActiveDot(0);
  }

  getNearestCardIndex() {
    const leftPosition = this.slider.scrollLeft + this.slider.offsetWidth / 4;
    let nearestIndex = 0;
    let minDistance = Infinity;

    this.cards.forEach((card, index) => {
      const distance = Math.abs(card.offsetLeft - leftPosition);
      if (distance < minDistance) {
        minDistance = distance;
        nearestIndex = index;
      }
    });

    return nearestIndex;
  }

  onScroll() {
    const index = this.getNearestCardIndex();
    if (index !== this.activeIndex) {
      this.activeIndex = index;
      this.updateActiveDot(index);
    }
  }

  onWheel(e) {
    e.preventDefault();
    const scrollAmount = e.deltaY || e.deltaX;
    this.slider.scrollLeft += scrollAmount > 0 ? 300 : -300;
  }

  onPointerDown(e) {
    this.isDragging = true;
    this.startX = e.clientX;
    this.scrollStart = this.slider.scrollLeft;
    e.preventDefault();
    this.slider.classList.add('grabbing');
    this.slider.setPointerCapture(e.pointerId);
  }

  onPointerMove(e) {
    if (!this.isDragging) return;
    e.preventDefault();
    const delta = this.startX - e.clientX;
    this.slider.scrollLeft = this.scrollStart + delta;
  }

  onPointerUp(e) {
    if (!this.isDragging) return;
    this.isDragging = false;
    this.slider.classList.remove('grabbing');
    if (e.pointerId) {
      this.slider.releasePointerCapture(e.pointerId);
    }
    const snapIndex = this.getNearestCardIndex();
    this.goTo(snapIndex);
  }

  updateActiveDot(index) {
    if (!this.dots) return;
    Array.from(this.dots.children).forEach((dot, i) => {
      dot.classList.toggle('active', i === index);
    });
  }

  goTo(index) {
    const target = this.cards[index];
    if (!target) return;
    target.scrollIntoView({ behavior: 'smooth', inline: 'start' });
    this.activeIndex = index;
    this.updateActiveDot(index);
  }
}

function initHorizontalSliders() {
  document.querySelectorAll('.horizontal-card-slider-wrapper').forEach((wrapper) => {
    new HorizontalSlider(wrapper);
  });
}

function initTestimonialsCarousel() {
  const testimonialCarousel = new TestimonialsCarousel();
  window.testimonialsCarousel = testimonialCarousel;
}

function handleVisibilityChange() {
  const carousel = window.testimonialsCarousel;
  if (!carousel) return;

  if (document.hidden) {
    carousel.pause();
  } else {
    carousel.resume();
  }
}

document.addEventListener('DOMContentLoaded', () => {
  initHorizontalSliders();
  initTestimonialsCarousel();
});
document.addEventListener('visibilitychange', handleVisibilityChange);
