#!/usr/bin/env python3
"""Per-run publish for the 2026-07-21 ~1:42pm ET heartbeat (HOLD/monitor tick).
Unique filename + atomic write (temp -> os.replace) + read-back verify, per OPS-ALERT rules."""
import json, os, sys, tempfile

SITE = os.path.dirname(os.path.abspath(__file__))
PATH = os.path.join(SITE, "engine-data.json")
TS = "2026-07-21T13:42:00-04:00"
STAMP = "1:42p"

with open(PATH) as f:
    d = json.load(f)

# ---- 1. updated ----
d["updated"] = TS

# ---- 2. pulse (prepend one, keep 15) ----
pulse_new = {
    "ts": TS,
    "text": ("1:42p — holding the freshly-rotated book (AMD/SMR/OKLO/VRT/CEG + the NVDA core, all 6 "
             "GTC-stopped) as the memory/semi rally confirms a 2nd day: MU +12% on a BofA $1,550 target, "
             "AMD +8%, INTC +8% on a Google-Cloud AI deal. No new trades this tick — we're already in "
             "the right theme, just entered mid-day so we only caught the tail. QQQ $709.6 is still ~0.7% "
             "under its ~$715 20-day, so the ~$16k paper 3x-powder stays armed for a CONFIRMED reclaim "
             "(front-running that line is what cost us all last week). LIVE: NVDA swing ticket still armed "
             "~$207, 6th day in cash pending Adam's tap."),
    "hype": ("Chips ripped a 2nd day and we're finally holding the right names — just sitting tight now. "
             "Keeping the leverage powder dry till the Nasdaq clears its line, because jumping early is "
             "exactly what burned us last week."),
}
d["pulse"] = [pulse_new] + d["pulse"]
d["pulse"] = d["pulse"][:15]

# ---- 3. feed (prepend one activity, keep 40) ----
feed_new = {
    "type": "activity",
    "ts": TS,
    "text": ("1:42pm run: HOLD/monitor — no new trades (already rotated 4x today into the leaders). "
             "Book in the right theme: semis + nuclear/AI-power all green, PAPER 6/6 GTC-stopped, zero naked. "
             "Not chasing anything extended up here; the ~$16k 3x powder waits for QQQ to clear its ~$715 "
             "20-day. LIVE flat $810 a 6th session (NVDA ticket armed/untapped). Both books == broker."),
}
d["feed"] = [feed_new] + d["feed"]
d["feed"] = d["feed"][:40]

