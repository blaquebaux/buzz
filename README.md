# Blaque Baux Buzz

**Alt-data & smart-money signals — social sentiment, 13F cloning, insider flow, buybacks. Via ETFs: a null, with a survivorship sting.**

Buzz is the family's one toe outside price-only data. The cheap first pass tests the **ETF embodiments** of each
alt-data signal — and finds not just that they don't work, but *why you'd be fooled into thinking they do*.

> **Not investment advice.** Educational/research software. See [DISCLAIMER](DISCLAIMER.md) and [LICENSE](LICENSE).

```bash
python3 research/buzz_1_altdata_etfs.py   # needs Alpaca data keys in the environment
```

## The finding (honest null)

[`research/buzz_1_altdata_etfs.py`](research/buzz_1_altdata_etfs.py) — each ETF on its own full window vs SPY,
then controlled for the large-cap-growth tilt (VUG):

| ETF | signal | window | Sharpe | α/VUG | M² exc | |
|---|---|---|---|---|---|---|
| BUZZ | social sentiment | 2021→2026 | +0.37 | −9.2% | −9.3% | live |
| GURU | 13F cloning | 2016→2026 | +0.64 | −2.2% | −4.3% | live |
| KNOW | insider sentiment | 2016→2026 | −0.04 | −8.2% | −16.3% | live |
| PKW | buyback flow | 2016→2026 | +0.73 | +1.2% | −2.6% | live |
| IBLN | billionaire 13F | 2016→**2018** | +1.17 | +4.2% | +0.1% | ✝ **delisted** |
| NFO | insider sentiment | 2016→**2020** | +1.17 | +2.5% | −0.3% | ✝ **delisted** |

SPY reference Sharpe +0.88. **Every *live* fund underperforms** — social and insider are outright disasters
(−57% and −76% drawdowns), 13F and buyback are growth-beta-or-worse. The only names with "alpha" (IBLN, NFO)
are the ones that **died mid-sample** — flattering 2–4 year stubs the market shut down.

## Verdict

**NULL — ETF-packaged alt-data is beta, not signal.** And the sharpest lesson is the **survivorship trap**: the
best-looking funds are the delisted ones, so a naïve screen of *surviving* alt-data ETFs reads up and lies. Reading
a dead fund's truncated window as alpha is precisely the error this sleeve exists to catch. Any real edge lives in
the **raw feeds** — news/NLP sentiment, 13F filings with the 45-day disclosure lag, Form-4 insider buys — with
lag-aware timing, which is a non-price feed and a `buzz_2`. The ETFs are the cheap first look, and they say no.

## Status
**Research — null (ETF proxies); raw-feed test is the open v2.** No live rail.

## Layout
```
research/  _buzz_common.py          — bars + toolkit + per-ETF pair() aligner
           buzz_1_altdata_etfs.py   — BUZZ/GURU/IBLN/NFO/KNOW/PKW vs SPY, growth-controlled, survivorship-flagged
```

## The Blaque Baux family
One sleeve of the **Blaque Baux** family. The [core repo](https://github.com/blaquebaux/base) is the
base/blueprint and holds the [full family roster](https://github.com/blaquebaux/base#the-blaquebaux-family).

## License
[MIT](LICENSE). (c) 2026 Carter Warrens.
