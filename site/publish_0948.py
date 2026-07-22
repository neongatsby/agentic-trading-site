#!/usr/bin/env python3
import json, os, tempfile

SITE = os.path.dirname(os.path.abspath(__file__))
PATH = os.path.join(SITE, "engine-data.json")
TS = "2026-07-22T09:48:00-04:00"

with open(PATH) as f:
    d = json.load(f)

d["updated"] = TS

d["status"] = [{"session": "Morning", "text": "Trimmed NVDA anchor into OKLO/SMR"}]

d["headlines"] = [
    "OKLO +4% leads the watchlist: Benzinga confirms it joined the Microsoft/NVIDIA-backed federal $200M nuclear-for-AI program; DOE AI-energy summit today; 12-mo analyst PT $86.50 (~96% upside)",
    "BINARY tonight: GOOGL + TSLA report after the close (IBM, TXN too) - the first Mag-7 AI-capex test; our OKLO/SMR/CEG nuclear book is insulated from it",
    "Chips mixed after a soft open: SOXL -2.6%, MU -1.1%, but AMD +0.6% and NVDA flat - the 2-day rip give-back is orderly, not a rout",
    "Super Micro (SMCI) +20% on results - the day's biggest single-name mover (not held; can't chase a +20% gap)",
    "Nuclear/power/space bid: OKLO +4%, RKLB +3%, CEG +1.7% - the fresh-catalyst pocket while the broad tape is soft (QQQ -0.6%)",
    "QQQ ~$705 = ~-1.4% under its $714.7 20-day - 3x (SOXL/TQQQ) stays gated",
    "VRT -2.5%, the watchlist laggard (datacenter cooling) - two-way into tonight's capex prints; kept on a short leash, stop $282"
]

