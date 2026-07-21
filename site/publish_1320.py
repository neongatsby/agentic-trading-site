#!/usr/bin/env python3
# Per-run publish for the 2026-07-21 13:20 ET heartbeat.
# Unique filename (never /tmp/update_engine.py). Atomic write + backup + verified read-back.
import json, os, tempfile, datetime

SITE = "/sessions/funny-determined-fermi/mnt/movita-backend/agentic-trading-site/site"
EDATA = os.path.join(SITE, "engine-data.json")
JOURNAL = "/sessions/funny-determined-fermi/mnt/Agentic Trading/journal/2026-07-21.md"
TS = "2026-07-21T13:20:00-04:00"

with open(EDATA) as f:
    d = json.load(f)

# ---- backup the pre-write good state ----
bak = os.path.join(SITE, "engine-data.backup-2026-07-21-1320.json")
with open(bak, "w") as f:
    json.dump(d, f, indent=1)

# ---- pulse (prepend one, keep ~15) ----
pulse_new = {
    "ts": TS,
    "text": ("1:20p — finally attacked the capture drag instead of narrating it: SOLD the flat/red PLTR laggard "
             "(100 @ $132.41, −$334) and rotated the cash INTO today's leading leg, the nuclear/AI-power complex. "
             "Started OKLO 200 (+5.8%) and added to SMR (now 700, +8.7%) and VRT (now 30, +4.7%). All six positions GTC-stopped, "
             "zero naked. 3x gate stays SHUT — QQQ $709 is ~0.9% under its $716 20-day — so no SOXL/TQQQ yet; ~$16.4k powder "
             "waits for that reclaim. LIVE: NVDA swing ticket still armed, 6th day in cash pending Adam's tap."),
    "hype": ("Dumped the dead-weight PLTR and moved the money into what's actually running today — nuclear/AI-power "
             "(OKLO, more SMR, more VRT). Everything's stop-protected. Keeping some cash dry until the Nasdaq clears its line before I touch the 3x.")
}
d["pulse"] = [pulse_new] + d.get("pulse", [])
d["pulse"] = d["pulse"][:15]

