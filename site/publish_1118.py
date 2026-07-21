import json, os, shutil, datetime
P='engine-data.json'
d=json.load(open(P))
TS='2026-07-21T11:18:00-04:00'

# ---- backup first ----
shutil.copy(P,'engine-data.backup-2026-07-21-1118.json')

# ---- pulse ----
d['pulse'].insert(0,{
 "ts":TS,
 "text":"11:18am - upgraded the LIVE ticket from the lagging PLTR to NVDA (3 sh ~$206, $186 stop, 0/3 day-trades used): today's leadership is the AI-infra/chip bid (SOX +3.7%, 2nd straight day; NVDA took a stake in neocloud Nebius) and NVDA is the NON-extended leader (+1.4% vs AMD +5.8% / INTC +7.3%), cheapest multiple in ~a decade, no earnings binary this week - a cleaner 'own the theme' entry than chasing the +6-14% names into their prints or holding red PLTR. Gate still SHUT (QQQ $708, -1.1% under its $716 20-day, day 6) so no 3x; holding the paper SQQQ hedge into Wed's GOOGL/TSLA earnings, paper otherwise unchanged (owns pop_rank-2 AMD, 5/5 stopped). Capture still ~0% with the biggest movers gated/extended, but the live setup quality is right and it's staged early, not at 3pm. Approve = NVDA fills now.",
 "hype":"Swapped the live ticket into NVDA - it's the cheap, un-extended one in the chip rally instead of the names that already ran +6-14%. Keeping the little hedge on until Google and Tesla report Wednesday."
})
d['pulse']=d['pulse'][:15]

# ---- status ----
d['status']=[
 {"session":"Open","text":"Bought AMD, trimmed SQQQ hedge"},
 {"session":"Late AM","text":"Upgraded live ticket PLTR->NVDA"},
 {"session":"Regime","text":"Gate shut day 6, QQQ <$716"}
]

# ---- headlines ----
d['headlines']=[
 "Chips rally a 2nd straight day (SOX +3.7%) on an AI-infrastructure rotation - Nasdaq +1%, ahead of Big Tech earnings",
 "NVIDIA takes a stake in neocloud Nebius + expands its Omniverse AI agent toolkit; +1.4%",
 "Intel +7%: Xeon-6 memory upgrade + Google Cloud AI deal - but Business Insider reports data-center layoffs; earnings Thu 7/23",
 "AMD +6% into its 7/22-23 Advancing AI event (Microsoft Helios deal); Marvell +7%, Arm +4% join the AI-infra bid",
 "GOOGL + TSLA report Wed after the close, INTC Thu - the week's binary earnings wall",
 "QQQ $708 still ~1.1% below its 20-day ($716) - the chip bounce hasn't cleared the leverage gate (day 6)",
 "Memory the one soft spot - a SanDisk/Micron-led selloff drags the momentum trade (SPMO worst month since 2015)",
 "Macro overhang: fresh US tariffs on Canada + Iran hostilities keep a risk-off tinge under the rally"
]

# ---- coverage: chg_pct + projection + updated for all; full rewrite for NVDA & PLTR ----
proj={
 "NVDA":(1.4, 2.8,"med","non-extended AI leader; Nebius stake; room to catch up",1),
 "AMD": (5.8, 5.5,"med","Advancing AI event 7/22-23 + MSFT Helios; extended",2),
 "INTC":(7.3, 6.0,"low","memory upgrade + Google AI deal, but Thu earnings + layoffs",3),
 "SMR": (7.0, 6.0,"low","nuclear/SMR momentum on the AI-power bid; thin float",4),
 "SOXL":(14.6,11.0,"low","3x semis ripping but gated + fade-prone",5),
 "RKLB":(4.6, 4.0,"med","space/defense momentum reclaiming its range",6),
 "VRT": (3.6, 3.5,"med","AI-power / datacenter-cooling bid",7),
 "IONQ":(4.3, 4.0,"low","quantum beta rides the risk-on tape",8),
 "TQQQ":(5.2, 4.5,"low","3x Nasdaq, gated under the 20-day",9),
 "CEG": (2.9, 2.5,"med","AI-power utility, steady bid",10),
 "TSLA":(3.5, 3.5,"low","up into Wed earnings - binary tomorrow",11),
 "BE":  (12.2,8.0,"low","dead-cat bounce off the TD Cowen flush; we cut it",12),
 "FNGU":(2.4, 3.0,"low","3x FANG+, gated; mega-cap lagging the chip rip",13),
 "PLTR":(-1.1,-0.5,"med","software out of favor while AI-infra leads; basing",14),
 "SQQQ":(-5.1,-5.0,"med","inverse bleeds on green tape; held as Wed-earnings hedge",15),
}
for c in d['coverage']:
    t=c['ticker']
    if t in proj:
        cp,tp,conf,basis,pr=proj[t]
        c['chg_pct']=cp
        c['projection']={"target_pct":tp,"confidence":conf,"basis":basis,"pop_rank":pr}
        c['updated']=TS

