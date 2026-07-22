#!/usr/bin/env python3
"""Post-close FINAL publish for 2026-07-22 ~4:20pm ET. Atomic write + backup + verify."""
import json, os, shutil, sys

SITE = os.path.dirname(os.path.abspath(__file__))
PATH = os.path.join(SITE, "engine-data.json")
TS = "2026-07-22T16:20:00-04:00"

with open(PATH) as f:
    d = json.load(f)

# ---- status (Morning -> Afternoon -> Evening) ----
d["status"] = [
    {"session": "Morning", "text": "Rotated laggard into RKLB mover"},
    {"session": "Afternoon", "text": "Leaders held, powder dry for print"},
    {"session": "Evening", "text": "GOOGL beat AH — deploy at open"},
]

# ---- headlines ----
d["headlines"] = [
    "GOOGL popped ~+2.5% after-hours on a Google Cloud + AI-capex beat (capex guide kept high) — a bullish read-through for our AI-power/infra book; deploy the powder into it at the 7/23 open",
    "TSLA fell ~3% after-hours on soft margins despite record 480k deliveries — its own story, not an AI-capex signal (we hold none)",
    "CEG closed +4.8% at fresh all-time highs — our held RS leader and pop_rank 1; nuclear-for-AI power bid, binary-insulated",
    "OKLO's DOE nuclear-for-AI catalyst confirmed live (joined the federal program alongside Microsoft/Nvidia) — our LIVE swing, held overnight above the $39 stop",
    "SMCI +19.9% on record AI-server backlog — the day's biggest watchlist mover but an un-chaseable earnings gap; a bullish tell for held AMD/NVDA",
    "PLTR -6.1% + SOFI -3.2% + BE -3.6% the worst watchlist names — all correctly dodged",
    "Regime still soft: QQQ $705 = ~1.3% under its $714 20-day → 3x gated; SPY $747 flat near a record",
    "Live broke a 7-session cash camp — OKLO one-tap filled at the $44.43 base; 0/3 PDT budget intact",
]

