#!/usr/bin/env python3
"""Atomic engine-data.json publish for the 2026-07-22 07:46a pre-market run.
Unique per-run script name + atomic os.replace + read-back verify (per OPS-ALERT-engine-data-clobber-2026-07-20)."""
import json, os, shutil, tempfile, sys

SITE = os.path.dirname(os.path.abspath(__file__))
PATH = os.path.join(SITE, "engine-data.json")
TS = "2026-07-22T07:46:00-04:00"

with open(PATH) as f:
    d = json.load(f)

# --- backup current good state before mutating ---
shutil.copy2(PATH, os.path.join(SITE, "engine-data.backup-2026-07-22-0746.json"))

# 1) status
d["status"] = [{"session": "Pre-market", "text": "Books clean; NVDA armed for the open"}]

# 2) headlines
d["headlines"] = [
    "BINARY tonight: GOOGL + TSLA + IBM + TXN all report after today's close — the big Mag-7 AI-capex test",
    "Futures lower, chips cooling: MU gives back part of its +12.8% as the 2-day semi rip digests",
    "OKLO / X-Energy confirmed in a Trump/DOE program to fast-track nuclear reactors for AI data centers",
    "NVDA + Wistron open a $700M Fort Worth plant for GB300 + Vera Rubin superchips",
    "Regime in the re-entry zone: QQQ $708.97 = -0.8% under its $714.67 20-day; S&P near a record",
    "Oil stays elevated (~$95) on Mideast risk — the overhang capping a risk-off open",
    "NVDA live swing armed for the 9:30 open — ends a 6-session live cash camp (3 sh, $186 stop, approve-anytime)",
    "Fear & Greed still in 'Fear' despite the Nasdaq's +1% Tuesday",
]

# 3) coverage projections + chg_pct (pre-open: no official move / SIP prints unavailable this run)
proj = {
 "NVDA": {"target_pct":0.5,"confidence":"med","basis":"least-extended AI leader + $700M Vera Rubin plant; chips cooling","pop_rank":4},
 "AMD":  {"target_pct":-0.5,"confidence":"med","basis":"owned leader digesting +8%; chips cool pre-open","pop_rank":5},
 "SMR":  {"target_pct":2.0,"confidence":"med","basis":"nuclear-for-AI sympathy with OKLO DOE catalyst","pop_rank":2},
 "MU":   {"target_pct":-2.0,"confidence":"med","basis":"extended after +12.8%; giving back pre-market","pop_rank":10},
 "BE":   {"target_pct":-2.5,"confidence":"med","basis":"spent parabolic after +14.8%; give-back risk","pop_rank":11},
 "OKLO": {"target_pct":3.5,"confidence":"med","basis":"confirmed Trump/DOE nuclear-for-AI program; RS leader","pop_rank":1},
 "RGTI": {"target_pct":0.0,"confidence":"low","basis":"quantum high-beta; tracks the cooling tape","pop_rank":9},
 "VRT":  {"target_pct":-0.5,"confidence":"low","basis":"data-center power giving back on a risk-off open","pop_rank":6},
 "IONQ": {"target_pct":0.0,"confidence":"low","basis":"quantum beta; cools with a risk-off tape","pop_rank":8},
 "RKLB": {"target_pct":0.5,"confidence":"low","basis":"space momentum, no fresh catalyst; tape-dependent","pop_rank":7},
 "CEG":  {"target_pct":1.0,"confidence":"med","basis":"nuclear utility rides the AI-power bid; steady","pop_rank":3},
 "TSLA": {"target_pct":0.0,"confidence":"med","basis":"reports after the close — the move is tonight","pop_rank":14},
 "SOXL": {"target_pct":-1.5,"confidence":"low","basis":"3x semis gated; chips cool into the binary","pop_rank":12},
 "TQQQ": {"target_pct":0.0,"confidence":"low","basis":"3x Nasdaq powder; awaits a QQQ 20-day reclaim","pop_rank":13},
}
for c in d["coverage"]:
    t = c["ticker"]
    if t in proj:
        c["projection"] = proj[t]
    c["chg_pct"] = "0.0%"   # pre-open; official move populates at the 9:30 open
    c["updated"] = TS

