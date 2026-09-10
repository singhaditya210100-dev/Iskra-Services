# Iskra Services prototype — working context

Handoff notes so this can be picked up in a fresh session. Read this before
editing anything.

---

## 1. What this is

A concept website prototype built by **Finfactor** for a client, **Iskra
Services** — a UK business-services firm in Harrow working mainly with
international founders (company setup, Innovator Founder visa support,
accounting/tax, funding, web, remote staffing).

Their current site (iskra.services) lists six services and leaves the visitor to
work out which one they need. **The prototype inverts that**: the visitor states
an objective and an AI advisor works out the services. The advisor is the
product thesis, but it lives in a closable chat widget — the site reads as a
site, and the advisor is there when wanted.

Status: **v2.2**, design prototype. Not a live service, no backend, nothing
regulated.

## 2. Where everything is

| | |
| --- | --- |
| Live site (GitHub Pages) | https://singhaditya210100-dev.github.io/Iskra-Services/ |
| Repo | https://github.com/singhaditya210100-dev/Iskra-Services |
| Local clone | `~/iskra-services-site` (dir name differs from repo — harmless) |
| **Artifact build (live AI)** | https://claude.ai/code/artifact/7f93ec36-a07f-48e1-a8a3-366295cbf6e6 |
| Original client brief | `~/Downloads/Client req.docx` |
| Costed proposal | `~/Desktop/Iskra Services - Website & AI Advisor Proposal.xlsx` |

**There are two builds of the same page** and the difference matters — see §6.

## 3. Client facts (verified from their site and Companies House)

- Iskra.services is a trading name of **Indigenous Consultants Limited**,
  registered in England & Wales, **no. 16043340**
- 79 College Road, Harrow HA1 1BD · 020 8123 3218 · info.iskraservices@gmail.com
- Brand marks: deep blue + gold (from the coin-stack chart in their logo),
  strapline **"Empowering businesses"**
- Six service areas: incubation, immigration support, accounting & tax, funding
  & R&D relief, web & marketing, remote staffing

⚠️ **Unresolved with the client:** the site claims *"20+ years"* experience while
the legal entity was incorporated in **2024**. Currently carried as "20+ years
across the team". Iskra should word this themselves.

## 4. Design direction

The client rejected the first version (a "case file" treatment — institutional,
Caslon, hairline rules) as too dense and too obviously AI-generated. **v2 is
modelled on https://foundersfactory.com/** at the client's explicit request:

- Full-bleed dark bands (nav, hero, intro, CTA, footer) with a large blurred
  colour blob, off-white body between them
- Very light word count. Hero is five words, a one-line lede, two buttons.
  Every section is a headline, one sentence, a link.
- One typeface at expanded widths, black pill buttons, outlined card carousel

Founders Factory uses forest green; **we use Iskra's navy** so it stays their
brand rather than a copy. Flip only if the client asks.

### Tokens (defined in `:root` in `index.html`)

```
--navy   #0E1E3A     --gold   #E9B949     --light  #F4F4F4
--navy-2 #13294D     --gold-2 #F6D983     --white  #FFFFFF
--black  #121212     --grey   #6B6F76     --line   #E0E2E6
--ok     #1E8A5A     --warn   #B7791F     --sky    #7FB3FF
font: Archivo (Google Fonts), variable width — `font-stretch` 100–118%
```

Single visual world, deliberately **not** theme-switched: every colour is painted
explicitly so the page holds on any host background.

## 5. The client's 10 requirements → where each lives

From `Client req.docx`. All ten are implemented; 3–10 render inside the widget's
**"Your case"** tab rather than as page sections.

| # | Requirement | Implementation |
| --- | --- | --- |
| 1 | Chatbot as primary interface | The widget; `GROUNDING` covers immigration routes, endorsement criteria, incorporation, tax, Iskra's services |
| 2 | Conversational assessment | Prompt rule: max two questions per message, chosen from what's still missing |
| 3 | Single persistent profile | `S.profile`, 13 fields, persisted to `localStorage`; the prompt is told never to re-ask a captured field |
| 4 | Pathway recommendation | `S.pathways` — score, verdict, why, missing, next |
| 5 | Context-aware guidance | `S.stage` (11 stages) sent on every call via `context()` |
| 6 | Explainable recommendations | "Why this score" disclosure under each route |
| 7 | Assessment & gap analysis | `S.assessment` + `S.actions` (prioritised, with owner) |
| 8 | Human-in-the-loop | `S.regulated.triggered` — advisor stops, routes to an IAA-registered adviser |
| 9 | AI-to-human handoff | `brief()` builds a handover brief from the case file; copy + download |
| 10 | Personalised services | `S.services` ranked now/next/later |

## 6. ⚠️ The two builds — read before editing

`index.html` in this repo is a **standalone page**. The artifact build is a
**fragment** — the claude.ai platform supplies `<!doctype>`, `<html>`, `<head>`
and `<body>` at publish time, so the artifact source starts straight at
`<title>`.

**Syncing between them means adding or removing that wrapper:**

- Artifact → repo: strip everything up to and including `<body>`, drop the
  in-body `<title>`, then re-add this repo's `<head>`
- Repo → artifact: remove the whole `<!doctype>…<body>` prologue and the
  trailing `</body></html>`

**The one line you must never lose** when moving to standalone:

```css
[hidden]:not([hidden="until-found"]){display:none!important}
```

The artifact host provides this. The widget, login modal, launcher, toast and
nudge are all toggled with the `hidden` attribute, and the page's own
`display:flex`/`grid` rules out-specify the browser default. Without it,
everything renders permanently on top of the page.

