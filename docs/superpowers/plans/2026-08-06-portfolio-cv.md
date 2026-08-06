# Renaldy Baskara Portfolio and CV Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build and verify a responsive static portfolio and ATS-friendly English PDF CV using only the verified profile brief.

**Architecture:** Semantic static HTML is styled with one local CSS file and enhanced by a small local JavaScript file. A separate print-optimized HTML source produces the PDF, while a Python verification script tests both deliverables at their observable boundaries.

**Tech Stack:** HTML5, CSS3, vanilla JavaScript, Python standard library, Chromium/print-to-PDF, pdftotext.

## Global Constraints

- Use only factual source material in `PROFILE_BRIEF.md`.
- Do not expose the source brief as a website route.
- Do not invent contact details, education, certifications, client names, or metrics.
- Make the website responsive and accessible and the CV English, clean, and machine-readable.

---

### Task 1: Verification contract

**Files:**
- Create: `tests/verify.py`

**Interfaces:**
- Consumes: `index.html`, `assets/styles.css`, `assets/main.js`, `Renaldy_Baskara_CV.pdf`
- Produces: process exit status and named verification results

- [ ] Write structural and content checks before deliverables exist.
- [ ] Run `python3 tests/verify.py` and confirm missing-artifact failures.
- [ ] Keep checks independently derived from the brief.

### Task 2: Portfolio website

**Files:**
- Create: `index.html`
- Create: `assets/styles.css`
- Create: `assets/main.js`

**Interfaces:**
- Produces: static website opening directly from disk or any static host

- [ ] Implement semantic content and exact public profile links.
- [ ] Implement responsive, high-contrast styling and keyboard focus states.
- [ ] Add progressive enhancement with reduced-motion support.
- [ ] Run `python3 tests/verify.py`; website checks must pass while PDF checks remain pending.

### Task 3: ATS-friendly PDF CV

**Files:**
- Create: `cv/Renaldy_Baskara_CV.html`
- Create: `Renaldy_Baskara_CV.pdf`

**Interfaces:**
- Produces: searchable English PDF with conventional single-column reading order

- [ ] Create the print source using only brief-backed statements.
- [ ] Generate PDF with local tooling.
- [ ] Extract text with `pdftotext` and inspect reading order.

### Task 4: Rendered verification and polish

**Files:**
- Modify only files implicated by verification findings.

**Interfaces:**
- Consumes: all deliverables
- Produces: verified desktop/mobile website and readable PDF

- [ ] Run the complete automated suite.
- [ ] Render website at desktop and mobile widths and inspect screenshots and browser console.
- [ ] Render PDF pages and inspect for clipping or layout faults.
- [ ] Re-run the complete suite after any fixes.

