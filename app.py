from datetime import datetime
import pathlib
import os
import shutil
import urllib.parse
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

import re


def _with_width(url: str, w: int) -> str:
    """Return a URL with the requested width parameter applied.

    If the URL already contains a `w=` query param, replace it. Otherwise append one.
    """
    if not url:
        return url
    # replace existing w=NUMBER
    if re.search(r"w=\d+", url):
        return re.sub(r"w=\d+", f"w={w}", url)
    # append width preserving existing query string
    if "?" in url:
        return url + f"&w={w}"
    return url + f"?auto=format&fit=crop&w={w}&q=80"


def src_for(url: str, w: int = 800) -> str:
    return _with_width(url, w)


def srcset_for(url: str, widths=(480, 800, 1200, 1900)) -> str:
    parts = [f"{_with_width(url, w)} {w}w" for w in widths]
    return ", ".join(parts)


# Make helpers available in Jinja templates
app.jinja_env.globals['src_for'] = src_for
app.jinja_env.globals['srcset_for'] = srcset_for

LOGO_FALLBACK_PATHS = [
    os.path.expanduser(r"~/Downloads/Avyukt Shape Logo-03.png"),
    r"C:\Users\imanj\Downloads\Avyukt Shape Logo-03.png",
]

def get_logo_image():
    static_images = pathlib.Path(os.path.join(app.root_path, 'static', 'images'))
    static_images.mkdir(parents=True, exist_ok=True)
    logo_static = static_images / 'navbar-logo.png'
    if logo_static.exists():
        return '/static/images/navbar-logo.png'
    for candidate in LOGO_FALLBACK_PATHS:
        if os.path.exists(candidate):
            try:
                shutil.copy(candidate, str(logo_static))
                return '/static/images/navbar-logo.png'
            except Exception:
                break
    return None

ROOMS = [
    {
        "name": "Single Room",
        "slug": "single-room",
        "type": "single",
        "price": "6,500",
        "img": "/static/images/optimized/opt_2b7d00ef_photo-1505693416388-ac5ce068fe85.jpg",
        "area": "25 m2",
        "guests": 1,
        "beds": 1,
        "description": "A bright, stylish room perfect for solo travelers."
    },
    {
        "name": "Double Room",
        "slug": "double-room",
        "type": "double",
        "price": "10,000",
        "img": "/static/images/optimized/opt_2b7d00ef_photo-1505693416388-ac5ce068fe85.jpg",
        "area": "35 m2",
        "guests": 2,
        "beds": 2,
        "description": "Comfort and elegance for couples or friends."
    },
    {
        "name": "Triple Room",
        "slug": "triple-room",
        "type": "suite",
        "price": "14,500",
        "img": "/static/images/optimized/opt_e1729fc3_photo-1542314831-068cd1dbfeeb.jpg",
        "area": "45 m2",
        "guests": 3,
        "beds": 3,
        "description": "Spacious accommodation for families or groups."
    },
    {
        "name": "Royal Duplex",
        "slug": "royal-duplex",
        "type": "suite",
        "price": "24,000",
        "img": "/static/images/optimized/opt_eea12cea_photo-1522708323590-d24dbb6b0267.jpg",
        "area": "120 m2",
        "guests": 4,
        "beds": 2,
        "description": "Luxury duplex suites with separate living and bedroom areas."
    }
]

OFFERS = [
    {"title": "Summer Escape", "description": "Save up to 25% when you book early and stay longer.", "cta": "Book early"},
    {"title": "Reward Night", "description": "Use points for complimentary stays and dining credits.", "cta": "Points stay"},
    {"title": "Group & Events", "description": "Custom packages for weddings, conferences, and private celebrations.", "cta": "Plan your event"}
]

