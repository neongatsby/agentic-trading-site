import json, os, tempfile

P = "engine-data.json"
d = json.load(open(P))
TS = "2026-07-22T04:19:00-04:00"

# ---------- PROJECTIONS + chg_pct (pre-market 7/22) ----------
# pre-market marks: holdings fresh from positions endpoint; watched non-holdings pre-open (~flat)
proj = {
 "OKLO": (4.0, "med", "DOE AI-energy summit today; +4.6% pre-mkt, sell-news risk", 1, "+4.6%"),
 "AMD":  (2.5, "med", "Advancing AI event today (MI355X/MI400); -2% pre-mkt", 2, "-2.3%"),
 "SMR":  (3.0, "med", "nuclear-for-AI sympathy on DOE catalyst; RS leader", 3, "+0.1%"),
 "NVDA": (1.5, "med", "AI-infra leader, no own-binary; live re-entry today", 4, "-1.0%"),
 "CEG":  (2.0, "med", "nuclear/power-for-AI on DOE catalyst", 5, "-0.4%"),
 "VRT":  (1.5, "low", "datacenter power/cooling, less extended", 6, "-0.1%"),
 "RGTI": (1.5, "low", "quantum risk-on bid; not owned", 7, "0.0%"),
 "IONQ": (1.0, "low", "quantum risk-on; not owned", 8, "0.0%"),
 "RKLB": (1.0, "low", "space momentum; not owned", 9, "0.0%"),
 "MU":   (0.0, "low", "extended +12% two days; digesting", 10, "0.0%"),
 "BE":   (-1.5,"low", "giveback risk after +14.8% squeeze", 11, "0.0%"),
 "TSLA": (0.0, "low", "reports tonight - binary, won't hold", 12, "0.0%"),
 "TQQQ": (1.0, "low", "3x powder parked till confirmed 20-day reclaim", 13, "0.0%"),
 "SOXL": (1.0, "low", "3x semis, gated OUT under the 20-day", 14, "0.0%"),
}
for c in d.get("coverage", []):
    t = c.get("ticker")
    if t in proj:
        tgt, conf, basis, rank, chg = proj[t]
        c["projection"] = {"target_pct": tgt, "confidence": conf, "basis": basis, "pop_rank": rank}
        c["chg_pct"] = chg
        c["updated"] = TS

# ---------- STATUS ----------
d["status"] = [{"session": "Pre-market", "text": "NVDA re-entry armed for open"}]

# ---------- HEADLINES ----------
d["headlines"] = [
 "Pre-mkt 7/22: DOE AI-energy summit TODAY - details on the $200M nuclear-for-AI program (OKLO, X-Energy, MSFT, NVDA); OKLO +4.6% pre-mkt",
 "BINARY WALL tonight: GOOGL + TSLA report after the close (first real AI-capex test); INTC follows Thursday",
 "AMD 'Advancing AI 2026' event today - MI355X launch, MI400 update; AMD -2% pre-mkt digesting a +8% day",
 "Regime risk-on: S&P at a record, QQQ $708.8 = -0.8% under its $714.7 20-day (re-entry zone), 2nd green session",
 "NVDA live swing armed for the 7/22 open - ends a 6-session live cash camp (3 sh, $186 stop, approve-anytime)",
 "Paper owns AMD/SMR/OKLO/VRT/CEG/NVDA - all 6 GTC-stopped, zero naked; OKLO the nuclear winner (+4.6% pre-mkt)",
 "Semis digest the 2-day memory rip (MU +12%): AMD/NVDA modestly red pre-market ahead of tonight's prints",
]

# ---------- PULSE (prepend one) ----------
pulse_new = {
 "ts": TS,
 "text": ("4:19a pre-market reconcile - both books == broker, zero naked. LIVE flat $810.32 cash (6th session) "
          "with the NVDA re-entry swing STAGED to fill at TODAY's open (3 sh ~$207, $186 stop, approve-anytime, "
          "0/3 same-day day-trades used) - firing it is the #1 action from yesterday's D+ (end the cash camp = the gate's re-entry). "
          "Fresh overnight catalyst: a Trump/DOE $200M nuclear-for-AI program (OKLO, X-Energy, MSFT, NVDA) with a DOE summit revealing details TODAY - "
          "OKLO +4.6% pre-mkt, owned in paper. Semis giving a little back pre-open (AMD -2.3%, NVDA -1.0%). "
          "Plan at the open: trim the paper NVDA anchor + trail OKLO/SMR stops up + lean the nuclear complex; NO fresh semi size into tonight's GOOGL/TSLA binary."),
 "hype": ("Pre-dawn check - books are clean and NVDA's still armed to buy the open, finally ending the 6-day cash streak. "
          "Overnight a government nuclear-for-AI push popped OKLO (we own it in paper); leaning that way today, but not chasing hot chips right before Google + Tesla report tonight."),
}
d["pulse"] = [pulse_new] + d.get("pulse", [])[:15]

