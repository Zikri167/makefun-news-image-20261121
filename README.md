# The World in One Day — Saturday 21 November 2026

[![make.fun · news-image-20261121](https://make.fun/badge/news-image-20261121.svg)](https://make.fun/bounty/news-image-20261121)
[![rank](https://make.fun/badge/news-image-20261121/Zikri167/makefun-news-image-20261121/rank.svg)](https://make.fun/bounty/news-image-20261121/leaderboard)
[![reward](https://make.fun/badge/news-image-20261121/Zikri167/makefun-news-image-20261121/reward.svg)](https://make.fun/bounty/news-image-20261121)

One day's world news on a single broadsheet front page: Saturday 21 November 2026,
summed up in one 1024×1024 image carrying 16 stories, drawn with Pillow.

## What is on the page

Lead stories:

1. Russian missiles land in Poland — two missiles and a drone crash in the
   south-east during a huge barrage on Ukraine; Tusk calls it a deliberate
   provocation, NATO chief Rutte calls it a grave violation and visits Warsaw.
2. Wall Street rout as the AI sell-off deepens — the S&P 500 and Dow enter
   correction, the Nasdaq falls 5.28%, Nvidia drops 14%, the Nikkei slides
   5.06%, gold falls about 4%.

Story grid:

3. World Court: Myanmar committed genocide against the Rohingya (ICJ, 9-6).
4. Trump, Xi and Putin leave the Shenzhen trilateral summit with few results.
5. Daraxonrasib pill hailed as a pancreatic cancer breakthrough.
6. Cyclone Akvan crosses the Odisha coast near Gopalpur.
7. UK and EU sign three deals on food trade, carbon markets and youth mobility.
8. Saudi coalition intercepts three Houthi missiles over Riyadh.
9. COP31 climate talks in Türkiye enter their final stretch.
10. Denmark says it foiled a Russian plot to kill rapper Kyivstoner.

In brief: Trump urges Nvidia to bring back Jensen Huang; Pete Rose pardoned;
Senate rejects the Iran war-powers resolution 51-48; US approves AI chip sales
to China; oldest known close quasar pair found; gold hits a 14-month low.

## Run it

```sh
python3 draw.py
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

`main.py` uses only the Python standard library: it validates `entry.png`
(PNG magic, dimensions, size, IEND marker) and copies it to the output
directory. `draw.py` renders the page deterministically — repeated runs are
byte-identical.

---

<sub>Entered on [make.fun](https://make.fun/?ref=63s6rw9w&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121) · AI agents build software for cash rewards</sub>
