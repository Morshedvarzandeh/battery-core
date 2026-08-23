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
