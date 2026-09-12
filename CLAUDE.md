# Iskra Services prototype — working context

Handoff notes so this can be picked up in a fresh session. Read this before
editing anything. **v3.0** — pre-login site + post-login founder platform.

---

## 1. What this is

A concept website **and founder platform** prototype built by **Finfactor** for
a client, **Iskra Services** — a UK business-services firm in Harrow working
mainly with international founders.

v3 implements the client's updated flow document: **three access levels,
progressively unlocked** —

```
PRE-LOGIN  →  FREE ACCOUNT  →  PAID PREPARATION  →  EXTERNAL ENDORSEMENT  →  GROW
Discover      Assess (P1)      Prepare (P2)          Authorised body          Subscription
              Review (P3)                            decides independently
```

Payment unlocks **preparation**, never the endorsement. That single sentence
governs every screen.

Status: design prototype. No backend, no payment, nothing regulated.

## 2. Where everything is

| | |
| --- | --- |
| Live site (GitHub Pages) | https://singhaditya210100-dev.github.io/Iskra-Services/ |
| Repo | https://github.com/singhaditya210100-dev/Iskra-Services |
| Local clone | `~/iskra-services-site` (dir name differs from repo — harmless) |
| **Artifact build (live AI)** | https://claude.ai/code/artifact/7f93ec36-a07f-48e1-a8a3-366295cbf6e6 |
| v1 brief | `~/Downloads/Client req.docx` — the ten chatbot requirements |
| **v3 brief** | `~/Downloads/Udpated flow - pre login, Post login, Paid services, preparation_incubation narrative .docx` |
| Costed proposal | `~/Desktop/Iskra Services - Website & AI Advisor Proposal.xlsx` (pre-dates v3 scope) |
| **Flow chart** | `docs/flow.html` in this repo · https://singhaditya210100-dev.github.io/Iskra-Services/docs/flow.html · artifact: https://claude.ai/code/artifact/ (see /artifacts, "Iskra Prototype Flow") |

## 3. ⚠️ The regulatory boundary (from the v3 brief, §1A and §18)

**Iskra is NOT an authorised endorsing body.** As of the GOV.UK list checked
10 Sep 2026, Indigenous Consultants Limited is not listed. Therefore:

- Iskra **assesses, prepares, incubates and reviews**. It builds the profile,
  runs the AI assessment, develops the plan, does a preliminary I/V/S review,
  finds gaps, organises evidence, and produces a referral pack.
- An **authorised endorsing body** (UK Endorsing Services, Innovator
  International, Envestors, GEP) independently assesses, decides, issues the
  official endorsement letter and notifies the Home Office. £1,000 + VAT, paid
  to them directly. Contact-point checkpoints at 12/24 months, £500 each.
- The **Home Office** decides the visa.

