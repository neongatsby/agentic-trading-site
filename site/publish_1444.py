import json, os, shutil, datetime

SITE = os.path.dirname(os.path.abspath(__file__))
F = os.path.join(SITE, "engine-data.json")
TS = "2026-07-21T14:44:00-04:00"
SHORT = "2:44p"

d = json.load(open(F))

# ---- backup first ----
bak = os.path.join(SITE, "engine-data.backup-2026-07-21-1444.json")
shutil.copy(F, bak)

# ---- current day % moves (prevClose -> latest, real from snapshots this run) ----
chg = {"NVDA":"+1.7%","AMD":"+8.1%","SMR":"+8.5%","MU":"+12.3%","BE":"+14.9%","OKLO":"+5.4%",
       "RGTI":"+6.7%","VRT":"+4.3%","IONQ":"+3.6%","RKLB":"+4.6%","CEG":"+3.5%","TSLA":"+2.7%",
       "SOXL":"+16.5%","TQQQ":"+5.7%"}

# ---- refreshed projections (exactly one pop_rank:1 = NVDA, our ownable-live catch-up pick) ----
proj = {
 "NVDA": {"target_pct":2.5,"confidence":"med","basis":"ownable laggard; MU HBM read-through, catch-up bet","pop_rank":1,"path_pct":[1.7,2.1,2.5]},
 "AMD":  {"target_pct":8.0,"confidence":"med","basis":"chip leader; own AMD earnings tmrw AH = binary","pop_rank":2},
 "MU":   {"target_pct":12.0,"confidence":"med","basis":"memory super-cycle catalyst (Anthropic); extended","pop_rank":3},
 "SMR":  {"target_pct":8.5,"confidence":"med","basis":"nuclear/AI-power breakout, owned","pop_rank":4},
 "BE":   {"target_pct":14.0,"confidence":"low","basis":"V-reversal; we sold on the delay catalyst, not chasing","pop_rank":5},
 "SOXL": {"target_pct":16.0,"confidence":"med","basis":"3x semis ripping but GATED (QQQ<20-day)","pop_rank":6},
 "RGTI": {"target_pct":6.5,"confidence":"low","basis":"quantum beta on the risk-on lift","pop_rank":7},
 "OKLO": {"target_pct":5.4,"confidence":"med","basis":"nuclear/AI-power, owned","pop_rank":8},
 "TQQQ": {"target_pct":5.7,"confidence":"med","basis":"3x Nasdaq, gated until the reclaim","pop_rank":9},
 "RKLB": {"target_pct":4.6,"confidence":"low","basis":"space beta, risk-on tape","pop_rank":10},
 "VRT":  {"target_pct":4.3,"confidence":"med","basis":"AI-power/datacenter, owned","pop_rank":11},
 "IONQ": {"target_pct":3.6,"confidence":"low","basis":"quantum beta","pop_rank":12},
 "CEG":  {"target_pct":3.5,"confidence":"med","basis":"nuclear power, owned","pop_rank":13},
 "TSLA": {"target_pct":2.7,"confidence":"low","basis":"into Wed earnings; rangey","pop_rank":14},
}
for c in d.get("coverage", []):
    t = c.get("ticker")
    if t in chg: c["chg_pct"] = chg[t]
    if t in proj: c["projection"] = proj[t]
    c["updated"] = SHORT

# ---- pulse (prepend one) ----
pulse_text = ("2:44p — Monitor/refresh into the close; nothing changed enough to trade. The book's in the day's real "
 "leaders and all 6 GTC-stopped (AMD +8.1%, SMR +8.5%, OKLO +5.4%), but the honest capture is only ~1–2% — we bought "
 "them mid-day and live's still in cash, so this is a D+, not a save. I'm explicitly NOT crediting the gated 3x as a win: "
 "SOXL +16.5% / TQQQ +5.7% went UP today, so the gate cost us upside — it's still the right rule over the sample, but it "
 "didn't 'dodge' anything today. Gate's shut by a hair (QQQ $709.5 vs its $714.7 20-day); I'd rather it clear tomorrow's "
 "GOOGL/TSLA/AMD prints before I lever the ~$16k powder. The one lever left is Adam's tap on the armed NVDA swing — that "
 "ends the 6-day live-cash streak.")
pulse_hype = ("Right names, all stopped — but we got in late so only caught a sliver of a big day; that's a D+, not a win. "
 "Waiting on QQQ to clear its line before adding leverage, and that NVDA tap is what finally gets live out of cash.")
d.setdefault("pulse", []).insert(0, {"ts": TS, "text": pulse_text, "hype": pulse_hype})
d["pulse"] = d["pulse"][:15]

