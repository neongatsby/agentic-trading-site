#!/usr/bin/env python3
import json, os, tempfile, shutil, datetime

SITE = os.path.dirname(os.path.abspath(__file__))
F = os.path.join(SITE, "engine-data.json")
TS = "2026-07-22T10:14:00-04:00"

with open(F) as fh:
    d = json.load(fh)

# ---- backup ----
bak = os.path.join(SITE, "engine-data.backup-2026-07-22-1014.json")
with open(bak, "w") as fh:
    json.dump(d, fh, indent=1)

# ---- status ----
d["status"] = [{"session": "Morning", "text": "Rotation paying; OKLO +5% leads"}]

# ---- headlines ----
d["headlines"] = [
    "OKLO +5.4% leads the watchlist - Benzinga confirms it joined the Microsoft/NVIDIA-backed $200M federal nuclear-for-AI program; DOE AI-energy summit details may drop today; 12-mo analyst PT $86.50 (~96% upside)",
    "BINARY tonight: GOOGL (rev ~$117B; the raised $180-190B capex guide is THE number) + TSLA (EPS ~$0.50) report after the close - the first real Mag-7 AI-capex test; our OKLO/SMR/CEG nuclear book is insulated",
    "NEW catalyst: AMD + Anthropic sign a 2-gigawatt, tens-of-billions chip deal - AMD to invest up to $5B in Anthropic (WSJ); AMD +1%, a real reason to keep the chip hold",
    "Chips recovered off a soft open: SOXL round-tripped from -7% to flat, AMD +1%, NVDA flat - the pre-market give-back didn't stick",
    "Nuclear/power/space bid broadening: OKLO +5.4%, RKLB +4.1%, CEG +3.4% (new high) - the fresh-catalyst pocket leading an otherwise flat tape",
    "QQQ $707.5 = ~-1.0% under its $714.7 20-day -> 3x (SOXL/TQQQ) stays gated; SPY flat near a record high",
    "CNN Fear & Greed still in 'Fear'; Polymarket leaned S&P opens lower on oil - but the open printed roughly flat",
]

