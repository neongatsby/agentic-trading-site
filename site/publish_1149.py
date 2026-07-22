#!/usr/bin/env python3
# Per-run engine-data publish (2026-07-22 ~11:49 ET). Unique name, atomic write, read-back verify.
import json, os, tempfile, shutil, datetime

SITE = os.path.dirname(os.path.abspath(__file__))
PATH = os.path.join(SITE, "engine-data.json")
NOW = "2026-07-22T11:49:00-04:00"

with open(PATH) as f:
    d = json.load(f)

# ---- backup the pre-write good state ----
bpath = os.path.join(SITE, "engine-data.backup-2026-07-22-1149.json")
with open(bpath, "w") as f:
    json.dump(d, f, indent=1)

d["updated"] = NOW

# ---- status ----
d["status"] = [
    {"session": "Morning", "text": "Rotated laggard into RKLB mover"}
]

# ---- headlines ----
d["headlines"] = [
    "Rocket Lab wins $266M Space Force suborbital-launch contract - RKLB +5%, watchlist's biggest mover today",
    "OKLO, X-Energy in $200M Trump/DOE program to fast-track nuclear reactors for AI data centers (MSFT/NVDA) - DOE AI-energy summit today",
    "Mega-cap earnings tonight: GOOGL, TSLA, IBM, TXN - first real Mag-7 AI-capex test after the close",
    "AMD + Anthropic 2-gigawatt chip deal (tens of $B); AMD to invest up to $5B in Anthropic - WSJ",
    "Nuclear-for-AI bid holds: CEG new highs +3.3%, OKLO +3.4%, SMR +0.9%",
    "Semis whippy: SOXL round-tripped -8% at the open -> +3% now; 3x still gated (QQQ -0.9% under its 20-day)",
    "Extended high-beta rolls over: PLTR -4.7%, SOFI -2.2% as money rotates to catalyst names",
    "Tape steady: SPY $749 near a record, QQQ flat"
]

