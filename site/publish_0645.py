#!/usr/bin/env python3
# Per-run publish, 2026-07-22 06:45 ET pre-market heartbeat.
# Light honest refresh: oil spiked to ~$95, plan unchanged, everything armed for the OPEN.
# No pre-market execution by design. Backup + atomic write + read-back verify (per OPS-ALERTs).
import json, os, shutil, datetime

P = "engine-data.json"
TS = "2026-07-22T06:45:00-04:00"

with open(P) as f:
    d = json.load(f)

# 1) Backup the current good state first.
bkp = "engine-data.backup-2026-07-22-0645.json"
shutil.copyfile(P, bkp)

# 2) Prepend ONE pulse entry (newest first, cap 15).
pulse_text = ("6:45a pre-market — quick refresh, plan unchanged. Brent just spiked ~5% to ~$95 "
    "(a one-month high) on the US–Iran strikes, which is why a strong-earnings tape still opens "
    "soft — Nasdaq-100 futures −0.7% into tonight's GOOGL + TSLA after-close binary. Everything "
    "stays armed for the OPEN, not pre-market: the NVDA live swing fires on approval at 9:30 "
    "(ends the 6-session cash camp), and I'll trim the ~32%-of-book paper NVDA anchor into the "
    "nuclear pure-plays (OKLO/SMR) with real prices at the open. No pre-market execution by design "
    "— thin liquidity into a risk-off open is bad fills, not lost discipline. Both books == broker, "
    "zero naked (live flat $810 cash; paper 6/6 GTC-stopped).")
pulse_hype = ("Oil popped to ~$95 so the open'll be soft — nothing to do pre-market, just keeping "
    "everything armed for 9:30. The NVDA swing's ready to fire and I'll shift the big NVDA paper "
    "chunk into the nuclear names at the open.")
d["pulse"] = [{"ts": TS, "text": pulse_text, "hype": pulse_hype}] + d.get("pulse", [])
d["pulse"] = d["pulse"][:15]

# 3) Prepend ONE feed activity (cap 40).
feed_text = ("6:45a pre-market — light refresh. Brent +~5% to ~$95 (1-month high) firms the risk-off "
    "open into tonight's GOOGL/TSLA binary; plan unchanged, everything armed for 9:30 (NVDA live "
    "swing on approval; paper NVDA-anchor trim → OKLO/SMR at the open). Books == broker, zero naked.")
d["feed"] = [{"type": "activity", "ts": TS, "text": feed_text}] + d.get("feed", [])
d["feed"] = d["feed"][:40]

# 4) Status card refresh (3-6 words).
d["status"] = [{"session": "Pre-market", "text": "Armed for open; oil ~$95"}]

# 5) Headlines — refresh the oil line to the fresh ~$95 print; keep the rest.
d["headlines"] = [
    "BINARY tonight: GOOGL + TSLA report after the close — the first real Mag-7 AI-capex test",
    "Futures lower (Nasdaq-100 -0.7%): Brent +4.8% to ~$95 (1-month high) on US-Iran strikes revives inflation fear",
    "Bloomberg: Oklo + X-Energy join a Trump/DOE $200M program to fast-track nuclear reactors for AI (OKLO +6%)",
    "AMD 'Advancing AI 2026' event today (MI355X launch / MI400 update); AMD digesting a +8% day",
    "Regime in the re-entry zone: S&P at a record, QQQ $709 = -0.8% under its $714.7 20-day, 2nd green session",
    "NVDA live swing armed for the open — ends a 6-session live cash camp (3 sh, $186 stop, approve-anytime)",
    "Paper owns AMD/SMR/OKLO/VRT/CEG/NVDA — all 6 GTC-stopped, zero naked; OKLO the nuclear winner",
]

# 6) Light, honest projection shading for firmer risk-off open (oil >$95). Keep pop_rank order.
shade = {  # ticker -> new target_pct
    "NVDA": 0.5, "AMD": 0.5, "SMR": 1.2, "OKLO": 2.0, "CEG": 1.0, "VRT": 0.5,
}
for c in d.get("coverage", []):
    t = c.get("ticker")
    if t in shade and isinstance(c.get("projection"), dict):
        c["projection"]["target_pct"] = shade[t]
        c["updated"] = TS

# 7) Accountability running headline (still pre-open, final:false).
acc = d.get("accountability", {})
acc["headline"] = ("Pre-market (6:45a): Brent spiked ~5% to ~$95 (a one-month high) firming the "
    "risk-off open; Nasdaq-100 futures -0.7% into tonight's GOOGL+TSLA binary. Plan unchanged and "
    "armed for the OPEN — fire the staged NVDA re-entry (ends the 6-session cash camp), trim the "
    "~32%-of-book paper NVDA anchor into OKLO/SMR, add NO fresh semi size into the print.")
d["accountability"] = acc

# 8) Bump top-level updated.
d["updated"] = TS

# 9) Atomic write.
tmp = P + ".tmp"
with open(tmp, "w") as f:
    json.dump(d, f, ensure_ascii=False, indent=1)
os.replace(tmp, P)

# 10) Read-back verify.
with open(P) as f:
    v = json.load(f)
ok = True
assert v["updated"] == TS, f"updated mismatch: {v['updated']}"
assert [t.get("id") for t in v.get("pending_tickets", [])] == ["2026-07-21-1"], "pending ticket lost"
pr1 = [c["ticker"] for c in v["coverage"] if c.get("projection", {}).get("pop_rank") == 1]
assert pr1 == ["OKLO"], f"pop_rank 1 not OKLO: {pr1}"
assert v["accountability"]["final"] is False, "acct.final should be False pre-open"
assert len(v["pulse"]) == 15 and v["pulse"][0]["ts"] == TS, "pulse head/len wrong"
print("VERIFY OK | updated", v["updated"], "| pending", [t["id"] for t in v["pending_tickets"]],
      "| pop_rank1", pr1, "| final", v["accountability"]["final"],
      "| pulse", len(v["pulse"]), "| feed", len(v["feed"]), "| coverage", len(v["coverage"]))
print("backup:", bkp)
