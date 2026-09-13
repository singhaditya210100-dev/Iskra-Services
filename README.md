# Iskra Services: website & founder platform prototype

A concept website prototype for **Iskra Services** (a trading name of Indigenous
Consultants Limited, Harrow), a UK business-services firm working with
international founders.

**Live preview:** https://singhaditya210100-dev.github.io/Iskra-Services/

> This is a design prototype, not a live service. It does not take instructions
> or payment, and nothing on it constitutes regulated immigration advice.
> Figures and timescales shown are illustrative.

## What it is

The current Iskra site lists six services and leaves the visitor to work out
which one they need. This prototype inverts that: the visitor states an
objective, and an AI advisor works out the services.

Three access levels, progressively unlocked: a route-agnostic public site with a
limited free advisor (the demo's answers are prefilled), a free founder account
that starts with nine assessment questions, and three paid preparation plans
(Business Assessment, Business Plan & Preparation, Endorsement Readiness), then
an external, independent endorsing body. Each route has its own page with the
official GOV.UK sources. The advisor floats as a
closable chat widget everywhere.

### The advisor

- Conversational assessment, no forms; it picks the next two questions from
  what it still needs to know
- One case file, built from the conversation and reused at every stage, so
  nothing is asked twice
- Route scoring (Innovator Founder, Global Talent, self-sponsorship, Expansion
  Worker) with the reasoning shown behind every score
- Business assessment, gap analysis and a prioritised action plan
- Regulated-advice detection, it stops and routes to an IAA-registered adviser
  rather than answering
- An adviser handover brief generated from the case file
- Iskra's services ranked against the case rather than listed as a menu

### Also included

- Login flow, email, Google, password reset, signed-in state (mocked; see below)
- Demo reset controls, so the prototype can be presented repeatedly from a clean
  slate

## Picking this up

[`CLAUDE.md`](CLAUDE.md) holds the working context: the client brief and how
each of its requirements is met, the design direction, how the advisor is
wired, the two-build gotcha, and what is still open. A Claude Code session
started in this directory loads it automatically.

## What's new in v4

- Pre-login: generic homepage for every route; the advisor collects basics,
  recommends Innovator Founder, and gates to sign-up naming the nine areas
- Post-login: nine-question intake **before** the dashboard (skippable); a
  horizontal milestone map; a dashboard that shows only the current step
- Business Assessment with I/V/S inside it, every area expandable, PDF export
- AI-generated business plan linked section-by-section to the assessment, PDF
- "Strengthen your case": company formation, eight specialists, IAA adviser
- Stripe-style test-mode checkout with receipts (no card is charged)
- Post-Endorsement removed for now

## Running it

It is a single self-contained `index.html`, assembled from `parts/`:

```sh
cat parts/01-head.html parts/02-site.html parts/03-app.html parts/04-js.html > index.html
```

Edit the parts, rebuild, then open the file directly, or:

```sh
python3 -m http.server 8000
# then visit http://localhost:8000
```

No build step, no dependencies. Archivo is loaded from Google Fonts; everything
else ships in the file.

## Two things that are deliberately not real

**The AI advisor falls back to a scripted walkthrough here.** The live version
calls Claude through the artifact runtime (`window.claude`), which only exists
inside the claude.ai viewer. On GitHub Pages that call returns nothing, so the
widget switches to a pre-written walkthrough and says so in its own status line
,  *"Scripted demo · replies are pre-written"*. The conversation still
demonstrates the full journey. For the live model, use the artifact build.

**The login is a mock.** No account is created and nothing is sent anywhere.
Name and email go into browser storage only; passwords are never stored. It
exists to show the flow, not to authenticate anyone.

## Resetting for a demo

State is kept in the viewer's own browser, so a demo needs a way back to a clean
slate:

| Control | Where | Clears |
| --- | --- | --- |
| ↻ | Chat widget header | Conversation and case file, stays signed in |
| Reset demo | Footer | Everything, including the account |
| `?demo` | On the URL | Everything, on load |

Both buttons arm on the first click and act on the second.

## Structure

```
index.html          the whole site + app, built from parts/, commit both
parts/01-head.html  head and all CSS
parts/02-site.html  pre-login marketing site
parts/03-app.html   post-login app shell, modals, chat widget
parts/04-js.html    state, advisor, modules, checkout, auth
CLAUDE.md           working context for the next session
.nojekyll           tells GitHub Pages to serve the file as-is
```

## Status

Prototype, v4.0. Search engines are excluded via `robots` metadata so this
cannot be confused with the live iskra.services site.
