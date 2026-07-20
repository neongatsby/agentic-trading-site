#!/usr/bin/env python3
import json, shutil, datetime, sys

P = "/sessions/confident-exciting-wozniak/mnt/movita-backend/agentic-trading-site/site/engine-data.json"
shutil.copy(P, P.replace("engine-data.json", "engine-data.backup-2026-07-20-1516.json"))

with open(P) as f:
    d = json.load(f)

TS = "2026-07-20T15:16:00-04:00"

# ---- fresh chg_pct by ticker (pulled this run) ----
chg = {
    "PLTR": 2.6, "AMD": 2.5, "INTC": 2.7, "NVDA": 0.0, "VRT": 1.0,
    "SOXL": 1.8, "TQQQ": 0.6, "CEG": 0.6, "FNGU": 2.0, "IONQ": -0.6,
    "RKLB": -2.9, "SQQQ": -1.1, "TSLA": -2.8, "BE": -5.4, "SOXS": -2.0,
}
# ---- fresh projections by ticker: (target_pct, confidence, basis, pop_rank, path) ----
proj = {
    "PLTR": (2.9, "high", "RS leader 2-wk high; bucking chip+software fade; live rotation in", 1, [2.6, 2.8, 2.9]),
    "AMD":  (2.4, "med", "Advancing AI PT raises but faded from +5.6%", 2, [2.5, 2.4, 2.4]),
    "INTC": (2.6, "med", "chip rebound faded from +6%", 3, [2.7, 2.6, 2.6]),
    "SOXL": (1.5, "med", "3x semis GATED; round-tripped +10%->+1.8%", 4, [1.8, 1.6, 1.5]),
    "VRT":  (0.9, "med", "data-center power bid; earnings 7/29 ahead", 5, [1.0, 0.9, 0.9]),
    "FNGU": (1.7, "low", "3x mega-cap GATED", 6, [2.0, 1.8, 1.7]),
    "NVDA": (0.2, "med", "flat, basing at 20-day support", 7, [0.0, 0.1, 0.2]),
    "CEG":  (0.8, "med", "low-beta power, green on a fady tape", 8, [0.6, 0.7, 0.8]),
    "TQQQ": (0.4, "med", "3x QQQ GATED under the 20-day", 9, [0.6, 0.5, 0.4]),
    "IONQ": (-0.3, "low", "quantum, no catalyst", 10, [-0.6, -0.4, -0.3]),
    "SQQQ": (-1.3, "med", "inverse hedge; QQQ pinned on its $698 low", 11, [-1.1, -1.2, -1.3]),
    "RKLB": (-2.7, "med", "pulling back from highs with the tape", 12, [-2.9, -2.8, -2.7]),
    "TSLA": (-2.7, "med", "weak into Wed earnings, lost $380", 13, [-2.8, -2.7, -2.7]),
    "BE":   (-5.2, "high", "CUT/filled - broken chart + TD Cowen delay note", 14, [-5.4, -5.3, -5.2]),
    "SOXS": (-1.8, "med", "inverse; chips net green today", 15, [-2.0, -1.9, -1.8]),
}

for c in d["coverage"]:
    t = c["ticker"]
    if t in chg:
        c["chg_pct"] = chg[t]
    if t in proj:
        tp, cf, bs, pr, pa = proj[t]
        c["projection"] = {"target_pct": tp, "confidence": cf, "basis": bs, "pop_rank": pr, "path_pct": pa}
    c["updated"] = TS

