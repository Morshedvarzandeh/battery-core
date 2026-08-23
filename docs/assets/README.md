# Battery Core design system

Three files, in the order you reach for them.

| File | Use it when |
| --- | --- |
| `page-template.html` | You are adding a page. Copy it, fill the placeholders. |
| `site.css` | The page uses the course shell. Link it; add no other CSS. |
| `module-theme.css` | The page brings its own stylesheet and only needs the palette. |

## Colour roles

The palette is one dark navy ground, one text pair, and three hues. Each hue
means one thing, so a reader can tell a module's tier before reading its label.

| Token | Hue | Means |
| --- | --- | --- |
| `--accent` | mint `#68e0bd` | The core path: required parts, primary actions, part numbers, the brand mark. |
| `--blue` | `#71b7ff` | Optional depth: the `B` parts that go further into a topic without being required to finish the chapter. |
| `--orange` | `#ffb067` | The toolkit: authoring and maintenance tools that build the course rather than teach it. |

Components never read those three directly. They read `--tier`, which a single
modifier class sets:

```html
<article class="study-step">…</article>                   <!-- core, mint   -->
<article class="study-step study-step-deeper">…</article>  <!-- depth, blue  -->
<article class="study-step study-step-toolkit">…</article> <!-- tool, orange -->
```

`--tier-core`, `--tier-deeper` and `--tier-toolkit` are the aliases in
`:root`. Recolour a tier there and every card, number, and link that belongs to
it follows.

Surfaces are the four navy steps — `--background`, `--surface-soft`,
`--surface`, `--surface-raised` — and text is `--text` or `--muted`. A page that
needs a colour not on this list is a page that needs a new documented role
first.

## Adding a page

1. Copy `page-template.html` to `docs/<area>/<module>/index.html`.
2. Replace every `{{ PLACEHOLDER }}` and delete the explanatory comments.
3. Fix the depth of the relative paths for where the copy actually sits.
4. Set the tier on the hero eyebrow, and use the same tier on the cards that
   link to the page from `docs/index.html` and `docs/chapter-1/index.html`.
5. Add a `README.md` beside it saying what the module teaches, what it
   simplifies, and how to run it.
6. Add the page to the static checks in `tests/test_course_homepage.py`.

## Adding a page that brings its own CSS

The interactive modules were each authored standalone, with their own generic
token set — `--background`, `--primary`, `--card`, `--border`,
`--viz-series-N`. Those defaults are blue-on-white and clash with the course.

`module-theme.css` re-declares that same contract in course colours. Link it
**after** the page's own stylesheet or `<style>` block, so it wins on source
order:

```html
<link rel="stylesheet" href="styles.css">
<link rel="stylesheet" href="../../assets/module-theme.css">
```

The module keeps its structure; only the colours move. It also brings the two
shared strips, which are namespaced `bc-` so they cannot collide with the
module's own classes:

- `.bc-modulebar` — the part label and the way back to the course.
- `.bc-footer` — the standard footer, including the Lemonergy attribution.

## Components in `site.css`

Layout: `.site-header`, `.hero`, `.guide-hero`, `.page-hero`, `.section`,
`.section-heading` (add `.compact` for a heading with no context paragraph),
`footer`.

Content: `.module-grid` + `.module-card`, `.study-sequence` + `.study-step`,
`.question-path`, `.checkpoint-grid`, `.principle-grid`, `.wide-card`,
`.closing`, `.tier-legend`.

Text roles: `.eyebrow` (tier colour), `.format` (blue, the delivery format of a
module), `.lede`, `.launch-note`, `.sr-only`.

Actions: `.button` + `.button-primary` / `.button-secondary`, `.card-action`,
`.text-link`.

Tool surface, for the authoring tools: `.tool-layout`, `.panel`, `.panel-label`,
`.control-row`, `.chip` (+ `.chip-primary`, `.chip-ghost`, and
`aria-pressed="true"` for the selected one), `.field`, `.switch`, `.nudge-pad`,
`.pill` (+ `data-state="warning"` / `"idle"`), `.canvas-card`,
`.tool-statusbar`.

## The study coach

`study-coach.js` turns the chapter's checkpoint questions into a loop: write an
answer, then compare it against the points a complete answer covers. It mounts
into `<div id="study-coach"></div>` and needs nothing else — no build step, no
network, no account.

There are two kinds of question, because two kinds are honestly possible
without a server:

| Kind | Types | How it is marked |
| --- | --- | --- |
| **Checked** | `drill`, `choice`, `multi`, `order` | Marked outright. The answer space is closed, so the coach can say exactly what was wrong and why. |
| **Self-checked** | prose (the default) | Not marked. The coach shows what a complete answer covers and the learner ticks their own. |

