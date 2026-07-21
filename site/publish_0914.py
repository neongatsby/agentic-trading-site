import json, os, shutil, datetime

ED = "engine-data.json"
TS = "2026-07-21T09:14:00-04:00"

d = json.load(open(ED))

# ---- backup the good current state first ----
shutil.copyfile(ED, "engine-data.backup-2026-07-21-0914.json")

d["updated"] = TS

# ---------- PULSE (prepend one, keep 15) ----------
new_pulse = {
  "ts": TS,
  "text": ("9:14am, ~15 min to the bell. Fresh pull: the chip pop is HOLDING into the open - "
    "SOXL +13%, INTC +5.3% (now an Intel-Fortinet security-chip deal on top of the first High-NA EUV in production), "
    "BE +5.4%, AMD +3.8% into its Advancing AI event - and NVDA is finally confirming a touch better (+1.4% vs +0.8% earlier). "
    "But we're still under the line: QQQ ~$705 is ~1.6% below its $716 20-day, so the gate stays SHUT (day 6) and I'm not chasing "
    "the gated 3x that's round-tripped 5 sessions straight (Benzinga even flags the momentum trade 'broke' - SPMO's worst month ever "
    "on the memory selloff). Plan locked into the open: the funded PLTR live buy stays staged (1x RS leader, -0.9% = a cheaper entry, no binary); "
    "paper holds 4/4 incl. the SQQQ hedge into Wed's GOOGL/TSLA/INTC prints. At the open I add a 1x leader (AMD/NVDA, never SOXL) with paper "
    "powder ONLY if NVDA holds green and QQQ presses $716. Day-trade budget 0/3."),
  "hype": ("Chips are still ripping into the open and NVDA's finally perking up, but we're under the line so no chasing the 3x - it's faded 5 days straight. "
    "Live PLTR buy's set for the bell; if the move actually holds I'll add a regular chip name in paper, not the leveraged one.")
}
d["pulse"] = [new_pulse] + d["pulse"]
d["pulse"] = d["pulse"][:15]

# ---------- FEED (prepend one activity, keep ~40) ----------
new_feed = {
  "ts": TS,
  "type": "activity",
  "text": ("9:14am pre-open (~15 min to bell): chip pop holding - SOXL +13%, INTC +5.3% (Intel-Fortinet deal + High-NA EUV), "
    "AMD +3.8%, NVDA confirming +1.4%. But QQQ ~$705 < $716 20-day -> gate shut day 6, no 3x chase (Benzinga: momentum trade 'broke', "
    "SPMO worst month ever). PLTR live buy staged for the open; paper holds 4/4 incl. the SQQQ hedge into Wed's GOOGL/TSLA/INTC wall. "
    "Add a 1x leader (AMD/NVDA) at the open only on a confirmed hold. Both books clean, 0/3 day-trades.")
}
d["feed"] = [new_feed] + d["feed"]
d["feed"] = d["feed"][:40]

# ---------- STATUS ----------
d["status"] = [
  {"session": "Pre-market", "text": "Chips hold: SOXL +13%, INTC +5.3%"},
  {"session": "Open plan", "text": "PLTR fills 9:30; 1x add on confirm"},
  {"session": "Books", "text": "Live $810 cash; paper 4/4 stopped"}
]

# ---------- HEADLINES ----------
d["headlines"] = [
  "Chip rally holds into the open - SOXL +13%, INTC +5.3%, AMD +3.8%, BE +5.4% premarket - on AMD's 'Advancing AI 2026' (7/22-23) + MSFT Helios, Intel's first High-NA EUV in production, and a new Intel-Fortinet security-chip deal.",
  "But it stays NARROW and gated: NVDA only +1.4%, and QQQ ~$705 is still ~1.6% under its $716 20-day - the same setup whose chip pops have round-tripped 5 sessions running.",
  "Warning under the hood: Benzinga flags the momentum trade 'broke' - the SPMO momentum ETF is having its worst month ever on the Micron/memory-chip selloff.",
  "NQ futures +1.3% / S&P +0.4% on chip strength + Iran ceasefire hopes easing oil; Kimi-K3 AI demand + IREN's raised $4B AI-cloud guide feed the bid.",
  "Big Tech earnings wall this week: GOOGL + TSLA Wed 7/22 AMC, INTC Thu 7/23 - the paper SQQQ hedge is insurance into it. TSLA soft (lease hikes + robotaxi fears).",
  "PLTR the clean 1x RS leader (no gate, Aug-3 earnings), -0.9% premarket = a cheaper entry - the funded live buy stays staged for the open.",
  "Regime gate SHUT day 6: no leveraged-index longs (SOXL/TQQQ/FNGU/UPRO off) until QQQ reclaims its 20-day on volume."
]

