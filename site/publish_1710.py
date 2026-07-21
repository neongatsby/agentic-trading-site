import json, os, sys, datetime

SITE = os.path.dirname(os.path.abspath(__file__))
TARGET = os.path.join(SITE, "engine-data.json")

with open(TARGET) as f:
    d = json.load(f)

# --- Guard: only graft onto the expected 4:45 settled-final base (7/20 clobber lesson) ---
assert d.get("updated","").startswith("2026-07-21T16:45"), f"BAD BASE updated={d.get('updated')}"
acc = d.get("accountability",{})
assert acc.get("final") is True and acc.get("grade")=="D+", f"BAD BASE acct final/grade={acc.get('final')}/{acc.get('grade')}"
assert acc.get("date")=="2026-07-21", f"BAD BASE acct date={acc.get('date')}"
pt = d.get("pending_tickets",[])
assert len(pt)==1 and pt[0].get("id")=="2026-07-21-1", f"BAD BASE pending={[t.get('id') for t in pt]}"
prev_pulse0_ts = d["pulse"][0]["ts"]

# --- Backup the good base before touching it ---
bak = os.path.join(SITE, "engine-data.backup-2026-07-21-1710.json")
with open(bak,"w") as f:
    json.dump(d, f, indent=1)

NEW_TS = "2026-07-21T17:10:00-04:00"

# --- Archive prior latest_recap, set the new heartbeat recap ---
d["_latest_recap_1645"] = d["latest_recap"]
d["latest_recap"] = (
  "5:08p 7/21 after-hours heartbeat (market closed, next open 7/22 09:30) - light verify-and-hold "
  "~23 min on from the 4:45 SETTLED finalize; grade stays final:true D+ (not re-graded). "
  "Independently re-checked both books at the broker: LIVE flat $810.32 cash, zero positions/orders "
  "(nothing naked, 6th straight cash session); PAPER 6 names ALL GTC-stopped + verified this run "
  "(AMD $490 / SMR $7.50 / OKLO $39 / VRT $282 / CEG $236 / NVDA $186), zero naked. Pulled AH snapshots - "
  "nothing near a stop: AMD $544.6, SMR $8.74, OKLO $45.9 (+4% AH), VRT $305.5, CEG $262.6, "
  "NVDA $206.7 (holding ~$207, right at the swing entry). Tape flat after-hours (S&P/Nasdaq ~-0.05%); "
  "tonight's earnings (ALK/NLY/COF) are not watchlist names - the binary stays Wed 7/22 after-close "
  "(GOOGL + TSLA). No trade this run (post-close; one-core rule; don't add fresh beta ahead of Wed). "
  "NVDA live swing ticket 2026-07-21-1 (3 sh, $211 marketable limit, $186 GTC stop) stays armed + pinged "
  "for the 7/22 open - the gate re-entry. Backup engine-data.backup-2026-07-21-1710.json."
)

# --- Prepend ONE pulse item; keep newest ~15 ---
new_pulse = {
  "ts": NEW_TS,
  "text": ("5:08p after-hours heartbeat (~23 min on from the 4:45 settled finalize). Re-verified both "
           "books at the broker: all 6 paper stops live (AMD $490 / SMR $7.50 / OKLO $39 / VRT $282 / "
           "CEG $236 / NVDA $186), LIVE flat $810.32 cash - zero naked either side. AH tape quiet "
           "(S&P/Nasdaq ~-0.05%); OKLO firmed +4% AH, NVDA holding ~$207 right at the swing entry. "
           "Tonight's prints (ALK/NLY/COF) aren't ours - the binary is Wed's GOOGL+TSLA after-close. "
           "No trade (post-close, one-core, don't add beta into Wed). NVDA live swing 2026-07-21-1 stays "
           "armed for the 7/22 open. Grade stays final D+."),
  "hype": ("Quick after-hours check - every position still has its stop and live's in cash, nothing "
           "exposed. NVDA's holding ~$207 so tomorrow's swing is still on; just watching till the open.")
}
d["pulse"] = [new_pulse] + d["pulse"]
d["pulse"] = d["pulse"][:15]

d["updated"] = NEW_TS

# --- Atomic write (temp -> os.replace); unique temp name in site dir ---
tmp = os.path.join(SITE, ".engine-data.publish_1710.tmp")
with open(tmp,"w") as f:
    json.dump(d, f, indent=1)
os.replace(tmp, TARGET)

# --- Read-back verification ---
with open(TARGET) as f:
    r = json.load(f)
ok = (
  r["updated"]==NEW_TS and
  r["accountability"]["final"] is True and
  r["accountability"]["grade"]=="D+" and
  r["accountability"]["date"]=="2026-07-21" and
  len(r["pending_tickets"])==1 and r["pending_tickets"][0]["id"]=="2026-07-21-1" and
  r["pulse"][0]["ts"]==NEW_TS and
  r["pulse"][1]["ts"]==prev_pulse0_ts and
  len(r["pulse"])==15 and
  len(r["coverage"])==14 and len(r["feed"])==41
)
print("READBACK_OK:", ok)
print("updated:", r["updated"])
print("acct:", r["accountability"]["date"], r["accountability"]["final"], r["accountability"]["grade"])
print("pending:", [t["id"] for t in r["pending_tickets"]])
print("pulse_len:", len(r["pulse"]), "| coverage:", len(r["coverage"]), "| feed:", len(r["feed"]))
print("pulse0.ts:", r["pulse"][0]["ts"], "| pulse1.ts:", r["pulse"][1]["ts"])
assert ok, "READBACK FAILED"
print("PUBLISH OK")