d["coverage"] = [
    {"ticker":"OKLO","name":"Oklo Inc.","theme":"Advanced nuclear for AI power","verdict":"buy","verdict_label":"Buy - live staged + paper added",
     "thesis":"**Day's RS leader (+4%) and pop_rank 1 on a confirmed, dated catalyst** - tapped for the Trump/DOE $200M program to fast-track advanced reactors for AI data centers (with MSFT/NVDA); DOE AI-energy summit TODAY. Base reclaim off ~$40, still under its early-July $49-50 highs (not extended), no own earnings to Aug 18, insulated from tonight's Mag-7 capex binary.",
     "hold_reason":"Small modular nuclear-reactor company; we own it for the confirmed government catalyst - it just got tapped for the Trump/DOE $200M program to build advanced reactors to power AI data centers, alongside Microsoft and NVIDIA. We're long 300 shares (blended ~$44.6) and added into strength this morning because it's the strongest name on our list and the story is playing out live, with a DOE summit today that could add detail. We'd sell if it lost the $40-41 base (stop's at $39); a sell-the-summit fade is the risk we're watching.",
     "size":"$13.8k (300 sh paper)","size_pct":15.3,"size_note":"added +100 into strength; 3rd-largest book weight",
     "plan_usd":"$735 live (staged, one tap) / +100 sh paper done","chg_pct":"+4.0%",
     "projection":{"target_pct":6.5,"confidence":"high","basis":"DOE nuclear-for-AI catalyst + summit today, RS leader","pop_rank":1,"path_pct":[4,5,6.5]},
     "updated":TS,"horizon":"swing (multi-day)"},
    {"ticker":"RKLB","name":"Rocket Lab","theme":"Space / launch momentum","verdict":"watch","verdict_label":"Watch - momentum (pop_rank 2)",
     "thesis":"**+3% and reclaimed $70** on space-launch momentum - the other strong green on the list today. A clean momentum name but no fresh catalyst we can point to, so it's a watch, not a chase into a soft tape.",
     "size":"-","size_pct":0,"size_note":"not held - watch",
     "plan_usd":"$0 - momentum watch, would want a pullback or a catalyst","chg_pct":"+3.0%",
     "projection":{"target_pct":3.5,"confidence":"med","basis":"space momentum breakout, reclaimed $70","pop_rank":2},
     "updated":TS,"horizon":"n/a"},
    {"ticker":"CEG","name":"Constellation Energy","theme":"Nuclear utility / power-for-AI","verdict":"hold","verdict_label":"Hold - power for AI",
     "thesis":"**Green (+1.7%) and insulated from tonight's binary** - the utility angle on AI power demand; owns the nuclear fleet that signs data-center power deals. Steadier way to own the AI-needs-electricity theme.",
     "hold_reason":"Constellation Energy - the utility angle on AI power demand, since it owns the nuclear fleet that can sign data-center power deals. It's green today (+1.7%) and, as a regulated power name, insulated from tonight's tech-capex earnings. We hold 16 shares with a $236 stop; a steadier way to own the same theme as OKLO/SMR.",
     "size":"$4.3k (16 sh paper)","size_pct":4.7,"size_note":"smallest core - steady power sleeve",
     "plan_usd":"held paper","chg_pct":"+1.7%",
     "projection":{"target_pct":2.5,"confidence":"med","basis":"power-for-AI bid, insulated from binary","pop_rank":3},
     "updated":TS,"horizon":"swing (multi-day)"},
    {"ticker":"SMR","name":"NuScale Power","theme":"Small modular reactors","verdict":"hold","verdict_label":"Hold - nuclear, added",
     "thesis":"**Same nuclear-for-AI theme as OKLO, earlier-stage and cheaper** - added +350 sh this morning as the insulated way to press the theme without more chip exposure into tonight's binary. Hasn't run yet today (~flat), part of why we like the entry.",
     "hold_reason":"NuScale - small modular reactors, the same nuclear-for-AI-power theme as OKLO but earlier-stage and cheaper per share. We added 350 shares (now 1050 total) this morning as the insulated way to press the theme without more chip exposure into tonight's binary. It hasn't run yet today, which is partly why we liked the entry; stop's at $7.50 under the base.",
     "size":"$9.2k (1050 sh paper)","size_pct":10.2,"size_note":"added +350; theme catch-up candidate",
     "plan_usd":"+350 sh paper done","chg_pct":"+0.2%",
     "projection":{"target_pct":2.0,"confidence":"med","basis":"nuclear theme catch-up, insulated","pop_rank":4},
     "updated":TS,"horizon":"swing (multi-day)"},
    {"ticker":"AMD","name":"Advanced Micro Devices","theme":"AI accelerators","verdict":"hold","verdict_label":"Hold - owned chip leader",
     "thesis":"**Green (+0.6%) after the soft open** - the AI-accelerator demand story intact, own earnings not until Aug 4. Held through tonight's Mag-7 prints with a $490 stop; exposed to the capex read but not oversized.",
     "hold_reason":"Our other big chip position, and it's actually green today after a soft open. We own 30 shares from the CPI-rally entry; the thesis is the same AI-accelerator demand story, and its own earnings aren't until Aug 4. We're holding through tonight's Mag-7 prints with the $490 stop; we'd reconsider if the whole chip complex breaks down.",
     "size":"$16.4k (30 sh paper)","size_pct":18.2,"size_note":"2nd-largest weight; green today",
     "plan_usd":"held paper","chg_pct":"+0.6%",
     "projection":{"target_pct":1.0,"confidence":"low","basis":"chip bid, but capex binary tonight caps it","pop_rank":5},
     "updated":TS,"horizon":"swing (multi-day)"},
    {"ticker":"IONQ","name":"IonQ","theme":"Quantum computing","verdict":"watch","verdict_label":"Watch - high-beta",
     "thesis":"**+0.4%, tracking the tape** - high-beta quantum name with no fresh catalyst; a watch that would move on broad risk-on, not something to force here.",
     "size":"-","size_pct":0,"size_note":"not held - watch",
     "plan_usd":"$0","chg_pct":"+0.4%",
     "projection":{"target_pct":0.8,"confidence":"low","basis":"quantum high-beta, tracks tape","pop_rank":6},
     "updated":TS,"horizon":"n/a"},
    {"ticker":"RGTI","name":"Rigetti Computing","theme":"Quantum computing","verdict":"watch","verdict_label":"Watch - high-beta",
     "thesis":"**+0.8%, mild green** - the other quantum high-beta name; no catalyst, watch only.",
     "size":"-","size_pct":0,"size_note":"not held - watch",
     "plan_usd":"$0","chg_pct":"+0.8%",
     "projection":{"target_pct":1.0,"confidence":"low","basis":"quantum high-beta","pop_rank":7},
     "updated":TS,"horizon":"n/a"},
    {"ticker":"NVDA","name":"NVIDIA","theme":"AI chip leader","verdict":"hold","verdict_label":"Hold - trimmed the anchor",
     "thesis":"**Trimmed 140->90 this morning** - it was 32% of the book and flat (the exact 7/21 laggard-too-heavy miss), so we cut it to ~21% and moved the cash into the OKLO/SMR movers. Core AI-capex thesis intact (Taiwan export orders +59%, Wistron/NVDA $700M plant) but exposed to tonight's GOOGL/TSLA read.",
     "hold_reason":"The AI-chip leader and still our biggest tech holding, but today it's the laggard - basically flat while nuclear runs. We trimmed it from 140 to 90 shares this morning to stop letting a flat mega-cap be a third of the book, and moved that money into the OKLO/SMR movers. We're keeping a core 90 shares (stop $186) because the AI-capex story is intact - but it's exposed to tonight's Google/Tesla earnings, so we didn't want it oversized into that.",
     "size":"$18.6k (90 sh paper)","size_pct":20.7,"size_note":"trimmed from 32% -> 21% of book",
     "plan_usd":"trimmed -50 sh paper; core held","chg_pct":"0.0%",
     "projection":{"target_pct":0.0,"confidence":"low","basis":"range-bound laggard into Mag-7 capex binary","pop_rank":8},
     "updated":TS,"horizon":"swing (multi-day)"},
    {"ticker":"MU","name":"Micron","theme":"HBM / memory","verdict":"watch","verdict_label":"Watch - extended, giving back",
     "thesis":"**-1.1%, unwinding part of its +12.8% rip** - the memory catalyst is real but it's extended; expressed via AMD/NVDA rather than chased here.",
     "size":"-","size_pct":0,"size_note":"not held - express via AMD/NVDA",
     "plan_usd":"$0 - extended","chg_pct":"-1.1%",
     "projection":{"target_pct":-1.5,"confidence":"low","basis":"giving back the +12.8% rip, extended","pop_rank":9},
     "updated":TS,"horizon":"n/a"},
    {"ticker":"BE","name":"Bloom Energy","theme":"Fuel cells / on-site power","verdict":"watch","verdict_label":"Watch - extended, don't chase",
     "thesis":"**-1.4%, consolidating after its run** - fuel-cell/on-site-power name we traded live last week; extended and range-bound now, no fresh reason to re-enter.",
     "size":"-","size_pct":0,"size_note":"not held - watch",
     "plan_usd":"$0 - no chase","chg_pct":"-1.4%",
     "projection":{"target_pct":-1.0,"confidence":"low","basis":"fuel-cell extended, consolidating","pop_rank":10},
     "updated":TS,"horizon":"n/a"},
    {"ticker":"VRT","name":"Vertiv","theme":"Datacenter cooling / power","verdict":"hold","verdict_label":"Hold - laggard, rotation candidate",
     "thesis":"**Weakest name today (-2.5%) and slipping below its range** - now a rotation candidate. Kept on a short leash: a strong GOOGL/MSFT capex print tonight would help it (it's a capex beneficiary), so we give it a little room; stop $282.",
     "hold_reason":"Vertiv - datacenter cooling and power gear, a picks-and-shovels AI-capex play. It's our weakest name today (-2.5%) and slipping below its recent range, so it's now a rotation candidate - if it keeps breaking down we'll cut it into a stronger name. We're giving it a little room because a strong capex print from Google/Microsoft tonight would actually help it; stop's at $282.",
     "size":"$8.9k (30 sh paper)","size_pct":9.9,"size_note":"rotation candidate if it loses $290",
     "plan_usd":"held paper - on a short leash","chg_pct":"-2.5%",
     "projection":{"target_pct":-2.0,"confidence":"low","basis":"datacenter laggard; two-way on tonight's capex","pop_rank":11},
     "updated":TS,"horizon":"swing (multi-day)"},
    {"ticker":"TSLA","name":"Tesla","theme":"EV / robotaxi / earnings tonight","verdict":"avoid","verdict_label":"Avoid - earnings tonight",
     "thesis":"**Flat (-0.2%) into its after-close print** - a binary tonight; no pre-print position by design.",
     "size":"-","size_pct":0,"size_note":"not held - binary tonight",
     "plan_usd":"$0 pre-print","chg_pct":"-0.2%",
     "projection":{"target_pct":0.0,"confidence":"low","basis":"earnings tonight = binary, avoid pre-print","pop_rank":12},
     "updated":TS,"horizon":"n/a"},
    {"ticker":"TQQQ","name":"ProShares 3x Nasdaq","theme":"3x leveraged (gated)","verdict":"watch","verdict_label":"Powder - awaits reclaim",
     "thesis":"**-1.8%, gated** - 3x Nasdaq stays in the powder pile until QQQ reclaims its $714.7 20-day; the regime gate that saved the book through the 7/14-20 wreck.",
     "size":"-","size_pct":0,"size_note":"dry powder while gated",
     "plan_usd":"$8-16k on a confirmed QQQ 20-day reclaim","chg_pct":"-1.8%",
     "projection":{"target_pct":-2.0,"confidence":"low","basis":"3x gated; awaits QQQ 20-day reclaim","pop_rank":13},
     "updated":TS,"horizon":"n/a"},
    {"ticker":"SOXL","name":"Direxion 3x Semis","theme":"3x leveraged (gated)","verdict":"avoid","verdict_label":"Gated - 3x under 20-day",
     "thesis":"**-2.6%, gated** - 3x semis giving back the 2-day rip; stays gated while QQQ is under its 20-day. Owning none of this is the gate working.",
     "size":"-","size_pct":0,"size_note":"gated - do not touch",
     "plan_usd":"$0 while gated","chg_pct":"-2.6%",
     "projection":{"target_pct":-3.0,"confidence":"med","basis":"3x under 20-day, semis soft","pop_rank":14},
     "updated":TS,"horizon":"n/a"}
]

