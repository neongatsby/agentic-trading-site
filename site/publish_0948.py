import json, os, datetime

SITE = "engine-data.json"
d = json.load(open(SITE))

TS = "2026-07-21T09:48:00-04:00"
d["updated"] = TS

# ---------- fresh day % moves (regular session, ~9:48 ET) ----------
chg = {"PLTR":-0.5,"AMD":5.0,"INTC":6.0,"NVDA":1.6,"VRT":2.7,"SOXL":12.1,"TQQQ":3.6,
       "CEG":1.4,"FNGU":1.2,"IONQ":1.4,"RKLB":1.3,"SQQQ":-3.5,"TSLA":1.6,"BE":9.7,"SMR":3.8}

# ---------- fresh projections (unique pop_rank 1..15) ----------
proj = {
 "AMD": {"target_pct":6.5,"confidence":"med","basis":"owned the pop; into 7/22-23 Advancing-AI event + MSFT Helios","pop_rank":1},
 "INTC":{"target_pct":6.5,"confidence":"med","basis":"High-NA EUV + Fortinet chip deal; earnings-Thu overhang","pop_rank":2},
 "SOXL":{"target_pct":11.0,"confidence":"low","basis":"biggest mover but gated 3x + fade-prone under 20-day","pop_rank":3},
 "NVDA":{"target_pct":3.0,"confidence":"med","basis":"confirmed the rally green; AI bellwether tell","pop_rank":4},
 "BE":  {"target_pct":8.0,"confidence":"low","basis":"dead-cat bounce off Mon TD-Cowen flush; not chasing","pop_rank":5},
 "PLTR":{"target_pct":0.5,"confidence":"med","basis":"RS leader but red on a chip-rotation day; live target","pop_rank":6},
 "VRT": {"target_pct":3.5,"confidence":"med","basis":"AI-datacenter power riding the chip bid","pop_rank":7},
 "TQQQ":{"target_pct":4.5,"confidence":"low","basis":"3x Nasdaq gated; tracks QQQ +1.3%","pop_rank":8},
 "SMR": {"target_pct":4.0,"confidence":"low","basis":"nuclear/SMR AI-power beta bouncing","pop_rank":9},
 "CEG": {"target_pct":2.5,"confidence":"med","basis":"held; nuclear-AI power, green","pop_rank":10},
 "IONQ":{"target_pct":3.0,"confidence":"low","basis":"quantum high-vol beta","pop_rank":11},
 "RKLB":{"target_pct":2.5,"confidence":"low","basis":"space beta consolidating","pop_rank":12},
 "FNGU":{"target_pct":3.0,"confidence":"low","basis":"3x gated FANG","pop_rank":13},
 "TSLA":{"target_pct":1.0,"confidence":"low","basis":"earnings Wed; lease hikes + robotaxi fears","pop_rank":14},
 "SQQQ":{"target_pct":-4.0,"confidence":"low","basis":"inverse hedge, trimmed to 100 sh","pop_rank":15},
}

for c in d["coverage"]:
    t = c["ticker"]
    if t in chg: c["chg_pct"] = chg[t]
    if t in proj: c["projection"] = proj[t]
    c["updated"] = "9:48a"

# ---------- targeted coverage rewrites ----------
def cov(t):
    for c in d["coverage"]:
        if c["ticker"]==t: return c
    return None

amd = cov("AMD")
amd["verdict"]="buy"; amd["verdict_label"]="Buy"
amd["thesis"]=("**Acted on the pop_rank-1 call - bought it as it confirmed post-open, no longer a premarket chase.** AMD is +5% into its 'Advancing AI 2026' event (7/22-23, San Francisco) on Microsoft's Helios rack-scale commitment - MI450/Instinct + EPYC Venice roadmap in focus. 1x = no gate issue, so it's the ownable chip leader where the 3x semis (SOXL +12%) are not. Bought 30 sh @ $527.80 in paper with a wide $458 GTC stop (below the 7/17 $460 structural low, -13%). Plan is to sell into strength if it runs into the event (buy-the-rumor risk on 7/22-23), stop does the work if the chip bid fades a 6th time.")
amd["hold_reason"]=("This was our top pop-pick all morning and it held green after the open, so we bought it rather than just watching it run. It's got a real forward catalyst - its big AI event is tomorrow - plus Microsoft's Helios deal landing days before. We're in 30 shares with a wide stop; if it runs into the event we take profits, and if the whole chip bounce fades again the stop protects us.")
amd["size"]="$15.9k paper (30 sh @ $527.80)"
amd["size_pct"]="~18% paper"
amd["size_note"]="bought 30 sh @ $527.80 on the post-open confirm; $458 GTC stop; live can't size a $528 share in the $810 sleeve"
amd["plan_usd"]="held 30 sh paper; sell into a 7/22-23 event pop, else the $458 stop works"
amd["horizon"]="swing"

