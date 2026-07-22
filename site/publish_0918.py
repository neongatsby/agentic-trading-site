import json, os, datetime

SITE="engine-data.json"
TS="2026-07-22T09:18:00-04:00"
with open(SITE) as f: d=json.load(f)

# backup
bak="engine-data.backup-2026-07-22-0918.json"
with open(bak,"w") as f: json.dump(d,f,indent=1)

# ---- top-level updated ----
d["updated"]=TS

# ---- status ----
d["status"]=[{"session":"Pre-market","text":"OKLO armed for the open"}]

# ---- headlines ----
d["headlines"]=[
 "BINARY tonight: GOOGL + TSLA report after the close (IBM, TXN, ServiceNow, AT&T too) - the first Mag-7 AI-capex test; Alphabet's '26 capex guide is the number for our book",
 "DOE AI-energy summit TODAY: OKLO + X-Energy $200M nuclear-for-AI program details may drop - OKLO the lone watchlist green pre-open (+2%, pop_rank 1)",
 "Risk-off open: Nasdaq-100 futures lower, chips giving back the 2-day rip - SOXL -8.3%, MU -3.9%, AMD -2.7%, NVDA -0.9%",
 "LIVE pivot: staged the OKLO swing for the 9:30 open (16 sh, $39 stop) in place of the NVDA laggard - own the mover, end the cash camp",
 "QQQ ~$703 pre-market = ~-1.6% under its $714.7 20-day - 3x (SOXL/TQQQ) stays gated",
 "Oil elevated (~$95, Mideast tensions) capping otherwise-strong earnings; ~88% of S&P Q2 reporters beating",
 "RKLB +2.1% the other pre-open green; nuclear (SMR/CEG) firm into the DOE summit while semis fade",
]

# ---- coverage: per-ticker chg_pct + projection; full rewrites for OKLO & NVDA ----
chg={"NVDA":"-0.9%","AMD":"-2.7%","SMR":"-0.7%","MU":"-3.9%","BE":"-2.5%","OKLO":"+2.0%",
 "RGTI":"-1.0%","VRT":"-3.2%","IONQ":"-1.5%","RKLB":"+2.1%","CEG":"-0.8%","TSLA":"+0.2%",
 "SOXL":"-8.3%","TQQQ":"-3.1%"}
proj={
 "OKLO":{"target_pct":4.0,"confidence":"high","basis":"DOE AI-energy summit TODAY + base reclaim; RS leader","pop_rank":1},
 "SMR":{"target_pct":2.5,"confidence":"med","basis":"nuclear-for-AI sympathy on DOE summit day","pop_rank":2},
 "CEG":{"target_pct":1.0,"confidence":"med","basis":"nuclear utility bid; steady defensive leg","pop_rank":3},
 "RKLB":{"target_pct":2.5,"confidence":"med","basis":"space momentum green vs a red tape","pop_rank":4},
 "NVDA":{"target_pct":-0.5,"confidence":"med","basis":"laggard; AI-capex read-through to tonight's binary","pop_rank":5},
 "AMD":{"target_pct":-1.5,"confidence":"low","basis":"giving back 2-day rip; event digested, Aug print ahead","pop_rank":6},
 "VRT":{"target_pct":-2.0,"confidence":"low","basis":"data-center power giving back on risk-off open","pop_rank":7},
 "TSLA":{"target_pct":0.0,"confidence":"med","basis":"reports after close - the move is tonight","pop_rank":8},
 "IONQ":{"target_pct":-2.0,"confidence":"low","basis":"quantum high-beta; cools risk-off","pop_rank":9},
 "RGTI":{"target_pct":-2.0,"confidence":"low","basis":"quantum high-beta; sells risk-off tape","pop_rank":10},
 "BE":{"target_pct":-3.0,"confidence":"med","basis":"spent parabolic after +16%; give-back risk","pop_rank":11},
 "MU":{"target_pct":-3.5,"confidence":"med","basis":"giving back the +12.8% rip; extended","pop_rank":12},
 "TQQQ":{"target_pct":-3.0,"confidence":"low","basis":"3x Nasdaq powder; awaits 20-day reclaim","pop_rank":13},
 "SOXL":{"target_pct":-6.0,"confidence":"med","basis":"3x semis unwinding the rip; gate vindicated","pop_rank":14},
}
for c in d["coverage"]:
    t=c["ticker"]
    if t in chg: c["chg_pct"]=chg[t]
    if t in proj: c["projection"]=proj[t]
    c["updated"]=TS

