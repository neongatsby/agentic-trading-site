#!/usr/bin/env python3
"""Publish engine-data.json — 2:20pm ET run 2026-07-20. Atomic write + os.replace."""
import json, os, tempfile

SITE = "/sessions/amazing-affectionate-johnson/mnt/movita-backend/agentic-trading-site/site"
P = os.path.join(SITE, "engine-data.json")
TS = "2026-07-20T14:20:00-04:00"

d = json.load(open(P))

# ---- pulse (prepend one) ----
pulse_text = ("2:20pm: Made the ROTATION the charter's been nagging about instead of holding flat a 6th time. "
 "LIVE: sharpened the BE-cut ticket - it's no longer just a broken chart, TD Cowen flagged MEANINGFUL DELAYS "
 "at BE's two largest data-center projects today, hitting the exact growth story we were holding into 7/28 for. "
 "BE is -3.7% to fresh 90-day lows on a GREEN tape (Nasdaq +0.8%, chips rebounding, MU +5%) = sellers own it; "
 "cutting into the $195->$206 bounce frees ~$620 to rotate live into the confirmed leader PLTR next run. "
 "PAPER: put idle cash to work - DOUBLED PLTR 50->100 sh @ $135.75 (it's +2.9% at a fresh 2-wk high, bucking BOTH "
 "the chip fade AND the ORCL/NOW/ADBE software selloff - our pop_rank 1) and re-armed the $125 GTC stop; kept the "
 "SQQQ hedge on. 5/5 stops verified, zero naked, ~$40k paper powder + $201 live dry. Gate still SHUT (QQQ $701, "
 "-2.2% under its $716 20-day). Next: BE tap -> live PLTR/NVDA; QQQ reclaims $716 -> add the gated names back. Day-trade 0/3.")
pulse_hype = ("Doubled PLTR in paper - it's the one thing climbing while chips and software both wobble. "
 "And I sharpened the Bloom sell after TD Cowen flagged delays at its two biggest data-center projects - "
 "rather hold that as broken and free the cash for what's working.")
d["pulse"] = [{"ts": TS, "text": pulse_text, "hype": pulse_hype}] + d.get("pulse", [])
d["pulse"] = d["pulse"][:15]

# ---- status (3 cards) ----
d["status"] = [
 {"session": "Morning", "text": "QQQ held $698, bounced; gate ON"},
 {"session": "Afternoon", "text": "Doubled PLTR paper; BE cut staged"},
]

# ---- headlines ----
d["headlines"] = [
 "QQQ ~$701 bounced off its $698 low but sits ~2.2% under its 20-day ($716); SPY near record highs - derate stays chip/tech-specific",
 "Chips rebound off the lows - Micron +5%, SOXL back to +5% off a +10% open; AMD +4% into its 'Advancing AI' event with 6 analyst PT raises",
 "TD Cowen flags meaningful delays at two of Bloom Energy's largest data-center projects - BE -3.7% at fresh 90-day lows on a green tape",
 "Enterprise software cracks: Oracle -4% on debt / AI-capex / OpenAI-credit fears - but PLTR bucks it, +2.9% to a fresh 2-week high",
 "Iran conflict escalates - continued US airstrikes; oil wavers ~$81",
 "Fed Board of Governors holds a closed meeting at 3:30pm ET",
 "Earnings week: GOOGL, TSLA, INTC, TXN Wed-Thu; BE 7/28, VRT 7/29",
 "Apple briefly overtook NVIDIA as the world's most valuable company",
]