# ---- coverage (full refresh, 15 names, both directions, one pop_rank==1) ----
d["coverage"] = [
 {"ticker":"AMD","name":"Advanced Micro Devices","theme":"AI chips","verdict":"hold","verdict_label":"Hold — owned leader",
  "thesis":"**Owned chip leader, +7.4% into Wednesday's 'Advancing AI' launch.** Reclaimed $541 from the $495 base as semis rip a 2nd day (MU +13%, INTC +8%). Wide $490 stop rides it through the event.",
  "hold_reason":"It's our clean owned semi leader — we're in it because the whole chip complex turned back up and AMD has a dated catalyst Wednesday (its Advancing-AI product launch). Entry avg ~$528, now ~$541. We keep the $490 stop wide on purpose so an event-day wobble doesn't shake us; we'd sell if it loses $490 or the launch disappoints.",
  "size":"$16.2k paper (30 sh)","size_pct":"18%","size_note":"core","plan_usd":"—","chg_pct":7.4,
  "projection":{"target_pct":9.0,"confidence":"high","basis":"chip 2nd-day momentum + Wed Advancing-AI event","pop_rank":1,"path_pct":[7.4,8.2,9.0]},
  "updated":"1:20p","horizon":"swing (through Wed event)"},
 {"ticker":"SMR","name":"NuScale Power","theme":"nuclear / AI power","verdict":"buy","verdict_label":"Buy — added",
  "thesis":"**Nuclear RS leader, +8.7%; added to 700 sh this run.** Small-modular-reactors are the cleanest AI-power derivative and SMR reclaimed $8.67 off the $7.6 base on heavy volume. $7.50 GTC stop below the base.",
  "hold_reason":"It's the relative-strength leader of the small-modular-reactor group, the freshest leg of the AI-power trade. We added today (now 700 sh, avg ~$8.63) because it broke back above its base with the nuclear bid. Watching the $8 area to hold; a break of $7.50 is our out.",
  "size":"$6.1k paper (700 sh)","size_pct":"7%","size_note":"added +400 today","plan_usd":"—","chg_pct":8.7,
  "projection":{"target_pct":10.0,"confidence":"med","basis":"nuclear RS leader, base reclaim on volume","pop_rank":2,"path_pct":[8.7,9.4,10.0]},
  "updated":"1:20p","horizon":"swing"},
 {"ticker":"NVDA","name":"NVIDIA","theme":"AI chips","verdict":"hold","verdict_label":"Hold — value leader",
  "thesis":"**Least-extended large-cap AI leader, +1.4% and coiling at $206 support.** Lagged the +8-13% AMD/INTC/MU pop = a cheaper entry in the group leader. Nebius-stake catalyst, cheapest multiple in a decade, no earnings binary until late Aug. $186 stop.",
  "hold_reason":"We hold the big core here (140 sh, avg ~$208) as the value/catch-up play in AI chips — cheaper and less-extended than the names that already ran, with a fresh Nebius-stake catalyst and no earnings landmine this week. It's been the laggard two days, which is the risk; we're watching for the catch-up move and would trim if it loses the $203 support.",
  "size":"$28.9k paper (140 sh) + live ticket 3 sh","size_pct":"32%","size_note":"core (capture drag)","plan_usd":"$620 live","chg_pct":1.4,
  "projection":{"target_pct":2.5,"confidence":"med","basis":"coiling at support, catch-up to chip group","pop_rank":3,"path_pct":[1.4,2.0,2.5]},
  "updated":"1:20p","horizon":"swing / live"},
 {"ticker":"OKLO","name":"Oklo Inc","theme":"nuclear / AI power","verdict":"buy","verdict_label":"Buy — new",
  "thesis":"**New nuclear momentum position, +5.8% off the $41 base.** Started 200 sh this run to widen capture on the AI-power leg alongside SMR. Reclaimed $44 with volume; $39 GTC stop below the base.",
  "hold_reason":"Fresh position (200 sh, avg ~$43.92) — started this run to add exposure to the nuclear/AI-power theme leading today. It bounced cleanly off the $41 support that held all last week. Watching $44-45 to clear; a loss of $39 is the stop.",
  "size":"$8.8k paper (200 sh)","size_pct":"10%","size_note":"new this run","plan_usd":"—","chg_pct":5.8,
  "projection":{"target_pct":7.0,"confidence":"med","basis":"nuclear bid, base reclaim","pop_rank":4,"path_pct":[5.8,6.5,7.0]},
  "updated":"1:20p","horizon":"swing"},
 {"ticker":"VRT","name":"Vertiv Holdings","theme":"data-center power/cooling","verdict":"buy","verdict_label":"Buy — added",
  "thesis":"**Data-center power/cooling leader, +4.7%; added to 30 sh.** The picks-and-shovels play on AI data-center buildout, reclaiming $305 from the $289 base with room to the $318-330 highs. $282 stop.",
  "hold_reason":"We hold and added to Vertiv (now 30 sh, avg ~$305) because it's the core data-center power/cooling infrastructure name and it's turning back up off its base — less extended than the chips. Watching for a push toward the early-July $318-330 highs; a break of $282 is the exit.",
  "size":"$9.2k paper (30 sh)","size_pct":"10%","size_note":"added +12 today","plan_usd":"—","chg_pct":4.7,
  "projection":{"target_pct":6.0,"confidence":"med","basis":"data-center capex leader, base reclaim","pop_rank":5,"path_pct":[4.7,5.4,6.0]},
  "updated":"1:20p","horizon":"swing"},
 {"ticker":"RGTI","name":"Rigetti Computing","theme":"quantum","verdict":"watch","verdict_label":"Watch",
  "thesis":"**Quantum momentum, +7.4% riding the risk-on tape.** High-beta mover but no fresh company catalyst — a watch, not a chase, next to the AI names we already own.",
  "size":"—","size_pct":"—","size_note":"—","plan_usd":"$2.5k IF it clears $15.5 on volume","chg_pct":7.4,
  "projection":{"target_pct":7.5,"confidence":"low","basis":"high-beta risk-on, no own catalyst","pop_rank":6},
  "updated":"1:20p","horizon":"—"},
 {"ticker":"INTC","name":"Intel","theme":"AI chips","verdict":"watch","verdict_label":"Watch — earnings 7/23",
  "thesis":"**+8.4% with the chip bid, but earnings Thursday 7/23 = binary.** We don't buy into an own-earnings landmine; watching how it trades post-print for a cleaner entry.",
  "size":"—","size_pct":"—","size_note":"—","plan_usd":"—","chg_pct":8.4,
  "projection":{"target_pct":8.0,"confidence":"med","basis":"chip momentum but 7/23 earnings binary","pop_rank":7},
  "updated":"1:20p","horizon":"post-earnings"},
 {"ticker":"RKLB","name":"Rocket Lab","theme":"space / defense","verdict":"watch","verdict_label":"Watch",
  "thesis":"**Space/defense RS name, +5.6%, reclaimed $69.** Strong relative strength but off-theme from today's AI-infra leadership; on the bench as a rotation candidate.",
  "size":"—","size_pct":"—","size_note":"—","plan_usd":"$3k IF it holds $69 into the close","chg_pct":5.6,
  "projection":{"target_pct":6.0,"confidence":"low","basis":"RS reclaim, off-theme today","pop_rank":8},
  "updated":"1:20p","horizon":"—"},
 {"ticker":"MU","name":"Micron Technology","theme":"memory / AI chips","verdict":"watch","verdict_label":"Watch — extended",
  "thesis":"**Today's headline mover, +12.9% on Morgan Stanley's 25% memory-price call.** The catalyst that lit the whole semi tape — but chasing a +13% parabolic post-call move is late; watching for a pullback.",
  "size":"—","size_pct":"—","size_note":"—","plan_usd":"—","chg_pct":12.9,
  "projection":{"target_pct":12.0,"confidence":"low","basis":"MS memory upgrade, but extended +13%","pop_rank":9},
  "updated":"1:20p","horizon":"—"},
 {"ticker":"IONQ","name":"IonQ","theme":"quantum","verdict":"watch","verdict_label":"Watch",
  "thesis":"**Quantum, +3.8% with the risk-on tape.** Lagging its peer RGTI today; no fresh catalyst — a watch.",
  "size":"—","size_pct":"—","size_note":"—","plan_usd":"—","chg_pct":3.8,
  "projection":{"target_pct":4.0,"confidence":"low","basis":"risk-on beta, lagging RGTI","pop_rank":10},
  "updated":"1:20p","horizon":"—"},
 {"ticker":"CEG","name":"Constellation Energy","theme":"nuclear power","verdict":"hold","verdict_label":"Hold — anchor",
  "thesis":"**Owned nuclear-power utility, +3.4%.** The lower-beta anchor of our AI-power basket, grinding higher with the theme. $236 stop.",
  "hold_reason":"We hold Constellation (16 sh, avg ~$261) as the steadier, lower-beta way to own the nuclear/AI-power theme next to SMR and OKLO. It's grinding up with the group. Fine holding into the theme; a break of $236 would be the exit.",
  "size":"$4.2k paper (16 sh)","size_pct":"5%","size_note":"anchor","plan_usd":"—","chg_pct":3.4,
  "projection":{"target_pct":4.0,"confidence":"med","basis":"nuclear-power anchor, steady bid","pop_rank":11},
  "updated":"1:20p","horizon":"swing"},
 {"ticker":"SOXL","name":"Semis 3x Bull","theme":"leveraged semis","verdict":"avoid","verdict_label":"Avoid — gated (3x)",
  "thesis":"**+16.9% — the day's biggest watchlist mover, and correctly gated.** 3x semis under QQQ's 20-day is exactly the fade-risk the gate exists for; we own the move via 1x AMD/SMR instead. Arms IF QQQ reclaims $716.",
  "size":"—","size_pct":"—","size_note":"—","plan_usd":"$4k IF QQQ>$716 on volume","chg_pct":16.9,
  "projection":{"target_pct":15.0,"confidence":"med","basis":"3x semis, gated until QQQ>716","pop_rank":12},
  "updated":"1:20p","horizon":"gated"},
 {"ticker":"TQQQ","name":"Nasdaq 3x Bull","theme":"leveraged index","verdict":"avoid","verdict_label":"Avoid — gated (3x)",
  "thesis":"**+5.8% but still gated — QQQ $709 is ~0.9% under its $716 20-day.** The powder (~$16k) is ready to fire the instant QQQ reclaims the line on volume.",
  "size":"—","size_pct":"—","size_note":"—","plan_usd":"$5k IF QQQ>$716 on volume","chg_pct":5.8,
  "projection":{"target_pct":6.0,"confidence":"med","basis":"3x index, gated until QQQ>716","pop_rank":13},
  "updated":"1:20p","horizon":"gated"},
 {"ticker":"TSLA","name":"Tesla","theme":"mega-cap / EV","verdict":"avoid","verdict_label":"Avoid — earnings 7/22",
  "thesis":"**+2.8% into Wednesday's earnings = binary.** Not taking an own-earnings gamble; standing aside.",
  "size":"—","size_pct":"—","size_note":"—","plan_usd":"—","chg_pct":2.8,
  "projection":{"target_pct":3.0,"confidence":"low","basis":"7/22 earnings binary","pop_rank":14},
  "updated":"1:20p","horizon":"post-earnings"},
 {"ticker":"SQQQ","name":"Nasdaq 3x Bear","theme":"inverse","verdict":"avoid","verdict_label":"Avoid — inverse",
  "thesis":"**−5.9% on a risk-on 2nd day; we cut ours earlier and are right to stay out.** No place for an inverse while the tape rips.",
  "size":"—","size_pct":"—","size_note":"—","plan_usd":"—","chg_pct":-5.9,
  "projection":{"target_pct":-6.0,"confidence":"med","basis":"inverse into a risk-on tape","pop_rank":15},
  "updated":"1:20p","horizon":"—"},
]

