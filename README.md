# Iskra Services — website prototype

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

The advisor sits in a closable chat widget rather than a dedicated section — the
site reads as a site, and the advisor is there when it's wanted.

### The advisor

- Conversational assessment — no forms; it picks the next two questions from
  what it still needs to know
- One case file, built from the conversation and reused at every stage, so
  nothing is asked twice
- Route scoring (Innovator Founder, Global Talent, self-sponsorship, Expansion
  Worker) with the reasoning shown behind every score
- Business assessment, gap analysis and a prioritised action plan
- Regulated-advice detection — it stops and routes to an IAA-registered adviser
  rather than answering
- An adviser handover brief generated from the case file
- Iskra's services ranked against the case rather than listed as a menu

### Also included

- Login flow — email, Google, password reset, signed-in state (mocked; see below)
- Demo reset controls, so the prototype can be presented repeatedly from a clean
  slate

## Running it

It is a single self-contained `index.html`. Open the file directly, or:

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
— *"Scripted demo · replies are pre-written"*. The conversation still
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
index.html    the entire site — markup, styles and behaviour
.nojekyll     tells GitHub Pages to serve the file as-is
```

## Status

Prototype, v2.2. Search engines are excluded via `robots` metadata so this
cannot be confused with the live iskra.services site.
