# Filament Prices TR

A home screen web app for iPhone that shows what base-model PLA and PETG
filament costs in Turkey, whether each offer is in stock, pre-order or out of
stock, and the price in US dollars at the current market rate.

Sister app to Printer Prices TR; same shape, same hourly job, different
watchlist.

## What is on the watchlist

- **Brands:** eSUN, Elegoo, Sunlu, Yousu, Porima, Creality, Bambu Lab.
- **Materials:** PLA and PETG, the plain base product only. Specialty lines
  are left out on purpose: PLA+, Silk, Matte, CF/carbon, Hyper, HS, Rapid,
  Pro, Tough, Marble, Sparkle, support material and so on.
- **Size:** 1 kg spools. Anything that states another weight (0.5 kg, 250 g,
  2 kg) or more than one spool in the box is dropped.
- **Colours:** black and white only. Off-white shades (ivory, bone, jade,
  cold white) count as white, so each row shows the store's own wording.
- **Spool and refill** are separate entries, labelled.

## How it works

- `collector/collect.py` runs once an hour on GitHub Actions
  (`.github/workflows/collect.yml`). It reads each store in
  `collector/stores.json`, finds the watchlist spools through the store's
  sitemap (or its Shopify product feed), opens every candidate product page
  and writes `docs/data/prices.json`.
- The job starts at 7 minutes past each hour (GitHub may start it a few
  minutes late) and commits only `docs/data/prices.json` and
  `collector/known_urls.json` (the cache of product URLs it has found). If
  the collector crashes or produces an empty result, nothing is published
  and the previous prices stay. If `main` changed during the run, the job
  rebases onto it before pushing.
- `docs/` is the web app, served by GitHub Pages. The Refresh button loads
  the newest `prices.json` and a live USD/TRY rate.
- Stores that answer automated reading with a bot check are not worked
  around. They are listed in the app under "Stores that could not be read".

## Changing the watchlist

Everything is at the top of `collector/collect.py`:

| What | Where |
| --- | --- |
| Brands | `BRANDS` |
| Materials | `MATERIALS` |
| Colours | `COLOURS` |
| Believable price range for 1 kg | `FLOOR`, `CEILING` |
| Which pages are worth opening | `URL_RE` |
| Specialty lines to exclude | `NOT_BASE_RE` |
| Other weights and multi-packs | `NOT_1KG_RE`, `MULTIPACK_RE` |
| Dryers, holders and other kit | `ACCESSORY_RE` |

To add PLA+ back, drop `plus` from `NOT_BASE_RE`. To add a colour, add it to
`COLOURS` and to `URL_RE`.

## Stores

Add a store to `collector/stores.json` with an `id`, `name` and `base` URL.
Optional keys: `platform: "shopify"`, `sitemaps`, `price_re` (when the page's
structured price excludes VAT), `instock_markers` and `preorder_markers`.

## Run it on a PC

    python collector/collect.py                  # full run
    python collector/collect.py --only robo90    # one store
    python collector/collect.py --probe          # print results, write nothing
    python collector/collect.py --rediscover     # ignore the cached product URLs
    python -m http.server 8765 --directory docs  # then open localhost:8765

Only the Python standard library is needed (`make_icons.py` needs Pillow).

## Notes

- Prices are the stores' own current prices in lira, VAT included.
- Dollar amounts are conversions, not store prices.
- If a store cannot be read during a run, its last known offers stay on
  screen marked as old, for up to 14 days.