new_pulse = {"ts":TS,
    "text":"9:48a, ~18 min into the session. EXECUTED the planned rotation on the paper book: trimmed the NVDA anchor 140->90 (it was 32% of the book and flat - the exact 7/21 laggard-too-heavy miss) and moved the ~$10k into the nuclear movers - OKLO +100 (now 300 sh) and SMR +350 (now 1050) - both insulated from tonight's GOOGL/TSLA capex binary; all stops cleanly re-armed, zero naked (6/6). OKLO is the day's watchlist leader (+4%) on its now-Benzinga-confirmed DOE nuclear-for-AI catalyst (summit today, $86.50 analyst PT) = still pop_rank 1, and paper is now properly weighted into it. LIVE still flat $810 cash: the OKLO ticket (16 sh, $47 marketable-limit, $39 stop) is armed to fill IMMEDIATELY on your tap - that tap is the one thing that ends the 7-session cash camp and puts the real money in the mover. Held ~21% paper cash as dry powder into the binary; no fresh semi size by design.",
    "hype":"Moved the paper money out of flat NVDA into OKLO and SMR - the nuclear names actually moving today, and they don't care about tonight's Google/Tesla earnings. The live OKLO buy's armed - one tap finally puts the real money in the mover."}
d["pulse"] = [new_pulse] + d.get("pulse", [])[:14]