# ---- status (session cards, Morning -> Afternoon) ----
d["status"] = [
 {"session":"Morning","text":"Cut SQQQ, bought SMR/VRT"},
 {"session":"Afternoon","text":"Rotated PLTR into nuclear leg"},
]

# ---- headlines ----
d["headlines"] = [
 "Nasdaq +1.3%, S&P +0.7% — semis lead a 2nd straight up day",
 "Micron +13% after Morgan Stanley sees memory prices +25% on AI demand",
 "Intel +8%, Marvell +7%, Astera +6% — chip complex broad-based",
 "Nuclear/AI-power bid: SMR +9%, RGTI +7%, OKLO +6%",
 "88% of S&P 500 reporters have beaten EPS so far this season",
 "Earnings on deck: TSLA & GOOGL Wed, INTC Thu — binaries ahead",
 "QQQ $709 — still ~0.9% under its 20-day; the 3x leverage gate stays shut",
]

# ---- feed (prepend 4 trade items, keep 40) ----
feed_new = [
 {"type":"trade","side":"sell","symbol":"PLTR","status":"filled","detail":"100 @ $132.41","reaction":"rotate","ts":TS,
  "text":"Sold PLTR — flat-to-red for a week while the AI-infra theme ripped. Took the small loss (−$334) to free the cash for something actually moving."},
 {"type":"trade","side":"buy","symbol":"OKLO","status":"filled","detail":"200 @ $43.92","reaction":"rotate","ts":TS,
  "text":"Started OKLO — nuclear name breaking back above its base with the AI-power bid. $39 stop under it."},
 {"type":"trade","side":"buy","symbol":"SMR","status":"filled","detail":"+400 @ ~$8.65 (now 700)","reaction":"rotate","ts":TS,
  "text":"Doubled up on SMR — the relative-strength leader of the nuclear group, +9% today. Now 700 shares, $7.50 stop."},
 {"type":"trade","side":"buy","symbol":"VRT","status":"filled","detail":"+12 @ ~$305 (now 30)","reaction":"rotate","ts":TS,
  "text":"Added Vertiv — the data-center power/cooling play, less extended than the chips. Now 30 shares, $282 stop."},
]
d["feed"] = feed_new + d.get("feed", [])
d["feed"] = d["feed"][:40]

