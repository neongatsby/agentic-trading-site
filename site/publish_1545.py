#!/usr/bin/env python3
# Engine-data publish for the ~3:45pm ET 2026-07-21 run.
# Surgical field updates + backup + atomic write (temp->os.replace) + read-back asserts.
import json, os, shutil

SITE = os.path.dirname(os.path.abspath(__file__))
F = os.path.join(SITE, "engine-data.json")
BACKUP = os.path.join(SITE, "engine-data.backup-2026-07-21-1545.json")
TS = "2026-07-21T15:45:00-04:00"

# 1) backup the current good state first
shutil.copy2(F, BACKUP)
d = json.load(open(F))

# 2) pulse (prepend one; keep ~15)
pulse_new = {
 "ts": TS,
 "text": "3:45p — Re-staged the live NVDA swing to fire at TOMORROW's open (approve anytime -> fills at the 7/22 open; ~$207 entry, $186 stop, multi-day/PDT-free) rather than let it expire untapped at 4pm — the 7/20 fix: commit at the open, don't ride a ticket all day. No new paper trade: the book already owns the day's leaders (AMD +7.6%, SMR +7.9%, OKLO +5.3%, VRT +4.1%, CEG +3.2%) and all 6 are GTC-stopped/verified, zero naked — but I'll grade it straight, mid-day entries mean paper's ~flat (+0.05%) while the theme ran +8-15%, and live sat cash a 6th day. QQQ closed ~$709, still ~0.8% under its $714.7 20-day, so the ~$16.4k 3x powder stays parked — I lever on a confirmed reclaim, ideally after Wed's GOOGL/TSLA prints, not into them. Grade D (running): right theme at last, but ~0-2% capture on a target-rich day isn't a save.",
 "hype": "Moved the NVDA buy to fire at tomorrow's open instead of letting it die tonight. Right names and all stopped, but we got in late again — only a sliver of a big day, so it's an honest D."
}
d["pulse"] = [pulse_new] + d.get("pulse", [])[:14]

# 3) status cards
d["status"] = [
 {"session": "Morning", "text": "Cut SQQQ + PLTR drags"},
 {"session": "Afternoon", "text": "Leaders held; NVDA staged for open"}
]

# 4) headlines
d["headlines"] = [
 "Nasdaq-100 +1.5% to 29,022; S&P +0.9% to a record ~7,508 — semis lead a broad risk-on rip",
 "Micron +12% — BofA reiterates Buy, $1,550 target; Taiwan/Korea export data confirms the chip recovery",
 "SOXL +15.3%, INTC +8.6% (Google-Cloud AI deal), AMD +7.6% into its 'Advancing AI 2026' event (7/22)",
 "Nuclear/AI-power bid broadens: SMR +7.9%, RGTI +6.3%, OKLO +5.3%, RKLB +4.9%, VRT +4.1%, CEG +3.2%",
 "NVDA +1.9% — the complex's laggard (9.3% Nebius stake); no earnings binary till late Aug = our live swing",
 "BE +15% V-reversal to ~$227 (we sold 7/20 on the verified delay catalyst — a watchlist miss)",
 "Binaries Wed 7/22: GOOGL + TSLA report after the close; QQQ $709 still ~0.8% under its $714.7 20-day",
 "3x still gated: SOXL/TQQQ ran but QQQ hasn't reclaimed its 20-day — powder waits for the confirmed break"
]