# ---- coverage updates keyed by ticker ----
cov = {
 "CEG": {"chg_pct": "+4.8%", "verdict": "buy", "verdict_label": "Buy - held RS leader",
   "thesis": "**pop_rank 1 - the insulated RS leader, and now with a capex tailwind.** Closed +4.8% at fresh all-time highs (~$275), held 16 sh from $260.68, stop $263 = gain locked green. Tonight's GOOGL cloud/capex beat (AI-capex intact) is pure fuel for a nuclear-for-AI power utility with NO earnings binary of its own. Above the breakout - we trail, not trim, and the 7/23 open deploy concentrates HERE + OKLO, weighting the mover not the +2.3% NVDA anchor.",
   "hold_reason": "Constellation is the nuclear utility powering the AI data-center boom - the cleanest 'AI needs power' play without chip-cycle risk. Long 16 sh from $260.68, at fresh highs today (+4.8%), the strongest name on our board, stop $263 locks the gain green. GOOGL's post-close capex beat only adds fuel; we hold, keep trailing, and add here at the 7/23 open on the confirmed-bullish print.",
   "size_note": "held; stop $263 (gain locked green)", "chg_note": "",
   "projection": {"target_pct": 3.8, "confidence": "high", "basis": "RS leader ATHs + GOOGL capex tailwind, binary-insulated", "pop_rank": 1}},
 "OKLO": {"chg_pct": "+0.8%", "verdict": "buy", "verdict_label": "Buy - LIVE filled + paper held",
   "thesis": "**pop_rank 2 - the LIVE real-money swing on its own DOE catalyst + a capex tailwind.** Closed +0.8% (~$44.5), round-tripped the AM +7.5% pop but holds the $40-41 base well above the $39 live / $43 paper stop. Catalyst confirmed live (Bloomberg 7/21, Benzinga 7/22: joined the federal nuclear-for-AI program with Microsoft/Nvidia). GOOGL's capex beat lifts the whole data-center-power complex. Higher-beta than CEG = a bigger pop candidate on a bullish open; held overnight (not a PDT day-trade).",
   "hold_reason": "OKLO is the live account's real-money swing - 16 sh from $44.43, filled today on the DOE program to fast-track nuclear for AI data centers. It gave back its morning pop but the federal-program catalyst is confirmed and developing, and it sits well above its $39 stop. We hold it overnight as a swing (preserving 0/3 PDT) and let the catalyst + the AI-capex tailwind work; a break of the base or a dead catalyst is the exit.",
   "size_note": "LIVE 16 sh (stop $39) + paper 300 sh (stop $43)", "chg_note": "",
   "projection": {"target_pct": 5.0, "confidence": "med", "basis": "own DOE catalyst + AI-power capex tailwind; high-beta", "pop_rank": 2}},
 "NVDA": {"chg_pct": "+2.3%", "verdict": "buy", "verdict_label": "Buy - held",
   "thesis": "**pop_rank 3 - the most AI-capex-levered name we own, and GOOGL just validated the capex.** Closed +2.3% (~$212), reclaimed the 20-day, stop $203. GOOGL's cloud/capex beat = a direct read-through to NVDA GPU demand, and SMCI's record backlog is a second bullish tell. The +2.3% 'anchor' - we hold it, but the 7/23 add goes to the CEG/OKLO movers, NOT more anchor weight (the repeat 'weight the mover' fix).",
   "hold_reason": "NVDA is the core AI-compute holding - 90 sh from $208.15, +2.3% today, stop $203. Tonight's GOOGL capex beat reads straight through to NVDA demand, so we hold it as our main AI-capex exposure. Watching the $203 stop; the mistake to avoid is letting this 21%-of-book anchor stay heavier than the CEG/OKLO movers - tomorrow's fresh cash goes to them.",
   "size_note": "held; stop $203", "chg_note": "",
   "projection": {"target_pct": 2.5, "confidence": "med", "basis": "GOOGL capex beat = direct GPU-demand read-through", "pop_rank": 3}},
 "AMD": {"chg_pct": "+1.4%", "verdict": "buy", "verdict_label": "Buy - held",
   "thesis": "**pop_rank 4 - the SMCI + GOOGL-capex read-through leg.** Closed +1.4% (~$552), stop $525, well above the breakout (green gain locked). Super Micro's record AI-server backlog + tonight's GOOGL capex beat both read straight through to AMD's data-center GPU/server demand. Hold and trail; a broken $525 or a capex disappointment on the calls is the sell tell.",
   "hold_reason": "AMD is our second AI-compute leg - 30 sh from $527.80, +4.7% since entry, stop $525 (green). SMCI's blowout backlog + GOOGL's capex beat are both read-throughs to AMD demand. We hold and trail; a broken $525 is the sell.",
   "size_note": "held; stop $525 (green)", "chg_note": "",
   "projection": {"target_pct": 2.2, "confidence": "med", "basis": "AI-GPU capex read-through + SMCI backlog", "pop_rank": 4}},
 "VRT": {"chg_pct": "-1.1%", "verdict": "watch", "verdict_label": "Watch - re-entry candidate",
   "thesis": "**A direct GOOGL-capex beneficiary we sold too early.** Closed -1.1% (~$301); we sold 30 sh at ~$299.5 this AM to fund the RKLB mover. AI-power/cooling for data centers is exactly what GOOGL's raised capex funds, so this is a prime re-entry candidate at the 7/23 open on a confirmed-bullish print - watch for a clean base reclaim, don't chase.",
   "hold_reason": "", "size_note": "sold AM to fund RKLB; top re-entry candidate on the capex print", "chg_note": "",
   "projection": {"target_pct": 2.8, "confidence": "med", "basis": "AI data-center power/cooling; direct GOOGL-capex beneficiary", "pop_rank": 5}},
 "SOXL": {"chg_pct": "+1.7%", "verdict": "avoid", "verdict_label": "Avoid - 3x gated",
   "thesis": "**3x-semis proxy - watched, not held (regime-gated).** Closed +1.7% tracking the AI-semi bid. QQQ is still ~1.3% under its 20-day ($705 vs $714), so the leverage gate keeps us OUT of 3x until a clean reclaim. A confirmed post-print reclaim of the 20-day on volume is the re-lever trigger - not yet.",
   "hold_reason": "", "size_note": "gated - QQQ under its 20-day", "chg_note": "",
   "projection": {"target_pct": 2.5, "confidence": "low", "basis": "3x semis track the capex bid; gated by QQQ<20-day", "pop_rank": 6}},
 "RKLB": {"chg_pct": "+0.8%", "verdict": "buy", "verdict_label": "Buy - held (entry chased)",
   "thesis": "**Space/defense momentum - but we top-ticked the entry (today's ding).** Closed +0.8% (~$69.7); the position is -4% from a $72.68 AM entry near the HOD. Holds above the $65.5 stop. Right name, chased fill - we hold for the launch-cadence/Neutron thesis but take NO add until a clean base; the lesson is buy the pullback, not the high tick.",
   "hold_reason": "Rocket Lab is our space/defense growth leg - 123 sh, but we bought near today's high tick and it faded, so the position is red though the stock is green on the day. Stop $65.5 caps it. We hold on the intact thesis but this is the first name to reassess if it breaks the base - the durable lesson is to add on pullbacks, not chase the HOD.",
   "size_note": "held; stop $65.5", "chg_note": "",
   "projection": {"target_pct": 1.2, "confidence": "low", "basis": "space momentum; holds above stop, no add until a base", "pop_rank": 7}},
 "SMR": {"chg_pct": "-0.3%", "verdict": "hold", "verdict_label": "Hold - theme laggard",
   "thesis": "**The theme LAGGARD - the first cut if tomorrow fades.** Closed ~flat (-0.3%, ~$8.68) while its nuclear-for-AI peers CEG (+4.8%) and OKLO ran - relative weakness. Holds above the $7.50 stop. A small-cap that rips WITH a strong AI-power tape, so a bullish GOOGL-capex open lifts it - but it is the #1 funding source if the print fades and we need to concentrate the leaders.",
   "hold_reason": "NuScale/SMR is our small-cap nuclear leg - 1050 sh, ~flat today and the weakest name on the board while its theme-mates lead. Stopped at $7.50 so downside is capped. A strong AI-power tape (tonight's GOOGL capex beat) lifts the whole complex including SMR, so we hold the asymmetry - but if the 7/23 open fades, this is the first position we cut to fund a confirmed leader.",
   "size_note": "held; stop $7.50 (the #1 funding source)", "chg_note": "",
   "projection": {"target_pct": 1.8, "confidence": "low", "basis": "small-cap nuclear lifts on the AI-power tailwind", "pop_rank": 8}},
 "IONQ": {"chg_pct": "-2.3%", "verdict": "watch", "verdict_label": "Watch - quiet",
   "thesis": "**Soft (-2.3%)**, no fresh catalyst - quantum names lagged the risk-off-into-the-print tape. Lifts if the tape holds risk-on after tonight's bullish read; nothing to do here without a volume move.",
   "hold_reason": "", "size_note": "no setup", "chg_note": "",
   "projection": {"target_pct": 1.0, "confidence": "low", "basis": "quantum beta; lifts if the tape holds risk-on", "pop_rank": 9}},
 "RGTI": {"chg_pct": "-0.3%", "verdict": "watch", "verdict_label": "Watch - drift",
   "thesis": "**-0.3%, low-conviction drift** - quantum, no catalyst. On the board for a volatility move only; not a trade.",
   "hold_reason": "", "size_note": "no setup", "chg_note": "",
   "projection": {"target_pct": 0.5, "confidence": "low", "basis": "quantum drift, no catalyst", "pop_rank": 10}},
 "BE": {"chg_pct": "-3.6%", "verdict": "watch", "verdict_label": "Watch - oversold bounce candidate",
   "thesis": "**Faded hard (-3.6% to ~$218) - watched, not held.** Gave back its Oaktree $1.7B fuel-cell/data-center pop. The catalyst is real and GOOGL's capex beat is a tailwind for AI-power infra, so it's an oversold-bounce candidate - watch for a reclaim of ~$226 on the print, not chasing the knife.",
   "hold_reason": "", "size_note": "no setup; watch a $226 reclaim", "chg_note": "",
   "projection": {"target_pct": 1.5, "confidence": "low", "basis": "fuel-cell/AI-power; oversold bounce on the capex tailwind", "pop_rank": 11}},
 "SMCI": {"chg_pct": "+19.9%", "verdict": "watch", "verdict_label": "Watch - already popped",
   "thesis": "**+19.9% blockbuster - the day's biggest watchlist mover but an un-chaseable earnings gap.** Record AI-server backlog + margins guided to 15-17% sent it gapping. We correctly did NOT chase a post-announcement gap into the binary (the top-tick trap) - we read it as a strong bullish tell for our held AMD/NVDA. Give-back risk now that the pop is spent.",
   "hold_reason": "", "size_note": "don't chase a +20% earnings gap", "chg_note": "",
   "projection": {"target_pct": -2.5, "confidence": "low", "basis": "earnings-gap digestion; give-back risk after +20%", "pop_rank": 12}},
 "SOFI": {"chg_pct": "-3.2%", "verdict": "avoid", "verdict_label": "Avoid - fading",
   "thesis": "**-3.2%**, no catalyst, fading with the risk-off fintech tape. We de-camped this name weeks ago; nothing to own here - dodged alongside PLTR.",
   "hold_reason": "", "size_note": "avoid; no catalyst", "chg_note": "",
   "projection": {"target_pct": -0.5, "confidence": "low", "basis": "no catalyst; fading with fintech", "pop_rank": 13}},
 "TSLA": {"chg_pct": "-1.3%", "verdict": "watch", "verdict_label": "Watch - fell on the print",
   "thesis": "**Reported tonight and FELL ~3% after-hours.** Closed -1.3% into the print, then dropped to ~$362 AH on soft margins despite a record 480k Q2 deliveries - the automotive-margin story, not an AI-capex read-through. We held none into its coin-flip; its drag is idiosyncratic and does NOT change the bullish GOOGL-capex read for our book.",
   "hold_reason": "", "size_note": "fell on the print - own-story drag, not held", "chg_note": "",
   "projection": {"target_pct": -2.5, "confidence": "med", "basis": "down ~3% AH on soft margins; own-story drag", "pop_rank": 14}},
 "PLTR": {"chg_pct": "-6.1%", "verdict": "avoid", "verdict_label": "Avoid - rolling over",
   "thesis": "**The worst watchlist name today (-6.1%) - correctly avoided.** Rolled over hard from ~$132 to ~$124, back below the breakout. No position; the AVOID paid again. Re-engage only on a base rebuild, not a falling knife.",
   "hold_reason": "", "size_note": "avoid; rolling over", "chg_note": "",
   "projection": {"target_pct": -1.0, "confidence": "low", "basis": "rolling over below breakout; avoid", "pop_rank": 15}},
}