# ---- coverage (14) ----
d["coverage"] = [
    {
        "ticker": "OKLO", "name": "Oklo Inc.", "theme": "Advanced nuclear for AI power",
        "verdict": "buy", "verdict_label": "Buy - live armed + paper held",
        "thesis": "**Day's RS leader (+5.4%) and pop_rank 1 on a confirmed, dated catalyst** - tapped for the Trump/DOE $200M program to fast-track advanced reactors for AI data centers (with MSFT/NVDA); a DOE AI-energy summit TODAY may add detail. Spiked to a $47.48 HOD, eased to ~$46.5 (not overextended), still under its early-July $49-50 highs, no own earnings to Aug 18, insulated from tonight's Mag-7 capex binary.",
        "hold_reason": "Small modular nuclear-reactor company; we own it for the confirmed government catalyst - it just got tapped for the Trump/DOE $200M program to build advanced reactors to power AI data centers, alongside Microsoft and NVIDIA. We're long 300 shares (blended ~$44.6) after adding into strength this morning because it's the strongest name on our list and the story is playing out live, with a DOE summit today that could add detail. It spiked to $47.48 and eased to ~$46.5 - a normal breather; we'd sell if it lost the $40-41 base (stop's at $39).",
        "size": "$14.0k (300 sh paper)", "size_pct": 15.4,
        "size_note": "added +100 into strength; pop_rank-1 mover", "plan_usd": "$768 live (armed $48 limit, one tap) / +100 sh paper done",
        "chg_pct": "+5.4%",
        "projection": {"target_pct": 7.0, "confidence": "high", "basis": "DOE summit today; RS leader, catalyst live", "pop_rank": 1, "path_pct": [5, 6, 7]},
        "updated": TS, "horizon": "swing (multi-day)",
    },
    {
        "ticker": "RKLB", "name": "Rocket Lab", "theme": "Space / launch momentum",
        "verdict": "watch", "verdict_label": "Watch - momentum (pop_rank 2)",
        "thesis": "**+4.1% and pushing a new HOD $72** on space-launch momentum - the strongest raw mover on the list after OKLO. Clean momentum but no fresh catalyst we can point to, so it's a watch, not a chase into a soft tape.",
        "size": "-", "size_pct": 0, "size_note": "not held - watch",
        "plan_usd": "$0 - momentum watch, would want a pullback or a catalyst", "chg_pct": "+4.1%",
        "projection": {"target_pct": 4.5, "confidence": "med", "basis": "space momentum, reclaimed $72", "pop_rank": 2},
        "updated": TS, "horizon": "n/a",
    },
    {
        "ticker": "CEG", "name": "Constellation Energy", "theme": "Nuclear utility / power-for-AI",
        "verdict": "hold", "verdict_label": "Hold - power for AI, new HOD",
        "thesis": "**Green (+3.4%) at a new high and insulated from tonight's binary** - the utility angle on AI power demand; owns the nuclear fleet that signs data-center power deals. Steadier way to own the AI-needs-electricity theme, and it's leading today.",
        "hold_reason": "Constellation Energy - the utility angle on AI power demand, since it owns the nuclear fleet that can sign data-center power deals. It's green today (+3.4%) at a new high and, as a regulated power name, insulated from tonight's tech-capex earnings. We hold 16 shares with a $236 stop; a steadier way to own the same theme as OKLO/SMR, and it's confirming today.",
        "size": "$4.3k (16 sh paper)", "size_pct": 4.7, "size_note": "smallest core - steady power sleeve, at HOD",
        "plan_usd": "held paper", "chg_pct": "+3.4%",
        "projection": {"target_pct": 4.0, "confidence": "med", "basis": "power-for-AI, new HOD, insulated from binary", "pop_rank": 3},
        "updated": TS, "horizon": "swing (multi-day)",
    },
    {
        "ticker": "AMD", "name": "Advanced Micro Devices", "theme": "AI accelerators",
        "verdict": "hold", "verdict_label": "Hold - fresh Anthropic catalyst",
        "thesis": "**+1.0% on a FRESH catalyst** - WSJ reports AMD + Anthropic signed a 2-gigawatt, tens-of-billions chip deal, with AMD investing up to $5B in Anthropic. Real demand signal for the AI-accelerator story; own earnings not until Aug 4. Held through tonight's Mag-7 prints with a $490 stop.",
        "hold_reason": "Our other big chip position, and today it has a real fresh catalyst: the WSJ reports AMD and Anthropic signed a 2-gigawatt chip deal worth tens of billions, with AMD investing up to $5B in Anthropic. We own 30 shares from the CPI-rally entry; that's a direct demand signal for AMD's AI accelerators, and its own earnings aren't until Aug 4. We're holding through tonight's Mag-7 prints with the $490 stop.",
        "size": "$16.5k (30 sh paper)", "size_pct": 18.2, "size_note": "2nd-largest weight; fresh Anthropic deal",
        "plan_usd": "held paper", "chg_pct": "+1.0%",
        "projection": {"target_pct": 2.5, "confidence": "med", "basis": "fresh 2GW Anthropic chip deal (WSJ)", "pop_rank": 4},
        "updated": TS, "horizon": "swing (multi-day)",
    },
    {
        "ticker": "SMR", "name": "NuScale Power", "theme": "Small modular reactors",
        "verdict": "hold", "verdict_label": "Hold - nuclear, added",
        "thesis": "**Same nuclear-for-AI theme as OKLO, earlier-stage and cheaper** - added +350 sh this morning as the insulated way to press the theme without more chip exposure into tonight's binary. Up +1% today, still early in the theme's move.",
        "hold_reason": "NuScale - small modular reactors, the same nuclear-for-AI-power theme as OKLO but earlier-stage and cheaper per share. We added 350 shares (now 1050 total) this morning as the insulated way to press the theme without more chip exposure into tonight's binary. It's up modestly (+1%) and hasn't run like OKLO yet, which is part of why we liked the entry; stop's at $7.50 under the base.",
        "size": "$9.2k (1050 sh paper)", "size_pct": 10.2, "size_note": "added +350; theme catch-up candidate",
        "plan_usd": "+350 sh paper done", "chg_pct": "+1.0%",
        "projection": {"target_pct": 2.0, "confidence": "med", "basis": "nuclear theme catch-up, insulated from binary", "pop_rank": 5},
        "updated": TS, "horizon": "swing (multi-day)",
    },
    {
        "ticker": "BE", "name": "Bloom Energy", "theme": "Fuel cells / on-site power",
        "verdict": "watch", "verdict_label": "Watch - bounced, still extended",
        "thesis": "**+1.1%, bounced off a weak open** - fuel-cell/on-site-power name we traded live last week; part of the power-for-AI pocket but extended after its run, no fresh reason to re-enter here.",
        "size": "-", "size_pct": 0, "size_note": "not held - watch",
        "plan_usd": "$0 - no chase", "chg_pct": "+1.1%",
        "projection": {"target_pct": 1.5, "confidence": "low", "basis": "fuel-cell bounce, still extended", "pop_rank": 6},
        "updated": TS, "horizon": "n/a",
    },
    {
        "ticker": "IONQ", "name": "IonQ", "theme": "Quantum computing",
        "verdict": "watch", "verdict_label": "Watch - high-beta",
        "thesis": "**+0.2%, tracking the tape** - high-beta quantum name with no fresh catalyst; a watch that would move on broad risk-on, not something to force here.",
        "size": "-", "size_pct": 0, "size_note": "not held - watch",
        "plan_usd": "$0", "chg_pct": "+0.2%",
        "projection": {"target_pct": 0.8, "confidence": "low", "basis": "quantum high-beta, tracks tape", "pop_rank": 7},
        "updated": TS, "horizon": "n/a",
    },
    {
        "ticker": "RGTI", "name": "Rigetti Computing", "theme": "Quantum computing",
        "verdict": "watch", "verdict_label": "Watch - high-beta",
        "thesis": "**+0.3%, mild green** - the other quantum high-beta name; no catalyst, watch only.",
        "size": "-", "size_pct": 0, "size_note": "not held - watch",
        "plan_usd": "$0", "chg_pct": "+0.3%",
        "projection": {"target_pct": 1.0, "confidence": "low", "basis": "quantum high-beta", "pop_rank": 8},
        "updated": TS, "horizon": "n/a",
    },
    {
        "ticker": "NVDA", "name": "NVIDIA", "theme": "AI chip leader",
        "verdict": "hold", "verdict_label": "Hold - trimmed the anchor",
        "thesis": "**Flat (~0%), the laggard** - trimmed 140->90 at the open (it was 32% of the book and going nowhere while nuclear ran) and moved the cash into OKLO/SMR. Core AI-capex thesis intact (and AMD's Anthropic deal reads through positively) but exposed to tonight's GOOGL/TSLA capex print.",
        "hold_reason": "The AI-chip leader and still a big tech holding, but today it's the laggard - basically flat while nuclear runs. We trimmed it from 140 to 90 shares this morning to stop letting a flat mega-cap be a third of the book, and moved that money into the OKLO/SMR movers. We're keeping a core 90 shares (stop $186) because the AI-capex story is intact - today's AMD/Anthropic deal is a positive read-through - but it's exposed to tonight's Google/Tesla earnings, so we didn't want it oversized into that.",
        "size": "$18.6k (90 sh paper)", "size_pct": 20.6, "size_note": "trimmed from 32% -> 21% of book at the open",
        "plan_usd": "trimmed -50 sh paper; core held", "chg_pct": "-0.1%",
        "projection": {"target_pct": 0.0, "confidence": "low", "basis": "range-bound laggard into Mag-7 capex binary", "pop_rank": 9},
        "updated": TS, "horizon": "swing (multi-day)",
    },
    {
        "ticker": "MU", "name": "Micron", "theme": "HBM / memory",
        "verdict": "watch", "verdict_label": "Watch - extended, cooling",
        "thesis": "**-0.2%, cooling after its +12.8% rip** - the memory catalyst is real but it's extended; expressed via AMD/NVDA rather than chased here.",
        "size": "-", "size_pct": 0, "size_note": "not held - express via AMD/NVDA",
        "plan_usd": "$0 - extended", "chg_pct": "-0.2%",
        "projection": {"target_pct": -0.5, "confidence": "low", "basis": "cooling after the +12.8% rip, extended", "pop_rank": 10},
        "updated": TS, "horizon": "n/a",
    },
    {
        "ticker": "VRT", "name": "Vertiv", "theme": "Datacenter cooling / power",
        "verdict": "hold", "verdict_label": "Hold - laggard, on a short leash",
        "thesis": "**Weakest held name (-1.0%)** but it bounced off its $293.9 low and held $290 - still a rotation candidate. Kept on a short leash: a strong GOOGL/MSFT capex print tonight would help it (it's a capex beneficiary), so we give it a little room; stop $282, cut if it loses $290.",
        "hold_reason": "Vertiv - datacenter cooling and power gear, a picks-and-shovels AI-capex play. It's our weakest name today (-1.0%) but it bounced off its lows and held $290, so we're still holding for now - if it breaks $290 we'll cut it into a stronger name. We're giving it a little room because a strong capex print from Google/Microsoft tonight would actually help it; stop's at $282.",
        "size": "$9.0k (30 sh paper)", "size_pct": 9.9, "size_note": "rotation candidate if it loses $290",
        "plan_usd": "held paper - on a short leash", "chg_pct": "-1.0%",
        "projection": {"target_pct": -1.0, "confidence": "low", "basis": "datacenter laggard; two-way on tonight's capex", "pop_rank": 11},
        "updated": TS, "horizon": "swing (multi-day)",
    },
    {
        "ticker": "TSLA", "name": "Tesla", "theme": "EV / robotaxi / earnings tonight",
        "verdict": "avoid", "verdict_label": "Avoid - earnings tonight",
        "thesis": "**Flat (-0.35%) into its after-close print** - a binary tonight (EPS ~$0.50, rev ~$25.3B; robotaxi/FSD the focus); no pre-print position by design.",
        "size": "-", "size_pct": 0, "size_note": "not held - binary tonight",
        "plan_usd": "$0 pre-print", "chg_pct": "-0.35%",
        "projection": {"target_pct": 0.0, "confidence": "low", "basis": "earnings tonight = binary, avoid pre-print", "pop_rank": 12},
        "updated": TS, "horizon": "n/a",
    },
    {
        "ticker": "TQQQ", "name": "ProShares 3x Nasdaq", "theme": "3x leveraged (gated)",
        "verdict": "watch", "verdict_label": "Powder - awaits reclaim",
        "thesis": "**-0.6%, gated** - 3x Nasdaq stays in the powder pile until QQQ reclaims its $714.7 20-day; the regime gate that saved the book through the 7/14-20 wreck.",
        "size": "-", "size_pct": 0, "size_note": "dry powder while gated",
        "plan_usd": "$8-16k on a confirmed QQQ 20-day reclaim", "chg_pct": "-0.6%",
        "projection": {"target_pct": -1.0, "confidence": "low", "basis": "3x gated; awaits QQQ 20-day reclaim", "pop_rank": 13},
        "updated": TS, "horizon": "n/a",
    },
    {
        "ticker": "SOXL", "name": "Direxion 3x Semis", "theme": "3x leveraged (gated)",
        "verdict": "avoid", "verdict_label": "Gated - 3x under 20-day",
        "thesis": "**Round-tripped from -7% at the open to ~flat** - the exact chop the gate protects against; stays gated while QQQ is under its 20-day. Owning none of this whipsaw is the gate working.",
        "size": "-", "size_pct": 0, "size_note": "gated - do not touch",
        "plan_usd": "$0 while gated", "chg_pct": "-0.2%",
        "projection": {"target_pct": -1.0, "confidence": "med", "basis": "3x under 20-day; round-tripped off the -7% open", "pop_rank": 14},
        "updated": TS, "horizon": "n/a",
    },
]