# ---- coverage (15 names, exactly one pop_rank 1 = OKLO) ----
d["coverage"] = [
    {
        "ticker": "OKLO", "name": "Oklo Inc.", "theme": "Advanced nuclear for AI power",
        "verdict": "buy", "verdict_label": "Buy - live armed + paper held",
        "thesis": "**Day's RS leader (+3.4%) and pop_rank 1 on a confirmed, dated catalyst** - the Trump/DOE $200M program to fast-track advanced reactors for AI data centers (OKLO+X-Energy w/ MSFT/NVDA); a DOE AI-energy summit TODAY may add detail. Spiked to $47.48, eased to ~$45.6 (normal breather), still under its early-July $49-50 highs, no own earnings to Aug 18, insulated from tonight's Mag-7 capex binary.",
        "hold_reason": "Small-modular nuclear-reactor company and the name we're most excited about - the Trump/DOE just tapped it (with X-Energy, plus Microsoft and Nvidia) for a $200M program to power AI data centers, and a DOE energy summit today could add detail. Paper owns 300 sh from the open rotation (~$44.6) and we trailed the stop up to $43 to lock more of the gain. We'd sell if it loses the $43 base or the summit turns into a sell-the-news fade.",
        "size": "$13.7k (300 sh paper)", "size_pct": 15.0, "size_note": "pop_rank-1 mover; paper stop trailed $41.50->$43",
        "plan_usd": "$730 live (armed $48 limit, one tap) / 300 sh paper held", "chg_pct": "+3.4%",
        "projection": {"target_pct": 6.0, "confidence": "high", "basis": "DOE AI-energy summit today may drop $200M details; RS leader", "pop_rank": 1, "path_pct": [3.4, 4.8, 6.0]},
        "updated": NOW, "horizon": "swing (multi-day)"
    },
    {
        "ticker": "RKLB", "name": "Rocket Lab", "theme": "Space / launch / defense",
        "verdict": "buy", "verdict_label": "Buy - added on the contract",
        "thesis": "**Watchlist's BIGGEST mover (+5.0%) on a fresh, dated catalyst** - won a $266M Space Force suborbital-launch contract (12 vehicles + 6 options). Rotated into it this run out of the flat VRT laggard - weighting the mover, and it's space/defense so it's insulated from tonight's chip-capex binary. New HOD; stop $65.50 under the base.",
        "hold_reason": "Rocket Lab - space launch and defense. We rotated into it this morning (123 sh, ~$72.68) out of the VRT laggard because it's the watchlist's biggest mover today on a fresh, real catalyst: a $266M Space Force suborbital-launch contract. Stop's at $65.50 under the base, and it's insulated from tonight's chip-capex prints so it diversifies the book. We'd cut it if it loses $65.50.",
        "size": "$8.9k (123 sh paper)", "size_pct": 9.8, "size_note": "new hold; rotated in from VRT this run",
        "plan_usd": "123 sh paper (rotated from VRT)", "chg_pct": "+5.0%",
        "projection": {"target_pct": 7.0, "confidence": "high", "basis": "$266M Space Force contract; biggest mover, new HOD", "pop_rank": 2, "path_pct": [5.0, 6.2, 7.0]},
        "updated": NOW, "horizon": "swing (multi-day)"
    },
    {
        "ticker": "CEG", "name": "Constellation Energy", "theme": "Nuclear utility / power-for-AI",
        "verdict": "hold", "verdict_label": "Hold - power for AI, new HOD",
        "thesis": "**New-high breakout (+3.3%), watchlist #3 mover** - the power-for-AI proxy catching the same nuclear/utility-for-datacenter bid as OKLO, insulated from tonight's semi/capex binary. Trailed the stop up to $260 (~breakeven) to lock the gain.",
        "hold_reason": "Constellation Energy - the big nuclear utility that's become an AI-power play. It broke to new highs again today as the nuclear-for-AI theme broadened off the OKLO headline. We own 16 sh from ~$260.68 and trailed the stop up to $260 (about breakeven) to protect the run. We'd let it go if it loses $260; otherwise we ride the theme.",
        "size": "$4.3k (16 sh paper)", "size_pct": 4.8, "size_note": "new-high breakout; stop trailed $255->$260",
        "plan_usd": "held paper", "chg_pct": "+3.3%",
        "projection": {"target_pct": 4.5, "confidence": "med", "basis": "new HOD; nuclear-for-AI bid broadening", "pop_rank": 3},
        "updated": NOW, "horizon": "swing (multi-day)"
    },
    {
        "ticker": "AMD", "name": "Advanced Micro Devices", "theme": "AI accelerators",
        "verdict": "hold", "verdict_label": "Hold - Anthropic catalyst",
        "thesis": "**+2.1%, up ~5% since entry on a FRESH catalyst** - WSJ: AMD + Anthropic signed a 2-gigawatt, tens-of-billions chip deal, AMD investing up to $5B in Anthropic; 'Advancing AI' event today. Own earnings not until Aug 4. Trailed the stop up to $515 (below today's low) to lock a chunk before tonight's semi read-through.",
        "hold_reason": "AMD popped on a fresh WSJ report it signed a 2-gigawatt chip deal with Anthropic (investing up to $5B in them) - a real demand signal - plus its AI event today. We own 30 sh from ~$527.80, now up ~5%. We trailed the stop up to $515 (below today's low) to lock in a chunk of the gain ahead of tonight's semi read-through.",
        "size": "$16.7k (30 sh paper)", "size_pct": 18.3, "size_note": "2nd-largest weight; stop trailed $490->$515",
        "plan_usd": "held paper", "chg_pct": "+2.1%",
        "projection": {"target_pct": 3.5, "confidence": "med", "basis": "Anthropic 2GW deal + AI event today", "pop_rank": 4},
        "updated": NOW, "horizon": "swing (multi-day)"
    },
    {
        "ticker": "NVDA", "name": "NVIDIA", "theme": "AI chip leader",
        "verdict": "hold", "verdict_label": "Hold - core into the print",
        "thesis": "**+2.3%, recovered from a soft open** - core AI-capex anchor (trimmed to 90 sh earlier this week to fund the nuclear movers). Directly exposed to tonight's GOOGL capex guide, so it's two-way into the close; holding the core through the print behind a wide $186 stop rather than trailing tight into a binary.",
        "hold_reason": "Nvidia - our AI-infrastructure anchor. We trimmed it earlier this week to fund the nuclear movers but kept a 90-sh core (~$208). It's +2.3% today. Heads-up: tonight's GOOGL earnings/capex guide reads straight through to NVDA, so it's two-way into the close - we're holding the core through the print behind a wide $186 stop rather than trailing it tight into a binary.",
        "size": "$19.1k (90 sh paper)", "size_pct": 21.0, "size_note": "largest weight; wide $186 stop through the print",
        "plan_usd": "held paper", "chg_pct": "+2.3%",
        "projection": {"target_pct": 2.5, "confidence": "med", "basis": "recovered with tape; GOOGL capex read tonight", "pop_rank": 5},
        "updated": NOW, "horizon": "swing (multi-day)"
    },
    {
        "ticker": "SMR", "name": "NuScale Power", "theme": "Small modular reactors",
        "verdict": "hold", "verdict_label": "Hold - nuclear peer",
        "thesis": "**Same nuclear-for-AI theme as OKLO, cheaper/earlier-stage** - +0.9%, lagging the leader but riding the same catalyst. The insulated way to press the theme without more chip exposure into tonight's binary.",
        "hold_reason": "NuScale - another small-modular-reactor name, our second nuclear-for-AI position. We added at the open alongside OKLO (1050 sh, ~$8.66) to weight the theme. It's lagging OKLO today (+0.9%) but riding the same catalyst; stop sits at $7.50. If it keeps trailing the leader we'd rotate it into OKLO or RKLB.",
        "size": "$9.2k (1050 sh paper)", "size_pct": 10.1, "size_note": "theme catch-up; lagging OKLO",
        "plan_usd": "held paper", "chg_pct": "+0.9%",
        "projection": {"target_pct": 2.0, "confidence": "med", "basis": "nuclear peer, lagging OKLO today", "pop_rank": 6},
        "updated": NOW, "horizon": "swing (multi-day)"
    },
    {
        "ticker": "SOXL", "name": "Direxion 3x Semis", "theme": "3x leveraged (gated)",
        "verdict": "avoid", "verdict_label": "Gated - 3x under 20-day",
        "thesis": "**Round-tripped from -8% at the open to ~+3%** - the exact chop the gate protects against; stays gated while QQQ is under its 20-day. Owning none of this whipsaw is the gate working.",
        "size": "-", "size_pct": 0, "size_note": "gated - do not touch",
        "plan_usd": "$0 while gated", "chg_pct": "+2.9%",
        "projection": {"target_pct": 3.0, "confidence": "low", "basis": "3x semis gated; round-tripped -8%->+3%", "pop_rank": 7},
        "updated": NOW, "horizon": "n/a"
    },
    {
        "ticker": "BE", "name": "Bloom Energy", "theme": "Fuel cells / on-site power",
        "verdict": "watch", "verdict_label": "Watch - quiet today",
        "thesis": "**+0.5%, quiet** - fuel-cell/on-site-power name we traded live last week; part of the power-for-AI pocket but no fresh reason to re-enter here.",
        "size": "-", "size_pct": 0, "size_note": "not held - watch",
        "plan_usd": "$0 - no chase", "chg_pct": "+0.5%",
        "projection": {"target_pct": 1.5, "confidence": "low", "basis": "fuel-cell AI-power play, quiet today", "pop_rank": 8},
        "updated": NOW, "horizon": "n/a"
    },
    {
        "ticker": "RGTI", "name": "Rigetti Computing", "theme": "Quantum computing",
        "verdict": "watch", "verdict_label": "Watch - high-beta",
        "thesis": "**+0.9%, mild green** - quantum high-beta; no catalyst, watch only.",
        "size": "-", "size_pct": 0, "size_note": "not held - watch",
        "plan_usd": "$0", "chg_pct": "+0.9%",
        "projection": {"target_pct": 1.5, "confidence": "low", "basis": "quantum peer, small bid", "pop_rank": 9},
        "updated": NOW, "horizon": "n/a"
    },
    {
        "ticker": "IONQ", "name": "IonQ", "theme": "Quantum computing",
        "verdict": "watch", "verdict_label": "Watch - high-beta",
        "thesis": "**+0.5%, tracking the tape** - high-beta quantum name with no fresh catalyst; would move on broad risk-on, not something to force here.",
        "size": "-", "size_pct": 0, "size_note": "not held - watch",
        "plan_usd": "$0", "chg_pct": "+0.5%",
        "projection": {"target_pct": 1.0, "confidence": "low", "basis": "quantum, drifting with the tape", "pop_rank": 10},
        "updated": NOW, "horizon": "n/a"
    },
    {
        "ticker": "MU", "name": "Micron", "theme": "HBM / memory",
        "verdict": "watch", "verdict_label": "Watch - extended, cooling",
        "thesis": "**-0.1%, cooling after its +12.8% rip** - the memory catalyst is real but it's extended; expressed via AMD/NVDA rather than chased here.",
        "size": "-", "size_pct": 0, "size_note": "not held - express via AMD/NVDA",
        "plan_usd": "$0 - extended", "chg_pct": "-0.1%",
        "projection": {"target_pct": 1.0, "confidence": "low", "basis": "memory/HBM, digesting the rip", "pop_rank": 11},
        "updated": NOW, "horizon": "n/a"
    },
    {
        "ticker": "TQQQ", "name": "ProShares 3x Nasdaq", "theme": "3x leveraged (gated)",
        "verdict": "watch", "verdict_label": "Powder - awaits reclaim",
        "thesis": "**-0.2%, gated** - 3x Nasdaq stays in the powder pile until QQQ reclaims its $714.7 20-day; the regime gate that saved the book through the 7/14-20 wreck. Re-entry trigger is close (QQQ within 1%) but not met - won't add 3x into tonight's binary.",
        "size": "-", "size_pct": 0, "size_note": "dry powder while gated",
        "plan_usd": "$8-16k on a confirmed QQQ 20-day reclaim (not into the binary)", "chg_pct": "-0.2%",
        "projection": {"target_pct": 0.5, "confidence": "low", "basis": "3x QQQ gated under its 20-day", "pop_rank": 12},
        "updated": NOW, "horizon": "n/a"
    },
    {
        "ticker": "VRT", "name": "Vertiv", "theme": "Datacenter cooling / power",
        "verdict": "avoid", "verdict_label": "Sold - rotated into RKLB",
        "thesis": "**SOLD this run (-1.6%, the only red name)** - the weakest held name and a capex-beneficiary that's two-way into tonight's binary. Rotated the ~$9k into RKLB, the day's biggest mover on a fresh contract - opportunity cost is a sell signal. ~-$158 realized.",
        "size": "-", "size_pct": 0, "size_note": "sold 30 sh ~$299.5; rotated to RKLB",
        "plan_usd": "$0 - rotated out", "chg_pct": "-1.6%",
        "projection": {"target_pct": -0.5, "confidence": "low", "basis": "sold; laggard, 2-way into the binary", "pop_rank": 13},
        "updated": NOW, "horizon": "n/a"
    },
    {
        "ticker": "PLTR", "name": "Palantir", "theme": "AI software / high-beta",
        "verdict": "avoid", "verdict_label": "Avoid - rolling over",
        "thesis": "**Worst watchlist name (-4.7%)** - extended high-beta breaking down as money rotates out of the crowded momentum names into catalyst plays. Hold none; dodged it.",
        "size": "-", "size_pct": 0, "size_note": "not held - avoid",
        "plan_usd": "$0", "chg_pct": "-4.7%",
        "projection": {"target_pct": -3.0, "confidence": "low", "basis": "extended high-beta rolling over", "pop_rank": 14},
        "updated": NOW, "horizon": "n/a"
    },
    {
        "ticker": "TSLA", "name": "Tesla", "theme": "EV / robotaxi / earnings tonight",
        "verdict": "avoid", "verdict_label": "Avoid - earnings tonight",
        "thesis": "**-0.4% into its after-close print** - a binary tonight (robotaxi/FSD the focus, ~7% implied swing); no pre-print position by design.",
        "size": "-", "size_pct": 0, "size_note": "not held - binary tonight",
        "plan_usd": "$0 pre-print", "chg_pct": "-0.4%",
        "projection": {"target_pct": -1.0, "confidence": "low", "basis": "earnings tonight, ~7% implied swing", "pop_rank": 15},
        "updated": NOW, "horizon": "n/a"
    }
]

