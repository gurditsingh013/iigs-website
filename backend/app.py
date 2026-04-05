"""
IIGS Backend — Flask API for content management
Serves site content as JSON, provides admin panel for updates.
Data stored in a simple JSON file (no database needed).
"""

import json
import os
from datetime import datetime
from flask import Flask, request, jsonify, send_from_directory, render_template_string
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

DATA_FILE = os.path.join(os.path.dirname(__file__), "data.json")
FRONTEND_DIR = os.path.join(os.path.dirname(__file__), "..", "src")


def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return get_default_data()


def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def get_default_data():
    return {
        "site": {
            "name": "IIGS",
            "fullName": "International Institute of Gurmat Studies, Inc.",
            "tagline": "Rekindling the Sikh Spirit",
            "motto": "Deg Teg Fateh",
            "mottoGurmukhi": "ਦੇਗ ਤੇਗ ਫ਼ਤਿਹ",
            "email": "gurpreet.kaur@iigs.com",
            "address": "16702 Tourmaline Street, Chino Hills, CA 91709",
            "phone": "",
            "youtube": "https://www.youtube.com/c/IIGSCalling",
            "facebook": "https://www.facebook.com/igscalling",
            "instagram": "",
        },
        "events": [
            {
                "id": "dek-2026",
                "title": "Darbar-E-Khalsa 2026",
                "subtitle": "41st Annual Celebration",
                "date": "2026-12-25",
                "time": "6:30 AM onwards",
                "location": "LA Fairgrounds (Fairplex), Pomona, CA",
                "address": "1101 W. McKinley Ave, Pomona, CA 91768",
                "gate": "Gate 17, Building 6",
                "parking": "$18.00 (debit/credit card only)",
                "description": "Every December 25th, over 15,000 Sikhs unite for the grandest celebration of Guru Gobind Singh Ji's birthday.",
                "image": "https://dvncorestorageprod.blob.core.windows.net/files/ProjectApplication/100289/Updates/DEK_2025.1_20251115013559128.png",
                "active": True,
            },
        ],
        "camps": [
            {
                "id": "94th-camp",
                "title": "94th Sikh International Youth Camp",
                "dates": "July 2026 (Dates TBA)",
                "location": "Camp Seely, San Bernardino Mountains",
                "address": "250 North Highway 138, City of Crestline, CA-92325",
                "age": "8-25 years; married Sikh couples 35 and under",
                "capacity": "200",
                "registrationOpen": True,
                "description": "Join us in the beautiful San Bernardino Mountains for a transformative week of Gurmat learning, adventure, and community.",
                "activities": [
                    "Naam Simran & Kirtan",
                    "Path Classes",
                    "Trekking & Nature",
                    "Gatka & Martial Arts",
                    "Swimming",
                    "Turban Tying",
                    "Gurmukhi Learning",
                    "Personality Development",
                    "Campfire Night",
                ],
                "image": "https://dvncorestorageprod.blob.core.windows.net/files/ProjectApplication/100289/Updates/93rd%20camp%20flyer_20250611045711687.jpg",
                "active": True,
            },
        ],
        "scholarships": {
            "title": "Captain K.H. Singh Memorial Scholarships",
            "established": 2011,
            "totalAwarded": "$60,000+",
            "annualAmount": "Five scholarships of $1,000 each",
            "eligibility": [
                "Open to Sikh students in USA & Canada",
                "High school seniors and college students up to age 22",
                "Based on academic excellence & community service",
                "One scholarship considers sports achievements",
            ],
            "deadline": "February 28, 2026",
            "pastWinners": [
                {"name": "Aagya Kaur", "location": "West Covina, CA", "year": "2021-22"},
                {"name": "Amrita Priya Kaur", "location": "West Covina, CA", "year": "2021-22"},
                {"name": "Amitoj Singh", "location": "Fontana, CA", "year": "2021-22"},
                {"name": "Ekas Kaur", "location": "Winnipeg, MB, Canada", "year": "2021-22"},
                {"name": "Harlene Kaur", "location": "Cypress, TX", "year": "2021-22"},
            ],
        },
        "kirtan_library": [
            {
                "id": "dewan-179",
                "title": "179th Virtual Global Kirtan Dewan",
                "raagi": "IIGS Global Sangat",
                "facebook_video_id": "2042391212898729",
                "type": "Virtual Dewan",
                "duration": "90 min",
            },
            {
                "id": "dewan-122",
                "title": "122nd Virtual Global Kirtan Dewan",
                "raagi": "IIGS Global Sangat",
                "facebook_video_id": "843921813288143",
                "type": "Virtual Dewan",
                "duration": "90 min",
            },
            {
                "id": "dewan-90",
                "title": "90th Virtual Global Kirtan Dewan",
                "raagi": "IIGS Global Sangat",
                "facebook_video_id": "637002794230366",
                "type": "Virtual Dewan",
                "duration": "90 min",
            },
        ],
        "sikh_portraits": [
            {
                "id": "sp-1",
                "title": "The Sikh Portrait — Issue 1",
                "image": "https://static.wixstatic.com/media/fb9c60_0022226423004b0798a724306d5d9905~mv2.jpg/v1/fill/w_400,h_450,al_c,q_80/fb9c60_0022226423004b0798a724306d5d9905~mv2.jpg",
                "description": "A monthly IIGS publication celebrating Sikh heritage.",
            },
            {
                "id": "sp-2",
                "title": "The Sikh Portrait — Issue 2",
                "image": "https://static.wixstatic.com/media/fb9c60_0e5494721b1a4a9abd660c0063532c00.jpg/v1/fill/w_400,h_450,al_c,q_80/fb9c60_0e5494721b1a4a9abd660c0063532c00.jpg",
                "description": "Inspiring stories from the Sikh community.",
            },
            {
                "id": "sp-3",
                "title": "The Sikh Portrait — Issue 3",
                "image": "https://static.wixstatic.com/media/fb9c60_17e63491db774faba67ed27db0c15b98~mv2.jpg/v1/fill/w_400,h_450,al_c,q_80/fb9c60_17e63491db774faba67ed27db0c15b98~mv2.jpg",
                "description": "Faith, heritage, and community.",
            },
            {
                "id": "sp-4",
                "title": "The Sikh Portrait — Issue 4",
                "image": "https://static.wixstatic.com/media/fb9c60_192d9b621a3745c38099ad38d4a4ed4b.jpg/v1/fill/w_400,h_450,al_c,q_80/fb9c60_192d9b621a3745c38099ad38d4a4ed4b.jpg",
                "description": "Voices of the Sikh youth.",
            },
            {
                "id": "sp-5",
                "title": "The Sikh Portrait — Issue 5",
                "image": "https://static.wixstatic.com/media/fb9c60_279bc317496a4568a595236a0c39adc1.png/v1/fill/w_400,h_450,al_c,q_85/fb9c60_279bc317496a4568a595236a0c39adc1.png",
                "description": "Celebrating our roots.",
            },
            {
                "id": "sp-6",
                "title": "The Sikh Portrait — Issue 6",
                "image": "https://static.wixstatic.com/media/fb9c60_439f561cfac64361a3ca2655738aac96.jpg/v1/fill/w_400,h_450,al_c,q_80/fb9c60_439f561cfac64361a3ca2655738aac96.jpg",
                "description": "Remembering our heroes.",
            },
            {
                "id": "sp-7",
                "title": "The Sikh Portrait — Issue 7",
                "image": "https://static.wixstatic.com/media/fb9c60_51b2d97bea5c46408f84c74f3481f06b~mv2.jpg/v1/fill/w_400,h_450,al_c,q_80/fb9c60_51b2d97bea5c46408f84c74f3481f06b~mv2.jpg",
                "description": "Sikh values in the modern world.",
            },
            {
                "id": "sp-8",
                "title": "The Sikh Portrait — Issue 8",
                "image": "https://static.wixstatic.com/media/fb9c60_73f7c696304643f9aff25b622a24a631~mv2.jpg/v1/fill/w_400,h_450,al_c,q_80/fb9c60_73f7c696304643f9aff25b622a24a631~mv2.jpg",
                "description": "Stories of courage and devotion.",
            },
        ],
        "testimonials": [
            {
                "quote": "Before camp, I didn't do paath, I was unaware of the Guru's teachings, and I didn't feel comfortable being a Sikh. After camp I have noticed a huge change in my attitude and behaviour.",
                "author": "IIGS Camper",
                "camp": "Youth Camp Alumna",
            },
            {
                "quote": "IIGS Camp was my nine-day treasure. It changed my life and connected me with my roots in ways I never imagined possible.",
                "author": "Avleen Kaur",
                "camp": "Camp Alumna",
            },
            {
                "quote": "Being around other kids like him at camp makes him feel like nobody can stop him.",
                "author": "Parent of IIGS Camper",
                "camp": "Camp Parent",
            },
        ],
        "virtual_dewans": {
            "schedule": "1st and 3rd Saturday of every month",
            "time_us": "6:30 PM - 8:00 PM PST",
            "time_india": "7:00 AM - 8:30 AM IST (Sunday)",
            "time_australia": "11:30 AM - 1:00 PM AEST (Sunday)",
            "duration": "90 minutes",
            "total_programs": "179+",
            "platforms": ["YouTube", "Facebook", "Zoom"],
        },
    }