# ---- score (real: alpha = live return - TQQQ benchmark since 7/2) ----
# live -18.97% ; TQQQ 7/2 $73.35 -> $71.57 = -2.4% ; alpha = -16.5
d["score"] = {"alphaPts":"-16.5","benchmark":"-2.4%","bestDay":"+3.2%",
              "bestDayName":"Jul 14 — CPI chip rally (settled)","winRate":"33%","tradeCount":6}

# ---- accountability (running, HONEST, C-) ----
d["accountability"] = {
 "date":"2026-07-21","final":False,"grade":"C- (running, intraday)",
 "headline":("Finally attacked the capture drag instead of narrating it: cut the flat/red PLTR laggard and rotated into the day's "
             "leading nuclear/AI-power leg (started OKLO, added SMR to 700 + VRT to 30). But the grade stays C- because we bought the "
             "movers LATE — the book is still ~flat (+0.1%) while the watchlist rips +8-17%, and NVDA at +1.4% is still 32% of it. "
             "Live is a 6th day in cash on an untapped ticket. Discipline held where it counts: gated SOXL +17% and skipped INTC +8% "
             "into its 7/23 print. Final grade at the close."),
 "capture":{"bestName":"SOXL +16.9% (3x, gated) / MU +12.9% & BE +15.4% (ownable) / SMR +8.7% (held)",
            "bestPct":"+16.9% / +12.9% / +8.7%","capturedPct":"paper ~+0.1%, live 0%",
            "rate":"low — book ~flat vs +8-17% movers; we own AMD/SMR/OKLO/VRT but entered mid-day so captured only the tail, and the flat NVDA core drags"},
 "missed":[
   {"from":"the flat PLTR laggard","to":"nuclear/AI-power leg (OKLO/SMR/VRT)",
    "note":"held PLTR flat-to-red a full week while the AI-infra theme accelerated; rotated it out THIS run — right move, ~a week late","delta":"−$334 realized, redeployed"},
   {"from":"watched MU/RGTI at the open","to":"owned the movers late",
    "note":"the AMD/SMR/VRT/OKLO adds captured only the tail of +5-13% moves because we entered mid-day, not at the open","delta":"tail capture only"},
   {"from":"live cash","to":"NVDA (staged, untapped)",
    "note":"6th straight session 100% live cash; ticket armed since 8:17a but only helps on Adam's tap","delta":"opportunity, pending tap"}
 ],
 "saved":[
   {"note":"Gated SOXL +16.9% and TQQQ +5.8% (3x under the 20-day) — the exact fade-risk the gate exists for; owned the move via 1x AMD/SMR instead","delta":"discipline intact"},
   {"note":"Skipped INTC +8.4% into Thursday's 7/23 earnings binary and didn't chase MU +12.9% / BE +15.4% parabolic","delta":"process"},
   {"note":"Cut the PLTR (and earlier SQQQ) drags and concentrated into the leading nuclear/AI-power theme — real active rotation, not camping","delta":"capture lever pulled"}
 ],
 "best":{"name":"AMD","note":"owned chip leader, +7.4% into Wed's Advancing-AI event; wide $490 stop holds it through the catalyst","delta":"+$394 open"},
 "worst":{"name":"PLTR","note":"the flat/red software laggard we finally cut — dead money for a week while the tape ran","delta":"−$334 realized"},
 "applying":"PLAYBOOK — rotate, don't camp: sell a laggard to fund the best available setup (opportunity cost IS a sell signal). Cut PLTR into the leading nuclear/AI-power leg.",
 "adjust":"Enter movers EARLIER — at the open when the theme is confirming, not mid-day after +5-8%. If QQQ reclaims $716 on volume, fire the ~$16k powder into a 3x starter (SOXL/TQQQ) same session. LIVE: the NVDA swing must get tapped to end the 6-day cash streak."
}

