import json, os, tempfile, shutil, sys

SITE = "/sessions/adoring-wonderful-bohr/mnt/movita-backend/agentic-trading-site/site"
SRC = os.path.join(SITE, "engine-data.json")
TS = "2026-07-22T08:15:00-04:00"
BACKUP = os.path.join(SITE, "engine-data.backup-2026-07-22-0815.json")

d = json.load(open(SRC))

# 1) updated
d["updated"] = TS

# 2) status (single pre-market card)
d["status"] = [{"session": "Pre-market", "text": "Chips fade pre-open; NVDA armed"}]

# 3) headlines
d["headlines"] = [
 "BINARY tonight: GOOGL + TSLA report after the close (IBM + TXN too) - the Mag-7 AI-capex test; Alphabet's '26 capex guide is the number for our book",
 "Risk-off open: Nasdaq-100 futures -1.26%, oil ~$95 on Mideast tensions capping otherwise-strong earnings",
 "2-day semi rip UNWINDING pre-open: SOXL -8.2%, MU -4.4%, TQQQ -2.7% giving back - the gate keeping us out of 3x semis vindicated",
 "OKLO the lone watchlist name green (+1.7%) - confirmed Trump/DOE nuclear-for-AI program keeps it in focus (pop_rank 1)",
 "NVDA -1.3% pre-open = cheaper re-entry; live swing armed for the 9:30 open to end a 6-session cash camp (3 sh, $186 stop, approve-anytime)",
 "Regime in the re-entry zone: QQQ $708.8 = -0.8% under its $714.7 20-day; S&P near a record",
 "AMD 'Advancing AI 2026' developer event today - owned into the catalyst (30 sh, $490 stop)",
 "Fear & Greed still 'Fear' despite the Nasdaq's green Tuesday"
]

# 4) coverage: refresh projection + updated (keep chg_pct pre-open convention)
proj = {
 "NVDA": (0.5, "med", "least-extended AI leader; chips fading into tonight's binary", 4),
 "AMD":  (0.5, "med", "Advancing AI event today vs +8% 2-day run digesting", 3),
 "SMR":  (1.5, "med", "nuclear-for-AI sympathy; softer pre-open (-1.4%)", 2),
 "MU":   (-4.0, "med", "giving back the +12.8% rip pre-open; extended", 13),
 "BE":   (-3.0, "med", "spent parabolic after +14.8%; give-back risk", 12),
 "OKLO": (3.0, "high", "DOE nuclear-for-AI leader; RS holding +1.7% as semis fade", 1),
 "RGTI": (-1.5, "low", "quantum high-beta; sells with the risk-off tape", 10),
 "VRT":  (-0.5, "low", "data-center power giving back on a risk-off open", 6),
 "IONQ": (-1.5, "low", "quantum beta; cools with a risk-off tape", 9),
 "RKLB": (-1.0, "low", "space momentum, no fresh catalyst; tape-dependent", 7),
 "CEG":  (0.8, "med", "nuclear utility rides the AI-power bid; steady", 5),
 "TSLA": (0.0, "med", "reports after the close - the move is tonight", 8),
 "SOXL": (-6.0, "med", "3x semis unwinding the 2-day rip; gate vindicated", 14),
 "TQQQ": (-2.0, "low", "3x Nasdaq powder; awaits a QQQ 20-day reclaim", 11),
}
seen_pop1 = 0
for c in d["coverage"]:
    t = c["ticker"]
    if t in proj:
        tp, conf, basis, pr = proj[t]
        c["projection"] = {"target_pct": tp, "confidence": conf, "basis": basis, "pop_rank": pr}
        if pr == 1: seen_pop1 += 1
        c["updated"] = TS
assert seen_pop1 == 1, f"expected exactly one pop_rank 1, got {seen_pop1}"

# 5) pulse prepend (trim to 15)
pulse_new = {
 "ts": TS,
 "text": "8:15a pre-market: nothing to fire pre-open by design - thin liquidity into tonight's GOOGL/TSLA binary with chips actively selling off (SOXL -8%, MU -4% giving back the 2-day rip). NVDA live re-entry stays armed for the 9:30 open (the D+ lesson's fix - ends the 6-session cash camp); paper NVDA->nuclear trim executes at the open. OKLO the one holding green (+1.7%) on its DOE catalyst = pop_rank 1. Both books == broker, zero naked.",
 "hype": "Chips are dumping the 2-day rip pre-open, so I'm not touching anything till the 9:30 bell - the NVDA buy's still armed to finally end our cash streak. OKLO's the only one holding up."
}
d["pulse"] = [pulse_new] + d["pulse"]
d["pulse"] = d["pulse"][:15]

