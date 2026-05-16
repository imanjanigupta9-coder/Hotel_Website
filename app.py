from datetime import datetime
import pathlib
import os
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

ROOMS = [
    {
        "name": "Single Room",
        "price": "6,500",
        "img": "https://images.unsplash.com/photo-1505693416388-ac5ce068fe85?auto=format&fit=crop&w=1200",
        "area": "25 m2",
        "guests": 1,
        "beds": 1,
        "description": "A bright, stylish room perfect for solo travelers."
    },
    {
        "name": "Double Room",
        "price": "10,000",
        "img": "https://images.unsplash.com/photo-1505693416388-ac5ce068fe85?auto=format&fit=crop&w=1200",
        "area": "35 m2",
        "guests": 2,
        "beds": 2,
        "description": "Comfort and elegance for couples or friends."
    },
    {
        "name": "Triple Room",
        "price": "14,500",
        "img": "https://images.unsplash.com/photo-1542314831-068cd1dbfeeb?auto=format&fit=crop&w=1200",
        "area": "45 m2",
        "guests": 3,
        "beds": 3,
        "description": "Spacious accommodation for families or groups."
    },
    {
        "name": "Royal Duplex",
        "price": "24,000",
        "img": "https://images.unsplash.com/photo-1522708323590-d24dbb6b0267?auto=format&fit=crop&w=1200",
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
        "quote": "From the moment we arrived, we were treated like royalty. Celestia's attention to detail and tranquil ambiance are unmatched.",
        "author": "Laura Greene",
        "location": "Jakarta",
        "image": "https://images.unsplash.com/photo-1494790108377-be9c29b29330?auto=format&fit=crop&w=400&q=80",
        "rating": 4.7,
        "badges": ["Excellent Point", "Top Company"],
        "rating_display": "4.7"
    },
    {
        "quote": "A wonderful, tranquil stay with warm service. The amenities exceeded our expectations and staff was incredibly attentive.",
        "author": "Priya Sharma",
        "location": "Mumbai",
        "image": "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?auto=format&fit=crop&w=400&q=80",
        "rating": 4.9,
        "badges": ["Client Feedback", "Top Company"],
        "rating_display": "4.9"
    },
    {
        "quote": "The rooms were beautiful and the location was perfect for our business retreat. Highly recommend for any occasion.",
        "author": "Arjun Kapoor",
        "location": "Bangalore",
        "image": "https://images.unsplash.com/photo-1500648767791-00dcc994a43e?auto=format&fit=crop&w=400&q=80",
        "rating": 4.8,
        "badges": ["Excellent Point", "Client Feedback"],
        "rating_display": "4.8"
    },
    {
        "quote": "We loved the dining options and the calm rooftop bar. Every moment here felt like a luxury getaway.",
        "author": "Maya Desai",
        "location": "Pune",
        "image": "https://images.unsplash.com/photo-1438761681033-6461ffad8d80?auto=format&fit=crop&w=400&q=80",
        "rating": 4.6,
        "badges": ["Top Company", "Client Feedback"],
        "rating_display": "4.6"
    }
]

AMENITIES = [
    {"title": "High-Speed Wi-Fi", "description": "Stay connected with powerful Wi-Fi in every room and public space."},
    {"title": "Smart Entertainment Systems", "description": "Modern in-room entertainment with streaming and premium audio."},
    {"title": "Fitness Center", "description": "A fully equipped gym for active guests and wellness routines."},
    {"title": "Spa and Wellness Center", "description": "Relaxation and recovery with spa treatments and tranquil spaces."},
    {"title": "In-Room Refreshments", "description": "Beverages and snacks delivered on demand to your suite."},
    {"title": "Gourmet Restaurants", "description": "Curated dining experiences with local and international menus."},
    {"title": "Grand Ballroom", "description": "Elegant event space for weddings, conferences, and celebrations."},
    {"title": "Meeting Rooms", "description": "Flexible workspaces with modern AV and support services."},
    {"title": "Outdoor Event Spaces", "description": "Beautiful open-air venues for receptions and special events."},
    {"title": "Poolside Café", "description": "Casual poolside refreshments with a chic lounge atmosphere."}
]

SERVICE_FEATURES = [
    {
        "title": "Rooms",
        "slug": "rooms-feature",
        "description": "Luxurious guest rooms designed with comfort, style, and restful amenities.",
        "img": "https://images.unsplash.com/photo-1505693416388-ac5ce068fe85?auto=format&fit=crop&w=900&q=80"
    },
    {
        "title": "Restaurant",
        "slug": "restaurant",
        "description": "Premium dining with local flavours, curated menus, and elegant ambience.",
        "img": "https://images.unsplash.com/photo-1498654896293-37aacf113fd9?auto=format&fit=crop&w=900&q=80"
    },
    {
        "title": "Hall",
        "slug": "hall",
        "description": "Grand event spaces for weddings, conferences, and private celebrations.",
        "img": "https://images.unsplash.com/photo-1524758631624-e2822e304c36?auto=format&fit=crop&w=900&q=80"
    },
    {
        "title": "Bar",
        "slug": "bar",
        "description": "Stylish bar experiences with cocktails, lounge seating, and evening vibes.",
        "img": "https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?auto=format&fit=crop&w=900&q=80"
    }
]

VALUE_ITEMS = [
    {"headline": "Indulge in World-Class Comfort and Convenience.", "description": "Every detail is designed to make your stay seamless and memorable."},
    {"headline": "Experience the Celestia Difference: Unparalleled Hospitality.", "description": "From arrival to departure, our team delivers thoughtful service at every step."},
    {"headline": "Trusted by 25,000+ world-class brands and organizations.", "description": "We create inspiring moments for guests, events, and corporate stays of all sizes."}
]