# --- API Routes ---


@app.route("/api/data", methods=["GET"])
def get_all_data():
    return jsonify(load_data())


@app.route("/api/data", methods=["PUT"])
def update_all_data():
    data = request.get_json()
    save_data(data)
    return jsonify({"status": "ok", "message": "Data updated successfully"})


@app.route("/api/<section>", methods=["GET"])
def get_section(section):
    data = load_data()
    if section in data:
        return jsonify(data[section])
    return jsonify({"error": "Section not found"}), 404


@app.route("/api/<section>", methods=["PUT"])
def update_section(section):
    data = load_data()
    data[section] = request.get_json()
    save_data(data)
    return jsonify({"status": "ok", "message": f"{section} updated"})


@app.route("/api/kirtan_library", methods=["POST"])
def add_kirtan():
    data = load_data()
    new_kirtan = request.get_json()
    new_kirtan["id"] = f"kirtan-{len(data['kirtan_library']) + 1}"
    data["kirtan_library"].append(new_kirtan)
    save_data(data)
    return jsonify({"status": "ok", "id": new_kirtan["id"]}), 201


@app.route("/api/contact", methods=["POST"])
def contact_form():
    form_data = request.get_json()
    # Log contact form submissions
    log_file = os.path.join(os.path.dirname(__file__), "contact_log.json")
    submissions = []
    if os.path.exists(log_file):
        with open(log_file, "r", encoding="utf-8") as f:
            submissions = json.load(f)
    form_data["timestamp"] = datetime.now().isoformat()
    submissions.append(form_data)
    with open(log_file, "w", encoding="utf-8") as f:
        json.dump(submissions, f, indent=2, ensure_ascii=False)
    return jsonify({"status": "ok", "message": "Message received! We'll get back to you soon."})