# ---- pulse (prepend, cap 15) ----
d["pulse"].insert(0, {
    "ts": TS,
    "text": "10:14a: held the book - the open rotation into OKLO/SMR/CEG is paying. OKLO is the day's RS leader +5.4% (spiked to $47.48, eased to ~$46.5) on its confirmed DOE nuclear-for-AI catalyst (summit details may drop today); CEG +3.4% at a new high; and AMD +1% just landed a fresh catalyst - a 2-gigawatt, tens-of-billions chip deal with Anthropic (WSJ, AMD investing up to $5B). Kept ~21% paper powder dry into tonight's GOOGL/TSLA capex binary instead of chasing extended names into it. All 6 paper stops verified live, zero naked; QQQ still ~1% under its 20-day so 3x stays gated. The one gap is still LIVE - flat cash a 7th session with the OKLO ticket armed ($48 limit, one tap fills near ~$46.5). We own the pop_rank-1 mover in paper; live just needs the tap.",
    "hype": "OKLO's still leading at +5% and we own it in paper, plus AMD just landed a huge Anthropic chip deal. Holding cash for tonight's Google/Tesla earnings instead of chasing - the only piece missing is the live OKLO buy, armed for one tap.",
})
d["pulse"] = d["pulse"][:15]

# ---- feed (prepend activity, cap ~40) ----
d["feed"].insert(0, {
    "type": "activity",
    "ts": TS,
    "text": "10:14a - Held both books, no new trade. The open rotation is paying: OKLO +5.4% (RS leader on the DOE nuclear catalyst, 300 sh paper), CEG +3.4% at a new high, AMD +1% on a fresh 2-gigawatt Anthropic chip deal (WSJ). Kept ~21% paper cash as powder into tonight's GOOGL/TSLA binary - no fresh semi/3x size (QQQ still under its 20-day). All 6 paper GTC stops verified live, zero naked. LIVE flat a 7th session; OKLO ticket armed ($48 limit, one-tap fill).",
})
d["feed"] = d["feed"][:40]

