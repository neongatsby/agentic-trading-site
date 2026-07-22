#!/usr/bin/env python3
"""Per-run publish for the 8:38p ET evening heartbeat (2026-07-21).
Surgical edits only: refresh timestamp, prepend one pulse, fold in the fresh
OKLO/X-Energy $200M nuclear-for-AI catalyst into the pop board + headlines.
Grade stays FINAL D+ (not re-graded). Atomic write + verify per OPS-ALERT."""
import json, os, shutil, sys

SITE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(SITE, "engine-data.json")
BAK = os.path.join(SITE, "engine-data.backup-2026-07-21-2038.json")
TMP = os.path.join(SITE, "engine-data.json.tmp")
TS = "2026-07-21T20:38:00-04:00"

# 1) backup current good state first
shutil.copyfile(SRC, BAK)

d = json.load(open(SRC))

# 2) timestamp
d["updated"] = TS

# 3) prepend one pulse item (newest first), keep ~15
pulse_item = {
    "ts": TS,
    "text": ("8:38p heartbeat - caught a FRESH after-close catalyst: a Trump/DOE $200M program to "
             "fast-track nuclear reactors for AI data centers taps OKLO + X-Energy (alongside Microsoft "
             "and NVDA). OKLO jumped ~+10% AH, X-Energy +12%. We already own OKLO (200 sh) and SMR (700 sh) "
             "in paper, both GTC-stopped - the nuclear-for-AI leg now has a government tailwind into "
             "tomorrow, so OKLO moves to pop_rank 1 (AMD's 'Advancing AI' event = 2). NVDA is named in the "
             "program too, a small extra tailwind for the live swing, still armed for the 7/22 open. Both "
             "books == broker: LIVE flat $810.32 cash (nothing naked), PAPER 6 names all stopped, zero "
             "naked. Grade stays final D+."),
    "hype": ("New tonight - a $200M gov push to build nuclear for AI names our OKLO (we own it). "
             "Bumped it to my top pick for tomorrow; NVDA's still set to buy at the open."),
}
d["pulse"] = [pulse_item] + d.get("pulse", [])
d["pulse"] = d["pulse"][:15]

# 4) coverage edits, by ticker
def cov(t):
    for c in d["coverage"]:
        if c["ticker"] == t:
            return c
    raise KeyError(t)

UPD = "7/21 8:38p (7/22 plan)"

# OKLO -> pop_rank 1 on the fresh federal catalyst
o = cov("OKLO")
o["projection"] = {"target_pct": 6, "confidence": "med",
                   "basis": "fresh $200M Trump/DOE nuclear-for-AI program; +10% AH",
                   "pop_rank": 1, "path_pct": [2, 4, 6]}
o["updated"] = UPD
o["thesis"] = ("**FRESH CATALYST (after-close 7/21): OKLO joins a Trump/DOE $200M program to fast-track "
               "nuclear reactors for AI data centers - jumped ~+10% AH.** Started 200 sh mid-day as the "
               "nuclear group broke higher; ~flat from our $43.92 entry, $39 stop under it. Government "
               "tailwind now under the whole nuclear-for-AI leg.")
o["hold_reason"] = ("Nuclear/AI-power name we own (200 sh from ~$43.92 mid-day, ~flat, $39 stop). Tonight it "
                    "got a real catalyst: the Trump administration/DOE tapped OKLO + X-Energy for a $200M "
                    "program to speed nuclear reactors for AI data centers, and it popped ~10% after-hours. "
                    "We're holding into tomorrow to let the government-backed nuclear-for-AI theme run; the "
                    "$39 stop is our line if the pop fades.")

# AMD -> pop_rank 2 (its own dated 'Advancing AI' event 7/22)
a = cov("AMD")
a["projection"]["pop_rank"] = 2
a["updated"] = UPD

# SMR -> pop_rank 3, bump on nuclear sympathy
s = cov("SMR")
s["projection"] = {"target_pct": 3, "confidence": "med",
                   "basis": "nuclear-for-AI theme; OKLO/X-Energy $200M program sympathy",
                   "pop_rank": 3}
s["updated"] = UPD