# ---- feed: prepend new items, cap 40 ----
new_feed = [
    {"type": "activity", "ts": NOW,
     "text": "11:49a - ACTIVE ROTATION: cut the VRT laggard (only red name, -1.6%, ~-$158 realized) into RKLB, the watchlist's BIGGEST mover (+5.0%) on a fresh $266M Space Force contract - weighting the mover, not the laggard, and swapping capex-beta for a name insulated from tonight's binary. Trailed 3 winners' stops UP (OKLO $41.50->$43, CEG $255->$260, AMD $490->$515); all 6 paper GTC-stopped, zero naked. LIVE flat a 7th session - OKLO one-tap still armed, the only gap. QQQ -0.9% under its 20-day, 3x gated (SOXL round-tripped -8%->+3%).",
     "reaction": "rotate"},
    {"type": "trade", "ts": NOW, "side": "sell", "symbol": "VRT", "status": "filled",
     "detail": "-30 @ ~$299.5 (paper)", "reaction": "rotate",
     "text": "Cut the only red name to fund the mover - opportunity cost is a sell signal. ~-$158 realized."},
    {"type": "trade", "ts": NOW, "side": "buy", "symbol": "RKLB", "status": "filled",
     "detail": "+123 @ $72.68 (paper)", "reaction": "rotate",
     "text": "Bought the day's biggest watchlist mover on a fresh $266M Space Force contract. Owning the pop, not watching it."}
]
d["feed"] = (new_feed + d.get("feed", []))[:40]