# ---- activity (top-level engine log, prepend) ----
d["activity"].insert(0, {
    "ts": TS, "kind": "engine",
    "title": "Wed 7/22 ~10:14am ET (RTH run, ~40 min in). Held both books. OKLO +5.4% leads the watchlist on its confirmed DOE nuclear-for-AI catalyst (summit details may drop today); CEG +3.4% new HOD; AMD +1% on a fresh WSJ-reported 2GW Anthropic chip deal. Reconciled clean both ways - LIVE flat $810.32 cash (7th session, nothing naked); PAPER 6/6 GTC-stopped, zero naked, $90,646.74 (+0.75%). QQQ -1.0% under its 20-day -> 3x gated. Kept ~21% paper powder into tonight's GOOGL/TSLA binary; OKLO live ticket armed ($48 limit). No new trade; running grade B-.",
})
d["activity"] = d["activity"][:30]

# ---- score ----
d["score"] = {
    "alphaPts": "-15.7",
    "benchmark": "-3.2%",
    "bestDay": "+3.2%",
    "bestDayName": "Jul 14 - CPI chip rally (settled)",
    "winRate": "33%",
    "tradeCount": 6,
}

# ---- accountability (running, final:false) ----
d["accountability"] = {
    "date": "2026-07-22", "final": False,
    "grade": "B- (running, intraday ~40 min in)",
    "headline": "The open rotation is paying - paper owns the pop_rank-1 mover OKLO (+5.4%) right as it leads, plus a fresh AMD/Anthropic catalyst; the one persistent failure is LIVE still flat a 7th session with the OKLO tap un-hit.",
    "capture": {
        "bestName": "OKLO (+5.4%, held 300 sh paper - our pop_rank-1 call, leading)",
        "bestPct": "+5.4%",
        "capturedPct": "paper +0.75% / live flat",
        "rate": "~14% headline - we OWN the #1 mover but it's ~15% of a diversified book; live cash is the real drag",
    },
    "missed": [
        {"from": "watch RKLB", "to": "-", "note": "RKLB +4.1% (pop_rank 2) ran and we don't own it - a no-catalyst momentum name, defensible skip, logged honestly", "delta": "~watch"},
        {"from": "live cash", "to": "OKLO", "note": "LIVE still flat while its own armed pick OKLO is +5.4% - the un-tapped ticket is the real capture gap (7th straight cash session)", "delta": "needs the tap"},
    ],
    "saved": [
        {"note": "Gate kept live out of SOXL, which opened -7% and round-tripped to flat - owning none of that whipsaw is the gate working", "delta": "whipsaw dodged"},
        {"note": "No fresh semi/3x size into tonight's GOOGL/TSLA binary; held ~21% paper powder + insulated nuclear (OKLO/SMR/CEG) instead", "delta": "binary hedged"},
    ],
    "best": {"name": "OKLO", "note": "+5.4% RS leader on the confirmed DOE catalyst; weighted up in paper at the open (+100 @ ~$46) right as it ran", "delta": "+$570 paper unrealized"},
    "worst": {"name": "VRT", "note": "-1.0% laggard; bounced off its $293.9 low and held $290, kept on a short leash into tonight's capex prints", "delta": "-$90 paper intraday"},
    "applying": "Weight to the MOVER, not the anchor + be IN the pop you called (7/21 lesson): paper is weighted into the pop_rank-1 OKLO and the live OKLO ticket is armed to put the real money in it too.",
    "adjust": "Close the live gap - keep the OKLO ticket armed and loud for the one-tap fill. Into tonight's GOOGL/TSLA binary: no fresh semi/3x size, keep VRT on a short leash (cut if it loses $290), trail OKLO/CEG stops up once a higher low confirms, and finalize capture honestly on the post-close run.",
}

