#!/usr/bin/env python3
# Surgical publish for engine-data.json — 2026-07-22 ~3:19p ET near-close run.
# Atomic write (temp -> os.replace) + read-back verify, per OPS-ALERT rules.
import json, os, tempfile
from datetime import datetime
from zoneinfo import ZoneInfo

P = os.path.join(os.path.dirname(os.path.abspath(__file__)), "engine-data.json")
now = datetime.now(ZoneInfo("America/New_York"))
TS = now.strftime("%Y-%m-%dT%H:%M:00-04:00")
HHMM = now.strftime("%-I:%M%p").lower().replace("pm","p").replace("am","a")

with open(P) as f:
    d = json.load(f)

# ---------- pulse (prepend, keep ~15) ----------
pulse_text = (
    f"{HHMM} - Fresh near-close pull, HOLDING both books into tonight's GOOGL/TSLA AI-capex "
    "referendum (both report right after the 4pm close; TSLA ~7.6% implied, the first real test of "
    "AI-capex at scale). Confirmed the read: we own the day's leaders - CEG +4.9% (fresh ATHs), "
    "NVDA +3.1%, AMD +2.2% - all GTC-stopped, zero naked; PLTR -6.6% and SOFI -3.5% correctly "
    "dodged. SMCI +26% (record AI backlog, margins guided 15-17%) is a bullish read-through for our "
    "held AMD/NVDA but an un-chaseable earnings gap. ~21% ($19.1k) paper powder stays DRY - not "
    "gambling into the coin-flip. Honest: capture is light (~8% of CEG; paper +0.39%, live flat) - "
    "the diversified book + flat OKLO/SMR -2% dilute it, and the +3% NVDA anchor outweighs the "
    "+4.9% CEG mover. Live OKLO swing rides its own DOE catalyst (summit detail still pending); "
    "holding it overnight (not a day-trade), 0/3 same-day day-trades used. Next auto-action: after "
    "tonight's print, pour the powder into the CONFIRMED direction at the 7/23 open - do NOT "
    "pre-position tonight."
)
pulse_hype = (
    "Holding our green leaders into tonight's Google/Tesla prints - the big AI-capex test - with a "
    "fifth of the paper account in cash ready to pounce on the confirmed move. Not chasing SMCI's "
    "+26% gap into a coin-flip."
)
d["pulse"] = [{"ts": TS, "text": pulse_text, "hype": pulse_hype}] + d.get("pulse", [])
d["pulse"] = d["pulse"][:15]

# ---------- feed (prepend activity, keep ~40) ----------
feed_item = {
    "type": "activity",
    "ts": TS,
    "reaction": "hold",
    "text": (
        f"{HHMM} - HOLD into the bell: both books GTC-stopped/zero naked into tonight's GOOGL/TSLA "
        "AI-capex binary. Own the day's leaders (CEG +4.9% ATHs, NVDA +3.1%, AMD +2.2%); dodged "
        "PLTR -6.6% / SOFI -3.5%. ~21% ($19.1k) paper powder dry for the confirmed post-print "
        "deploy. Live OKLO swing held on its DOE catalyst, 0/3 live day-trades used."
    ),
}
d["feed"] = [feed_item] + d.get("feed", [])
d["feed"] = d["feed"][:40]

# ---------- status (Morning kept, Afternoon refreshed) ----------
d["status"] = [
    {"session": "Morning", "text": "Rotated laggard into RKLB mover"},
    {"session": "Afternoon", "text": "Green leaders held, powder dry"},
]

# ---------- headlines ----------
d["headlines"] = [
    "Alphabet + Tesla report tonight after the close - the first real test of AI-capex at scale (TSLA ~7.6% implied); tape de-risked in (QQQ -0.2%, oil +2% to $88)",
    "CEG at fresh all-time highs (~$275, +4.9%) - the nuclear-for-AI power bid stays firm, binary-insulated",
    "Super Micro +26% on a record AI-server backlog + margins guided 15-17% - bullish read-through for held AMD/NVDA + DELL",
    "NVDA +3.1%, AMD +2.2% lead the AI-semis into the Mag-7 print - we own both, GTC-stopped",
    "OKLO's morning +7.5% pop round-tripped to flat - the 7/21 nuclear headline sold off; DOE $200M summit detail still pending",
    "PLTR -6.6% the worst watchlist name (extended, rolling over) + SOFI -3.5% - both correctly dodged",
    "Oil +2% to $88 on the 11th night of Iran strikes - the macro risk overhang into earnings",
    "Intel also reports this week - more AI-capex / PC read-through on deck",
]