@app.route("/api/register", methods=["POST"])
def camp_registration():
    form_data = request.get_json()
    log_file = os.path.join(os.path.dirname(__file__), "registrations.json")
    registrations = []
    if os.path.exists(log_file):
        with open(log_file, "r", encoding="utf-8") as f:
            registrations = json.load(f)
    form_data["timestamp"] = datetime.now().isoformat()
    registrations.append(form_data)
    with open(log_file, "w", encoding="utf-8") as f:
        json.dump(registrations, f, indent=2, ensure_ascii=False)
    return jsonify({"status": "ok", "message": "Registration submitted successfully!"})


@app.route("/api/newsletter", methods=["POST"])
def newsletter_signup():
    form_data = request.get_json()
    log_file = os.path.join(os.path.dirname(__file__), "newsletter.json")
    subs = []
    if os.path.exists(log_file):
        with open(log_file, "r", encoding="utf-8") as f:
            subs = json.load(f)
    form_data["timestamp"] = datetime.now().isoformat()
    subs.append(form_data)
    with open(log_file, "w", encoding="utf-8") as f:
        json.dump(subs, f, indent=2, ensure_ascii=False)
    return jsonify({"status": "ok", "message": "Subscribed!"})


# --- Admin Panel ---


@app.route("/admin")
def admin_panel():
    return render_template_string(ADMIN_HTML)


