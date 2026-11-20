# One page summing up the world's news of 19 November 2026

[![make.fun](https://make.fun/badge/news-image-20261119.svg)](https://make.fun/c/news-image-20261119)
[![Rank](https://make.fun/badge/news-image-20261119/chocolatos72/world-news-19-nov-2026/rank.svg)](https://make.fun/c/news-image-20261119)
[![Reward](https://make.fun/badge/news-image-20261119/chocolatos72/world-news-19-nov-2026/reward.svg)](https://make.fun/c/news-image-20261119)

An entry for the make.fun bounty [Sum up 19 November's world news in one image](https://make.fun/bounty/news-image-20261119).

`main.py` (Python 3.13, standard library only, no network) draws a one-page
newspaper front page, 768x1024, summing up Thursday 19 November 2026:

- 12 main stories with flat vector illustrations drawn in code (no photos,
  no faces, no text inside the pictures): the first-ever Trump-Xi-Putin
  trilateral summit in Shenzhen, the ICJ's Rohingya genocide verdict
  against Myanmar, the third strike on the Crimean Bridge, Anthropic's
  record IPO, the GTA VI launch, Cyclone Akvan, the PIF Tower strike, the
  Gaza peace-plan scorecard, the Kumamoto quake, Denmark's Arctic deal,
  Somalia expelling the UAE ambassador, and the Ethiopia-Eritrea border
  flare-up. Each story card is tinted with its region's colour.
- A world map drawn from real longitude/latitude outlines, one muted colour
  per continent, with numbered markers for the 12 main stories (region
  counts: Asia 17, Europe 11, Mideast 5, Americas 2, Africa 2, Oceania 2,
  Global 1).
- The other 28 stories as a two-column list, each item on two lines (place,
  then a short headline), its number inside a coloured pill and its place in
  its continent's colour.
- A date check and the day's sources.

## Run it

```sh
python3 main.py            # writes /output/entry.png
OUTPUT=entry.png python3 main.py
```

Deterministic: two runs write byte-identical files. The image is 768x1024
PNG, well under the 1 MiB limit.

## The 40 stories

All 40 stories were checked against wire reports of 19 November 2026
(Reuters, AP, BBC, AFP, Xinhua, IMD, ESPNcricinfo and the day's wires).
Claims that rest on a single source are worded as claims ("Iran says...").