for entry in d["coverage"]:
    t = entry.get("ticker")
    if t in cov:
        u = cov[t]
        for k, v in u.items():
            if k == "chg_note":
                continue
            entry[k] = v
        entry["updated"] = TS

# ---- pulse (prepend one, keep ~15) ----
pulse_new = {
 "ts": TS,
 "text": "4:20p (post-close, FINAL) - Today's grade: C+. Green both books and we OWNED the day's best tradeable mover - CEG +4.8% at fresh highs (our pop_rank 1, held) - plus we broke the 7-session live cash camp (OKLO filled on its DOE catalyst, $39 stop, held overnight). Avoided every red name (PLTR -6.1%, SOFI -3.2%, BE -3.6%) and correctly skipped SMCI's +19.9% earnings gap. Honest debit: capture is light (~6% of CEG; paper +0.3%, live +0.2%) - I chased RKLB at the top tick this AM (-$369) and under-weighted the CEG mover vs the flat NVDA anchor, two mistakes already in my Playbook. THE PRINT broke our way: GOOGL +2.5% after-hours on a cloud/capex beat (AI-capex intact), TSLA -3% on its own margins, NVDA/AMD flat - so the binary is bullish for our AI-infra book. NEXT (7/23 open): deploy the 21% ($19.1k) paper powder into the confirmed direction - concentrate CEG + OKLO, weight the mover not the anchor; hold OKLO live. Execute at the open, not at 3pm.",
 "hype": "Solid-not-great day - C+. Owned our best mover (CEG at record highs) and finally got the real account off the sidelines into OKLO, but I chased Rocket Lab too high this morning - that's the ding. Google's earnings just popped it +2.5% after hours, good sign for our AI-power names, so tomorrow at the open I put the dry powder to work."
}
d["pulse"] = [pulse_new] + d.get("pulse", [])
d["pulse"] = d["pulse"][:15]

