# Iskra Services prototype — working context

Handoff notes so this can be picked up in a fresh session. Read this before
editing anything. **v4.0** — generic pre-login site, intake-first founder
platform, merged Business Assessment, AI-generated plan, test-mode checkout,
PDF documents, specialist requests.

---

## 1. What this is

A concept website **and founder platform** prototype built by **Finfactor** for
a client, **Iskra Services** — a UK business-services firm in Harrow working
mainly with international founders.

The pre-login site is **route-agnostic** (Innovator Founder, Global Talent,
Expansion Worker, self-sponsorship). The prototype's *flow* is deliberately
**Innovator Founder-centric**: the advisor collects basics and recommends that
route; the platform prepares a case for it.

```
PRE-LOGIN                 FREE ACCOUNT                    PAID                     EXTERNAL
generic site + limited    9-question intake FIRST →       P1 Business Assessment   authorised
advisor (answers          free assessment → dashboard     P2 AI plan + gaps + evid body decides
prefilled) → recommends   focused on the current step     P3 human review + pack
Innovator Founder → gate  + "strengthen your case"
```

Payment unlocks **preparation**, never the endorsement.

## 2. Where everything is

| | |
| --- | --- |
| Live site (GitHub Pages) | https://singhaditya210100-dev.github.io/Iskra-Services/ |
| Repo | https://github.com/singhaditya210100-dev/Iskra-Services |
| Local clone | `~/iskra-services-site` |
| **Artifact build (live AI)** | https://claude.ai/code/artifact/7f93ec36-a07f-48e1-a8a3-366295cbf6e6 |
| Flow chart (**reflects v3.1** — see §13) | `docs/flow.html` · artifact 5a08d09c-0360-4a45-9361-02c0b3ccc844 |
| v1 brief | `~/Downloads/Client req.docx` |
| v3 brief | `~/Downloads/Udpated flow - pre login, Post login, Paid services, preparation_incubation narrative .docx` |
| v4 change request | the user's message of 13 Sep 2026 (12 pre-/post-login items) — all implemented |
| Costed proposal | `~/Desktop/Iskra Services - Website & AI Advisor Proposal.xlsx` (pre-dates v3/v4 scope) |

## 3. ⚠️ The regulatory boundary

**Iskra is NOT an authorised endorsing body.** It assesses, prepares, incubates
and reviews. An authorised endorsing body (UK Endorsing Services, Innovator
International, Envestors, GEP) decides and issues the letter; the Home Office
decides the visa. Never show "pay to unlock endorsement"; never present a
readiness view as a Home Office score (`notHO` fragment). Free tier shows
traffic lights; a numeric readiness (`readinessScore()`, strong 100 / moderate
55 / weak 20, averaged) appears only inside paid modules, labelled preparatory.
The endorsing body's approval is an **explicit labelled click**, never automatic.

## 4. Client facts

Trading name of **Indigenous Consultants Limited**, no. **16043340**, 79 College
Road, Harrow HA1 1BD · 020 8123 3218 · info.iskraservices@gmail.com. Brand:
navy + gold, "Empowering businesses". ⚠️ "20+ years" vs 2024 incorporation is
still unresolved with the client.

## 5. Design direction

Modelled on foundersfactory.com at the client's request (v1 was rejected as
dense and AI-generated): navy full-bleed bands, blurred gold blob, off-white
body, Archivo variable-width, black pill buttons. App shell: 250px rail, white
panels, semantic lights (`--ok/--warn/--bad`) separate from the gold accent.
Checkout is styled like Stripe Checkout (order summary left, card form right,
"Powered by stripe", TEST MODE badge) because Stripe is the UK's most common
online PSP — it is a mock, prefilled with Stripe's 4242 test card.

## 6. Build

`index.html` is assembled from `parts/`:

```sh
cd ~/iskra-services-site
cat parts/01-head.html parts/02-site.html parts/03-app.html parts/04-js.html > index.html
python3 tools/artifact-fragment.py index.html /tmp/frag.html   # artifact build
git add -A && git commit -m "…" && git push                     # Pages serves index.html
```