# ---- pulse: prepend one, cap 15 ----
new_pulse = {
    "ts": NOW,
    "text": "Rotated the flat VRT laggard into RKLB - it's the watchlist's biggest mover (+5%) on a fresh $266M Space Force contract, and the swap cuts capex-beta before tonight's GOOGL/TSLA binary. Trailed OKLO/CEG/AMD stops up to lock gains; all 6 paper positions stopped, ~21% powder for the post-print open. Live's still cash a 7th session - the OKLO one-tap is armed and it's the only gap. Next: hold the movers through the binary, deploy the powder tomorrow on what confirms.",
    "hype": "Swapped our one dead-weight name for RKLB, today's biggest mover on a fresh $266M contract. Live's still just sitting in cash though - that one tap is all that's missing."
}
d["pulse"] = ([new_pulse] + d.get("pulse", []))[:15]

# ---- latest_recap (rotate prev0) ----
d["_latest_recap_prev0"] = d.get("latest_recap", "")
d["latest_recap"] = ("11:49a 7/22 (RTH, market OPEN). ACTIVE ROTATION this run - cut the VRT laggard (30 sh @ ~$299.5, the only red name, ~-$158 realized) and put it into RKLB (123 sh @ $72.68), the watchlist's BIGGEST mover today (+5.0%) on a fresh, dated catalyst: a $266M Space Force suborbital-launch contract (confirmed Benzinga). Weights the MOVER not the laggard (7/21 lesson) AND cuts capex-beta before tonight's GOOGL/TSLA/IBM/TXN binary - RKLB is space/defense, insulated from it. Trailed 3 winners' stops UP to lock gains: OKLO $41.50->$43, CEG $255->$260, AMD $490->$515. Reconciled clean both ways - LIVE flat $810.32 cash (7th session, 0 positions/orders, nothing naked); PAPER 6/6 GTC-stopped (AMD $515 / CEG $260 / NVDA $186 / OKLO $43 / RKLB $65.50 / SMR $7.50), zero naked, $91,072 (+1.2%), ~21% cash. REGIME: QQQ $708.2 = -0.9% under its $714.67 20-day -> 3x gated (SOXL round-tripped -8%->+3%, glad we skipped it); SPY $748.9 near a record. Re-entry trigger is CLOSE (QQQ within 1% of its 20-day) but NOT met - today's tape is flat/narrow, not a clean 2nd green session, and I won't add 3x into tonight's binary. OKLO live ticket 2026-07-22-1 stays armed ($48 limit, $39 stop, one tap) - the only real gap. Running grade B-. Next run: confirm any OKLO fill if tapped, watch DOE-summit headlines + RKLB follow-through + QQQ vs its 20-day, respect the binary.")

