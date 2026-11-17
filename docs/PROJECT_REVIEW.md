# Project review

Reviewed and improved on 2026-11-17. The original findings below describe the supplied baseline; the following status section records the implemented changes and verification.

## Short-term improvements completed

- **Photography update:** the page and slides now show Hailey Dawson using a 3D-printed hand and Danny Letain with an engineering team. These are credited, independently sourced real-world references, with JPEG fallbacks and responsive WebP variants. The full-size WebP pair is 403,140 bytes; the 640-pixel pair is 87,524 bytes. See `ASSET_CREDITS.md` for licenses and modifications.
- **Image loading:** slide content and images render only when first visited. Before the real-photo update, the earlier conceptual PNG pair had been optimized from 4,149,086 bytes to 233,520 bytes of full-size WebP images.
- **Progressive enhancement:** page content is visible by default, navigation stays expanded without its script, and presentation buttons become available only after initialization.
- **Maintainability:** page CSS and JavaScript were extracted into `site.css` and `site.js`; page/illustration overrides were removed from presentation CSS, and HTML/CSS were expanded into readable sections.
- **Navigation and accessibility:** a skip link, `aria-current` indicators, a complete section menu at every breakpoint, Escape/outside-click menu closing, and preserved modal focus management. Overflowing slides remain scrollable from their beginning.
- **Slide targets:** the process has a stable `proceso` ID and its slide returns to the correct section. The return-to-section control is available on mobile too.
- **References and branding:** four public reference links with consultation date, an SVG favicon, and basic Open Graph title/description/locale metadata.
- **Repository quality:** asset provenance notes, reproducible image generation, expanded static checks, and an automated Chromium interaction check included in CI.

## Folder analysis

| Location | Contents and role |
| --- | --- |
| `newlife-site/` | Existing Git repository on `main`, initially containing one commit and no remote. This is the publishable project. |
| `newlife-site/dist/index.html` | Spanish single-page academic website, public references, and presentation shell. |
| `newlife-site/dist/site.css` / `site.js` | Page styles, responsive navigation, scroll status, and optional reveal effects. |
| `newlife-site/dist/presentation.js` | Hard-coded content for 11 slides, rendering logic, keyboard/touch controls, fullscreen, and modal focus management. |
| `newlife-site/dist/presentation.css` | Presentation-only styles. |
| `newlife-site/dist/assets/` | JPEG reference photos and responsive WebP variants, earlier unused conceptual artwork, and an SVG favicon. |
| `newlife-site/.openai/hosting.json` | Static publish-directory setting and a project-specific hosting identifier. |
| `source-docs/` | Empty. The class notes referenced by page number in the website are not included here. |
| `tools-temp/` | One-off page transformation scripts, library transfer/download tooling, 17 note images, transfer metadata, Python cache files, and a deployment archive. |

The scripts in `tools-temp/` reflect earlier editing and transfer operations rather than a reproducible build pipeline. For example, `add_presentation.py` asserts that the presentation is absent before inserting it, so rerunning it against the current page fails. Use the editable files in `dist/` for ongoing development.

## What is implemented

- A responsive concept website about personalized hand prostheses, 3D printing, AI, IoT, cloud collaboration, circular production, and potential customers.
- An integrated presentation dialog with 11 slides and multiple navigation methods.
- Real-world reference photographs with creator/source/license credits and clear distinctions between the photographed initiatives and the conceptual NewLife proposal.
- Relative local asset paths, Spanish language metadata, image descriptions, lazy loading on some images, and reduced-motion handling.
- No application server, database, account system, CAD pipeline, AI model integration, sensor integration, or cloud design-management service is present.

The current technology choice fits a small academic showcase: it has a small operational footprint and does not require a framework to publish.

## GitHub preparation included

- README with local preview, validation, repository publication, and deployment instructions.
- Ignore rules, text/binary Git attributes, and editor settings.
- Contribution guidance and a manual browser checklist.
- A dependency-free Python checker plus Node.js JavaScript syntax checks, run by GitHub Actions.
- A Chromium browser check for progressive enhancement, layouts, and deck interactions, also configured in GitHub Actions.
- A manually triggered GitHub Pages workflow that validates before uploading `dist/`.

## Original prioritized findings

The evidence in this section describes the initial version. Use the completed-status section above and remaining-work section below for current priorities.

### 1. Keep content usable when JavaScript is unavailable — high priority

**Evidence:** `dist/index.html` sets `[data-reveal]` to `opacity: 0` by default. The normal code path makes elements visible through JavaScript; the reduced-motion CSS is the only independent fallback. A disabled or failed script leaves substantial content invisible for users without that preference. The presentation launch buttons also remain available when the presentation script cannot run.

**Suggested change:** make content visible by default and enable reveal effects only after successful initialization. Hide or disable presentation controls until their handlers are ready. Check the page with JavaScript disabled and with a deliberately failed script request.

### 2. Optimize the illustrations — high priority

**Evidence:** `prosthesis.png` is 1,843,448 bytes and `workshop.png` is 2,305,638 bytes: approximately **4.15 MB combined** before transport compression. These dominate the website's file size. The same URLs are reused, so they are generally cached rather than downloaded once per slide.

