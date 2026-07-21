import json, os, tempfile, datetime

SITE = "engine-data.json"
TS = "2026-07-21T07:42:00-04:00"

with open(SITE) as f:
    d = json.load(f)

# ---- backup first ----
with open("engine-data.backup-2026-07-21-0742.json","w") as b:
    json.dump(d, b, indent=1)

# ---- 1. pulse (prepend, trim 15) ----
pulse_text = ("7:42am pre-open - pulled fresh data and nothing changed the plan. QQQ is bid ~1.4% higher "
 "to ~$706 pre-market, but that's still ~1.5% under my $716.12 20-day, so the leverage gate stays SHUT "
 "(day 6) - no 3x chips into a bounce that's faded 5 days running. Confirmed PLTR reports Aug 3 (NOT this "
 "week) with no fresh negative, so the funded live buy (5 sh, $122 stop) stays STAGED to fill at the 9:30 "
 "open - executing yesterday's D-grade fix of rotating live into the leader early. Paper keeps its SQQQ hedge "
 "into Wed's GOOGL/TSLA prints; both books re-verified clean and 4/4 GTC-stopped. No trade this run (thin "
 "pre-market feed); next action is the open. Live same-day day-trade budget 0/3 used.")
pulse_hype = ("Chips are bouncing again but we're still under my line, so no leverage yet. The PLTR buy's queued "
 "for the open (earnings aren't till Aug 3, nothing scary this week) and both accounts are clean and stopped.")
d["pulse"].insert(0, {"ts": TS, "text": pulse_text, "hype": pulse_hype})
d["pulse"] = d["pulse"][:15]

# ---- 2. feed activity item (prepend) ----
feed_text = ("7:42am pre-open reconcile: fresh pull confirms the plan. QQQ premarket ~$705.7 (+1.38%) still < $716.12 "
 "20-day -> gate shut day 6, no 3x chips. PLTR earnings verified Aug 3 (not this week); live buy staged for the "
 "open, paper SQQQ hedge held into GOOGL/TSLA Wed. Both books clean, 4/4 GTC-stopped. Day-trade 0/3.")
d["feed"].insert(0, {"ts": TS, "type": "activity", "text": feed_text})

# ---- 3. projections refresh (keep chg_pct; market not open yet) ----
proj = {
 "PLTR": {"target_pct":2.0,"confidence":"med","basis":"1x RS leader owned both books; risk-on open, Aug-3 earnings = no binary","pop_rank":1,"path_pct":[0.6,1.3,2.0]},
 "AMD":  {"target_pct":3.0,"confidence":"med","basis":"Advancing AI 2026 event today - real catalyst but faded Mon (chase risk)","pop_rank":2},
 "NVDA": {"target_pct":2.5,"confidence":"med","basis":"Nebius stake + chip revival on the +1.4% Nasdaq gap","pop_rank":3},
 "VRT":  {"target_pct":1.8,"confidence":"med","basis":"AI-infra/data-center beta rides the +1.4% tape","pop_rank":4},
 "SMR":  {"target_pct":2.0,"confidence":"low","basis":"small-nuclear high-beta momentum bounce","pop_rank":5},
 "INTC": {"target_pct":1.5,"confidence":"low","basis":"chip bounce, but reports Thu = binary risk building","pop_rank":6},
 "CEG":  {"target_pct":0.7,"confidence":"med","basis":"defensive AI-power name, low beta","pop_rank":7},
 "RKLB": {"target_pct":1.5,"confidence":"low","basis":"space high-beta rebound off -2.7% Mon","pop_rank":8},
 "IONQ": {"target_pct":1.5,"confidence":"low","basis":"quantum high-beta catches the risk-on bid","pop_rank":9},
 "TSLA": {"target_pct":-0.5,"confidence":"low","basis":"soft into Wed AMC print; Cybercab called 'irrelevant'","pop_rank":10},
 "SOXL": {"target_pct":2.8,"confidence":"low","basis":"3x semis - GATED, pops fade under 20-day; don't own","pop_rank":11},
 "TQQQ": {"target_pct":1.4,"confidence":"low","basis":"3x Nasdaq - GATED OFF while QQQ < 20-day","pop_rank":12},
 "FNGU": {"target_pct":1.6,"confidence":"low","basis":"3x FANG - GATED OFF, decay risk in chop","pop_rank":13},
 "SQQQ": {"target_pct":-2.5,"confidence":"med","basis":"inverse falls on the +1.4% gap - deliberate hedge cost","pop_rank":14},
 "BE":   {"target_pct":-0.5,"confidence":"low","basis":"cut on verified project-delay catalyst; no reason to own","pop_rank":15},
}
for c in d["coverage"]:
    t = c["ticker"]
    if t in proj:
        c["projection"] = proj[t]
        c["updated"] = TS

# ---- 4. status cards ----
d["status"] = [
 {"session":"Pre-market","text":"QQQ ~$706, under $716 gate d6"},
 {"session":"Open plan","text":"PLTR buy fills 9:30; hedge on"},
 {"session":"Books","text":"Live $810 cash; paper 4/4 stopped"},
]

# ---- 5. headlines: light refresh of the regime line ----
d["headlines"][1] = ("Regime GATED day 6: QQQ premarket ~$705.7 (+1.38%) still under its 20-day $716.12 "
 "(-1.5%) - a +1.4% open doesn't clear the gate, so leveraged-index longs (TQQQ/SOXL/FNGU) stay OFF.")

# ---- 6. accountability running card (keep final:false) ----
acc = d["accountability"]
acc["headline"] = ("Pre-open 7/21 (running): the 7:42am read reconfirms the D-grade fix is IN MOTION - the funded "
 "PLTR buy stays STAGED to fill at the OPEN, rotating live into the pop_rank-1 RS leader early instead of camping "
 "cash. Chip revival is real (QQQ ~$706 premarket, AMD into its Advancing-AI event) but QQQ still ~1.5% under its "
 "$716.12 20-day -> gate SHUT day 6, no 3x chase. PLTR earnings verified Aug 3 (not this week) = no binary on the "
 "leader; GOOGL+TSLA report Wed AMC -> the paper SQQQ hedge is deliberate insurance, not lazy cash. Grade finalizes post-close.")
acc["adjust"] = ("At the open: if QQQ reclaims/holds $716 on volume, cut the paper SQQQ hedge and redeploy into "
 "PLTR/the confirmed leader (and re-lever live); if it fails again, let the PLTR live buy fill and ride, keep the "
 "hedge into GOOGL/TSLA Wed. Don't cut the hedge on a mere gap-up before the binary prints. Rotate the leader-buy "
 "EARLY (open, not 3pm) - that's the whole D-grade fix.")

# ---- 7. live/paper blocks: refresh ts + paper equity ----
d["live"]["updated"] = TS
d["paper"]["updated"] = TS
d["paper"]["equity"] = 89199.32

# ---- 8. top-level updated ----
d["updated"] = TS

# ---- 9. atomic write ----
dir_ = os.path.dirname(os.path.abspath(SITE))
fd, tmp = tempfile.mkstemp(dir=dir_, suffix=".tmp")
with os.fdopen(fd, "w") as f:
    json.dump(d, f, indent=1, ensure_ascii=False)
os.replace(tmp, SITE)

print("WROTE", SITE)