# ---- accountability (running, final:false) ----
d["accountability"] = {
    "date": "2026-07-22", "final": False, "grade": "B- (running, ~2h15m in)",
    "headline": "Fixed the capture gap in real time - rotated the flat VRT laggard into RKLB, the watchlist's biggest mover (+5.0%) on a fresh $266M Space Force contract, so paper now OWNS the top mover instead of watching it; +1.2%, all 6 GTC-stopped, 3x gated through the SOXL -8%->+3% whipsaw. The lone failure stays LIVE flat a 7th session with the OKLO one-tap un-hit.",
    "capture": {
        "bestName": "RKLB +5.0% - the biggest watchlist mover, NOW HELD after this run's rotation",
        "bestPct": "+5.0%",
        "capturedPct": "paper +1.2% / live flat",
        "rate": "~24% headline vs RKLB, but we rotated INTO the +5% mover this run and own OKLO/CEG/AMD (all green); LIVE cash is the real drag, not selection"
    },
    "missed": [
        {"from": "live cash", "to": "OKLO", "note": "LIVE flat a 7th session while its own armed pick OKLO is +3.4% - the un-tapped ticket is the real capture gap", "delta": "needs the tap"},
        {"from": "paper (pre-11:49)", "to": "RKLB", "note": "owned RKLB only from ~11:49 - captured the rotation, not the full morning +5% run", "delta": "~partial"}
    ],
    "saved": [
        {"note": "Regime gate kept us clear of 3x semis - SOXL round-tripped -8%->+3% intraday; owning it would've been a whipsaw, not a win", "delta": "whipsaw dodged"},
        {"note": "Trailed OKLO->$43, CEG->$260, AMD->$515 to lock gains before tonight's binary; all 6 stops verified live", "delta": "gains protected"},
        {"note": "Cut binary-exposed VRT and kept ~21% powder - no fresh semi/3x size into the GOOGL/TSLA capex prints", "delta": "binary de-risked"}
    ],
    "avoided": {
        "worstName": "PLTR", "worstPct": "-4.7%",
        "note": "PLTR is the worst watchlist name today (-4.7%, extended high-beta rolling over) alongside SOFI -2.2% - we hold none, dodged both",
        "amount": "none held", "rate": "100% dodged (no position)"
    },
    "best": {"name": "RKLB + OKLO", "note": "the day's biggest mover (rotated into) and the pop_rank-1 RS leader - movers owned, not just watched", "delta": "+5.0% / +3.4%"},
    "worst": {"name": "VRT", "note": "sold the only red laggard at ~-$158 realized - an opportunity-cost rotation into RKLB, logged honestly", "delta": "-$158 realized"},
    "applying": "Weight to the MOVER + own the biggest name you're tracking (7/21 lesson): rotated the flat VRT laggard into RKLB, the day's biggest mover on a fresh catalyst, and trailed the winners' stops before the binary. Plus the earned regime gate - stayed clear of gated 3x semis.",
    "adjust": "Close the live gap - OKLO one-tap stays armed and loud. Hold the movers through tonight's GOOGL/TSLA/IBM/TXN binary with verified stops; no fresh 3x while QQQ is under its 20-day; ~21% powder for tomorrow's post-print open. Finalize capture honestly on the post-close run."
}