new_feed = [
    {"type":"activity","ts":TS,"text":"9:47a - EXECUTED the NVDA-anchor -> nuclear-mover rotation on paper (the 7/21 weight-to-the-mover fix), at the open with real prices and clean stop re-arms. Trimmed NVDA 140->90 (~$207.1), added OKLO +100 (~$46.00, now 300 sh) and SMR +350 (~$8.74, now 1050 sh). Book re-weighted: NVDA 32%->21%, OKLO 10%->15%. All 6 paper positions GTC-stopped, zero naked (verified at the broker). LIVE unchanged - flat $810 cash, OKLO ticket armed for a one-tap intraday fill."},
    {"type":"trade","ts":TS,"side":"buy","symbol":"OKLO","status":"filled","detail":"+100 @ ~$46.00 (paper)","reaction":"rotate","text":"Added to the leader into strength - OKLO now 300 sh, our pop_rank-1 name on the DOE nuclear catalyst. Weighting the mover, not the laggard."},
    {"type":"trade","ts":TS,"side":"buy","symbol":"SMR","status":"filled","detail":"+350 @ ~$8.74 (paper)","reaction":"rotate","text":"Pressed the nuclear theme via SMR (now 1050 sh) - insulated from tonight's tech-capex binary and hadn't run yet today."},
    {"type":"trade","ts":TS,"side":"sell","symbol":"NVDA","status":"filled","detail":"-50 @ ~$207.1 (paper)","reaction":"rotate","text":"Trimmed the flat NVDA anchor from 32% to ~21% of the book - a flat mega-cap shouldn't be a third of the book while the nuclear names run. Core 90 sh held, stop $186."}
]
d["feed"] = new_feed + d.get("feed", [])[:36]

