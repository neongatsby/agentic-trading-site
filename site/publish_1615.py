#!/usr/bin/env python3
"""Post-close finalize publish for 2026-07-21. Atomic write + backup + verify (per OPS-ALERT-engine-data-clobber)."""
import json, os, shutil, sys, tempfile

SITE = os.path.dirname(os.path.abspath(__file__))
PATH = os.path.join(SITE, "engine-data.json")
TS = "2026-07-21T16:15:00-04:00"

d = json.load(open(PATH))

# ---- backup the good pre-write state ----
bak = os.path.join(SITE, "engine-data.backup-2026-07-21-1615.json")
shutil.copyfile(PATH, bak)

# ---- updated ----
d["updated"] = TS

# ---- accountability (FINAL) ----
d["accountability"] = {
  "date": "2026-07-21",
  "final": True,
  "grade": "D+",
  "headline": ("A +8-15% memory-led risk-on rip and we captured ~3% of it: PAPER finally owned the RIGHT theme "
    "(AMD/SMR/OKLO/VRT/CEG/NVDA, all green, all 6 GTC-stopped, zero naked) - real credit - but mid-day entries "
    "+ a 39%-of-book NVDA anchor (+1.9%) held it to +0.42%, and LIVE sat 100% cash a 6TH straight session for 0% capture. "
    "The regime gate that rightly saved us through the 7/14-7/20 wreck has become a cash-trap on the way back UP: it has a "
    "fast EXIT but no RE-ENTRY. Genuine saves - didn't chase parabolic MU/BE/SOXL at the highs, cut the SQQQ hedge (-5.6%) "
    "+ flat PLTR (-1.6%) into the rip, owned none of the -16% SOXS trap, held every stop. Fix is staged: NVDA live swing fires at tomorrow's open."),
  "capture": {
    "bestName": "SOXL +15.7% (3x, gated) / BE +14.8% (watched, sold 7/20) / MU +12.0%; best OWNED = SMR +9.3% & AMD +8.1% (paper)",
    "bestPct": "+15.7% (SOXL) / +14.8% (BE)",
    "capturedPct": "paper +0.42%, live 0%",
    "rate": "~3% (paper +0.42% div SOXL +15.7%); live 0% - owned the right theme but mid-day tail + NVDA anchor + live in cash"
  },
  "missed": [
    {"from": "BE (live, sold 3 sh @ $203.03 on 7/20 delay catalyst)", "to": "holding BE",
     "note": "BE V-reversed +14.8% to $226.50 today - the exit was on a verified catalyst but got run over; the day's biggest real-money miss",
     "delta": "~+$70 vs held"},
    {"from": "live cash (6th straight day)", "to": "any leader at the open",
     "note": "live captured 0% of a +8-15% rip; a single ~$600 open swing in AMD/SMR would've made ~+$45 - the gate has no re-entry trigger",
     "delta": "~+$45 forgone"},
    {"from": "NVDA anchor (39% of paper, +1.9%)", "to": "the +6-9% pure-plays (SMR/OKLO/AMD)",
     "note": "over-weighting the slow mega-cap laggard capped paper's blended capture at +0.42%",
     "delta": "weight drag"}
  ],
  "saved": [
    {"note": "Didn't chase parabolic MU +12% / BE +15% / SOXL +15.7% at the highs - the top-tick chase the Playbook names", "delta": "avoided chase"},
    {"note": "Cut the SQQQ hedge (fell -5.6% as QQQ ripped) + the flat/red PLTR laggard (-1.6%) into the rally", "delta": "redeployed"},
    {"note": "Owned NONE of the -16.3% SOXS inverse trap", "delta": "avoided -16%"},
    {"note": "Zero naked - all 6 paper positions GTC-stopped, verified at the broker this run", "delta": "risk bounded"}
  ],
  "best": {"name": "AMD (paper, 30 sh)", "note": "the semis leader we actually owned - stock +8.1%, our position +3.3% from the mid-day add", "delta": "+$516 paper"},
  "worst": {"name": "BE (live)", "note": "sold $203 on 7/20, reversed +14.8% to $226.50 - the catalyst exit got run over by the theme", "delta": "~-$70 opportunity"},
  "capture_trend": "49% (7/14) -> ~0% x4 (7/15-7/20) -> ~3% (7/21) - still not off the floor; live 0% is the anchor",
  "projection_grade": ("MISS - pop_rank-1 NVDA closed +1.9% (near the +2.5% call) but was the board's LAGGARD, not a pop; the real "
    "pops (SOXL/BE/MU/SMR +9-16%) were owned only in paper, partially. Calling the laggard 'pop_rank 1' games the metric. Tracker -> 2-for-4."),
  "applying": "Playbook: regime gate + don't-chase-extension - protected capital on the way down, but capped upside on the rip (the tension, named).",
  "adjust": ("FIRE the staged NVDA swing at the 7/22 open (that IS the re-entry) + add a gate RE-ENTRY trigger: 2 green risk-on days "
    "+ QQQ within ~1% of its 20-day + theme up on a real catalyst = re-enter the leader at the next open, don't wait for the textbook reclaim.")
}