TESTIMONIALS = [
    {
        "quote": "From the moment we arrived, we were treated like royalty. AVYUKT VIEW's attention to detail and tranquil ambiance are unmatched.",
        "author": "Laura Greene",
        "location": "Jakarta",
        "image": "/static/images/optimized/opt_a9141a63_photo-1494790108377-be9c29b29330.jpg",
        "rating": 4.7,
        "badges": ["Excellent Point", "Top Company"],
        "rating_display": "4.7"
    },
    {
        "quote": "A wonderful, tranquil stay with warm service. The amenities exceeded our expectations and staff was incredibly attentive.",
        "author": "Priya Sharma",
        "location": "Mumbai",
        "image": "/static/images/optimized/opt_6a5ec629_photo-1507003211169-0a1dd7228f2d.jpg",
        "rating": 4.9,
        "badges": ["Client Feedback", "Top Company"],
        "rating_display": "4.9"
    },
    {
        "quote": "The rooms were beautiful and the location was perfect for our business retreat. Highly recommend for any occasion.",
        "author": "Arjun Kapoor",
        "location": "Bangalore",
        "image": "/static/images/optimized/opt_16d519c9_photo-1500648767791-00dcc994a43e.jpg",
        "rating": 4.8,
        "badges": ["Excellent Point", "Client Feedback"],
        "rating_display": "4.8"
    },
    {
        "quote": "We loved the dining options and the calm rooftop bar. Every moment here felt like a luxury getaway.",
        "author": "Maya Desai",
        "location": "Pune",
        "image": "/static/images/optimized/opt_2d22f108_photo-1438761681033-6461ffad8d80.jpg",
        "rating": 4.6,
        "badges": ["Top Company", "Client Feedback"],
        "rating_display": "4.6"
    }
]

# Updated amenities to the requested core list
AMENITIES = [
    {"title": "High-Speed Wi-Fi", "icon": "fa-solid fa-wifi", "description": "Stay connected with powerful Wi-Fi in every room and throughout the hotel."},
    {"title": "Smart Entertainment", "icon": "fa-solid fa-tv", "description": "Modern in-room entertainment with streaming and premium audio."},
    {"title": "In-Room Refreshments", "icon": "fa-solid fa-mug-saucer", "description": "Beverages and snacks delivered to your room on request."},
    {"title": "Gourmet Restaurant", "icon": "fa-solid fa-utensils", "description": "Curated dining experiences with local and international menus."},
    {"title": "Dining & Bar", "icon": "fa-solid fa-wine-glass", "description": "A stylish restaurant and bar offering cocktails, small plates, and premium beverages."},
    {"title": "24/7 Guest Support", "icon": "fa-solid fa-clock", "description": "Round-the-clock service for reservations, room requests, and dining assistance."}
]

SERVICE_FEATURES = [
    {
        "title": "Rooms",
        "slug": "rooms-feature",
        "description": "Luxurious guest rooms designed with comfort, style, and restful amenities.",
        "img": "/static/images/optimized/opt_5993971e_photo-1505693416388-ac5ce068fe85.jpg"
    },
    {
        "title": "Restaurant",
        "slug": "restaurant",
        "description": "Premium dining with local flavours, curated menus, and elegant ambience.",
        "img": "/static/images/optimized/opt_d66e4236_photo-1498654896293-37aacf113fd9.jpg"
    },
    {
        "title": "Bar",
        "slug": "bar",
        "description": "Stylish bar experiences with cocktails, lounge seating, and evening vibes.",
        "img": "/static/images/optimized/opt_f14943c4_photo-1517248135467-4c7edcad34c4.jpg"
    }
]

VALUE_ITEMS = [
    {"headline": "Indulge in World-Class Comfort and Convenience.", "description": "Every detail is designed to make your stay seamless and memorable."},
    {"headline": "Experience the AVYUKT VIEW Difference: Unparalleled Hospitality.", "description": "From arrival to departure, our team delivers thoughtful service at every step."},
    {"headline": "Trusted by 25,000+ world-class brands and organizations.", "description": "We create inspiring moments for guests, events, and corporate stays of all sizes."}
]

CONTACT_DETAILS = {
    "address": "123 MG Road, Central District, Bangalore, Karnataka 560001",
    "phone": "+91 80 1234 5678",
    "email": "hello@avyuktview.com",
    "hours": "Open daily 8:00 AM – 11:00 PM"
}

BOOKING_LINK = "https://your-backend-booking-link.com/reserve"  # Update this with your backend booking URL

ABOUT_US = {
    "title": "About AVYUKT VIEW",
    "tagline": "Where Luxury Meets Hospitality",
    "description": "Welcome to AVYUKT VIEW, Bangalore's premier luxury hotel. Since our inception, we've been dedicated to delivering world-class hospitality and unforgettable experiences to every guest.",
    "mission": "Our mission is to blend local charm with modern comfort, creating meaningful moments for every traveler who walks through our doors.",
    "highlights": [
        {
            "title": "World-Class Comfort",
            "description": "Experience luxurious rooms designed with every detail in mind for your utmost comfort and relaxation."
        },
        {
            "title": "Exceptional Service",
            "description": "Our dedicated team provides personalized service and attention that makes your stay truly memorable."
        },
        {
            "title": "Prime Location",
            "description": "Located in the heart of Bangalore with easy access to business districts, shopping, and cultural attractions."
        },
        {
            "title": "Premium Amenities",
            "description": "From world-class dining to refined bar service, every amenity is crafted for your pleasure."
        }
    ]
}