# ---- paper block ----
d["paper"]["equity"] = 89695.51
d["paper"]["updated"] = TS
d["paper"]["equity_note"] = ("Paper ~$89.7k (+0.1% vs Mon) — AMD +7.4% / SMR +8.7% / OKLO +5.8% / VRT +4.7% / CEG +3.4% offset by flat "
    "NVDA +1.4% and the realized PLTR rotation (−$334). 6/6 GTC-stopped, zero naked (AMD 30/$490, NVDA 140/$186, SMR 700/$7.50, "
    "OKLO 200/$39, VRT 30/$282, CEG 16/$236). ~$16.4k cash = gated 3x powder for a QQQ $716 reclaim.")
if d["paper"].get("equity_curve") and d["paper"]["equity_curve"][-1].get("date") == "Jul 21":
    d["paper"]["equity_curve"][-1]["value"] = 89695.51

# ---- live block (values unchanged; refresh note/ts) ----
d["live"]["updated"] = TS
d["live"]["equity_note"] = ("LIVE flat $810.32 cash / zero positions / zero naked; 1 pending ticket = BUY NVDA 3 sh (~$206, $186 stop). "
    "6th straight session in cash — pending Adam's tap. −19.0% since $1,000 inception.")

# ---- pending_tickets (NVDA swing stays armed) ----
d["pending_tickets"] = [{
 "id":"2026-07-21-1","symbol":"NVDA","side":"buy","size":"$620","qty":3,
 "entry":"~$206 marketable — market open, approve = fills now","trigger":None,"stop":186,
 "bracket":"stop $186 GTC (below the late-June $192 base, −9.7%)",
 "thesis":("Funded live rotation OUT of a 6th day of cash and INTO the leading AI-infra/chip theme via the NON-extended leader. "
           "NVDA +1.4% (lagged the +8-13% AMD/INTC/MU = cheaper entry), fresh Nebius-stake catalyst, cheapest multiple in a decade, "
           "no earnings binary this week. Chip bid confirmed a 2nd day + QQQ nearing its ~$716 gate. Wide $186 stop. Approve -> fills at market now.")
}]