# ---------- coverage: refresh chg_pct + projection (+ thesis/hold_reason for held) ----------
cov_updates = {
    "CEG": {
        "chg_pct": "+4.9%",
        "size_note": "held; stop $263 (gain locked green)",
        "projection": {"target_pct": 5.0, "confidence": "high", "basis": "new-highs RS leader; nuclear-for-AI bid firm, binary-insulated", "pop_rank": 1},
        "thesis": "**pop_rank 1 - the day's strongest insulated RS leader.** Fresh all-time highs ~$275 (+4.9%), stop trailed to $263 = gain locked green. Nuclear-for-AI power utility with NO earnings tonight, so it is clean of the GOOGL/TSLA capex binary while a strong cloud-capex print only adds fuel. Above the breakout - we trail, not trim; a confirmed-strong print concentrates the deploy HERE, not the NVDA anchor.",
        "hold_reason": "Constellation is the nuclear utility powering the AI data-center boom - the cleanest 'AI needs power' play without chip-cycle risk. Long 16 sh from $260.68, at fresh highs today (+4.9%), the strongest name on our board, stop $263 locks the gain green. No earnings tonight means it rides the AI-power theme regardless of how Google or Tesla print - we hold, keep trailing, and add here on a confirmed-strong print.",
    },
    "NVDA": {
        "chg_pct": "+3.1%",
        "size_note": "held; stop $203",
        "projection": {"target_pct": 3.2, "confidence": "med", "basis": "most AI-capex-levered held name into tonight's GOOGL/TSLA print", "pop_rank": 2},
        "thesis": "**pop_rank 2 - the most AI-capex-levered name we own into the print.** +3.1% to ~$213.6, reclaimed the 20-day, stop $203. GOOGL cloud-capex + TSLA are tonight's direct read-through to NVDA demand, and SMCI's record backlog today is a bullish tell. The +3% 'anchor' - we hold through the binary, but the confirmed-add goes to CEG the mover, not here.",
        "hold_reason": "NVDA is the core AI-compute holding - 90 sh from $208.15, +3.1% today, stop $203. It is the single most sensitive name to tonight's GOOGL/TSLA capex signal, so we hold it through the print as our main directional AI-capex exposure. Watching the $203 stop and the print reaction; a weak capex read is the one thing that would trim it.",
    },
    "AMD": {
        "chg_pct": "+2.2%",
        "size_note": "held; stop $525 (green)",
        "projection": {"target_pct": 2.5, "confidence": "med", "basis": "SMCI record-backlog read-through; AI-GPU demand; held", "pop_rank": 3},
        "thesis": "**pop_rank 3 - SMCI read-through leader.** +2.2% to ~$556, stop $525, well above the breakout. Super Micro's record AI-server backlog + 15-17% margin guide is a direct bullish tell for AMD's data-center GPU/server demand, and it rides the same capex signal tonight. Hold through the print; stop locks a green gain.",
        "hold_reason": "AMD is our second AI-compute leg - 30 sh from $527.80, +5.5% since entry, stop $525 (green). Today's SMCI blowout backlog is a read-through to AMD's data-center demand. We hold and trail; a broken $525 or a weak capex print is the sell tell.",
    },
    "OKLO": {
        "chg_pct": "+0.6%",
        "size_note": "LIVE 16 sh (stop $39) + paper 300 sh (stop $43)",
        "projection": {"target_pct": 0.5, "confidence": "med", "basis": "round-tripped AM pop; DOE detail pending; held swing", "pop_rank": 5},
        "thesis": "**The LIVE real-money swing on its own DOE catalyst.** Round-tripped the AM +7.5% pop (47.48 high) back to ~$44.4/flat as the 7/21 nuclear headline sold off, but holds the $40-41 base well above the $39 live / $43 paper stop. DOE $200M summit detail still pending = the catalyst that made us buy. Hold overnight (not a PDT day-trade); binary-insulated.",
        "hold_reason": "OKLO is the live account's real-money swing - 16 sh from $44.43, filled today on the Trump/DOE $200M program to fast-track nuclear for AI data centers (MSFT/NVDA partners). It gave back its morning pop but the actual summit detail hasn't dropped yet, so the thesis is intact and it sits above its $39 stop. We hold it overnight as a swing (not a day-trade, preserving PDT budget) and let the catalyst work; a break of the base or a dead catalyst is the exit.",
    },
    "RKLB": {
        "chg_pct": "+0.8%",
        "size_note": "held; stop $65.5",
        "projection": {"target_pct": 1.0, "confidence": "low", "basis": "space momentum; top-ticked entry, holding above stop", "pop_rank": 7},
        "thesis": "**Space/defense momentum - but we top-ticked the entry.** +0.8% to ~$69.7 today; the position is -3.9% from a $72.68 AM entry near the HOD (the execution ding). Holds above the $65.5 stop. Right name, chased fill - we hold for the thesis, no add until a clean base.",
        "hold_reason": "Rocket Lab is our space/defense growth leg - 123 sh, but we bought near today's high tick ($72.68) and it faded, so the position is red though the stock is green on the day. Stop $65.5 caps it. We hold on the intact launch-cadence / Neutron thesis but this is the first name to reassess if it breaks the base - the lesson is to add on pullbacks, not chase the HOD.",
    },
    "SMR": {
        "chg_pct": "-2.0%",
        "size_note": "held; stop $7.50 (the #1 funding source)",
        "projection": {"target_pct": -2.0, "confidence": "low", "basis": "nuclear laggard at the low; first cut if the print is weak", "pop_rank": 13},
        "thesis": "**The theme LAGGARD - first cut if the print is weak.** -2.0% to ~$8.53 (day low) while its nuclear-for-AI peers CEG (+4.9%) and OKLO ran - relative weakness. Holds above the $7.50 stop. Small-cap SMR rips WITH a strong AI-power read tonight, so we hold the capped-downside optionality into the print rather than sell at the low; but it is the #1 funding source for a confirmed leader.",
        "hold_reason": "NuScale/SMR is our small-cap nuclear leg - 1050 sh, -2% today and the weakest name on the board while its theme-mates lead. It is stopped at $7.50 so downside is capped, and a strong AI-power print tonight would lift the whole nuclear complex including SMR - so we hold the asymmetry into the catalyst rather than dump it at the low. If the print is weak, this is the first position we cut to fund the confirmed leader.",
    },
    "SMCI": {
        "chg_pct": "+20.2%",
        "projection": {"target_pct": 20.0, "confidence": "low", "basis": "record AI backlog earnings gap - un-chaseable", "pop_rank": 4},
        "thesis": "**+26% blockbuster - but an un-chaseable earnings gap.** Record AI-server backlog + margins guided to 15-17% sent it gapping (fading from the +26% HOD to ~+20%). We do NOT chase a pre/post-announcement gap into tonight's binary - the top-tick trap. Instead we read it as a strong bullish tell for our held AMD/NVDA (+ DELL confirming).",
    },
    "SOXL": {
        "chg_pct": "+3.2%",
        "projection": {"target_pct": 3.0, "confidence": "low", "basis": "3x semis; tracks the print reaction, gated by QQQ<20-day", "pop_rank": 6},
        "thesis": "**3x-semis proxy - watched, not held (regime-gated).** +3.2% tracking the AI-semi bid, but QQQ is still fractionally under its 20-day, so the leverage gate keeps us OUT of 3x-index/semi longs until a clean reclaim. The confirmed post-print reclaim is the re-lever trigger, not tonight.",
    },
    "IONQ": {
        "chg_pct": "-1.7%",
        "projection": {"target_pct": -1.5, "confidence": "low", "basis": "quantum beta soft into a risk-off print", "pop_rank": 9},
    },
    "RGTI": {
        "chg_pct": "-0.7%",
        "projection": {"target_pct": -0.7, "confidence": "low", "basis": "quantum beta; range-bound, no catalyst", "pop_rank": 10},
    },
    "TSLA": {
        "chg_pct": "-1.3%",
        "projection": {"target_pct": -1.3, "confidence": "low", "basis": "reports tonight ~7.6% implied; margins the swing", "pop_rank": 12},
        "thesis": "**Reports tonight - the binary itself.** -1.3% into the print (~7.6% options-implied move). Record 480k Q2 deliveries but the swing is automotive gross margin + the robotaxi/robot narrative. We do NOT hold it into its own coin-flip - watch the reaction as the AI-capex/consumer read-through for the rest of the board.",
    },
    "VRT": {
        "chg_pct": "-0.6%",
        "projection": {"target_pct": -0.5, "confidence": "low", "basis": "AI-power infra; SMCI tailwind vs risk-off tape", "pop_rank": 8},
    },
    "BE": {
        "chg_pct": "-1.6%",
        "projection": {"target_pct": -1.5, "confidence": "low", "basis": "faded a +5% intraday pop; fuel-cell, not held", "pop_rank": 11},
        "thesis": "**Faded its intraday pop - watched, not held.** Ran to $229.7 (+1.5%) then gave it back to -1.6% (~$223). The Oaktree $1.7B fuel-cell/data-center catalyst is real but the tape sold the rip; no clean base to enter. Watch for a reclaim of $226 on a strong print - not chasing.",
    },
    "PLTR": {
        "chg_pct": "-6.6%",
        "projection": {"target_pct": -6.5, "confidence": "med", "basis": "extended, rolling over; correctly avoided (worst watchlist name)", "pop_rank": 15},
        "thesis": "**The worst watchlist name today (-6.6%) - correctly avoided.** Extended and rolling over hard from ~$132 to ~$124, back below the breakout. No position; the AVOID paid. Re-engage only on a base rebuild, not a falling knife.",
    },
    "SOFI": {
        "chg_pct": "-3.5%",
        "projection": {"target_pct": -3.5, "confidence": "low", "basis": "fintech risk-off; correctly avoided", "pop_rank": 14},
    },
}