| Part | Holds |
| --- | --- |
| `01-head.html` | head + all CSS. Keep `[hidden]{display:none!important}`. |
| `02-site.html` | `#site`: nav, hero, nine-areas band, ladder (5), routes (4), **What you get (9 value cards)**, pricing (Free/P1/P2/P3 + external row), CTA, about, footer |
| `03-app.html` | `#app`: top bar, **horizontal milestone map** (`#map`), rail (8 modules), 8 `#m-*` panes; Stripe-style checkout; **request modal** (`#req`); auth; toast; nudge; launcher; widget |
| `04-js.html` | loads jsPDF 2.5.1 from cdnjs, then everything |

The artifact is a fragment (platform supplies `<!doctype>…<body>`); the repo
file is standalone. `tools/artifact-fragment.py` converts. Republish with
`capabilities: {sample: {}, downloads: true}` or omit to carry forward.

## 7. State model (v4)

`S` → `localStorage["iskra-case-v4"]`; `user` → `iskra-session`.

```
S.plan        free | readiness | preparation | endorsement   (PLAN_RANK; buying P3 implies P1+P2)
S.profile     ~20 keys (PROFILE_GROUPS) filled by the chat + My Profile
S.turns, S.gated, S.stage, S.regulated              — advisor
S.intake      {problem, solution, market, model, competition, differentiation, founder, funding, uk}
S.intakeSeen  first-login intake shown/skipped     S.intakeTouched  demo answers seeded once
S.assessment  null | {route, overall, areas:[{key, verdict, summary, assessed, evidence[], gaps[], move, answer}], ivs:{innovation|viability|scalability:{verdict,note}}}
S.assessedLive  bool     S.editIntake  re-answer mode
S.bplan       null | {sections:{17 keys}, live, version}   S.bplanEdits {key:text}
S.evidence, S.human {status}, S.external {status, body}, S.requests [{kind, items, at}], S.module
```

`JOURNEY[]` (7: profile, assess, business, plan, gaps, review, endorse) is
derived, rendered as the map. `currentStep()` drives the dashboard's single
big card. `NEEDS`: business→readiness; plan/gaps/evidence→preparation;
review→endorsement.

## 8. The v4 change request → where each item lives

**Pre-login**
1. Generic homepage, IF-centric flow — hero/routes/copy in `02-site`; recommendation in `VISITOR_SCRIPT[4]` and the visitor tier rules in `GROUNDING`
2. Prefilled answers — `prefill` on each script step, `setPrefill()`, `LIVE_PREFILLS` for live mode; `#w-prefill` hint; chips hidden while a prefill is present
3. Collect basics then recommend — four groups (basics / business / founder+team / funding+UK) then the recommendation + gate
4. Gate names the parameters — `gateBubble()` lists the nine areas as chips

**Post-login**
1. Intake first on first login — `enterApp()` → `showModule("assess",{firstRun:true})`; "Skip for now" sets `intakeSeen`
2. Rail without AI Advisor / My Journey; journey is the top map — `03-app`, `renderApp()`
3. Dashboard = current step — `currentStep()` + `.now-card`; future steps only in the map
4. Nine attributes before assessment — `AREAS`, `intakeForm()`, `runAssessment()` requires 9/9
5. I/V/S under Business Assessment — `IVS_MAP` + `IVS_DETAIL` rendered inside `business`; no separate module
6. Post-assessment CTAs — `strengthenPanel()`: company formation, 8 specialists, IAA adviser → `openRequest(kind, spec)`
7. Post-Endorsement removed — no module; endorsed state offers IAA + formation requests
8. Dummy payment — `openCheckout()` / `wireCheckout()`, Stripe-style, VAT 20%, test card prefilled, receipt screen
9. Detailed expandable assessment — `<details class="ba">` per area with assessed / evidence / gaps / move / your answer
10. AI plan from the assessment, linked — `generatePlan()` (live `sample.json` or `composePlan()`), `PLAN_SECTIONS[].basedOn`, `planStatus()`, "Based on" chips jump to the card
11. PDF + share — `pdfAssessment()`, `pdfPlan()` via jsPDF; `savePdf()` uses the artifact `downloads` capability or a blob link; `shareDoc()` uses Web Share with a file, else copies a summary + link
12. Value-adds on pre-login — the **What you get** section (9 cards) and the ladder note

