#!/usr/bin/env python3
from pathlib import Path
from html.parser import HTMLParser
import json
import re
import subprocess
import shutil
import sys

ROOT = Path(__file__).resolve().parents[1]
errors = []

def require(condition, message):
    if not condition:
        errors.append(message)

class AuditParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids, self.links, self.images = set(), [], []
        self.landmarks, self.metas, self.scripts = [], [], []
    def handle_starttag(self, tag, attrs):
        data = dict(attrs)
        if "id" in data: self.ids.add(data["id"])
        if tag == "a": self.links.append(data)
        if tag == "img": self.images.append(data)
        if tag == "meta": self.metas.append(data)
        if tag == "script": self.scripts.append(data)
        if tag in {"header", "nav", "main", "footer"}: self.landmarks.append(tag)

index_path = ROOT / "index.html"
require(index_path.exists(), "index.html exists")
html = index_path.read_text(encoding="utf-8") if index_path.exists() else ""
parser = AuditParser(); parser.feed(html)

for landmark in ("header", "nav", "main", "footer"):
    require(landmark in parser.landmarks, f"semantic landmark: {landmark}")
for section_id in ("about", "experience", "projects", "skills", "contact"):
    require(section_id in parser.ids, f"section exists: {section_id}")

linkedin = "https://www.linkedin.com/in/mrenaldybaskara?trk=contact-info"
upwork = "https://www.upwork.com/freelancers/~01356ddc4dbcc68cb0?companyReference=2062589248382688414&mp_source=share"
email = "mailto:renaldybaskara8@gmail.com"
whatsapp = "https://wa.me/6281272103353"
instagram = "https://www.instagram.com/renaldybaskara?igsh=ZHhtNmtpYXdxajly&utm_source=qr"
hrefs = [link.get("href", "") for link in parser.links]
require(linkedin in hrefs, "exact LinkedIn link")
require(upwork in hrefs, "exact Upwork link")
require(email in hrefs, "exact email link")
require(whatsapp in hrefs, "exact WhatsApp link")
require(instagram in hrefs, "exact Instagram link")
require("Email me" in html, "email contact label")
require("Message on WhatsApp" in html, "WhatsApp contact label")
require("Instagram" in html, "Instagram contact label")
require("April 2024" in html and "Present" in html, "current role dates")
require("April 2021" in html and "April 2024" in html, "prior role dates")
require("part-time" in html.lower() and "full-time" in html.lower() and "remote" in html.lower(), "availability message")
require("200,000" in html and "EDC" in html, "verified EDC context")
require("React.js" in html and "TypeScript" in html, "website Languages include React.js and TypeScript")
require("Working Style" not in html and "Accountable" not in html and "Detail Oriented" not in html, "website omits working style")
require("PROFILE_BRIEF" not in html, "source brief is not exposed")
full_name = "Muhammad Renaldy Baskara"
canonical = "https://famledger.my.id/renaldybaskara/"
require(html.count(full_name) >= 5, "full name appears throughout public site")
require(re.search(r'<p class="hero-name">Muhammad Renaldy Baskara</p>', html) is not None, "full name is prominent in hero")
require('rel="canonical" href="' + canonical + '"' in html, "accurate canonical URL")
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
require(person.get("sameAs") == [linkedin, upwork, email, whatsapp, instagram], "JSON-LD exact public profiles and contact links")
require(person.get("worksFor", {}).get("name") == "Bank Rakyat Indonesia", "JSON-LD current employer")
emails = re.findall(r"[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}", html)
require(set(emails) == {"renaldybaskara8@gmail.com"}, "only supplied email is used")
visible_html = re.sub(r'<script\b[^>]*>.*?</script>', ' ', html, flags=re.S)
visible_html = re.sub(r'<[^>]+>', ' ', visible_html)
require(not re.search(r"(?:\+?\d[\s().-]*){8,}", re.sub(r"200,000\+?", "", visible_html)), "no invented phone number")
for image in parser.images:
    require(bool(image.get("alt")), "all images have non-empty alt text")
image_sources = [image.get("src") for image in parser.images]
require(image_sources.count("assets/bri-logo-full.jpg") == 2, "BRI logo appears for both BRI roles")
require("assets/edc-merchant-payment.jpg" not in image_sources and "assets/wpe-echannel-logo.jpg" not in image_sources, "EDC and WPE project images are omitted")
require(not (ROOT / "assets/renaldy-baskara.jpg").exists(), "portrait asset removed")
for local_ref in ("assets/styles.css", "assets/main.js"):
    require((ROOT / local_ref).exists(), f"local asset exists: {local_ref}")

pdf = ROOT / "Muhammad_Renaldy_Baskara_CV.pdf"
require(pdf.exists(), "PDF CV exists")
if pdf.exists():
    if shutil.which("pdftotext"):
        result = subprocess.run(["pdftotext", "-layout", str(pdf), "-"], capture_output=True, text=True)
        require(result.returncode == 0, "PDF text extraction succeeds")
        text = result.stdout
    else:
        from pypdf import PdfReader
        text = "\n".join(page.extract_text() or "" for page in PdfReader(str(pdf)).pages)
        require(bool(text.strip()), "PDF text extraction succeeds")
    for phrase in (full_name, "Senior Backend Engineer", "Bank Rakyat Indonesia", "IT Manager", "IT Junior Manager", "Payment Gateway Development", "LinkedIn", "Upwork"):
        require(phrase in text, f"PDF contains: {phrase}")
    require("April 2024 - Present" in text, "PDF current role dates")
    require("April 2021 - April 2024" in text, "PDF prior role dates")
    require("React.js" in text and "TypeScript" in text, "PDF Languages include React.js and TypeScript")
    require("Working Style" not in text and "Accountable for Outcomes" not in text and "Detail Oriented" not in text, "PDF omits working style")
    require("@" not in text, "PDF has no invented email")
    try:
        from pypdf import PdfReader
        metadata = PdfReader(str(pdf)).metadata
        require(metadata.title == f"{full_name} CV", "PDF metadata title uses full name")
        require(metadata.author == full_name, "PDF metadata author uses full name")
    except ImportError:
        errors.append("pypdf available for PDF metadata verification")

for source in (ROOT / "PROFILE_BRIEF.md", ROOT / "cv/Renaldy_Baskara_CV.html", ROOT / "cv/generate_cv.py"):
    require(full_name in source.read_text(encoding="utf-8"), f"full name in {source.relative_to(ROOT)}")

if errors:
    print("VERIFICATION FAILED")
    for error in errors: print(f"- {error}")
    sys.exit(1)
print("VERIFICATION PASSED: website structure, factual constraints, assets, links, and PDF text")
