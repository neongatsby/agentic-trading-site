#!/usr/bin/env python3
"""Per-run publish (2026-07-21 05:43 ET pre-market heartbeat). Unique name; atomic write; read-back verify."""
import json, os, shutil, sys

SITE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(SITE, "engine-data.json")
BAK = os.path.join(SITE, "engine-data.backup-2026-07-21-0543.json")
TMP = os.path.join(SITE, ".engine-data.tmp-0543.json")
NEW_TS = "2026-07-21T05:43:00-04:00"

with open(SRC) as f:
    d = json.load(f)

# 1) backup the current good state first
shutil.copyfile(SRC, BAK)

# 2) prepend ONE pulse entry, keep newest-first ~15
new_pulse = {
    "ts": NEW_TS,
    "text": ("5:43am ET pre-market — independent broker re-reconciliation reconfirms both books CLEAN: "
             "LIVE flat ($810.32 cash, zero positions/orders, nothing naked); PAPER 4/4 GTC-stopped "
             "(PLTR 100/$125, NVDA 90/$186, SQQQ 310/$38, CEG 16/$236). Recomputed QQQ's 20-day MA fresh = "
             "$716.1 vs Monday's $696.06 close → still 2.8% under, leverage gate SHUT day 6. Overnight news "
             "changes nothing for the plan (ARK trimmed AMD, NVDA took a 9.3% Nebius stake, Cramer 'go to "
             "other sectors' but still backs NVDA/INTC; no fresh PLTR catalyst). PLTR live ticket 2026-07-20-3 "
             "stays staged for the OPEN — no blind pre-market trades, no new live surface pre-6am. "
             "Next: decisions + the PLTR fill land at the 9:30 open."),
    "hype": ("Checked everything again — both accounts clean, all stops set, nothing naked. Nasdaq's still under "
             "its line so no leverage; the PLTR buy's just waiting on the 9:30 open."),
}
d["pulse"] = [new_pulse] + d.get("pulse", [])
d["pulse"] = d["pulse"][:15]

# 3) bump top-level + coverage freshness timestamps (projection values validated vs this run's data, unchanged)
d["updated"] = NEW_TS
for c in d.get("coverage", []):
    c["updated"] = NEW_TS

# 4) accountability (7/20 final D), pending_tickets (PLTR 2026-07-20-3), score, status, headlines untouched — still correct

# 5) atomic write
with open(TMP, "w") as f:
    json.dump(d, f, ensure_ascii=False, indent=1)
os.replace(TMP, SRC)

# 6) read-back verify
with open(SRC) as f:
    v = json.load(f)
assert v["updated"] == NEW_TS, "updated ts mismatch"
assert v["pulse"][0]["ts"] == NEW_TS, "pulse not prepended"
assert len(v["pulse"]) == 15, "pulse len != 15"
pr1 = [c["ticker"] for c in v["coverage"] if c.get("projection", {}).get("pop_rank") == 1]
assert pr1 == ["PLTR"], f"pop_rank-1 not unique PLTR: {pr1}"
acct = v["accountability"]
assert acct["date"] == "2026-07-20" and acct["grade"] == "D" and acct["final"] is True, "accountability drifted"
pt = [t["id"] for t in v.get("pending_tickets", [])]
assert pt == ["2026-07-20-3"], f"pending_tickets drifted: {pt}"
print("OK publish 0543")
print("  updated:", v["updated"])
print("  pulse[0].ts:", v["pulse"][0]["ts"], "| len:", len(v["pulse"]))
print("  pop_rank-1:", pr1)
print("  accountability:", acct["date"], acct["grade"], "final=", acct["final"])
print("  pending_tickets:", pt)
print("  score:", json.dumps(v.get("score")))