## 9. The advisor

Live (artifact only): `GROUNDING` + `context()` (tier, profile, intake count,
assessment verdicts) → `sampleFn.json()`; `streamReply()` types the reply out.
Envelope is now small: `reply, suggestions, gate, stage, profile, regulated` —
**no scoring in chat**; assessment lives in the platform. `apply()` discards
`gate` for logged-in users and never scores visitors.

Scripted: `VISITOR_SCRIPT` (5 steps + hold) with `prefill`; `MEMBER_SCRIPT`
(4 steps). `extract()` fills profile gaps from typed text but **never
overwrites** a value the script or user already set.

## 10. Simulated, and says so

Login · checkout (test mode) · assessment in scripted mode (`DEMO_ASSESSMENT`)
· plan in scripted mode (`composePlan()` from the intake answers) · human
review auto-approves after 2.6 s · endorsing body decision is a labelled click
· evidence uploads are flags · specialist requests are recorded locally.

In the artifact, **assessment and plan generation are live** (`sample.json`)
with the scripted versions as fallback; the result panel says which.

## 11. Demo script (~6 minutes)

1. Site → **Start free AI assessment**. The opener is prefilled; press Send
   five times. Fifth reply recommends Innovator Founder and gates.
2. **Create free account** → lands on the nine questions (prefilled). Show
   "Skip for now" exists; click **Run Free Founder Assessment** (≈3 s).
3. Result: nine lights, three tests, "Where your case is weak", **Strengthen
   your case** (formation / specialists / IAA). Click a specialist → request.
4. Dashboard: one big current step. Top map shows the rest.
5. **Unlock Package 1** → Stripe-style checkout, Pay → Business Assessment:
   expand a card, **Download PDF**.
6. Unlock P2 → **Generate business plan** → open a "Needs evidence" section →
   click its "Based on" chip → lands on the assessment card. Download PDF.
7. Unlock P3 → Request review → approve → pick a body → Submit → **Simulate
   the endorsing body's decision** → endorsed; CTAs for IAA adviser and
   company formation.
8. Footer **Reset demo** ×2.

## 12. Demo reset

↻ in the widget keeps plan + intake, clears chat + assessment. Footer
**Reset demo** clears everything. `?demo`/`?reset` on the URL clears on load.

## 13. Known gaps / open items

- [ ] `docs/flow.html` still draws **v3.1** (AI Advisor module, My Journey,
      Post-Endorsement, Grow) — it carries a banner saying so. Redraw for v4
      when the flow settles.
- [ ] Proposal spreadsheet pre-dates v3/v4 scope — re-cut before it goes out.
- [ ] Prices (£249 / £749 / £1,490) illustrative; VAT shown at 20%.
- [ ] Live-mode assessment/plan prompts are untested against a real model in
      this session — run once in the artifact before a client demo.
- [ ] `docs/` is served by Pages; anything put there is public.
- [ ] Rotate any GitHub token that has appeared in a chat transcript.

## 14. QA notes (13 Sep 2026)

Driven against the local build with in-page assertion scripts (~150 checks):
pre-login prefills → gate; sign-up → intake-first; skip; run assessment; P1
checkout (validation, auto-format, receipt); expandable cards; both PDFs
build (page counts checked); P2 plan generation, statuses, edits, "Based on"
links; gaps from the assessment; P3 → endorsing body → final CTAs; all three
request modals; logout/login; ↻ and Reset demo; 400px iframe pass over every
module and both modals. GitHub Pages caches `index.html` — verify a push with
`?v=<sha>`. A same-origin test iframe **shares localStorage** with the parent —
reset inside the iframe before asserting first-run behaviour.
