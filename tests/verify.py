#!/usr/bin/env python3
from html.parser import HTMLParser
from pathlib import Path
import json
import re
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
errors = []


def require(condition, message):
    if not condition:
        errors.append(message)


class AuditParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids = set()
        self.links = []
        self.images = []
        self.landmarks = []
        self.metas = []
        self.project_order = []

    def handle_starttag(self, tag, attrs):
        data = dict(attrs)
        if "id" in data:
            self.ids.add(data["id"])
        if tag == "a":
            self.links.append(data)
        if tag == "img":
            self.images.append(data)
        if tag == "meta":
            self.metas.append(data)
        if tag in {"header", "nav", "main", "footer"}:
            self.landmarks.append(tag)
        if data.get("data-project"):
            self.project_order.append(data["data-project"])


index_path = ROOT / "index.html"
styles_path = ROOT / "assets/styles.css"
script_path = ROOT / "assets/main.js"
require(index_path.exists(), "index.html exists")
require(styles_path.exists(), "assets/styles.css exists")
require(script_path.exists(), "assets/main.js exists")

html = index_path.read_text(encoding="utf-8") if index_path.exists() else ""
css = styles_path.read_text(encoding="utf-8") if styles_path.exists() else ""
js = script_path.read_text(encoding="utf-8") if script_path.exists() else ""
parser = AuditParser()
parser.feed(html)

for landmark in ("header", "nav", "main", "footer"):
    require(landmark in parser.landmarks, f"semantic landmark: {landmark}")
for section_id in ("top", "portfolio", "capabilities", "experience", "contact", "project-drawer"):
    require(section_id in parser.ids, f"section exists: {section_id}")

linkedin = "https://www.linkedin.com/in/mrenaldybaskara?trk=contact-info"
upwork = "https://www.upwork.com/freelancers/~01356ddc4dbcc68cb0?companyReference=2062589248382688414&mp_source=share"
email = "mailto:renaldybaskara6@gmail.com"
whatsapp = "https://wa.me/6281272103353"
instagram = "https://www.instagram.com/renaldybaskara?igsh=ZHhtNmtpYXdxajly&utm_source=qr"
booking_source = "https://github.com/renaldybaskara/bookingcalendar"
vehicle_source = "https://github.com/renaldybaskara/rent-car"
hrefs = [link.get("href", "") for link in parser.links]
for href, label in (
    (linkedin, "exact LinkedIn link"),
    (upwork, "exact Upwork link"),
    (email, "exact email link"),
    (whatsapp, "exact WhatsApp link"),
    (instagram, "exact Instagram link"),
    (booking_source, "Booking Calendar source link"),
    (vehicle_source, "Vehicle Management source link"),
):
    require(href in hrefs or href in html, label)

require("Explore my portfolio" in html, "hero portfolio CTA")
require("Send WhatsApp" in html, "hero WhatsApp CTA")
for label in ("View CV", "LinkedIn", "Upwork", "Email"):
    require(label in html, f"large hero professional link: {label}")
require('href="Muhammad_Renaldy_Baskara_CV.pdf"' in html, "CV link")

require("Senior Backend Engineer / Technical Lead" in html, "current role wording")
require("Backend Engineering" in html, "core domain wording")
require("Scalable" in html and "High Concurrency" in html and "Production Grade" in html, "focus wording")
require("PAYMENT ECOSYSTEM" not in html.upper(), "payment ecosystem proof card removed")
require("200,000" not in html and "200.000" not in html, "200k EDC metric removed")
require(re.search(r"ISO\s?8583 messages?", html, re.I), "ISO 8583 described as messages")
require(not re.search(r"ISO\s?8583\s+flows?", html, re.I), "ISO 8583 is not described as a flow")

expected_project_order = ["edc", "budgetin", "sayar", "echannel", "calendar", "vehicle"]
require(parser.project_order == expected_project_order, "project order is EDC, Budgetin, MB Sayar, E-Channel, Calendar, Vehicle")
for project_name in (
    "EDC Merchant Payment Platform",
    "Budgetin",
    "MB Sayar",
    "BRI E-Channel Monitoring Portal",
    "Automatic Booking Calendar",
    "Vehicle Management App",
):
    require(project_name in html, f"project present: {project_name}")

for phrase in ("Mastercard", "Visa", "JCB", "QRIS", "ProSwitching", "REST API messages (JSON)", "Kafka", "OpenShift", "Elasticsearch", "Kibana", "MySQL", "PostgreSQL"):
    require(phrase in html, f"EDC project content: {phrase}")
for phrase in ("React Native", "Expo", "AI-powered", "OCR", "Stripe", "Async processing", "Cloud server"):
    require(phrase in html, f"Budgetin project content: {phrase}")
require("Laravel" in html and "confidential" in html.lower(), "confidential Laravel E-Channel summary")
for phrase in ("FullCalendar", "iCal", "conflict detection", "Node.js", "Express"):
    require(phrase in html, f"Booking Calendar content: {phrase}")
for phrase in ("C#", "WinForms", "Laravel Sanctum", "invoice"):
    require(phrase in html, f"Vehicle Management content: {phrase}")
for phrase in ("Jetpack Compose", "NetworkStatsManager", "Room", "local-first"):
    require(phrase in html, f"MB Sayar content: {phrase}")

project_json_match = re.search(r'<script id="project-data" type="application/json">(.*?)</script>', html, re.S)
try:
    project_data = json.loads(project_json_match.group(1)) if project_json_match else {}
