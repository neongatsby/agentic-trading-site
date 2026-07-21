import json, os, shutil, datetime

SITE="engine-data.json"
TS="2026-07-21T08:44:00-04:00"

# backup first
bkp=f"engine-data.backup-2026-07-21-0844.json"
shutil.copy(SITE, bkp)

d=json.load(open(SITE))

# ---- updated ----
d["updated"]=TS

# ---- pulse (prepend, trim to 15) ----
new_pulse={
 "ts":TS,
 "text":"8:44am pre-open - the chip pop kept EXTENDING overnight (SOXL +12.5%, INTC +5.4% on the first High-NA EUV in production, AMD +3.8% on the confirmed MSFT-Helios deal, even beaten-down BE +5.4%). But it's still NARROW: NVDA won't confirm (muted) and QQQ ~$705 is still ~1.6% under my $716 20-day, so the gate stays SHUT (day 6) and I'm not chasing the 3x that's round-tripped 5 sessions straight. PLTR ticked red premkt (-0.9%) = a cheaper entry on the RS leader, not a reason to bail, so the funded live buy stays staged for the 9:30 open. Paper holds 4/4 incl. the SQQQ hedge into Wed's GOOGL/TSLA/INTC prints; I add a 1x leader (AMD/NVDA, never SOXL) only if the open confirms. 0/3 day-trades used.",
 "hype":"Chips ripped even harder overnight, but NVDA's still not playing along and we're under the line - so no chasing the 3x. PLTR dipped a hair (cheaper entry), so the live buy's still set for the open."
}
d["pulse"]=[new_pulse]+d["pulse"][:14]

# ---- status ----
d["status"]=[
 {"session":"Pre-market","text":"Semis extend: SOXL +12.5%, INTC +5.4%"},
 {"session":"Open plan","text":"PLTR fills 9:30; add 1x on confirm"},
 {"session":"Books","text":"Live $810 cash; paper 4/4 stopped"}
]

# ---- headlines ----
d["headlines"]=[
 "Chip bounce EXTENDS and builds into a 2nd session - SOXL +12.5%, INTC +5.4%, AMD +3.8%, even beaten-down BE +5.4% premarket - on AMD's Microsoft 'Helios' data-center deal + Intel's first High-NA EUV production milestone.",
 "But it's still NARROW: NVDA won't confirm (muted premkt) and QQQ ~$705 stays ~1.6% under its $716.12 20-day - the same gated setup whose chip pops have round-tripped 5 sessions running.",
 "NQ futures +1.3% / S&P +0.4% on chip strength + Iran ceasefire hopes easing oil - capped by this week's Big Tech earnings wall.",
 "Midweek catalyst cluster: AMD 'Advancing AI 2026' 7/22-23, GOOGL + TSLA earnings Wed 7/22 AMC, INTC Thu 7/23 - the paper SQQQ hedge is insurance into it.",
 "PLTR the clean 1x RS leader (no gate, Aug-3 earnings), -0.9% premarket = a cheaper entry - the funded live buy stays staged for the open.",
 "Regime gate SHUT day 6: no leveraged-index longs (SOXL/TQQQ/FNGU/UPRO stay off) until QQQ reclaims its 20-day on volume."
]