def setc(t,**kw):
    for c in d["coverage"]:
        if c["ticker"]==t:
            c.update(kw); return
    raise SystemExit("ticker not found: "+t)

setc("OKLO",
 verdict="hold", verdict_label="Hold + live buy (staged for open)",
 thesis="**The watchlist's RS leader and the pop we called - the lone green name pre-open (+2%) while the 2-day semi rip gives back (SOXL -8%, MU -4%, NVDA -1%).** On a CONFIRMED, DATED catalyst: the Trump/DOE $200M program to fast-track nuclear reactors for AI data centers (OKLO + X-Energy, w/ MSFT/NVDA), with details possibly announced TODAY at a DOE AI-energy summit. Clean base reclaim off ~$40 (not extended), no earnings until Aug 18, insulated from tonight's GOOGL/TSLA binary. Now the LIVE swing (16 sh, $39 stop) - staged to fire at the open.",
 size="$9.0k (200 sh)", size_pct=10.1, size_note="Paper leg + the live swing pick",
 plan_usd="$720 live / held paper",
 hold_reason="Nuclear/AI-power name we own in paper (200 sh from ~$43.92, +2%, $39 stop) and are now buying LIVE. The catalyst is live and dated: the Trump/DOE $200M program to speed nuclear reactors for AI data centers (OKLO + X-Energy), with details possibly announced today at a DOE AI-energy summit. It's the lone watchlist name green pre-open while semis give back - the relative-strength tell. We'd sell if the summit disappoints and it loses the $41-42 base; the $39 stop is the line.",
 horizon="swing (multi-day)")

setc("NVDA",
 verdict="hold", verdict_label="Hold - paper core (laggard)",
 thesis="**The group's biggest laggard on the 2-day rip (+1.9% vs MU/AMD +8-12%), -0.9% pre-open - held in paper, no longer the live pick.** We pivoted the live swing to OKLO (the green RS leader on a dated catalyst) rather than own the laggard into tonight's GOOGL/TSLA capex binary, which NVDA reads through to. Still a solid paper core (140 sh, $186 stop); no own earnings until late Aug.",
 size="$28.8k (140 sh)", size_pct=32.3, size_note="Largest paper position - the anchor to trim at the open",
 plan_usd="held paper (trim toward the movers)",
 hold_reason="Our biggest paper position and the group's laggard - 140 sh from ~$208 (about flat), -0.9% pre-open. We read it as the catch-up name (Micron's HBM blowout reads through to NVDA GPUs), but at ~32% of the paper book it is the anchor we plan to trim at the open into the nuclear movers (the 'weight to the mover, not the anchor' lesson). No longer the live pick - we moved that to OKLO. The $186 stop is our line if the whole AI trade rolls over.",
 horizon="swing (multi-day)")

# ---- pulse (prepend, keep 15) ----
d["pulse"]=[{
 "ts":TS,
 "text":"9:18a pre-market (~12 min to open). Pivoted the live swing from the NVDA laggard to OKLO: fresh prints show chips giving back the 2-day rip (SOXL -8%, MU -4%, NVDA -1%) while OKLO is the ONE green name (+2%) on its confirmed Trump/DOE nuclear-for-AI catalyst - and there is a DOE AI-energy summit TODAY where the $200M program details may drop. Owning the pop_rank-1 RS leader (not the laggard) is the 7/21 'weight to the mover' fix, and it's insulated from tonight's GOOGL/TSLA binary. OKLO ticket 2026-07-22-1 (16 sh, $39 stop) staged to fill at the open - approve anytime; NVDA ticket retired. Paper: hold the 6/6-stopped book, trim the ~32% NVDA anchor into the movers AT the open (not into the pre-open low). LIVE flat $810 cash / 0 naked; PAPER ~$89k, 6/6 stopped.",
 "hype":"Swapped the live buy from NVDA to OKLO - it's the only green name this morning, on a government nuclear-for-AI catalyst with a summit this afternoon. Owning the mover, not the laggard; one tap fills it at the open."
}]+d["pulse"]
d["pulse"]=d["pulse"][:15]