The split is not squeamishness. Grading prose offline means keyword matching,
and keyword matching grades vocabulary rather than understanding: *"the
separator does **not** block electrons"* contains every right word and is
wrong, while a correct answer in different words scores nothing. A confidently
wrong grade is worse than no grade, because the learner cannot tell it
happened. Anything that genuinely can be checked is therefore written as a
closed-form question instead — which is also better teaching, since a
well-chosen distractor names the misconception the learner actually holds.

Every number in a drill comes from the same relationship the tested Python
implements — `current_from_c_rate`, `ideal_duration_hours`, `arrhenius_factor`,
`parabolic_film_thickness` — and the two physical constants the browser cannot
import are compared against `battery_core.aging` by a test, so the copy cannot
drift.

Progress lives in `localStorage` under `battery-core-chapter-1-coach`. A browser
with site data blocked studies without saved progress rather than getting a
broken page. A `<noscript>` block beside the mount point says the questions are
all written out in the sequence above, because they are.

To add a question, append to `QUESTIONS` in `study-coach.js`. Every question
carries the same envelope:

```js
{
  id: "p05-something",          // stable — it keys saved progress
  group: "part",                 // "part" or "chapter"; drives the filters
  tier: "core",                  // "core" or "deeper"; drives the badge colour
  part: "Part 05",
  module: "../fundamentals/…/",  // where to go to revisit it
  moduleLabel: "Part 05 · …",
  question: "…",
  hints: ["…", "…"],            // revealed one at a time
  note: "…",                     // optional: a limit worth stating
}
```

Then one of these bodies decides how it is answered and marked:

```js
// prose — the default when no `type` is set
points: ["…", "…"]              // what a complete answer covers

// choice — exactly one correct; multi — any number correct
type: "choice",
options: [
  { text: "…", correct: true, why: "Why this is the right reading." },
  { text: "…", why: "Which misconception this option is, and why it fails." },
]

// order — `items` in the CORRECT order; the coach shuffles for display
type: "order",
items: ["First step", "Second step", "…"]

// drill — numeric, generated fresh each time
type: "drill",
drill: "cRateCurrent"           // a key of DRILLS
```

Two rules worth keeping:

- **Every option needs a `why`, including the wrong ones.** A distractor that
  is only marked wrong teaches nothing; a distractor that says *which*
  misunderstanding it represents does the actual teaching. A test enforces the
  count matches.
- **Keep `points` to what a complete answer genuinely needs.** The learner
  ticks each one, so a padded list makes an honest self-score look like a
  failure.

A new drill is an entry in `DRILLS` with `generate`, `prompt`, `answer`,
`working`, a `label` for the input, and a `tolerance` as a fraction. Mirror a
tested function rather than inventing arithmetic, and add the comparison to
`tests/test_study_coach.py`.

## The mascot

The coach has a face: a lemon in a headset, for Lemonergy. It is drawn as
inline SVG in `study-coach.js` rather than embedded as an image, for three
reasons — it stays sharp at any size, it costs no request on a page that is
meant to be self-contained, and a drawing can change expression where a bitmap
cannot.

`data-mood` on the `<svg>` selects the expression, and `site.css` does the rest:

| Mood | When | What moves |
| --- | --- | --- |
| `idle` | a new question | gentle smile |
| `thinking` | a hint is shown, or an answer revealed | one brow raised, mouth flat |
| `happy` | marked fully correct | broad smile, sparkle |
| `encouraging` | marked partly or fully wrong | inner brow ends raised, soft mouth |

Expressions swap whole `<path>` elements by `display` rather than animating the
CSS `d` property. Firefox does not support `d`, and a mascot that freezes in
one major browser is worse than a slightly longer SVG.

