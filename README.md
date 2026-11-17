# NewLife 3D

A Spanish-language academic concept website exploring personalized hand prostheses, additive manufacturing, and circular design. It includes a scrolling website and an integrated **11-slide presentation**.

The proposed AI, IoT, cloud, and manufacturing services are project concepts. The implemented software is the website and its presentation interface. Real photographs show independent prosthetics initiatives, with source and license credits; they do not depict NewLife clients or products.

## Features

- Responsive sections covering the idea, product, process, enabling technologies, sustainability, market, and future research.
- Presentation mode with slide selection, arrow-key navigation, touch gestures, and optional fullscreen.
- Presentation focus management, live slide announcements, and reduced-motion styles.
- Responsive WebP photographs with JPEG fallbacks; slide images render on first visit.
- Visible content and expanded navigation when JavaScript is unavailable.
- Skip-to-content navigation, accessible active-section indicators, and public references.
- Static HTML, CSS, and JavaScript; no package installation or build step.

## Run locally

From the repository root, with Python 3 installed:

```sh
python -m http.server 8000 --bind 127.0.0.1 --directory dist
```

Open <http://localhost:8000>. Stop the server with `Ctrl+C`.

The website uses Google Fonts over the network and falls back to system sans-serif fonts. All site images and scripts are local.

### Presentation controls

Click **Presentar** or **Presentar el proyecto** to open the slides.

| Control | Action |
| --- | --- |
| Arrow keys / Page Up / Page Down | Previous or next slide |
| Home / End | First or last slide |
| Slide selector | Jump to a slide |
| Horizontal swipe | Previous or next slide on touch devices |
| Ver apartado web | Close the presentation and open its associated section |
| Esc / Volver a la web | Close the presentation |

Fullscreen depends on browser support. A browser may consume the first Escape press to leave fullscreen.

## Repository layout

```text
newlife-site/
├── .github/workflows/     # Automated checks and manual Pages deployment
├── .openai/hosting.json   # Existing project-specific hosting configuration
├── dist/                 # Editable website and deployment root
│   ├── assets/           # Reference photos, responsive WebP copies, and SVG favicon
│   ├── index.html        # Page content, references, and presentation shell
│   ├── site.css          # Theme, page layout, navigation, and illustrations
│   ├── site.js           # Navigation, scroll status, and optional reveal effects
│   ├── presentation.css  # Presentation-only styles
│   └── presentation.js   # Slide content and presentation behavior
├── docs/                 # Project review and asset credits
├── scripts/              # Static/browser checks and optional image optimization
└── CONTRIBUTING.md
```

**`dist/` is the source of truth**, despite its conventional build-output name. Edit these files directly and keep them in Git. There is no separate source tree or generated build to regenerate them from.

The parent workspace also contains `source-docs/` (currently empty) and `tools-temp/` (one-off editing scripts, download/transfer helpers, note images, and a deployment archive). The Git repository starts at `newlife-site/`.

## Checks

Install Python **3.10+** and Node.js **24+**, then run:

```sh
python scripts/check_site.py
```

The checker verifies page metadata, unique IDs, image alternative text and dimensions, local assets (including `srcset`), fragment links, ARIA target references, slide-section destinations, and JavaScript syntax. It resolves local paths with exact filename casing for compatibility with GitHub Pages. It does not fetch external links.

### Browser checks

Install the optional browser tooling, then run:

```sh
python -m pip install playwright==1.65.2
python -m playwright install chromium
python scripts/check_browser.py
```

The browser check starts and stops its own local preview server. It covers disabled/failed JavaScript, responsive navigation, WebP selection, all 11 slides at desktop and mobile sizes, keyboard controls, focus, fullscreen, and the swipe handler. It blocks remote font requests to exercise the system-font fallback. Use `--screenshots EXISTING_DIRECTORY` to save preview screenshots.

GitHub Actions runs both static and browser checks on pushes and pull requests. See [CONTRIBUTING.md](CONTRIBUTING.md) for additional manual checks.

## Image maintenance

The optimized images are ready to serve. To regenerate them after editing the JPEG working masters:

```sh
python -m pip install Pillow==13.0.0
python scripts/optimize_images.py
```

This produces 640, 1024, and 1536-pixel-wide WebP copies. The current full-size pair totals **403,140 bytes**, compared with **782,963 bytes** for the JPEG pair: **48.5% smaller**. The 640-pixel pair totals about **88 KB**. Browsers select an appropriate variant using `<picture>` and `srcset`.

To re-import the original licensed photographs and regenerate all variants, run `python scripts/optimize_images.py --download`. The import verifies source checksums and creates the 1536×1024 JPEG working masters. See [asset credits](docs/ASSET_CREDITS.md) for photo context, sources, licenses, and modification details.

## GitHub repository

The project repository is [calebmartinc14/newlife](https://github.com/calebmartinc14/newlife).

To get a local copy:

```sh
git clone https://github.com/calebmartinc14/newlife.git
```

From the repository root, review and publish future changes with:

```sh
git status
git diff
git add dist README.md CONTRIBUTING.md docs scripts .github .gitignore .gitattributes .editorconfig
git commit -m "Update site"
git push origin main
```

### Deploy with GitHub Pages

1. In the GitHub repository, open **Settings → Pages** and set **Source** to **GitHub Actions**.
2. Open **Actions → Deploy GitHub Pages → Run workflow** and select `main`.
3. After validation and deployment complete, use the URL shown in the deployment job or Pages settings.

Deployment is manually triggered. Run the workflow again to publish later updates. The workflow uploads only `dist/`, and relative asset paths support the GitHub Pages project URL `https://calebmartinc14.github.io/newlife/` once Pages is enabled and deployed.

For other static hosts, set the publish directory to `dist` and leave the build command empty.

## Project review and next steps

See [the project review](docs/PROJECT_REVIEW.md) for the folder analysis, completed improvements, and remaining recommendations. Useful follow-ups include a full accessibility review, additional research references, and URL-specific sharing metadata after publication.

## Licensing

A code license has not been selected. The reference photographs have their own documented licenses; see [asset credits](docs/ASSET_CREDITS.md) for their attribution and the remaining logo/earlier-artwork provenance details.
