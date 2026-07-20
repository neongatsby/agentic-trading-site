#!/usr/bin/env python3
import json

P = "/sessions/confident-exciting-wozniak/mnt/movita-backend/agentic-trading-site/site/engine-data.json"
with open(P) as f:
    d = json.load(f)

TS = "2026-07-20T15:16:00-04:00"

# ---- pulse prepend ----
d["pulse"].insert(0, {
    "ts": TS,
    "text": ("3:16pm: DID IT - the rotation the whole week's grades have begged for is EXECUTING, not just journaled. "
        "Adam tapped the BE cut at 2:57pm and it FILLED (sold 3 sh @ $203.03, ~-$59 realized), so LIVE is now 100% clean cash ($810) instead of 100% stuck in the worst name on the board. "
        "Immediately staged the redeploy: a live approve-now ticket (2026-07-20-2) to BUY 5 sh PLTR (~$680) - the confirmed 1x RS leader, +2.6% at a fresh 2-week high while the chip pop fully round-tripped (SOXL +10%->+1.8%, AMD +5.6%->+2.5%) AND software cracks (ORCL/NOW/ADBE -4%). "
        "One tap and LIVE finally OWNS the pop we called pop_rank 1, with a wide $122 GTC stop below the base. Paper unchanged - already holds PLTR (100 sh) + the SQQQ hedge that pays if QQQ loses its $698 low into the close. "
        "QQQ $697 on its day low, still under the 20-day, gate SHUT. 4/4 paper stops GTC, live flat/clean, zero naked. Multi-day swing = 0 day-trade budget burned (0/3)."),
    "hype": "Big one: you tapped the Bloom cut and it filled, so live is finally OUT of the dead name - and I've already teed up the Palantir buy. One tap and we own the leader I've been calling all week. Everything else held, hedge still on."
})

# ---- feed prepend (newest first): BE filled, PLTR pending, activity ----
feed_new = [
    {
        "ts": TS, "type": "trade", "side": "sell", "symbol": "BE",
        "status": "filled", "reaction": "rotate", "detail": "3 sh live @ $203.03",
        "text": ("Live BE cut FILLED - you tapped it at 2:57pm and the fast-lane sold all 3 shares @ $203.03, cancelling the $188 stop first. "
            "Live's out of the accidental all-in (~-$59 realized on the $222.64 top-tick entry) and sitting on clean cash to rotate into the leader. The week-long BE camp is finally closed.")
    },
    {
        "ts": TS, "type": "trade", "side": "buy", "symbol": "PLTR",
        "status": "pending", "reaction": "rotate", "detail": "5 sh live ~$680 - staged for your tap",
        "text": ("Live PLTR buy is teed up - one tap puts the freed BE cash into the RS leader (+2.6%, fresh 2-wk high, our pop_rank 1) behind a wide $122 GTC stop. "
            "This is the capture fix: LIVE finally owning the pop we called instead of the laggard. Multi-day swing, burns 0 day-trade budget.")
    },
    {
        "ts": TS, "type": "activity",
        "text": ("3:16pm: The BE->PLTR rotation is executing - BE cut filled @ $203.03, live PLTR buy staged (5 sh, $122 stop). "
            "QQQ $697 on its day low under the 20-day, chips fully round-tripped, PLTR the lone RS leader we're rotating into. Paper held (owns PLTR + the SQQQ hedge). 4/4 paper stops GTC, zero naked. Day-trade 0/3.")
    },
]
d["feed"] = feed_new + d["feed"]

# ---- accountability (running, final:false) ----
a = d["accountability"]
a["date"] = "2026-07-20"
a["final"] = False
a["grade"] = "C (running)"
a["headline"] = ("The week-long capture fix is finally EXECUTING, not just staged: Adam tapped the BE cut and it FILLED (sold 3 sh @ $203.03), so live is OUT of the worst name on the board, "
    "and I've fired a live ticket to rotate the freed $810 into pop_rank-1 PLTR (+2.6%, the RS leader bucking both the chip round-trip and the software selloff). One tap and LIVE finally owns the leader. "
    "Day's realized capture is still low (live ate BE's -4.2% before the cut), but the DECISION quality is now right - and the structural fix (live IN the leader, not a dead camp) is in motion.")