# ---------- FEED (prepend one activity) ----------
feed_new = {
 "type": "activity",
 "ts": TS,
 "text": ("4:19am pre-market reconcile - both books == broker, zero naked. LIVE flat $810 cash (6th session); NVDA re-entry swing staged to fill at TODAY's open "
          "($186 stop, 0/3 day-trades). PAPER 6/6 GTC-stopped; OKLO +4.6% pre-mkt on the fresh DOE nuclear-for-AI program (summit details today). "
          "At the open: trim NVDA anchor, trail OKLO/SMR stops, lean nuclear; no fresh semi size into tonight's GOOGL/TSLA binary."),
}
d["feed"] = [feed_new] + d.get("feed", [])[:40]

# ---------- PENDING TICKETS (refresh NVDA note to 'today') ----------
d["pending_tickets"] = [{
 "id": "2026-07-21-1",
 "symbol": "NVDA",
 "side": "buy",
 "size": "$633",
 "qty": 3,
 "entry": "~$207 - approve ANYTIME -> fills at TODAY's (7/22) open. Multi-day swing, PDT-free (0/3 day-trades used). Marketable-limit $211 gives a gap-up cushion; taps before 4pm fill immediately.",
 "trigger": None,
 "stop": 186,
 "bracket": "stop $186 GTC (below the late-June $192 base, -10.2%)",
 "thesis": "Ends a 6th day of live cash by owning the AI-infra/semis leader via the NON-extended name. NVDA reclaimed its 20-day (~$201.7), sits mid-range, is -1% pre-mkt (cheaper entry), holds a ~$5B Nebius stake + is named in the DOE AI-energy program, and has NO own earnings binary this week (GOOGL/TSLA print tonight, NVDA doesn't). Wide $186 stop. This IS the gate re-entry - fires at the open.",
}]

# ---------- ACCOUNTABILITY (fresh 7/22 running card) ----------
d["accountability"] = {
 "date": "2026-07-22",
 "final": False,
 "grade": "TBD (pre-open)",
 "headline": ("Pre-market: the live NVDA re-entry is staged to fire at the open - ending a 6-session cash camp is today's #1 action (the gate's missing re-entry). "
              "Fresh DOE nuclear-for-AI catalyst has OKLO +4.6% pre-mkt (owned in paper); semis give a little back before tonight's GOOGL/TSLA binary."),
 "capture": {"bestName": "TBD - market not open (OKLO +4.6% pre-mkt leads the watchlist so far)", "bestPct": "-", "capturedPct": "-", "rate": "pre-open"},
 "missed": [],
 "saved": [{"note": "Zero naked into the open - all 6 paper positions GTC-stopped, live flat; verified at the broker this run", "delta": "risk bounded"}],
 "best": {"name": "-", "note": "TBD (pre-open)", "delta": "-"},
 "worst": {"name": "-", "note": "TBD (pre-open)", "delta": "-"},
 "applying": "Gate RE-ENTRY rule (new 7/21 lesson): 2 green sessions + QQQ within ~1% of its 20-day (-0.8%) + theme on a real catalyst all line up -> re-enter the leader at the open. Firing the staged NVDA swing.",
 "adjust": "Weight to the MOVER, not the anchor: at the open trim the paper NVDA anchor (~32% of book) and lean the freed capital into the nuclear-for-AI complex (OKLO/SMR/CEG) on the live DOE-summit catalyst; keep live to the risk-managed NVDA core (don't chase +10% OKLO with the real-money sleeve).",
}

# ---------- LIVE / PAPER blocks (refresh notes/marks) ----------
if "live" in d:
    d["live"]["equity"] = 810.32
    d["live"]["cash"] = 810.32
    d["live"]["positions"] = []
    d["live"]["updated"] = TS
    d["live"]["equity_note"] = ("LIVE flat $810.32 cash / zero positions / zero naked (6th cash session). "
        "1 staged ticket = BUY NVDA 3 sh (~$207, $186 stop) set to fill at TODAY's 7/22 open - approve anytime. Firing it is the plan's #1 action.")
if "paper" in d:
    d["paper"]["equity"] = 89694.98
    d["paper"]["updated"] = TS
    d["paper"]["equity_note"] = ("Paper ~$89.7k (pre-market mark, -0.3% vs Mon's $89,998 provisional close) - semis giving back "
        "(AMD -2.3%, NVDA -1.0%) partly offset by OKLO +4.6% on the DOE nuclear catalyst. 6 names, all GTC-stopped, zero naked. "
        "Plan at the open: trim the NVDA anchor + trail OKLO/SMR stops up + lean the nuclear complex.")

# score unchanged (no new live closed trades); keep as-is
d["updated"] = TS

# ---------- ATOMIC WRITE ----------
fd, tmp = tempfile.mkstemp(dir=".", prefix=".ed_", suffix=".json")
with os.fdopen(fd, "w") as f:
    json.dump(d, f, ensure_ascii=False, indent=1)
os.replace(tmp, P)
print("WROTE", P)
