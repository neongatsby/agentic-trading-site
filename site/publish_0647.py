import json, os, shutil, datetime

SRC = "engine-data.json"
TS = "2026-07-21T06:47:00-04:00"

# 1) backup the current good state
bak = "engine-data.backup-2026-07-21-0647.json"
shutil.copyfile(SRC, bak)

d = json.load(open(SRC))

# 2) prepend fresh pulse entry, trim to 15
pulse_text = ("6:47am ET pre-market — nothing material moved since the 6:10 read, and one calendar point is now nailed down: "
 "Alphabet AND Tesla both report Wednesday 7/22 after the close (Intel Thu 7/23), so the paper SQQQ hedge into that binary "
 "is validated, not a guess. Recomputed the gate off settled daily bars myself: QQQ 20-day = $716.12, and pre-market QQQ ~$705.7 "
 "(+1.38%) is still ~1.5% under it — leverage gate stays SHUT day 6, no blind pre-market trades. LIVE: the PLTR open-buy "
 "(ticket 2026-07-20-3, 5 sh, $122 stop, approve-anytime -> fills at the 9:30 open) stands — the funded BE->PLTR rotation "
 "and the direct fix for yesterday's cash-locked D. PAPER: holding all 4 + the hedge into Wed's prints; ~$40.5k powder staged "
 "for the open QQQ-vs-$716 fork. Both books reconcile clean at the broker, 4/4 GTC-stopped, nothing naked. Day-trade 0/3.")
pulse_hype = ("Quiet pre-market — confirmed Google and Tesla both report Wednesday, so the hedge stays on for it. "
 "Nasdaq's still under its line so no leverage; PLTR's locked to buy at the open and both books are clean.")
d["pulse"] = [{"ts": TS, "text": pulse_text, "hype": pulse_hype}] + d["pulse"]
d["pulse"] = d["pulse"][:15]

# 3) refresh status cards
d["status"] = [
  {"session": "Pre-market", "text": "QQQ +1.4% ~$705, under $716 gate d6"},
  {"session": "Open plan", "text": "PLTR buy fills 9:30; hedge into Wed"},
  {"session": "Books", "text": "Live $810 cash; paper 4/4 stopped"},
]

# 4) accountability headline refresh (still running / pre-open)
acc = d["accountability"]
acc["final"] = False
acc["grade"] = "running (pre-open)"
acc["headline"] = ("Pre-open 7/21 (running): applying yesterday's D-grade fix directly - the funded PLTR buy is STAGED to fill at the OPEN, "
 "so live rotates into the pop_rank-1 leader early instead of camping cash. Calendar now confirmed: GOOGL + TSLA both report Wed 7/22 AMC "
 "(INTC Thu), so the paper SQQQ hedge is deliberate insurance into a binary, not lazy cash. Leverage gate SHUT day 6 "
 "(pre-mkt QQQ ~$705.7 vs the 20-day $716.12). Grade finalizes post-close.")

# 5) timestamps + fresh paper equity mark
d["updated"] = TS
d["paper"]["updated"] = TS
d["paper"]["equity"] = 89206.09
d["live"]["updated"] = TS

# 6) atomic write: temp -> os.replace
tmp = SRC + ".tmp"
with open(tmp, "w") as f:
    json.dump(d, f, ensure_ascii=False, indent=1)
os.replace(tmp, SRC)

# 7) read-back verification
v = json.load(open(SRC))
assert v["updated"] == TS, "updated mismatch"
assert v["accountability"]["final"] is False, "final flag"
assert v["pulse"][0]["ts"] == TS, "pulse head"
assert len(v["pulse"]) == 15, "pulse len"
assert len(v["pending_tickets"]) == 1 and v["pending_tickets"][0]["id"] == "2026-07-20-3", "pending ticket"
assert v["paper"]["equity"] == 89206.09, "paper equity"
print("VERIFY OK")
print("updated:", v["updated"])
print("pulse[0].ts:", v["pulse"][0]["ts"], "| len:", len(v["pulse"]))
print("acc.final:", v["accountability"]["final"], "| grade:", v["accountability"]["grade"])
print("pending:", v["pending_tickets"][0]["id"], v["pending_tickets"][0]["symbol"], v["pending_tickets"][0]["qty"], "sh")
print("coverage names:", [c["ticker"] for c in v["coverage"]])
print("pop_rank1:", [c["ticker"] for c in v["coverage"] if c.get("projection",{}).get("pop_rank")==1])
print("backup:", bak, os.path.getsize(bak), "bytes | live size:", os.path.getsize(SRC), "bytes")