# ---- activity (prepend one) ----
act_new = {
 "ts": TS, "kind": "engine",
 "title": "Wed 7/22 ~4:20pm ET (post-close, FINAL). Grade C+. Reconciled clean vs the broker both ways: LIVE $811.85 (OKLO 16 sh @ $44.43 / $99 cash / $39 GTC stop verified / 0-3 PDT), PAPER $90,469 (+0.3% reg close, prov.), 6/6 GTC-stopped (AMD $525/CEG $263/NVDA $203/OKLO $43/RKLB $65.50/SMR $7.50), zero naked, ~21% ($19.1k) powder dry. Owned the day's best tradeable mover CEG +4.8% (pop_rank 1, HIT); avoided PLTR -6.1%/SOFI -3.2%/BE -3.6%; did NOT chase SMCI +19.9% earnings gap; broke the 7-session live cash camp (OKLO on its DOE catalyst). Debit: capture ~6% of CEG - chased RKLB top-tick (-$369) + under-weighted the mover vs the NVDA anchor. PRINT broke bullish: GOOGL +2.5% AH (cloud/capex beat), TSLA -3% AH (own margins), NVDA/AMD flat. Regime: QQQ $705 = -1.25% under its $714 20-day -> 3x gated. Score: live -18.8% since inception, alpha -14.6 vs TQQQ -4.2%. NEXT 7/23 open: deploy the powder into CEG + OKLO (weight the mover); hold OKLO live; execute at the open."
}
d["activity"] = [act_new] + d.get("activity", [])
d["activity"] = d["activity"][:40]