sqqq = cov("SQQQ")
sqqq["thesis"]=("**The losing hedge, trimmed hard - it was the book's single biggest drag on a green tape.** SQQQ (-3.5% today, 3x inverse Nasdaq) bled every green session this week while QQQ ground up. Cut 210 of 310 sh @ ~$41.18 (~-$244 realized) and kept 100 sh as a reduced hedge into Wed's GOOGL/TSLA/INTC earnings wall - the regime gate is still shut (QQQ under its 20-day) so a small short stays as insurance, but camping the full size while the market rose was lazy money. $38 GTC stop on the residual.")
sqqq["hold_reason"]=("This is our downside insurance - it goes up when the Nasdaq falls. It's been losing money all week because the market kept grinding higher, so we cut most of it today and kept a small piece into Wednesday's big earnings (Google, Tesla, Intel). If the market keeps ripping the $38 stop takes us out; if those prints disappoint, the residual pays off.")
sqqq["size"]="$4.1k paper (100 sh, trimmed from 310)"
sqqq["size_pct"]="~5% paper"
sqqq["size_note"]="TRIMMED 310->100 sh today (~-$244 realized); $38 GTC stop on the residual"
sqqq["plan_usd"]="residual 100 sh hedge into Wed's earnings wall; cut fully if QQQ reclaims $716"

pltr = cov("PLTR")
pltr["size_note"]="paper 100 sh (stop $125); live PLTR buy still staged (ticket 2026-07-20-3, 5 sh, $122 stop) - approve anytime, fills now"
pltr["plan_usd"]="live ~$680 into PLTR - ticket 2026-07-20-3, approve = fills immediately (market open)"
pltr["hold_reason"]=("It's our clean 1x relative-strength leader - the AI-software name that kept making 2-week highs while software peers cracked. Today it's red as money rotates into chips, but that's a cheaper entry, not a broken thesis (no earnings until Aug 3). Paper owns 100 shares; the live buy is staged for approval. We stay in while it holds the low-$130s; the $125/$122 stops do the work if it doesn't.")

# ---------- status ----------
d["status"]=[
 {"session":"Open","text":"Bought AMD pop, cut SQQQ hedge"},
 {"session":"Regime","text":"Gate shut: QQQ under 20-day"},
 {"session":"Books","text":"Live cash; paper 5/5 stopped"},
]

# ---------- headlines ----------
d["headlines"]=[
 "Chip rally holds post-open and broadens: INTC +6.0%, AMD +5.0%, SOXL +12%, BE +9.7% - and NVDA finally confirms green +1.6% - on AMD's 7/22-23 Advancing AI event, Intel's High-NA EUV + Fortinet chip deal.",
 "Still gated: QQQ $705 is ~1.5% under its $716 20-day and SPY only +0.3% - a Nasdaq/chip-specific move, not broad risk-on - so the 3x-index gate holds (no SOXL/TQQQ).",
 "Engine action: trimmed the paper SQQQ hedge 310->100 sh (bleeding -3.5% on the green tape) and bought AMD 30 sh into its event - rotating the book into a real mover.",
 "Under the hood, Benzinga flags the momentum trade 'broke' (SPMO's worst month ever on the memory selloff) - why a small hedge stays on into Wed.",
 "Big Tech earnings wall: GOOGL + TSLA Wed 7/22 AMC, INTC Thu 7/23 - the residual SQQQ is insurance into it.",
 "PLTR the clean 1x RS leader (Aug-3 earnings, no gate) but -0.5% today, lagging the chip tape; the funded live buy stays staged for approval.",
 "Iran ceasefire hopes ease oil; NQ futures +1.3% on the chip bid + IREN's raised $4B AI-cloud guide.",
]

# ---------- pulse (prepend, keep 15) ----------
pulse_new = {
 "ts": TS,
 "text": ("9:48am, first post-open run - the open fork resolved GREEN. NVDA confirmed the chip rally (+1.6%), breadth is broad (AMD +5%, INTC +6%, BE +9.7%) and QQQ +1.3% is holding well above Monday's $696 - so I stopped babysitting the losing SQQQ hedge (-3.5%, the book's #1 drag) and acted on the AMD pop I called pop_rank-1 all morning. PAPER: trimmed SQQQ 310->100 (~-$244 realized, keep a small hedge into Wed's earnings wall) and bought AMD 30 sh @ $527.80 into its 7/22-23 event, $458 stop. Both books zero-naked. LIVE: PLTR buy still staged for approval (1x RS leader, red = cheap; can't cleanly size a $528 AMD share in the $810 sleeve). Capture's still low intraday - SOXL +12%/BE +9.7% are gated/dead-cat un-ownables - but the book is finally IN a real mover. Day-trade budget 0/3."),
 "hype": ("Stopped babysitting the losing short and finally bought the AMD pop I've called all week - the book's in a real mover now. Kept a small hedge for Wednesday's earnings, wide stops on everything.")
}
d["pulse"] = [pulse_new] + d["pulse"]
d["pulse"] = d["pulse"][:15]

