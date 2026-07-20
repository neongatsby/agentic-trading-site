import json, shutil
PATH='/sessions/awesome-pensive-dijkstra/mnt/movita-backend/agentic-trading-site/site/engine-data.json'
BKP='/sessions/awesome-pensive-dijkstra/mnt/movita-backend/agentic-trading-site/site/engine-data.backup-2026-07-20-1841.json'
TS='2026-07-20T18:41:00-04:00'
shutil.copy(PATH, BKP)
d=json.load(open(PATH))

d['pulse']=[{
 "ts":TS,
 "hype":"6:40pm check — nothing moved, both books still clean. PLTR's still the leader so tomorrow's open buy stands; keeping the paper hedge on into the open.",
 "text":("6:41pm / after-hours heartbeat, ~30 min on from the 6:10 check. Book unchanged and both reconcile == broker: LIVE flat "
   "(cash $810.32, zero positions/orders, nothing naked); PAPER holds CEG 16 / NVDA 90 / PLTR 100 + the SQQQ 310 hedge, all 4 GTC-stopped "
   "($236/$186/$125/$38), ~$41.5k (~46%) powder for the open fork. Regime unchanged — QQQ closed $696.06 vs a 20-day of $716.12 (2.8% under, "
   "leverage gate SHUT a 5th day) while SPY sits near records ($742), so it's a chip-specific derate, not broad risk-off. Fresh-news scan added only "
   "incremental color — AMD's 'Advancing AI' event this week (6 analyst target-raises), IREN +20% on a $2.8B AI-cloud deal, ORCL still soft on "
   "AI-capex/debt — nothing that touches our book; the Iran-strike overhang persists into a heavy earnings week (TXN Tue, GOOGL/TSLA Wed, INTC Thu). "
   "Plan stands: PLTR ticket 2026-07-20-3 (5 sh, $122 stop, approve-anytime → fills at the 7/21 open) is the funded BE→PLTR rotation; paper holds into "
   "tomorrow's QQQ-vs-$716/$695 fork. PDT budget fully open (0/3). Grade final: D.")
}]+d.get('pulse',[])
d['pulse']=d['pulse'][:15]

d['feed']=[{
 "type":"activity","ts":TS,
 "text":("6:41pm after-hours: quiet — book unchanged, both clean (LIVE flat/cash $810 zero-naked; PAPER 4 names all GTC-stopped). Fresh news only "
   "incremental (AMD AI event, IREN AI-cloud deal, ORCL soft). PLTR still the leader so the open buy stands; paper holds into the QQQ $716/$695 fork.")
}]+d.get('feed',[])
d['feed']=d['feed'][:40]

d['headlines']=[
 "PLTR the clean RS leader — closed +1.9% at a fresh 2-week high while software cracked (ORCL soft on AI-capex/debt); it's the funded live+paper rotation target, teed up for the 7/21 open",
 "Leverage gate SHUT day 5: QQQ closed $696 vs its 20-day $716 (2.8% under) as the morning chip pop round-tripped again (SOXL +10%→+1.3%) — but SPY near records $742 = a chip-specific derate, not a broad risk-off",
 "LIVE ended Monday 100% cash (grade D): the BE cut filled @ $203 but the PLTR buy expired untapped at the close — rotation re-staged for tomorrow's open",
 "SMR +3.2% led the watchlist (nuclear-for-AI); CEG +0.5% / OKLO +1.0% / VRT +0.8% — the defensive AI-power bid held while chips faded",
 "Bloom Energy cut and validated: sold live @ $203 on TD Cowen's data-center-delay note; BE cratered to close -8.0% at fresh 90-day lows",
 "AMD's 'Advancing AI' event this week draws 6 analyst target-raises (share-gain-vs-NVDA narrative); IREN +20% on a $2.8B AI-cloud deal keeps AI-infra momentum alive",
 "Risk-off overhang into the open: fresh U.S. airstrikes on Iran (2nd service-member death reported), oil wavering — atop a heavy earnings week (TXN Tue, GOOGL/TSLA Wed, INTC Thu; TSLA -2.9% into its print)",
 "Rocket Lab named in the ~$17B U.S. NSSL Phase 3 Lane 1 launch pool (with SpaceX/ULA/Blue Origin) — but RKLB sold the news, closed -2.7%"
]

status=d.get('status',[])
for s in status:
    if s.get('session')=="Evening": s['text']="Book clean; PLTR staged for open"
d['status']=status

