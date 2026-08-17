# Contact Links Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add working email, WhatsApp, and Instagram contact actions to the static portfolio and verify their exact destinations.

**Architecture:** Keep the current static HTML contact section and represent each destination as a native anchor. Update the page's JSON-LD profile metadata and the existing Python audit so the behavior is explicit and regression-tested.

**Tech Stack:** HTML, JSON-LD, Python standard-library HTML parser and assertions.

## Global Constraints

- Use the exact email `renaldybaskara6@gmail.com`.
- Use the WhatsApp direct-chat URL `https://wa.me/6281272103353`.
- Use the supplied Instagram URL `https://www.instagram.com/renaldybaskara?igsh=ZHhtNmtpYXdxajly&utm_source=qr`.
- Preserve existing LinkedIn and Upwork links and the current visual styling.
- Do not add a backend, contact form, or JavaScript click handler.

---

### Task 1: Add contact-link regression coverage

**Files:**
- Modify: `tests/verify.py`

**Interfaces:**
- Consumes: Parsed anchors from `index.html` and the existing JSON-LD `Person` object.
- Produces: Assertions that fail until all three contact destinations and labels are present.

- [ ] **Step 1: Add exact contact constants and href assertions**

Add these values next to the existing `linkedin` and `upwork` constants, then assert each exact href is present in `hrefs` and each label appears in the HTML:

```python
email = "mailto:renaldybaskara6@gmail.com"
whatsapp = "https://wa.me/6281272103353"
instagram = "https://www.instagram.com/renaldybaskara?igsh=ZHhtNmtpYXdxajly&utm_source=qr"
require(email in hrefs, "exact email link")
require(whatsapp in hrefs, "exact WhatsApp link")
require(instagram in hrefs, "exact Instagram link")
require("Email me" in html, "email contact label")
require("Message on WhatsApp" in html, "WhatsApp contact label")
require("Instagram" in html, "Instagram contact label")
```

- [ ] **Step 2: Update the expected JSON-LD sameAs array**

Replace the existing exact `sameAs` assertion with:

```python
require(person.get("sameAs") == [linkedin, upwork, email, whatsapp, instagram], "JSON-LD exact public profiles and contact links")
```

- [ ] **Step 3: Run the focused verification to confirm RED**

Run: `python tests/verify.py`

Expected: `VERIFICATION FAILED` with failures for the exact email, WhatsApp, and Instagram links, their labels, and the expanded JSON-LD array.

### Task 2: Implement the approved contact actions

**Files:**
- Modify: `index.html:10` for JSON-LD metadata.
- Modify: `index.html:109` for the contact action anchors.

**Interfaces:**
- Consumes: The exact contact constants from Task 1.
- Produces: Native HTML links that launch email, WhatsApp chat, and Instagram.

- [ ] **Step 1: Extend JSON-LD sameAs**

Set the JSON-LD `sameAs` value to:

```json
["https://www.linkedin.com/in/mrenaldybaskara?trk=contact-info","https://www.upwork.com/freelancers/~01356ddc4dbcc68cb0?companyReference=2062589248382688414&mp_source=share","mailto:renaldybaskara6@gmail.com","https://wa.me/6281272103353","https://www.instagram.com/renaldybaskara?igsh=ZHhtNmtpYXdxajly&utm_source=qr"]
```

- [ ] **Step 2: Add the three contact anchors**

Add these anchors inside `.contact-actions` after the existing Upwork anchor:

```html
<a class="button button-secondary" href="mailto:renaldybaskara6@gmail.com">Email me <span aria-hidden="true">↗</span></a>
<a class="button button-secondary" href="https://wa.me/6281272103353" target="_blank" rel="noopener noreferrer">Message on WhatsApp <span aria-hidden="true">↗</span></a>
<a class="button button-secondary" href="https://www.instagram.com/renaldybaskara?igsh=ZHhtNmtpYXdxajly&amp;utm_source=qr" target="_blank" rel="noopener noreferrer">Instagram <span aria-hidden="true">↗</span></a>
```

### Task 3: Verify and review

**Files:**
- Inspect: `index.html`
- Inspect: `tests/verify.py`

**Interfaces:**
- Consumes: Implemented HTML and verification assertions.
- Produces: Fresh evidence that all existing and new portfolio requirements pass.

- [ ] **Step 1: Run the full verification suite**

Run: `python tests/verify.py`

Expected: exit code 0 and `VERIFICATION PASSED: website structure, factual constraints, assets, links, and PDF text`.

- [ ] **Step 2: Check the final diff for scope and whitespace**

Run: `git diff --check; git diff -- index.html tests/verify.py`

Expected: no whitespace errors and only the approved metadata, contact anchors, and verification changes.