# ---- coverage (15 names, refreshed) ----
d["coverage"] = [
 {"ticker":"PLTR","name":"Palantir","theme":"AI software / RS leader","verdict":"buy","verdict_label":"Buy","chg_pct":2.9,
  "thesis":"**THE confirmed relative-strength leader - and the one name working.** PLTR is +2.9% to a fresh 2-week high, breaking out while BOTH the chip complex fades (SOXL +10%->+5%) AND enterprise software cracks (ORCL/NOW/ADBE -4%). That's textbook RS: green when its neighbors are red. It's a 1x stock (no gate issue) so we own it aggressively - DOUBLED paper 50->100 sh @ $135.75 this run and it's the live redeploy target the moment the BE cut frees cash.",
  "hold_reason":"PLTR is the account's RS anchor - the cleanest thing bucking a weak tape, so we just doubled the paper position (100 sh, $125 GTC stop) and it's where freed LIVE cash goes next. We hold while it makes higher lows and holds the $130 breakout base; we'd trim if it loses ~$130 or the AI-software bid rolls over.",
  "size":"$13.6k paper (100 sh)","size_pct":"~15% paper","size_note":"doubled this run; live redeploy target on the BE cut","plan_usd":"live ~$680 into PLTR once BE frees cash",
  "updated":TS,"horizon":"swing",
  "projection":{"target_pct":3.8,"confidence":"high","basis":"1x RS leader, fresh 2-wk high, bucking chip+software fade","pop_rank":1,"path_pct":[3.0,3.4,3.8]}},

 {"ticker":"AMD","name":"Advanced Micro Devices","theme":"AI chips / Advancing AI event","verdict":"watch","verdict_label":"Watch","chg_pct":4.0,
  "thesis":"**Today's catalyst mover: AMD +4% into its 'Advancing AI' event, with 6 Wall Street firms raising price targets** on top of the MSFT Helios data-center win. A real forward catalyst + momentum is our setup - BUT it already ran (476->522) and it's a chip, the exact group the gate says don't chase while QQQ is under its 20-day. Watch for a pullback/reclaim rather than chasing the HOD.",
  "hold_reason":"","size":"-","size_pct":"-","size_note":"Not owned - real forward catalyst (Advancing AI) but chip-gated + extended; want a pullback, not the HOD.","plan_usd":"$0 (watch)",
  "updated":TS,"horizon":"swing",
  "projection":{"target_pct":4.5,"confidence":"med","basis":"Advancing AI event + 6 PT raises; but extended + chip-gated","pop_rank":2}},

 {"ticker":"NVDA","name":"NVIDIA","theme":"AI leader / 1x bellwether","verdict":"buy","verdict_label":"Buy","chg_pct":0.9,
  "thesis":"**Held in paper (90 sh @ $209.23, $186 GTC stop) - the gate-compliant 1x way to own the AI tape.** NVDA +0.9%, holding RS above $203 while chips chop; Bristol Myers just adopted its DGX SuperPOD (another enterprise-AI proof point). It's the #2 live/paper redeploy magnet behind PLTR on a confirmed QQQ $716 reclaim. Own it 1x, don't lever it under the 20-day.",
  "hold_reason":"NVDA is the cleanest 1x AI-compute hold with no near-term earnings binary (late-Aug), so it's a redeploy magnet. We hold 90 paper shares behind a wide $186 GTC stop; add on a QQQ $716 reclaim, trim if it loses ~$198 or the AI-capex story cracks.",
  "size":"$18.4k paper (90 sh)","size_pct":"~21% paper","size_note":"held; adds on a $716 reclaim","plan_usd":"add on a QQQ $716 reclaim",
  "updated":TS,"horizon":"swing",
  "projection":{"target_pct":1.3,"confidence":"med","basis":"1x AI bellwether, RS but capped under the 20-day; GOOGL Wed","pop_rank":3}},

 {"ticker":"INTC","name":"Intel","theme":"Turnaround / Q2 earnings this week","verdict":"watch","verdict_label":"Watch","chg_pct":3.7,
  "thesis":"**+3.7% and holding, on its Q2 earnings this week + a Google Cloud AI partnership.** A real ownable 1x catalyst name that's held its gains - but it's already run two days and reports mid-week, so chasing it here risks the 7/17 top-tick mistake. Watch into the print.",
  "hold_reason":"","size":"-","size_pct":"-","size_note":"Not owned - real earnings catalyst but extended into a mid-week print; a logged capture miss, not a chase-now.","plan_usd":"$0 (watch)",
  "updated":TS,"horizon":"swing",
  "projection":{"target_pct":4.0,"confidence":"low","basis":"Q2 earnings + Google Cloud, but extended pre-print","pop_rank":4}},

 {"ticker":"VRT","name":"Vertiv","theme":"Data-center power / earnings 7/29","verdict":"watch","verdict_label":"Watch","chg_pct":1.8,
  "thesis":"**+1.8%, the data-center-cooling/power play into 7/29 earnings.** Recovered off last week's washout with the AI-infra bid; a 1x way to own the buildout that doesn't depend on the chips themselves. Watch for a base + a QQQ reclaim before committing ahead of the print.",
  "hold_reason":"","size":"-","size_pct":"-","size_note":"Not owned - AI-infra catalyst (7/29) but wait for a base + regime confirm.","plan_usd":"$0 (watch)",
  "updated":TS,"horizon":"swing",
  "projection":{"target_pct":2.5,"confidence":"med","basis":"data-center power bid; 7/29 earnings ahead","pop_rank":5}},

 {"ticker":"SOXL","name":"Direxion Semi Bull 3x","theme":"3x semis / gated leverage","verdict":"avoid","verdict_label":"Avoid","chg_pct":5.2,
  "thesis":"**Biggest raw mover, but GATED.** SOXL ripped +10% at the open and gave back half to ~+5% - the 'chip pop sells by lunch' pattern that's held all week. It's a 3x-long the gate bars while QQQ is under its 20-day; we don't touch it. Its fade is the confirmation our SQQQ hedge is positioned right.",
  "hold_reason":"Not held and gated - a 3x semi long the regime gate bars under a sub-20-day QQQ. Its round-trip off a +10% open is exactly the bull-trap we're avoiding.","size":"0 (avoid)","size_pct":"0%","size_note":"Gated 3x-long; re-lever candidate only on a QQQ $716 reclaim.","plan_usd":"-",
  "updated":TS,"horizon":"flat",
  "projection":{"target_pct":3.0,"confidence":"low","basis":"biggest raw mover but gated 3x; round-tripped +10%->+5%","pop_rank":6}},

 {"ticker":"SQQQ","name":"ProShares -3x QQQ","theme":"Inverse hedge (paper)","verdict":"hold","verdict_label":"Hedge","chg_pct":-2.3,
  "thesis":"**The deliberate paper hedge (310 sh @ $42.36, $38 GTC stop).** Down -2.3% today as QQQ bounced off $698 - the expected drag on a green day. We hold it as insurance while QQQ is under its 20-day with Iran + software cracking; it's the paid-off side only if $698 breaks. Per plan we CUT it fast on a QQQ $716 reclaim, not before.",
  "hold_reason":"SQQQ is our sub-20-day / Iran insurance in paper - it bleeds on green days by design. We hold while QQQ is under $716; a confirmed $698 break makes it pay, a $716 reclaim is the signal to cut it fast and flip the cash into PLTR/NVDA.",
  "size":"$12.9k paper (310 sh)","size_pct":"~14% paper","size_note":"held hedge; cut on a $716 reclaim","plan_usd":"cut on a QQQ $716 reclaim",
  "updated":TS,"horizon":"swing",
  "projection":{"target_pct":-2.5,"confidence":"med","basis":"inverse; stays red while QQQ holds $698 and grinds up","pop_rank":10}},

 {"ticker":"TQQQ","name":"ProShares 3x QQQ","theme":"3x Nasdaq / gated / benchmark","verdict":"avoid","verdict_label":"Avoid","chg_pct":2.3,
  "thesis":"**Our benchmark and a re-lever candidate - gated for now.** TQQQ +2.3% with the bounce but QQQ is still under its 20-day, so the gate keeps us out (this is the exact exposure that drove the -14.6% week). Re-lever ONLY on a confirmed $716 reclaim on volume.",
  "hold_reason":"Not held - gated 3x-index long and the buy-and-hold benchmark. The gate keeps leveraged capital out until QQQ reclaims its 20-day on volume.","size":"0 (avoid)","size_pct":"0%","size_note":"Gated; re-lever only on a confirmed $716 reclaim.","plan_usd":"-",
  "updated":TS,"horizon":"flat",
  "projection":{"target_pct":2.0,"confidence":"low","basis":"3x Nasdaq, gated under the 20-day","pop_rank":9}},

 {"ticker":"CEG","name":"Constellation Energy","theme":"Nuclear / AI-power","verdict":"hold","verdict_label":"Hold","chg_pct":0.7,
  "thesis":"**Held in paper (16 sh @ $260.68, $236 GTC stop) - the defensive AI-power anchor.** CEG +0.7%, the kind of low-beta nuclear/data-center-power name that holds up when high-beta chops. Quiet hold behind its stop; not adding, not cutting.",
  "hold_reason":"CEG is our defensive AI-power hold - nuclear supply into data-center demand, lower beta than the chips. We hold 16 paper shares behind a $236 GTC stop; it's a steady anchor, cut only if it loses $236 or a better setup needs the capital.",
  "size":"$4.1k paper (16 sh)","size_pct":"~5% paper","size_note":"held anchor","plan_usd":"hold",
  "updated":TS,"horizon":"swing",
  "projection":{"target_pct":1.0,"confidence":"low","basis":"low-beta AI-power; steady in a choppy tape","pop_rank":8}},

 {"ticker":"FNGU","name":"MicroSectors FANG+ 3x","theme":"3x mega-cap tech / gated","verdict":"avoid","verdict_label":"Avoid","chg_pct":3.1,
  "thesis":"**+3.1% with the mega-cap bid, but gated 3x.** FANG+ leverage the gate bars under a sub-20-day QQQ. A re-lever candidate on a $716 reclaim, not before.",
  "hold_reason":"Not held - gated 3x mega-cap long. Same regime gate as TQQQ/SOXL.","size":"0 (avoid)","size_pct":"0%","size_note":"Gated 3x; re-lever only on a $716 reclaim.","plan_usd":"-",
  "updated":TS,"horizon":"flat",
  "projection":{"target_pct":2.5,"confidence":"low","basis":"3x FANG+, gated under the 20-day","pop_rank":11}},

 {"ticker":"IONQ","name":"IonQ","theme":"Quantum / high-beta","verdict":"watch","verdict_label":"Watch","chg_pct":0.8,
  "thesis":"**+0.8%, steadying with the risk names.** Quantum high-beta that whipsaws with the tape; no catalyst today. Watch only - a QQQ reclaim would be the tell for the high-beta cohort.",
  "hold_reason":"","size":"-","size_pct":"-","size_note":"Not owned - high-beta watch, no catalyst; needs a regime turn.","plan_usd":"$0 (watch)",
  "updated":TS,"horizon":"swing",
  "projection":{"target_pct":1.5,"confidence":"low","basis":"quantum high-beta, tracks the tape; no catalyst","pop_rank":12}},

 {"ticker":"RKLB","name":"Rocket Lab","theme":"Space / high-beta","verdict":"watch","verdict_label":"Watch","chg_pct":0.5,
  "thesis":"**+0.5%, holding last week's level.** Space high-beta that ran hard then based; no fresh catalyst. Watch for a breakout on a broad-tape green light.",
  "hold_reason":"","size":"-","size_pct":"-","size_note":"Not owned - based after a big run; watch for a catalyst + regime turn.","plan_usd":"$0 (watch)",
  "updated":TS,"horizon":"swing",
  "projection":{"target_pct":1.5,"confidence":"low","basis":"space high-beta, based; no catalyst today","pop_rank":13}},

 {"ticker":"TSLA","name":"Tesla","theme":"High-beta / earnings Wed","verdict":"watch","verdict_label":"Watch","chg_pct":-1.8,
  "thesis":"**-1.8%, the red one - faded from $386 to $374 into Wed earnings.** High-beta laggard today; the print Wed is the binary. No position; watch the reaction, don't pre-position into the gap.",
  "hold_reason":"","size":"-","size_pct":"-","size_note":"Not owned - weak today; earnings-binary Wed, watch the reaction.","plan_usd":"$0 (watch)",
  "updated":TS,"horizon":"swing",
  "projection":{"target_pct":-1.5,"confidence":"low","basis":"faded into Wed earnings binary; weakest mega-cap today","pop_rank":14}},

 {"ticker":"SOXS","name":"Direxion Semi Bear 3x","theme":"Inverse semis","verdict":"avoid","verdict_label":"Avoid","chg_pct":-5.8,
  "thesis":"**-5.8% as chips rebounded - the mirror of SOXL.** We hedge via SQQQ, not SOXS (semi-inverse is more volatile). Only relevant if a confirmed chip breakdown resumes; not touched.",
  "hold_reason":"Not held - we express downside via SQQQ, not the more-volatile semi-inverse. Watch only on a confirmed chip breakdown.","size":"0 (avoid)","size_pct":"0%","size_note":"Downside expressed via SQQQ instead.","plan_usd":"-",
  "updated":TS,"horizon":"flat",
  "projection":{"target_pct":-4.0,"confidence":"low","basis":"inverse semis; bleeds as chips rebound","pop_rank":15}},

 {"ticker":"BE","name":"Bloom Energy","theme":"Fuel cells / CUTTING","verdict":"sell","verdict_label":"Sell","chg_pct":-3.7,
  "thesis":"**CUTTING - now a broken chart AND a fresh fundamental crack.** TD Cowen flagged meaningful delays at BE's two largest data-center projects today - a direct hit to the growth story that was the only reason to hold into 7/28. BE is -3.7% to fresh 90-day lows ($195) on a GREEN tape; the $195->$206 bounce is a dead-cat. It's the entire live book from a bad top-tick entry ($222.64, -7%). The $188 stop can't protect a 7/28 gap. Cut ticket staged for the tap; frees ~$620 to rotate into PLTR.",
  "hold_reason":"We're cutting BE, not holding it. It's the accidental all-in live position from a top-tick entry, now down -7% with a broken chart and - as of today - a TD Cowen note flagging delays at its two biggest data-center projects. Selling into the bounce (~$206 vs the $195 low) frees the cash to rotate into the confirmed leader; we keep the option to re-enter with defined risk near 7/28 if it stabilizes.",
  "size":"$0.6k live (3 sh)","size_pct":"~75% live","size_note":"CUT staged (ticket 2026-07-20-1) - frees ~$620 to rotate into PLTR","plan_usd":"sell-to-close ~$620",
  "updated":TS,"horizon":"exit",
  "projection":{"target_pct":-3.0,"confidence":"med","basis":"broken chart + fresh TD Cowen data-center-delay note; dead-cat bounce","pop_rank":7}},
]