d["score"] = {"alphaPts":"-14.5","benchmark":"-4.4%","bestDay":"+3.2%","bestDayName":"Jul 14 - CPI chip rally (settled)","winRate":"33%","tradeCount":6}

d["accountability"] = {
    "date":"2026-07-22","final":False,"grade":"running (intraday, ~18 min in)",
    "headline":"EXECUTED the 7/21 fix on paper - trimmed the 32% flat-NVDA anchor into the OKLO/SMR nuclear movers so the book is finally weighted to the pop_rank-1 mover (OKLO +4%), all stops re-armed zero-naked; the one remaining gap is LIVE, still flat cash with the OKLO ticket armed for a one-tap fill.",
    "capture":{"bestName":"OKLO (+4.0%, held both books - our pop_rank-1 call)","bestPct":"+4.0%","capturedPct":"paper +0.2% / live flat","rate":"~5% and early - the rotation just re-weighted paper toward OKLO/SMR; the point of the trim is to lift capture from here, not to have banked it 18 min in"},
    "missed":[{"from":"watch RKLB","to":"-","note":"RKLB +3% (called pop_rank 2) ran and we don't own it - a momentum name with no catalyst we could point to, so a defensible skip, but logging it honestly","delta":"~watch"}],
    "saved":[
        {"note":"Executed the NVDA->nuclear rotation with zero naked window mishandled - cancelled stops, filled, re-armed all 6 GTC stops (independently re-verified at the broker)","delta":"risk bounded"},
        {"note":"No fresh semi/3x size into tonight's GOOGL/TSLA/IBM/TXN binary; rotated INTO insulated nuclear (OKLO/SMR/CEG) instead - the gate + de-risk working together","delta":"binary hedged"}],
    "best":{"name":"OKLO","note":"+4.0% RS leader on the confirmed DOE catalyst; now properly weighted in paper and armed live","delta":"+$525 paper intraday"},
    "worst":{"name":"VRT","note":"-2.5% laggard slipping below its range; kept on a short leash into tonight's capex prints","delta":"-$225 paper intraday"},
    "applying":"Weight to the MOVER, not the anchor + be IN the pop you called (7/21 lesson): EXECUTED - trimmed the 32% NVDA anchor into OKLO/SMR at the open so paper is now weighted to the pop_rank-1 mover, and the live OKLO ticket is armed to put the real money in it too.",
    "adjust":"Close the live gap: the paper fix is done; LIVE is still flat, so keep the OKLO ticket armed and loud for the one-tap fill. Into tonight's binary - no fresh semi size, keep VRT on a short leash (cut into a stronger name if it loses $290), and finalize capture honestly at the close."
}

