#!/usr/bin/env python3
"""Per-run publisher for the 2026-07-21 ~10:19a management run.
Follows OPS-ALERT rules: unique script name, backup first, atomic write, verify read-back."""
import json, os, shutil, sys, tempfile

SITE = os.path.dirname(os.path.abspath(__file__))
PATH = os.path.join(SITE, "engine-data.json")
TS = "2026-07-21T10:19:00-04:00"

with open(PATH) as f:
    data = json.load(f)

print("TOP-LEVEL KEYS:", list(data.keys()))

# ---- backup the current good state first ----
bak = os.path.join(SITE, "engine-data.backup-2026-07-21-1019.json")
shutil.copyfile(PATH, bak)

# ---- top-level freshness stamp ----
data["updated"] = TS

# ---- status (<=3 terse cards, Morning->Afternoon->Evening) ----
data["status"] = [
    {"session": "Open",   "text": "Bought AMD, cut SQQQ hedge"},
    {"session": "Regime", "text": "Gate shut day 6: QQQ under $716"},
    {"session": "Books",  "text": "Live cash; PLTR staged, tap fills"},
]

# ---- headlines (most relevant first) ----
data["headlines"] = [
    "Chip bounce fading from the open highs on cue: SOXL +13%->+9.2%, AMD +6.3%->+4.0% (near its day low), INTC +4.4% - the same 'pop-then-fade under the 20-day' that's round-tripped 5 sessions running.",
    "Gate shut day 6: QQQ $703 is ~1.8% under its $716 20-day while SPY +0.4% sits near records - a chip/Nasdaq-specific bid, not broad risk-on - so no SOXL/TQQQ 3x longs.",
    "BE +10.4% is today's biggest watchlist mover - a dead-cat bounce off Monday's TD Cowen data-center-delay flush; we cut it live at $203 on the broken thesis, not chasing it back.",
    "SMR +5.2% and the nuclear-for-AI names bid again on AI-power demand; an extended ~$8 spec - watch, don't chase.",
    "AMD +4.0% holding green into its 7/22-23 Advancing AI event (MSFT Helios rack-scale) - the ownable 1x chip leader we hold in paper.",
    "Earnings wall midweek: GOOGL + TSLA Wed 7/22 AMC, INTC Thu 7/23 - the residual 100-sh SQQQ hedge is insurance into it.",
    "PLTR the clean 1x RS leader (Aug 3 earnings, no gate) but -0.4% today, lagging the chip tape; the funded live buy stays staged for approval.",
]