# 4) pulse (prepend one; keep ~15)
pulse_text = ("7:46a pre-market - confirming heartbeat ~35 min on from 7:11a; fresh 7:30-9:30 wires only harden the plan. "
    "Futures are lower and chips are cooling (MU giving back part of its +12.8%; NVDA a mild positive on the Wistron $700M Vera-Rubin plant) "
    "into tonight's GOOGL/TSLA/IBM/TXN after-close binary - so no fresh semi size and no pre-market execution by design. "
    "Both books == broker, zero naked: LIVE flat $810.32 cash (7th session pending) with the NVDA re-entry armed to fill at the 9:30 open "
    "($186 stop, 0/3 day-trades); PAPER 6/6 GTC-stopped. QQQ -0.8% under its 20-day = re-entry zone holds; pop_rank 1 = OKLO on the confirmed DOE nuclear-for-AI catalyst. "
    "At the open: fire NVDA live + trim the paper NVDA anchor toward the nuclear movers.")
pulse_hype = ("Nothing to fire pre-open - the NVDA buy's armed for the open and everything's stopped. "
    "Not adding chips into tonight's Google/Tesla earnings; nuclear (OKLO) is my top pick on the government catalyst.")
d["pulse"] = [{"ts": TS, "text": pulse_text, "hype": pulse_hype}] + d["pulse"]
d["pulse"] = d["pulse"][:15]

# 5) feed (prepend one activity; keep ~40)
feed_text = ("7:46a pre-market - confirming heartbeat: re-checked both books at the broker (LIVE flat $810.32 cash / 0 orders; "
    "PAPER 6/6 GTC-stopped - AMD/SMR/OKLO/VRT/CEG/NVDA; zero naked). Fresh wires confirm futures lower + chips cooling (MU giving back) "
    "into tonight's GOOGL/TSLA/IBM/TXN binary; OKLO/X-Energy DOE nuclear-for-AI program corroborated; NVDA+Wistron $700M Vera-Rubin plant opened. "
    "Regime unchanged (QQQ -0.8% under its 20-day, re-entry zone). NVDA live swing armed for the 9:30 open; no pre-market execution by design.")
d["feed"] = [{"type": "activity", "ts": TS, "text": feed_text}] + d["feed"]
d["feed"] = d["feed"][:40]

# 6) accountability (running, pre-open)
a = d["accountability"]
a["date"] = "2026-07-22"
a["final"] = False
a["grade"] = "TBD (pre-open)"
a["headline"] = ("Pre-market (7:46a): confirming heartbeat - both books re-reconciled clean (LIVE flat cash, PAPER 6/6 GTC-stopped, zero naked). "
    "Futures lower / chips cooling (MU giving back its +12.8%) into tonight's GOOGL+TSLA+IBM+TXN after-close binary; QQQ -0.8% under its 20-day holds the re-entry zone. "
    "Plan armed for the OPEN - fire the staged NVDA re-entry to end the 6-session cash camp, trim the paper NVDA anchor toward the nuclear movers, add NO fresh semi size into the print.")
a["capture"] = {
    "bestName": "TBD - pre-open (OKLO leads the watchlist on the confirmed DOE nuclear-for-AI catalyst)",
    "bestPct": "-", "capturedPct": "-", "rate": "pre-open"}
a["saved"] = [{
    "note": "Zero naked into the open - all 6 paper positions GTC-stopped (verified at the broker), live flat; independently re-reconciled this run (7:46a)",
    "delta": "risk bounded"}]
a["applying"] = ("Gate RE-ENTRY rule (7/21 lesson): 2 green sessions (7/20+7/21) + QQQ within ~1% of its 20-day (-0.8%) + theme on a real, corroborated catalyst "
    "(nuclear-for-AI) all line up -> re-enter the leader at the OPEN. Firing the staged NVDA swing ends the 6-session cash camp.")
