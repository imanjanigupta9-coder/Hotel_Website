const mobileMenuBtn = document.getElementById('mobile-menu-btn');
const mobileMenu = document.getElementById('mobile-menu');
const bookingForm = document.getElementById('booking-form');
const availabilityStatus = document.getElementById('availability-status');
const validationMessage = document.getElementById('validation-message');
const searchButton = document.getElementById('search-button');
const langPickerBtn = document.getElementById('lang-picker-btn');
const langMenu = document.getElementById('lang-menu');

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
    site_title_hero: 'AVYUKT VIEW',
    hero_tagline: 'A New Chapter of Luxury in Bangalore',
    hero_description: 'Premium luxury hotel with world-class amenities, fine dining, and exceptional service in the heart of Bangalore.',
    about_label: 'About Us',
    rooms_label: 'Rooms',
    services_label: 'Services',
    offers_label: 'Offers',
    partners_label: 'Partners',
    contact_label: 'Contact',
    book_now_button: 'Book Now!',
    explore_rooms: 'Explore Rooms',
    name_label: 'Name',
    placeholder_name: 'Name',
    adults_label: 'Adults',
    children_label: 'Children',
    room_label: 'Room',
    book_now: 'Book Now',
    services_heading: 'Our hotel services',
    services_title: 'Rooms, Bar, Restaurant, SwimmingPool',
    services_desc: 'AVYUKT VIEW brings premium guest rooms, elevated dining, grand events, and stylish evenings together in one modern destination.',
    reserve_now: 'Reserve now',
    featured_heading: 'Featured Experiences',
    featured_title: 'Uplifted Page Features with Unique Imagery',
    featured_desc: 'Each feature below uses its own image, bold styling, and visual dynamics to make the page feel more premium.',
    check_in_label: 'Check In',
    check_out_label: 'Check Out',
    rate_pref_label: 'Rate Preference',
    check_button: 'Find Rooms',
    accommodation_title: 'Accommodation',
    amenities_heading: 'Copper Bar & Facilities',
    faq_title: 'Guest Information (FAQ)',
    partners_heading: 'Our partners',
    partners_desc: 'Trusted by 25,000+ world-class brands and organizations of all sizes.',
    offers_heading: 'Curated Packages for Every Stay',
    offers_desc: 'Discover seasonal packages designed for romantic getaways, family retreats, and business travel.',
    luxury_title: 'Luxury Living, Surrounded by Nature\'s Beauty',
    testimonial_label: 'TESTIMONIAL',
    testimonial_heading: 'Client Feedback & Reviews',
    testimonial_desc: 'Feedback collected from bookings and guest stays, pulled directly from our backend reviews.',
    testimonial_status: 'Live guest feedback from booking records',
    placeholder_email: 'Email',
    chat_input_placeholder: 'Ask about bookings, policies...'
  },
  hi: {
    site_title_hero: 'AVYUKT VIEW',
    hero_tagline: 'बेंगलुरु में विलासिता का एक नया अध्याय',
    hero_description: 'विश्व स्तरीय सुविधाओं, उत्कृष्ट भोजन और बेहतरीन सेवा के साथ प्रीमियम लक्ज़री होटल।',
    about_label: 'हमारे बारे में',
    rooms_label: 'कमरे',
    services_label: 'सेवाएँ',
    offers_label: 'ऑफ़र',
    partners_label: 'पार्टनर',
    contact_label: 'संपर्क',
    book_now_button: 'अभी बुक करें!',
    explore_rooms: 'गुणवत्ता कमरे खोजें',
    name_label: 'नाम',
    placeholder_name: 'नाम',
    adults_label: 'वयस्क',
    children_label: 'बच्चे',
    room_label: 'कमरा',
    book_now: 'अब बुक करें',
    services_heading: 'हमारी होटल सेवाएँ',
    services_title: 'Rooms, Bar, Restaurant, SwimmingPool',
    services_desc: 'AVYUKT VIEW प्रीमियम गेस्ट रूम, उच्च स्तरीय भोजन, भव्य कार्यक्रम और स्टाइलिश शामों को एक आधुनिक स्थल में लाता है।',
    reserve_now: 'अभी आरक्षित करें',
    featured_heading: 'विशेष सुविधाएँ',
    featured_title: 'विशिष्ट इमेजरी के साथ उन्नत अनुभव',
    featured_desc: 'प्रत्येक फीचर अपनी छवि, बोल्ड स्टाइलिंग और दृश्य गतिशीलता का उपयोग करता है ताकि पेज अधिक प्रीमियम लगे।',
    accommodation_title: 'आवास',
    amenities_heading: 'कॉप्पर बार और सुविधाएँ',
    faq_title: 'मेहमान जानकारी (अक्सर पूछे जाने वाले प्रश्न)',
    partners_heading: 'हमारे साझेदार',
    partners_desc: '25,000+ विश्व स्तरीय ब्रांड और संगठनों द्वारा भरोसा किया गया।',
    offers_heading: 'हर प्रवास के लिए तैयार पैकेज',
    offers_desc: 'रोमांटिक गेटवे, परिवारिक छुट्टियाँ, और व्यापार यात्राओं के लिए मौसमी पैकेज देखें।',
    luxury_title: 'प्रकृति की सुंदरता से घिरी विलासिता',
    testimonial_label: 'टेस्टिमोनियल',
    testimonial_heading: 'मूल्यांकन और समीक्षाएँ',
    testimonial_desc: 'बुकिंग रिकॉर्ड और मेहमान अनुभव से सीधे लिया गया फीडबैक।',
    testimonial_status: 'बुकींग रिकॉर्ड से लाइव गेस्ट फीडबैक',
    placeholder_email: 'ईमेल',
    chat_input_placeholder: 'बुकिंग, नीतियों के बारे में पूछें...'
  },
  te: {
    site_title_hero: 'AVYUKT VIEW',
    hero_tagline: 'బెంగళూరులో విలాసానికి ఒక కొత్త అధ్యాయం',
    hero_description: 'ప్రపంచ స్థాయి సదుపాయాలు, ఉత్తమ ఆహారం మరియు అసాధారణ సేవ కలిగిన ప్రీమియం లగ్జరీ హోటల్.',
    about_label: 'మన గురించి',
    rooms_label: 'గదులు',
    services_label: 'సేవలు',
    offers_label: 'ఆఫర్లు',
    partners_label: 'భాగస్వాములు',
    contact_label: 'సంపర్కం',
    book_now_button: 'ఇప్పుడే బుక్ చేయండి!',
    explore_rooms: 'గదులను అన్వేషించండి',
    name_label: 'పేరు',
    placeholder_name: 'పేరు',
    adults_label: 'బడ్లు',
    children_label: 'పిల్లలు',
    room_label: 'గది',
    book_now: 'ఇప్పుడు బుక్ చేయండి',
    services_heading: 'మన హోటల్ సేవలు',
    services_title: 'Rooms, Bar, Restaurant, SwimmingPool',
    services_desc: 'AVYUKT VIEW అత్యువోద్గత గెస్ట్ గదులు, అధిక రుచికరమైన భోజనం, ఘన ఈవెంట్లు మరియు శైలీచేసిన సాయంత్రాలను ఒక ఆధునిక గమ్యం లో కలిపి తెస్తుంది.',
    reserve_now: 'ఇప్పుడే రిజర్వ్ చేయండి',
    featured_heading: 'ప్రత్యేక అనుభవాలు',
    featured_title: 'అసాధారణ చిత్రాలతో ఉన్నత విశేషాలు',
    featured_desc: 'ప్రతి లక్షణం ప్రత్యేక నాడితో, బోల్డ్ శైలింగ్ తో మరియు దృశ్య డైనమిక్ తో పేజీని మరింత ప్రీమియమ్ గా అనిపింపజేస్తుంది.',
    accommodation_title: 'వసతి',
    amenities_heading: 'కాపర్ బార్ & సదుపాయాలు',
    faq_title: 'అతిథి సమాచారం (FAQ)',
    partners_heading: 'మా భాగస్వాములు',
    partners_desc: '25,000+ ప్రపంచ స్థాయి బ్రాండ్ మరియు సంస్థలు విశ్వసించనివారు.',
    offers_heading: 'ప్రతి వసతి కోసం రూపొందించిన ప్యాకేజీలు',
    offers_desc: 'ప్రేమ పర్యటనలు, కుటుంబ విహారాలు మరియు వ్యాపార ప్రయాణాలకు సీజనల్ ప్యాకేజీలను కనుగొనండి.',
    luxury_title: 'ప్రకృతి అందంతో చుట్టిన విలాసం',
    testimonial_label: 'సాక్ష్యపత్రం',
    testimonial_heading: 'క్లయంట్ అభిప్రాయాలు & సమీక్షలు',
    testimonial_desc: 'బుకింగ్ రికార్డుల నుండి, అతిథి నివాసాల నుండి సేకరించిన అభిప్రాయాలు.',
    testimonial_status: 'బుకింగ్ రికార్డుల నుండి ప్రత్యక్ష అతిథి అభిప్రాయం',
    placeholder_email: 'ఇమెయిల్',
    chat_input_placeholder: 'బుకింగ్, విధానాలు గురించి అడగండి...'
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

  document.querySelectorAll('[data-i18n-placeholder]').forEach((element) => {
    const key = element.dataset.i18nPlaceholder;
    if (translations[lang] && translations[lang][key]) {
      element.placeholder = translations[lang][key];
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

function setLanguageMenuState(open) {
  if (!langMenu || !langPickerBtn) return;
  langMenu.classList.toggle('hidden', !open);
  langPickerBtn.setAttribute('aria-expanded', open ? 'true' : 'false');
}

if (langPickerBtn && langMenu) {
  const savedLang = localStorage.getItem('site-lang') || 'en';
  applyLanguage(savedLang);

  langPickerBtn.addEventListener('click', () => {
    const isOpen = !langMenu.classList.contains('hidden');
    setLanguageMenuState(!isOpen);
  });

  document.addEventListener('click', (event) => {
    if (!langMenu.contains(event.target) && !langPickerBtn.contains(event.target)) {
      setLanguageMenuState(false);
    }
  });

  document.querySelectorAll('.lang-option').forEach((option) => {
    option.addEventListener('click', () => {
      const selectedLang = option.dataset.lang;
      applyLanguage(selectedLang);
      setLanguageMenuState(false);
    });
  });
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
    if (validationMessage) {
      validationMessage.textContent = 'Please enter date first';
    }
    searchButton.disabled = true;
    searchButton.classList.add('opacity-50', 'cursor-not-allowed');
    return;
  }

  if (validationMessage) {
    validationMessage.textContent = '';
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


