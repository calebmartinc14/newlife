# Contributing

## Development

1. Create a branch for a focused change.
2. Edit the website directly in `dist/`; no build is required.
3. Preview with `python -m http.server 8000 --bind 127.0.0.1 --directory dist`.
4. Run `python scripts/check_site.py` with Python 3.10+ and Node.js 24+ installed.
5. Run `python scripts/check_browser.py` for changes to layout or interactions. The optional Playwright installation steps are in the README.
6. Open a pull request explaining the change and how it was checked. Include screenshots for visual changes.

## Content and code conventions

- Keep visitor-facing copy in Spanish and preserve accents with UTF-8 encoding.
- Update both `dist/index.html` and the slide data in `dist/presentation.js` when shared information changes.
- Keep asset paths relative so deployment works under a GitHub Pages repository path.
- Preserve accessible names, keyboard operation, focus restoration, and reduced-motion support.
- Keep `dist/` tracked: it is the actual website source.
- Add references for factual claims and distinguish project proposals from implemented features.
- Document the source and reuse terms of new assets.
- Keep page styles/behavior in `site.css`/`site.js` and deck styling/behavior in `presentation.css`/`presentation.js`.
- After changing either JPEG photo master, regenerate WebP variants with `scripts/optimize_images.py` and include them in the change. Preserve source/author/license credits in the page, slides, and `docs/ASSET_CREDITS.md`.
- Keep content visible by default and reveal JavaScript-only controls only when ready.

## Browser checklist

- Check the layout on desktop, tablet, and a narrow mobile viewport; watch for horizontal overflow.
- Open and close the mobile menu, follow each section link, and check the scroll progress indicator.
- Open the presentation from each launch button and visit all 11 slides.
- Check the slide selector, previous/next buttons, arrow keys, Home/End, and touch swipes where available.
- Check fullscreen entry/exit, Escape, returning to a web section, and focus restoration.
- Use Tab and Shift+Tab to confirm focus stays in the open presentation.
- Check reduced-motion preferences, browser zoom, and image loading.
- Disable JavaScript and confirm the text and section links remain usable.
- After deployment, verify assets load under the repository subpath.