d["updated"] = TS

# ---- atomic write ----
dir_ = os.path.dirname(EDATA)
fd, tmp = tempfile.mkstemp(dir=dir_, suffix=".tmp")
with os.fdopen(fd, "w") as f:
    json.dump(d, f, ensure_ascii=False, indent=1)
os.replace(tmp, EDATA)

# ---- verified read-back ----
with open(EDATA) as f:
    v = json.load(f)
ranks = sorted(c["projection"]["pop_rank"] for c in v["coverage"])
top = [c["ticker"] for c in v["coverage"] if c["projection"]["pop_rank"] == 1]
assert v["updated"] == TS, "updated mismatch"
assert v["accountability"]["final"] is False and v["accountability"]["grade"].startswith("C-"), "accountability mismatch"
assert len(v["coverage"]) == 15 and ranks == list(range(1,16)), f"coverage ranks bad: {ranks}"
assert top == ["AMD"], f"pop_rank1 not unique AMD: {top}"
assert v["pending_tickets"][0]["id"] == "2026-07-21-1", "ticket missing"
assert abs(v["paper"]["equity"] - 89695.51) < 1, "paper equity bad"
assert len(v["pulse"]) == 15 and v["pulse"][0]["ts"] == TS, "pulse bad"
assert v["feed"][0]["symbol"] == "PLTR" and v["feed"][0]["status"] == "filled", "feed bad"
print("VERIFIED OK | updated", v["updated"], "| grade", v["accountability"]["grade"],
      "| pop1", top, "| ranks", ranks[0], "-", ranks[-1],
      "| paper", v["paper"]["equity"], "| pulse", len(v["pulse"]), "| feed", len(v["feed"]),
      "| headlines", len(v["headlines"]), "| coverage", len(v["coverage"]))