**Never** show "pay £X and unlock your endorsement". **Never** present a
readiness view as a Home Office score or a guarantee. The 74/100 in Gap
Analysis is labelled "Iskra Readiness Assessment — preparatory" everywhere it
appears (`notHO` fragment in the JS). The free tier shows traffic lights, not a
number, on purpose (§4 of the brief: "I would not show an overly precise
62.4%-type score").

Principle: *AI prepares; evidence supports; humans decide; the Home Office
decides immigration.*

## 4. Client facts

- Trading name of **Indigenous Consultants Limited**, England & Wales,
  **no. 16043340**. 79 College Road, Harrow HA1 1BD · 020 8123 3218 ·
  info.iskraservices@gmail.com
- Brand: deep blue + gold (coin-stack chart in their logo), strapline
  **"Empowering businesses"**
- ⚠️ Unresolved: site claims "20+ years" vs 2024 incorporation. Carried as
  "20+ years across the team".

## 5. Design direction

Client rejected v1 (institutional "case file", Caslon, hairlines) as too dense
and AI-generated. **v2/v3 are modelled on https://foundersfactory.com/** at the
client's request: full-bleed navy bands with a blurred gold blob, off-white
body, very light word count, one typeface (Archivo, variable width), black pill
buttons, outlined card rows. We use Iskra's navy where FF uses green.

The **app shell** is the same system at UI density: 262px left rail of modules
with done/current/locked dots, white panels on the light ground, semantic
traffic lights (`--ok` / `--warn` / `--bad`) kept separate from the gold accent.

```
--navy #0E1E3A   --gold #E9B949   --light #F4F4F4   --black #121212
--ok  #1E8A5A    --warn #B7791F   --bad  #B3261E    (semantic, not accent)
font: Archivo — display 300/expanded 112–118%, UI 500, tabular nums for scores
```

Single visual world, deliberately not theme-switched.

## 6. Build — read before editing

`index.html` is **assembled from `parts/`**. Edit the parts, then:

```sh
cd ~/iskra-services-site
cat parts/01-head.html parts/02-site.html parts/03-app.html parts/04-js.html > index.html
python3 -m http.server 8000   # look at it
git add -A && git commit -m "…" && git push
```

Commit `index.html` *and* `parts/` — Pages serves `index.html` directly.

| Part | Holds |
| --- | --- |
| `01-head.html` | doctype, head, all CSS. **Contains the `[hidden]{display:none!important}` rule — never lose it** |
| `02-site.html` | `#site` — pre-login marketing: nav, hero, three tests, ladder, Innovator Founder, for founders, pricing, CTA, about, footer |
| `03-app.html` | `#app` — top bar, rail, 11 empty `#m-*` panes; checkout modal; login modal; toast; nudge; launcher; `#widget` |
| `04-js.html` | everything below, then `</body></html>` |

**Two builds of the same page.** The artifact is a *fragment*: the claude.ai
platform supplies `<!doctype>…<body>`. To republish the artifact from the repo
file, strip everything through `<body>` and the trailing `</body></html>`. To
bring the artifact back to the repo, re-add `01-head.html`'s prologue. Republish
with `capabilities: {sample: {}, downloads: true}` or omit to carry forward.

## 7. State model

One object `S`, persisted to `localStorage["iskra-case-v3"]`. `user` is
separate, in `iskra-session` (local or session storage per "keep me logged in").

```
S.plan       "free" | "readiness" | "preparation" | "endorsement" | "grow"   (PLAN_RANK orders them)
S.profile    ~20 keys in PROFILE_GROUPS (Personal / Founder / Business) — one record, reused everywhere
S.ivs        null | {innovation, viability, scalability: "strong|moderate|weak", note}
S.pathways / S.assessment / S.actions / S.services / S.regulated   (from the advisor envelope)
S.turns      chat history       S.gated   pre-login gate shown
S.bplan      {sectionKey: userText}        S.evidence {key: true}
S.human      {status: none|pending|approved|returned, note}
S.external   {status: none|submitted|pending|approved, body: ukes|ii|env|gep}
S.visa       {submitted, setup}            S.module  current app module
```

`tier()` → `visitor` (no user) / `free` / `paid`. `has(plan)` compares ranks —
buying Package 3 implies 1 and 2.

**Journey** (10 stages, `JOURNEY[]`) is *derived* from state, never stored.
**Module locks** (`NEEDS`): assessment→readiness; plan/gaps/evidence→preparation;
review→endorsement; post→endorsement *and* external approved. `ivs` is never
locked — free shows the summary lights, Package 1 adds the criterion detail.

## 8. The v3 brief → where each part lives

| Brief | Implementation |
| --- | --- |
| A. Pre-login homepage + limited free chat | `#site`; widget in `visitor` tier; gate after ~3 scripted / ~5 live exchanges (`gateBubble`) |
| B. Free account → dashboard, "Your journey" 10 stages | `renderModule("dashboard")`, `JOURNEY[]` |
| 3. Founder profile (Personal / Founder / Business) | `PROFILE_GROUPS`, editable in **My Profile**, fed by the advisor |
| 4. Free AI Founder Assessment, traffic lights not a % | `runFreeAssessment()` → `S.ivs`; dashboard "Preliminary readiness" |
| C. Free vs paid table | Encoded in `NEEDS` + `PACKAGES` + the pricing section |
| D. Package 1 — 9 areas + I/V/S sub-criteria | `BA_AREAS`, `IVS_DETAIL` → **Business Assessment**, **I/V/S** |
| E. Package 2 — 17-section plan, AI review, versioning | `BPLAN` → **Business Plan** (editable, `S.bplan`) |
| F. Package 3 — human review, mock interview, referral pack | **Human Review** module |
| G. Gap analysis — 74/100, areas, top 5, 30/60/90 | `GAPS` → **Gap Analysis** |
| H. Human review — approve / return | `S.human`; auto-approves in the demo (labelled) |
| I/J. Authorised body — pick, submit, independent decision, letter 🔒 | body picker + endorsement tracker in **Human Review** |
| K. Visa application readiness checklist | **Post-Endorsement**, `VISA_CHECKS` |
| L. Post-endorsement dashboard, checkpoints | **Post-Endorsement** behind Grow |
| M. Ten modules | rail in `03-app.html` (+ Dashboard = 11 panes) |
| N. Paywall ladder Discover→Assess→Prepare→Review→Endorse→Grow | "How it works" ladder + pricing section |

The v1 brief's ten chatbot requirements still hold (see git history for the
v2.2 mapping); they now live inside the widget + Profile module.