# 5) coverage — refresh chg_pct + projection + updated by ticker (preserve prose)
upd = {
 "NVDA": {"chg_pct": "+1.9%", "verdict_label": "Hold + live buy (staged for open)",
   "thesis": "**The group's biggest laggard, +1.9% while MU/INTC/AMD ran +8-12% — the catch-up name, not a broken one.** Micron's HBM blowout reads straight through to NVDA GPUs; least-extended AI leader, no earnings binary until late Aug (GOOGL/TSLA print Wed, NVDA doesn't). $186 stop under the late-June base. Also the live swing — re-staged to fire at tomorrow's open.",
   "hold_reason": "This is our core AI position and today's laggard — up ~1.9% while memory names ran +8-12%. We hold 140 sh from ~$208 (about flat) and it just took a 9.3% stake in neocloud Nebius; Micron's HBM-demand blowout reads straight through to NVDA GPUs, so we read it as the catch-up name. It's also the live swing we're trying to own — re-staged to fill at tomorrow's open. The $186 stop is our line if the whole AI trade rolls over.",
   "projection": {"target_pct": 2.5, "confidence": "med", "basis": "laggard catch-up; no binary till Aug + HBM read-through", "pop_rank": 1, "path_pct": [1.9, 2.2, 2.5]}},
 "AMD": {"chg_pct": "+7.6%",
   "projection": {"target_pct": 2.0, "confidence": "med", "basis": "'Advancing AI' event 7/22, but +7.6% extended", "pop_rank": 2, "path_pct": [7.6, 8.5, 9.5]}},
 "MU": {"chg_pct": "+12.0%",
   "projection": {"target_pct": 1.5, "confidence": "low", "basis": "memory supercycle leader; very extended", "pop_rank": 3}},
 "SMR": {"chg_pct": "+7.9%",
   "projection": {"target_pct": 1.5, "confidence": "low", "basis": "nuclear RS leader; extended +7.9%", "pop_rank": 4}},
 "RGTI": {"chg_pct": "+6.3%",
   "projection": {"target_pct": 2.0, "confidence": "low", "basis": "quantum high-beta; tracks the risk-on tape", "pop_rank": 5}},
 "OKLO": {"chg_pct": "+5.3%",
   "projection": {"target_pct": 1.5, "confidence": "low", "basis": "nuclear/AI-power; near our entry", "pop_rank": 6}},
 "RKLB": {"chg_pct": "+4.9%",
   "projection": {"target_pct": 2.0, "confidence": "low", "basis": "space/defense beta; rode the risk-on day", "pop_rank": 7}},
 "VRT": {"chg_pct": "+4.1%",
   "projection": {"target_pct": 1.5, "confidence": "low", "basis": "AI-power infra; near our entry", "pop_rank": 8}},
 "BE": {"chg_pct": "+15.0%",
   "projection": {"target_pct": 0.0, "confidence": "low", "basis": "spent parabolic; we're OUT, not chasing", "pop_rank": 9}},
 "IONQ": {"chg_pct": "+2.9%",
   "projection": {"target_pct": 1.5, "confidence": "low", "basis": "quantum beta; follows the tape", "pop_rank": 10}},
 "CEG": {"chg_pct": "+3.2%",
   "projection": {"target_pct": 1.0, "confidence": "low", "basis": "nuclear utility; steadier lower-beta", "pop_rank": 11}},
 "SOXL": {"chg_pct": "+15.3%",
   "projection": {"target_pct": 2.0, "confidence": "low", "basis": "3x semis on a hot tape - GATED (QQQ<20d)", "pop_rank": 12}},
 "TSLA": {"chg_pct": "+2.2%",
   "projection": {"target_pct": 1.0, "confidence": "low", "basis": "reports Wed - binary; avoid into the print", "pop_rank": 13}},
 "TQQQ": {"chg_pct": "+5.7%",
   "projection": {"target_pct": 1.5, "confidence": "low", "basis": "3x Nasdaq - GATED until QQQ reclaims 20d", "pop_rank": 14}},
}
for c in d["coverage"]:
    u = upd.get(c.get("ticker"))
    if u:
        c.update(u)
        c["updated"] = "3:45p"

# 6) feed — prepend one activity item; keep ~40
feed_new = {
 "type": "activity", "ts": TS,
 "text": "3:45pm — Into the close: re-staged the LIVE NVDA swing to fire at TOMORROW's OPEN (approve anytime -> fills 7/22 open, ~$207, $186 stop, 0 day-trades) so it stops dying untapped at 4pm — the 7/20 execution-timing fix. No new paper trade: 6/6 GTC-stopped in the day's leaders (AMD +7.6%, SMR +7.9%, OKLO +5.3%), zero naked, but honest capture ~0-2% on a +8-15% tape -> grade D (running). QQQ $709 still under its $714.7 20-day -> ~$16.4k 3x powder parked for a confirmed reclaim past Wed's GOOGL/TSLA prints."
}
d["feed"] = [feed_new] + d.get("feed", [])[:39]

# 7) activity headline list — prepend; keep ~21
act_new = {
 "ts": TS, "kind": "engine",
 "title": "Tue 7/21 ~3:45pm ET (RTH, ~15m to close). Re-staged live NVDA swing for TOMORROW's open (7/20 fix) — no new paper trade. Paper 6/6 GTC-stopped in the day's leaders; live cash 6th day. Honest capture ~0-2% on a +8-15% tape -> D running. 3x gated: QQQ $709.2 vs $714.7 20-day."
}
d["activity"] = [act_new] + d.get("activity", [])[:20]

# 8) score (alpha real from TQQQ 7/2 $73.35 -> $71.46 = -2.6%; live -19.0% since $1,000)
d["score"] = {
 "alphaPts": "-16.4", "benchmark": "-2.6%", "bestDay": "+3.2%",
 "bestDayName": "Jul 14 — CPI chip rally (settled)", "winRate": "33%", "tradeCount": 6
}

