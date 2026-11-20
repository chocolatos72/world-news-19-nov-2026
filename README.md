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
  flare-up. The header band stays dark navy with the red date box and
  the gold count box, as in the earlier version. The page is one flat
  cream; every story sits in its own bordered box, and every illustrated
  story carries a coloured label bar over a sharply bordered illustration.
  The day's six big numbers are large red figures with thin rules between
  them (no boxes). 37 stories (three list items were dropped to keep the
  boxes readable).
- A world map drawn from real longitude/latitude outlines, one muted colour
  per continent, with numbered markers for the 12 main stories (region
  counts: Asia 16, Europe 10, Mideast 5, Americas 1, Africa 2, Oceania 2,
  Global 1).
- The other 25 stories as a two-column list, each item in its own bordered
  box on two lines (place, then a short headline), its number inside a
  coloured pill and its place in its continent's colour.
- A date check box, a line of stories left out as other days' news, and
  the day's sources.

## Run it

```sh
python3 main.py            # writes /output/entry.png
OUTPUT=entry.png python3 main.py
```

Deterministic: two runs write byte-identical files. The image is 768x1024
PNG, well under the 1 MiB limit.

## The 37 stories

All 37 stories were checked against wire reports of 19 November 2026
(Reuters, AP, BBC, AFP, Xinhua, IMD, ESPNcricinfo and the day's wires).
Claims that rest on a single source are worded as claims ("Iran says...").
