# Contact Links Design

## Goal

Make the portfolio's email, WhatsApp, and Instagram contact actions open the correct destination when selected.

## Design

The existing contact section remains the single contact entry point. Add three buttons using native anchors:

- Email uses `mailto:renaldybaskara6@gmail.com`.
- WhatsApp uses `https://wa.me/6281272103353`, which opens a direct chat using the international phone format without punctuation.
- Instagram uses the user-provided profile URL and opens in a new tab with `rel="noopener noreferrer"`.

Add the email, WhatsApp, and Instagram destinations to the JSON-LD `Person.sameAs` array while retaining the existing LinkedIn and Upwork profiles.

## Scope and constraints

- Preserve the existing dark portfolio layout and button styling.
- Do not add a contact form, backend, or JavaScript click handler.
- Use the exact user-provided email, phone number, and Instagram URL.
- Keep the existing LinkedIn and Upwork actions unchanged.

## Verification

Extend `tests/verify.py` to assert the exact contact hrefs, the new JSON-LD `sameAs` array, and the presence of the contact labels. Run the full Python verification script after implementation.
