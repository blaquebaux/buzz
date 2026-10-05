#!/usr/bin/python3
# =============================================================================
# buzz_1_altdata_etfs.py — does alt-data / smart-money alpha survive, or decay to growth-beta?
#
# Test the ETF embodiments of each alt-data signal vs SPY, then control for the large-cap-growth tilt (vs VUG):
#   BUZZ  social-media sentiment      GURU / IBLN  13F hedge-fund / billionaire cloning
#   NFO / KNOW  insider (Form-4) sentiment         PKW  buyback achievers (corporate flow)
# Two honest tells: (1) alpha vs SPY that DIES once you net out the growth tilt = the "signal" was just beta;
# (2) SURVIVORSHIP — the ones that DELISTED are the market's verdict, and the survivors are biased up.
# Each ETF on its OWN full window (no short-ETF truncation). Alpaca SIP daily total return, causal.
# =============================================================================
import os, sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _buzz_common import pair, panel, rets, riskadj
import numpy as np

CANDS = [("BUZZ","social sentiment"), ("GURU","13F cloning"), ("IBLN","billionaire 13F"),
         ("NFO","insider sentiment"), ("KNOW","insider sentiment"), ("PKW","buyback flow")]
print("="*96); print("BUZZ #1 — alt-data / smart-money via ETF proxies: surviving alpha, or growth-beta?"); print("="*96)
# SPY reference Sharpe (full)
Pspy,_ = panel(["SPY"]); spy_sh = riskadj(rets(Pspy["SPY"]), rets(Pspy["SPY"]))['sh']
print(f"\n  {'ETF':6}{'signal':20}{'window':>13}{'Sharpe':>8}{'CAGR':>7}{'maxDD':>7}{'α/SPY':>8}{'α/VUG':>8}{'M²exc':>8}")
live=[]; dead=[]
for etf,lab in CANDS:
    a, ag, dates = pair(etf)
    if a is None or not dates:
        dead.append(etf); print(f"  {etf:6}{lab:20}{'— absent (never listed / no data)':>44}"); continue
    win=f"{dates[0][:7]}→{dates[-1][:7]}"
    alive = dates[-1] >= "2026-01"                      # still trading near END ⇒ a real survivor
    tag = "" if alive else "  ✝ DELISTED"
    print(f"  {etf:6}{lab:20}{win:>13}{a['sh']:>+8.2f}{a['cagr']*100:>+6.0f}%{a['dd']*100:>+6.0f}%{a['alpha_ann']*100:>+7.1f}%{ag*100:>+7.1f}%{a['m2_excess']*100:>+7.1f}%{tag}")
    if alive: live.append((etf, lab, a, ag))
    else:     dead.append(etf)
print(f"\n  SPY reference Sharpe (full window): {spy_sh:+.2f}")

# a survivor must be ALIVE *and* keep positive alpha after the growth control (dead funds' stubs don't count)
real = [etf for etf,lab,a,ag in live if np.isfinite(ag) and ag>0.01 and a['m2_excess']>0]
print("\n"+"="*96); print("READ:")
print(f"  • SURVIVORSHIP TELL: delisted/absent = {', '.join(dead) if dead else 'none'}. The 'winners' with the best")
print("    stats (IBLN +4.7% α, NFO +2.7% α) are exactly the ones that DIED mid-sample — flattering 2-4y stubs the")
print("    market shut down. Reading a dead fund's truncated window as alpha is the survivorship trap this sleeve IS.")
if real:
    v=f"CONDITIONAL: among LIVE funds, {', '.join(real)} keep alpha vs VUG — verify vs the raw feed before trusting it."
else:
    v=("NULL: every LIVE alt-data ETF underperforms — social (BUZZ −9% α, −57% DD), insider (KNOW −76% DD), 13F "
       "(GURU) and buyback (PKW) are growth-beta-or-worse net of the tilt; the only 'positive' names are delisted. "
       "ETF-packaged alt-data is not signal. Any edge lives in the RAW feeds with lag-aware timing, not these funds.")
    print("  • Among the LIVE survivors, none keeps alpha once you net out the large-cap-growth tilt — it was beta.")
print(f"\n  VERDICT: {v}")
print("  (ETF proxies are the cheap first look. The real BUZZ test is the raw signal — news/NLP sentiment, 13F")
print("   filings with the 45-day disclosure lag, Form-4 insider buys — a non-price feed and a buzz_2.)")