# ---- latest_recap ----
d["_latest_recap_prev"] = d.get("latest_recap", "")
d["latest_recap"] = ("4:20p 7/22 (post-close, FINAL grade C+). Reconciled CLEAN both ways vs the broker: "
 "LIVE $811.85 (OKLO 16 sh 88% / $99 cash / 0-3 day-trades, nothing naked), OKLO $39 GTC stop verified. "
 "PAPER $90,469 (+0.3% reg close, prov.; ~+0.5% on the AH mark as NVDA/AMD firmed), 6/6 GTC-stopped "
 "(AMD $525 / CEG $263 / NVDA $203 / OKLO $43 / RKLB $65.50 / SMR $7.50), zero naked, ~21% ($19.1k) cash DRY. "
 "CAPTURE light ~6% of the best held mover CEG +4.8% (our pop_rank 1 - a projection HIT, tracker 3-for-5); "
 "the biggest watchlist mover SMCI +19.9% was an un-chaseable earnings gap (correctly skipped, bullish tell for held AMD/NVDA). "
 "Debit: chased RKLB at the $72.68 top tick (-$369) + under-weighted the CEG mover vs the flat NVDA anchor (both repeat Playbook mistakes). "
 "Credit: broke the 7-session LIVE cash camp (OKLO on its DOE nuclear-for-AI catalyst, held overnight, 0/3 PDT preserved); avoided PLTR -6.1% / SOFI -3.2% / BE -3.6%. "
 "THE PRINT broke BULLISH for our book: GOOGL +2.5% AH (Google Cloud + AI-capex beat), TSLA -3% AH (soft margins, its own story), NVDA/AMD flat AH. "
 "REGIME: QQQ closed $705.35 = -1.25% under its $714.25 20-day -> 3x gated; SPY $747 flat near a record. "
 "SCORE (real): live -18.8% since $1,000 inception; benchmark TQQQ 7/2 $73.35 -> 7/22 $70.28 = -4.2%; alpha -14.6 pts. "
 "NEXT (7/23 OPEN): deploy the 21% paper powder into the CONFIRMED AI-infra direction - concentrate CEG (RS leader) + OKLO, WEIGHT THE MOVER not the +2.3% NVDA anchor; if the open fades the print, cut SMR first and stay light. "
 "LIVE: hold OKLO overnight; at the open, if a clearly stronger confirmed leader emerges send a live OKLO->leader rotation ticket, else HOLD ($99 cash only). "
 "Execute at the OPEN, not 3pm. Did NOT pre-position tonight. Published engine-data.json only (no data.json, no git). Backup engine-data.backup-2026-07-22-1620.json.")