# ---- coverage: refresh chg_pct + projection + updated for every name ----
cov = {
    "AMD":  {"chg_pct": 4.0,  "proj": {"target_pct": 5.0,  "confidence": "med", "basis": "owned the pop; drifts into 7/22-23 event + MSFT Helios", "pop_rank": 1}},
    "INTC": {"chg_pct": 4.4,  "proj": {"target_pct": 5.0,  "confidence": "med", "basis": "High-NA EUV first + Fortinet deal; earnings-Thu overhang", "pop_rank": 2}},
    "SOXL": {"chg_pct": 9.2,  "proj": {"target_pct": 8.0,  "confidence": "low", "basis": "biggest 3x mover but gated + fading under the 20-day", "pop_rank": 3}},
    "SMR":  {"chg_pct": 5.2,  "proj": {"target_pct": 5.5,  "confidence": "low", "basis": "nuclear-for-AI spec bid; extended, not chasing", "pop_rank": 4}},
    "NVDA": {"chg_pct": 0.5,  "proj": {"target_pct": 2.0,  "confidence": "med", "basis": "bellwether laggard resting on its 20-day support", "pop_rank": 5}},
    "TQQQ": {"chg_pct": 3.0,  "proj": {"target_pct": 3.5,  "confidence": "low", "basis": "3x Nasdaq gated; tracks QQQ +1.0%", "pop_rank": 6}},
    "VRT":  {"chg_pct": 2.4,  "proj": {"target_pct": 3.0,  "confidence": "med", "basis": "AI-datacenter power riding the chip bid; earns 7/29", "pop_rank": 7}},
    "PLTR": {"chg_pct": -0.4, "proj": {"target_pct": 1.0,  "confidence": "med", "basis": "1x RS leader lagging the chip day; the live target", "pop_rank": 8}},
    "BE":   {"chg_pct": 10.4, "proj": {"target_pct": 8.0,  "confidence": "low", "basis": "dead-cat bounce off the TD Cowen flush; cut, not chasing", "pop_rank": 9}},
    "TSLA": {"chg_pct": 2.5,  "proj": {"target_pct": 2.0,  "confidence": "low", "basis": "bouncing into Wed earnings; binary, avoid", "pop_rank": 10}},
    "CEG":  {"chg_pct": 1.9,  "proj": {"target_pct": 2.5,  "confidence": "med", "basis": "held; nuclear-AI power ballast, green", "pop_rank": 11}},
    "IONQ": {"chg_pct": 2.7,  "proj": {"target_pct": 3.0,  "confidence": "low", "basis": "quantum high-beta bouncing with the risk tape", "pop_rank": 12}},
    "RKLB": {"chg_pct": 2.2,  "proj": {"target_pct": 2.5,  "confidence": "low", "basis": "space beta basing; won the $17B NSSL award", "pop_rank": 13}},
    "FNGU": {"chg_pct": 0.7,  "proj": {"target_pct": 1.5,  "confidence": "low", "basis": "3x FANG gated; mega-cap muted today", "pop_rank": 14}},
    "SQQQ": {"chg_pct": -3.0, "proj": {"target_pct": -3.5, "confidence": "low", "basis": "inverse hedge bleeding; 100 sh held into Wed prints", "pop_rank": 15}},
}
seen_ranks = []
for entry in data.get("coverage", []):
    t = entry.get("ticker")
    if t in cov:
        entry["chg_pct"] = cov[t]["chg_pct"]
        entry["projection"] = cov[t]["proj"]
        entry["updated"] = "10:19a"
        seen_ranks.append(cov[t]["proj"]["pop_rank"])
# AMD position note refresh (faded to its day low but held)
for entry in data.get("coverage", []):
    if entry.get("ticker") == "AMD":
        entry["size_note"] = "held 30 sh @ $527.80 (paper); +4% but faded from the $535 open high to near its day low - $458 GTC stop; sell into a 7/22-23 event pop"
    if entry.get("ticker") == "SQQQ":
        entry["size_note"] = "residual 100 sh (trimmed from 310); -3% today, the book's biggest day drag; $38 GTC stop; cut fully on a QQQ $716 reclaim"

assert sorted(seen_ranks) == list(range(1, 16)), f"pop_rank not 1..15 unique: {sorted(seen_ranks)}"

# ---- feed: prepend one activity item ----
data["feed"].insert(0, {
    "ts": TS, "type": "activity",
    "text": "10:19am management run: both books re-verified clean at the broker (PAPER 5/5 GTC-stopped, zero naked - AMD/PLTR/NVDA/CEG/SQQQ; LIVE flat $810 cash). No new trades - the morning already rotated (cut the SQQQ hedge 310->100, bought AMD 30 sh). Chip pop fading on cue (SOXL +13%->+9.2%, AMD near its day low), QQQ $703 still under its $716 20-day (gate shut day 6). Biggest movers un-owned: BE +10.4% (cut, broken thesis), SOXL +9.2% (gated), SMR +5.2% (spec). PLTR live buy still staged - approve = fills now. Day-trade 0/3.",
})