# ---- 4. coverage: chg_pct + projection + updated (+ hold_reason for held) ----
cov = {
 "AMD": {"chg": 8.0, "proj": {"target_pct": 8.5, "confidence": "med", "basis": "2nd-day semi rally broadening (memory+AI-capex); owned leader", "pop_rank": 1, "path_pct": [8.0, 8.3, 8.5]},
         "hold": "Our clean owned chip leader — we're in it because the whole semi complex turned back up (memory-price upgrades lifting MU/INTC/AMD) and AMD is the highest-quality name in it. Entry avg ~$528, now ~$544 (+3% for us). We keep the $490 stop wide on purpose so a wobble doesn't shake us; we'd sell if it loses $490 or the chip bid clearly rolls over."},
 "NVDA": {"chg": 1.7, "proj": {"target_pct": 3.0, "confidence": "med", "basis": "megacap catch-up as chip bid broadens; least-extended leader", "pop_rank": 2, "path_pct": [1.7, 2.4, 3.0]},
          "hold": "The megacap AI leader and our largest position — the core chip bet and also the live swing candidate. It LAGGED today (+1.7% vs AMD/MU +8-12%), which is the setup: cheapest, least-extended leader with catch-up room and no earnings binary until late August. Entry avg ~$208, now ~$207 (flat). Stop $186 wide below the late-June base; we'd trim if it can't catch up while the group runs."},
 "SMR": {"chg": 8.7, "proj": {"target_pct": 9.0, "confidence": "med", "basis": "nuclear/AI-power bid; high-beta continuation", "pop_rank": 3},
         "hold": "Small-modular-nuclear name we own for the AI-power theme — data centers need power and this is a high-beta way to play it. Added to 700 sh this morning as it broke higher (+8.7% today), entry ~$8.63, now ~$8.66. Stop $7.50 wide under the base; we'd sell if the nuclear/power bid fades or it loses $7.50."},
 "OKLO": {"chg": 5.6, "proj": {"target_pct": 6.0, "confidence": "med", "basis": "nuclear momentum on the AI-power bid", "pop_rank": 6},
          "hold": "Nuclear/AI-power name started this morning as it reclaimed its base with the power bid (+5.6% today). Entry ~$43.92, now ~$43.86 (flat so far — entered mid-move). Stop $39 under the reclaim; we'd cut it if the AI-power theme rolls or $39 breaks."},
 "VRT": {"chg": 4.7, "proj": {"target_pct": 5.0, "confidence": "med", "basis": "data-center power capex proxy", "pop_rank": 8},
         "hold": "Vertiv — data-center power & cooling, a direct picks-and-shovels play on AI capex. Added to 30 sh this morning (+4.7% today), entry ~$304.78, now ~$305.5. Stop $282 wide; we'd sell if data-center spend fears return or it loses $282."},
 "CEG": {"chg": 3.8, "proj": {"target_pct": 4.0, "confidence": "med", "basis": "AI-power utility bid; steadier", "pop_rank": 10},
         "hold": "Constellation — nuclear utility powering AI data centers, our steadiest AI-power hold. Held from ~$260.68, now ~$263 (+3.8% today). Stop $236 wide below structure; we'd sell if the power-demand bid unwinds or $236 breaks."},
 "MU": {"chg": 12.2, "proj": {"target_pct": 12.5, "confidence": "med", "basis": "BofA $1,550 + MS memory-price upgrades; supercycle", "pop_rank": 4}},
 "SOXL": {"chg": 16.7, "proj": {"target_pct": 17.0, "confidence": "low", "basis": "3x semis rip but GATED under the QQQ 20-day", "pop_rank": 5}},
 "INTC": {"chg": 8.2, "proj": {"target_pct": 8.0, "confidence": "low", "basis": "Google-Cloud AI deal + Xeon upgrade; 7/23 earnings binary", "pop_rank": 7}},
 "RKLB": {"chg": 5.4, "proj": {"target_pct": 5.5, "confidence": "low", "basis": "space high-beta on a risk-on tape", "pop_rank": 9}},
 "RGTI": {"chg": 7.6, "proj": {"target_pct": 7.5, "confidence": "low", "basis": "quantum high-beta risk-on", "pop_rank": 11}},
 "TQQQ": {"chg": 5.9, "proj": {"target_pct": 6.0, "confidence": "low", "basis": "3x Nasdaq but GATED under the 20-day", "pop_rank": 12}},
 "IONQ": {"chg": 4.2, "proj": {"target_pct": 4.0, "confidence": "low", "basis": "quantum sympathy move", "pop_rank": 13}},
 "TSLA": {"chg": 2.8, "proj": {"target_pct": 2.5, "confidence": "low", "basis": "drifting into 7/22 earnings binary — no edge", "pop_rank": 14}},
 "SQQQ": {"chg": -5.8, "proj": {"target_pct": -6.0, "confidence": "med", "basis": "inverse — bleeds as the tape rallies (correctly exited)", "pop_rank": 15}},
}
ranks_seen = []
for c in d["coverage"]:
    t = c["ticker"]
    if t in cov:
        c["chg_pct"] = cov[t]["chg"]
        c["projection"] = cov[t]["proj"]
        c["updated"] = STAMP
        if "hold" in cov[t]:
            c["hold_reason"] = cov[t]["hold"]
        ranks_seen.append(cov[t]["proj"]["pop_rank"])

# ---- 5. headlines ----
d["headlines"] = [
    "Nasdaq +1.3%, S&P +0.9%, Dow +0.8% — semis lead a 2nd straight up day",
    "Micron +12% — BofA reits Buy, $1,550 target: 'open-source AI models guzzle memory'",
    "AMD +8%, Intel +8% (Google-Cloud AI deal + Xeon memory upgrade), Marvell & Arm +4-7%",
    "Nuclear/AI-power bid broad: SMR +9%, RGTI +8%, OKLO +6%, VRT +5%",
    "Earnings on deck: TSLA & GOOGL Wed 7/22, INTC Thu 7/23 — binaries ahead",
    "QQQ $709.6 — still ~0.7% under its ~$715 20-day; the 3x leverage gate stays SHUT",
    "SPY $748.7 near a record; risk-on rotation back into AI infrastructure",
]

