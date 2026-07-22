#!/usr/bin/env python3
# Per-run publish (2026-07-22 05:17 ET pre-market heartbeat). Unique name, atomic write, verified read-back.
import json, os, tempfile

SITE = os.path.dirname(os.path.abspath(__file__))
PATH = os.path.join(SITE, "engine-data.json")
TS   = "2026-07-22T05:17:00-04:00"

with open(PATH) as f:
    d = json.load(f)

d["updated"] = TS

# ---- PULSE (prepend one; keep ~15) ----
pulse_text = ("5:17a pre-market - corroborated today's catalysts on the wire before the open. Bloomberg confirms "
    "Oklo + X-Energy joined a Trump/DOE program to fast-track nuclear reactors for AI data centers (why OKLO gapped "
    "~6% - we own 200 sh in paper), and TSLA reports Q2 tonight alongside GOOGL: the first real AI-capex binary. "
    "Futures are indicated slightly lower on higher oil, so semis are digesting the 2-day memory rip (MU +12%) into "
    "the print. Nothing to execute pre-open: LIVE flat $810 / zero naked (6th session) with the NVDA re-entry armed "
    "to fire at 9:30 ($186 stop, 0/3 day-trades); PAPER 6/6 GTC-stopped. At the open I fire the NVDA swing (the gate "
    "re-entry), trim the ~32%-of-book paper NVDA anchor, and lean the nuclear-for-AI names - without chasing the "
    "parabolic +6-9% movers into tonight's binary.")
pulse_hype = ("Everything's clean and stopped, just waiting on 9:30. Confirmed the nuclear-for-AI news that popped OKLO "
    "and that Tesla + Google report tonight, so I'll fire the NVDA buy at the open but not chase hot chips into the print.")
d["pulse"] = [{"ts": TS, "text": pulse_text, "hype": pulse_hype}] + d.get("pulse", [])
d["pulse"] = d["pulse"][:15]

# ---- FEED (prepend one activity; keep ~40) ----
feed_text = ("5:17am pre-market - corroborated catalysts on the wire: Bloomberg confirms OKLO/X-Energy joined the "
    "Trump/DOE nuclear-for-AI program (OKLO's gap), TSLA+GOOGL report tonight, futures indicated lower on oil. Both "
    "books == broker, zero naked. NVDA re-entry armed for the open; plan holds - fire NVDA, trim the paper NVDA "
    "anchor, lean nuclear, no chase into the binary.")
d["feed"] = [{"type": "activity", "ts": TS, "text": feed_text}] + d.get("feed", [])
d["feed"] = d["feed"][:40]

# ---- STATUS ----
d["status"] = [{"session": "Pre-market", "text": "NVDA armed; catalysts confirmed"}]

# ---- HEADLINES ----
d["headlines"] = [
    "Wire confirms it: Bloomberg - Oklo & X-Energy join a Trump/DOE program to fast-track nuclear reactors for AI (OKLO gapped ~6%)",
    "BINARY tonight: TSLA + GOOGL report after the close - first real AI-capex test; futures indicated lower on higher oil",
    "AMD 'Advancing AI 2026' event today (MI355X launch / MI400 update); AMD ~-2% pre-mkt digesting a +8% day",
    "Regime in the re-entry zone: S&P at a record, QQQ $709 = -0.8% under its $714.7 20-day, 2nd green session",
    "NVDA live swing armed for the open - ends a 6-session live cash camp (3 sh, $186 stop, approve-anytime)",
    "Paper owns AMD/SMR/OKLO/VRT/CEG/NVDA - all 6 GTC-stopped, zero naked; OKLO the nuclear winner",
    "Semis digest the 2-day memory rip into tonight's prints; SK Hynix denies the Intel-Ohio buyout report",
]

# ---- ACCOUNTABILITY (running pre-open; not final) ----
a = d.get("accountability", {})
a["date"] = "2026-07-22"
a["final"] = False
a["grade"] = "TBD (pre-open)"
a["headline"] = ("Pre-market: catalysts corroborated on the wire (Bloomberg - OKLO/X-Energy join the DOE nuclear-for-AI push; "
    "TSLA+GOOGL report tonight). Firing the staged NVDA re-entry at the open is today's #1 action - it ends a 6-session cash "
    "camp (the gate's missing re-entry). Semis soft pre-open on higher oil into tonight's binary; not chasing extension.")
a["capture"] = {
    "bestName": "TBD - pre-open (OKLO leads the watchlist on the fresh DOE nuclear-for-AI catalyst)",
    "bestPct": "-", "capturedPct": "-", "rate": "pre-open"}
a["saved"] = [{"note": "Zero naked into the open - all 6 paper positions GTC-stopped, live flat; independently re-verified at the broker this run", "delta": "risk bounded"}]
a["applying"] = ("Gate RE-ENTRY rule (7/21 lesson): 2 green sessions + QQQ within ~1% of its 20-day (-0.8%) + theme on a real, "
    "corroborated catalyst (nuclear-for-AI) all line up -> re-enter the leader at the OPEN. Firing the staged NVDA swing.")