**Suggested change:** export WebP or AVIF variants with PNG fallbacks, provide smaller responsive sizes through `srcset`/`sizes`, and preserve image descriptions and dimensions. Compare visual quality, transferred bytes, and Largest Contentful Paint on a throttled mobile connection.

### 3. Make the source easier to maintain — medium priority

**Evidence:** most CSS is compressed into very long lines. Main styles and navigation code are embedded in `index.html`, while `presentation.css` also overrides page navigation and image styling.

**Suggested change:** format the source, extract page CSS and JavaScript into named files, and group page and deck styles by responsibility. Keep the no-build workflow unless future requirements justify introducing tooling. Recheck responsive layouts after separating overrides.

### 4. Reduce page/slide content drift — medium priority

**Evidence:** explanations are separately authored in the HTML and the `slides` array. The process slide's `section` is `producto`, but the actual process section has no ID, so “Ver apartado web” points to the product instead of the process.

**Suggested change:** give the process section a stable ID and update its slide target. Document shared wording or introduce a small shared content source if the site expands. Keep slide summaries concise rather than mechanically copying full page paragraphs.

### 5. Add accessible, public references — medium priority

**Evidence:** technology and sustainability claims cite “apuntes” by page and section, but those notes are not available in the repository. Two competitor links are supplied, without a broader bibliography or dated comparison.

**Suggested change:** add a sources section containing titles, authors/publishers, URLs, and access dates. Where appropriate, link to publicly available sources for additive manufacturing, circular design, and the emerging technologies. Include teaching material only with suitable reuse terms. A small comparison table would make the market proposal more concrete.

### 6. Extend accessibility and responsive verification — medium priority

**Evidence:** the deck already includes focus trapping, inert background content, a live status region, and focus restoration. Active page navigation is represented by a CSS class only. Navigation rules hide the future link at some intermediate widths, and the conclusion link is hidden on desktop by an override.

**Suggested change:** add a skip-to-content link, expose the active section with `aria-current`, and consider keeping all section links available through an earlier menu breakpoint. Check the menu's Escape behavior, deck scrolling on short screens, zoom, screen-reader announcements, and fullscreen focus behavior in actual browsers. Evaluate color contrast with a tool rather than inferring it from appearance.

### 7. Improve presentation and sharing polish — lower priority

**Evidence:** basic description and theme metadata are present; there is no favicon, Open Graph metadata, dedicated social preview, or print stylesheet. Google Fonts is an external dependency.

**Suggested change:** add a favicon and share image, then set social metadata and a canonical URL once the public URL is known. Consider a printable summary or slide export for classroom use and self-hosted fonts if reliable offline presentation matters.

### 8. Record ownership and asset provenance — before encouraging reuse

**Evidence:** no license or asset provenance document was supplied. Images identify themselves as AI-generated but have no accompanying record of the generation source or reuse terms.

**Suggested change:** have the project owner choose a code license and document illustration provenance and terms in an asset credits file. Add author/project attribution that the owner wants to publish.

## Remaining useful follow-ups

1. Publish the prepared repository and enable GitHub Pages.
2. Choose a code license and complete creator/generation/reuse details in `ASSET_CREDITS.md`.
3. Add references for the emerging-technology research ideas and develop a dated market comparison. Keep shared page/slide wording aligned as it evolves.
4. Once the public URL is known, add an absolute canonical URL and social-preview image URL.
5. Review with a screen reader, contrast tooling, browser zoom, Firefox, and Safari. Consider offline fonts or a print/export view if classroom use calls for them.

## Validation scope

`python scripts/check_site.py` checks static structure, image dimensions, local paths including `srcset`, fragment and ARIA targets, slide destinations, and JavaScript syntax. `python scripts/check_browser.py` exercises interactions in Chromium. Both are configured in GitHub Actions. These checks do not constitute a full accessibility audit or a measured Core Web Vitals benchmark.

### Local results

- The checker passed after the photo update: 1 HTML page, 43 local references, and 2 JavaScript sources.
- In-memory fault injection confirmed that the checker rejects missing assets, incorrect filename casing, missing fragment targets, duplicate IDs, images without an `alt` attribute, and invalid JavaScript.
- Chromium checks passed with JavaScript disabled, with either page or presentation JavaScript blocked, and with normal/reduced motion.
- Page navigation/layout checks passed at 1440×900, 1280×720, 1024×768, 768×1024, 375×812, and 320×640.
- All 11 slides passed horizontal-overflow and scroll-start checks at 1440×900, 844×390, 375×812, and 320×640.
- Keyboard navigation, slide selection, focus trapping/restoration, fullscreen entry/exit, correct process-section return, and the swipe handler passed. Page and slide images selected WebP sources; no PNG requests occurred in the page-loading check.
- Tests served the site under `/dist/` to exercise subpath-compatible relative URLs. Desktop/mobile screenshots were also inspected locally.
- The four new public references were retrieved successfully during implementation. GitHub-hosted workflow execution remains to be exercised after publication.
