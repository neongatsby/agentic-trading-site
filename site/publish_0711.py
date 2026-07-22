#!/usr/bin/env python3
"""Atomic engine-data publish — 2026-07-22 07:11 ET pre-market heartbeat.
Per OPS-ALERT clobber lesson: unique script name, backup first, atomic os.replace, read-back verify."""
import json, os, shutil, sys

SITE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(SITE, "engine-data.json")
TS = "2026-07-22T07:11:00-04:00"
BACKUP = os.path.join(SITE, "engine-data.backup-2026-07-22-0711.json")

d = json.load(open(SRC))

# 0) backup the good current state BEFORE mutating
shutil.copyfile(SRC, BACKUP)

# 1) updated
d["updated"] = TS

# 2) pulse — prepend one, keep 15
pulse_text = ("7:11a pre-market — reconciled both books at the broker and recomputed the regime; nothing "
  "changes the plan. LIVE is flat ($810.32 cash, zero orders, nothing naked — 6th session); PAPER is "
  "6/6 GTC-stopped, zero naked, ~$89.5k (down ~0.5% pre-market as AMD/NVDA/VRT give a little back vs OKLO "
  "+3.8%). QQQ's 20-day recomputes to $714.67 with the close $708.97 = −0.8% under → still the re-entry "
  "zone. Oil +4% to ~$95 (Iran, 11th night) has index futures soft (NDX −0.7%) and chips cooling after two "
  "green days, into tonight's GOOGL+TSLA binary. Everything stays armed for the OPEN: the NVDA live swing "
  "fires on approval at 9:30 (ends the cash camp), then I trim the ~32% paper NVDA anchor into the nuclear "
  "pure-plays with real prices. No pre-market execution — thin liquidity + a binary tonight = bad fills.")
pulse_hype = ("Checked both accounts — all good, nothing exposed. Oil's up so the open'll be soft; I'm holding "
  "fire till 9:30 when the NVDA trade can actually fill and I shift the big NVDA paper chunk into the nuclear names.")
d["pulse"] = [{"ts": TS, "text": pulse_text, "hype": pulse_hype}] + d["pulse"]
d["pulse"] = d["pulse"][:15]

# 3) feed — prepend one activity, keep 40
feed_item = {"type": "activity", "ts": TS, "text": (
  "7:11a pre-market — re-reconciled both books at the broker (LIVE flat $810 cash / zero orders; PAPER 6/6 "
  "GTC-stopped; zero naked) and recomputed QQQ vs its 20-day ($708.97 vs $714.67 = −0.8%, re-entry zone). "
  "Oil +4% to ~$95 keeps the open soft into tonight's GOOGL/TSLA binary; plan armed for 9:30 (NVDA swing on "
  "approval + paper NVDA→nuclear trim). No pre-market execution by design.")}
d["feed"] = [feed_item] + d["feed"]
d["feed"] = d["feed"][:40]

# 4) status — refresh the Pre-market card
d["status"] = [{"session": "Pre-market", "text": "Books verified clean; armed for open"}]

# 5) headlines — light refresh, keep current + add the beat-rate line
d["headlines"] = [
  "BINARY tonight: GOOGL + TSLA report after the close — the first real Mag-7 AI-capex test",
  "Oil +4% to ~$95 (1-month high) as Rubio says Iran 'not serious'; 11th night of US strikes revives inflation fear",
  "Bloomberg/DOE: Oklo + X-Energy tapped for a $200M program to fast-track nuclear reactors for AI (OKLO +3.8% pre-mkt)",
  "AMD 'Advancing AI 2026' event today (MI355X / MI400) — AMD digesting a +8% day, ~−1.7% pre-mkt",
  "Regime in the re-entry zone: QQQ $708.97 = −0.8% under its $714.67 20-day (recomputed); S&P at a record, 2nd green session",
  "NVDA live swing armed for the 9:30 open — ends a 6-session live cash camp (3 sh, $186 stop, approve-anytime)",
  "88% of S&P Q2 reporters have beaten profit estimates — strong earnings, but the oil overhang caps the open",
]