# --- Serve Frontend ---


@app.route("/")
def serve_index():
    return send_from_directory(FRONTEND_DIR, "index.html")


@app.route("/<path:path>")
def serve_static(path):
    return send_from_directory(FRONTEND_DIR, path)


ADMIN_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>IIGS Admin Panel</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <script>
    tailwind.config = {
      theme: {
        extend: {
          colors: {
            wheat: { 50: '#FEFCF6', 500: '#D4A017', 600: '#B8860B' },
            bark: { 50: '#FAF5EB', 100: '#F0E6D0', 700: '#5C4A32', 800: '#3D2E1C', 900: '#2C1E0F' },
            khanda: { 50: '#FBF7EE', 100: '#F5ECDA', 400: '#D4A017', 500: '#B8860B' },
          },
        },
      },
    }
  </script>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
  <style>body { font-family: Inter, sans-serif; }</style>
</head>
<body class="bg-bark-50 min-h-screen">
  <nav class="bg-bark-900 text-white px-6 py-4 flex items-center justify-between">
    <div class="flex items-center gap-3">
      <span class="text-xl font-bold text-khanda-400">IIGS</span>
      <span class="text-white/60 text-sm">Admin Panel</span>
    </div>
    <a href="/" class="text-white/60 hover:text-white text-sm">View Site &rarr;</a>
  </nav>

  <div class="max-w-5xl mx-auto px-4 py-8">
    <div class="mb-6 flex gap-2 flex-wrap" id="tabs">
      <button onclick="showTab('site')" class="tab-btn active">Site Info</button>
      <button onclick="showTab('events')" class="tab-btn">Events</button>
      <button onclick="showTab('camps')" class="tab-btn">Camps</button>
      <button onclick="showTab('scholarships')" class="tab-btn">Scholarships</button>
      <button onclick="showTab('kirtan')" class="tab-btn">Kirtan Library</button>
      <button onclick="showTab('portraits')" class="tab-btn">Sikh Portraits</button>
      <button onclick="showTab('testimonials')" class="tab-btn">Testimonials</button>
      <button onclick="showTab('dewans')" class="tab-btn">Virtual Dewans</button>
      <button onclick="showTab('submissions')" class="tab-btn">Submissions</button>
    </div>

    <div id="content" class="bg-white rounded-xl shadow-md p-6 border border-bark-100">
      <div id="loading" class="text-center py-12 text-bark-400">Loading data...</div>
    </div>

    <div id="status" class="mt-4 text-center text-sm hidden"></div>
  </div>

  <style>
    .tab-btn { padding: 0.5rem 1rem; border-radius: 0.5rem; font-size: 0.875rem; font-weight: 500; background: white; color: #5C4A32; border: 1px solid #E8DCC8; transition: all 0.2s; }
    .tab-btn:hover { background: #FBF7EE; }
    .tab-btn.active { background: #D4A017; color: white; border-color: #D4A017; }
    .field-label { display: block; font-size: 0.75rem; font-weight: 600; color: #5C4A32; margin-bottom: 0.25rem; text-transform: uppercase; letter-spacing: 0.05em; }
    .field-input { width: 100%; padding: 0.5rem 0.75rem; border: 1px solid #E8DCC8; border-radius: 0.5rem; font-size: 0.875rem; background: #FDFBF7; }
    .field-input:focus { outline: none; border-color: #D4A017; box-shadow: 0 0 0 2px rgba(212,160,23,0.15); }
    .save-btn { background: #D4A017; color: white; padding: 0.625rem 1.5rem; border-radius: 9999px; font-weight: 600; font-size: 0.875rem; transition: all 0.2s; }
    .save-btn:hover { background: #B8860B; }
    .add-btn { background: #3D2E1C; color: white; padding: 0.5rem 1rem; border-radius: 0.5rem; font-weight: 500; font-size: 0.8125rem; }
    .delete-btn { color: #dc2626; font-size: 0.75rem; font-weight: 500; }
    .item-card { background: #FDFBF7; border: 1px solid #E8DCC8; border-radius: 0.75rem; padding: 1rem; margin-bottom: 0.75rem; }
  </style>

  <script>
    let siteData = {};
    let currentTab = 'site';

    async function loadData() {
      const res = await fetch('/api/data');
      siteData = await res.json();
      showTab('site');
    }

    async function saveAll() {
      const res = await fetch('/api/data', {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(siteData),
      });
      const result = await res.json();
      showStatus(result.message, 'green');
    }

    function showStatus(msg, color) {
      const el = document.getElementById('status');
      el.textContent = msg;
      el.className = 'mt-4 text-center text-sm text-' + color + '-600 font-medium';
      el.classList.remove('hidden');
      setTimeout(() => el.classList.add('hidden'), 3000);
    }

    function showTab(tab) {
      currentTab = tab;
      document.querySelectorAll('.tab-btn').forEach((b, i) => {
        const tabs = ['site','events','camps','scholarships','kirtan','portraits','testimonials','dewans','submissions'];
        b.classList.toggle('active', tabs[i] === tab);
      });

      const el = document.getElementById('content');
      if (tab === 'site') renderSite(el);
      else if (tab === 'events') renderEvents(el);
      else if (tab === 'camps') renderCamps(el);
      else if (tab === 'scholarships') renderScholarships(el);
      else if (tab === 'kirtan') renderKirtan(el);
      else if (tab === 'portraits') renderPortraits(el);
      else if (tab === 'testimonials') renderTestimonials(el);
      else if (tab === 'dewans') renderDewans(el);
      else if (tab === 'submissions') renderSubmissions(el);
    }

    function field(label, value, onchange) {
      return '<div class="mb-3"><label class="field-label">' + label + '</label><input class="field-input" value="' + (value||'').replace(/"/g,'&quot;') + '" onchange="' + onchange + '"></div>';
    }

    function textarea(label, value, onchange) {
      return '<div class="mb-3"><label class="field-label">' + label + '</label><textarea class="field-input" rows="3" onchange="' + onchange + '">' + (value||'') + '</textarea></div>';
    }

    function renderSite(el) {
      const s = siteData.site;
      el.innerHTML = '<h2 class="text-lg font-bold text-bark-800 mb-4">Site Information</h2>' +
        field('Organization Name', s.fullName, "siteData.site.fullName=this.value") +
        field('Tagline', s.tagline, "siteData.site.tagline=this.value") +
        field('Motto', s.motto, "siteData.site.motto=this.value") +
        field('Email', s.email, "siteData.site.email=this.value") +
        field('Address', s.address, "siteData.site.address=this.value") +
        field('Phone', s.phone, "siteData.site.phone=this.value") +
        field('YouTube URL', s.youtube, "siteData.site.youtube=this.value") +
        field('Facebook URL', s.facebook, "siteData.site.facebook=this.value") +
        field('Instagram URL', s.instagram, "siteData.site.instagram=this.value") +
        '<div class="mt-6"><button class="save-btn" onclick="saveAll()">Save Changes</button></div>';
    }

    function renderEvents(el) {
      let html = '<h2 class="text-lg font-bold text-bark-800 mb-4">Events</h2>';
      siteData.events.forEach((e, i) => {
        html += '<div class="item-card">' +
          field('Title', e.title, "siteData.events["+i+"].title=this.value") +
          field('Subtitle', e.subtitle, "siteData.events["+i+"].subtitle=this.value") +
          field('Date (YYYY-MM-DD)', e.date, "siteData.events["+i+"].date=this.value") +
          field('Time', e.time, "siteData.events["+i+"].time=this.value") +
          field('Location', e.location, "siteData.events["+i+"].location=this.value") +
          field('Address', e.address, "siteData.events["+i+"].address=this.value") +
          field('Image URL', e.image, "siteData.events["+i+"].image=this.value") +
          textarea('Description', e.description, "siteData.events["+i+"].description=this.value") +
          '<button class="delete-btn" onclick="siteData.events.splice('+i+',1);showTab(\'events\')">Remove</button></div>';
      });
      html += '<button class="add-btn" onclick="siteData.events.push({id:\'event-\'+Date.now(),title:\'\',subtitle:\'\',date:\'\',time:\'\',location:\'\',address:\'\',image:\'\',description:\'\',active:true});showTab(\'events\')">+ Add Event</button>';
      html += '<div class="mt-6"><button class="save-btn" onclick="saveAll()">Save Changes</button></div>';
      el.innerHTML = html;
    }

    function renderCamps(el) {
      let html = '<h2 class="text-lg font-bold text-bark-800 mb-4">Camps</h2>';
      siteData.camps.forEach((c, i) => {
        html += '<div class="item-card">' +
          field('Title', c.title, "siteData.camps["+i+"].title=this.value") +
          field('Dates', c.dates, "siteData.camps["+i+"].dates=this.value") +
          field('Location', c.location, "siteData.camps["+i+"].location=this.value") +
          field('Address', c.address, "siteData.camps["+i+"].address=this.value") +
          field('Age Range', c.age, "siteData.camps["+i+"].age=this.value") +
          field('Capacity', c.capacity, "siteData.camps["+i+"].capacity=this.value") +
          field('Image URL', c.image, "siteData.camps["+i+"].image=this.value") +
          textarea('Description', c.description, "siteData.camps["+i+"].description=this.value") +
          '<button class="delete-btn" onclick="siteData.camps.splice('+i+',1);showTab(\'camps\')">Remove</button></div>';
      });
      html += '<button class="add-btn" onclick="siteData.camps.push({id:\'camp-\'+Date.now(),title:\'\',dates:\'\',location:\'\',address:\'\',age:\'\',capacity:\'\',image:\'\',description:\'\',activities:[],registrationOpen:true,active:true});showTab(\'camps\')">+ Add Camp</button>';
      html += '<div class="mt-6"><button class="save-btn" onclick="saveAll()">Save Changes</button></div>';
      el.innerHTML = html;
    }

    function renderScholarships(el) {
      const s = siteData.scholarships;
      el.innerHTML = '<h2 class="text-lg font-bold text-bark-800 mb-4">Scholarship Program</h2>' +
        field('Title', s.title, "siteData.scholarships.title=this.value") +
        field('Total Awarded', s.totalAwarded, "siteData.scholarships.totalAwarded=this.value") +
        field('Annual Amount', s.annualAmount, "siteData.scholarships.annualAmount=this.value") +
        field('Application Deadline', s.deadline, "siteData.scholarships.deadline=this.value") +
        '<div class="mt-6"><button class="save-btn" onclick="saveAll()">Save Changes</button></div>';
    }

    function renderKirtan(el) {
      let html = '<h2 class="text-lg font-bold text-bark-800 mb-4">Kirtan Library</h2><p class="text-sm text-bark-400 mb-4">Add kirtan recordings. Use the Facebook Video ID from the video URL.</p>';
      siteData.kirtan_library.forEach((k, i) => {
        html += '<div class="item-card">' +
          field('Title', k.title, "siteData.kirtan_library["+i+"].title=this.value") +
          field('Raagi / Artist', k.raagi, "siteData.kirtan_library["+i+"].raagi=this.value") +
          field('Facebook Video ID', k.facebook_video_id, "siteData.kirtan_library["+i+"].facebook_video_id=this.value") +
          field('Type (e.g. Shabad, Dewan)', k.type, "siteData.kirtan_library["+i+"].type=this.value") +
          field('Duration', k.duration, "siteData.kirtan_library["+i+"].duration=this.value") +
          '<button class="delete-btn" onclick="siteData.kirtan_library.splice('+i+',1);showTab(\'kirtan\')">Remove</button></div>';
      });
      html += '<button class="add-btn" onclick="siteData.kirtan_library.push({id:\'kirtan-\'+Date.now(),title:\'\',raagi:\'\',facebook_video_id:\'\',type:\'\',duration:\'\'});showTab(\'kirtan\')">+ Add Kirtan</button>';
      html += '<div class="mt-6"><button class="save-btn" onclick="saveAll()">Save Changes</button></div>';
      el.innerHTML = html;
    }

    function renderPortraits(el) {
      let html = '<h2 class="text-lg font-bold text-bark-800 mb-4">The Sikh Portrait</h2>';
      siteData.sikh_portraits.forEach((p, i) => {
        html += '<div class="item-card flex gap-4 items-start"><div class="flex-shrink-0"><img src="'+p.image+'" class="w-20 h-24 object-cover rounded" onerror="this.style.display=\'none\'"></div><div class="flex-1">' +
          field('Title', p.title, "siteData.sikh_portraits["+i+"].title=this.value") +
          field('Image URL', p.image, "siteData.sikh_portraits["+i+"].image=this.value") +
          field('Description', p.description, "siteData.sikh_portraits["+i+"].description=this.value") +
          '<button class="delete-btn" onclick="siteData.sikh_portraits.splice('+i+',1);showTab(\'portraits\')">Remove</button></div></div>';
      });
      html += '<button class="add-btn" onclick="siteData.sikh_portraits.push({id:\'sp-\'+Date.now(),title:\'\',image:\'\',description:\'\'});showTab(\'portraits\')">+ Add Portrait</button>';
      html += '<div class="mt-6"><button class="save-btn" onclick="saveAll()">Save Changes</button></div>';
      el.innerHTML = html;
    }

    function renderTestimonials(el) {
      let html = '<h2 class="text-lg font-bold text-bark-800 mb-4">Testimonials</h2>';
      siteData.testimonials.forEach((t, i) => {
        html += '<div class="item-card">' +
          textarea('Quote', t.quote, "siteData.testimonials["+i+"].quote=this.value") +
          field('Author', t.author, "siteData.testimonials["+i+"].author=this.value") +
          field('Camp / Role', t.camp, "siteData.testimonials["+i+"].camp=this.value") +
          '<button class="delete-btn" onclick="siteData.testimonials.splice('+i+',1);showTab(\'testimonials\')">Remove</button></div>';
      });
      html += '<button class="add-btn" onclick="siteData.testimonials.push({quote:\'\',author:\'\',camp:\'\'});showTab(\'testimonials\')">+ Add Testimonial</button>';
      html += '<div class="mt-6"><button class="save-btn" onclick="saveAll()">Save Changes</button></div>';
      el.innerHTML = html;
    }

    function renderDewans(el) {
      const d = siteData.virtual_dewans;
      el.innerHTML = '<h2 class="text-lg font-bold text-bark-800 mb-4">Virtual Dewans</h2>' +
        field('Schedule', d.schedule, "siteData.virtual_dewans.schedule=this.value") +
        field('Time (US)', d.time_us, "siteData.virtual_dewans.time_us=this.value") +
        field('Time (India)', d.time_india, "siteData.virtual_dewans.time_india=this.value") +
        field('Time (Australia)', d.time_australia, "siteData.virtual_dewans.time_australia=this.value") +
        field('Duration', d.duration, "siteData.virtual_dewans.duration=this.value") +
        field('Total Programs', d.total_programs, "siteData.virtual_dewans.total_programs=this.value") +
        '<div class="mt-6"><button class="save-btn" onclick="saveAll()">Save Changes</button></div>';
    }

    async function renderSubmissions(el) {
      let html = '<h2 class="text-lg font-bold text-bark-800 mb-4">Form Submissions</h2>';
      try {
        const contactRes = await fetch('/api/contact-log');
        const regRes = await fetch('/api/registration-log');
        const newsRes = await fetch('/api/newsletter-log');
        html += '<h3 class="font-semibold text-bark-700 mt-4 mb-2">Contact Messages</h3>';
        if (contactRes.ok) {
          const contacts = await contactRes.json();
          contacts.reverse().forEach(c => {
            html += '<div class="item-card text-sm"><strong>' + (c.name||'') + '</strong> (' + (c.email||'') + ')<br>' + (c.subject||'') + '<br><span class="text-bark-400">' + (c.message||'') + '</span><br><span class="text-xs text-bark-300">' + (c.timestamp||'') + '</span></div>';
          });
        } else { html += '<p class="text-bark-400 text-sm">No messages yet.</p>'; }

        html += '<h3 class="font-semibold text-bark-700 mt-4 mb-2">Newsletter Subscribers</h3>';
        if (newsRes.ok) {
          const subs = await newsRes.json();
          subs.reverse().forEach(s => {
            html += '<div class="item-card text-sm">' + (s.email||'') + ' <span class="text-xs text-bark-300">' + (s.timestamp||'') + '</span></div>';
          });
        } else { html += '<p class="text-bark-400 text-sm">No subscribers yet.</p>'; }
      } catch(e) { html += '<p class="text-bark-400 text-sm">Could not load submissions.</p>'; }
      el.innerHTML = html;
    }

    // Submission log API routes
    loadData();
  </script>
</body>
</html>
"""

# Extra routes for admin to view submissions
@app.route("/api/contact-log")
def get_contact_log():
    log_file = os.path.join(os.path.dirname(__file__), "contact_log.json")
    if os.path.exists(log_file):
        with open(log_file, "r", encoding="utf-8") as f:
            return jsonify(json.load(f))
    return jsonify([])


@app.route("/api/registration-log")
def get_registration_log():
    log_file = os.path.join(os.path.dirname(__file__), "registrations.json")
    if os.path.exists(log_file):
        with open(log_file, "r", encoding="utf-8") as f:
            return jsonify(json.load(f))
    return jsonify([])


@app.route("/api/newsletter-log")
def get_newsletter_log():
    log_file = os.path.join(os.path.dirname(__file__), "newsletter.json")
    if os.path.exists(log_file):
        with open(log_file, "r", encoding="utf-8") as f:
            return jsonify(json.load(f))
    return jsonify([])


if __name__ == "__main__":
    # Initialize data file if it doesn't exist
    if not os.path.exists(DATA_FILE):
        save_data(get_default_data())
        print("Created default data.json")

    print("\n  IIGS Website Server")
    print("  ====================")
    print("  Frontend:  http://localhost:5000")
    print("  Admin:     http://localhost:5000/admin")
    print("  API:       http://localhost:5000/api/data")
    print()
    app.run(debug=True, port=5000)
