# Asset notes

## Real-world reference photographs

The website and slides use real photographs of independent prosthetics initiatives. The people, organizations, and devices pictured are not NewLife clients, collaborators, or products. These photos were retrieved and their source pages reviewed on 2026-11-17.

### Hailey Dawson using a 3D-printed hand

- **Local master:** `dist/assets/prosthesis-use.jpg`.
- **Title:** Hailey Dawson first pitch at Orioles Park, August 2015.
- **Photographer:** [Keith Allison](https://www.flickr.com/photos/keithallison/20646373096/).
- **Date:** 2015-08-17.
- **Source:** [Wikimedia Commons file page](https://commons.wikimedia.org/wiki/File:Hailey_Dawson_first_pitch_at_Orioles_Park,_August_2015.jpg).
- **License:** [Creative Commons Attribution-ShareAlike 2.0 Generic](https://creativecommons.org/licenses/by-sa/2.0/).
- **Context:** Hailey Dawson uses a 3D-printed hand to throw the ceremonial first pitch at a baseball game. This is a real application of the kind of technology discussed by the academic proposal.
- **Changes:** cropped around Hailey and her throwing hand, resized to 1536×1024, JPEG/WebP recompression, responsive resizing, metadata removal, and display framing. The local master and all `prosthesis-use-*.webp` derivatives are distributed under **CC BY-SA 2.0**.
- **Verified original SHA-1:** `ec5b004f844e5b77fc0ad67eba6b63251c9c69e1`.

### Danny Letain and the engineering team

- **Local master:** `dist/assets/prosthesis-team.jpg`.
- **Title:** Danny Letain et l'equipe d'ingenieur.
- **Photographer/publisher:** Dale Northey / [Simon Fraser University](https://www.flickr.com/photos/sfupamr/26687556342/).
- **Date:** 2016-03-18.
- **Source:** [Wikimedia Commons file page](https://commons.wikimedia.org/wiki/File:Danny_Letain_et_l%27equipe_d%27ingenieur.jpg).
- **License used:** [Creative Commons Attribution 2.0 Generic](https://creativecommons.org/licenses/by/2.0/).
- **License record:** the Commons page displays a CC0 template, but its Flickr review explicitly records **CC BY 2.0** for the original source and flags that mismatch. This project uses the verified CC BY 2.0 terms, with photographer/publisher attribution.
- **Context:** Danny Letain with a bionic arm and an engineering team. It illustrates collaboration with the person using a prosthesis; it does not document NewLife or demonstrate 3D printing.
- **Changes:** resized to 1536×1024 with minimal aspect-ratio cropping, JPEG/WebP recompression, responsive resizing, metadata removal, and display framing. The local master and all `prosthesis-team-*.webp` derivatives are distributed under **CC BY 2.0**.
- **Verified original SHA-1:** `8857c60866ba1a10810bd1a0c72f14cdf2965e22`.

### Responsive variants and regeneration

Each photo has 640, 1024, and 1536-pixel-wide WebP versions, generated with Pillow 13.0.0 at quality 82 and method 6. The JPEGs serve as working masters and browser fallbacks.

| Photograph | Local JPEG | Full-size WebP |
| --- | ---: | ---: |
| Hailey Dawson | 467,716 bytes | 275,498 bytes |
| Danny Letain and team | 315,247 bytes | 127,642 bytes |
| **Combined** | **782,963 bytes** | **403,140 bytes** |

The full-size WebP pair is 48.5% smaller than the JPEG pair; the 640-pixel pair totals 87,524 bytes. Actual requests depend on viewport, pixel density, caching, and browser support.

`python scripts/optimize_images.py` regenerates WebP variants from the JPEG working masters. Add `--download` to re-import the two verified source files before generating the variants. This checks the original checksums and resizes the photos without changing their attribution or license terms. The website's **Fuentes → Fotografías** section and the slide captions also provide credits and source/license links.

## Earlier conceptual artwork

The earlier `prosthesis.png`, `workshop.png`, and their WebP derivatives were supplied or generated during the initial concept design. They are no longer referenced by the page or slides. Their AI generation service, prompt, creator, date, and reuse terms were not supplied.

## Logo and favicon

`dist/assets/favicon.svg` adapts the inline SVG brand mark already supplied in the website. No separate creator or license was supplied for the original mark.

## Fonts and references

The page requests DM Sans and Space Grotesk through Google Fonts, with system sans-serif fallbacks. Public conceptual references are linked in the website's **Fuentes** section. Photograph licenses apply to the photographs and their derivatives; a separate code license has not been selected.
