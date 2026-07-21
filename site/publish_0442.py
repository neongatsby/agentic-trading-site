#!/usr/bin/env python3
"""Per-run publish (2026-07-21 04:42 ET pre-market). Light, non-clobbering surgical update.
Atomic write (temp -> os.replace) + read-back verify, per OPS-ALERT-engine-data-clobber rules."""
import json, os, tempfile, sys

SITE = os.path.dirname(os.path.abspath(__file__))
PATH = os.path.join(SITE, "engine-data.json")
TS = "2026-07-21T04:42:00-04:00"

with open(PATH) as f:
    d = json.load(f)

# --- Backup the current (good, 04:12) state first ---
bak = os.path.join(SITE, "engine-data.backup-2026-07-21-0442.json")
with open(bak, "w") as f:
    json.dump(d, f, ensure_ascii=False, indent=1)

# --- 1. Prepend ONE pulse (newest first) ---
pulse_text = (
    "4:42am ET — independent broker reconciliation reconfirms both books CLEAN: LIVE flat "
    "($810.32 cash, zero positions/orders, nothing naked); PAPER 4/4 GTC-stopped (PLTR 100/$125, "
    "NVDA 90/$186, CEG 16/$236, SQQQ 310/$38, zero naked). Gate still SHUT day 6 (QQQ $696 vs its "
    "~$716 20-day; SPY $742 near records → chip-specific, not broad). Calendar correction: the "
    "mega-cap AI prints (GOOGL/MSFT/META) are NOT this week — the only watchlist catalyst is TSLA "
    "Wed 7/22 after the close (~7.6% implied), with INTC Thu; today's reporters (GM, Capital One) "
    "aren't ours, so it's a pure positioning day. PLTR open-buy (ticket 2026-07-20-3, 5 sh, $122 stop) "
    "stands to fill at the 9:30 open — yesterday's cash-lock fix. No new live ticket surfaced "
    "pre-6am (timing rule); paper holds into the QQQ $716-reclaim / $695-break fork. Day-trade 0/3."
)
pulse_hype = (
    "Double-checked everything against the broker — both accounts clean, nothing unprotected. "
    "Turns out big tech earnings aren't this week (just Tesla Wed), so today's quiet; PLTR's still set "
    "to buy at the open."
)
d.setdefault("pulse", []).insert(0, {"ts": TS, "text": pulse_text, "hype": pulse_hype})
d["pulse"] = d["pulse"][:15]

# --- 2. Prepend ONE feed activity item ---
feed_text = (
    "4:42am pre-market: independent broker reconcile — LIVE flat ($810.32 cash, zero-naked), PAPER "
    "4/4 GTC-stopped (PLTR/NVDA/CEG/SQQQ). Gate shut day 6 (QQQ $696 vs $716 20-day). Calendar fix: "
    "mega-cap AI names (GOOGL/MSFT/META) aren't this week — only TSLA Wed 7/22 AMC + INTC Thu are "
    "watchlist-relevant; today's a positioning day. PLTR open-buy stands. Day-trade 0/3."
)
d.setdefault("feed", []).insert(0, {"ts": TS, "type": "activity", "text": feed_text})

# --- 3. Fix the earnings-calendar headline (was: "GOOGL, TSLA and TXN all Wed") ---
hl = d.get("headlines", [])
for i, h in enumerate(hl):
    if isinstance(h, str) and h.startswith("Heavy earnings week"):
        hl[i] = (
            "Earnings calendar (corrected): TSLA reports Wed 7/22 after the close (~7.6% implied move, "
            "record Q2 deliveries eyed); INTC Thu 7/23. The mega-cap AI names (GOOGL/MSFT/META) are NOT "
            "this week — today's GM/Capital One prints aren't on the watchlist, so it's a positioning day."
        )
        break

# --- 4. Minor status refresh (Morning card) ---
for card in d.get("status", []):
    if card.get("session") == "Morning":
        card["text"] = "Gate shut d6; positioning day"
        break

# --- 5. Bump the top-level timestamp ---
d["updated"] = TS

# --- Atomic write (temp -> os.replace) ---
fd, tmp = tempfile.mkstemp(dir=SITE, prefix=".engine-data.", suffix=".tmp")
try:
    with os.fdopen(fd, "w") as f:
        json.dump(d, f, ensure_ascii=False, indent=1)
    os.replace(tmp, PATH)
finally:
    if os.path.exists(tmp):
        os.remove(tmp)

# --- Read-back verify ---
with open(PATH) as f:
    v = json.load(f)
assert v["updated"] == TS, f"updated mismatch: {v['updated']}"
assert v["accountability"]["date"] == "2026-07-20" and v["accountability"]["final"] is True and v["accountability"]["grade"] == "D", "accountability drifted"
assert len(v["pending_tickets"]) == 1 and v["pending_tickets"][0]["id"] == "2026-07-20-3" and v["pending_tickets"][0]["symbol"] == "PLTR", "pending ticket drifted"
assert v["pulse"][0]["ts"] == TS and v["pulse"][0]["text"].startswith("4:42am"), "pulse not prepended"
assert v["feed"][0]["ts"] == TS, "feed not prepended"
assert len(v.get("coverage", [])) == 15, "coverage count changed"
assert not any(isinstance(h, str) and "GOOGL, TSLA and TXN" in h for h in v["headlines"]), "stale GOOGL headline remains"
print("PUBLISH-0442-OK")
print("updated:", v["updated"])
print("pulse[0].ts:", v["pulse"][0]["ts"])
print("accountability:", v["accountability"]["date"], v["accountability"]["final"], v["accountability"]["grade"])
print("pending:", v["pending_tickets"][0]["id"], v["pending_tickets"][0]["symbol"])
print("coverage:", len(v["coverage"]), "names; headlines:", len(v["headlines"]))