# ---- feed (prepend trade + activity) ----
new_feed = [
 {"ts":TS,"type":"trade","side":"buy","symbol":"PLTR","status":"filled","reaction":"rotate",
  "detail":"50 sh paper @ $135.75 -> 100 sh",
  "text":"Doubled the winner. PLTR's the only name bucking BOTH the chip fade and the ORCL/NOW/ADBE software selloff (+2.9%, fresh 2-wk high, my pop_rank 1), so I put idle paper cash to work - 50->100 sh, re-armed the $125 GTC stop. The anti-camping move: lazy cash into the confirmed leader, SQQQ hedge still on."},
 {"ts":TS,"type":"activity",
  "text":"2:20pm rotation: sharpened the BE cut on a FRESH catalyst - TD Cowen flagged meaningful delays at Bloom's two largest data-center projects, exactly the growth story we held into 7/28 for; BE -3.7% to fresh 90-day lows on a green tape. Cut staged for your tap, frees ~$620 to rotate live into PLTR. Doubled PLTR paper 50->100. 5/5 stops verified GTC, zero naked. Gate still SHUT (QQQ $701, -2.2% under its $716 20-day). Day-trade 0/3."},
] + d.get("feed", [])
d["feed"] = new_feed[:40]

# ---- score ----
d["score"] = {"alphaPts":"-12.2","benchmark":"-5.9%","bestDay":"+3.2%",
 "bestDayName":"Day 9 - CPI chip rally (settled)","winRate":"40%","tradeCount":5}