# ---- accountability (FINAL) ----
d["accountability"] = {
 "date": "2026-07-22", "final": True, "grade": "C+",
 "headline": "Green both books and OWNED the day's best tradeable mover (CEG +4.8% fresh ATHs, held = pop_rank 1 HIT) + broke the 7-session LIVE cash camp (OKLO on its own DOE catalyst, $39 stop) + avoided every red name (PLTR -6.1%, SOFI -3.2%, BE -3.6%) + kept ~21% powder DRY into the GOOGL/TSLA binary that then broke BULLISH (GOOGL +2.5% AH). Honest debit: capture is light (~6% of CEG; paper +0.3%, live +0.2%) - two REPEAT Playbook mistakes diluted it: chased RKLB at the top tick (-$369) and under-weighted the CEG mover vs the flat NVDA anchor. The +19.9% SMCI print was an un-chaseable earnings gap, correctly not chased.",
 "capture": {
   "bestName": "CEG +4.8% (HELD, fresh ATHs) - best tradeable mover",
   "bestPct": "+4.8%",
   "capturedPct": "paper +0.3% / live +0.2% (prov.)",
   "rate": "~6% of the best held mover (CEG); the biggest watchlist mover SMCI +19.9% was an un-chaseable earnings gap, correctly skipped"
 },
 "missed": [
   {"from": "RKLB top-tick entry ($72.68)", "to": "RKLB on a VWAP pullback",
    "note": "chased the AM HOD; position -4% though the stock closed +0.8% - repeat 'don't chase the HOD' mistake", "delta": "-$369 unrealized"},
   {"from": "NVDA anchor (+2.3%, 21% of book)", "to": "CEG the mover (+4.8%, 4.8% of book)",
    "note": "weight sat on the flat anchor while the insulated RS leader stayed under-sized - 'weight the mover, not the anchor', 3 sessions running", "delta": "~-$35 est"}
 ],
 "saved": [
   {"note": "Broke the 7-session LIVE cash camp - OKLO one-tap filled at the $44.43 base on its own DOE nuclear-for-AI catalyst; held overnight (not a day-trade), 0/3 PDT preserved, $39 stop verified", "delta": "camp broken"},
   {"note": "Kept ~21% ($19.1k) paper powder DRY into the GOOGL/TSLA binary instead of gambling pre-print - the print broke bullish (GOOGL +2.5% AH), so tomorrow we deploy into confirmation", "delta": "coin-flip dodged"},
   {"note": "Did NOT chase SMCI's +19.9% earnings gap into the binary - read it as a bullish tell for held AMD/NVDA", "delta": "top-tick dodged"}
 ],
 "avoided": {
   "worstName": "PLTR", "worstPct": "-6.1%",
   "note": "PLTR the worst watchlist name (-6.1%, rolling over) + SOFI -3.2% + BE -3.6%; hold none, dodged all three",
   "amount": "none held", "rate": "100% dodged"
 },
 "best": {"name": "CEG", "note": "nuclear-for-AI RS leader at fresh ATHs, held not watched (pop_rank 1 HIT); stop $263 locks the gain, binary-insulated", "delta": "+4.8%"},
 "worst": {"name": "RKLB", "note": "chased the mover near the AM top tick - right name, entry too high (position -4% though the stock closed +0.8%)", "delta": "-$369 unrealized"},
 "applying": "7/22 - weight to the insulated MOVER (CEG) + broke the live cash camp (OKLO, held as a swing not a day-trade). Playbook: execute rotations, don't chase the HOD (broke this on RKLB - re-committing).",
 "adjust": "7/23: the GOOGL/TSLA print broke BULLISH for AI-capex (GOOGL +2.5% AH on a cloud/capex beat; TSLA -3% is its own margin story, not a read-through; NVDA/AMD flat). At the 7/23 OPEN, deploy the 21% ($19.1k) paper powder into the CONFIRMED AI-infra direction - concentrate into CEG (RS leader) + OKLO, WEIGHT THE MOVER not the +2.3% NVDA anchor; if the open fades the print, cut SMR (the laggard) first and stay light. LIVE: hold OKLO overnight; at the open, if a clearly stronger confirmed leader emerges send a live OKLO->leader rotation ticket, else HOLD (only $99 cash; OKLO already expresses the theme + its own catalyst). Execute at the OPEN, not 3pm. And STOP the two repeats: no HOD chases, size the mover >= the anchor."
}