# ---- pending_tickets ----
d["pending_tickets"] = [{
    "id": "2026-07-22-1", "symbol": "OKLO", "side": "buy",
    "size": "$768", "qty": 16,
    "entry": "OKLO spiked to a $47.48 HOD on the DOE catalyst then eased to ~$46.5 (+5.4%), so the $48 marketable limit now fills a tap NEAR THE MONEY (~$46.5) - a LESS extended entry than the earlier spike (16 x $48 = $768 < $810 BP). Approve ANYTIME -> fills at <=$48; if it spikes back above $48 the limit rests and fills on a pullback. Multi-day swing, PDT-free (0/3).",
    "trigger": None, "stop": 39.0,
    "bracket": "stop $39 GTC (below the $40-41 base / 7/17 $39.53 low, ~-16% from ~$46.5)",
    "thesis": "Ends a 7th straight session of live cash by owning the watchlist's ACTUAL RS leader (pop_rank 1), not the laggard. OKLO is the day's strongest name (+5.4%) on a confirmed, dated catalyst (Trump/DOE $200M nuclear-for-AI program with MSFT/NVDA; DOE summit today; $86.50 analyst PT). Base reclaim off ~$40, no earnings to Aug 18, insulated from tonight's GOOGL/TSLA binary. Wide $39 stop, ~$120 max risk.",
    "limit": 48.0,
}]

