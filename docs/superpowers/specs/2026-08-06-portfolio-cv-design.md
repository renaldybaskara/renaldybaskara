# Renaldy Baskara Portfolio and CV Design

## Purpose

Create two polished, factual career assets from `PROFILE_BRIEF.md`: a responsive static portfolio and an English ATS-friendly PDF CV. Both prioritize payment engineering, backend/software engineering, and technical leadership without adding unsupported facts.

## Information architecture

The website is a single semantic page with skip navigation, a compact header, hero positioning, verified impact context, capability overview, formal experience timeline, project summaries, grouped skills, availability, and public profile links. LinkedIn and Upwork are the only contact channels. The source brief remains a project file and is never linked or copied into a public web directory.

The CV uses a conventional single-column reading order: identity and headline, public links, summary, core competencies, professional experience, selected projects, technical skills, and availability. It omits contact, education, certification, location, client, and metrics not in the brief.

## Visual system

Use a technical editorial style inspired by payment infrastructure: deep navy surfaces, warm amber signals, cool off-white content, fine grid/rail details, strong typographic hierarchy, and restrained motion. Local/system fonts avoid third-party requests. Components remain readable without JavaScript, keyboard operable, high contrast, and responsive down to narrow mobile screens.

## Implementation

- `index.html`: semantic content and metadata.
- `assets/styles.css`: responsive layout, accessibility states, visual system, and reduced-motion handling.
- `assets/main.js`: progressive enhancement for current year and section reveal only; no content dependency.
- `cv/Renaldy_Baskara_CV.html`: print source for the PDF.
- `Renaldy_Baskara_CV.pdf`: generated CV artifact.
- `tests/verify.py`: structural, factual, link, accessibility-baseline, and PDF-text checks.

## Verification

Automated checks validate required sections, exact public links, factual boundaries, semantic landmarks, absence of invented contact fields, local asset references, and extracted PDF text. Local browser rendering is checked at desktop and mobile widths, including console errors. PDF rendering and text extraction are inspected for clipping, page count, machine-readable order, and required content.