# 6) coverage — refresh chg_pct with fresh pre-market marks + projections + updated ts
premkt_chg = {"AMD": "-1.7%", "CEG": "-0.7%", "NVDA": "-1.0%", "OKLO": "+3.8%", "SMR": "+0.4%", "VRT": "-2.4%"}
# projection updates: (target_pct, confidence, basis, pop_rank)
proj = {
  "OKLO": (4.0, "med", "confirmed DOE $200M nuclear-for-AI program; +3.8% pre-mkt, RS leader", 1),
  "SMR":  (2.5, "med", "nuclear-for-AI sympathy w/ OKLO DOE catalyst; green pre-mkt", 2),
  "AMD":  (1.5, "med", "'Advancing AI 2026' event today vs a risk-off, digest-the-+8% tape", 3),
  "CEG":  (1.0, "med", "AI-power leg rides the nuclear bid; steady", 4),
  "NVDA": (0.5, "med", "funded live swing — least-extended AI leader, laggard, wide $186 stop", 5),
  "VRT":  (-0.5, "low", "data-center power giving back; red pre-mkt on the risk-off open", 6),
  "RKLB": (1.0, "low", "space momentum, no fresh catalyst; tape-dependent", 7),
  "RGTI": (0.5, "low", "quantum high-beta; tracks the tape, cooling", 8),
  "IONQ": (0.5, "low", "quantum high-beta; tracks the tape, cooling", 9),
  "MU":   (-0.5, "med", "memory extended after +12%; cools on the risk-off open", 10),
  "BE":   (-2.0, "med", "extended after +14.8%; gives back on a cooling tape", 11),
  "TSLA": (0.0, "med", "reports after the close — the move is tonight, not intraday", 12),
  "TQQQ": (0.0, "low", "3x Nasdaq flat/soft on the risk-off open under the 20-day", 13),
  "SOXL": (-1.0, "low", "3x semis cooling after +15.7%; risk-off caps it", 14),
}
for c in d["coverage"]:
    t = c["ticker"]
    if t in premkt_chg:
        c["chg_pct"] = premkt_chg[t]
    if t in proj:
        tp, conf, basis, rank = proj[t]
        c["projection"]["target_pct"] = tp
        c["projection"]["confidence"] = conf
        c["projection"]["basis"] = basis
        c["projection"]["pop_rank"] = rank
    c["updated"] = TS

# 7) accountability — running, pre-open, refreshed headline + saved note (final:false)
acc = d["accountability"]
acc["date"] = "2026-07-22"
acc["final"] = False
acc["grade"] = "TBD (pre-open)"
acc["headline"] = ("Pre-market (7:11a): both books re-reconciled clean at the broker (live flat, paper 6/6 "
  "GTC-stopped, zero naked); QQQ recomputes to −0.8% under its $714.67 20-day = the re-entry zone. Oil +4% "
  "to ~$95 keeps futures soft (NDX −0.7%) into tonight's GOOGL+TSLA binary. Plan armed for the OPEN — fire "
  "the staged NVDA re-entry, trim the paper NVDA anchor into nuclear, add NO fresh semi size into the print.")
acc["capture"]["bestName"] = "TBD - pre-open (OKLO leads the watchlist +3.8% pre-mkt on the DOE nuclear-for-AI catalyst)"
acc["capture"]["bestPct"] = "-"
acc["capture"]["capturedPct"] = "-"
acc["capture"]["rate"] = "pre-open"
acc["saved"] = [{"note": "Zero naked into the open — all 6 paper positions GTC-stopped (verified at the broker), live flat; independently re-reconciled this run (7:11a)", "delta": "risk bounded"}]

# --- ATOMIC WRITE ---
tmp = SRC + ".tmp0711"
with open(tmp, "w") as f:
    json.dump(d, f, ensure_ascii=False, indent=1)
os.replace(tmp, SRC)

# --- READ-BACK VERIFY ---
v = json.load(open(SRC))
pop1 = [c["ticker"] for c in v["coverage"] if c.get("projection", {}).get("pop_rank") == 1]
assert v["updated"] == TS, "updated mismatch"
assert v["accountability"]["final"] is False, "final should be False pre-open"
assert len(v["pending_tickets"]) == 1 and v["pending_tickets"][0]["id"] == "2026-07-21-1", "NVDA ticket must persist"
assert v["pending_tickets"][0]["symbol"] == "NVDA", "pending must be NVDA"
assert pop1 == ["OKLO"], f"pop_rank1 should be OKLO, got {pop1}"
assert len(v["pulse"]) == 15 and v["pulse"][0]["ts"] == TS, "pulse prepend/trim failed"
assert len(v["feed"]) == 40 and v["feed"][0]["ts"] == TS, "feed prepend/trim failed"
assert v["pending_tickets"][0]["stop"] == 186, "NVDA stop must be 186"
print("VERIFY OK")
print("updated:", v["updated"])
print("pop_rank1:", pop1, "| pending:", v["pending_tickets"][0]["symbol"], v["pending_tickets"][0]["qty"], "sh, stop", v["pending_tickets"][0]["stop"])
print("acc.final:", v["accountability"]["final"], "| grade:", v["accountability"]["grade"])
print("pulse[0].ts:", v["pulse"][0]["ts"], "| feed[0].ts:", v["feed"][0]["ts"])
print("backup:", os.path.basename(BACKUP), os.path.getsize(BACKUP), "bytes")