# ---- score (update alpha + benchmark off live TQQQ; no live round-trip closed this run) ----
d["score"] = {
    "alphaPts": "-16.1",
    "benchmark": "-2.9%",
    "bestDay": "+3.2%",
    "bestDayName": "Jul 14 - CPI chip rally (settled)",
    "winRate": "33%",
    "tradeCount": 6
}

# ---- paper equity + curve ----
d.setdefault("paper", {})
d["paper"]["equity"] = 91071.62
d["paper"]["updated"] = NOW
d["paper"]["equity_note"] = "Paper $91,072 (+1.2% intraday). Rotated the VRT laggard into RKLB (the day's biggest mover, +5.0%, fresh $266M Space Force contract); now owns OKLO +3.4% / CEG +3.3% / AMD +2.1% / NVDA +2.3% / RKLB +5.0% / SMR +0.9% - all 6 GTC-stopped, zero naked. ~21% cash powder held into tonight's GOOGL/TSLA capex binary; no fresh 3x while gated."
if isinstance(d["paper"].get("equity_curve"), list) and d["paper"]["equity_curve"]:
    last = d["paper"]["equity_curve"][-1]
    if last.get("date") == "Jul 22":
        last["value"] = 91071.62
    else:
        d["paper"]["equity_curve"].append({"date": "Jul 22", "value": 91071.62})

