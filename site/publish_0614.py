#!/usr/bin/env python3
"""Per-run atomic publish for the 2026-07-22 ~06:14 ET pre-market heartbeat.
Surgical incremental update onto the existing good base (5:39 run). Atomic write + read-back verify."""
import json, os, shutil, tempfile, datetime

SITE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(SITE, "engine-data.json")
TS = "2026-07-22T06:14:00-04:00"

with open(SRC) as f:
    d = json.load(f)

# ---- 0) backup the good pre-write state ----
bak = os.path.join(SITE, "engine-data.backup-2026-07-22-0614.json")
shutil.copyfile(SRC, bak)

# ---- 1) top-level timestamp ----
d["updated"] = TS

# ---- 2) status card (Pre-market) ----
d["status"] = [{"session": "Pre-market", "text": "NVDA armed; oil spike, chips soft"}]

# ---- 3) headlines (today's drivers first) ----
d["headlines"] = [
    "BINARY tonight: GOOGL + TSLA report after the close - the first real Mag-7 AI-capex test",
    "Futures lower (Nasdaq-100 -0.7%): Brent >$92 on an 11th night of US-Iran strikes revives inflation fear",
    "Bloomberg: Oklo + X-Energy join a Trump/DOE $200M program to fast-track nuclear reactors for AI (OKLO +6%)",
    "AMD 'Advancing AI 2026' event today (MI355X launch / MI400 update); AMD ~-2% pre-mkt after a +8% day",
    "Regime in the re-entry zone: S&P at a record, QQQ $709 = -0.8% under its $714.7 20-day, 2nd green session",
    "NVDA live swing armed for the open - ends a 6-session live cash camp (3 sh, $186 stop, approve-anytime)",
    "Paper owns AMD/SMR/OKLO/VRT/CEG/NVDA - all 6 GTC-stopped, zero naked; OKLO the nuclear winner",
]

# ---- 4) prepend one pulse entry ----
pulse_text = ("6:14a pre-market - fresh 6am wires firm the caution and I re-verified the book. "
    "Nasdaq-100 futures -0.7% (Dow -0.1%, S&P -0.3%) with Brent back above $92 on an 11th straight night "
    "of US strikes on Iran - that oil-inflation overhang is why a strong-earnings tape opens soft, into tonight's "
    "GOOGL + TSLA after-close binary. Re-confirmed both books == broker, zero naked: LIVE flat $810.32 cash "
    "(6th session, 0/3 same-day day-trades used) with the NVDA re-entry armed to fire at 9:30 ($186 stop); "
    "PAPER 6/6 GTC-stopped. Plan holds - fire the NVDA swing at the open (the gate re-entry), then trim the "
    "paper NVDA anchor toward the nuclear-for-AI names, add NO fresh semi size into the binary. OKLO stays "
    "pop_rank 1 on its confirmed DOE nuclear-for-AI program (owned 200 sh in paper); NVDA is the risk-managed "
    "real-money swing, not today's biggest expected pop.")
pulse_hype = ("Checked everything again - clean and stopped, nothing to do till the 9:30 open. Oil's spiking on the "
    "Iran strikes so futures are red, and I won't chase hot chips into tonight's Google + Tesla prints - just firing "
    "the NVDA buy at the open.")
d.setdefault("pulse", [])
d["pulse"].insert(0, {"ts": TS, "text": pulse_text, "hype": pulse_hype})
d["pulse"] = d["pulse"][:15]

# ---- 5) refresh coverage projections (timestamps + light risk-off haircut; keep pop_rank order) ----
# firmer risk-off (oil + futures -0.7%) => shave the high-beta long targets a touch
tweaks = {
    "NVDA": {"target_pct": 0.6, "basis": "least-extended AI leader; live re-entry, no own binary"},
    "AMD":  {"target_pct": 0.8, "basis": "Advancing AI event today but digesting +8% as chips cool + oil up"},
    "SMR":  {"target_pct": 1.5, "basis": "nuclear-for-AI bid; extended, risk-off tape"},
    "OKLO": {"target_pct": 2.2, "basis": "confirmed DOE nuclear-for-AI program; RS leader, tape cooling"},
    "CEG":  {"target_pct": 1.2, "basis": "nuclear-for-AI beneficiary, least-extended of the group"},
    "VRT":  {"target_pct": 0.8, "basis": "AI-datacenter power/cooling, tracks the complex"},
}
for c in d.get("coverage", []):
    c["updated"] = TS
    t = tweaks.get(c.get("ticker"))
    if t and isinstance(c.get("projection"), dict):
        c["projection"]["target_pct"] = t["target_pct"]
        c["projection"]["basis"] = t["basis"]

# ---- 6) accountability: refresh running headline (still pre-open, final:false) ----
acc = d.get("accountability", {})
acc["headline"] = ("Pre-market (6:14a): 6am wires firm the caution - Nasdaq-100 futures -0.7% with Brent back >$92 on "
    "an 11th night of US-Iran strikes reviving inflation fear, into tonight's GOOGL+TSLA binary. Plan unchanged: fire "
    "the staged NVDA re-entry at the open (ends the 6-session cash camp), trim the paper NVDA anchor toward "
    "nuclear-for-AI, and add NO fresh semi size into the print.")
d["accountability"] = acc

# ---- 7) refresh live/paper equity marks (scalar only; do NOT touch daily equity_curve) ----
if isinstance(d.get("live"), dict):
    d["live"]["equity"] = 810.32
    d["live"]["updated"] = TS
if isinstance(d.get("paper"), dict):
    d["paper"]["equity"] = 89501.81
    d["paper"]["updated"] = TS

# ---- 8) atomic write (temp -> os.replace) ----
fd, tmp = tempfile.mkstemp(dir=SITE, prefix=".ed_tmp_", suffix=".json")
with os.fdopen(fd, "w") as f:
    json.dump(d, f, ensure_ascii=False, indent=1)
os.replace(tmp, SRC)

# ---- 9) read-back verify ----
with open(SRC) as f:
    chk = json.load(f)
ok = True
if chk.get("updated") != TS: ok = False; print("FAIL updated", chk.get("updated"))
if chk.get("accountability", {}).get("final") is not False: ok = False; print("FAIL final")
pt = chk.get("pending_tickets", [])
if not (len(pt) == 1 and pt[0].get("id") == "2026-07-21-1" and pt[0].get("symbol") == "NVDA"):
    ok = False; print("FAIL pending_tickets", pt)
if chk.get("pulse", [{}])[0].get("ts") != TS: ok = False; print("FAIL pulse head")
pop1 = [c.get("ticker") for c in chk.get("coverage", []) if c.get("projection", {}).get("pop_rank") == 1]
if pop1 != ["OKLO"]: ok = False; print("FAIL pop_rank1", pop1)
print("VERIFY", "OK" if ok else "MISMATCH")
print("updated:", chk.get("updated"))
print("pulse[0].ts:", chk.get("pulse", [{}])[0].get("ts"))
print("pending:", [(t.get("id"), t.get("symbol"), t.get("side"), t.get("qty")) for t in pt])
print("pop_rank1:", pop1, "| coverage n:", len(chk.get("coverage", [])))
print("acc.final:", chk.get("accountability", {}).get("final"), "| grade:", chk.get("accountability", {}).get("grade"))
print("size bytes:", os.path.getsize(SRC))
