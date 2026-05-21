import pathlib, re
path = pathlib.Path('static/js/main.js')
text = path.read_text(encoding='utf-8')
start = text.find("'Open full gallery': '", 21980)
assert start != -1, 'chunk start not found'
end = text.find("\n  }\n};", start)
assert end != -1, 'chunk end not found'
chunk = text[start:end]
lines = chunk.splitlines()
pattern = re.compile(r"^(\s*)(?:'((?:\\'|[^'])*)'|\"((?:\\\"|[^\"])*)\"|([A-Za-z_][A-Za-z0-9_]*)):\s*(.*)$")
entries = []
for line in lines:
    m = pattern.match(line)
    if not m:
        raise SystemExit(f'unmatched line: {line!r}')
    indent, s1, s2, s3, rest = m.groups()
    key = s1 if s1 is not None else s2 if s2 is not None else s3
    quote = "'" if s1 is not None else '"' if s2 is not None else ''
    entries.append((line, indent, quote, key, rest))

hi_translations = {
    'Open full gallery': 'पूर्ण गैलरी खोलें',
    'Our Story': 'हमारी कहानी',
    'Our Values': 'हमारे मूल्य',
    'Our partners': 'हमारे साझेदार',
    'Packages tailored for your journey.': 'आपकी यात्रा के अनुसार तैयार पैकेज।',
    'Partners': 'साझेदार',
    'Phone': 'फोन',
    'Phone:': 'फोन:',
    'Plan events': 'कार्यक्रमों की योजना बनाएं',
    'Plan events →': 'कार्यक्रमों की योजना बनाएं →',
    'Premier exposure': 'प्रधान प्रदर्शन',
    'Premium partner network': 'प्रीमियम साझेदार नेटवर्क',
    'Premium room escapes': 'प्रीमियम कमरे अनुभव',
    'Price / night': 'मूल्य / रात',
    'Private bookings': 'निजी बुकिंग',
    'Quick contact': 'त्वरित संपर्क',
    'Ready to book?': 'बुक करने के लिए तैयार?',
    'Reception hours': 'रिसेप्शन समय',
    'Reliable service': 'विश्वसनीय सेवा',
    'Reserve Dining & Bar': 'डाइनिंग और बार आरक्षित करें',
    'Reserve now': 'अब आरक्षित करें',
    'Reserve your stay': 'अपना प्रवास आरक्षित करें',
    'Restaurant': 'रेस्टोरेंट',
    'Rooftop Dining': 'रूफटॉप डाइनिंग',
    'Room': 'कमरा',
    'Room Details': 'कमरे का विवरण',
    'Room comfort': 'कमरे की सुविधा',
    'Room specifications': 'कक्ष विनिर्देश',
    'Rooms': 'कमरे',
    'Rooms & Galleries': 'कमरे और गैलरियां',
    'Rooms & galleries': 'कमरे और गैलरियां',
    'Rooms designed for couples or friends.': 'जोड़े या दोस्तों के लिए डिज़ाइन किए गए कमरे।',
    'Savor signature meals in a stunning rooftop setting with city skyline views.': 'शहर के स्काईलाइन दृश्यों के साथ शानदार रूफटॉप सेटिंग में सिग्नेचर भोजन का आनंद लें।',
    'Seamless guest experiences': 'निरंतर अतिथि अनुभव',
    'See the menu': 'मेनू देखें',
    'Select your dates and book directly for the best rate.': 'सर्वश्रेष्ठ दर के लिए अपनी तारीखें चुनें और सीधे बुक करें।',
    'Send': 'भेजें',
    'Send a message and we’ll reply shortly.': 'एक संदेश भेजें और हम शीघ्र ही उत्तर देंगे।',
    'Send message': 'संदेश भेजें',
    'Services': 'सेवाएँ',
    'Sign Up': 'साइन अप करें',
    'Sign up our newsletter': 'हमारे न्यूज़लेटर के लिए साइन अप करें',
    'Signature Suites': 'सिग्नेचर सूट',
    'Signature bar': 'सिग्नेचर बार',
    'Signature restaurant dining': 'सिग्नेचर रेस्टोरेंट डाइनिंग',
    'Single & Deluxe': 'सिंगल और डीलक्स',
    'Smartly styled rooms ideal for solo travel, business stays, and short breaks.': 'सोलो यात्रा, व्यापारिक ठहराव, और छोटे ब्रेक के लिए स्मार्ट तरीके से डिज़ाइन किए गए कमरे।',
    'Special Offers': 'विशेष ऑफ़र',
    'Stay': 'ठहरें',
    'Stylish Guest Rooms': 'स्टाइलिश अतिथि कमरे',
    'Suite': 'सूट',
    'Suite-level comfort and space for families and groups.': 'परिवारों और समूहों के लिए सुइट स्तर का आराम और जगह।',
    'Suites & Large Rooms': 'सूइट्स और बड़े कमरे',
    "Thanks! We\\'ll keep you updated.": 'धन्यवाद! हम आपको अपडेट کرتے रहेंगे।',
    'Top Company': 'शीर्ष कंपनी',
    'Trusted by 25,000+ world-class brands and organizations of all sizes.': '25,000+ विश्वस्तरीय ब्रांड और सभी आकार की संस्थाओं द्वारा भरोसा किया गया।',
    'Trusted by 25,000+ world-class brands and organizations.': '25,000+ विश्व स्तरीय ब्रांड और संस्थाओं द्वारा भरोसा किया गया।',
    'Trusted by leading brands': 'प्रमुख ब्रांडों द्वारा भरोसा किया गया',
    'Until 12:00': '12:00 तक',
    'Uplifted Page Features with Unique Imagery': 'अद्वितीय चित्रों के साथ उन्नत पेज फीचर',
    'Use our booking link to reserve a room or check availability instantly.': 'कमरा आरक्षित करने या उपलब्धता तुरंत जांचने के लिए हमारे बुकिंग लिंक का उपयोग करें।',
    'View amenities': 'सुविधाएं देखें',
    'View gallery': 'गैलरी देखें',
    'Visit us': 'हमसे मिलें',
    'Warm Hospitality': 'गरम आतिथ्य',
    'We respect your privacy. Unsubscribe at any time.': 'हम आपकी गोपनीयता का सम्मान करते हैं। किसी भी समय सदस्यता रद्द करें।',
    '+': '+',
    "0 else '4.7' }} • Excellent Point": "0 else '4.7' }} • Excellent Point",
    "0 else 'Jakarta' }}": "0 else 'Jakarta' }}",
    "0 else 'Laura Greene' }}": "0 else 'Laura Greene' }}",
    '1 Bed': '1 बिस्तर',
    '1 Bed Options': '1 बिस्तर विकल्प',
    '2 Bed': '2 बिस्तर',
    '2 Bed Options': '2 बिस्तर विकल्प',
    'A New Chapter of Luxury in Bangalore': 'बेंगलुरु में विलासिता का एक नया अध्याय',
    'A closer look at the space': 'स्थान पर करीब से नज़र',
    'A curated dining experience for every meal.': 'हर भोजन के लिए चुना हुआ डाइनिंग अनुभव।',
    'A seamless dining experience for every guest.': 'हर अतिथि के लिए सहज डाइनिंग अनुभव।',
    'Browse our curated gallery for the {{ selected_room.type }} room.': 'चयनित {{ selected_room.type }} कमरे के लिए हमारी चयनित गैलरी ब्राउज़ करें।',
    'Up to {{ selected_room.guests }} guests': 'अधिकतम {{ selected_room.guests }} अतिथि',
    'हिन्दी': 'हिन्दी',
    'తెలుగు': 'తెలుగు',
    '“': '“',
    '•': '•',
    '• Airport transfers & local logistics': '• एयरपोर्ट ट्रांसफर और स्थानीय लॉजिस्टिक्स',
    '• Chef-curated meals and seasonal dishes': '• शेफ द्वारा तैयार भोजन और मौसमी व्यंजन',
    '• Comfortable table service': '• आरामदायक टेबल सेवा',
    '• Direct booking link': '• सीधे बुकिंग लिंक',
    '• Group dining for guests and business meals': '• अतिथि और व्यावसायिक भोजन के लिए समूह डाइनिंग',
    '• Group dining support': '• समूह डाइनिंग समर्थन',
    '• In-room dining and curated experiences': '• इन-रूम डाइनिंग और चयनित अनुभव',
    '• Local and international favorites': '• स्थानीय और अंतरराष्ट्रीय पसंद',
    '• Nightly lounge service': '• रात्री लाउंज सेवा',
    '• Personalized concierge & reservations': '• व्यक्तिगत कंसीयर्ज़ और आरक्षण',
    '• Premium cocktails': '• प्रीमियम कॉकटेल',
    '• Private dining experiences and bar menus': '• निजी डाइनिंग अनुभव और बार मेनू',
    '• Seasonal tasting menu': '• मौसमी टेस्टिंग मेनू',
    '• Table reservations': '• टेबल आरक्षण',
    '• Wine pairings': '• वाइन पेयरिंग',
    '₹{{ room.price }}': '₹{{ room.price }}',
    '₹{{ selected_room.price }}': '₹{{ selected_room.price }}',
    '−': '−',
    '◆': '◆',
    '✓': '✓',
    '✕': '✕',
    'What’s included': 'क्या शामिल है',
    'Why choose AVYUKT VIEW services?': 'AVYUKT VIEW सेवाओं को क्यों चुनें?',
    'Why choose dining with us': 'हमारे साथ डाइनिंग क्यों चुनें',
    'Why choose our seasonal offers?': 'हमारे मौसमी ऑफ़र क्यों चुनें?',
    'Why our partners choose AVYUKT VIEW': 'हमारे साझेदार AVYUKT VIEW को क्यों चुनते हैं',
    'Your Journey to Relaxation Starts Here.': 'आराम की आपकी यात्रा यहीं से शुरू होती है।',
    '© 2026 AVYUKT VIEW. All rights reserved.': '© 2026 AVYUKT VIEW। सभी अधिकार सुरक्षित।',
    'Find Rooms': 'कमरे खोजें',
    'Please enter date first': 'कृपया पहले तारीख दर्ज करें',
    'Select dates and guests to preview rates.': 'दरें देखने के लिए तारीख और अतिथि चुनें।',
    'Unable to retrieve rate details right now. Please try again later.': 'अभी दर विवरण प्राप्त नहीं किया जा सकता। कृपया बाद में पुनः प्रयास करें।',
    'There was an error contacting the chat service. Please try again later.': 'चैट सेवा से संपर्क करने में त्रुटि हुई। कृपया बाद में पुनः प्रयास करें।',
    'chat_input_placeholder': 'बुकिंग, नीतियों के बारे में पूछें...',
    'name_label': 'नाम',
    'placeholder_name': 'नाम',
    'adults_label': 'वयस्क',
    'children_label': 'बच्चे',
    'room_label': 'कमरा',
    'book_now': 'अभी बुक करें',
    'book_now_button': 'अब बुक करें!'
}

def escape_js_value(value):
    return value.replace('\\', '\\\\').replace("'", "\\'")

hi_lines = []
for line, indent, quote, key, rest in entries:
    if key not in hi_translations:
        raise SystemExit(f'Missing hi translation for {key!r}')
    value = hi_translations[key]
    escaped = escape_js_value(value)
    line_end = ',' if line.strip().endswith(',') else ''
    key_text = f"{quote}{key}{quote}" if quote else key
    hi_lines.append(f"{indent}{key_text}: '{escaped}'{line_end}")

kn_lines = [line for line, *_ in entries]
replacement = '\n'.join(hi_lines) + '\n  },\n  kn: {\n' + '\n'.join(kn_lines) + '\n  }\n};'
new_text = text[:start] + replacement + text[end:]
path2 = pathlib.Path('static/js/main.js')
path2.write_text(new_text, encoding='utf-8')
print('patched', len(entries), 'entries, hi+kn blocks created')