for c in d.get("coverage", []):
    t = c.get("ticker")
    if t in cov_updates:
        for k, v in cov_updates[t].items():
            c[k] = v
        c["updated"] = TS

# ---------- accountability (running, not final) ----------
d["accountability"] = {
    "date": "2026-07-22",
    "final": False,
    "grade": "C+ (running, ~40m to close)",
    "headline": (
        "Green and owning the day's leaders (CEG +4.9% ATHs, NVDA +3.1%, AMD +2.2%, all GTC-stopped) "
        "with ~21% ($19.1k) paper powder DRY into tonight's GOOGL/TSLA AI-capex referendum - not "
        "gambled into the coin-flip. LIVE is finally working (OKLO swing on its own DOE catalyst, "
        "ending the 7-session cash camp). Honest debit: capture is light (~8% of CEG; paper +0.39%, "
        "live flat) - the diversified book + flat OKLO / SMR -2% dilute it, and the +3% NVDA anchor "
        "outweighs the +4.9% CEG mover; the +26% SMCI print was an un-chaseable earnings gap we "
        "correctly did not chase into the binary."
    ),
    "capture": {
        "bestName": "CEG +4.9% (HELD, fresh ATHs)",
        "bestPct": "+4.9%",
        "capturedPct": "paper +0.39% / live -0.07%",
        "rate": "~8% of the best held leader (CEG); excludes the un-chaseable +26% SMCI earnings gap",
    },
    "missed": [
        {
            "from": "NVDA anchor (+3.1%, 21% of book)",
            "to": "CEG the mover (+4.9%, only 4.8% of book)",
            "note": "weight sat on the +3% anchor while the +4.9% RS leader stayed under-sized - the recurring 'weight to the mover, not the anchor' drag",
            "delta": "~-$40 est",
        },
        {
            "from": "RKLB top-tick entry ($72.68)",
            "to": "RKLB on a VWAP pullback",
            "note": "bought near the AM HOD; position -3.9% though the stock is +0.8% - right name, chased entry",
            "delta": "~-$348 unrealized",
        },
    ],
    "saved": [
        {"note": "Kept ~21% ($19.1k) paper powder DRY rather than pre-positioning into tonight's GOOGL/TSLA coin-flip with oil +2% on the Iran overhang", "delta": "coin-flip dodged"},
        {"note": "Did NOT chase SMCI's +26% earnings gap into the binary - read it as a bullish tell for held AMD/NVDA instead", "delta": "top-tick dodged"},
        {"note": "Broke the 7-session LIVE cash camp - OKLO one-tap filled at the $44.43 base on a live DOE catalyst; holding it overnight (not a day-trade), 0/3 PDT budget used", "delta": "camp broken"},
    ],
    "avoided": {
        "worstName": "PLTR",
        "worstPct": "-6.6%",
        "note": "PLTR the worst watchlist name (-6.6%, extended, rolling over) + SOFI -3.5%; hold neither, dodged both",
        "amount": "none held",
        "rate": "100% dodged",
    },
    "best": {"name": "CEG", "note": "nuclear-for-AI RS leader at fresh ATHs, held not watched; stop $263 locks the gain green + binary-insulated", "delta": "+4.9%"},
    "worst": {"name": "RKLB", "note": "bought the mover near the top tick this AM - right name, entry too high (position -3.9% though stock +0.8%)", "delta": "-$348 unrealized"},
    "applying": "7/22 - weight to the insulated MOVER (CEG) not the +3% anchor + don't pre-position the powder into tonight's coin-flip; broke the live cash camp (OKLO), holding it as a swing, not a day-trade.",
    "adjust": (
        "AFTER tonight's GOOGL/TSLA print, deploy the 21% paper powder into the CONFIRMED direction at "
        "the 7/23 open - strong AI-capex (cloud capex raised, hyperscaler spend intact) -> concentrate "
        "into the insulated RS leader CEG (weight the MOVER, not the +3% NVDA anchor) + OKLO; weak / "
        "capex-cut -> cut SMR (the -2% laggard) first, stay light, consider a small inverse. Do NOT "
        "pre-position tonight. LIVE: OKLO is the swing on its DOE catalyst - hold overnight, do NOT "
        "day-trade it (preserve 0/3 PDT budget); post-print, the freed $99 + any SMR-rotation funds the "
        "confirmed leader via a clean at-the-open ticket. Pre-stage the plan so the post-close run "
        "deploys FAST (the 'execute at the open, not at 3pm' rule)."
    ),
}