# 6) feed prepend (trim to 40)
feed_new = {
 "type": "activity",
 "ts": TS,
 "text": "8:15a pre-market - heartbeat. Fresh wires + prints confirm the risk-off open: NDX futures -1.26%, oil ~$95 (Mideast), and the 2-day semi rip is unwinding pre-open (SOXL -8.2%, MU -4.4%, TQQQ -2.7%, NVDA -1.3%) into tonight's GOOGL+TSLA+IBM+TXN after-close binary. OKLO +1.7% is the lone watchlist name holding green on its confirmed DOE nuclear-for-AI catalyst (pop_rank 1). Both books == broker, zero naked: LIVE flat $810.32 cash (6th session, 0/3 day-trades) with the NVDA re-entry armed for the 9:30 open ($186 stop); PAPER 6/6 GTC-stopped (~$88.9k, semis soft pre-open). No pre-market execution by design - the SOXL -8% give-back is exactly why (bad fills into a selloff before a binary); NVDA swing + paper NVDA->nuclear trim fire at the OPEN with real prices/stops."
}
d["feed"] = [feed_new] + d["feed"]
d["feed"] = d["feed"][:40]

# 7) accountability (keep final:false, grade TBD; refresh headline + saved)
a = d["accountability"]
a["date"] = "2026-07-22"
a["final"] = False
a["grade"] = "TBD (pre-open)"
a["headline"] = "Pre-market (8:15a): heartbeat - both books re-reconciled clean (LIVE flat $810.32 cash, PAPER 6/6 GTC-stopped, zero naked). The 2-day semi rip is unwinding pre-open (SOXL -8%, MU -4%) into tonight's GOOGL+TSLA+IBM+TXN binary - vindicating the gate that kept us out of 3x semis; QQQ -0.8% under its 20-day holds the re-entry zone. Plan armed for the OPEN: fire the staged NVDA re-entry to end the 6-session cash camp, trim the paper NVDA anchor toward the nuclear movers (OKLO the RS leader), add NO fresh semi size into the print."
a["capture"] = {
 "bestName": "TBD - pre-open (OKLO leads the watchlist +1.7% on the confirmed DOE nuclear-for-AI catalyst)",
 "bestPct": "-", "capturedPct": "-", "rate": "pre-open"
}
a["saved"] = [
 {"note": "Zero naked into the open - all 6 paper positions GTC-stopped (verified at the broker), live flat; independently re-reconciled this run (8:15a).", "delta": "risk bounded"},
 {"note": "Gate keeping live OUT of 3x semis vindicated pre-open - SOXL -8.2% / MU -4.4% giving back the 2-day rip before the binary.", "delta": "fade dodged"}
]
# applying + adjust unchanged (still today's plan)

# 8) paper equity mark refresh (pre-market)
d["paper"]["equity"] = 88880.77
d["paper"]["updated"] = TS
d["paper"]["equity_note"] = "Paper ~$88.9k (pre-market mark, -1.2% vs Mon's $89,998 close) - semis giving back the 2-day rip pre-open (NVDA/AMD/SMR soft) partly offset by OKLO's DOE nuclear catalyst; 6/6 GTC-stopped, zero naked."

# ---- backup current, then atomic write ----
shutil.cop(SRC, BACKUP) if False else shutil.copyfile(SRC, BACKUP)
fd, tmp = tempfile.mkstemp(dir=SITE, prefix=".engine-data.tmp-", suffix=".json")
with os.fdopen(fd, "w") as f:
    json.dump(d, f, ensure_ascii=False, indent=1)
os.replace(tmp, SRC)

# ---- read-back verify ----
v = json.load(open(SRC))
assert v["updated"] == TS, "updated mismatch"
assert v["accountability"]["final"] is False, "final should be False pre-open"
assert "TBD" in v["accountability"]["grade"], "grade should be TBD pre-open"
assert len(v["pending_tickets"]) == 1 and v["pending_tickets"][0]["id"] == "2026-07-21-1", "NVDA ticket missing"
assert v["pending_tickets"][0]["symbol"] == "NVDA" and v["pending_tickets"][0]["qty"] == 3
p1 = [c["ticker"] for c in v["coverage"] if c["projection"]["pop_rank"] == 1]
assert p1 == ["OKLO"], f"pop_rank1 should be OKLO, got {p1}"
assert len(v["pulse"]) == 15 and v["pulse"][0]["ts"] == TS, "pulse bad"
assert len(v["feed"]) == 40 and v["feed"][0]["ts"] == TS, "feed bad"
print("PUBLISH OK")
print("  updated:", v["updated"])
print("  grade:", v["accountability"]["grade"], "| final:", v["accountability"]["final"])
print("  pending:", v["pending_tickets"][0]["symbol"], v["pending_tickets"][0]["qty"], "sh, stop", v["pending_tickets"][0]["stop"])
print("  pop_rank1:", p1[0])
print("  pulse/feed:", len(v["pulse"]), "/", len(v["feed"]))
print("  paper equity:", v["paper"]["equity"])
print("  backup:", os.path.basename(BACKUP), os.path.getsize(BACKUP), "bytes")