a["capture"] = {
    "bestName": "INTC / PLTR",
    "bestPct": "+2.7% / +2.6%",
    "capturedPct": "live -4.2% / paper -0.9%",
    "rate": ("paper OWNS pop_rank-1 PLTR +2.6% - within a hair of the best ownable-1x mover (INTC +2.7%), so paper's SELECTION captured the leader - but the flat NVDA (90 sh) + the SQQQ hedge dragged paper to -0.9%; "
        "live sat 100% in BE (-5.4%) until the 2:57pm cut, so its realized day capture is negative. The best raw mover SOXL round-tripped +10%->+1.8% (gated 3x, correctly skipped). The fix - live INTO PLTR - is now firing.")
}
a["missed"] = [
    {
        "from": "BE (broken camp)",
        "to": "PLTR",
        "note": "Live sat 100% in BE (-5.4%) most of the day while PLTR +2.6% ran - the week-long capture failure. NOW RESOLVING: BE cut FILLED @ $203.03, live PLTR buy staged and tap-gated - live finally rotating into the leader.",
        "delta": "rotation executing"
    },
    {
        "from": "n/a",
        "to": "SOXL +1.8% / INTC +2.7%",
        "note": "biggest raw movers round-tripped (SOXL +10%->+1.8% gated 3x, gate dodged the chase again; INTC +6%->+2.7% faded late-day) - PLTR the cleaner ownable-1x we own+rotate",
        "delta": "low-capture cost, accepted"
    }
]
a["saved"] = [
    {"note": "EXECUTED the rotation, not just journaled it - BE cut filled on the tap AND the PLTR redeploy staged the same run; live finally moving from the worst name into the leader", "delta": "the structural capture fix, in motion"},
    {"note": "Cut BE on a VERIFIED fresh catalyst (TD Cowen data-center-delay note) into the $203 bounce, not the $195 low - de-risked the accidental all-in on real news vs stop-hope into binary 7/28 earnings", "delta": "clean exit on a broken thesis"},
    {"note": "Doubled the CONFIRMED 1x RS leader (PLTR 50->100) in paper - the one name bucking both the chip fade and the ORCL/NOW/ADBE software selloff", "delta": "capture on what's actually working"},
    {"note": "Did NOT chase the +10%->+1.8% SOXL round-trip or the faded INTC/AMD HOD, and did NOT short $698 support that held all day - the known late-day traps", "delta": "avoided the round-trip + the whipsaw"},
    {"note": "4/4 paper stops verified GTC (PLTR $125 / NVDA $186 / SQQQ $38 / CEG $236), live flat/clean, zero naked either book", "delta": "never-naked held"}
]
a["best"] = {
    "name": "PLTR (paper 100 sh + live buy staged)",
    "note": "+2.6% holding a fresh 2-wk high, the cleanest RS leader bucking BOTH the chip fade and the software selloff - our pop_rank 1, doubled in paper and now the live rotation target",
    "delta": "the RS anchor, sized up + going live"
}
a["worst"] = {
    "name": "BE (cut/filled)",
    "note": "-5.4% to fresh 90-day lows + the TD Cowen data-center-delay note; the accidental top-tick all-in that dragged live all week - now closed for ~-$59 realized",
    "delta": "-$59 realized, camp closed"
}
a["applying"] = ("Charter v5 ACTIVE-ROTATION + the regime gate: cut the broken live camp on a VERIFIED catalyst (BE/TD Cowen, sold into the $203 bounce), "
    "and the instant it freed cash FIRE it into the confirmed 1x RS leader (live PLTR ticket) rather than camping cash or chasing a faded 3x - the exact fix the ~0%-capture week demanded.")
a["adjust"] = ("Next run: confirm the PLTR buy FILLED (reconcile queue/trade-placed + live positions), verify its $122 GTC stop attached (never-naked #1 priority), and set the honest post-close capture grade. "
    "If PLTR fills, LIVE finally owns the leader and the multi-week ~0% capture streak's structural fix is booked. Stay hair-trigger on QQQ $698 (loses it -> the SQQQ hedge pays, consider a small live SQQQ) and $716 (reclaims -> add the gated 3x names back).")

# ---- latest_recap + updated ----
d["latest_recap"] = ("3:16pm ET - THE ROTATION EXECUTED. Adam tapped the BE cut at 2:57pm and it FILLED (sold 3 sh @ $203.03, ~-$59, multi-day so PDT-free); "
    "live is now 100% clean cash ($810.32), OUT of the week-long BE camp. Immediately staged live ticket 2026-07-20-2 = BUY 5 sh PLTR (~$680, marketable limit $137, $122 GTC stop) - "
    "approve = buy the confirmed pop_rank-1 RS leader now (+2.6%, fresh 2-wk high, bucking the fully round-tripped chip pop SOXL +10%->+1.8% AND the ORCL/NOW/ADBE software selloff). "
    "Reconciled both books clean: LIVE flat/cash, no naked, no open orders; PAPER = broker (CEG 16 / NVDA 90 / PLTR 100 / SQQQ 310), all 4 GTC-stopped, zero naked, ~45% cash. "
    "QQQ $697 on its day low, ~2.6% under its $716 20-day (gate SHUT), SPY $742 near record highs = chip-specific. Held paper (owns PLTR + the SQQQ hedge that pays on a $698 break). "
    "Grade C running (final:false) - day capture low (live ate BE -4.2%) but the decision quality is finally right: live rotating from the worst name into the leader. "
    "Score alpha -11.6 vs TQQQ -7.4% since 7/2 ($73.35->$67.91). Day-trade 0/3. Published engine-data.json only; backup engine-data.backup-2026-07-20-1516.json.")
d["updated"] = TS

with open(P, "w") as f:
    json.dump(d, f, indent=2, ensure_ascii=False)
print("phase2 written; pulse len", len(d["pulse"]), "feed len", len(d["feed"]))