# ---- accountability (running) ----
d["accountability"] = {
 "date":"2026-07-20","final":False,"grade":"C (running)",
 "headline":"Finally ROTATED instead of holding flat a 6th time: doubled the one working name (PLTR +2.9%, our pop_rank 1, bucking both the chip fade AND the software selloff) in paper, and sharpened the BE cut on a REAL fresh catalyst - TD Cowen flagged delays at Bloom's two largest data-center projects, hitting the exact growth story we were holding for. Capture today is still low - live is 100% in BE (-3.7%, the day's WORST watchlist name) until the cut fills - but the fix is now in MOTION, not just journaled: BE cut staged + PLTR doubled + live redeploy on deck. Gate stays SHUT (QQQ -2.2% under its 20-day) so no chase of the +10%->+5% SOXL round-trip.",
 "capture":{"bestName":"SOXL","bestPct":"+5.2% (3x - GATED)",
  "capturedPct":"live -3.2% / paper ~-0.9% (provisional)",
  "rate":"low - live is 100% in BE (-3.7%, the WORST watchlist name) so its capture is deeply negative; paper OWNS PLTR +2.9% (best held 1x, our pop_rank 1 - IN it) but the SQQQ hedge offsets. Best raw mover SOXL +5.2% is gated 3x (correctly skipped); best ownable-but-unheld 1x = AMD +4.0% / INTC +3.7%."},
 "missed":[
  {"from":"BE (broken camp)","to":"PLTR / AMD","note":"Live sat 100% in BE (-3.7%) while PLTR +2.9% and AMD +4% ran - the exact capture failure. FIXED this run: BE cut sharpened on the TD Cowen delay note + staged; PLTR doubled in paper; live redeploy into PLTR fires once the cut frees cash.","delta":"rotation now in motion, not just noted"},
  {"from":"n/a","to":"SOXL +5.2% / FNGU +3.1% / TQQQ +2.3%","note":"biggest raw movers but gated 3x under the 20-day; SOXL round-tripped from a +10% open, so the gate dodged the chase again","delta":"low-capture cost, accepted"}],
 "saved":[
  {"note":"Deployed idle paper cash into the CONFIRMED 1x RS leader (PLTR, doubled 50->100) rather than a gated chip name - the one thing bucking both the chip AND software fade","delta":"capture on what's actually working"},
  {"note":"Acted on a FRESH fundamental catalyst - TD Cowen's BE data-center-delay note - to sharpen the cut, vs holding a freshly-downgraded broken chart on stop-hope into 7/28","delta":"de-risks the accidental all-in on real news"},
  {"note":"Held the regime gate - no chase of the gated 3x semis that round-tripped from a +10% open (SOXL +10%->+5%)","delta":"avoided the week's signature bull-trap"},
  {"note":"5/5 stops verified GTC through the add (PLTR re-armed on 100 sh @ $125), zero naked","delta":"never-naked held"}],
 "best":{"name":"PLTR (paper, doubled)","note":"+2.9% to a fresh 2-wk high, the cleanest RS leader bucking BOTH the chip fade and the ORCL/NOW/ADBE software selloff - our pop_rank 1, now doubled 50->100","delta":"the RS anchor, sized up"},
 "worst":{"name":"BE (cutting)","note":"-3.7% to fresh 90-day lows on a green tape + a TD Cowen data-center-delay note - a broken chart with a freshly-cracked fundamental; the accidental all-in that's dragged live all week","delta":"~-$27 live today"},
 "avoided":{"worstName":"SOXL/chip open-chasers","worstPct":"+10%->+5% (a ~-5% round-trip)","note":"the gate kept us out of the +10% gated 3x-semi open pop that gave back half - the textbook bull-trap","amount":"avoided ~-5% on any chase slug","rate":"high"},
 "applying":"Charter v5 ACTIVE-ROTATION + the regime gate: stop camping the broken live name (cut BE on the TD Cowen catalyst, sell into the $206 bounce not the $195 low), deploy lazy cash into the CONFIRMED 1x RS leader (doubled PLTR paper), keep the gated 3x + the live redeploy waiting on confirmation (QQQ $716 reclaim / BE cash freed).",
 "adjust":"Finish the rotation: once Adam taps the BE cut, next run fire the freed ~$820 into PLTR/NVDA (multi-day swing, PDT-free) so LIVE finally owns the leader, not the laggard. Stay hair-trigger on QQQ $716 (reclaim -> cut SQQQ, add gated names back) and $698 (loses it -> press the fade, arm a small live SQQQ). Capture's been ~0 a week - the fix is getting live OUT of dead camps and INTO the RS leader, now in motion."
}

