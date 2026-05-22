const mobileMenuBtn = document.getElementById('mobile-menu-btn');
const mobileMenu = document.getElementById('mobile-menu');
// booking-related elements are looked up dynamically because the booking sidebar
// can be replaced when switching rooms in-page.
function qs(id) { return document.getElementById(id); }

function currentBookingForm() { return qs('booking-form'); }
function currentAvailabilityStatus() { return qs('availability-status'); }
function currentValidationMessage() { return qs('validation-message'); }
function currentSearchButton() { return qs('search-button'); }
function currentAvailabilityModal() { return qs('availability-modal'); }
function currentAvailabilityModalMessage() { return qs('availability-modal-message'); }
function currentAvailabilityModalClose() { return qs('availability-modal-close'); }
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
    updateBookingButtonState();
  }
}

function bindGuestButtons() {
  document.querySelectorAll('.guest-button').forEach((button) => {
    button.onclick = () => {
      const target = button.dataset.target;
      const delta = button.classList.contains('guest-increment') ? 1 : -1;
      updateGuestValue(target, delta);
    };
  });
}

function setStatus(message = '', success = true) {
  const availabilityStatus = currentAvailabilityStatus();
  if (!availabilityStatus) return;
  availabilityStatus.textContent = message;
  availabilityStatus.className = success
    ? 'rounded-3xl border border-emerald-300 bg-emerald-50 p-4 text-sm text-emerald-700'
    : 'rounded-3xl border border-rose-300 bg-rose-50 p-4 text-sm text-rose-700';
}

function showAvailabilityModal(message, available = true) {
  const availabilityModal = currentAvailabilityModal();
  const availabilityModalMessage = currentAvailabilityModalMessage();
  if (!availabilityModal || !availabilityModalMessage) return;
  availabilityModalMessage.textContent = message;
  availabilityModal.classList.remove('hidden');
  availabilityModal.classList.add('flex');
  availabilityModalMessage.className = available ? 'text-sm leading-relaxed text-slate-200 mb-6' : 'text-sm leading-relaxed text-rose-300 mb-6';
}

function hideAvailabilityModal() {
  const availabilityModal = currentAvailabilityModal();
  if (!availabilityModal) return;
  availabilityModal.classList.add('hidden');
  availabilityModal.classList.remove('flex');
}

async function performAvailabilityCheck() {
  const bookingForm = currentBookingForm();
  const availabilityStatus = currentAvailabilityStatus();
  const validationMessage = currentValidationMessage();
  if (!bookingForm || !availabilityStatus || !validationMessage) return;

  const name = bookingForm.querySelector('[name="name"]')?.value.trim() || '';
  const checkIn = bookingForm.querySelector('[name="check_in"]')?.value || '';
  const checkOut = bookingForm.querySelector('[name="check_out"]')?.value || '';
  const roomType = bookingForm.querySelector('[name="room_type"]')?.value || '';
  const adults = bookingForm.querySelector('[name="adults"]')?.value || '1';
  const children = bookingForm.querySelector('[name="children"]')?.value || '0';

  if (!name || !checkIn || !checkOut || !roomType) {
    setStatus('Fill in all booking fields before checking availability.', false);
    validationMessage.textContent = 'Complete every field to check availability.';
    return;
  }

  if (new Date(checkOut) < new Date(checkIn)) {
    setStatus('Check-out must be the same day or after check-in.', false);
    validationMessage.textContent = 'Please select valid check-in and check-out dates.';
    return;
  }

  setStatus('Checking availability...', true);
  validationMessage.textContent = '';

  try {
    const formData = new FormData();
    formData.append('name', name);
    formData.append('check_in', checkIn);
    formData.append('check_out', checkOut);
    formData.append('room_type', roomType);
    formData.append('adults', adults);
    formData.append('children', children);

    const response = await fetch('/check_availability', {
      method: 'POST',
      body: formData
    });

    if (!response.ok) {
      throw new Error('Availability service unavailable');
    }

    const data = await response.json();
    if (data.available) {
      setStatus('Room is available! You can proceed with booking.', true);
      showAvailabilityModal(`Great news! ${roomType} is available from ${checkIn} to ${checkOut}. Book fast before it fills up!`, true);
    } else {
      setStatus('Sorry, that room is not available for these dates.', false);
      showAvailabilityModal(`Unfortunately ${roomType} is not available for your selected dates. Try another room or date range.`, false);
    }
  } catch (error) {
    setStatus('Availability check is not connected yet.', false);
    showAvailabilityModal('The backend availability service is not connected yet. Please add the backend link to enable live room checks.', false);
  }
}