# ---- feed (prepend one activity) ----
feed_item = {"type":"activity","ts":TS,
 "text":("2:44pm refresh — HOLD/monitor, no new trade. Book in the leaders, 6/6 GTC-stopped, zero naked. Honest read: "
 "capture ~1–2% on a +12–16% day → grade D+ (running). Not chasing MU +12% / BE +15% at 2pm (top-tick risk). "
 "3x still gated (QQQ $709.5 < $714.7 20-day); ~$16k powder for a confirmed reclaim past Wed's GOOGL/TSLA prints. "
 "LIVE NVDA swing armed + untapped — 6th day in cash.")}
d.setdefault("feed", []).insert(0, feed_item)
d["feed"] = d["feed"][:40]

# ---- activity (top-of-page engine line) ----
d.setdefault("activity", []).insert(0, {"ts":TS,"kind":"engine",
 "title":("Tue 7/21 ~2:44pm ET (RTH). Monitor/refresh — no new trade. Paper 6/6 GTC-stopped in the day's leaders; "
 "live still cash w/ NVDA swing armed+untapped (6th day). Honest capture ~1–2% on a +12–16% tape → D+ running. "
 "3x gated: QQQ $709.5 vs $714.7 20-day.")})
d["activity"] = d["activity"][:40]

# ---- status ----
d["status"] = [
 {"session":"Morning","text":"Cut SQQQ + PLTR drags"},
 {"session":"Afternoon","text":"Leaders held; 3x powder dry"},
]

# ---- headlines (refreshed, real) ----
d["headlines"] = [
 "Nasdaq up a 2nd straight day — semis + memory lead; SPY $748 near a record",
 "Micron +12.3% — blowout: Anthropic memory deal, BofA reits Buy $1,550 ('AI models guzzle memory')",
 "Memory super-cycle broad: WDC/SanDisk/SK Hynix surge; DRAM complex rips",
 "AMD +8%, Intel +8% (Google-Cloud AI deal) — chips the market's leading sector",
 "Nuclear/AI-power bid: SMR +8.5%, RGTI +6.7%, OKLO +5.4%, VRT +4.3%",
 "Binaries on deck: AMD + GOOGL + TSLA report Wed 7/22; INTC Thu 7/23",
 "QQQ $709.5 — still ~0.7% under its $714.7 20-day; the 3x leverage gate stays shut",
 "BE +14.9% — V-reversal off yesterday's delay-catalyst flush (we're out, not chasing)",
]

# ---- accountability (running, honest) ----
d["accountability"] = {
 "date":"2026-07-21","final":False,"grade":"D+ (running, intraday)",
 "headline":("Right book, late and light — a target-rich +12–16% risk-on day and we captured ~1–2%. Paper is finally IN the "
  "actual leaders (semis + nuclear/AI-power, all 6 GTC-stopped) but bought mid-day = tail only; live is a 6th straight session "
  "100% cash on an armed-but-untapped NVDA ticket. Honest correction to earlier: gating SOXL +16.5% / TQQQ +5.7% did NOT 'save' "
  "us today — they went UP, so the gate cost upside (still the right rule over the sample, just not a win today). Real credit: "
  "cut the SQQQ + PLTR drags, didn't chase parabolic MU/BE, zero naked. Finalizes at the close."),
 "capture":{
   "bestName":"BE +14.9% (sold 7/20, unowned) & MU +12.3% (memory catalyst, unowned); SOXL +16.5% ran but was correctly gated (3x)",
   "bestPct":"+14.9% / +12.3%",
   "capturedPct":"paper +0.2%, live 0%",
   "rate":"~1–2% — owned the right leaders (AMD/SMR/OKLO) but entered mid-day = tail capture; live flat in cash"},
 "missed":[
   {"from":"BE (sold 7/20 @ $203 on the delay catalyst)","to":"holding BE","note":"BE V-reversed +14.9% to ~$226 today; the cut was on a real verified catalyst but price ran hard against it — a watchlist miss","delta":"~+$70 vs held (3 sh)"},
   {"from":"the open","to":"mid-day entries","note":"AMD/SMR/OKLO/VRT added mid-day — captured only the tail of +5–8% moves, not the whole run","delta":"tail only"},
   {"from":"live cash","to":"MU / the memory catalyst","note":"MU +12.3% on the Anthropic deal was the day's cleanest catalyst; unowned, and by 2pm too extended to chase","delta":"missed, now chase-risk"},
   {"from":"live cash","to":"NVDA (armed, untapped)","note":"6th straight session 100% live cash; ticket armed since 8:17a, only fills on Adam's tap","delta":"opportunity, pending tap"}],
 "saved":[
   {"note":"Cut the SQQQ hedge into the rally — it fell ~6% today as QQQ ripped; holding it would've bled","delta":"avoided hedge drag"},
   {"note":"Cut the flat PLTR laggard (−1.6% today, the only red watchlist name) and redeployed to leaders","delta":"−$334 realized, redeployed"},
   {"note":"Didn't chase parabolic MU +12% / BE +15% at 2pm — the top-tick mistake the Playbook names","delta":"avoided chase risk"},
   {"note":"Zero naked — all 6 paper positions GTC-stopped, verified at the broker this run","delta":"risk bounded"}],
 "avoided":{"worstName":"PLTR","worstPct":"−1.6%","note":"the only red watchlist name; already cut this session — broad green tape, little downside to dodge","amount":"~$0 (small)","rate":"n/a on a risk-on day"},
 "best":{"name":"AMD (paper)","note":"the one big winner we actually owned into the move — +8.1% today","delta":"+$486 unrealized"},
 "worst":{"name":"live cash (structural, 6th day)","note":"a +12–16% target-rich day captured $0 live; the NVDA fix is armed but needs the tap — execution-timing, not selection","delta":"0% of the day"},
 "applying":"Applying the 7/20 lesson: the capture gap is EXECUTION-TIMING, not regime — cut drags and commit to the leaders in the MORNING, not mid-day. Today's paper rotation was right but a beat late; live's NVDA fix is armed for the tap.",
 "adjust":"Tomorrow: commit the live core at/near the OPEN (don't let the ticket ride untapped all day again) and take paper's leader entries on the FIRST confirmation, not mid-day — stop paying the tail-only tax. Lever the 3x only once QQQ closes above its $714.7 20-day, ideally past Wed's GOOGL/TSLA/AMD prints."
}