# ---- score ----
d["score"] = {"alphaPts": "-14.6", "benchmark": "-4.2%", "bestDay": "+3.2%",
              "bestDayName": "Jul 14 - CPI chip rally (settled)", "winRate": "33%", "tradeCount": 7}

# ---- pending_tickets (none tonight) ----
d["pending_tickets"] = []

# ---- live block ----
d["live"]["equity"] = 811.85
d["live"]["cash"] = 99.43
d["live"]["positions"] = [
  {"symbol": "OKLO", "qty": 16, "avg_price": 44.43, "price": 44.53, "value": 712.42,
   "stop": 39, "unrealized_pl": 1.54, "unrealized_pct": 0.22}
]
d["live"]["updated"] = TS
d["live"]["equity_note"] = ("LIVE $811.85 (prov., +0.2% on the day) - OKLO 16 sh @ $44.43 (88% of equity, $99 cash), $39 GTC stop verified live at the broker. "
  "OKLO closed +0.8% (~$44.5), holding the $40-41 base well above the stop; its DOE nuclear-for-AI catalyst is confirmed live and it's insulated from tonight's GOOGL/TSLA binary. "
  "Held overnight as a swing (0/3 same-day day-trades used, nothing naked). Broke a 7-session cash camp. Post-print deploy (if any) fires at the 7/23 open.")
for pt in d["live"]["equity_curve"]:
    if pt.get("date") == "Jul 22":
        pt["value"] = 811.85

# ---- paper block ----
d["paper"]["equity"] = 90468.55
d["paper"]["updated"] = TS
d["paper"]["equity_note"] = ("Paper $90,469 (prov.; +0.3% at the 4pm regular close, firming to ~+0.5% on the AH mark as NVDA/AMD held). "
  "6 names (AMD/CEG/NVDA/OKLO/RKLB/SMR) all GTC-stopped, zero naked; ~21% ($19.1k / $19,127) cash held DRY for the confirmed post-binary deploy at the 7/23 open. "
  "GOOGL's +2.5% AH capex beat cues a bullish AI-infra open - deploy into CEG + OKLO, weight the mover.")
for pt in d["paper"]["equity_curve"]:
    if pt.get("date") == "Jul 22":
        pt["value"] = 90468.55

# ---- top-level updated ----
d["updated"] = TS

# ---- backup + atomic write ----
backup = os.path.join(SITE, "engine-data.backup-2026-07-22-1620.json")
shutil.copyfile(PATH, backup)
tmp = PATH + ".tmp"
with open(tmp, "w") as f:
    json.dump(d, f, indent=1, ensure_ascii=False)
os.replace(tmp, PATH)

# ---- verify read-back ----
with open(PATH) as f:
    v = json.load(f)
assert v["updated"] == TS, "updated mismatch"
assert v["accountability"]["final"] is True, "final not true"
assert v["accountability"]["grade"] == "C+", "grade mismatch"
assert v["pending_tickets"] == [], "pending not empty"
ranks = sorted(c["projection"]["pop_rank"] for c in v["coverage"])
assert ranks[0] == 1 and ranks.count(1) == 1, f"pop_rank not exactly one 1: {ranks}"
assert len(v["coverage"]) == 15, f"coverage len {len(v['coverage'])}"
assert v["live"]["positions"][0]["symbol"] == "OKLO", "live pos wrong"
print("OK publish verified")
print("updated:", v["updated"])
print("grade:", v["accountability"]["grade"], "final:", v["accountability"]["final"])
print("pop_ranks sorted:", ranks)
print("pulse len:", len(v["pulse"]), "| activity len:", len(v["activity"]))
print("live eq:", v["live"]["equity"], "| paper eq:", v["paper"]["equity"])
print("score:", v["score"])
print("coverage chg_pct:", [(c["ticker"], c["chg_pct"], c["projection"]["pop_rank"]) for c in v["coverage"]])