# ---------- score (recompute alpha vs buy-and-hold TQQQ) ----------
# live 809.75 / 1000 inception = -19.03%; TQQQ 7/2 close 73.35 -> 70.805 today = -3.47%; alpha -15.6
d["score"] = {
    "alphaPts": "-15.6",
    "benchmark": "-3.5%",
    "bestDay": "+3.2%",
    "bestDayName": "Jul 14 - CPI chip rally (settled)",
    "winRate": "33%",
    "tradeCount": 7,
}

# ---------- pending_tickets: none (no live ticket into the coin-flip) ----------
d["pending_tickets"] = []

# ---------- equity curves: update today's point ----------
def upsert(curve, label, value):
    for pt in curve:
        if pt.get("date") == label:
            pt["value"] = value
            return
    curve.append({"date": label, "value": value})

if isinstance(d.get("live"), dict) and isinstance(d["live"].get("equity_curve"), list):
    upsert(d["live"]["equity_curve"], "Jul 22", 809.75)
if isinstance(d.get("paper"), dict) and isinstance(d["paper"].get("equity_curve"), list):
    upsert(d["paper"]["equity_curve"], "Jul 22", 90325.71)

d["updated"] = TS

# ---------- atomic write ----------
dir_ = os.path.dirname(P)
fd, tmp = tempfile.mkstemp(dir=dir_, prefix=".engine-data.", suffix=".tmp")
with os.fdopen(fd, "w") as f:
    json.dump(d, f, ensure_ascii=False, indent=1)
os.replace(tmp, P)

# ---------- read-back verify ----------
with open(P) as f:
    chk = json.load(f)
assert chk["updated"] == TS, "updated mismatch"
assert chk["accountability"]["final"] is False
assert chk["accountability"]["date"] == "2026-07-22"
assert chk["pending_tickets"] == []
pr1 = [c["ticker"] for c in chk["coverage"] if c.get("projection", {}).get("pop_rank") == 1]
assert pr1 == ["CEG"], f"pop_rank1 = {pr1}"
print("OK", TS, "| pulse", len(chk["pulse"]), "| feed", len(chk["feed"]),
      "| coverage", len(chk["coverage"]), "| pop_rank1", pr1,
      "| grade", chk["accountability"]["grade"])