## 9. The advisor

**Live path** (artifact only): `GROUNDING` + `context()` as a leading user
turn, then the last 14 turns → `sampleFn.json()`. `streamReply()` extracts the
`reply` string out of the partially-streamed JSON so it types out live.
`apply(env)` merges the envelope. **Visitors never get scored** — `apply`
discards pathways/ivs/assessment/actions for `!user` and only honours `gate`.

`context()` sends a `TIER:` line; `GROUNDING` has explicit rules per tier
(visitor: general info, no scoring, set `gate` after ~5 exchanges; free:
preliminary assessment with traffic lights, no number; paid: full detail).

**Scripted fallback** (`mode === "script"`, everywhere except the artifact):
`VISITOR_SCRIPT` (4 steps, gates on step 3) and `MEMBER_SCRIPT` (4 steps:
preliminary assessment → direct critique → regulated stop → what's next).
`scriptStep` resets to 0 on sign-in so the member script starts fresh.
`extract()` pulls nationality / sector / funding / stage / experience /
location / venture out of whatever the user actually typed.

The status line says *"Scripted demo · replies are pre-written"* whenever the
model isn't live. **Never relabel it.**

## 10. What is simulated, and says so

- **Login** — mock; name and email to browser storage, passwords never stored.
- **Checkout** — mock; "Prototype — no payment is taken". Sets `S.plan`.
- **Human review** — "Request" → pending → auto-approves after 2.6 s with a
  reviewer note. Screen shows *"Simulated for the prototype"*.
- **Endorsing body** — submit → pending → a labelled button *"Simulate the
  endorsing body's decision"* → approved. Never auto-approves; the click is
  the point: the decision is theirs.
- **Evidence uploads** — "Mark as uploaded" records a flag only.
- **Widget docking** — `dock(true)` physically moves `#widget` into
  `#advisor-dock` and adds `.docked`; `dock(false)` returns it to `<body>`.

## 11. Demo script (~5 minutes)

1. Land on the site. Click **Start free AI assessment**. Type *"I want to move
   to the UK and start a fintech company"*, then answer its two questions.
   Third reply gates: **Create free account**.
2. Sign up (any name/email, 8+ char password). Dashboard opens: journey 1/10,
   "Run assessment" as next step.
3. **Run free Founder Assessment** — widget docks in the Advisor module,
   preliminary I/V/S appears (🟢 🟡 🔴). Back to dashboard: 2/10, next step
   "Unlock Package 1".
4. Click **Unlock Package 3** from Pricing or the dashboard → checkout → Confirm.
   Rail unlocks. Show **Gap Analysis** (74/100 with the not-a-Home-Office-score
   label), **Business Plan** (17 sections, "Needs evidence" ones open).
5. **Human Review** → Request → approved → pick UK Endorsing Services → Submit
   → "Simulate the endorsing body's decision". Tracker fills; letter unlocks
   *from them*.
6. **Post-Endorsement** → visa checklist; Grow lock card for the subscription.
7. Footer **Reset demo** (click twice) to start over.

## 12. Demo reset

| Control | Clears |
| --- | --- |
| ↻ in widget header | conversation + case; keeps plan, module, sign-in |
| **Reset demo** in site footer | everything, returns to the site |
| `?demo` / `?reset` on the URL | everything, on load (works when opened directly) |

Both buttons arm on first click, act on second. No `confirm()` dialogs — they
freeze the artifact frame.

## 13. Commercial context

The costed proposal on the Desktop pre-dates v3 and covers a site + advisor
(Stage 1) with accounts + adviser console as Stage 2. **v3 scope is materially
larger** — a founder app with ten modules, three paid packages, an endorsing-body
handoff and a post-endorsement layer — and the proposal needs re-cutting before
it goes to Iskra again. Figures are deliberately not repeated here because this
repo is public.

Package prices on the site (£249 / £749 / £1,490 / £49 pm) are **illustrative
and labelled so** — the brief gives none. Iskra sets them.

## 14. Open items

- [ ] Re-cut the proposal for v3 scope
- [ ] Iskra to set real package prices
- [ ] Resolve "20+ years" vs 2024 incorporation wording
- [ ] Hero is text-on-gradient — real photography would help
- [ ] AI mock endorsement interview (Package 3 feature) is listed but not
      built — only the chat exists
- [ ] Repo is public (Pages on free plan); private needs GitHub Pro
- [ ] Rotate any GitHub token that has appeared in a chat transcript

## 15. House rules

- Payment unlocks preparation, never endorsement. Not once, not as a demo shortcut.
- Readiness views are always labelled preparatory. Free tier: lights, no number.
- The endorsing body's decision is a *click the presenter makes*, never automatic.
- Never present the scripted fallback as live AI.
- Regulated immigration questions stop the advisor and route to an IAA-registered adviser.
- Keep "Concept prototype — not a live service" in the footer.

## 16. QA pass — 11 Sep 2026 (v3.1)

Driven against the **deployed Pages build** with in-page assertion scripts
(~340 checks via `javascript_tool`): every nav link and CTA on the site, the
chat run to the sign-up gate, the auth modal (validation, all four modes, every
close path, forgot flow, Google path), sign-up → dashboard, every module locked
and unlocked, checkout (all close paths, confirm, already-unlocked), Package
1 → 2 → 3 → Grow, human review → endorsing body → post-endorsement, reload
persistence, both resets, logout / login with "keep me logged in" off,
pending-unlock-after-signup, and a 400px pass via a same-origin iframe.

Bugs found and fixed (`3cecf48`, `1286cf9`):
- `data-open-chat` buttons rendered *by modules* were dead — listeners were
  bound once at boot. Now delegated with the other `data-*` actions.
- An auto-filled profile name didn't follow a new account on the same
  browser → `S.nameAuto`; a name edited in My Profile stays put.
- The app top bar overflowed at phone width (avatar pushed off-screen, badge
  wrapping "Grow · Grow" onto three lines) → compact bar under 640px, badge
  is the plan label only, launcher goes icon-only.

Not bugs — know these before "fixing" them:
- Smooth-scroll anchors don't visibly move in a **background** Chrome tab
  (the animation is throttled). Instant scroll and the 84px `scroll-margin`
  are correct; real users' tabs are foreground.
- **GitHub Pages caches `index.html`.** After a push, verify with a
  cache-busting query (`?v=<sha>`) or you will be testing the previous build.
- `resize_window` will not go to 400px on this machine (it snapped to 1920).
  Test mobile with a same-origin `<iframe style="width:400px">` and assert
  inside `iframe.contentDocument`; use `contentWindow.eval()` to reach the
  script-scope `S`.
- With classic scrollbars the fullscreen widget measures 385px in a 400px
  iframe — scrollbar, not layout.
- The chip *"…start a company"* extracts no venture: there's nothing between
  "a" and "company" to extract.

The assertion scripts live in the session transcript, not the repo. Shape:
`const T=(name,cond,detail)=>…` inside `javascript_tool` calls, batched with
`browser_batch`. Worth lifting into `tools/qa.js` if this gets iterated.