# ---- pending_tickets ----
d["pending_tickets"] = [
 {"id":"2026-07-20-1","symbol":"BE","side":"sell","size":"$620","qty":3,
  "entry":"~$206 market sell-to-close (approve = sell now; $200 floor)","trigger":None,"stop":None,
  "bracket":"n/a - sell-to-close; the fast-lane cancels the $188 GTC stop (b2b62cc5) first, then sells",
  "thesis":"Cut BE - now a broken chart AND a fresh fundamental crack. TD Cowen flagged MEANINGFUL DELAYS at BE's two largest data-center projects today, hitting the exact growth story that was the only reason to hold into 7/28. BE is -3.7% to fresh 90-day lows ($195) on a GREEN tape (chips rebounding, MU +5%); the $195->$206 bounce is a dead-cat. It's the entire live book from a top-tick entry ($222.64, -7%), an accidental all-in. A $188 stop can't protect a binary 7/28 gap. Selling into THIS bounce frees ~$620 (-> ~$820 live cash) to rotate into the confirmed 1x RS leader PLTR (green +2.9%, fresh 2-wk high, bucking chip+software - our pop_rank 1, doubled in paper). Multi-day exit - burns 0 PDT day-trade budget (0/3). Paper already cut BE @ $196.68."}
]

# ---- live / paper blocks ----
d["live"]["equity"] = 818.87
d["live"]["cash"] = 201.26
d["live"]["positions"] = 1
d["live"]["updated"] = TS
d["live"]["equity_note"] = ("Live -3.2% today (~$819). BE ~$206, -3.7% at fresh 90-day lows + a TD Cowen data-center-delay note - "
 "the accidental all-in from a top-tick entry; $188 GTC stop live, BE-cut ticket staged for your tap (frees ~$620 -> rotate into PLTR). "
 "$201 cash dry. -18.1% since $1,000 inception.")