# ---------- COVERAGE (chg_pct + projection + updated) ----------
cov = {
 "PLTR": (-0.9, 1.5, "med", "RS leader; red premkt = cheaper swing entry, no earnings", 5),
 "AMD":  (3.8, 3.5, "med", "Advancing-AI event 7/22 + MSFT Helios momentum; chase-flagged", 1),
 "INTC": (5.3, 4.0, "med", "High-NA EUV first + Fortinet deal; earnings Thu caps", 3),
 "NVDA": (1.4, 2.0, "med", "confirming 1x semi leader/breadth tell; China-AI overhang", 2),
 "VRT":  (3.2, 2.5, "low", "AI-power/cooling bid rides the chip tape", 7),
 "SOXL": (13.0, 5.0, "low", "biggest mover but gated 3x, faded 5 sessions", 4),
 "TQQQ": (3.75, 3.0, "low", "gated 3x Nasdaq; off until QQQ>20-day", 11),
 "CEG":  (0.0, 0.5, "med", "AI-power hold, no premkt print, ~flat", 13),
 "FNGU": (3.0, 2.5, "low", "gated 3x FANG+; off until QQQ>20-day", 12),
 "IONQ": (3.2, 2.5, "low", "quantum beta rides the risk-on tape", 8),
 "RKLB": (2.0, 2.0, "low", "space beta, modest bid", 9),
 "SQQQ": (-3.9, -3.5, "med", "inverse hedge; pays if the chip pop fades again", 15),
 "TSLA": (0.5, 0.5, "low", "soft into Wed earnings; lease hikes, robotaxi fears", 14),
 "BE":   (5.4, 3.0, "low", "dead-cat bounce off -8% flush; earnings 7/28", 6),
 "SMR":  (1.9, 2.0, "low", "nuclear/SMR beta with risk-on", 10),
}
for c in d["coverage"]:
    t = c["ticker"]
    if t in cov:
        chg, tgt, conf, basis, rank = cov[t]
        c["chg_pct"] = chg
        c["projection"] = {"target_pct": tgt, "confidence": conf, "basis": basis, "pop_rank": rank}
        c["updated"] = "9:14a"

# PLTR extra freshening
for c in d["coverage"]:
    if c["ticker"] == "PLTR":
        c["size_note"] = "doubled in paper (100 sh); live PLTR buy staged for the 7/21 open (ticket 2026-07-20-3, 5 sh, $122 stop)"
        c["plan_usd"] = "live ~$680 into PLTR - ticket 2026-07-20-3, approve anytime = buy at the 9:30 open"

# ---------- ACCOUNTABILITY (running pre-open) ----------
a = d["accountability"]
a["date"] = "2026-07-21"
a["final"] = False
a["grade"] = "running (pre-open)"
a["headline"] = ("Pre-open 7/21 (running, ~15 min to the bell): the chip pop is HOLDING - SOXL +13% / INTC +5.3% / AMD +3.8% / BE +5.4% - "
  "and NVDA finally confirms a touch (+1.4%), but QQQ ~$705 is still ~1.6% under its $716.12 20-day, so the gate holds SHUT (d6) and I'm "
  "not chasing the 3x that's faded 5 sessions running (Benzinga: the momentum trade 'broke', SPMO's worst month ever). The 7/20 D-fix stays "
  "in motion - the funded PLTR live buy is STAGED for the OPEN (1x RS leader, -0.9% = cheaper entry, no binary). Honest top pop-pick is AMD "
  "into its 7/22-23 event; the gate-compliant capture plan is to add the 1x leader (AMD/NVDA, never SOXL) with paper powder on a confirmed "
  "open hold. Capture risk owned: if the chip bid HOLDS today, AMD/INTC out-pop my staged PLTR. Grade finalizes post-close.")