# ---- score ----
d["score"] = {"alphaPts": "-16.3", "benchmark": "-2.7%", "bestDay": "+3.2%",
              "bestDayName": "Jul 14 - CPI chip rally (settled)", "winRate": "33%", "tradeCount": 6}

# ---- status (Morning -> Afternoon -> Evening) ----
d["status"] = [
  {"session": "Morning", "text": "Cut SQQQ + PLTR drags"},
  {"session": "Afternoon", "text": "Leaders held; NVDA staged for open"},
  {"session": "Evening", "text": "Final D+: ~3% capture; NVDA armed"}
]

# ---- headlines ----
d["headlines"] = [
  "Close 7/21: Nasdaq-100 +1.5% (29,022), S&P +0.9% record - memory-led semis rip, day 2",
  "Micron +12%, INTC +8.6%, AMD +8.1%, SOXL +15.7% - the 2-day AI/memory recovery",
  "BE +14.8% V-reversal to $226.50 - we sold 7/20 on the verified delay catalyst (a live miss)",
  "Wed 7/22 BINARY: GOOGL + TSLA report after the close - the tape positions into it all day",
  "AMD 'Advancing AI 2026' event Wed 7/22 - a same-day catalyst (but +8% already extended)",
  "NVDA +1.9% - the complex laggard (9.3% Nebius stake); our live swing, staged for the open",
  "Regime: QQQ closed $708.8, -0.8% under its $714.7 20-day - 3x powder still parked",
  "Paper owns AMD/SMR/OKLO/VRT/CEG/NVDA (all GTC-stopped); live flat $810 cash, 6th day"
]

# ---- pulse (prepend ONE final entry, keep newest ~15) ----
pulse_new = {
  "ts": TS,
  "text": ("4:15p, FINAL - Grade D+. Honest: a +8-15% memory-led rip (SOXL +15.7%, MU +12%, AMD +8.1%) and we captured ~3%. "
    "Paper finally owns the RIGHT theme - AMD/SMR/OKLO/VRT/CEG/NVDA, every one green, all 6 GTC-stopped, zero naked - but "
    "mid-day entries + a 39%-of-book NVDA anchor (+1.9%) held it to +0.42%, and live sat cash a 6th straight day (0%). Real "
    "credit: didn't chase parabolic MU/BE/SOXL at the highs, cut the SQQQ hedge (-5.6%) + flat PLTR into the rip, dodged the "
    "-16% SOXS trap, held every stop. The lesson I'm acting on: the gate has a fast EXIT but no RE-ENTRY - it kept live out of "
    "the whole round-trip back up. Fix is staged - the NVDA swing fires at tomorrow's open (approve anytime, $186 stop); that's "
    "the re-entry. Careful into Wed's after-close GOOGL/TSLA prints."),
  "hype": ("Rough grade - a big up day and we only caught a sliver, and live's still in cash. Fix's set: the NVDA buy fires at tomorrow's open.")
}
d["pulse"] = [pulse_new] + d.get("pulse", [])[:14]