function updateBookingButtonState() {
  const bookingForm = currentBookingForm();
  const searchButton = currentSearchButton();
  const validationMessage = currentValidationMessage();
  if (!bookingForm || !searchButton) return;

  const nameInput = bookingForm.querySelector('[name="name"]');
  const checkInInput = bookingForm.querySelector('[name="check_in"]');
  const checkOutInput = bookingForm.querySelector('[name="check_out"]');
  const roomSelect = bookingForm.querySelector('[name="room_type"]');

  const name = nameInput ? nameInput.value.trim() : '';
  const checkIn = checkInInput ? checkInInput.value : '';
  const checkOut = checkOutInput ? checkOutInput.value : '';
  const roomType = roomSelect ? roomSelect.value : '';

  const validDates = checkIn && checkOut && new Date(checkOut) >= new Date(checkIn);
  const formIsValid = name && checkIn && checkOut && roomType && validDates;

  if (formIsValid) {
    searchButton.disabled = false;
    searchButton.classList.remove('opacity-50', 'cursor-not-allowed');
    if (validationMessage) validationMessage.textContent = '';
    setStatus('Ready to book — submit when you are ready.', true);
  } else {
    searchButton.disabled = true;
    searchButton.classList.add('opacity-50', 'cursor-not-allowed');
    if (validationMessage) {
      validationMessage.textContent = 'Please fill all booking fields and choose a valid check-out date.';
    }
    setStatus('Complete all fields to enable booking.', false);
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

function bindRoomSwitchLinks() {
  document.querySelectorAll('.room-switch').forEach((link) => {
    // avoid duplicate handlers
    link.onclick = async function (e) {
      e.preventDefault();
      const href = link.getAttribute('href');
      if (!href) return;
      try {
        const res = await fetch(href);
        if (!res.ok) throw new Error('Failed to load room');
        const html = await res.text();
        const parser = new DOMParser();
        const doc = parser.parseFromString(html, 'text/html');
        const newMain = doc.querySelector('main');
        if (newMain) {
          const main = document.querySelector('main');
          main.innerHTML = newMain.innerHTML;
          history.pushState({}, '', href);
          // rebind dynamic widgets in the newly injected content
          initializePageComponents();
          window.scrollTo({ top: 0, behavior: 'smooth' });
        }
      } catch (err) {
        console.error('room switch failed', err);
        window.location.href = href; // fallback to full navigation
      }
    };
  });
}

function bindAvailabilityModalClose() {
  const btn = currentAvailabilityModalClose();
  if (btn) btn.onclick = hideAvailabilityModal;
}

function bindBookingForm() {
  const bookingForm = currentBookingForm();
  if (!bookingForm) return;
  bookingForm.querySelectorAll('input, select').forEach((field) => {
    field.onchange = updateBookingButtonState;
    field.oninput = updateBookingButtonState;
  });
  const searchButton = currentSearchButton();
  if (searchButton) searchButton.onclick = performAvailabilityCheck;
  bookingForm.onsubmit = (event) => {
    const sb = currentSearchButton();
    if (sb && sb.disabled) event.preventDefault();
  };
}

function initializePageComponents() {
  // set date mins
  const today = new Date().toISOString().split('T')[0];
  document.querySelectorAll('input[type="date"]').forEach((d) => { d.min = today; if (!d.value) d.value = today; });
  bindGuestButtons();
  bindBookingForm();
  bindAvailabilityModalClose();
  bindRoomSwitchLinks();
  revealOnScroll();
  updateBookingButtonState();
}

// initialize booking and room-switch handlers on first load
initializePageComponents();

window.addEventListener('scroll', revealOnScroll);
window.addEventListener('load', () => {
  revealOnScroll();
  // prevent past dates selection and set min to today for all date inputs
  const today = new Date().toISOString().split('T')[0];
  document.querySelectorAll('input[type="date"]').forEach((d) => {
    d.min = today;
    // if empty, set to today so same-day booking is easier to test
    if (!d.value) d.value = today;
  });
  updateBookingButtonState();
});