# ---- equity curves: set Jul 22 marks to actual ----
def set_curve(curve, date, value):
    for pt in curve:
        if pt.get("date") == date:
            pt["value"] = value
            return
    curve.append({"date": date, "value": value})

set_curve(d["paper"]["equity_curve"], "Jul 22", 90646.74)
set_curve(d["live"]["equity_curve"], "Jul 22", 810.32)

# ---- latest_recap (stash old, set new) ----
d["_latest_recap_0955"] = d.get("latest_recap", "")
d["latest_recap"] = ("10:14a 7/22 (RTH, market OPEN ~40 min in). HELD both books - no new trade. The 9:48 open rotation is paying: "
    "OKLO +5.4% leads the watchlist (spiked $47.48, eased ~$46.5) on its confirmed Trump/DOE $200M nuclear-for-AI catalyst "
    "(OKLO+X-Energy w/ MSFT/NVDA; DOE summit details may drop today), CEG +3.4% at a new HOD, and AMD +1% on a FRESH "
    "WSJ-reported 2GW / tens-of-billions Anthropic chip deal (AMD investing up to $5B). Reconciled clean both ways - "
    "LIVE flat $810.32 cash (7th session, 0 positions/orders, nothing naked); PAPER 6/6 GTC-stopped "
    "(AMD $490/CEG $236/NVDA $186/OKLO $39/SMR $7.50/VRT $282), zero naked, $90,646.74 (+0.75%), ~21% cash. "
    "REGIME: QQQ $707.5 = -1.0% under its $714.67 20-day -> 3x gated; SPY flat near a record. Refreshed the OKLO live "
    "ticket 2026-07-22-1 (16 sh, $48 limit now a near-money/less-extended tap, $39 GTC stop) - armed, un-tapped. No fresh "
    "size into tonight's GOOGL/TSLA capex binary; ~21% powder for the post-print move. Running grade B- (paper owns the "
    "pop_rank-1 mover; live still the gap). Next run: confirm any OKLO fill if tapped, watch DOE-summit headlines + QQQ vs its 20-day, respect the binary.")

