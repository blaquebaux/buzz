#!/usr/bin/python3
# =============================================================================
# _buzz_common.py — shared helpers for Blaque Baux BUZZ (alt-data / sentiment / smart-money signals).
# Alpaca SIP daily bars; reads ALPACA_KEY_ID / ALPACA_SECRET_KEY from env. Read-only.
#
# BUZZ is the family's one toe outside price-only data: social sentiment, 13F hedge-fund cloning, insider
# (Form-4) sentiment, buyback flow. The cheap first pass uses the ETF EMBODIMENTS of each (BUZZ/GURU/NFO/
# KNOW/IBLN/PKW) — which also exposes a brutal honest tell: SURVIVORSHIP. Several of these alt-data ETFs have
# DELISTED (the market's verdict on the strategy), so the live ones are the survivors, biased UP. Verdicts
# control for the growth tilt (vs VUG) — most "sentiment alpha" is just large-cap-growth beta wearing alt-data.
# The real signal lives in the RAW feeds (news/NLP, 13F filings with lag, Form-4) — a v2; this is the proxy.
# =============================================================================
import os, json, urllib.request, math
import numpy as np

H = {"APCA-API-KEY-ID": os.environ["ALPACA_KEY_ID"], "APCA-API-SECRET-KEY": os.environ["ALPACA_SECRET_KEY"]}
START, END = "2016-01-01", "2026-08-01"
_cache = {}

def bars(s):
    if s in _cache: return _cache[s]
    u = (f"https://data.alpaca.markets/v2/stocks/bars?symbols={s}&timeframe=1Day"
         f"&start={START}&end={END}&adjustment=all&feed=sip&limit=10000")
    try:
        d = json.load(urllib.request.urlopen(urllib.request.Request(u, headers=H), timeout=40))
        _cache[s] = {b["t"][:10]: b["c"] for b in d.get("bars", {}).get(s, [])}
    except Exception:
        _cache[s] = {}
    return _cache[s]

def panel(syms):
    D = {s: bars(s) for s in syms}; D = {s: v for s, v in D.items() if len(v) > 250}
    if not D: return {}, []
    u = list(D); dates = sorted(set.intersection(*[set(D[s]) for s in u]))
    return {s: np.array([D[s][d] for d in dates], float) for s in u}, dates

def rets(px): return px[1:] / px[:-1] - 1

def stats(r):
    r = np.asarray(r, float); r = r[np.isfinite(r)]
    if len(r) < 30 or r.std() == 0: return dict(sh=float('nan'), cagr=float('nan'), dd=float('nan'), vol=float('nan'))
    cum = np.cumprod(1 + r)
    return dict(sh=r.mean()/r.std()*math.sqrt(252), cagr=cum[-1]**(252/len(r))-1,
                dd=(cum/np.maximum.accumulate(cum)-1).min(), vol=r.std()*math.sqrt(252))

def jensens_alpha(r, rb, rf=0.0):
    r = np.asarray(r, float); rb = np.asarray(rb, float); m = np.isfinite(r) & np.isfinite(rb); r, rb = r[m], rb[m]
    if len(r) < 30 or np.var(rb) == 0: return dict(alpha_ann=float('nan'), beta=float('nan'))
    beta = float(np.cov(r, rb)[0, 1]/np.var(rb))
    return dict(alpha_ann=(r.mean() - beta*rb.mean())*252, beta=beta)

def m_squared(r, rb, rf=0.0):
    r = np.asarray(r, float); rb = np.asarray(rb, float); r = r[np.isfinite(r)]; rb = rb[np.isfinite(rb)]
    if len(r) < 30 or r.std() == 0 or rb.std() == 0: return dict(m2_excess=float('nan'))
    shp = r.mean()/r.std()*math.sqrt(252); shb = rb.mean()/rb.std()*math.sqrt(252)
    return dict(m2_excess=(shp - shb)*rb.std()*math.sqrt(252))

def riskadj(r, rb, rf=0.0):
    out = dict(stats(r)); out.update(jensens_alpha(r, rb, rf)); out.update(m_squared(r, rb, rf))
    return out

def pair(etf, bench="SPY", growth="VUG"):
    """Align one ETF to SPY + a growth control over the ETF's own window; return (riskadj vs SPY, alpha vs growth, dates)."""
    P, dates = panel([etf, bench, growth])
    if etf not in P or bench not in P: return None, float('nan'), []
    r = rets(P[etf]); rb = rets(P[bench])
    a = riskadj(r, rb)
    ag = jensens_alpha(r, rets(P[growth]))["alpha_ann"] if growth in P else float('nan')
    return a, ag, dates