**Republishing the artifact** needs `capabilities: {sample: {}, downloads: true}`
— or just omit `capabilities` on a redeploy and the stored declaration carries
forward.

## 7. How the advisor works

State lives in one object, `S`, keyed to `localStorage` under `iskra-case-v2`.

**Live path** (`mode === "live"`, artifact only):

1. `context()` renders the current case file into text
2. Input is `[{role:"user", content: GROUNDING + context()}, ...last 14 turns]`
3. `sampleFn.json(input, {cache:false, signal, onText})` — one call returns both
   the chat reply and the state updates as a single JSON envelope
4. `streamReply(raw)` incrementally extracts the `reply` string out of the
   *partially streamed* JSON so the message types out live rather than appearing
   after parse
5. `apply(env)` merges the envelope into `S`; panels re-render

The envelope is `{reply, suggestions, stage, profile, pathways, assessment,
actions, services, regulated}`. The prompt asks for **only changed keys**, which
keeps responses small and honest about what's still unknown.

**Fallback path** (`mode === "script"`): `SCRIPT[]` — six pre-written steps
walking the whole journey, with light keyword extraction (`extract()`) pulling
nationality, sector, funding, stage and experience out of whatever the user
actually types, so the case file still fills from their words.

Errors branch on `err.code`. `FATAL` codes (`not_granted`, `sampling_disabled`,
…) switch to scripted mode and *answer the message that was just sent* so nothing
is dropped. Everything else surfaces viewer-facing copy from `ERROR_COPY`.

## 8. What is deliberately fake

**The advisor falls back to scripted on GitHub Pages.** It calls Claude through
`window.claude`, which only exists inside the claude.ai artifact viewer. On any
other host `claude.use("sample")` resolves null and the widget switches to the
pre-written walkthrough — and *says so* in its status line
(*"Scripted demo · replies are pre-written"*). This is intentional and honest;
never relabel it. **Demo the artifact link when you want the live model.**

**The login is a mock.** No account is created, nothing is sent anywhere. Name
and email go to browser storage (`iskra-session`); passwords are never stored.
It exists to demonstrate the flow. Real auth is Phase 3 — and the standing
recommendation is to rent it (Clerk/Supabase), not build it.

## 9. Demo controls

State is per-browser, so demos need a way back to clean:

| Control | Where | Clears |
| --- | --- | --- |
| ↻ | Widget header | Conversation + case, stays signed in |
| Reset demo | Footer | Everything including the account |
| `?demo` / `?reset` | URL | Everything on load, then strips the param |

Both buttons arm on first click, act on second (`armConfirm()`). No `confirm()`
dialogs anywhere — they freeze the page inside a sandboxed artifact frame.

## 10. Editing and deploying

Single self-contained `index.html`. No build step, no dependencies, no
framework. Archivo comes from Google Fonts; everything else ships in the file.

```sh
cd ~/iskra-services-site
python3 -m http.server 8000     # then http://localhost:8000
# edit, then:
git add -A && git commit -m "..." && git push
```

Pages rebuilds in ~30–60s. Pushing needs a token with **Contents: write**
(the account has two GitHub identities — `singhaditya210100-dev` owns this repo;
the `gh` CLI on this machine is logged in as `adityasingh42069`, which has **no**
access to it).

`noindex, nofollow` is set deliberately so a prototype cannot outrank or be
mistaken for the live iskra.services. Keep it until the client says otherwise.

The repo is **public** because GitHub Pages requires that on a free plan. It
carries the client's name, branding and contact details.

## 11. Commercial context

A costed proposal exists at
`~/Desktop/Iskra Services - Website & AI Advisor Proposal.xlsx` — six sheets,
client-facing, GBP and INR. **Figures are deliberately not repeated here because
this repo is public.**

Shape of the programme:

- **Stage 1 (recommended commitment)** — Phase 1 marketing site + Phase 2 AI
  advisor. 10 weeks.
- **Stage 2 (indicative)** — Phase 3 accounts & case-file backend + Phase 4
  adviser console (where handoffs actually land — often forgotten, and it is a
  whole second app).
- Legal is a **pass-through, billed at cost**: a DPIA is effectively mandatory
  (the advisor profiles individuals and touches immigration data), plus an
  immigration-law review of the regulated-advice boundary.

Two things that drive the real build cost and are routinely underestimated:
**knowledge-base curation** (structuring UK immigration + endorsement content),
and the **evaluation harness** proving the advisor refuses regulated questions
reliably rather than usually. Neither is optional in this domain. Budget
knowledge-base refresh as an ongoing retainer item — an advisor quoting last
year's Home Office rules is worse than no advisor.

## 12. Open items

- [ ] Proposal needs Finfactor's registered address + VAT/GST on the cover, and
      the prototype link pasted into Next Steps (currently "supplied separately")
- [ ] Resolve the "20+ years" vs 2024-incorporation wording with Iskra
- [ ] Hero is text-on-gradient — ask Iskra for real photography (office, founders)
- [ ] Firm up Stage 2 pricing if they commit to Stage 1
- [ ] Decide whether the repo should stay public (private Pages needs GitHub Pro)

## 13. House rules for this prototype

- **Never present the scripted fallback as live AI.** The status line is load-
  bearing honesty.
- **Never let the advisor give regulated immigration advice.** The escalation
  path is a product feature and a legal requirement, not a nicety.
- Any figure, fee or threshold shown is **indicative** and must say so.
- Keep the "Concept prototype — not a live service" marker in the footer while
  this is a mockup.