# ---- live equity + curve (flat cash, unchanged) ----
d.setdefault("live", {})
d["live"]["equity"] = 810.32
d["live"]["updated"] = NOW
d["live"]["equity_note"] = "Live $810.32, 100% cash a 7th straight session (0 positions/orders, nothing naked). The OKLO one-tap ticket (16 sh, $48 limit, $39 stop) is armed - approve fills it at the next print. Closing this cash gap is the single highest-value action; -19.0% since $1,000 inception."
if isinstance(d["live"].get("equity_curve"), list) and d["live"]["equity_curve"]:
    last = d["live"]["equity_curve"][-1]
    if last.get("date") == "Jul 22":
        last["value"] = 810.32
    else:
        d["live"]["equity_curve"].append({"date": "Jul 22", "value": 810.32})

# ---- atomic write ----
fd, tmp = tempfile.mkstemp(dir=SITE, suffix=".tmp")
with os.fdopen(fd, "w") as f:
    json.dump(d, f, indent=1, ensure_ascii=False)
os.replace(tmp, PATH)

# ---- read-back verify ----
with open(PATH) as f:
    chk = json.load(f)
assert chk["updated"] == NOW, "updated mismatch"
assert chk["accountability"]["date"] == "2026-07-22" and chk["accountability"]["final"] is False, "acct mismatch"
assert len(chk["pending_tickets"]) == 1 and chk["pending_tickets"][0]["id"] == "2026-07-22-1", "ticket mismatch"
assert chk["coverage"][0]["ticker"] == "OKLO" and chk["coverage"][0]["projection"]["pop_rank"] == 1, "pop_rank mismatch"
pr1 = [c["ticker"] for c in chk["coverage"] if c["projection"]["pop_rank"] == 1]
assert pr1 == ["OKLO"], f"exactly one pop_rank1 expected, got {pr1}"
assert chk["paper"]["equity"] == 91071.62 and chk["live"]["equity"] == 810.32, "equity mismatch"
print("OK verify:",
      "updated", chk["updated"],
      "| grade", chk["accountability"]["grade"],
      "| cov", len(chk["coverage"]),
      "| feed", len(chk["feed"]),
      "| pulse", len(chk["pulse"]),
      "| pop1", pr1)
