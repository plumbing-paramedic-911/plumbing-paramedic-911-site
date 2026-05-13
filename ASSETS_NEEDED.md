# Image & Asset Checklist

The site references the following files. Upload them to the repository root (or the indicated path) before launch. All paths assume the canonical host `https://plumbingparamedic911.com`.

## Required at root `/`

| File | Size | Purpose |
| --- | --- | --- |
| `/logo.png` | 600 × 600 px, transparent PNG | Schema.org `Organization.logo` and visible logos |
| `/favicon.png` | 512 × 512 px PNG | Source for all favicons |
| `/favicon.ico` | 32×32 / 16×16 multi-icon | Legacy favicon for older browsers |
| `/favicon-16x16.png` | 16 × 16 | Standard favicon |
| `/favicon-32x32.png` | 32 × 32 | Standard favicon (retina) |
| `/apple-touch-icon.png` | 180 × 180 | iOS home-screen icon |
| `/apple-touch-icon-152x152.png` | 152 × 152 | iPad |
| `/apple-touch-icon-120x120.png` | 120 × 120 | iPhone (older) |
| `/apple-touch-icon-76x76.png` | 76 × 76 | iPad mini (older) |
| `/android-chrome-192x192.png` | 192 × 192 | Android home-screen |
| `/android-chrome-512x512.png` | 512 × 512 | Android splash + PWA |
| `/og-image.jpg` | 1200 × 630 JPG | Open Graph / Twitter Card default |
| `/safari-pinned-tab.svg` | square SVG | Optional Safari pinned-tab icon |

## Per-page OG images (optional but recommended)

Drop these in `/images/og/`. If a per-page OG image is missing, the default `/og-image.jpg` is used.

| File | For page |
| --- | --- |
| `/images/og/home-1200x630.jpg` | Home |
| `/images/og/emergency-1200x630.jpg` | /services/24-7-emergency-plumbing/ |
| `/images/og/drain-cleaning-1200x630.jpg` | /services/drain-cleaning/ |
| `/images/og/water-heater-1200x630.jpg` | /services/water-heater-repair-replacement/ |
| `/images/og/leak-detection-1200x630.jpg` | /services/leak-detection/ |
| `/images/og/fixtures-1200x630.jpg` | /services/plumbing-fixture-installation-repair/ |
| `/images/og/well-pump-1200x630.jpg` | /services/well-pump-repair/ |
| `/images/og/backflow-1200x630.jpg` | /services/backflow-prevention-testing/ |
| `/images/og/commercial-1200x630.jpg` | /services/commercial-plumbing/ |
| `/images/og/abbeville-1200x630.jpg` | /service-areas/abbeville-sc/ |
| `/images/og/greenwood-1200x630.jpg` | /service-areas/greenwood-sc/ |
| `/images/og/anderson-1200x630.jpg` | /service-areas/anderson-sc/ |
| `/images/og/laurens-1200x630.jpg` | /service-areas/laurens-sc/ |
| `/images/og/mccormick-1200x630.jpg` | /service-areas/mccormick-sc/ |
| `/images/og/ninety-six-1200x630.jpg` | /service-areas/ninety-six-sc/ |
| `/images/og/calhoun-falls-1200x630.jpg` | /service-areas/calhoun-falls-sc/ |
| `/images/og/due-west-1200x630.jpg` | /service-areas/due-west-sc/ |

## Photos referenced in schema (recommended for Google Business + AI engines)

Drop in `/images/`. Use real, original photos of the truck, team, and completed work.

| File | Aspect | Purpose |
| --- | --- | --- |
| `/images/truck-1x1.jpg` | 1:1 (1000×1000) | Schema `image` array — square |
| `/images/truck-4x3.jpg` | 4:3 (1200×900) | Schema `image` array — 4:3 |
| `/images/truck-16x9.jpg` | 16:9 (1920×1080) | Schema `image` array — 16:9 |
| `/images/eric-callaway.jpg` | 4:5 (800×1000) | Schema `Person.image` — owner headshot |

## How to generate the icon set quickly

The easiest path is to upload one square master PNG (1024 × 1024) and use a free generator such as **realfavicongenerator.net** or **favicon.io** to produce every size above in one zip. Drop the zip contents into the repo root.

## After uploading

1. Verify each path returns 200 (no 404s) in browser devtools.
2. Run the homepage URL through Google's Rich Results Test (`https://search.google.com/test/rich-results`) to confirm schema images load.
3. Run the homepage through the Meta Sharing Debugger (`https://developers.facebook.com/tools/debug/`) and the Twitter/X Card Validator to confirm OG image renders.