# ---- feed (prepend activity, keep 40) ----
d["feed"]=[{
 "type":"activity","ts":TS,
 "text":"9:18a pre-market (~12 min to open). PIVOTED the live swing: retired the NVDA laggard ticket and staged OKLO 2026-07-22-1 (16 sh, marketable-limit $47, $39 GTC stop) to fire at the 9:30 open - approve anytime, PDT-free. Why: first real 7/22 prints show the 2-day semi rip giving back (SOXL -8.3%, MU -3.9%, AMD -2.7%, NVDA -0.9%) while OKLO is the lone green watchlist name (+2%) on its confirmed Trump/DOE $200M nuclear-for-AI catalyst, details possibly dropping TODAY at a DOE AI-energy summit - and it's insulated from tonight's GOOGL/TSLA Mag-7 binary. Owning the pop_rank-1 RS leader (not the laggard) is the 7/21 'weight to the mover' fix. Both books == broker, zero naked: LIVE flat $810.32 cash (0/3 day-trades); PAPER 6/6 GTC-stopped (~$89k). Paper NVDA-anchor->nuclear-mover trim executes AT the open (real prices, clean stop re-arm), not into the pre-open low."
}]+d["feed"]
d["feed"]=d["feed"][:40]

# ---- pending_tickets (replace with OKLO) ----
d["pending_tickets"]=[{
 "id":"2026-07-22-1","symbol":"OKLO","side":"buy","size":"$720","qty":16,
 "entry":"~$45 - approve ANYTIME -> fills at TODAY's (7/22) 9:30 open. Multi-day swing, PDT-free (0/3 day-trades). Marketable-limit $47 gives a gap-up cushion; a tap before 4pm fills immediately.",
 "trigger":None,"stop":39.0,
 "bracket":"stop $39 GTC (below this week's $40-41 base / the 7/17 $39.53 low, -13%)",
 "thesis":"Ends the live cash camp by owning the watchlist's ACTUAL RS leader (pop_rank 1), not the laggard. OKLO is the lone green name pre-open (+2%) on a confirmed, DATED catalyst - the Trump/DOE $200M nuclear-for-AI program (OKLO + X-Energy), details possibly at a DOE AI-energy summit TODAY. Base reclaim off ~$40, no earnings until Aug 18, insulated from tonight's GOOGL/TSLA binary. Wide $39 stop."
}]

# ---- accountability (running, pre-open) ----
a=d["accountability"]
a["date"]="2026-07-22"; a["final"]=False; a["grade"]="TBD (pre-open)"
a["headline"]="Pre-market (9:18a, ~12 min to open): PIVOTED the live swing from the NVDA laggard to OKLO - the pop_rank-1 RS leader and lone green name (+2%) on a confirmed, DATED DOE nuclear-for-AI catalyst (summit TODAY), insulated from tonight's GOOGL/TSLA binary. Retired the NVDA ticket, staged OKLO 2026-07-22-1 (16 sh, $39 stop) for the open. Both books re-reconciled clean, zero naked. This finally aims live at the mover, not the laggard - the 7/21 fix."
a["capture"]={"bestName":"TBD - pre-open (OKLO leads the watchlist +2% on the DOE nuclear-for-AI catalyst; summit today)","bestPct":"-","capturedPct":"-","rate":"pre-open"}
a["missed"]=[]
a["saved"]=[
 {"note":"Zero naked into the open - all 6 paper positions GTC-stopped (independently re-verified at the broker this run); live flat.","delta":"risk bounded"},
 {"note":"Gate keeping live OUT of 3x semis vindicated again pre-open - SOXL -8.3%, MU -3.9%, AMD -2.7% giving back the 2-day rip; OKLO the lone green.","delta":"fade dodged"}
]
a["best"]={"name":"-","note":"TBD (pre-open)","delta":"-"}
a["worst"]={"name":"-","note":"TBD (pre-open)","delta":"-"}
a["applying"]="Weight to the MOVER, not the anchor + be IN the pop you called (7/21 lesson): pivot the live swing from the NVDA laggard to OKLO - the pop_rank-1 RS leader on a dated catalyst - so live finally owns the mover, not a safety-blanket laggard. Wide $39 stop bounds it."
a["adjust"]="At the open, execute the paper trim of the ~32%-of-book NVDA anchor into the nuclear movers (OKLO/SMR) INTO strength with clean stop re-arms - not pre-open (avoids a naked window / blind auction fill). No fresh semi size into tonight's GOOGL/TSLA binary."