# ---- 6. status ----
d["status"] = [
    {"session": "Morning", "text": "Cut SQQQ + PLTR drags"},
    {"session": "Afternoon", "text": "Holding leaders; gate still shut"},
]

# ---- 7. paper block ----
d["paper"]["equity"] = 89844.86
d["paper"]["updated"] = TS
for pt in d["paper"]["equity_curve"]:
    if pt["date"] == "Jul 21":
        pt["value"] = 89844.86
d["paper"]["equity_note"] = ("Paper ~$89.8k (+0.25% vs Mon) — AMD +8.0% / SMR +8.7% / OKLO +5.6% / VRT +4.7% / "
    "CEG +3.8% offset by the flat NVDA core (+1.7%, 32% of book) and the realized PLTR rotation (−$334). "
    "6/6 GTC-stopped, zero naked (AMD 30/$490, NVDA 140/$186, SMR 700/$7.50, OKLO 200/$39, VRT 30/$282, CEG 16/$236). "
    "~$16.4k cash = gated 3x powder for a confirmed QQQ ~$715 reclaim.")

# ---- 8. live block ----
d["live"]["updated"] = TS
d["live"]["equity_note"] = ("LIVE flat $810.32 cash / zero positions / zero naked; 1 pending ticket = BUY NVDA 3 sh "
    "(~$207, $186 stop, swing/0 day-trades). 6th straight session in cash — armed since 8:17a, pending Adam's tap. "
    "−19.0% since $1,000 inception.")

# ---- 9. latest_recap (archive prior, set fresh) ----
d["_latest_recap_1320"] = d.get("latest_recap")
d["latest_recap"] = ("1:42p 7/21 — HOLD/monitor tick (no new trades; already rotated 4x today into the leaders). "
    "Book: paper 6 names AMD/CEG/NVDA/OKLO/SMR/VRT, all GTC-stopped, ~$89.8k (+0.25% vs Mon), ~$16.4k cash = 3x powder "
    "ARMED for a QQQ ~$715 reclaim. Theme confirmed day 2: MU +12% (BofA $1,550 memory target), AMD +8%, INTC +8% "
    "(Google-Cloud AI deal), SOXL +17% gated. Regime: QQQ $709.6 (+2.0%), still ~0.7% under its ~$715 20-day — gate "
    "stays SHUT, no 3x yet (front-running it caused last week's drawdown). SPY $748.7 near record. LIVE flat $810 a 6th "
    "session — NVDA ticket 2026-07-21-1 armed/untapped (3 sh, $186 stop). Both books == broker, zero naked. "
    "Grade C- running — right theme, late entries, low capture.")

# ---- 10. accountability (running, final:false) ----
a = d["accountability"]
a["date"] = "2026-07-21"
a["final"] = False
a["grade"] = "C- (running, intraday)"
a["headline"] = ("Right theme, late entry: the book is finally in the day's leaders (semis + nuclear/AI-power, all 6 "
    "GTC-stopped) but we bought them mid-day, so we caught only the tail — paper ~+0.25% while the watchlist rips "
    "+8-17%, and the flat NVDA core (32% of book) drags. LIVE is a 6th day in cash on an armed-but-untapped NVDA ticket. "
    "Real discipline held: gated the 3x (SOXL +17% / TQQQ +6%) our own rule keeps us out of under the 20-day, didn't chase "
    "parabolic MU/BE, cut the SQQQ + PLTR drags. Final grade at the close.")