CONTACT_DETAILS = {
    "address": "123 MG Road, Central District, Bangalore, Karnataka 560001",
    "phone": "+91 80 1234 5678",
    "email": "hello@thezenithhotel.com",
    "hours": "Open daily 8:00 AM – 11:00 PM"
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

PRESTIGE_SUITE = {
    "name": "Prestige Suite",
    "size": "600 m2",
    "guests": 6,
    "beds": 3,
    "description": "A perfect blend of elegance and comfort, featuring expansive living spaces and breathtaking views. With luxurious furnishings, a private balcony, and exclusive amenities, it’s designed to provide an unparalleled retreat for discerning guests.",
    "details": "Proin donec scelerisque risus sociosqu hac adipiscing. Hendrerit cursus nam fames eget sagittis hac sit diam aenean. Elit viverra mi imperdiet netus hendrerit malesuada morbi. Tempor finibus nibh cursus si mi magnis tellus taciti amet. Suscipit auctor integer dui euismod erat penatibus dignissim si pede.\n\nPenatibus magna velit aenean adipiscing semper pede. Turpis scelerisque ornare netus pretium interdum hac volutpat nisl ligula. Duis molestie habitant porttitor luctus enim ligula nisl. Proin duis hendrerit aenean neque nisl. In nibh leo non inceptos eget pede.",
    "amenities": [
        "High-Speed Wi-Fi",
        "Smart Entertainment Systems",
        "Fitness Center",
        "Spa and Wellness Center",
        "In-Room Refreshments",
        "Gourmet Restaurants",
        "Grand Ballroom",
        "Meeting Rooms",
        "Outdoor Event Spaces",
        "Poolside Café"
    ],
    "discount": "Discount up to 35% for members",
    "price": "$1,099 / night"
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
    if any(k in msg for k in ("amenities", "spa", "pool", "restaurant", "dining")):
        return "We offer spa & wellness, rooftop dining, meeting spaces, and more. See the ‘Featured Facilities’ section on the site for details."
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
    {"name": "MakeMyTrip", "url": "https://www.makemytrip.com", "logo": "https://upload.wikimedia.org/wikipedia/commons/3/36/Makemytrip_logo.svg"},
    {"name": "Booking.com", "url": "https://www.booking.com", "logo": "https://upload.wikimedia.org/wikipedia/commons/6/69/Booking.com_logo.svg"},
    {"name": "Expedia", "url": "https://www.expedia.com", "logo": "https://upload.wikimedia.org/wikipedia/commons/5/5f/Expedia_Logo.svg"},
    {"name": "Cleartrip", "url": "https://www.cleartrip.com", "logo": "https://upload.wikimedia.org/wikipedia/commons/0/05/Cleartrip-logo.svg"},
    {"name": "Airbnb", "url": "https://www.airbnb.com", "logo": "https://upload.wikimedia.org/wikipedia/commons/6/69/Airbnb_Logo_B%C3%A9lo.svg"},
    {"name": "Tripadvisor", "url": "https://www.tripadvisor.in", "logo": "https://upload.wikimedia.org/wikipedia/commons/7/73/Tripadvisor_logo.svg"}
]

PAGES = [
    {"title": "About Us", "category": "Pages", "summary": "Discover our story, hospitality values, and the guest-first service philosophy behind The Zenith.", "hover_detail": "Learn how our hotel blends local charm with modern comfort for every stay.", "link": "/pages#about"},
    {"title": "Our Rooms", "category": "Pages", "summary": "Explore beautifully appointed rooms and suites designed for comfort, convenience, and elevated relaxation.", "hover_detail": "Browse room options that suit couples, families, and business travelers alike.", "link": "/pages#rooms"},
    {"title": "Amenities", "category": "Pages", "summary": "See our premium amenities including dining, wellness, business spaces, and leisure experiences.", "hover_detail": "Review the facilities that make every stay more convenient and memorable.", "link": "/pages#amenities"},
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
    hero_image = '/static/images/hero.png' if hero_static.exists() else 'https://images.unsplash.com/photo-1566073771259-6a8506099945?auto=format&fit=crop&w=1900&q=80'
    logo_image = '/static/images/navbar-logo.png' if logo_static.exists() else None
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
        subscribe_success=subscribed
    )

@app.route('/rooms')
def rooms_page():
    static_images = pathlib.Path(os.path.join(app.root_path, 'static', 'images'))
    logo_static = static_images / 'navbar-logo.png'
    logo_image = '/static/images/navbar-logo.png' if logo_static.exists() else None
    return render_template(
        'rooms.html',
        rooms=ROOMS,
        overview_features=ROOM_OVERVIEW_FEATURES,
        rating=ROOM_RATING,
        service_features=SERVICE_FEATURES,
        contact=CONTACT_DETAILS,
        partners=PARTNERS,
        logo_image=logo_image
    )

@app.route('/pages')
def pages_page():
    static_images = pathlib.Path(os.path.join(app.root_path, 'static', 'images'))
    logo_static = static_images / 'navbar-logo.png'
    logo_image = '/static/images/navbar-logo.png' if logo_static.exists() else None
    return render_template(
        'pages.html',
        pages=PAGES,
        contact=CONTACT_DETAILS,
        partners=PARTNERS,
        logo_image=logo_image
    )

@app.route('/detail-room')
def detail_room():
    return render_template(
        'detail_room.html',
        suite=PRESTIGE_SUITE,
        contact=CONTACT_DETAILS,
        partners=PARTNERS,
        service_features=SERVICE_FEATURES
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
    name = request.form.get('name', '')
    email = request.form.get('email', '')

    external_url = (
        f"https://your-backend-link.com/reserve?in={check_in}"
        f"&out={check_out}&adults={adults}&children={children}"
    )
    return redirect(external_url)

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