a["adjust"] = ("Weight to the MOVER not the anchor AND don't chase extension (the 7/21 core tension): at the open trim the "
    "~32%-of-book paper NVDA anchor and redeploy into relative strength that ISN'T parabolic - avoid chasing +6-9% OKLO/SMR at "
    "their highs into the DOE reveal; keep live to the risk-managed NVDA core, no fresh semi size into tonight's GOOGL/TSLA binary.")
d["accountability"] = a

# ---- PROJECTIONS (measured refresh; futures indicated lower into tonight's binary) ----
proj = {
    "OKLO": {"target_pct": 3.0, "confidence": "med", "basis": "DOE nuclear-for-AI summit reveals details today; owned", "pop_rank": 1},
    "AMD":  {"target_pct": 2.0, "confidence": "med", "basis": "Advancing AI event today (MI355X/MI400); digesting +8%", "pop_rank": 2},
    "SMR":  {"target_pct": 2.0, "confidence": "med", "basis": "nuclear-for-AI complex bid; extended +9%", "pop_rank": 3},
    "CEG":  {"target_pct": 1.8, "confidence": "med", "basis": "nuclear-for-AI beneficiary, least-extended of the group", "pop_rank": 4},
    "NVDA": {"target_pct": 1.0, "confidence": "med", "basis": "least-extended AI leader; live re-entry, no own binary", "pop_rank": 5},
    "VRT":  {"target_pct": 1.2, "confidence": "low", "basis": "AI-datacenter power/cooling, tracks the complex", "pop_rank": 6},
    "RKLB": {"target_pct": 1.5, "confidence": "low", "basis": "space momentum, on the SMCI/RKLB radar", "pop_rank": 7},
    "RGTI": {"target_pct": 1.0, "confidence": "low", "basis": "quantum high-beta, tracks risk appetite", "pop_rank": 8},
    "IONQ": {"target_pct": 1.0, "confidence": "low", "basis": "quantum high-beta, no fresh catalyst", "pop_rank": 9},
    "MU":   {"target_pct": -0.5, "confidence": "med", "basis": "digesting the +12% memory blowout into a semis pullback", "pop_rank": 10},
    "BE":   {"target_pct": -2.0, "confidence": "med", "basis": "extended +15%; fade risk + short-seller overhang", "pop_rank": 11},
    "TSLA": {"target_pct": 0.0, "confidence": "med", "basis": "coiled into tonight's Q2 earnings binary", "pop_rank": 12},
    "TQQQ": {"target_pct": 0.5, "confidence": "low", "basis": "3x QQQ - gated (QQQ under 20-day), no re-lever", "pop_rank": 13},
    "SOXL": {"target_pct": 0.5, "confidence": "low", "basis": "3x semis, extended, avoid into the binary", "pop_rank": 14},
}
for c in d.get("coverage", []):
    t = c.get("ticker")
    if t in proj:
        c["projection"] = proj[t]
        c["updated"] = TS

# ---- LIVE / PAPER marks (real broker numbers this run) ----
if "live" in d:
    d["live"]["equity"] = 810.32
    d["live"]["cash"] = 810.32
    d["live"]["positions"] = []
    d["live"]["updated"] = TS
if "paper" in d:
    d["paper"]["equity"] = 89563.74
    d["paper"]["updated"] = TS
    d["paper"]["equity_note"] = ("Paper ~$89.56k (pre-market mark, -0.5% vs Mon's $89,998 close) - semis giving a little back "
        "pre-open (AMD/NVDA soft) partly offset by OKLO's DOE nuclear catalyst; 6/6 GTC-stopped, zero naked.")

# ---- ATOMIC WRITE ----
fd, tmp = tempfile.mkstemp(dir=SITE, prefix=".engine-data.", suffix=".tmp")
with os.fdopen(fd, "w") as f:
    json.dump(d, f, ensure_ascii=False, indent=1)
os.replace(tmp, PATH)

# ---- VERIFY READ-BACK ----
with open(PATH) as f:
    v = json.load(f)
ranks = sorted((c.get("projection") or {}).get("pop_rank") for c in v.get("coverage", []))
n1 = sum(1 for c in v.get("coverage", []) if (c.get("projection") or {}).get("pop_rank") == 1)
print("updated:", v["updated"])
print("pulse[0].ts:", v["pulse"][0]["ts"], "| len pulse:", len(v["pulse"]))
print("feed[0].ts:", v["feed"][0]["ts"], "| len feed:", len(v["feed"]))
print("accountability.final:", v["accountability"]["final"], "| grade:", v["accountability"]["grade"])
print("pending_tickets:", [(p.get("id"), p.get("symbol")) for p in v.get("pending_tickets", [])])
print("pop_rank==1 count:", n1, "| ranks:", ranks)
print("live.equity:", v["live"]["equity"], "| paper.equity:", v["paper"]["equity"])
print("OK VALID JSON")