# NVDA -> pop_rank 4 (laggard catch-up + named in the program; our live swing)
n = cov("NVDA")
n["projection"]["pop_rank"] = 4
n["projection"]["basis"] = "AI-infra laggard catch-up; named in the $200M AI-energy program; our live swing"
n["updated"] = UPD

# RGTI -> pop_rank 5 (bumped down one to make room)
r = cov("RGTI")
r["projection"]["pop_rank"] = 5
r["updated"] = UPD

# assert pop_rank uniqueness across the board
ranks = [c["projection"]["pop_rank"] for c in d["coverage"] if "projection" in c and "pop_rank" in c["projection"]]
assert len(ranks) == len(set(ranks)), f"pop_rank collision: {sorted(ranks)}"
assert ranks.count(1) == 1 and cov("OKLO")["projection"]["pop_rank"] == 1, "OKLO must be sole pop_rank 1"

# 5) headlines (most relevant first), keep 8
d["headlines"] = [
    "AFTER-CLOSE 7/21: Trump/DOE $200M program taps OKLO + X-Energy (with MSFT, NVDA) to fast-track nuclear reactors for AI data centers - OKLO +10% AH, XE +12%",
    "Close 7/21: S&P record 7,509 (+0.9%), Nasdaq +1.3% - memory-led semi rip a 2nd day (SOX +5%)",
    "Wed 7/22 BINARY WALL: GOOGL + TSLA report after the close, INTC follows Thursday - tape positions all day",
    "AMD +8% on a Microsoft AI deal; 'Advancing AI 2026' event Wed 7/22 (MI355X launch, MI400 update)",
    "NVDA 9.3% / ~$5B Nebius stake CONFIRMED in SEC filing; also named in the $200M AI-energy program - live swing armed for the 7/22 open",
    "Micron +12%, SanDisk +14% - memory super-cycle; S.Korea export data confirms AI demand",
    "Regime: QQQ $708.8 still ~0.8% under its $714.7 20-day - 3x powder parked for a confirmed reclaim",
    "Paper owns AMD/SMR/OKLO/VRT/CEG/NVDA (all GTC-stopped); live flat $810, 6th cash session",
]

# 6) status: refresh Evening card
for st in d.get("status", []):
    if st.get("session") == "Evening":
        st["text"] = "Caught OKLO nuclear catalyst"

# 7) paper/live blocks: refresh updated ts + note the catalyst (values unchanged)
d["paper"]["updated"] = TS
pn = d["paper"].get("equity_note", "")
if "nuclear leg" not in pn:
    d["paper"]["equity_note"] = pn + " | AH 7/21: OKLO/SMR nuclear leg got a fresh $200M federal nuclear-for-AI catalyst (bullish into 7/22)."
d["live"]["updated"] = TS

# 8) guardrails: do NOT let this run touch the final grade or the staged ticket
assert d["accountability"]["final"] is True and d["accountability"]["grade"] == "D+", "grade must stay final D+"
assert any(t.get("id") == "2026-07-21-1" and t.get("symbol") == "NVDA" for t in d["pending_tickets"]), "NVDA ticket must persist"

# 9) atomic write
with open(TMP, "w") as f:
    json.dump(d, f, indent=1, ensure_ascii=False)
    f.flush()
    os.fsync(f.fileno())
os.replace(TMP, SRC)

# 10) verify read-back
v = json.load(open(SRC))
assert v["updated"] == TS
assert v["pulse"][0]["ts"] == TS
assert v["accountability"]["final"] is True and v["accountability"]["grade"] == "D+"
assert any(t.get("id") == "2026-07-21-1" for t in v["pending_tickets"])
assert next(c for c in v["coverage"] if c["ticker"] == "OKLO")["projection"]["pop_rank"] == 1
print("OK publish_2038: updated", v["updated"],
      "| pulse[0]", v["pulse"][0]["ts"],
      "| grade", v["accountability"]["grade"], "final", v["accountability"]["final"],
      "| pending", [t["symbol"] for t in v["pending_tickets"]],
      "| OKLO pop_rank", next(c for c in v["coverage"] if c["ticker"] == "OKLO")["projection"]["pop_rank"],
      "| coverage n", len(v["coverage"]))