a["adjust"] = ("Weight to the MOVER not the anchor AND don't chase extension: at the open trim the ~32%-of-book paper NVDA anchor and redeploy into relative strength that ISN'T parabolic "
    "- don't chase the extended OKLO/SMR pop at its highs; keep live to the risk-managed NVDA core, no fresh semi size into tonight's GOOGL/TSLA binary.")

# 7) latest_recap rotate (preserve old under a free unique key)
d["_latest_recap_prev1"] = d.get("latest_recap", "")
d["latest_recap"] = ("7:46a 7/22 pre-market (market CLOSED, opens 9:30) - confirming heartbeat ~35 min on from the 7:11a run; nothing changes the plan. "
    "Fresh 7:30-9:30 wires HARDEN the caution: S&P/Nasdaq futures lower, chips cooling (MU giving back part of its +12.8% surge; AMD ~$533 into an Aug-4 print; "
    "NVDA a mild positive on the Wistron $700M Fort Worth Vera-Rubin plant) into tonight's after-close binary wall - GOOGL + TSLA + IBM + TXN all report - "
    "so NO fresh semi size and no pre-market execution by design. Both books == broker, zero naked: LIVE flat $810.32 cash (7th session unless tapped) with NVDA live ticket "
    "2026-07-21-1 (3 sh, marketable-limit $211, $186 stop) ARMED to fill at the 9:30 open - approve anytime, 0/3 day-trades, PDT-free swing; PAPER 6 names ALL GTC-stopped "
    "(AMD $490 / SMR $7.50 / OKLO $39 / VRT $282 / CEG $236 / NVDA $186), each clear of its stop. Regime UNCHANGED, recomputed off 7/21 closes: QQQ $708.97 vs its $714.67 20-day "
    "= -0.8% under = the re-entry zone (2 green sessions 7/20+7/21 + theme on a real catalyst) -> firing NVDA at the open IS the gate re-entry (7/21 lesson). pop_rank 1 = OKLO on the "
    "corroborated Trump/DOE nuclear-for-AI program (OKLO/X-Energy). DATA NOTE: SIP recent-data subscription blocked this run so pre-market prints aren't on the feed - chg_pct is pre-open "
    "and repopulates at the 9:30 open; decisions rest on 7/21 closes + the regime calc + fresh news. AT THE OPEN: fire NVDA live + trim the ~32%-of-book paper NVDA anchor toward the "
    "nuclear movers (OKLO/SMR/CEG) without chasing the extended pop; no fresh semis into the binary. Grade running: pre-open (TBD).")

# 8) top-level updated
d["updated"] = TS

# --- atomic write + read-back verify ---
fd, tmp = tempfile.mkstemp(dir=SITE, prefix=".engine-data.", suffix=".tmp")
with os.fdopen(fd, "w") as f:
    json.dump(d, f, ensure_ascii=False, indent=1)
os.replace(tmp, PATH)

# verify
with open(PATH) as f:
    chk = json.load(f)
assert chk["updated"] == TS, "updated mismatch"
assert chk["accountability"]["final"] is False
assert len(chk["pending_tickets"]) == 1 and chk["pending_tickets"][0]["symbol"] == "NVDA"
ranks = sorted(c["projection"]["pop_rank"] for c in chk["coverage"])
assert ranks == list(range(1, len(chk["coverage"]) + 1)), f"pop_rank not unique 1..N: {ranks}"
top = [c["ticker"] for c in chk["coverage"] if c["projection"]["pop_rank"] == 1]
assert top == ["OKLO"], f"pop_rank 1 = {top}"
print("OK verified. updated:", chk["updated"])
print("pulse[0].ts:", chk["pulse"][0]["ts"], "| pulse len:", len(chk["pulse"]))
print("feed len:", len(chk["feed"]), "| coverage:", len(chk["coverage"]))
print("pop_rank1:", top, "| grade:", chk["accountability"]["grade"])
print("live:", chk["live"]["equity"], "| paper:", chk["paper"]["equity"])