# ---- append journal entry ----
entry = """

### 1:20pm ET — Management + ROTATION run (market OPEN, regular hours)

**Regime (fresh pull):** QQQ $709.5 (+1.9%), 20-day computed = **$716.1** -> QQQ ~0.9% UNDER the gate, day 6 SHUT but on the cusp. SPY $748.7. Nasdaq +1.3% / S&P +0.7% — semis lead a 2nd straight up day (MU +12.9% on Morgan Stanley's +25% memory-price call, INTC +8.4%, MRVL/Astera +6-7%). Nuclear/AI-power the freshest leg: SMR +8.7%, RGTI +7.4%, OKLO +5.8%. Risk-ON.

**Reconciled (both books == broker, verified):** LIVE flat $810.32 cash, zero positions/orders; NVDA ticket 2026-07-21-1 staged/untapped (3 sh, $186 stop). PAPER equity $89,695.51, cash $16.4k. Fixed a data-vs-broker drift: the published note still listed SQQQ 50 + omitted SMR/VRT — real book was already AMD/CEG/NVDA/PLTR/SMR/VRT. Also caught SMR's stop covering only 294 of 300 sh (6 naked) — resolved by the add + full 700-sh re-stop.

**ACTED on the 12:50 flag ("PLTR = #1 rotation candidate") + the accountability adjust (rotate, don't camp):**
- SOLD PLTR 100 @ $132.41 (−$334 realized) — flat-to-red a full week while the AI-infra theme accelerated; opportunity-cost sell. Cancelled its $125 stop first.
- STARTED OKLO 200 @ $43.92 ($39 GTC stop) — nuclear momentum, clean $41-base reclaim.
- ADDED SMR +400 -> 700 @ ~$8.63 avg ($7.50 GTC stop) — the nuclear RS leader.
- ADDED VRT +12 -> 30 @ ~$304.78 avg ($282 GTC stop) — data-center power/cooling.
- Wash-trade rejects on the SMR/VRT adds (opposite-side stop existed) — handled by cancel-stop -> buy -> re-arm full-qty stop. Brief naked window, re-stopped within seconds.
- PAPER now 6 names, **6/6 GTC-stopped, zero naked**: AMD 30/$490, CEG 16/$236, NVDA 140/$186, OKLO 200/$39, SMR 700/$7.50, VRT 30/$282. ~82% deployed, ~$16.4k powder ARMED for a QQQ $716 reclaim -> 3x starter.
- Held the 3x gate SHUT (no SOXL +16.9% / TQQQ +5.8% chase — under the 20-day) and skipped INTC +8.4% into its 7/23 print.

**LIVE:** kept the NVDA swing ticket armed/current (non-extended, no-binary, $186 stop). Did NOT re-place (already pinged since 8:17a; no spam). 6th day of live cash is the run's weak spot — fills on Adam's tap. Day-trade budget 0/3 (all-swing).

**Grade C- (running, HONEST):** real rotation this run (cut the laggard, concentrated into the leading nuclear/AI-power leg) but book still ~+0.1% because the movers were bought LATE (tail capture) and NVDA is still 32% at +1.4%. Did NOT grade-inflate. pop_rank 1 = **AMD** (owned, +7.4%, Wed Advancing-AI event). Score: live −19.0%; TQQQ benchmark 7/2 $73.35 -> $71.57 = −2.4%; **alpha −16.5 pts**.

**Published** engine-data.json atomically (unique publish_1320.py, temp -> os.replace; backup engine-data.backup-2026-07-21-1320.json). Read-back **VERIFIED**: updated 13:20, ranks 1-15 unique w/ pop1=AMD, NVDA ticket present, accountability running C-/final:false, pulse 15, feed 40, coverage 15, paper $89,695.51 / live $810.32. Did NOT write site/data.json; no git.

**Next action:** watch the QQQ-vs-$716 fork — a reclaim on volume opens the gate -> deploy the ~$16.4k powder into a 3x starter (SOXL/TQQQ) + strongest 1x same session. Manage OKLO/SMR/VRT into the close; trail stops on higher lows. Reconcile the NVDA live tap if it fills. Watch into Wed's TSLA/GOOGL prints (7/22) + INTC (7/23).
"""
with open(JOURNAL, "a") as f:
    f.write(entry)
print("JOURNAL appended.")