ROOM_OVERVIEW_FEATURES = [
    {"title": "Unparalleled Luxury", "copy": "Vehicula ad at tincidunt sociosqu letius iaculis consectetuer semper aenean parturient imperdiet."},
    {"title": "Stunning Locations", "copy": "Vehicula ad at tincidunt sociosqu letius iaculis consectetuer semper aenean parturient imperdiet."},
    {"title": "Exclusive Amenities", "copy": "Vehicula ad at tincidunt sociosqu letius iaculis consectetuer semper aenean parturient imperdiet."},
    {"title": "Convenience and Accessibility", "copy": "Vehicula ad at tincidunt sociosqu letius iaculis consectetuer semper aenean parturient imperdiet."}
]

ROOM_RATING = {
    "satisfaction": 92,
    "experience": "4.8",
    "feedback": "4.7",
    "reviews": 384
}

# Simple Terms & Conditions snippet used by the chat helper
TERMS_AND_CONDITIONS = (
    "By booking through our website you agree to our standard terms and conditions, "
    "including cancellation policies, payment authorization, and liability limits. "
    "Special offers may have separate terms — please review offer details or contact us for clarifications."
)


def generate_chat_reply(message: str) -> str:
    """Generate a simple rule-based reply using site details and terms.

    This is intentionally lightweight. Replace with an actual AI integration
    (OpenAI, Anthropic, etc.) for richer, policy-aware responses.
    """
    msg = (message or "").lower()
    if not msg.strip():
        return "Hi — tell me what you'd like to know about the hotel, bookings, or policies."

    # Keywords mapping
    if any(k in msg for k in ("book", "booking", "reserve", "reserve")):
        return (
            "You can reserve a room using our booking form. Select dates and guests, "
            "then click ‘Find Rooms’ or ‘Reserve Now’. For group bookings or special requests, "
            "please contact us at " + CONTACT_DETAILS["email"] + "."
        )
    if any(k in msg for k in ("price", "rate", "cost", "price list", "how much")):
        return (
            "Rates vary by dates and room type. Use the booking preview to see estimated price per night, "
            "or provide your dates and guests here and I'll estimate a rate for you."
        )
    if any(k in msg for k in ("check in", "check-in", "check out", "checkout", "time")):
        return "Standard check-in is at 2:00 PM and check-out is at 12:00 PM. Early check-in is subject to availability."
    if any(k in msg for k in ("wifi", "internet")):
        return "We provide high-speed WiFi across the property. Ask the front desk for access details during your stay."
    if any(k in msg for k in ("cancel", "cancellation", "refund")):
        return (
            "Cancellation terms depend on the rate you booked. Please review the terms attached to your reservation or contact us at "
            + CONTACT_DETAILS["email"] + " for assistance. " + TERMS_AND_CONDITIONS
        )
    if any(k in msg for k in ("amenities", "pool", "restaurant", "dining")):
        return "We offer premium rooms, restaurant dining, and bar experiences. See the ‘Featured Facilities’ section on the site for details."
    if any(k in msg for k in ("policy", "terms", "conditions", "terms and conditions")):
        return TERMS_AND_CONDITIONS

    # Fallback reply referencing contact details and human support
    return (
        "I can help with bookings, rates, and policies — or connect you to our team. "
        "Contact us at " + CONTACT_DETAILS["phone"] + " or " + CONTACT_DETAILS["email"] + "."
    )



FAQ_ITEMS = [
    {"question": "What is the standard check-in time?", "answer": "Standard check-in is at 2:00 PM and check-out is at 12:00 PM. Early check-in is subject to availability."},
    {"question": "Is there a dress code for the restaurant?", "answer": "We suggest smart casual attire. Some venues may require guests to be 21 or older after 8:00 PM."},
    {"question": "Can you help with airport transfers?", "answer": "Yes—we can arrange private transfers, ride-share pickup, and local transport on request."},
    {"question": "Do you offer late check-out or room upgrades?", "answer": "Late check-out and room upgrades are available subject to availability. Please request them during booking or at check-in."},
    {"question": "Are pets allowed at the hotel?", "answer": "We offer pet-friendly room options with advance reservation. Please contact our team for pet policy details and fees."}
]