# ---------- feed (prepend trade cards, keep 40) ----------
feed_new = [
 {"ts":TS,"type":"trade","side":"buy","status":"filled","symbol":"AMD","detail":"30 sh @ $527.80",
  "reaction":"rotate",
  "text":"Bought AMD - 30 sh @ $527.80 (paper). Acting on the pop_rank-1 call: +5% into its 7/22-23 Advancing AI event, 1x (no gate), $458 GTC stop below the $460 structural low. The ownable chip leader where SOXL (3x) is gated."},
 {"ts":TS,"type":"trade","side":"sell","status":"filled","symbol":"SQQQ","detail":"210 sh @ ~$41.18",
  "reaction":"rotate",
  "text":"Trimmed the SQQQ hedge 310->100 sh (~-$244 realized). It was -3.5% and the book's biggest drag on a green tape - stopped camping the losing short, kept 100 sh as insurance into Wed's GOOGL/TSLA/INTC prints. $38 GTC stop on the residual."},
 {"ts":TS,"type":"activity",
  "text":"9:48am open fork resolved GREEN: NVDA confirmed (+1.6%), breadth broad (AMD +5%, INTC +6%, BE +9.7%), QQQ +1.3% holding above Monday's $696. Rotated paper toward capture - cut the losing hedge, bought the AMD pop. Live PLTR buy still staged. 3x-index gate still shut (QQQ < $716); no SOXL/TQQQ chase. 0/3 day-trades."},
]
d["feed"] = feed_new + d["feed"]
d["feed"] = d["feed"][:40]

# ---------- accountability (running, intraday - HONEST) ----------
d["accountability"]={
 "date":"2026-07-21","final":False,"grade":"running (~C, intraday)",
 "headline":("First post-open run: acted on the open fork - cut the losing SQQQ hedge (-3.5%, the book's biggest drag) and bought the AMD pop_rank-1 I called all morning (+5%, into its 7/22-23 event), so the book is finally IN a real mover. But capture is still low right now: the day's two biggest watchlist movers - SOXL +12% and BE +9.7% - are structurally un-ownable (SOXL is the gated 3x; BE a negative-catalyst dead-cat bounce off Monday's TD Cowen flush), and the residual SQQQ + red PLTR keep paper ~flat (-0.16%) while live sits in cash (0%) awaiting the PLTR tap. The rotation is right and early (the 7/20 D-fix in motion), but the un-ownable movers cap today's ceiling. Final grade at the close."),
 "capture":{"bestName":"SOXL (gated 3x) / BE (dead-cat)","bestPct":"+12.1% / +9.7%","capturedPct":"paper -0.16%, live 0%","rate":"~0% intraday - best movers un-ownable; AMD +5% now owned"},
 "missed":[
   {"from":"paper SQQQ hedge","to":"AMD (pop_rank-1)","note":"cut the losing hedge and bought AMD on the 9:47 confirmation rather than at the 9:31 bell - gave up ~1% of AMD's open pop","delta":"~-$150 on 30 sh"}
 ],
 "saved":[
   {"note":"Held the 3x-index gate a 6th day - did NOT chase SOXL +12%/TQQQ +3.6% under a sub-20-day QQQ (the pop that's round-tripped 5 sessions running)","delta":"discipline intact"},
   {"note":"Trimmed the SQQQ hedge that was -3.5% and the book's single biggest drag, instead of camping it another session","delta":"stopped the bleed, freed ~$8.6k"}
 ],
 "best":{"name":"AMD (bought 30 sh @ $527.80)","note":"acted on the pop_rank-1 call - into its 7/22-23 event with momentum, 1x (no gate), wide $458 stop","delta":"+5% and owned"},
 "worst":{"name":"SQQQ hedge","note":"the week's losing bet - trimmed today at ~-$244 realized on 210 sh; arguably should've been cut a session earlier","delta":"-$244 realized"},
 "avoided":{"worstName":"gated 3x chip chase (SOXL +12% / TQQQ +3.6%)","worstPct":"TBD at close","note":"the gate kept both books out of the leveraged-index pop that's faded 5 sessions running under the 20-day","amount":"pending the close","rate":"high on any gated chase"},
 "applying":"PLAYBOOK Earned Rule #1 (regime gate - no 3x-index long under the 20-day) + the 7/20 D-fix 'rotate EARLY': cut the dead hedge and added the ownable 1x leader (AMD) in the MORNING, not at 3pm.",
 "adjust":"If the chip bid holds into the afternoon and QQQ presses $716, add a 2nd 1x leader (NVDA) with paper powder and cut the last SQQQ; if it fades back under $700, the residual hedge + wide AMD stop do the work. Watch the AMD event (7/22-23) for a sell-into-strength exit."
}

# score: unchanged intraday (no new LIVE close; recompute at post-close). Note TQQQ bounced +3.6% today.
# pending_tickets: keep PLTR ticket 2026-07-20-3 (staged, ready to fire now).

# ---------- atomic write + backup ----------
bak = "engine-data.backup-2026-07-21-0948.json"
with open(bak,"w") as f: json.dump(d,f,indent=1,ensure_ascii=False)
tmp = SITE+".tmp"
with open(tmp,"w") as f: json.dump(d,f,indent=1,ensure_ascii=False)
os.replace(tmp, SITE)
print("WROTE", SITE, "and", bak)