# ---- feed (prepend ONE final activity item, keep ~40) ----
feed_new = {
  "type": "activity",
  "ts": TS,
  "text": ("4:15pm FINAL - Grade D+ on the day. +8-15% memory-led rip; paper owned the right theme (AMD/SMR/OKLO/VRT/CEG/NVDA, "
    "all 6 GTC-stopped, zero naked) but mid-day entries + a 39%-of-book NVDA anchor (+1.9%) held it to +0.42%, and live sat cash "
    "a 6th straight day (0% capture). Saves: no parabolic chase, cut SQQQ/PLTR into the rip, dodged the -16% SOXS trap. Lesson: "
    "the gate has no RE-ENTRY - fix staged, NVDA swing fires at tomorrow's open, $186 stop.")
}
d["feed"] = [feed_new] + d.get("feed", [])[:40]

# ---- activity (top-level; prepend one engine entry, keep ~20) ----
act_new = {"ts": TS, "kind": "engine",
  "title": ("Tue 7/21 ~4:15pm ET (post-close FINAL). Grade D+: +8-15% rip, ~3% capture. Paper 6/6 GTC-stopped in the day's "
    "leaders (zero naked); live cash a 6th day (0%). Lesson: regime gate has a fast exit but no re-entry -> NVDA live swing staged "
    "to fire at the 7/22 open. Projection MISS (NVDA laggard, not the pop); tracker 2-for-4.")}
d["activity"] = [act_new] + d.get("activity", [])[:20]

# ---- coverage: final EOD chg_pct + TOMORROW (7/22) projections (exactly one pop_rank:1) ----
COV = {
  "AMD":  {"chg": "+8.1%",  "tgt": 3.0,  "conf": "med", "pop": 1,  "basis": "Advancing AI 2026 event 7/22 - same-day catalyst (own it paper)", "path": [1.5, 2.4, 3.0]},
  "NVDA": {"chg": "+1.9%",  "tgt": 2.5,  "conf": "med", "pop": 2,  "basis": "laggard catch-up if theme holds; live swing, no own-binary", "path": [1.0, 1.8, 2.5]},
  "RGTI": {"chg": "+7.2%",  "tgt": 2.5,  "conf": "low", "pop": 3,  "basis": "quantum high-beta - moves most on a risk-on tape"},
  "SMR":  {"chg": "+9.3%",  "tgt": 2.0,  "conf": "low", "pop": 4,  "basis": "nuclear RS leader; rides risk-on but extended +9%"},
  "OKLO": {"chg": "+6.3%",  "tgt": 2.0,  "conf": "low", "pop": 5,  "basis": "AI-power beta near breakout; tracks the tape"},
  "MU":   {"chg": "+12.0%", "tgt": 1.0,  "conf": "low", "pop": 6,  "basis": "memory leader but very extended +12% - cool-off risk"},
  "RKLB": {"chg": "+5.2%",  "tgt": 2.0,  "conf": "low", "pop": 7,  "basis": "space/defense beta rode the risk-on day"},
  "VRT":  {"chg": "+4.4%",  "tgt": 1.5,  "conf": "low", "pop": 8,  "basis": "AI-power infra; near our entry, steadier"},
  "IONQ": {"chg": "+3.7%",  "tgt": 2.0,  "conf": "low", "pop": 9,  "basis": "quantum beta follows the tape"},
  "BE":   {"chg": "+14.8%", "tgt": 0.0,  "conf": "low", "pop": 10, "basis": "spent parabolic +15% - we're OUT, not chasing"},
  "CEG":  {"chg": "+3.5%",  "tgt": 1.0,  "conf": "low", "pop": 11, "basis": "nuclear utility; steadier lower-beta hold"},
  "TSLA": {"chg": "+2.5%",  "tgt": 1.5,  "conf": "low", "pop": 12, "basis": "reports Wed after close - binary; avoid into the print"},
  "SOXL": {"chg": "+15.7%", "tgt": 1.5,  "conf": "low", "pop": 13, "basis": "3x semis on a hot tape - GATED (QQQ<20d)"},
  "TQQQ": {"chg": "+5.5%",  "tgt": 1.0,  "conf": "low", "pop": 14, "basis": "3x Nasdaq - GATED until QQQ reclaims its 20-day"},
}
for c in d.get("coverage", []):
  t = c.get("ticker")
  if t in COV:
    m = COV[t]
    c["chg_pct"] = m["chg"]
    proj = {"target_pct": m["tgt"], "confidence": m["conf"], "basis": m["basis"], "pop_rank": m["pop"]}
    if "path" in m:
      proj["path_pct"] = m["path"]
    c["projection"] = proj
    c["updated"] = "7/21 4:15p close"