PARTNERS = [
    {"name": "Accufirm", "url": "#", "logo": "/static/images/logo_accufirm.svg"},
    {"name": "Bloomly", "url": "#", "logo": "/static/images/logo_bloomly.svg"},
    {"name": "Brighto", "url": "#", "logo": "/static/images/logo_brighto.svg"},
    {"name": "Digancy", "url": "#", "logo": "/static/images/logo_digancy.svg"},
    {"name": "Ecoscape", "url": "#", "logo": "/static/images/Logo_ecoscape.svg"},
    {"name": "Femmous", "url": "#", "logo": "/static/images/logo_femmous.svg"},
    {"name": "Fincco D", "url": "#", "logo": "/static/images/logo_fincco_d.svg"},
    {"name": "KeyGenie", "url": "#", "logo": "/static/images/logo_keygenie.svg"}
]

PAGES = [
    {"title": "About Us", "category": "Pages", "summary": "Discover our story, hospitality values, and the guest-first service philosophy behind AVYUKT VIEW.", "hover_detail": "Learn how our hotel blends local charm with modern comfort for every stay.", "link": "/pages#about"},
    {"title": "Our Rooms", "category": "Pages", "summary": "Explore beautifully appointed rooms and suites designed for comfort, convenience, and elevated relaxation.", "hover_detail": "Browse room options that suit couples, families, and business travelers alike.", "link": "/pages#rooms"},
    {"title": "Amenities", "category": "Pages", "summary": "See our premium amenities including dining, bar, room comfort, and guest care.", "hover_detail": "Review the facilities that make every stay more convenient and memorable.", "link": "/pages#amenities"},
    {"title": "Dining & Bar", "category": "Pages", "summary": "Browse signature dining experiences, curated menus, and sophisticated bar settings.", "hover_detail": "Discover the restaurants, lounges, and bar experiences crafted for every mood.", "link": "/pages#dining"},
    {"title": "Events & Meetings", "category": "Pages", "summary": "Plan weddings, meetings, and celebrations in flexible venues with attentive event support.", "hover_detail": "View our event spaces, meeting packages, and tailored planning services.", "link": "/pages#events"},
    {"title": "Contact", "category": "Pages", "summary": "Reach our reservations and guest services team quickly for bookings and special requests.", "hover_detail": "Get direct contact details for reservations, inquiries, and guest support.", "link": "/pages#contact"}
]

@app.route('/')
def index():
    subscribed = request.args.get('subscribed')
    # prefer user-provided static images if available, otherwise use defaults
    static_images = pathlib.Path(os.path.join(app.root_path, 'static', 'images'))
    hero_static = static_images / 'hero.png'
    logo_static = static_images / 'navbar-logo.png'
    hero_image = '/static/images/hero.png' if hero_static.exists() else '/static/images/optimized/opt_bb02fee9_photo-1566073771259-6a8506099945.jpg'
    logo_image = get_logo_image()
    return render_template(
        'index.html',
        rooms=ROOMS,
        offers=OFFERS,
        testimonials=TESTIMONIALS,
        amenities=AMENITIES,
        service_features=SERVICE_FEATURES,
        hero_image=hero_image,
        logo_image=logo_image,
        value_items=VALUE_ITEMS,
        contact=CONTACT_DETAILS,
        faq_items=FAQ_ITEMS,
        partners=PARTNERS,
        about_us=ABOUT_US,
        booking_link=BOOKING_LINK,
        subscribe_success=subscribed
    )

@app.route('/rooms')
def rooms_page():
    return room_details_page()


@app.route('/room-details')
def room_details_page():
    logo_image = get_logo_image()
    slug = request.args.get('slug')
    enriched = []
    selected_room = None
    for r in ROOMS:
        rcopy = r.copy()
        rcopy['slug'] = rcopy.get('slug') or rcopy.get('name','').lower().replace(' ','-')
        rcopy['amenities'] = ["High-Speed Wi-Fi", "Smart TV", "Mini Bar", "Air Conditioning", "Complimentary Breakfast"]
        enriched.append(rcopy)
        if slug and rcopy['slug'] == slug:
            selected_room = rcopy

    if not selected_room and enriched:
        selected_room = enriched[0]

    related_rooms = [room for room in enriched if room['slug'] != selected_room['slug']]
    gallery_images = _load_gallery_images(selected_room.get('type'))

    return render_template(
        'room_details.html',
        selected_room=selected_room,
        related_rooms=related_rooms,
        gallery_images=gallery_images,
        logo_image=logo_image,
        contact=CONTACT_DETAILS,
        partners=PARTNERS,
        booking_link=BOOKING_LINK
    )