for pt in d["live"]["equity_curve"]:
    if pt["date"] == "Jul 20": pt["value"] = 818.87

d["paper"]["equity"] = 89624.14
d["paper"]["updated"] = TS
d["paper"]["equity_note"] = ("Paper ~-0.9% today (provisional; PLTR/NVDA/CEG green, SQQQ hedge the deliberate drag). ROTATED idle cash into the leader: "
 "DOUBLED PLTR 50->100 sh @ $135.75 ($125 GTC stop), the RS name bucking both the chip fade and the software selloff. "
 "4 names all GTC-stopped, zero naked; ~$40.5k (~45%) powder held for a QQQ $716 reclaim (add gated names back) or $698 break.")
for pt in d["paper"]["equity_curve"]:
    if pt["date"] == "Jul 20": pt["value"] = 89624.14

d["updated"] = TS

# ---- atomic write ----
fd, tmp = tempfile.mkstemp(dir=SITE, suffix=".tmp")
with os.fdopen(fd, "w") as f:
    json.dump(d, f, ensure_ascii=False, indent=1)
os.replace(tmp, P)

# verify
d2 = json.load(open(P))
assert d2["updated"] == TS
assert len(d2["coverage"]) == 15
ranks = sorted(c["projection"]["pop_rank"] for c in d2["coverage"])
assert ranks[0] == 1 and ranks.count(1) == 1, f"pop_rank1 issue: {ranks}"
assert d2["pending_tickets"][0]["id"] == "2026-07-20-1"
print("PUBLISH-1420-OK")
print("coverage:", len(d2["coverage"]), "| pop_rank1:", [c["ticker"] for c in d2["coverage"] if c["projection"]["pop_rank"]==1])
print("pulse[0].ts:", d2["pulse"][0]["ts"], "| feed len:", len(d2["feed"]))
print("live eq:", d2["live"]["equity"], "| paper eq:", d2["paper"]["equity"])
print("grade:", d2["accountability"]["grade"])