# ---- PLTR entry: live rotation now firing ----
for c in d["coverage"]:
    if c["ticker"] == "PLTR":
        c["verdict"] = "buy"; c["verdict_label"] = "Buy"
        c["thesis"] = ("**THE confirmed relative-strength leader - the one name working, and now the LIVE rotation target.** "
            "PLTR is +2.6% holding a fresh 2-week high while the morning chip pop fully round-tripped (SOXL +10%->+1.8%, AMD +5.6%->+2.5%, NVDA back to flat) AND enterprise software cracks (ORCL -4.4%, NOW -4.2%, ADBE -4%). "
            "Textbook RS: green at its highs while every neighbor fades. Catalyst-backed - FY26 rev guide RAISED to $7.66B, net-dollar-retention 150%, remaining deal value $11.8B, the July Nvidia sovereign-AI partnership + Army NGC2 Foundry win, 8 straight beats. "
            "1x stock (no gate issue), so we own it aggressively: doubled paper to 100 sh AND, now that the BE cut freed $810 live cash, a live approve-now ticket (2026-07-20-2, 5 sh, $122 stop) is staged to finally put LIVE in the leader.")
        c["hold_reason"] = ("PLTR is the account's RS anchor - the cleanest thing bucking a weak tape - so we doubled the paper position (100 sh, $125 GTC stop) and, the instant BE freed live cash, staged the live buy (5 sh, $122 stop). "
            "We hold while it makes higher lows and holds the $130-136 base; a clean break of $136.9 opens the gap toward $142. We'd trim if it loses ~$130 or the AI-software bid rolls over.")
        c["size"] = "$13.6k paper (100 sh) + live buy staged (5 sh)"
        c["size_pct"] = "~15% paper"
        c["size_note"] = "doubled in paper; LIVE rotation firing now (BE cut freed $810)"
        c["plan_usd"] = "live ~$680 into PLTR - ticket 2026-07-20-2, approve = buy now"
        c["horizon"] = "swing"
    if c["ticker"] == "BE":
        c["verdict"] = "avoid"; c["verdict_label"] = "Cut (filled)"
        c["thesis"] = ("**CUT - the week-long live camp is closed.** Adam tapped the sell at 2:57pm and it FILLED (3 sh @ $203.03, ~-$59 realized on the $222.64 top-tick entry). "
            "The exit was on a broken chart AND a fresh, verified fundamental crack: TD Cowen (Osborne, Hold, $235 PT) flagged meaningful delays at BE's two largest data-center projects (Oracle Project Jupiter's air permit + FERC-stuck pipeline; AEP Cheyenne slipped 2yrs) - hitting the exact growth story that was the only reason to hold into 7/28. "
            "BE -5.4% to fresh 90-day lows while FuelCell rallied. Freed $810 is rotating into PLTR.")
        c["hold_reason"] = ""
        c["size"] = "-"; c["size_pct"] = "-"
        c["size_note"] = "CUT/filled @ $203.03 - freed $810 -> PLTR"
        c["plan_usd"] = "done - proceeds rotating to PLTR"
        c["horizon"] = "exit"

# ---- status ----
d["status"] = [
    {"session": "Morning", "text": "QQQ held $698, bounced; gate ON"},
    {"session": "Afternoon", "text": "BE cut FILLED; live rotating into PLTR"},
]

# ---- headlines refresh ----
d["headlines"] = [
    "QQQ $697 sitting ON its day low, ~2.6% under its 20-day ($716); SPY flat at record highs - the derate stays chip/tech-specific, leverage gate SHUT",
    "Morning chip pop FULLY round-tripped into the close: SOXL +10%->+1.8%, AMD +5.6%->+2.5%, INTC +6%->+2.7% - the same 'fade under the 20-day' pattern as ASML/TSMC last week",
    "Bloom Energy CUT: live sold BE @ $203 after TD Cowen flagged meaningful delays at its two largest data-center projects (Oracle Jupiter permit + AEP Cheyenne -2yrs); BE -5.4% to fresh 90-day lows",
    "PLTR the clean RS leader: +2.6% holding a fresh 2-week high while chips round-trip and software (ORCL -4.4%, NOW -4.2%, ADBE -4%) cracks - the live redeploy target",
    "Enterprise software cracks: Oracle -4.4%, ServiceNow -4.2%, Adobe -4% - the derate spreads from chips to software, PLTR the lone green AI-software name",
    "Heavy earnings week: GOOGL, TSLA, INTC, TXN Wed-Thu; BE 7/28, VRT 7/29 - TSLA -2.8% into its print",
    "Nuclear/SMR names bid on the AI-power theme; CEG steady (+0.6%) as tech fades",
    "Fed Board of Governors held a closed meeting 3:30pm ET; Iran conflict simmers with fresh US airstrikes, oil wavering ~$81",
]

# ---- pending_tickets: swap BE cut -> PLTR buy ----
d["pending_tickets"] = [{
    "id": "2026-07-20-2",
    "symbol": "PLTR",
    "side": "buy",
    "size": "$680",
    "qty": 5,
    "entry": "~$135.8 marketable buy (approve = buy PLTR now)",
    "trigger": None,
    "stop": 122,
    "bracket": "stop $122 GTC (below the $129-131 two-week base, -10%)",
    "thesis": "The funded BE->PLTR rotation. BE is cut (freed $810); fire it into the confirmed 1x RS leader. PLTR +2.6% at a fresh 2-week high while the chip pop round-tripped (SOXL +10%->+1.8%) and software cracks (ORCL/NOW/ADBE -4%). FY26 guide raised to $7.66B, NDR 150%, Nvidia sovereign-AI partnership. 1x = no gate issue. This finally gets LIVE OUT of the dead camp and INTO the pop we called pop_rank 1. 5 sh keeps a BP buffer so the marketable-limit reserve can't reject; multi-day swing, burns 0 PDT budget (0/3)."
}]

# ---- score ----
d["score"] = {
    "alphaPts": "-11.6",
    "benchmark": "-7.4%",
    "bestDay": "+3.2%",
    "bestDayName": "Day 9 - CPI chip rally (settled)",
    "winRate": "33%",
    "tradeCount": 6,
}

print("phase1 ok:", len(d["coverage"]), "coverage;", "pending", d["pending_tickets"][0]["id"])
with open(P, "w") as f:
    json.dump(d, f, indent=2, ensure_ascii=False)
print("written")