# 9) accountability (running; finalizes on the post-close run)
d["accountability"] = {
 "date": "2026-07-21", "final": False, "grade": "D (running, intraday)",
 "headline": "A +8-15% risk-on rip and we captured ~0-2%: paper finally owns the RIGHT theme (AMD/SMR/OKLO/VRT/CEG, all GTC-stopped, zero naked) but mid-day entries left it ~flat (+0.05%), and live is a 6th straight session 100% cash on an armed NVDA swing — now re-staged to fire at tomorrow's open. Honest: the 3x gate (SOXL +15.3%, TQQQ +5.7%) COST upside today — still the right rule over the sample, not a 'save.' Real credit: cut the SQQQ/PLTR drags into the rip, didn't chase MU +12% / BE +15% at the highs, verified AMD's binary is Aug 4 so we hold it through tomorrow's event. Finalizes at the close.",
 "capture": {
   "bestName": "BE +15.0% (sold 7/20, unowned) & MU +12.0% (memory, unowned); SOXL +15.3% ran but was correctly gated (3x)",
   "bestPct": "+15.0% / +12.0%",
   "capturedPct": "paper +0.05%, live 0%",
   "rate": "~0-2% — owned the right theme but mid-day entries = tail; live flat in cash"
 },
 "missed": [
   {"from": "BE (sold 7/20 @ $203 on the verified delay catalyst)", "to": "holding BE",
    "note": "BE V-reversed +15% to ~$227 today — the cut was on a real catalyst but price ran hard against it; the day's biggest ownable miss", "delta": "~+$71 vs held (3 sh live)"},
   {"from": "the open", "to": "mid-day leader entries",
    "note": "AMD/SMR/OKLO/VRT/CEG added mid-day — captured the tail of +4-8% moves, not the whole run", "delta": "tail only"},
   {"from": "live cash", "to": "NVDA (armed, untapped a 6th day)",
    "note": "live sat 100% cash all day; NVDA swing armed since 8:17a — now re-staged for tomorrow's open so it can't expire untapped again", "delta": "pending tap"}
 ],
 "saved": [
   {"note": "Cut the SQQQ hedge into the rally — it fell ~5.7% today as QQQ ripped; holding it would've bled", "delta": "avoided hedge drag"},
   {"note": "Cut the flat/red PLTR laggard (-1.5% today, the lone red watchlist name) and redeployed toward the leaders", "delta": "redeployed"},
   {"note": "Didn't chase parabolic MU +12% / BE +15% at the highs — the top-tick mistake the Playbook names", "delta": "avoided chase"},
   {"note": "Zero naked — all 6 paper positions GTC-stopped, verified at the broker this run", "delta": "risk bounded"},
   {"note": "Re-staged NVDA to fill at the OPEN instead of riding an untapped ticket to a 4pm death — the 7/20 execution-timing fix", "delta": "process fix applied"}
 ],
 "avoided": {
   "worstName": "SQQQ / PLTR", "worstPct": "-5.7% / -1.5%",
   "note": "the two drags we cut this morning; on a broad-green day there was little else to dodge", "amount": "small", "rate": "n/a on risk-on"
 },
 "best": {"name": "AMD (paper)", "note": "the one leader we owned into a real move — +7.6% today, Advancing AI event tomorrow", "delta": "+$426 unrealized"},
 "worst": {"name": "live cash (structural, 6th day)", "note": "a +8-15% target-rich day captured 0% live; the fix (fire at the open) is now staged, not just narrated", "delta": "0% of the day"},
 "applying": "Applying the 7/20 lesson: the capture gap is EXECUTION-TIMING, not regime — commit at the OPEN. Today's theme selection was finally right; the entries (and the untapped live ticket) were a beat late, so I re-staged NVDA to fire at tomorrow's open.",
 "adjust": "Tomorrow: let the NVDA swing fill at the OPEN (don't wait), and take any paper leader add on the FIRST confirmation, not mid-day. Lever the ~$16.4k 3x powder only once QQQ closes above its $714.7 20-day — ideally after Wed's GOOGL/TSLA prints, not into them."
}