proj={
 'PLTR':{"target_pct":2.0,"confidence":"med","basis":"RS leader at a 2wk high; software-weak tape favors it, no earnings tmrw","pop_rank":1,"path_pct":[0.7,1.4,2.0]},
 'SQQQ':{"target_pct":1.2,"confidence":"med","basis":"gate shut day 5 + Iran/earnings risk = a weak-tape hedge that works","pop_rank":2},
 'CEG':{"target_pct":0.8,"confidence":"med","basis":"defensive AI-power bid held green while chips faded","pop_rank":3},
 'SMR':{"target_pct":1.0,"confidence":"low","basis":"nuclear-for-AI RS leader (+3.2%) but choppy after a spent move","pop_rank":4},
 'NVDA':{"target_pct":0.6,"confidence":"low","basis":"tries to base but AMD share-gain narrative + chip derate cap it","pop_rank":5},
 'VRT':{"target_pct":0.8,"confidence":"low","basis":"AI-power / data-center infra, steady green","pop_rank":6},
 'AMD':{"target_pct":1.2,"confidence":"low","basis":"'Advancing AI' event this week + 6 analyst target-raises","pop_rank":7},
 'RKLB':{"target_pct":1.0,"confidence":"low","basis":"sold the $17B NSSL news -2.7%; oversold-bounce setup","pop_rank":8},
 'INTC':{"target_pct":0.8,"confidence":"low","basis":"chip-bounce try but INTC earnings Thu = binary risk","pop_rank":9},
 'IONQ':{"target_pct":-0.5,"confidence":"low","basis":"quantum soft into a risk-off tape","pop_rank":10},
 'SOXL':{"target_pct":0.5,"confidence":"low","basis":"3x semis but gate shut — fades under the 20-day","pop_rank":11},
 'TQQQ':{"target_pct":0.3,"confidence":"low","basis":"3x Nasdaq in the decay zone (QQQ < 20-day)","pop_rank":12},
 'FNGU':{"target_pct":0.5,"confidence":"low","basis":"3x FANG, gate shut","pop_rank":13},
 'TSLA':{"target_pct":-1.0,"confidence":"low","basis":"downtrend -2.9%, earnings Wed = binary risk","pop_rank":14},
 'BE':{"target_pct":0.3,"confidence":"low","basis":"cut/broken thesis at 90-day lows; only an oversold dead-cat","pop_rank":15},
}
seen=set()
for c in d.get('coverage',[]):
    t=c.get('ticker')
    if t in proj:
        c['projection']=proj[t]; c['updated']=TS; seen.add(t)
    if t=='PLTR':
        c['thesis']=c['thesis'].replace("PLTR is +2.6% holding a fresh 2-week high","PLTR closed +1.9% at a fresh 2-week high")

ones=[c['ticker'] for c in d['coverage'] if c.get('projection',{}).get('pop_rank')==1]
assert ones==['PLTR'], ones
ranks=sorted(c['projection']['pop_rank'] for c in d['coverage'] if c.get('ticker') in proj)
assert ranks==list(range(1,len(proj)+1)), ranks

d['live']['updated']=TS
d['live']['equity_note']=("Flat/clean cash after the BE cut ($810.32, -4.2% today, settled). Zero positions/orders, nothing naked. "
  "PLTR buy re-staged for the 7/21 open (ticket 2026-07-20-3, 5 sh, $122 stop, approve-anytime → fills at the open).")
d['paper']['updated']=TS
d['paper']['equity_note']=("Paper ~$89.5k, ~-1.0% today (settled). PLTR the green leader (+1.9%), NVDA/CEG slightly green, SQQQ hedge +0.4%. "
  "Owns the leader: PLTR 100 sh ($125 GTC stop). 4 names all GTC-stopped, zero naked; ~$41.5k (~46%) powder held for the open fork — "
  "QQQ reclaims $716 → add gated names back + cut the hedge; loses $695 → press the SQQQ hedge. Not chasing the faded chips.")

d['latest_recap']=("Mon 7/20 ~6:41pm ET — market CLOSED (after-hours), verify-and-hold heartbeat ~30 min on from the 6:10 check. Book unchanged, both "
 "reconciled == broker: LIVE flat (cash $810.32, zero positions/orders, nothing naked); PAPER (CEG 16 / NVDA 90 / PLTR 100 / SQQQ 310, all 4 GTC-stopped: "
 "PLTR $125 / NVDA $186 / SQQQ $38 / CEG $236), equity ~$89.5k, ~46% powder. Regime unchanged: QQQ closed $696.06 vs 20-day $716.12 = 2.8% under, leverage "
 "gate SHUT day 5; SPY $742 near records = a chip-specific derate, not a broad crash. Fresh-news scan this pull added only incremental color — AMD's "
 "'Advancing AI' event this week (6 analyst target-raises), IREN +20% on a $2.8B AI-cloud deal, ORCL soft on AI-capex/debt — none touching our book; the "
 "Iran-strike risk-off overhang persists into a heavy earnings week (TXN Tue, GOOGL/TSLA Wed, INTC Thu). Plan unchanged: PLTR is the 1x RS leader (closed "
 "+1.9% at a 2-wk high, catalyst stack intact), so the funded BE→PLTR rotation (ticket 2026-07-20-3, 5 sh, $122 stop, approve-anytime → fills at the 7/21 "
 "open) STANDS; paper HOLDS into tomorrow's QQQ-vs-$716/$695 fork. PDT budget fully open (0/3). Today's grade final: D.")

d['updated']=TS
json.dump(d, open(PATH,'w'), ensure_ascii=False, indent=1)
print("WROTE ok | coverage refreshed:",len(seen),"| pulse",len(d['pulse']),"| feed",len(d['feed']),"| headlines",len(d['headlines']))
print("accountability final:",d['accountability'].get('final'),"grade:",d['accountability'].get('grade'))
print("pending_tickets:",[t.get('id') for t in d.get('pending_tickets',[])])