def _normalize_gallery_type(value: str | None) -> str | None:
    if not value:
        return None
    normalized = value.lower().replace('_', '-').strip()
    mapping = {
        'single-room': 'single',
        'single': 'single',
        'double-room': 'double',
        'double': 'double',
        'triple-room': 'suite',
        'triple': 'suite',
        'royal-duplex': 'suite',
        'duplex': 'suite',
        'suite': 'suite',
        'all': 'all'
    }
    if normalized in mapping:
        return mapping[normalized]
    if 'single' in normalized:
        return 'single'
    if 'double' in normalized:
        return 'double'
    if 'triple' in normalized or 'duplex' in normalized or 'suite' in normalized:
        return 'suite'
    return None


def _scan_folder(folder: pathlib.Path, img_type: str) -> list[dict]:
    imgs = []
    if folder.exists() and folder.is_dir():
        for f in sorted(folder.iterdir()):
            if f.suffix.lower() in ('.jpg', '.jpeg', '.png', '.webp'):
                imgs.append({"src": f"/static/images/galleries/{img_type}/{f.name}", "alt": f.name, "type": img_type})
    return imgs


def _load_gallery_images(gallery_type: str | None) -> list[dict]:
    static_galleries = pathlib.Path(os.path.join(app.root_path, 'static', 'images', 'galleries'))
    images = []
    if gallery_type:
        folder = static_galleries / gallery_type
        images = _scan_folder(folder, gallery_type)
    if not images:
        images = [
            {"src": "/static/images/optimized/opt_2b7d00ef_photo-1505693416388-ac5ce068fe85.jpg&q=80", "alt": "Single bed room", "type": "single"},
            {"src": "/static/images/optimized/opt_e1729fc3_photo-1542314831-068cd1dbfeeb.jpg&q=80", "alt": "Double bed room", "type": "double"},
            {"src": "/static/images/optimized/opt_eea12cea_photo-1522708323590-d24dbb6b0267.jpg&q=80", "alt": "Suite room", "type": "suite"},
            {"src": "/static/images/optimized/opt_2b7d00ef_photo-1505693416388-ac5ce068fe85.jpg&q=80", "alt": "Single bed room 2", "type": "single"},
            {"src": "/static/images/optimized/opt_2b7d00ef_photo-1505693416388-ac5ce068fe85.jpg&q=80", "alt": "Double bed room 2", "type": "double"},
            {"src": "/static/images/optimized/opt_e1729fc3_photo-1542314831-068cd1dbfeeb.jpg&q=80", "alt": "Suite room 2", "type": "suite"}
        ]
    if gallery_type and gallery_type != 'all':
        images = [img for img in images if img['type'] == gallery_type]
    return images


@app.context_processor
def inject_rooms():
    # make room list available to all templates for header dropdown and selectors
    return { 'all_rooms': ROOMS }


@app.route('/gallery')
def gallery_page():
    logo_image = get_logo_image()
    requested = request.args.get('type')
    gallery_type = _normalize_gallery_type(requested) or 'all'
    gallery_images = []

    if gallery_type == 'all':
        for room_type in ['single', 'double', 'suite']:
            gallery_images.extend(_scan_folder(pathlib.Path(os.path.join(app.root_path, 'static', 'images', 'galleries', room_type)), room_type))
    else:
        gallery_images = _load_gallery_images(gallery_type)

    return render_template('gallery.html', gallery_images=gallery_images, contact=CONTACT_DETAILS, gallery_type=gallery_type, logo_image=logo_image, booking_link=BOOKING_LINK)

@app.route('/pages')
def pages_page():
    static_images = pathlib.Path(os.path.join(app.root_path, 'static', 'images'))
    logo_static = static_images / 'navbar-logo.png'
    logo_image = get_logo_image()
    return render_template(
        'pages.html',
        pages=PAGES,
        faq_items=FAQ_ITEMS,
        contact=CONTACT_DETAILS,
        partners=PARTNERS,
        logo_image=logo_image,
        booking_link=BOOKING_LINK
    )

@app.route('/about')
def about_page():
    logo_image = get_logo_image()
    return render_template(
        'about.html',
        about_us=ABOUT_US,
        contact=CONTACT_DETAILS,
        partners=PARTNERS,
        booking_link=BOOKING_LINK,
        logo_image=logo_image
    )

