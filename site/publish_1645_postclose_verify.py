import json, os, shutil, datetime

SRC = "engine-data.json"
BAK = "engine-data.backup-2026-07-21-1645.json"
TMP = ".engine-data.tmp-1645"

# Backup first
shutil.copyfile(SRC, BAK)
d = json.load(open(SRC))

TS = "2026-07-21T16:45:00-04:00"

pulse_text = ("4:45p post-close (SETTLED verify) - Re-checked the whole day at the real close and the D+ grade holds on "
"SETTLED prices, not an intraday mark. Independently reconciled both books to the broker: LIVE flat $810.32 cash "
"(6th straight session, 0% capture on the real money), PAPER 6 names (AMD/SMR/OKLO/VRT/CEG/NVDA) all GTC-stopped, "
"zero naked. Coverage %s tie to the official closes (NVDA +1.9%, AMD +8.1%, SMR +9.3%, MU +12.0%, BE +14.8%, "
"SOXL +15.7% gated); paper's +0.42% is off official closes, not the inflated after-hours tick. QQQ closed $708.8, "
"still ~0.8% under its $714.7 20-day, so the ~$16k 3x powder stays parked into Wed's GOOGL/TSLA prints. One live "
"lever, untouched and ready: the NVDA swing ticket is staged AND already pinged to the phone - one tap fills it at "
"tomorrow's open, $186 stop. That tap is the re-entry. No new trade - post-close, plan set, don't chase extension into a binary.")
pulse_hype = ("Double-checked everything at the real close: grade holds, nothing's naked, live's still in cash. "
"The NVDA buy is already on your phone - one tap and it's in at tomorrow's open.")

d["pulse"].insert(0, {"ts": TS, "text": pulse_text, "hype": pulse_hype})
d["pulse"] = d["pulse"][:15]

activity_title = ("Tue 7/21 ~4:45pm ET (post-close, SETTLED verify). Independently reconciled both books to the broker at "
"the real close: LIVE flat $810.32 cash (6th day, 0% capture on real money), PAPER 6/6 GTC-stopped "
"(AMD/SMR/OKLO/VRT/CEG/NVDA), zero naked. Confirmed the D+ grade holds on SETTLED closes - coverage %s tie to "
"official closes; paper +0.42% off official marks (not the after-hours OKLO tick). QQQ closed $708.8 < $714.7 "
"20-day -> ~$16k 3x powder parked. NVDA live swing staged + already pinged to phone (msg 36), resting for the "
"7/22 open ($186 stop, 0/3 day-trades). No new trade - plan already set; won't chase extended semis into Wed's "
"GOOGL/TSLA binary. Score unchanged: alpha -16.3 vs TQQQ -2.7% since 7/2; live -19.0% inception.")

d["activity"].insert(0, {"ts": TS, "kind": "engine", "title": activity_title})
d["activity"] = d["activity"][:22]

# Update status Evening to reflect the settled verify
for s in d["status"]:
    if s.get("session") == "Evening":
        s["text"] = "Final D+ (settled); NVDA armed"

d["latest_recap"] = ("4:45p 7/21 post-close (SETTLED verify) - Real post-close run: independently reconciled both books to the "
"broker and confirmed the day's D+ grade holds on SETTLED closes (the earlier 'final' was written off an intraday "
"mark). LIVE flat $810.32 cash, zero naked, 6th straight cash session = 0% capture on the real money. PAPER 6 names "
"(AMD/SMR/OKLO/VRT/CEG/NVDA) all GTC-stopped/verified at the broker, zero naked; +0.42% off official closes (the "
"$90.4k account field is an inflated AH mark - graded off the settled close per the 7/15 data-integrity rule). "
"Coverage %s all tie to official closes (NVDA +1.9%, AMD +8.1%, SMR +9.3%, MU +12.0%, BE +14.8%, SOXL +15.7% gated, "
"TQQQ +5.5%). REGIME: QQQ closed $708.78 vs 20-day $714.7 = 0.8% under, leverage gate SHUT day 6 -> ~$16k 3x powder "
"parked for a confirmed reclaim, ideally past Wed's GOOGL/TSLA after-close prints. LIVE lever: NVDA swing ticket "
"2026-07-21-1 (3 sh, $211 marketable limit, $186 GTC stop) staged AND already pinged to the phone (telegram msg 36) "
"- approve anytime -> fills at the 7/22 open; the gate re-entry. No new trade this run (post-close; one-core rule; "
"don't add fresh beta into Wed's binary). Accountability stays final:true D+. Score alpha -16.3 vs TQQQ -2.7% since "
"7/2 ($73.35->$71.38); live -19.0% inception. Backup engine-data.backup-2026-07-21-1645.json.")

d["updated"] = TS

# Atomic write
with open(TMP, "w") as f:
    json.dump(d, f, indent=1, ensure_ascii=False)
    f.flush(); os.fsync(f.fileno())
os.replace(TMP, SRC)

# Read-back verify
v = json.load(open(SRC))
assert v["updated"] == TS, f"updated mismatch: {v['updated']}"
assert v["accountability"]["final"] is True and v["accountability"]["grade"] == "D+", "accountability drift"
assert [t["id"] for t in v["pending_tickets"]] == ["2026-07-21-1"], "pending_tickets drift"
assert v["pulse"][0]["ts"] == TS and len(v["pulse"]) == 15, "pulse drift"
assert v["activity"][0]["ts"] == TS, "activity drift"
assert v["paper"]["equity"] == 89997.84 and v["live"]["equity"] == 810.32, "equity drift"
assert len(v["coverage"]) == 14, "coverage drift"
print("VERIFY OK")
print("updated:", v["updated"])
print("pulse[0].ts:", v["pulse"][0]["ts"], "| len:", len(v["pulse"]))
print("activity[0].ts:", v["activity"][0]["ts"], "| len:", len(v["activity"]))
print("accountability:", v["accountability"]["final"], v["accountability"]["grade"])
print("pending:", [t["id"] for t in v["pending_tickets"]])
print("status Evening:", [s["text"] for s in v["status"] if s["session"]=="Evening"])
print("file bytes:", os.path.getsize(SRC))