# ---- pulse: prepend one entry ----
data["pulse"].insert(0, {
    "ts": TS,
    "text": "10:19am, one-hour-in management run - no new trades (the morning already did the rotation). Both books re-verified clean: PAPER 5/5 GTC-stopped zero-naked (AMD/PLTR/NVDA/CEG/SQQQ), LIVE flat $810 cash with the PLTR buy (ticket 2026-07-20-3, $122 stop) still staged - one tap fills it now. The open chip pop is fading on cue - SOXL +13%->+9.2%, AMD +6%->+4% (near its day low), QQQ $703 still ~1.8% under its $716 20-day (gate shut day 6) - so no 3x chase. Honest read: paper's -0.5% while the biggest movers run un-owned (BE +10.4% dead-cat, SOXL +9.2% gated, SMR +5.2% spec); AMD's the one clean ownable leader and we hold it. Powder stays dry for a QQQ $716 reclaim or a fade into Wed's GOOGL/TSLA prints. Day-trade 0/3.",
    "hype": "One hour in, nothing worth chasing - the chip pop's fading like it has all week, so no leverage; we own the one clean mover (AMD) while PLTR sits a tap from filling live.",
})

# ---- accountability (running, intraday) ----
data["accountability"] = {
    "date": "2026-07-21",
    "final": False,
    "grade": "C (running, intraday)",
    "headline": "One hour in: the D-fix is executing - I rotated EARLY (cut the losing SQQQ hedge 310->100 and bought the pop_rank-1 AMD in the MORNING, not at 3pm like yesterday) and own the one clean ownable mover (AMD +4%). But capture is still ~0%: paper's -0.5% on the day while the three biggest watchlist movers run un-owned - BE +10.4% (a dead-cat bounce off the TD Cowen flush we correctly cut), SOXL +9.2% (the gated 3x), SMR +5.2% (an extended ~$8 spec) - and LIVE is still 100% cash awaiting the PLTR tap. Process improved over yesterday; the result hasn't yet. The gate is on trial: it's kept us out of a SOXL pop that's fading again on cue (5th session), but if these chip pops stop fading it costs capture. Final grade at the close.",
    "capture": {
        "bestName": "BE (dead-cat) / SOXL (gated 3x)",
        "bestPct": "+10.4% / +9.2%",
        "capturedPct": "paper -0.5%, live 0%",
        "rate": "~0% - biggest movers un-ownable; AMD +4% owned",
    },
    "missed": [
        {"from": "live cash", "to": "PLTR (staged, untapped)", "note": "live's been 100% cash awaiting the tap while the RS leader + chip movers trade - the staged ticket is the fix but only helps once tapped", "delta": "opportunity, pending tap"},
        {"from": "paper SQQQ hedge", "to": "a clean 1x leader", "note": "the residual 100-sh SQQQ (-3%) still drags the book on a green tape; kept as Wed-earnings insurance but it caps today's capture", "delta": "-$124 day drag"},
    ],
    "saved": [
        {"note": "Held the 3x gate a 6th day - didn't chase SOXL +13%->+9.2% / TQQQ +3.0% under a sub-20-day QQQ; the pop is fading again on cue (5th session)", "delta": "discipline intact"},
        {"note": "All 5 paper stops verified live GTC, zero naked; live clean cash - never-naked held both books", "delta": "safety intact"},
    ],
    "best": {"name": "AMD (30 sh @ $527.80, paper)", "note": "owned the pop_rank-1 chip leader into its 7/22-23 event - the one clean ownable mover today", "delta": "+4% and owned"},
    "worst": {"name": "SQQQ hedge", "note": "the residual 100 sh (-3% today) is the book's biggest day drag; kept as Wed insurance but it's on a leash - cut on a QQQ $716 reclaim", "delta": "-$124 day drag"},
    "avoided": {"worstName": "gated 3x chip chase (SOXL/TQQQ)", "worstPct": "faded from +13% to +9.2% and still going", "note": "the gate kept both books out of the leveraged pop that's round-tripped 5 sessions running", "amount": "pending the close", "rate": "high on any gated chase"},
    "applying": "PLAYBOOK Earned Rule #1 (regime gate - no 3x-index long under the 20-day) + the 7/20 D-fix 'rotate EARLY': cut the dead hedge and bought the ownable 1x leader (AMD) in the MORNING, and staged the live leader-buy pre-open, not at 3pm.",
    "adjust": "Live needs to actually FILL - the PLTR tap is the whole game; if it's still cash by the close that's another D on execution. Paper: on a clean QQQ $716 reclaim cut the last SQQQ + add a 1x leader (NVDA); on a fade under $700 the hedge + wide AMD stop do the work into Wed's GOOGL/TSLA prints. Watch AMD's 7/22-23 event for a sell-into-strength exit.",
}