# ---- live block ----
d["live"]["equity"]=810.32
d["live"]["cash"]=810.32
d["live"]["positions"]=[]
d["live"]["updated"]=TS
d["live"]["equity_note"]="LIVE flat $810.32 cash / zero positions / zero naked (7th cash session pending the open). 1 staged ticket = BUY OKLO 16 sh (~$45, $39 stop, $720) set to fill at TODAY's 7/22 open - approve anytime. Pivoted from the retired NVDA laggard ticket to own the pop_rank-1 mover. Firing it is the plan's #1 action."

# ---- paper block ----
d["paper"]["equity"]=89020.31
d["paper"]["updated"]=TS
d["paper"]["equity_note"]="Paper ~$89.0k (pre-market mark) - OKLO +2% leading on the DOE nuclear catalyst offsets chips giving back the 2-day rip (NVDA/AMD/VRT/MU soft); 6/6 GTC-stopped, zero naked. Plan: trim the ~32%-of-book NVDA anchor into the nuclear movers (OKLO/SMR) at the open."

# ---- latest_recap ----
d["latest_recap"]="9:18a 7/22 pre-market (market CLOSED, opens 9:30). KEY ACTION: pivoted the LIVE swing from the NVDA laggard to OKLO. Fresh 7/22 prints show the 2-day semi rip giving back (SOXL -8.3%, MU -3.9%, AMD -2.7%, NVDA -0.9%, TQQQ -3.1%) while OKLO is the LONE green watchlist name (+2%) on its confirmed Trump/DOE $200M nuclear-for-AI catalyst (OKLO + X-Energy, w/ MSFT/NVDA) - and Bloomberg notes program details could be announced TODAY at a DOE AI-energy summit. Retired NVDA ticket 2026-07-21-1 (voided the queue file, archived to retired-...-superseded-by-oklo.json) and staged OKLO 2026-07-22-1 (16 sh, marketable-limit $47, $39 GTC stop, ~$720) to fill at the open - approve anytime, PDT-free swing. Rationale: own the pop_rank-1 RS leader/mover, not the safety-blanket laggard (7/21 'weight to the mover' lesson); OKLO has no own earnings until Aug 18 and is insulated from tonight's GOOGL/TSLA Mag-7 capex binary. Both books re-reconciled clean at the broker, zero naked: LIVE flat $810.32 cash (0/3 day-trades); PAPER 6/6 GTC-stopped (AMD $490 / SMR $7.50 / OKLO $39 / VRT $282 / CEG $236 / NVDA $186), equity ~$89.0k. Regime: QQQ ~$703 = ~-1.6% under its $714.7 20-day, 3x stays gated. AT THE OPEN: trim the ~32%-of-book paper NVDA anchor into the nuclear movers with clean stop re-arms (into strength, not the pre-open low); no fresh semi size into tonight's binary. Grade running: pre-open (TBD). pop_rank 1 = OKLO."

# ---- atomic write ----
tmp=SITE+".tmp"
with open(tmp,"w") as f: json.dump(d,f,indent=1,ensure_ascii=False)
os.replace(tmp,SITE)
print("WROTE",SITE,"backup",bak)