for c in d['coverage']:
    if c['ticker']=='NVDA':
        c['verdict']="buy"; c['verdict_label']="Buy - live"
        c['thesis']="**The non-extended AI leader - now the funded LIVE pick.** While AMD/INTC ran +6-7%, NVDA is only +1.4% (it lagged = a cheaper entry in the group leader), took a stake in neocloud Nebius, and trades at its cheapest forward multiple in ~a decade. Staged a live BUY (3 sh ~$206, $186 GTC stop below the late-June $192 base) + hold 90 sh paper. No earnings binary until late Aug."
        c['hold_reason']="The AI-chip bellwether and the theme leader that's actually bid this week. We hold 90 sh in paper and just staged a live buy - it lagged today's +6% chip pop, so we get the leader at a non-extended price with a fresh Nebius catalyst. A clean break of $186 or a bad read-through from this week's GOOGL/TSLA/INTC prints gets us out."
        c['size']="$18.5k paper (90 sh) + live ticket 3 sh"; c['size_pct']="~21% paper"
        c['size_note']="LIVE pick - ticket 2026-07-21-1 (3 sh, $186 stop); +90 sh paper"
        c['plan_usd']="$620 live (3 sh) on approve"
    if c['ticker']=='PLTR':
        c['verdict']="hold"; c['verdict_label']="Hold - paper"
        c['thesis']="**Basing but out of favor while AI-infra leads.** PLTR is red -1.1% as money rotates into chips/AI-infra; it's holding its $131-133 two-week base but not leading. We RETIRED the live buy ticket in favor of the non-extended NVDA and keep the 100-sh paper position on its $125 stop into the Aug 3 print."
        c['hold_reason']="Our software/AI-analytics leader, but a laggard on a chip-led tape. We hold 100 sh in paper at a $125 stop; today it's the wrong theme, so we pulled the live ticket and put that idea into NVDA. We stay in the paper hold while it bases above $129-131; a break there or a failed Aug 3 print gets us out."
        c['size']="$13.3k paper (100 sh)"; c['size_pct']="~15% paper"
        c['size_note']="paper hold; live ticket retired -> NVDA"; c['plan_usd']="no live plan (retired)"

# ---- pending_tickets ----
d['pending_tickets']=[{
 "id":"2026-07-21-1","symbol":"NVDA","side":"buy","size":"$620","qty":3,
 "entry":"~$206 marketable - market open, approve = fills now","trigger":None,"stop":186,
 "bracket":"stop $186 GTC (below the late-June $192 base, -9.7%)",
 "thesis":"Funded live rotation OUT of a 6th day of cash and INTO the leading AI-infra/chip theme via the NON-extended leader. NVDA +1.4% (lagged the +6% AMD/INTC = cheaper entry), fresh Nebius-stake catalyst, cheapest multiple in a decade, no earnings binary this week. Wide $186 stop. Approve -> fills at market now."
}]

# ---- feed ----
d['feed'].insert(0,{"ts":"2026-07-21T11:17:00-04:00","type":"activity","text":"Retired the live PLTR buy ticket (2026-07-20-3): PLTR is red -1.1% while the AI-infra/chip bid runs - lagging the theme, not leading it. Rotated the live idea into NVDA, the non-extended leader of the group that's bid."})
d['feed'].insert(0,{"ts":TS,"type":"trade","side":"buy","status":"pending","symbol":"NVDA","detail":"3 @ ~$206","reaction":"rotate","text":"Staged a LIVE buy on NVDA (3 sh, $186 stop) - the non-extended AI leader (+1.4% vs the +6-14% AMD/INTC/SOXL that are gated or extended into earnings). Approve = fills now; gets live out of a 6th day of cash into the theme that's running."})
d['feed']=d['feed'][:40]

# ---- activity (top-level engine log) ----
if isinstance(d.get('activity'),list):
    d['activity'].insert(0,{"ts":TS,"kind":"engine","title":"Tue 7/21 ~11:18am ET (RTH, market open). Upgraded the LIVE ticket PLTR->NVDA (3 sh ~$206, $186 GTC stop) - the non-extended AI leader in a 2nd-day chip rally (SOX +3.7%), vs chasing the gated 3x (SOXL +14.6%) or the earnings-extended INTC +7.3%/AMD +5.8%. Gate shut day 6 (QQQ $708 < $716 20-day). Paper unchanged, 5/5 GTC-stopped ($89.48k); live flat $810 cash awaiting the tap. Both books zero-naked."})
    d['activity']=d['activity'][:30]

