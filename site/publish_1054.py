#!/usr/bin/env python3
# Unique per-run publish (2026-07-21 10:54 ET) — atomic write + read-back verify (anti-clobber OPS rule)
import json, os, tempfile, sys

SITE = os.path.dirname(os.path.abspath(__file__))
P = os.path.join(SITE, "engine-data.json")
TS = "2026-07-21T10:54:00-04:00"

d = json.load(open(P))

# ---- backup the good current state FIRST ----
bak = os.path.join(SITE, "engine-data.backup-2026-07-21-1054.json")
with open(bak, "w") as f:
    json.dump(d, f, indent=1)

# ---- coverage: fresh chg_pct + projection per ticker (ranks 1-15 unique, AMD=1) ----
COV = {
 "AMD":  {"chg": 4.9,  "verdict":"buy",   "proj":{"target_pct":5.5,"confidence":"med","basis":"into 7/22 AI event + MSFT Helios + memory cycle","pop_rank":1,"path_pct":[4.9,5.2,5.5]}},
 "INTC": {"chg": 6.1,  "verdict":"watch", "proj":{"target_pct":6.5,"confidence":"med","basis":"first High-NA EUV in production; leads chips, earns Thu","pop_rank":2}},
 "SOXL": {"chg": 12.1, "verdict":"avoid", "proj":{"target_pct":9.0,"confidence":"low","basis":"3x semis rips but gated + faded 5 sessions","pop_rank":3}},
 "SMR":  {"chg": 6.3,  "verdict":"watch", "proj":{"target_pct":6.0,"confidence":"low","basis":"nuclear-for-AI spec, extended","pop_rank":4}},
 "NVDA": {"chg": 0.9,  "verdict":"hold",  "proj":{"target_pct":2.0,"confidence":"med","basis":"Nebius stake; the muted confirm tell","pop_rank":5}},
 "BE":   {"chg": 11.7, "verdict":"avoid", "proj":{"target_pct":9.0,"confidence":"low","basis":"dead-cat bounce off TD Cowen flush, no upgrade","pop_rank":6}},
 "TQQQ": {"chg": 4.1,  "verdict":"avoid", "proj":{"target_pct":3.5,"confidence":"low","basis":"3x QQQ gated under the 20-day","pop_rank":7}},
 "VRT":  {"chg": 2.7,  "verdict":"watch", "proj":{"target_pct":3.0,"confidence":"med","basis":"AI data-center power/cooling bid","pop_rank":8}},
 "IONQ": {"chg": 3.5,  "verdict":"watch", "proj":{"target_pct":3.5,"confidence":"low","basis":"quantum spec riding risk-on","pop_rank":9}},
 "RKLB": {"chg": 3.3,  "verdict":"watch", "proj":{"target_pct":3.0,"confidence":"low","basis":"space momentum, steady","pop_rank":10}},
 "TSLA": {"chg": 3.4,  "verdict":"avoid", "proj":{"target_pct":2.5,"confidence":"low","basis":"bounce into Wed earnings (binary)","pop_rank":11}},
 "PLTR": {"chg": -0.8, "verdict":"buy",   "proj":{"target_pct":1.5,"confidence":"med","basis":"RS-leader dip; cheaper live swing, not today's pop","pop_rank":12}},
 "CEG":  {"chg": 2.2,  "verdict":"hold",  "proj":{"target_pct":2.5,"confidence":"med","basis":"nuclear/defensive, owned in paper","pop_rank":13}},
 "FNGU": {"chg": 2.3,  "verdict":"avoid", "proj":{"target_pct":3.0,"confidence":"low","basis":"3x mega-cap gated under the 20-day","pop_rank":14}},
 "SQQQ": {"chg": -4.1, "verdict":"hold",  "proj":{"target_pct":-3.5,"confidence":"low","basis":"inverse hedge; pops only if chips fade","pop_rank":15}},
}
for c in d["coverage"]:
    t = c.get("ticker")
    if t in COV:
        c["chg_pct"] = COV[t]["chg"]
        c["verdict"] = COV[t]["verdict"]
        c["projection"] = COV[t]["proj"]
        c["updated"] = TS

# refresh PLTR + AMD hold_reason to current (owned/live names)
for c in d["coverage"]:
    if c.get("ticker") == "PLTR":
        c["hold_reason"] = ("Our clean 1x relative-strength leader - the AI-software name that kept printing 2-week highs "
            "while software peers cracked. Today it's RED (-0.8%) as money rotates into chips, but that's a cheaper entry, "
            "not a broken thesis (no gate, no earnings till Aug 3, fresh DA Davidson $175 upgrade + Burry covered). We hold 100 sh in paper "
            "and the live buy ticket is refreshed and one tap away. We'd cut it only if $129-131 base breaks (the $122/$125 stops sit just below).")
    if c.get("ticker") == "AMD":
        c["hold_reason"] = ("Bought 30 sh @ $527.80 at the open (paper) - the pop_rank-1 call: the ownable 1x chip leader running into "
            "its 7/22-23 Advancing AI event on the Microsoft Helios rack-scale deal, plus a memory-cycle tailwind. 1x so no regime-gate issue. "
            "Wide $458 GTC stop. We watch the event + whether NVDA finally confirms the semi bid; a sell-the-event fade is the risk we're stopped against.")