@app.route('/partners')
def partners_page():
    logo_image = get_logo_image()
    return render_template(
        'partners.html',
        partners=PARTNERS,
        contact=CONTACT_DETAILS,
        booking_link=BOOKING_LINK,
        logo_image=logo_image
    )

@app.route('/services')
def services_page():
    logo_image = get_logo_image()
    return render_template(
        'services.html',
        partners=PARTNERS,
        amenities=AMENITIES,
        contact=CONTACT_DETAILS,
        booking_link=BOOKING_LINK,
        logo_image=logo_image
    )

@app.route('/dining-bar')
def dining_bar_page():
    logo_image = get_logo_image()
    return render_template(
        'dining_bar.html',
        contact=CONTACT_DETAILS,
        booking_link=BOOKING_LINK,
        logo_image=logo_image
    )

@app.route('/offers')
def offers_page():
    logo_image = get_logo_image()
    return render_template(
        'offers.html',
        offers=OFFERS,
        contact=CONTACT_DETAILS,
        booking_link=BOOKING_LINK,
        logo_image=logo_image
    )

@app.route('/contact')
def contact_page():
    logo_image = get_logo_image()
    return render_template(
        'contact.html',
        contact=CONTACT_DETAILS,
        booking_link=BOOKING_LINK,
        logo_image=logo_image
    )

@app.route('/features')
def features_page():
    logo_image = get_logo_image()
    return render_template(
        'features.html',
        partners=PARTNERS,
        amenities=AMENITIES,
        contact=CONTACT_DETAILS,
        booking_link=BOOKING_LINK,
        logo_image=logo_image
    )

@app.route('/join')
def join_page():
    logo_image = get_logo_image()
    return render_template(
        'join.html',
        contact=CONTACT_DETAILS,
        booking_link=BOOKING_LINK,
        logo_image=logo_image
    )

@app.route('/check_availability', methods=['POST'])
def check_availability():
    check_in = request.form.get('check_in')
    check_out = request.form.get('check_out')
    adults = int(request.form.get('adults', 1))
    children = int(request.form.get('children', 0))

    if not check_in or not check_out:
        return {
            "available": False,
            "message": "Please select both check-in and check-out dates.",
            "price": None
        }

    try:
        start_date = datetime.fromisoformat(check_in).date()
        end_date = datetime.fromisoformat(check_out).date()
    except ValueError:
        return {
            "available": False,
            "message": "Enter valid dates for check-in and check-out.",
            "price": None
        }

    if end_date <= start_date:
        return {
            "available": False,
            "message": "Check-out must be after check-in.",
            "price": None
        }

    nights = (end_date - start_date).days
    base_price = 7000 + adults * 1500 + children * 1000 + nights * 800
    message = f"Available from ₹{base_price:,} per night for {nights} night(s)."

    return {
        "available": True,
        "message": message,
        "price": base_price,
        "nights": nights
    }

@app.route('/book', methods=['POST'])
def handle_booking():
    check_in = request.form.get('check_in')
    check_out = request.form.get('check_out')
    adults = request.form.get('adults', '1')
    children = request.form.get('children', '0')
    name = request.form.get('name', '').strip()
    room_type = request.form.get('room_type', '')

    booking_params = {
        'name': name,
        'check_in': check_in,
        'check_out': check_out,
        'adults': adults,
        'children': children,
        'room_type': room_type,
    }

    if BOOKING_LINK and 'your-backend-booking-link.com' not in BOOKING_LINK:
        params = urllib.parse.urlencode(booking_params, doseq=True)
        return redirect(f"{BOOKING_LINK}?{params}")

    return render_template(
        'booking_confirmation.html',
        name=name,
        check_in=check_in,
        check_out=check_out,
        adults=adults,
        children=children,
        room_type=room_type,
        logo_image=get_logo_image(),
        contact=CONTACT_DETAILS,
        booking_link=BOOKING_LINK
    )

@app.route('/subscribe', methods=['POST'])
def subscribe():
    email = request.form.get('email', '').strip()
    if not email:
        return redirect(url_for('index', subscribed='0'))
    return redirect(url_for('index', subscribed='1'))


@app.route('/chat', methods=['POST'])
def chat():
    # Accept JSON or form POST
    message = request.form.get('message') if request.form.get('message') is not None else request.json.get('message', '')
    reply = generate_chat_reply(message)
    return {"reply": reply}

if __name__ == '__main__':
    # Binds to the port provided by the host environment, defaults to 5000
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