# ---- accountability ----
d['accountability']={
 "date":"2026-07-21","final":False,"grade":"C (running, intraday)",
 "headline":"Process keeps tightening: I upgraded the LIVE ticket EARLY (11am) from the lagging red PLTR to the non-extended AI leader NVDA - the theme that's actually running - instead of a 3pm scramble or a chase of the +6-14% names into their binaries. But capture is still ~0%: the biggest movers are un-ownable here (SOXL +14.6% gated 3x, BE +12.2% dead-cat, INTC +7.3% extended into Thu earnings), AMD +5.8% is owned only in paper, and LIVE is still cash awaiting the tap. Gate on trial a 6th day. Final grade at the close.",
 "capture":{"bestName":"SOXL (gated 3x) / BE (dead-cat)","bestPct":"+14.6% / +12.2%","capturedPct":"paper ~-0.2%, live 0%","rate":"~0% - biggest movers un-ownable; AMD +5.8% owned in paper"},
 "missed":[
  {"from":"live cash","to":"NVDA (staged, untapped)","note":"live's been 100% cash 6 sessions; upgraded the ticket to the non-extended leader so it pings fresh - only helps once tapped","delta":"opportunity, pending tap"},
  {"from":"paper SQQQ hedge (100 sh)","to":"a 1x leader","note":"the residual SQQQ (-5.1% today) drags on a green tape; kept as Wed-earnings insurance but it caps capture","delta":"-$218 intraday drag"}
 ],
 "saved":[
  {"note":"Held the 3x gate a 6th day - didn't chase SOXL +14.6% / TQQQ +5.2% under a sub-20-day QQQ; the pop has faded 5 straight sessions","delta":"discipline intact"},
  {"note":"Upgraded live to the NON-extended NVDA instead of chasing INTC +7.3% / AMD +5.8% into their earnings binaries","delta":"process intact"},
  {"note":"Both books verified at the broker: paper 5/5 GTC-stopped, live clean cash - never-naked","delta":"safety intact"}
 ],
 "best":{"name":"AMD (30 sh @ $527.80, paper)","note":"owns the pop_rank-2 1x chip leader (+5.8%) into its 7/22-23 event","delta":"+5.8% name, owned"},
 "worst":{"name":"SQQQ hedge (100 sh)","note":"the residual inverse (-5.1% today) is the book's biggest day drag; on a leash - cut on a QQQ $716 reclaim","delta":"-$218 intraday"},
 "avoided":{"worstName":"gated 3x chase (SOXL/TQQQ) + earnings-extended names (INTC/AMD)","worstPct":"SOXL +14.6% now but round-tripped +13->+9% on the same fade pattern; INTC into Thu binary","note":"the gate + the non-extended-leader rule kept both books out of the leveraged pop and the earnings binaries","amount":"~$0 (didn't chase)","rate":"held the line"},
 "applying":"The 7/20 D-lesson: stage the leader-buy EARLY, not at 3pm - upgraded the live ticket to NVDA now at 11am; and pick the NON-extended leader over chasing +6-14% names into their prints.",
 "adjust":"If QQQ reclaims $716 on volume, cut the SQQQ hedge and deploy paper powder + the freed gate into the confirmed leaders; if the chip bid fades a 6th time into Wed's GOOGL/TSLA, the hedge pays and non-extended NVDA holds up better than the +6-14% names."
}

# ---- score ----
d['score']={"alphaPts":"-16.0","benchmark":"-3.0%","bestDay":"+3.2%","bestDayName":"Jul 14 - CPI chip rally (settled)","winRate":"33%","tradeCount":6}

# ---- live / paper marks + equity curve ----
d['live']['equity']=810.32
d['live']['updated']=TS
d['live']['equity_note']="LIVE flat $810.32 cash / zero positions / zero naked; 1 pending ticket = BUY NVDA 3 sh ($186 stop). -19.0% since $1,000 inception."
if d['live']['equity_curve'][-1]['date']!='Jul 21':
    d['live']['equity_curve'].append({"date":"Jul 21","value":810.32})

d['paper']['equity']=89476.02
d['paper']['updated']=TS
d['paper']['equity_note']="Paper ~$89.48k (-0.2% vs Mon - AMD +5.8%/CEG +2.9% offset by the SQQQ hedge -5.1% + soft NVDA/PLTR), 5/5 GTC-stopped, zero naked (AMD 30/$458, PLTR 100/$125, NVDA 90/$186, CEG 16/$236, SQQQ 100/$38), ~37% cash powder for a QQQ $716 reclaim."
if d['paper']['equity_curve'][-1]['date']!='Jul 21':
    d['paper']['equity_curve'].append({"date":"Jul 21","value":89476.02})

# ---- latest_recap + updated ----
d['latest_recap']="11:18am 7/21 - Upgraded the LIVE ticket PLTR->NVDA (3 sh ~$206, $186 stop): the AI-infra/chip bid is the day's leadership (SOX +3.7%, NVDA-Nebius stake) and NVDA is the non-extended leader vs the +6-14% AMD/INTC/SOXL that are gated or extended into earnings. Gate shut day 6 (QQQ $708 < $716). Paper unchanged, 5/5 stopped, owns pop_rank-2 AMD + the SQQQ hedge into Wed GOOGL/TSLA. Live flat $810 cash awaiting the NVDA tap."
d['updated']=TS

# ---- atomic write ----
tmp=P+'.tmp'
json.dump(d,open(tmp,'w'),indent=1)
os.replace(tmp,P)
print("WROTE",P)