a["capture"] = {
  "bestName": "TBD at the close",
  "bestPct": "-",
  "capturedPct": "-",
  "rate": "pending - pre-open; live set to own PLTR at the open, paper owns it + the hedge, 1x-leader add planned on a confirmed open hold"
}
a["saved"] = [
  {"note": "Kept the leader-buy STAGED for the OPEN (approve-anytime -> fills 9:30), holding yesterday's cut+rotate-EARLIER D-fix in motion instead of a late-3pm proposal", "delta": "fix applied"},
  {"note": "Held the regime gate a 6th day - refused to chase the 3x semis into a +13% SOXL / +5.3% INTC premarket pop that, 5 sessions running, has round-tripped back under the 20-day (Benzinga: momentum trade 'broke')", "delta": "discipline intact"}
]
a["best"] = {
  "name": "PLTR (staged live + owned paper)",
  "note": "the 1x RS leader, no gate, intact catalyst (Nvidia partnership, Army NGC2, no earnings until Aug 3) - set to be owned in BOTH books at the open",
  "delta": "selection + execution aligned pre-open"
}
a["worst"] = {"name": "-", "note": "no trades yet today; grade finalizes post-close", "delta": "-"}
a["applying"] = ("PLAYBOOK Earned Rule #1 (regime gate) + 'cut+rotate EARLIER' (7/20 D-fix): no leveraged-index long while QQQ < its 20-day even on a "
  "+13% SOXL premarket pop that's faded all week; the PLTR leader-buy is staged for the OPEN so the rotation completes early instead of camping cash.")
a["adjust"] = ("At the open: if the semi strength is REAL and BROAD (NVDA confirms green, QQQ pressing/through $716) - deploy paper dry powder into the "
  "1x leader (AMD into its 7/22 event / NVDA), NOT the gated 3x, and trim the SQQQ hedge toward $716. If it fades AGAIN (the 5-day pattern - NVDA rolls, "
  "QQQ rejects $716) - keep the hedge into Wed's GOOGL/TSLA/INTC prints and let the PLTR live buy ride. Be IN pop_rank-1 AMD via paper on a confirmed hold; "
  "don't chase the premarket HOD.")

# ---------- LIVE / PAPER blocks ----------
d["live"]["equity"] = 810.32
d["live"]["cash"] = 810.32
d["live"]["positions"] = []
d["live"]["updated"] = TS
d["live"]["equity_note"] = ("Flat/clean cash ($810.32), zero positions/orders, nothing naked. PLTR buy staged for the 7/21 open "
  "(ticket 2026-07-20-3, 5 sh, ~$135 marketable, $122 GTC stop, approve-anytime -> fills at 9:30). Broker-verified 09:09 ET.")

d["paper"]["equity"] = 89260.98
d["paper"]["updated"] = TS
d["paper"]["equity_note"] = ("Paper ~$89.26k (-0.4% vs Mon as the SQQQ hedge bleeds into the gap-up), 4/4 GTC-stopped, zero naked "
  "(PLTR 100/$125, NVDA 90/$186, CEG 16/$236, SQQQ 310/$38). ~$40.5k (~45%) dry powder held for the open: on a CONFIRMED broad semi hold "
  "(NVDA green, QQQ -> $716) add the 1x leader (AMD into its 7/22 event / NVDA) - NOT the gated 3x - and trim SQQQ; if it fades again, keep the hedge into Wed's prints.")

# ---------- latest_recap ----------
d["latest_recap"] = ("Pre-open 7/21 (~15 min to bell) - chip pop holding (SOXL +13%, INTC +5.3%, AMD +3.8%) but gate still SHUT "
  "(QQQ ~$705 vs $716 20-day, NVDA only +1.4%), so no 3x chase. Funded PLTR live buy staged for the open (Monday's cash-locked-D fix). "
  "Live flat $810 cash; paper 4/4 GTC-stopped, ~45% powder for the open fork.")

# ---------- ATOMIC WRITE ----------
tmp = ED + ".tmp0914"
with open(tmp, "w") as f:
    json.dump(d, f, ensure_ascii=False, indent=1)
os.replace(tmp, ED)
print("WROTE", ED)