# ---- pulse: prepend one, keep newest 15 ----
pulse_new = {
 "ts": TS,
 "text": ("10:54am management run - refreshed the LIVE PLTR buy ticket in place (5 sh, $122 stop, ~$134 marketable) so it's current and "
   "pings fresh; it's the 1x RS leader, red today (-0.8%) = a cheaper entry, not a broken thesis, and I'd rather own it than chase INTC +6% / "
   "SOXL +12% / AMD +5% into Wed's GOOGL/TSLA and Thu's INTC prints. Gate shut day 6 (QQQ $705.6 still ~1.5% under its $716 20-day), so no 3x "
   "chase - SOXL's +12% is the exact setup that's faded 5 sessions straight. Paper holds AMD (owned the pop_rank-1 chip leader since the open) "
   "+ NVDA/CEG/PLTR + the SQQQ hedge into the earnings wall; I cut the hedge and add the 1x leader only on a QQQ $716 reclaim. Honest capture "
   "risk: if the chip bid holds today, our books trail the extended names. Day-trade 0/3."),
 "hype": ("Refreshed the live PLTR ticket so it's current - the leader's red today, which is a cheaper entry, not a reason to bail. "
   "Still not chasing the chip pop that's faded 5 days running right into this week's big earnings.")
}
d["pulse"] = [pulse_new] + d.get("pulse", [])
d["pulse"] = d["pulse"][:15]

# ---- status (3 cards) ----
d["status"] = [
 {"session":"Open",        "text":"Bought AMD, cut SQQQ hedge"},
 {"session":"Late morning","text":"Refreshed live PLTR buy ticket"},
 {"session":"Regime",      "text":"Gate shut day 6, QQQ <$716"},
]

# ---- headlines ----
d["headlines"] = [
 "Nasdaq +0.9% as chip stocks revive a 2nd session; Big Tech earnings loom this week",
 "Micron +5.7%, Broadcom +3.4% on Morgan Stanley's 'robust memory cycle' (+25% pricing) call",
 "Intel +6%: first chipmaker to deploy ASML High-NA EUV in production; reports Thursday",
 "AMD +5% into its 7/22-23 Advancing AI event on the Microsoft Helios rack-scale deal",
 "GOOGL + TSLA report Wed after the close, INTC Thu - the week's binary earnings wall",
 "QQQ $705.6 still ~1.5% under its 20-day ($716) - the chip bounce hasn't cleared the gate",
 "Palantir -0.8% but backed by a DA Davidson $175 upgrade + Burry covering his short",
 "Iran 10-day-ceasefire hopes ease oil; SPY near records (+0.5%)",
]

# ---- feed: prepend 2, keep newest ~40 ----
feed_new = [
 {"ts": TS, "type":"activity",
  "text":("10:54am management run: both books re-verified at the broker - PAPER 5/5 GTC-stopped zero-naked "
    "(AMD/PLTR/NVDA/CEG/SQQQ), LIVE flat $810 cash. Refreshed the live PLTR buy ticket in place (current levels, $122 stop). "
    "Gate shut day 6 (QQQ $705.6 < $716); holding the SQQQ hedge into Wed's earnings wall. No 3x chase.")},
 {"ts": TS, "type":"trade", "side":"buy", "status":"pending", "symbol":"PLTR",
  "detail":"5 sh @ ~$134 (live, staged)", "reaction":"hold",
  "text":("Refreshed the live PLTR buy ticket (2026-07-20-3) with current levels so it stays tappable and pings fresh - same trade, "
    "same $122 stop. It sat a day without a phone ping; this keeps the 1x leader one tap away instead of letting live rot in cash a 6th session.")},
]
d["feed"] = feed_new + d.get("feed", [])
d["feed"] = d["feed"][:40]

