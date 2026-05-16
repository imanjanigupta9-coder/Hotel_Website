const mobileMenuBtn = document.getElementById('mobile-menu-btn');
const mobileMenu = document.getElementById('mobile-menu');
const bookingForm = document.getElementById('booking-form');
const availabilityStatus = document.getElementById('availability-status');
const searchButton = document.getElementById('search-button');
const langSelect = document.getElementById('lang-select');

/* Chat widget elements */
const chatOpenBtn = document.getElementById('chat-open-btn');
const chatCloseBtn = document.getElementById('chat-close-btn');
const chatWidget = document.getElementById('chat-widget');
const chatForm = document.getElementById('chat-form');
const chatInput = document.getElementById('chat-input');
const chatMessages = document.getElementById('chat-messages');

function appendChatMessage(text, from = 'bot') {
  if (!chatMessages) return;
  const wrap = document.createElement('div');
  wrap.className = `chat-message ${from}`;
  wrap.innerHTML = `<div class="bubble">${text}</div>`;
  chatMessages.appendChild(wrap);
  chatMessages.scrollTop = chatMessages.scrollHeight;
}

function setChatTyping(show = true) {
  if (!chatMessages) return;
  let t = chatMessages.querySelector('.typing');
  if (show) {
    if (!t) {
      t = document.createElement('div');
      t.className = 'chat-message bot typing';
      t.innerHTML = '<div class="bubble"><span class="dot"></span><span class="dot"></span><span class="dot"></span></div>';
      chatMessages.appendChild(t);
      chatMessages.scrollTop = chatMessages.scrollHeight;
    }
  } else if (t) {
    t.remove();
  }
}

async function sendChatMessage(message) {
  if (!message || !message.trim()) return;
  appendChatMessage(message, 'user');
  chatInput.value = '';
  setChatTyping(true);

  try {
    const res = await fetch('/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message })
    });
    const data = await res.json();
    setChatTyping(false);
    appendChatMessage(data.reply || 'Sorry, I could not generate an answer right now.', 'bot');
  } catch (err) {
    setChatTyping(false);
    appendChatMessage('There was an error contacting the chat service. Please try again later.', 'bot');
  }
}

// Chat UI bindings
if (chatOpenBtn && chatWidget) {
  chatOpenBtn.addEventListener('click', () => {
    chatWidget.classList.remove('hidden');
    setTimeout(() => chatInput.focus(), 200);
  });
}
if (chatCloseBtn && chatWidget) {
  chatCloseBtn.addEventListener('click', () => chatWidget.classList.add('hidden'));
}
if (chatForm) {
  chatForm.addEventListener('submit', (e) => {
    e.preventDefault();
    const msg = chatInput.value;
    sendChatMessage(msg);
  });
}

const translations = {
  en: {
    site_title_hero: 'THE ZENITH',
    hero_tagline: 'A New Chapter of Luxury in Bangalore',
    check_in_label: 'Check In',
    check_out_label: 'Check Out',
    adults_label: 'Adults',
    children_label: 'Children',
    rate_pref_label: 'Rate Preference',
    check_button: 'Find Rooms',
    offers_label: 'Offers',
    accommodation_title: 'Accommodation',
    amenities_heading: 'Copper Bar & Facilities',
    faq_title: 'Guest Information (FAQ)',
    partners_heading: 'Our partners'
  },
  hi: {
    site_title_hero: 'THE ZENITH',
    hero_tagline: 'बेंगलुरु में विलासिता का एक नया अध्याय',
    check_in_label: 'चेक इन',
    check_out_label: 'चेक आउट',
    adults_label: 'वयस्क',
    children_label: 'बच्चे',
    rate_pref_label: 'दर प्राथमिकता',
    check_button: 'कमरों को देखें',
    offers_label: 'ऑफ़र',
    accommodation_title: 'आवास',
    amenities_heading: 'कॉप्पर बार और सुविधाएँ',
    faq_title: 'मेहमान जानकारी (अक्सर पूछे जाने वाले प्रश्न)',
    partners_heading: 'हमारे साझेदार'
  }
};