# ---- paper / live equity blocks ----
if "paper" in d:
  d["paper"]["equity"] = 89997.84
  d["paper"]["updated"] = TS
  ec = d["paper"].get("equity_curve", [])
  if ec and ec[-1].get("date") == "Jul 21":
    ec[-1]["value"] = 89997.84
  d["paper"]["equity_note"] = ("Paper ~$90.0k (+0.42% vs Mon settled $89,617, provisional post-close mark) - owns the day's "
    "leaders (AMD +8.1% / SMR +9.3% / OKLO +6.3% / VRT +4.4% / CEG +3.5% / NVDA +1.9%); the modest gain reflects mid-day "
    "entries (tail only) + the 39%-of-book NVDA anchor. All 6 GTC-stopped, zero naked.")

if "live" in d:
  d["live"]["equity"] = 810.32
  d["live"]["cash"] = 810.32
  d["live"]["positions"] = []
  d["live"]["updated"] = TS
  ec = d["live"].get("equity_curve", [])
  if ec and ec[-1].get("date") == "Jul 21":
    ec[-1]["value"] = 810.32
  d["live"]["equity_note"] = ("LIVE flat $810.32 cash / zero positions / zero naked (6th straight cash session). 1 pending ticket "
    "= BUY NVDA 3 sh (~$207, $186 stop), staged to fill at the 7/22 open - approve anytime.")

# ---- pending_tickets: keep NVDA, clean the entry text now the 4pm close has passed ----
d["pending_tickets"] = [{
  "id": "2026-07-21-1",
  "symbol": "NVDA",
  "side": "buy",
  "size": "$633",
  "qty": 3,
  "entry": "~$207 - approve ANYTIME -> fills at the 7/22 OPEN (multi-day swing, PDT-free, 0/3 day-trades used). Marketable-limit $211 gives a gap-up cushion.",
  "trigger": None,
  "stop": 186,
  "bracket": "stop $186 GTC (below the late-June $192 base, -10.2%)",
  "thesis": ("Ends a 6th day of live cash by owning the leading AI-infra/semis theme via the NON-extended leader. NVDA +1.9% today "
    "LAGGED the +8-12% AMD/MU/INTC complex = a cheaper entry in the group leader; it just took a 9.3% stake in neocloud Nebius and "
    "Micron's memory blowout reads straight through to NVDA HBM/GPU demand. No earnings binary until late Aug (AMD 8/4; GOOGL/TSLA "
    "print Wed - NVDA doesn't). Wide $186 stop. This IS the gate re-entry - fires at the open (the 7/20 execution-timing fix).")
}]

# ---- ATOMIC WRITE ----
fd, tmp = tempfile.mkstemp(dir=SITE, suffix=".tmp")
with os.fdopen(fd, "w") as f:
  json.dump(d, f, ensure_ascii=False, indent=1)
os.replace(tmp, PATH)

# ---- VERIFY read-back ----
v = json.load(open(PATH))
assert v["updated"] == TS, "updated mismatch"
assert v["accountability"]["final"] is True, "final not True"
assert v["accountability"]["grade"] == "D+", "grade mismatch"
assert len(v["pending_tickets"]) == 1 and v["pending_tickets"][0]["symbol"] == "NVDA", "pending mismatch"
pops = sorted(c["projection"]["pop_rank"] for c in v["coverage"] if c.get("projection"))
assert pops.count(1) == 1, "must be exactly one pop_rank:1"
print("OK verified.")
print(" updated     :", v["updated"])
print(" grade/final :", v["accountability"]["grade"], "/", v["accountability"]["final"])
print(" score       :", v["score"])
print(" pop_rank 1  :", [c["ticker"] for c in v["coverage"] if c.get("projection", {}).get("pop_rank") == 1])
print(" pending     :", v["pending_tickets"][0]["symbol"], v["pending_tickets"][0]["qty"], "sh, stop", v["pending_tickets"][0]["stop"])
print(" ranks       :", pops)
print(" paper eq    :", v["paper"]["equity"], "| live eq :", v["live"]["equity"])