# ---- accountability (running intraday, honest, NOT final) ----
d["accountability"] = {
 "date":"2026-07-21","final":False,"grade":"C (running, intraday)",
 "headline":("Process improved over yesterday's D - I rotated EARLY in the morning (bought the pop_rank-1 AMD at the open in paper and "
   "refreshed the live leader ticket now, not a 3pm proposal), and I own the one clean ownable mover (AMD +4.9%). But capture is still ~0%: "
   "paper's ~-0.4% while the biggest watchlist movers run un-owned - SOXL +12.1% (the gated 3x), BE +11.7% (a dead-cat off the TD Cowen flush "
   "we correctly cut), INTC +6.1% (extended into Thu earnings) - and LIVE is still 100% cash awaiting the PLTR tap. The gate is on trial: it's "
   "kept us out of a SOXL pop that's faded 5 sessions straight, but if the chip bid holds this time it costs capture. Final grade at the close."),
 "capture":{"bestName":"SOXL (gated 3x) / BE (dead-cat)","bestPct":"+12.1% / +11.7%",
   "capturedPct":"paper ~-0.4%, live 0%","rate":"~0% - biggest movers un-ownable; AMD +4.9% owned in paper"},
 "missed":[
   {"from":"live cash","to":"PLTR (staged, untapped)","note":"live's been 100% cash all morning awaiting the tap while the RS leader + chip movers trade; refreshed the ticket so it pings fresh - only helps once tapped","delta":"opportunity, pending tap"},
   {"from":"paper SQQQ hedge (100 sh)","to":"a 1x leader","note":"the residual SQQQ (-4% today) still drags on a green tape; kept as Wed-earnings insurance but it caps today's capture","delta":"-$175 intraday drag"},
 ],
 "saved":[
   {"note":"Held the 3x gate a 6th day - didn't chase SOXL +12% / TQQQ +4% under a sub-20-day QQQ; the pop has faded 5 straight sessions","delta":"discipline intact"},
   {"note":"Both books verified at the broker: paper 5/5 GTC-stopped, live clean cash - never-naked held both books","delta":"safety intact"},
 ],
 "best":{"name":"AMD (30 sh @ $527.80, paper)","note":"owned the pop_rank-1 1x chip leader into its 7/22-23 event - the one clean ownable mover","delta":"+4.9% name, owned"},
 "worst":{"name":"SQQQ hedge (100 sh)","note":"the residual hedge (-4% today) is the book's biggest day drag; on a leash - cut on a QQQ $716 reclaim","delta":"-$175 intraday"},
 "avoided":{"worstName":"gated 3x chip chase (SOXL/TQQQ)","worstPct":"up now but round-tripped +13%->+9% intraday on the same 5-session fade pattern",
   "note":"the gate kept both books out of the leveraged pop that's the account's most expensive lesson","amount":"~$0 (didn't chase)","rate":"held the line"},
 "applying":"Applying the 7/20 D-lesson: rotate EARLY in the morning - bought AMD at the open (paper) + refreshed the live leader ticket now, not a 3pm proposal that can't fill.",
 "adjust":"If QQQ reclaims $716 on volume, cut the SQQQ hedge and rotate paper powder into the 1x leader; if the chip bid fades a 6th session, the hedge pays and the non-extended PLTR holds up better than the +6-12% names.",
}

# ---- score (benchmark/alpha recomputed real; TQQQ 7/2 $73.35 -> $70.40) ----
d["score"] = {"alphaPts":"-15.0","benchmark":"-4.0%","bestDay":"+3.2%",
 "bestDayName":"Jul 14 - CPI chip rally (settled)","winRate":"33%","tradeCount":6}

# ---- pending_tickets (id must match queue ticket 2026-07-20-3) ----
d["pending_tickets"] = [{
 "id":"2026-07-20-3","symbol":"PLTR","side":"buy","size":"$670","qty":5,
 "entry":"~$134 marketable - market open, approve = fills now","trigger":None,"stop":122,
 "bracket":"stop $122 GTC (below the $129-131 two-week base, -9%)",
 "thesis":("The funded live rotation into the 1x RS leader (no gate, Aug 3 earnings). PLTR -0.8% today, lagging the chip tape = a cheaper entry, "
   "not a broken thesis. Refreshed so it stays tappable; gets LIVE out of a 6th straight session of cash with a wide $122 stop. Approve anytime -> fills at market."),
}]

# ---- current-equity scalars if present ----
if isinstance(d.get("live"), dict) and "equity" in d["live"]: d["live"]["equity"] = 810.32
if isinstance(d.get("paper"), dict) and "equity" in d["paper"]: d["paper"]["equity"] = 89305.39

d["updated"] = TS

# ---- atomic write ----
fd, tmp = tempfile.mkstemp(dir=SITE, suffix=".tmp")
with os.fdopen(fd, "w") as f:
    json.dump(d, f, indent=1)
os.replace(tmp, P)

# ---- read-back verify ----
r = json.load(open(P))
cov = r["coverage"]
ranks = sorted(c["projection"]["pop_rank"] for c in cov)
ones = [c["ticker"] for c in cov if c["projection"]["pop_rank"] == 1]
assert r["updated"] == TS, "updated ts mismatch"
assert ranks == list(range(1,16)), f"ranks not 1-15 unique: {ranks}"
assert ones == ["AMD"], f"pop_rank 1 not unique AMD: {ones}"
assert r["pending_tickets"][0]["id"] == "2026-07-20-3", "pending id mismatch"
assert r["accountability"]["date"] == "2026-07-21" and r["accountability"]["final"] is False, "acct mismatch"
assert len(r["pulse"]) == 15 and r["pulse"][0]["ts"] == TS, "pulse mismatch"
assert len(cov) == 15, "coverage len"
print("VERIFY OK")
print("updated:", r["updated"])
print("pop_rank1:", ones, "| ranks:", ranks)
print("pending:", r["pending_tickets"][0]["id"], r["pending_tickets"][0]["symbol"], r["pending_tickets"][0]["size"])
print("acct:", r["accountability"]["date"], "final", r["accountability"]["final"], "|", r["accountability"]["grade"])
print("score:", r["score"]["benchmark"], r["score"]["alphaPts"])
print("pulse:", len(r["pulse"]), "| feed:", len(r["feed"]), "| headlines:", len(r["headlines"]))