# 10) pending_tickets (NVDA re-staged for the open)
d["pending_tickets"] = [{
 "id": "2026-07-21-1", "symbol": "NVDA", "side": "buy", "size": "$633", "qty": 3,
 "entry": "~$207 — approve anytime -> fills at TOMORROW's (7/22) open (multi-day swing, PDT-free, 0/3 day-trades). Marketable-limit $211 gives gap-up cushion; fills immediately if tapped before today's 4pm close.",
 "trigger": None, "stop": 186,
 "bracket": "stop $186 GTC (below the late-June $192 base, -10.2%)",
 "thesis": "Ends a 6th day of live cash by owning the leading AI-infra/semis theme via the NON-extended leader. NVDA +1.9% today LAGGED the +8-12% AMD/MU/INTC complex = a cheaper entry in the group leader; it just took a 9.3% stake in neocloud Nebius and Micron's memory blowout reads straight through to NVDA HBM/GPU demand. No earnings binary until late Aug (AMD 8/4; GOOGL/TSLA print Wed — NVDA doesn't). Wide $186 stop. Re-staged to fire at the OPEN — the 7/20 execution-timing fix."
}]

# 11) live block
d["live"]["equity"] = 810.32
d["live"]["cash"] = 810.32
d["live"]["positions"] = []
d["live"]["updated"] = TS
d["live"]["equity_note"] = "LIVE flat $810.32 cash / zero positions / zero naked; 1 pending ticket = BUY NVDA 3 sh (~$207, $186 stop, swing / 0 day-trades) RE-STAGED to fill at tomorrow's (7/22) OPEN. 6th straight session in cash — the tap is the lever; staging at the open is the 7/20 execution-timing fix."
for pt in d["live"].get("equity_curve", []):
    if pt.get("date") == "Jul 21":
        pt["value"] = 810.32

# 12) paper block (fresh broker equity $89,661.93; correct Mon to settled $89,617.78)
d["paper"]["equity"] = 89661.93
d["paper"]["updated"] = TS
d["paper"]["equity_note"] = "Paper ~$89.66k (+0.05% vs Mon settled $89,617, provisional intraday) — owns the day's leaders (AMD +7.6% / SMR +7.9% / OKLO +5.3% / VRT +4.1% / CEG +3.2% / NVDA +1.9%) but ~flat reflects mid-day entries (tail only) + the realized SQQQ de-hedge & PLTR cut. All 6 GTC-stopped, verified; ~$16.4k dry = 3x powder for a confirmed QQQ $714.7 reclaim."
for pt in d["paper"].get("equity_curve", []):
    if pt.get("date") == "Jul 20":
        pt["value"] = 89617.78
    if pt.get("date") == "Jul 21":
        pt["value"] = 89661.93

# 13) latest_recap + updated
d["latest_recap"] = "3:45p 7/21 — Re-staged live NVDA swing to fire at TOMORROW's open (7/20 execution-timing fix), no new paper trade. Paper 6 names AMD/CEG/NVDA/OKLO/SMR/VRT all GTC-stopped, ~$89.66k, ~$16.4k = 3x powder for a confirmed QQQ $714.7 reclaim (prefer post-GOOGL/TSLA Wed). Tape: record S&P close, Nasdaq-100 +1.5%; MU +12% (BofA $1,550), SOXL +15.3%/TQQQ +5.7% ran but stayed GATED. LIVE: 6th day cash — the tap (now staged for the open) is the lever. Honest grade D (running): right book, late+light, ~0-2% capture."
d["updated"] = TS

# 14) atomic write
tmp = F + ".tmp"
with open(tmp, "w") as f:
    json.dump(d, f, ensure_ascii=False, indent=1)
os.replace(tmp, F)

# 15) read-back verification + asserts
r = json.load(open(F))
ranks = [c["projection"]["pop_rank"] for c in r["coverage"] if "projection" in c]
assert r["updated"] == TS, "updated mismatch"
assert r["accountability"]["final"] is False and r["accountability"]["grade"].startswith("D"), "accountability mismatch"
assert r["pending_tickets"][0]["symbol"] == "NVDA", "pending mismatch"
assert ranks.count(1) == 1, f"pop_rank not unique: {sorted(ranks)}"
assert len(r["coverage"]) == 14, "coverage count changed"
assert r["pulse"][0]["ts"] == TS, "pulse not prepended"
print("PUBLISH OK")
print("updated:", r["updated"])
print("grade:", r["accountability"]["grade"], "| final:", r["accountability"]["final"])
print("pop_rank=1:", [c["ticker"] for c in r["coverage"] if c.get("projection",{}).get("pop_rank")==1])
print("ranks sorted:", sorted(ranks))
print("pending:", r["pending_tickets"][0]["symbol"], r["pending_tickets"][0]["size"], "expires-at-open")
print("pulse[0]:", r["pulse"][0]["text"][:70], "...")
print("coverage chg:", {c["ticker"]: c["chg_pct"] for c in r["coverage"]})
print("live:", r["live"]["equity"], "| paper:", r["paper"]["equity"])
print("backup:", os.path.basename(BACKUP), os.path.getsize(BACKUP), "bytes")