# ---- score (real) ----
d["score"] = {"alphaPts":"-16.4","benchmark":"-2.6%","bestDay":"+3.2%",
 "bestDayName":"Jul 14 — CPI chip rally (settled)","winRate":"33%","tradeCount":6}

# ---- paper / live blocks ----
pap = d.setdefault("paper", {})
pap["equity"] = 89811.52
pap["updated"] = TS
for pt in pap.get("equity_curve", []):
    if pt.get("date") == "Jul 21": pt["value"] = 89811.52
pap["equity_note"] = ("Paper ~$89.8k (+0.2% vs Mon) — owns the day's leaders (AMD +8.1% / SMR +8.5% / OKLO +5.4% / VRT +4.3% / "
 "CEG +3.5%) but the +0.2% reflects mid-day entries (tail only) + the realized SQQQ de-hedge & PLTR cut (−$334). "
 "6/6 GTC-stopped, zero naked (AMD 30/$490, NVDA 140/$186, SMR 700/$7.50, OKLO 200/$39, VRT 30/$282, CEG 16/$236). "
 "~$16.4k cash = gated 3x powder for a confirmed QQQ ~$715 reclaim, ideally past Wed's earnings.")

liv = d.setdefault("live", {})
liv["equity"] = 810.32; liv["cash"] = 810.32; liv["positions"] = []
liv["updated"] = TS
for pt in liv.get("equity_curve", []):
    if pt.get("date") == "Jul 21": pt["value"] = 810.32
liv["equity_note"] = ("LIVE flat $810.32 cash / zero positions / zero naked; 1 pending ticket = BUY NVDA 3 sh (~$207, $186 stop, "
 "swing / 0 day-trades used). 6th straight session in cash — armed since 8:17a, pending Adam's tap. −19.0% since $1,000 inception.")

# ---- latest_recap ----
d["latest_recap"] = ("2:44p 7/21 — Monitor/refresh (no new trade). Paper 6 names AMD/CEG/NVDA/OKLO/SMR/VRT, all GTC-stopped, "
 "~$89.8k, ~$16.4k cash = 3x powder for a confirmed QQQ $714.7 reclaim (prefer post-GOOGL/TSLA). Theme: MU +12.3% (Anthropic "
 "memory deal, BofA $1,550), semis + nuclear/AI-power green; SOXL +16.5% / TQQQ +5.7% ripped but stayed GATED. LIVE: NVDA swing "
 "armed + untapped, 6th day cash — the tap is the lever. Honest grade D+ (running): right book, late+light, ~1–2% capture.")

d["updated"] = TS

# ---- atomic write ----
tmp = F + ".tmp"
with open(tmp, "w") as fh:
    json.dump(d, fh, ensure_ascii=False, indent=1)
os.replace(tmp, F)
print("WROTE", F)