a["capture"] = {
    "bestName": "SOXL +16.7% (3x, gated) / BE +15.9% & MU +12.2% (ownable, unowned) / SMR +8.7% & AMD +8.0% (held)",
    "bestPct": "+16.7% / +12–16% / +8.7%",
    "capturedPct": "paper ~+0.25%, live 0%",
    "rate": "low — ~2–3% of the day's best mover; the held names were entered mid-day (tail only) and the flat NVDA core (32%) drags",
}
a["missed"] = [
    {"from": "the flat PLTR laggard", "to": "nuclear/AI-power leg (OKLO/SMR/VRT)",
     "note": "held PLTR flat-to-red a full week while the AI-infra theme accelerated; rotated it out this run — right move, ~a week late",
     "delta": "−$334 realized, redeployed"},
    {"from": "the open", "to": "mid-day entries",
     "note": "AMD/SMR/VRT/OKLO added mid-day, so we captured only the tail of +5-13% moves instead of the whole run",
     "delta": "tail capture only"},
    {"from": "live cash", "to": "NVDA (armed, untapped)",
     "note": "6th straight session 100% live cash; ticket armed since 8:17a but only helps on Adam's tap",
     "delta": "opportunity, pending tap"},
]
a["saved"] = [
    {"note": "Gated SOXL +16.7% and TQQQ +5.9% (3x under the 20-day) — the exact fade-risk the gate exists for after last week's gap-through losses; owned the move via 1x AMD/SMR instead", "delta": "discipline intact"},
    {"note": "Didn't chase parabolic MU +12% / BE +16% at the highs, and skipped INTC +8% into its 7/23 earnings binary", "delta": "process"},
    {"note": "Cut the SQQQ inverse and the week-long PLTR drag and concentrated into the leading nuclear/AI-power theme — real active rotation, not camping", "delta": "capture lever pulled"},
]
a["best"] = {"name": "AMD", "note": "owned chip leader +8.0%; wide $490 stop rides it through the memory-led 2nd-day rally", "delta": "+$480 open"}
a["worst"] = {"name": "PLTR", "note": "the flat/red software laggard we finally cut — dead money for a week while the tape ran", "delta": "−$334 realized"}
a["applying"] = "PLAYBOOK — rotate, don't camp: sell a laggard to fund the best available setup (opportunity cost IS a sell signal). Cut PLTR/SQQQ into the leading nuclear/AI-power + semi legs."
a["adjust"] = "Enter movers EARLIER — at the open when the theme is confirming, not mid-day after +5-8%. Fire the ~$16k 3x powder into SOXL/TQQQ the same session ONLY on a confirmed QQQ ~$715 reclaim (not before). LIVE: the NVDA swing must get tapped to end the 6-day cash streak."

# ---- 11. score: refresh alphaPts off fresh prices (live -19.0% vs TQQQ -2.4%) ----
d["score"]["alphaPts"] = "-16.6"
d["score"]["benchmark"] = "-2.4%"

# ---- ATOMIC WRITE ----
fd, tmp = tempfile.mkstemp(dir=SITE, prefix=".engine-data.tmp-", suffix=".json")
try:
    with os.fdopen(fd, "w") as f:
        json.dump(d, f, ensure_ascii=False, indent=1)
    os.replace(tmp, PATH)
finally:
    if os.path.exists(tmp):
        os.remove(tmp)

# ---- READ-BACK VERIFY ----
with open(PATH) as f:
    v = json.load(f)
ranks = sorted(c["projection"]["pop_rank"] for c in v["coverage"])
ones = [c["ticker"] for c in v["coverage"] if c["projection"]["pop_rank"] == 1]
assert v["updated"] == TS, f"updated mismatch: {v['updated']}"
assert v["accountability"]["final"] is False, "final should be False intraday"
assert v["accountability"]["grade"].startswith("C-"), f"grade: {v['accountability']['grade']}"
assert any(t["id"] == "2026-07-21-1" and t["symbol"] == "NVDA" for t in v["pending_tickets"]), "NVDA ticket missing"
assert ones == ["AMD"], f"exactly one pop_rank1 expected=AMD, got {ones}"
assert len(v["pulse"]) == 15 and v["pulse"][0]["ts"] == TS, "pulse head/len wrong"
assert len(v["coverage"]) == 15, "coverage len wrong"
print("VERIFY OK")
print("updated:", v["updated"])
print("grade:", v["accountability"]["grade"], "| final:", v["accountability"]["final"])
print("pop_rank1:", ones, "| all ranks:", ranks)
print("pending:", [(t["id"], t["symbol"], t["side"], t.get("qty")) for t in v["pending_tickets"]])
print("paper eq:", v["paper"]["equity"], "| live eq:", v["live"]["equity"])
print("pulse len:", len(v["pulse"]), "| feed len:", len(v["feed"]))
print("score:", v["score"]["alphaPts"], v["score"]["benchmark"])