# ---- score (alpha recomputed real: live -19.0% vs buy&hold TQQQ 7/2 $73.35 -> $69.65 = -5.0%) ----
data["score"] = {
    "alphaPts": "-13.9",
    "benchmark": "-5.0%",
    "bestDay": "+3.2%",
    "bestDayName": "Jul 14 - CPI chip rally (settled)",
    "winRate": "33%",
    "tradeCount": 6,
}

# ---- paper / live intraday marks ----
data["paper"]["equity"] = 89181.76
data["paper"]["updated"] = TS
data["paper"]["equity_note"] = "Paper ~$89.18k (-0.5% vs Mon - AMD +4% offset by the SQQQ hedge -3% + flat NVDA/PLTR), 5/5 GTC-stopped, zero naked (AMD 30/$458, PLTR 100/$125, NVDA 90/$186, CEG 16/$236, SQQQ 100/$38). ~$33.4k (~37%) dry powder held in a gated regime: on a QQQ $716 reclaim add a 1x leader (NVDA) + cut the hedge; on a fade the hedge covers into Wed's GOOGL/TSLA prints. No 3x under the 20-day."

data["live"]["equity"] = 810.32
data["live"]["cash"] = 810.32
data["live"]["positions"] = []
data["live"]["updated"] = TS
data["live"]["equity_note"] = "Flat/clean cash ($810.32), zero positions/orders, nothing naked. PLTR buy staged for approval (ticket 2026-07-20-3, 5 sh, ~$134 marketable, $122 GTC stop) - market's open, approve = fills now. Broker-verified 10:15 ET. Live's been in cash since the 7/20 BE cut - the tap is the whole game."

# ---- pending_tickets: the staged PLTR live buy ----
data["pending_tickets"] = [{
    "id": "2026-07-20-3", "symbol": "PLTR", "side": "buy", "size": "$680", "qty": 5,
    "entry": "~$134 marketable - market open, approve = fills now", "trigger": None, "stop": 122,
    "bracket": "stop $122 GTC (below the $129-131 two-week base, -10%)",
    "thesis": "The funded BE->PLTR rotation into the confirmed 1x RS leader (Aug 3 earnings, no gate). PLTR -0.4% today lagging the chip tape = a cheaper entry, not a broken thesis. Gets LIVE out of cash and into the leader with a wide $122 stop. Approve anytime -> fills at market.",
}]

# ---- atomic write ----
fd, tmp = tempfile.mkstemp(dir=SITE, prefix=".engine-data.", suffix=".tmp")
with os.fdopen(fd, "w") as f:
    json.dump(data, f, indent=1, ensure_ascii=False)
os.replace(tmp, PATH)

# ---- verify read-back ----
with open(PATH) as f:
    chk = json.load(f)
assert chk["updated"] == TS
assert chk["accountability"]["date"] == "2026-07-21" and chk["accountability"]["final"] is False
assert chk["accountability"]["grade"].startswith("C")
assert chk["pending_tickets"][0]["id"] == "2026-07-20-3"
assert chk["pulse"][0]["ts"] == TS
assert chk["score"]["alphaPts"] == "-13.9"
assert abs(chk["paper"]["equity"] - 89181.76) < 1
ranks = sorted(c["projection"]["pop_rank"] for c in chk["coverage"])
assert ranks == list(range(1, 16)), ranks
top = [c["ticker"] for c in chk["coverage"] if c["projection"]["pop_rank"] == 1]
print("VERIFY OK. pop_rank1:", top, "| coverage:", len(chk["coverage"]),
      "| pulse:", len(chk["pulse"]), "| feed:", len(chk["feed"]),
      "| grade:", chk["accountability"]["grade"])
print("backup at:", os.path.basename(bak))