The lemon yellow is `--lemon`, and it is the one hue outside the role system in
[Colour roles](#colour-roles). That is deliberate and narrow: the mascot is
illustration, not a UI state, so `--lemon` never marks a tier, a status, or a
control. If it starts appearing on buttons, the role system has been broken.

## An AI tutor

The coach ships with the AI mode **off**, and the page therefore makes no
network request at all. Turn it on by pointing the mount element at an endpoint:

```html
<div id="study-coach" data-tutor-endpoint="https://tutor.example.workers.dev"></div>
```

An "Ask the tutor" panel then appears for free-form follow-up questions. It
POSTs JSON and expects JSON back:

```jsonc
// request
{ "question": "…", "context": { "chapter": 1, "checkpointId": "p01-paths", "checkpoint": "…" } }
// response
{ "reply": "…" }
```

If the endpoint is unreachable the panel says so and the checkpoints keep
working, so a fork that never configures one loses nothing.

**Never put an API key in the page.** Everything under `docs/` is public, and a
key in client-side JavaScript is a key anyone can read and spend. The endpoint
has to be a small proxy that holds the key server-side. A complete Cloudflare
Worker doing that:

```js
import Anthropic from "@anthropic-ai/sdk";

const SYSTEM = `You are a tutor for Chapter 1 of the Battery Core course, which
covers lithium-ion cell anatomy, nominal capacity and C-rate, cell production
including all-solid-state routes, and battery aging.

Answer only within that scope; for anything else, say it is outside Chapter 1.

Teach rather than hand over answers: when the learner is working a checkpoint,
point at the idea they are missing before you state the result. Keep replies
under 150 words.

Hold the course's own distinction between an exact definition and a prediction.
I = Q x C and t = 1 / C are definitions. Runtime, capacity fade, and impedance
rise are predictions that need a validated model of a specific cell, so never
state one as a fact. Say when you are unsure.`;

const CORS = {
  "access-control-allow-origin": "https://morshedvarzandeh.github.io",
  "access-control-allow-headers": "content-type",
  "access-control-allow-methods": "POST, OPTIONS",
};

export default {
  async fetch(request, env) {
    if (request.method === "OPTIONS") return new Response(null, { headers: CORS });
    if (request.method !== "POST") return new Response("Method not allowed", { status: 405 });

    // A public endpoint needs a limit, or one script drains the account.
    const ip = request.headers.get("cf-connecting-ip") ?? "anonymous";
    const { success } = await env.TUTOR_LIMIT.limit({ key: ip });
    if (!success) {
      return Response.json({ reply: "Too many questions just now — try again shortly." },
                           { status: 429, headers: CORS });
    }

    const { question, context } = await request.json();
    if (typeof question !== "string" || question.length > 2000) {
      return Response.json({ reply: "That question was empty or too long." },
                           { status: 400, headers: CORS });
    }

    const client = new Anthropic({ apiKey: env.ANTHROPIC_API_KEY });
    const message = await client.beta.messages.create({
      model: "claude-opus-5",
      max_tokens: 1024,             // deliberately short: this is a tutor reply
      betas: ["server-side-fallback-2026-07-01"],
      fallbacks: "default",         // a policy decline is retried on another model
      system: SYSTEM,
      messages: [{
        role: "user",
        content: context?.checkpoint
          ? `Checkpoint being worked on: ${context.checkpoint}\n\nQuestion: ${question}`
          : question,
      }],
    });

    if (message.stop_reason === "refusal") {
      return Response.json({ reply: "I can't answer that one. Try rephrasing it." },
                           { headers: CORS });
    }
    const reply = message.content.filter((b) => b.type === "text").map((b) => b.text).join("");
    return Response.json({ reply }, { headers: CORS });
  },
};
```

Deploy it with `ANTHROPIC_API_KEY` as a secret (`wrangler secret put`) and a
`TUTOR_LIMIT` rate-limiting binding in `wrangler.toml`. Set
`access-control-allow-origin` to your own origin — leaving it `*` lets any site
spend your key.

Two things worth knowing before switching it on:

- **It will sometimes be wrong.** A model answering checkpoint questions on a
  teaching site costs more when it errs than it would elsewhere, because the
  learner is not yet able to catch it. The system prompt above pushes back
  toward the module for that reason, and the panel says answers can be wrong.
- **It costs money per message.** `claude-opus-5` is $5.00 per million input
  tokens and $25.00 per million output. Roughly $0.015 a message at the sizes
  above. Cheaper models exist — `claude-sonnet-5` at $3.00/$15.00,
  `claude-haiku-4-5` at $1.00/$5.00 — and switching is a one-line change, but
  a smaller model is more likely to state the physics wrong, which is the
  failure that matters most here. That trade is yours to make, not the
  default's.

## Rules the pages hold to

- No external requests. Every page is self-contained: no CDN scripts, no
  hosted fonts, no analytics. `docs/index.html` carries no `<script>` at all.
- A skip link is the first focusable element, and it targets `#main-content`.
- Every landmark is labelled: `aria-label` on `nav`, `aria-labelledby` on each
  `section`.
- Interactive state is announced — `aria-pressed` on toggles, `role="status"`
  with `aria-live="polite"` on anything that changes without a page load.
- Motion respects `prefers-reduced-motion`; `site.css` already does this for
  every transition it defines.
- The footer keeps the Lemonergy attribution. It is the Appropriate Legal
  Notice required by the additional term in [`NOTICE`](../../NOTICE).