except json.JSONDecodeError:
    project_data = {}
require(list(project_data) == expected_project_order, "project JSON order matches visible rail")
require(project_data.get("sayar", {}).get("actions") == [], "MB Sayar has no external source button")
require(len(project_data.get("sayar", {}).get("images", [])) >= 3, "MB Sayar has a multi-image gallery")
require(project_data.get("calendar", {}).get("actions", [{}])[0].get("url") == booking_source, "Calendar JSON source URL")
require(project_data.get("vehicle", {}).get("actions", [{}])[0].get("url") == vehicle_source, "Vehicle JSON source URL")

for heading in ("Senior Backend Developer", "Professional Web Developer", "Professional Full-Stack Developer"):
    require(heading in html, f"capability: {heading}")
require("capability-media" not in html, "capability cards contain no project pictures")

require("April 2024" in html and "Present" in html, "current BRI role dates")
require("April 2021" in html and "April 2024" in html, "prior BRI role dates")
require("part-time" in html.lower() and "full-time" in html.lower() and "remote" in html.lower(), "availability message")

full_name = "Muhammad Renaldy Baskara"
canonical = "https://famledger.my.id/renaldybaskara/"
require(html.count(full_name) >= 3, "full name appears throughout public site")
require('rel="canonical" href="' + canonical + '"' in html, "canonical URL")
meta_properties = {item.get("property"): item.get("content") for item in parser.metas if item.get("property")}
require(meta_properties.get("og:type") == "website", "Open Graph website type")
require(meta_properties.get("og:url") == canonical, "Open Graph canonical URL")
require(full_name in meta_properties.get("og:title", ""), "Open Graph full name")
json_ld_blocks = re.findall(r'<script type="application/ld\+json">(.*?)</script>', html, re.S)
try:
    person = json.loads(json_ld_blocks[0]) if json_ld_blocks else {}
except json.JSONDecodeError:
    person = {}
require(person.get("@type") == "Person", "JSON-LD Person type")
require(person.get("name") == full_name, "JSON-LD full name")
require(person.get("url") == canonical, "JSON-LD canonical URL")
require(person.get("sameAs") == [linkedin, upwork, email, whatsapp, instagram], "JSON-LD exact public profiles and contacts")
require(person.get("worksFor", {}).get("name") == "Bank Rakyat Indonesia", "JSON-LD current employer")
emails = re.findall(r"[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}", html)
require(set(emails) == {"renaldybaskara6@gmail.com"}, "only the approved email is used")

for image in parser.images:
    require(bool(image.get("alt")), "all images have non-empty alt text")
image_sources = [image.get("src") for image in parser.images]
require(image_sources.count("assets/bri-logo-full.jpg") == 2, "BRI logo appears for both roles")
require(image_sources.count("assets/profile-photo.jpeg") == 1, "profile portrait appears once")
required_assets = (
    "assets/profile-photo.jpeg",
    "assets/edc-merchant-payment.png",
    "assets/famledger-financial-management.png",
    "assets/booking-calendar-ui.png",
    "assets/mb-sayar-list.png",
    "assets/mb-sayar-create.png",
    "assets/mb-sayar-detail.png",
    "assets/vehicle-management-ui.svg",
)
for asset in required_assets:
    require((ROOT / asset).exists(), f"asset exists: {asset}")

for selector in ("scroll-snap-type", "prefers-reduced-motion", ".project-drawer", ".professional-links"):
    require(selector in css, f"CSS behavior/style present: {selector}")
for behavior in ("setInterval", "visibilitychange", "Escape", "openProject", "closeProject", "moveGallery", "focus"):
    require(behavior in js, f"JavaScript behavior present: {behavior}")

require(".superpowers/" in (ROOT / ".gitignore").read_text(encoding="utf-8"), "local mockups are ignored")
tracked = subprocess.run(["git", "ls-files", ".superpowers", "docs/superpowers"], cwd=ROOT, capture_output=True, text=True)
require(not tracked.stdout.strip(), "no superpowers files are tracked")

pdf = ROOT / "Muhammad_Renaldy_Baskara_CV.pdf"
require(pdf.exists(), "PDF CV exists")
if pdf.exists():
    if shutil.which("pdftotext"):
        result = subprocess.run(["pdftotext", "-layout", str(pdf), "-"], capture_output=True, text=True)
        require(result.returncode == 0, "PDF text extraction succeeds")
        pdf_text = result.stdout
    else:
        from pypdf import PdfReader
        pdf_text = "\n".join(page.extract_text() or "" for page in PdfReader(str(pdf)).pages)
        require(bool(pdf_text.strip()), "PDF text extraction succeeds")
    for phrase in (full_name, "Senior Backend Engineer", "Bank Rakyat Indonesia", "IT Manager", "IT Junior Manager"):
        require(phrase in pdf_text, f"PDF contains: {phrase}")

for source in (ROOT / "cv/Renaldy_Baskara_CV.html", ROOT / "cv/generate_cv.py"):
    require(source.exists() and full_name in source.read_text(encoding="utf-8"), f"full name in {source.relative_to(ROOT)}")

if errors:
    print("VERIFICATION FAILED")
    for error in errors:
        print(f"- {error}")
    sys.exit(1)
print("VERIFICATION PASSED: redesign content, accessibility, assets, links, project data, and PDF")