# ---- updated ----
d["updated"] = TS

# ---- atomic write ----
fd, tmp = tempfile.mkstemp(dir=SITE, suffix=".tmp")
with os.fdopen(fd, "w") as fh:
    json.dump(d, fh, indent=1)
os.replace(tmp, F)

# ---- read-back verify ----
with open(F) as fh:
    v = json.load(fh)
assert v["updated"] == TS, "updated mismatch"
assert v["accountability"]["final"] is False, "final should be false"
assert v["accountability"]["grade"].startswith("B-"), "grade mismatch"
ranks = [c["projection"]["pop_rank"] for c in v["coverage"]]
assert ranks.count(1) == 1, "must be exactly one pop_rank 1"
assert v["coverage"][0]["ticker"] == "OKLO" and v["coverage"][0]["projection"]["pop_rank"] == 1, "OKLO must be pop_rank 1"
assert len(v["pending_tickets"]) == 1 and v["pending_tickets"][0]["id"] == "2026-07-22-1", "pending ticket mismatch"
assert v["score"]["alphaPts"] == "-15.7", "score mismatch"
assert len(v["coverage"]) == 14, "coverage count"
assert len(v["pulse"]) == 15 and v["pulse"][0]["ts"] == TS, "pulse mismatch"
pj = [x for x in v["paper"]["equity_curve"] if x["date"] == "Jul 22"][0]["value"]
assert abs(pj - 90646.74) < 0.01, "paper curve mismatch"
print("VERIFY OK")
print("updated:", v["updated"])
print("grade:", v["accountability"]["grade"], "| final:", v["accountability"]["final"])
print("pop_rank1:", v["coverage"][0]["ticker"], "| coverage:", len(v["coverage"]))
print("pulse:", len(v["pulse"]), "| feed:", len(v["feed"]), "| activity:", len(v["activity"]))
print("pending:", v["pending_tickets"][0]["id"], v["pending_tickets"][0]["symbol"], "$"+str(v["pending_tickets"][0]["limit"]))
print("score alpha:", v["score"]["alphaPts"], "benchmark:", v["score"]["benchmark"])
print("paper Jul22:", pj, "| live Jul22:", [x for x in v["live"]["equity_curve"] if x["date"]=="Jul 22"][0]["value"])