# ---- coverage: update chg_pct + projection + updated ----
upd={
 "PLTR":(-0.9,{"target_pct":1.5,"confidence":"med","basis":"RS leader, red premkt = cheaper swing entry, no earnings","pop_rank":8}),
 "AMD":(3.8,{"target_pct":4.5,"confidence":"med","basis":"MSFT Helios deal + 7/22 event; best ownable 1x","pop_rank":1}),
 "INTC":(5.4,{"target_pct":5.0,"confidence":"med","basis":"first High-NA EUV in production; leads chips, earnings Thu","pop_rank":2}),
 "NVDA":(0.8,{"target_pct":2.0,"confidence":"med","basis":"the confirm tell; muted premkt, needs to turn green","pop_rank":3}),
 "VRT":(1.2,{"target_pct":1.5,"confidence":"low","basis":"AI-infra beta, follows the semis","pop_rank":10}),
 "SOXL":(12.5,{"target_pct":6.0,"confidence":"low","basis":"3x semis +12% but GATED + round-tripped 5 sessions","pop_rank":4}),
 "TQQQ":(3.8,{"target_pct":3.5,"confidence":"low","basis":"3x Nasdaq, GATED under the 20-day","pop_rank":9}),
 "CEG":(0.3,{"target_pct":0.4,"confidence":"med","basis":"defensive, flat premkt","pop_rank":14}),
 "FNGU":(2.5,{"target_pct":2.2,"confidence":"low","basis":"3x FANG+, GATED","pop_rank":11}),
 "IONQ":(1.0,{"target_pct":1.2,"confidence":"low","basis":"quantum risk-on beta","pop_rank":12}),
 "RKLB":(2.0,{"target_pct":2.5,"confidence":"low","basis":"space/high-beta, bounces with the tape","pop_rank":7}),
 "SQQQ":(-3.6,{"target_pct":-3.5,"confidence":"med","basis":"inverse hedge; bleeds on the chip gap, insurance into Wed","pop_rank":15}),
 "TSLA":(0.5,{"target_pct":0.5,"confidence":"low","basis":"soft into Wed earnings; Cybercab noise","pop_rank":13}),
 "BE":(5.4,{"target_pct":4.0,"confidence":"low","basis":"+5% bounce off Monday's -8% TD Cowen flush; suspect","pop_rank":5}),
 "SMR":(1.5,{"target_pct":2.0,"confidence":"low","basis":"SMR nuclear beta, modest premkt","pop_rank":6}),
}
for c in d["coverage"]:
    t=c.get("ticker")
    if t in upd:
        chg,proj=upd[t]
        c["chg_pct"]=chg
        c["projection"]=proj
        c["updated"]="8:44a"

# ---- accountability (running, pre-open) ----
a=d["accountability"]
a["date"]="2026-07-21"
a["final"]=False
a["grade"]="running (pre-open)"
a["headline"]=("Pre-open 7/21 (running): the chip pop kept EXTENDING (SOXL +12.5% / INTC +5.4% / AMD +3.8% / BE +5.4% premkt) but stayed NARROW - NVDA won't confirm and QQQ ~$705 is still ~1.6% under its $716.12 20-day, so the gate holds SHUT (d6) and I'm not chasing the 3x pop that's faded 5 sessions running (the account's costliest lesson). The D-grade fix stays in motion: the funded PLTR live buy is STAGED for the OPEN (1x RS leader, -0.9% premkt = cheaper entry, no binary). Honest top pop-pick is AMD into its 7/22-23 event; the gate-compliant capture plan is to add the 1x leader (AMD/NVDA, never SOXL) with paper dry powder on a confirmed open hold. Capture risk owned: if the chip bid HOLDS today, AMD/INTC out-pop my staged PLTR. Grade finalizes post-close.")
a["capture"]={
 "bestName":"TBD at the close",
 "bestPct":"-",
 "capturedPct":"-",
 "rate":"pending - pre-open; live set to own PLTR at the open, paper owns it + the hedge, 1x-leader add planned on a confirmed open hold"
}
a["missed"]=[]
a["saved"]=[
 {"note":"Kept the leader-buy STAGED for the OPEN (approve-anytime -> fills 9:30), holding yesterday's cut+rotate-earlier fix in motion instead of a late-3pm proposal","delta":"fix applied"},
 {"note":"Held the regime gate a 6th day - refused to chase the 3x semis into a +12.5% SOXL / +5.4% INTC premarket pop that, 5 sessions running, has round-tripped back under the 20-day","delta":"discipline intact"}
]

# ---- atomic write ----
tmp=SITE+".tmp"
with open(tmp,"w") as f:
    json.dump(d,f,ensure_ascii=False,indent=1)
os.replace(tmp,SITE)

# ---- read-back verify ----
v=json.load(open(SITE))
ranks=sorted(c["projection"]["pop_rank"] for c in v["coverage"])
pop1=[c["ticker"] for c in v["coverage"] if c["projection"]["pop_rank"]==1]
pending=[t["symbol"] for t in v.get("pending_tickets",[])]
print("VERIFY updated:", v["updated"])
print("VERIFY pulse len:", len(v["pulse"]), "| pulse[0].ts:", v["pulse"][0]["ts"])
print("VERIFY coverage len:", len(v["coverage"]))
print("VERIFY pop_ranks:", ranks, "| unique 1-15:", ranks==list(range(1,16)))
print("VERIFY pop_rank1:", pop1)
print("VERIFY pending_tickets:", pending)
print("VERIFY accountability:", v["accountability"]["date"], v["accountability"]["final"], v["accountability"]["grade"])
print("VERIFY score unchanged:", v["score"])
print("OK" if (v["updated"]==TS and len(v["pulse"])==15 and ranks==list(range(1,16)) and pop1==["AMD"] and pending==["PLTR"] and v["accountability"]["final"]==False) else "MISMATCH")
