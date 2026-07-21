#!/usr/bin/env python3
"""Per-run publish (unique name) — 2026-07-20 7:45pm ET evening refresh.
Follows OPS-ALERT-engine-data-clobber rules: unique filename, atomic write
(temp -> os.replace), read-back verification, backup before overwrite."""
import json, os, tempfile, shutil, sys

SITE = os.path.dirname(os.path.abspath(__file__))
PATH = os.path.join(SITE, "engine-data.json")

with open(PATH) as f:
    d = json.load(f)

# --- Guard: only proceed if the base is today's known-good state ---
assert d.get("accountability", {}).get("date") == "2026-07-20", \
    f"unexpected accountability date {d.get('accountability',{}).get('date')}"
assert d.get("accountability", {}).get("grade") == "D", \
    f"unexpected grade {d.get('accountability',{}).get('grade')}"
pend = d.get("pending_tickets", [])
assert len(pend) == 1 and pend[0].get("symbol") == "PLTR", \
    f"unexpected pending_tickets {pend}"

# --- Backup the current good state before touching it ---
shutil.copy(PATH, os.path.join(SITE, "engine-data.backup-2026-07-20-1945.json"))

TS = "2026-07-20T19:45:00-04:00"

new_pulse = {
    "ts": TS,
    "text": ("7:45pm / near the after-hours close — final evening check. Re-verified both books vs the "
             "broker: unchanged and clean (LIVE flat, $810.32 cash, zero positions/orders, nothing naked; "
             "PAPER's CEG 16 / NVDA 90 / PLTR 100 / SQQQ 310 all GTC-stopped). Re-ran the gate off settled "
             "daily bars — QQQ $696.06 vs a 20-day of $716.1 = 2.8% under, SHUT a 5th straight day — so the "
             "paper SQQQ hedge stays on into Wed's GOOGL/TSLA prints. Tomorrow is the fix for today's D: the "
             "PLTR open-buy (5 sh, $122 stop) is staged to get LIVE out of cash and into the RS leader at the "
             "OPEN, not at 3pm like today. At the open I react to the fork — QQQ reclaims $716 → cut the hedge "
             "+ re-add gated names; loses $695 → let SQQQ run."),
    "hype": ("Last look tonight — nothing moved, both books clean. PLTR buy's locked for the open so we get in "
             "the leader early instead of late, and the hedge stays on into Google/Tesla earnings."),
}

pulse = d.get("pulse", [])
# avoid duplicate if a 19:45 entry somehow already exists
pulse = [p for p in pulse if p.get("ts") != TS]
pulse.insert(0, new_pulse)
d["pulse"] = pulse[:15]

d["updated"] = TS

# --- Atomic write: temp in same dir -> os.replace ---
fd, tmp = tempfile.mkstemp(dir=SITE, prefix=".engine-data.", suffix=".tmp")
with os.fdopen(fd, "w") as f:
    json.dump(d, f, ensure_ascii=False, indent=1)
os.replace(tmp, PATH)

# --- Read-back verification ---
with open(PATH) as f:
    chk = json.load(f)
ok = (
    chk.get("updated") == TS
    and chk.get("accountability", {}).get("final") is True
    and chk.get("accountability", {}).get("grade") == "D"
    and len(chk.get("pending_tickets", [])) == 1
    and chk["pending_tickets"][0].get("symbol") == "PLTR"
    and chk.get("pulse", [{}])[0].get("ts") == TS
)
print("READBACK_OK" if ok else "READBACK_FAIL")
print("updated:", chk.get("updated"))
print("accountability:", chk["accountability"]["grade"], "final=", chk["accountability"]["final"])
print("pending:", [p["symbol"] for p in chk.get("pending_tickets", [])])
print("pulse[0]:", chk["pulse"][0]["ts"], "| count:", len(chk["pulse"]))
print("coverage names:", len(chk.get("coverage", [])))
if not ok:
    sys.exit(1)