d["pending_tickets"] = [{
    "id":"2026-07-22-1","symbol":"OKLO","side":"buy","size":"$735","qty":16,
    "entry":"~$46 - approve ANYTIME -> fills IMMEDIATELY at the marketable-limit $47 (OKLO ~$45.9 now). Multi-day swing, PDT-free (0/3 day-trades). The 9:30 open has passed; this is a live intraday fill on your tap.",
    "trigger":None,"stop":39.0,
    "bracket":"stop $39 GTC (below this week's $40-41 base / the 7/17 $39.53 low, -15%)",
    "thesis":"Ends the 7th straight session of live cash by owning the watchlist's ACTUAL RS leader (pop_rank 1), not the laggard. OKLO is the day's strongest name (+4%) on a confirmed, dated catalyst (Trump/DOE $200M nuclear-for-AI program with MSFT/NVDA; DOE summit today; $86.50 analyst PT). Base reclaim off ~$40, no earnings to Aug 18, insulated from tonight's GOOGL/TSLA binary. Wide $39 stop, ~$110 max risk."
}]

d["live"]["equity"] = 810.32
d["live"]["cash"] = 810.32
d["live"]["positions"] = []
d["live"]["updated"] = TS
d["live"]["equity_note"] = "LIVE flat $810.32 cash / zero positions / zero naked (7th cash session). 1 staged ticket = BUY OKLO 16 sh (~$46, $47 marketable-limit, $39 stop, $735) armed to fill IMMEDIATELY on your tap - the 9:30 open has passed so a tap now fills on the spot. This is the one action that ends the cash camp and puts the real money in the pop_rank-1 mover."
lc = d["live"].get("equity_curve", [])
if not (lc and lc[-1].get("date") == "Jul 22"):
    lc.append({"date":"Jul 22","value":810.32})
d["live"]["equity_curve"] = lc

d["paper"]["equity"] = 90161.19
d["paper"]["updated"] = TS
d["paper"]["equity_note"] = "Paper ~$90.2k (+0.2% intraday). EXECUTED the rotation: trimmed NVDA 140->90 (~21% of book, from 32%) into OKLO +100 (300 sh) and SMR +350 (1050 sh) - the nuclear movers, insulated from tonight's binary. 6/6 GTC-stopped, zero naked; ~21% cash held as dry powder into the GOOGL/TSLA prints. OKLO +4% leads; VRT -2.5% the laggard on a short leash."
pc = d["paper"].get("equity_curve", [])
if not (pc and pc[-1].get("date") == "Jul 22"):
    pc.append({"date":"Jul 22","value":90161.19})
d["paper"]["equity_curve"] = pc

fd, tmp = tempfile.mkstemp(dir=SITE, suffix=".tmp")
with os.fdopen(fd, "w") as f:
    json.dump(d, f, indent=1, ensure_ascii=False)
os.replace(tmp, PATH)

with open(PATH) as f:
    chk = json.load(f)
assert chk["updated"] == TS
assert chk["accountability"]["date"] == "2026-07-22"
assert len(chk["pending_tickets"]) == 1 and chk["pending_tickets"][0]["id"] == "2026-07-22-1"
assert len(chk["coverage"]) == 14 and chk["coverage"][0]["ticker"] == "OKLO"
ranks = [c["projection"]["pop_rank"] for c in chk["coverage"]]
assert ranks.count(1) == 1
print("OK updated=%s pulse=%d feed=%d coverage=%d alpha=%s benchmark=%s" % (chk["updated"], len(chk["pulse"]), len(chk["feed"]), len(chk["coverage"]), chk["score"]["alphaPts"], chk["score"]["benchmark"]))
print("pop_rank_1 =", [c["ticker"] for c in chk["coverage"] if c["projection"]["pop_rank"]==1])