function applyLanguage(lang) {
  if (!lang) return;
  document.documentElement.lang = lang;
  localStorage.setItem('site-lang', lang);

  document.querySelectorAll('[data-i18n]').forEach((element) => {
    const key = element.dataset.i18n;
    if (translations[lang] && translations[lang][key]) {
      element.textContent = translations[lang][key];
    }
  });
}

const guestLimits = {
  adults: { min: 1, max: 10 },
  children: { min: 0, max: 6 }
};

function updateGuestValue(target, delta) {
  const valueEl = document.getElementById(`${target}-value`);
  const inputEl = document.getElementById(`${target}-input`);
  if (!valueEl || !inputEl) return;
  const current = parseInt(inputEl.value, 10);
  const next = Math.min(Math.max(current + delta, guestLimits[target].min), guestLimits[target].max);
  inputEl.value = next;
  valueEl.textContent = next.toString().padStart(1, '0');
  if (bookingForm) {
    checkAvailability();
  }
}

document.querySelectorAll('.guest-button').forEach((button) => {
  button.addEventListener('click', () => {
    const target = button.dataset.target;
    const delta = button.classList.contains('guest-increment') ? 1 : -1;
    updateGuestValue(target, delta);
  });
});

if (langSelect) {
  const savedLang = localStorage.getItem('site-lang') || 'en';
  langSelect.value = savedLang;
  applyLanguage(savedLang);
  langSelect.addEventListener('change', () => applyLanguage(langSelect.value));
}

function setStatus(message = '', success = true) {
  if (!availabilityStatus) return;
  availabilityStatus.textContent = message;
  availabilityStatus.className = success
    ? 'rounded-3xl border border-emerald-300 bg-emerald-50 p-4 text-sm text-emerald-700'
    : 'rounded-3xl border border-rose-300 bg-rose-50 p-4 text-sm text-rose-700';
}

async function checkAvailability() {
  if (!bookingForm || !searchButton || !availabilityStatus) return;
  const formData = new FormData(bookingForm);
  const checkIn = formData.get('check_in');
  const checkOut = formData.get('check_out');

  if (!checkIn || !checkOut) {
    setStatus('Select dates and guests to preview rates.', false);
    searchButton.disabled = true;
    searchButton.classList.add('opacity-50', 'cursor-not-allowed');
    return;
  }

  try {
    const response = await fetch('/check_availability', {
      method: 'POST',
      body: formData
    });
    const data = await response.json();
    setStatus(data.message, data.available);

    if (data.available) {
      searchButton.disabled = false;
      searchButton.classList.remove('opacity-50', 'cursor-not-allowed');
    } else {
      searchButton.disabled = true;
      searchButton.classList.add('opacity-50', 'cursor-not-allowed');
    }
  } catch (error) {
    setStatus('Unable to retrieve rate details right now. Please try again later.', false);
    searchButton.disabled = true;
    searchButton.classList.add('opacity-50', 'cursor-not-allowed');
  }
}

function revealOnScroll() {
  document.querySelectorAll('.reveal-hidden').forEach((element) => {
    const rect = element.getBoundingClientRect();
    if (rect.top < window.innerHeight - 80) {
      element.classList.add('reveal-visible');
    }
  });
}

if (mobileMenuBtn && mobileMenu) {

  mobileMenuBtn.addEventListener('click', () => {
    mobileMenu.classList.toggle('hidden');
  });
}

document.querySelectorAll('header nav a, #mobile-menu a').forEach((link) => {
  link.addEventListener('click', () => {
    if (mobileMenu) mobileMenu.classList.add('hidden');
  });
});

if (bookingForm) {
  bookingForm.querySelectorAll('input, select').forEach((field) => {
    field.addEventListener('change', checkAvailability);
  });

  searchButton.addEventListener('click', checkAvailability);

  bookingForm.addEventListener('submit', (event) => {
    if (searchButton.disabled) {
      event.preventDefault();
    }
  });
}

window.addEventListener('scroll', revealOnScroll);
window.addEventListener('load', () => {
  revealOnScroll();
  checkAvailability();
});


