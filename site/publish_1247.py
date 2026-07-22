import json, os, time, shutil

SITE = "engine-data.json"
TICKET = "/sessions/youthful-lucid-mccarthy/mnt/movita-backend/queue/trade-ticket-2026-07-22-1.json"
TS = "2026-07-22T12:47:00-04:00"

# --- backup first ---
bak = "engine-data.backup-2026-07-22-1247.json"
shutil.copyfile(SITE, bak)
d = json.load(open(SITE))

d["updated"] = TS

# ---------- PULSE ----------
pulse_text = ("12:47p - Trailed the winners' stops UP again into tonight's GOOGL/TSLA/IBM/TXN binary and kept the book intact: "
"AMD $515->$525, NVDA $186->$203 (just under today's low), CEG $260->$263 - all 6 paper names stay GTC-stopped, zero naked, "
"~21% powder ($19k) kept DRY to deploy post-binary per yesterday's note (not into a coin-flip). Honest read: paper cooled to "
"+0.62% from the morning's +1.3% peak as OKLO round-tripped its +7.6% spike back to +1.3% and RKLB - which I bought near the "
"top tick this AM - sits red on entry; capture slipped to ~18% vs CEG/RKLB's +3.5%. We own the right movers, but the RKLB "
"top-tick entry is today's execution ding. LIVE flat cash a 7th session; the OKLO one-tap is refreshed and live near the "
"$44.7 base (better entry than the spike, $39 stop, 0/3 day-trades). Next: hold through the binary, deploy the powder tomorrow.")
pulse_hype = ("Locked the winners' stops up and kept cash dry for after tonight's Google/Tesla earnings instead of gambling it into the print. "
"Owning the right names, but I chased Rocket Lab too high this morning - that's the miss; the Oklo one-tap's still there to get the real account in.")
d["pulse"] = [{"ts": TS, "text": pulse_text, "hype": pulse_hype}] + d.get("pulse", [])
d["pulse"] = d["pulse"][:15]

# ---------- STATUS ----------
d["status"] = [
  {"session": "Morning", "text": "Rotated laggard into RKLB mover"},
  {"session": "Afternoon", "text": "Trailed stops up; powder dry for binary"},
]

# ---------- HEADLINES ----------
d["headlines"] = [
  "Mega-cap earnings tonight: GOOGL + TSLA (plus IBM, TXN) after the close - the season's biggest AI-capex test",
  "Nuclear-for-AI leadership rotates to CEG (+3.5%, new highs); OKLO fades its +7.6% spike back to +1.3% into today's DOE summit",
  "OKLO/X-Energy formally in the Trump/DOE $200M nuclear-for-AI program (MSFT/NVDA partners) - Bloomberg-confirmed",
  "Semis stay bid: NVDA +3.2%, AMD +2.1%, SOXL +3.5% as Taiwan posts record +59% export orders confirming the AI supercycle",
  "SMCI holds a +24% moonshot on a record $60B AI-server order haul + margin guide-up - bullish buildout read-through",
  "RKLB +3.5% holds its $266M Space Force win; RS firm in space/defense",
  "Extended high-beta keeps rolling over: PLTR -4.9%, SOFI -2.8% as money rotates to catalyst names",
  "Tape digests the 2-day rip: SPY +0.2% near records, QQQ flat and still just under its 20-day (3x gated)",
]

# ---------- COVERAGE ----------
cov = []
def C(**k): cov.append(k)

C(ticker="OKLO", name="Oklo Inc.", theme="Advanced nuclear for AI power", verdict="buy",
  verdict_label="Buy - live armed + paper held",
  thesis="**pop_rank 1 on a live, dated catalyst** - the Trump/DOE $200M program to fast-track advanced reactors for AI data centers (OKLO+X-Energy w/ MSFT/NVDA), Bloomberg-confirmed, with a DOE AI-energy summit TODAY that may drop detail this afternoon. Spiked to $47.48, faded to ~$44.7 back on the $44.9 intraday base (a better entry than the spike) - no own earnings to Aug 18, insulated from tonight's Mag-7 capex binary.",
  hold_reason="Small nuclear-reactor company that just got formally named into the Trump/DOE $200M program to power AI data centers alongside Microsoft and Nvidia - that's the catalyst we bought. Paper owns 300 sh near $44.6 (stop $43) and there's a live one-tap ticket to finally get the real account in too. It ran +7.6% this morning then gave it back; we hold through today's DOE summit and would cut it if $43 breaks or the summit clearly disappoints.",
  size="$13.4k (300 sh paper)", size_pct=14.8, size_note="pop_rank-1; paper stop $43; live armed one-tap",
  plan_usd="$715 live (armed $48 limit, one tap) / 300 sh paper held", chg_pct="+1.3%",
  projection={"target_pct":3.5,"confidence":"med","basis":"DOE summit detail may drop this PM; catalyst intact","pop_rank":1,"path_pct":[1.3,2.4,3.5]},
  updated=TS, horizon="swing (multi-day)")

C(ticker="CEG", name="Constellation Energy", theme="Nuclear utility for AI power", verdict="buy",
  verdict_label="Buy - paper held (RS leader)",
  thesis="**Today's actual nuclear RS leader - +3.5% at NEW HIGHS** ($274 HOD) while OKLO/SMR fade. The blue-chip way to own power-for-AI; structurally insulated from tonight's GOOGL/TSLA capex binary. Held 16 sh (~$261), stop trailed $260->$263 under today's $263.3 low to lock the new-high gain.",
  hold_reason="Constellation is the big nuclear utility - the blue-chip way to own the same power-for-AI theme, and today it's the one actually making new highs. We're in at ~$261 and just trailed the stop up to $263 to lock the gain. It's insulated from tonight's Google/Tesla earnings so we're happy holding through the binary; we'd only sell if it lost the $263 shelf.",
  size="$4.3k (16 sh paper)", size_pct=4.8, size_note="new-high leader; stop trailed $260->$263",
  plan_usd="held paper", chg_pct="+3.5%",
  projection={"target_pct":4.5,"confidence":"high","basis":"nuclear RS leader at new highs, binary-insulated","pop_rank":2},
  updated=TS, horizon="swing (multi-day)")

C(ticker="NVDA", name="NVIDIA Corp.", theme="AI accelerators", verdict="buy",
  verdict_label="Buy - paper held",
  thesis="**+3.2% near a $214 HOD** on the semis supercycle bid - Taiwan just posted record +59% June export orders confirming AI demand. Held 90 sh (~$208), stop trailed $186->$203 (just under today's $205 low) to protect the gain into tonight's GOOGL/TSLA capex read-through. No own earnings to late Aug.",
  hold_reason="The AI-chip leader, and today the whole complex is bid - Taiwan just posted record export orders confirming the supercycle. We're in at ~$208, up nicely, and trailed the stop to $203 (just under today's low) to protect the gain into tonight's Google/Tesla capex prints, which read straight through to Nvidia demand. Ride it if they beat; the stop takes us out near breakeven if they disappoint.",
  size="$19.2k (90 sh paper)", size_pct=21.3, size_note="largest weight; stop trailed $186->$203",
  plan_usd="held paper", chg_pct="+3.2%",
  projection={"target_pct":3.5,"confidence":"med","basis":"semis supercycle bid; capped by tonight's binary","pop_rank":3},
  updated=TS, horizon="swing (multi-day)")

C(ticker="RKLB", name="Rocket Lab", theme="Space / defense launch", verdict="buy",
  verdict_label="Buy - paper held (rotated in)",
  thesis="**Day's biggest watchlist mover +3.5%** on a fresh $266M Space Force contract - rotated in this morning. Honest ding: bought near the $72.9 top tick, so it's red on our ~$72.7 entry despite being green on the day. Stop wide at $65.50; thesis (contract momentum) intact.",
  hold_reason="Rocket Lab - we rotated into it this morning because it was the day's biggest watchlist mover on a fresh $266M Space Force contract. Honestly we bought it a bit high, right near the top tick, so it's red on our entry even though it's +3.5% on the day - that's the execution lesson today. Thesis is intact and the stop's wide at $65.50, so we're holding for the multi-day contract momentum.",
  size="$8.8k (123 sh paper)", size_pct=9.7, size_note="mover rotation; bought near HOD (ding); stop $65.50",
  plan_usd="held paper", chg_pct="+3.5%",
  projection={"target_pct":4.0,"confidence":"med","basis":"$266M Space Force contract momentum","pop_rank":4},
  updated=TS, horizon="swing (multi-day)")

C(ticker="AMD", name="Advanced Micro Devices", theme="AI accelerators", verdict="buy",
  verdict_label="Buy - paper held",
  thesis="**+2.1% off a $558 HOD**, our biggest paper winner (+5% from ~$528), riding the semis bid + the BofA-flagged $170B server-CPU battle vs NVDA. Own earnings not until Aug 4. Stop trailed $515->$525 under today's $526.6 base to lock ~breakeven-plus into the binary.",
  hold_reason="The other big AI-chip name, riding the same semis strength. We're up ~5% from ~$528 and it's our biggest paper winner; stop trailed to $525 to lock in roughly breakeven-plus. Its own earnings aren't until Aug 4, so the main risk tonight is a sympathy move off Google/Tesla - we hold and let the stop do the work.",
  size="$16.7k (30 sh paper)", size_pct=18.4, size_note="biggest winner (+5%); stop trailed $515->$525",
  plan_usd="held paper", chg_pct="+2.1%",
  projection={"target_pct":2.5,"confidence":"med","basis":"server-CPU battle + semis strength; near HOD","pop_rank":6},
  updated=TS, horizon="swing (multi-day)")

C(ticker="SOXL", name="3x Semis Bull ETF", theme="3x leveraged semis", verdict="avoid",
  verdict_label="Avoid - whipsaw / 3x gated",
  thesis="**+3.5% but round-tripped -8%->+4% today** - a $147-166 whiplash. The regime gate (QQQ still under its 20-day) keeps us OUT of 3x into tonight's binary; owning this would be a coin-flip, not an edge.",
  hold_reason="",
  size="-", size_pct=0, size_note="3x gated by regime; whipsaw risk",
  plan_usd="watch only (3x gated)", chg_pct="+3.5%",
  projection={"target_pct":4.5,"confidence":"low","basis":"3x semis; huge whipsaw risk into binary","pop_rank":5},
  updated=TS, horizon="intraday")

C(ticker="SMCI", name="Super Micro", theme="AI servers", verdict="watch",
  verdict_label="Watch - already popped",
  thesis="**+24% moonshot** on a record $60B AI-server order haul + margins guided to 15-17% (from ~8%). A bullish read-through for the whole AI-buildout book, but chasing a +24% midday gap is the top-tick trap - we take the sympathy read, not the chase.",
  hold_reason="",
  size="-", size_pct=0, size_note="don't chase a +24% gap",
  plan_usd="watch only (no-chase)", chg_pct="+24.2%",
  projection={"target_pct":24.0,"confidence":"low","basis":"already popped +24%; extended, no-chase","pop_rank":7},
  updated=TS, horizon="intraday")

C(ticker="RGTI", name="Rigetti Computing", theme="Quantum computing", verdict="watch",
  verdict_label="Watch",
  thesis="**+0.4%, quiet** - quantum sympathy name with no fresh catalyst today. On the board for a momentum flag but no setup right now.",
  hold_reason="",
  size="-", size_pct=0, size_note="no catalyst today",
  plan_usd="watch only", chg_pct="+0.4%",
  projection={"target_pct":0.5,"confidence":"low","basis":"quantum sympathy, thin, no catalyst","pop_rank":8},
  updated=TS, horizon="intraday")

C(ticker="IONQ", name="IonQ Inc.", theme="Quantum computing", verdict="watch",
  verdict_label="Watch",
  thesis="**-0.2%, flat** - the larger quantum name, no catalyst today. Watching for a volume breakout; nothing actionable now.",
  hold_reason="",
  size="-", size_pct=0, size_note="flat, no catalyst",
  plan_usd="watch only", chg_pct="-0.2%",
  projection={"target_pct":-0.2,"confidence":"low","basis":"quantum flat, no catalyst","pop_rank":9},
  updated=TS, horizon="intraday")

C(ticker="SMR", name="NuScale Power", theme="Small modular nuclear", verdict="hold",
  verdict_label="Hold - paper (weakest name)",
  thesis="**-1.0%, the nuclear laggard** while CEG makes new highs and OKLO holds. Same power-for-AI theme but the weakest name we hold; basically breakeven at ~$8.66, wide $7.50 stop. First candidate to rotate OUT of post-binary if it keeps lagging.",
  hold_reason="NuScale, the small-cap nuclear name - same power-for-AI theme but the laggard of the group today, roughly flat-to-red while CEG makes new highs. We're basically breakeven at ~$8.66 with a wide $7.50 stop. It's the weakest name we hold, so it's first on the chopping block to rotate out of after tonight's earnings if it keeps lagging.",
  size="$9.0k (1050 sh paper)", size_pct=10.0, size_note="weakest hold; rotation candidate post-binary",
  plan_usd="held paper", chg_pct="-1.0%",
  projection={"target_pct":-1.0,"confidence":"low","basis":"nuclear laggard fading vs CEG/OKLO","pop_rank":10},
  updated=TS, horizon="swing (multi-day)")

C(ticker="TSLA", name="Tesla Inc.", theme="EV / earnings binary", verdict="watch",
  verdict_label="Watch - reports tonight",
  thesis="**-0.4%, drifting into its own earnings binary tonight.** Too much event risk to position; watching the after-hours print for a next-day read on high-beta risk appetite.",
  hold_reason="",
  size="-", size_pct=0, size_note="earnings tonight - event risk",
  plan_usd="watch only (earnings binary)", chg_pct="-0.4%",
  projection={"target_pct":-0.5,"confidence":"low","basis":"drifting into tonight's earnings binary","pop_rank":11},
  updated=TS, horizon="intraday")

C(ticker="VRT", name="Vertiv Holdings", theme="Data-center cooling", verdict="avoid",
  verdict_label="Avoid - sold this morning",
  thesis="**-1.3%, the capex-beta laggard** we rotated out of this AM (~-$158 realized) to fund RKLB. Confirming the sell - it's red while the movers ran. Stays off until it reclaims structure.",
  hold_reason="",
  size="-", size_pct=0, size_note="sold AM into RKLB; opportunity-cost rotation",
  plan_usd="avoid (rotated out)", chg_pct="-1.3%",
  projection={"target_pct":-1.5,"confidence":"low","basis":"capex-beta laggard, red post-rotation","pop_rank":12},
  updated=TS, horizon="intraday")

C(ticker="SOFI", name="SoFi Technologies", theme="Fintech / high-beta", verdict="avoid",
  verdict_label="Avoid - rolling over",
  thesis="**-2.8%, high-beta fintech rolling over** with the rest of the extended complex. No catalyst; money is rotating out of it into the AI-power/semis names. Dodged.",
  hold_reason="",
  size="-", size_pct=0, size_note="high-beta rolling over; dodged",
  plan_usd="avoid", chg_pct="-2.8%",
  projection={"target_pct":-3.0,"confidence":"low","basis":"high-beta fintech rolling over, no catalyst","pop_rank":13},
  updated=TS, horizon="intraday")

C(ticker="PLTR", name="Palantir", theme="AI software / high-beta", verdict="avoid",
  verdict_label="Avoid - worst name",
  thesis="**Worst watchlist name -4.9%** - extended high-beta AI-software rolling over hard (lost $132 to $126). The tell that money is rotating from momentum crowd-favorites into dated catalysts. Hold none; dodged.",
  hold_reason="",
  size="-", size_pct=0, size_note="worst name; extended, rolling over",
  plan_usd="avoid (worst RS)", chg_pct="-4.9%",
  projection={"target_pct":-5.0,"confidence":"med","basis":"worst RS, extended, rolling over hard","pop_rank":14},
  updated=TS, horizon="intraday")

d["coverage"] = cov

# ---------- FEED (prepend one activity) ----------
feed_item = {"type":"activity","ts":TS,
  "text":("12:47p - HOLD + TRAIL: trailed AMD/NVDA/CEG stops up (->$525 / ->$203 / ->$263) to lock gains into tonight's "
  "GOOGL/TSLA binary; all 6 paper names stay GTC-stopped, zero naked. Kept the ~21% ($19k) powder DRY for the post-binary "
  "deploy rather than gambling it into the print. Honest ding: OKLO round-tripped its +7.6% spike to +1.3% and RKLB (bought "
  "near the top tick this AM) is red on entry - capture ~18%; we own the movers but the RKLB entry was chased. LIVE flat a "
  "7th session; OKLO one-tap refreshed + live near the $44.7 base."),
  "reaction":"hold"}
d["feed"] = [feed_item] + d.get("feed", [])
d["feed"] = d["feed"][:40]

# ---------- SCORE (TQQQ ~flat today; carry real prior computation) ----------
d["score"] = {"alphaPts":"-16.4","benchmark":"-2.6%","bestDay":"+3.2%",
  "bestDayName":"Jul 14 - CPI chip rally (settled)","winRate":"33%","tradeCount":6}

# ---------- ACCOUNTABILITY (running, honest) ----------
d["accountability"] = {
  "date":"2026-07-22","final":False,"grade":"C+ (running, ~3h in)",
  "headline":("Owning the right names - CEG/RKLB/NVDA, the day's movers - but capture cooled to ~18% as OKLO round-tripped its "
  "+7.6% spike back to +1.3% and RKLB was bought at the top tick this morning (the day's real execution ding). Paper +0.62%, "
  "all GTC-stopped into tonight's binary with 21% dry. LIVE flat cash a 7th session remains the biggest single drag; the OKLO "
  "one-tap is refreshed and live at the base."),
  "capture":{"bestName":"CEG +3.5% / RKLB +3.5% (both HELD)","bestPct":"+3.5%","capturedPct":"paper +0.62% / live flat",
    "rate":"~18% - we own the best movers but the blend is dragged by OKLO's give-back, flat SMR, and RKLB's top-tick entry; LIVE cash is the real 0% drag"},
  "missed":[
    {"from":"live cash","to":"OKLO","note":"LIVE flat a 7th session while its armed pick OKLO sits on a live DOE-summit catalyst - the un-tapped ticket is the capture gap","delta":"needs the tap"},
    {"from":"market-buy RKLB at the high","to":"scale-in near VWAP","note":"chased RKLB at the top tick (+0 -> -$131); the mover was right, the entry wasn't","delta":"-$131 unrealized"}
  ],
  "saved":[
    {"note":"Trailed AMD/NVDA/CEG stops up to lock gains into tonight's GOOGL/TSLA binary rather than risk giving them back","delta":"gains locked"},
    {"note":"Did NOT chase SMCI's +24% gap or deploy the last 21% powder into a coin-flip binary - kept it dry for the confirmed post-binary direction","delta":"coin-flip dodged"},
    {"note":"Regime gate kept us out of 3x SOXL, which round-tripped -8% -> +4%","delta":"whipsaw dodged"}
  ],
  "avoided":{"worstName":"PLTR","worstPct":"-4.9%","note":"PLTR is the worst watchlist name (-4.9%, extended, rolling over) alongside SOFI -2.8% - hold none, dodged both","amount":"none held","rate":"100% dodged"},
  "best":{"name":"CEG","note":"the nuclear RS leader at new highs, held not watched; stop trailed up to lock the gain","delta":"+3.5%"},
  "worst":{"name":"RKLB","note":"bought the mover at the top tick this morning - right name, wrong entry","delta":"-$131 unrealized"},
  "applying":"Weight to the MOVER + own the biggest name you're tracking (7/21) - we own CEG/RKLB/NVDA, the day's movers.",
  "adjust":"Two levers: (1) keep the OKLO one-tap loud + refreshed at the base to finally get LIVE in; (2) when rotating into the day's mover, scale in near VWAP/the base - don't market-buy the top tick (the RKLB ding). Deploy the 21% paper powder post-binary into the confirmed direction."
}

# ---------- PENDING_TICKETS (refresh OKLO to current) ----------
d["pending_tickets"] = [{
  "id":"2026-07-22-1","symbol":"OKLO","side":"buy","size":"$715","qty":16,
  "entry":"OKLO faded its $47.48 HOD back to ~$44.7 (+1.3%), sitting right on the $44.9 intraday base - so the $48 marketable limit fills NEAR THE MONEY (~$44.7), a better entry than the morning spike (16 sh x ~$44.7 = ~$715 < $810 BP). Approve ANYTIME -> fills at <=$48; if it spikes back it rests and fills on a pullback. Multi-day swing, PDT-free (0/3 day-trades).",
  "trigger":None,"stop":39.0,
  "bracket":"stop $39 GTC (below the $40-41 base / 7/17 $39.53 low, ~-13% from ~$44.7)",
  "thesis":"Ends a 7th session of live cash by owning the pop_rank-1 nuclear-for-AI name on a live, Bloomberg-confirmed catalyst - OKLO formally in the Trump/DOE $200M program (w/ MSFT/NVDA), DOE AI-energy summit TODAY may drop detail this PM. No own earnings to Aug 18, structurally insulated from tonight's GOOGL/TSLA capex binary. Faded to the base = the lower-risk entry. 25-analyst 12-mo PT $86.50 (~90% upside). Wide $39 stop (~$92 max risk on ~$715). Paper already owns 300 sh, stop $43."
}]

# ---------- ATOMIC WRITE ----------
tmp = SITE + ".tmp"
with open(tmp, "w") as f:
    json.dump(d, f, ensure_ascii=False, indent=1)
os.replace(tmp, SITE)
print("engine-data.json written; backup:", bak)

# ---------- refresh LIVE ticket file (atomic) ----------
ticket = {
  "id":"2026-07-22-1","side":"buy","symbol":"OKLO","qty":16,"size":"$715","limit":48.0,
  "entry":"OKLO faded its $47.48 HOD back to ~$44.7 (+1.3% today), sitting right on the $44.9 intraday base - so the $48 marketable limit fills a tap NEAR THE MONEY (~$44.7), a BETTER entry than the morning spike (16 sh x ~$44.7 = ~$715 reserve < $810 BP). Approve ANYTIME -> fills at <=$48; if it spikes back above $48 the limit rests and fills on any pullback. Multi-day swing, PDT-free (0/3 day-trades used).",
  "trigger":None,"stop":39.0,
  "bracket":"stop $39 GTC (below this week's $40-41 base / the 7/17 $39.53 low, ~-13% from ~$44.7)",
  "horizon":"swing (multi-day, PDT-free) - 0 day-trades used",
  "thesis":"Ends a 7th straight session of live cash by owning the pop_rank-1 nuclear-for-AI name on a live, Bloomberg-confirmed catalyst: OKLO is formally in the Trump/DOE $200M program to fast-track advanced reactors for AI data centers (with X-Energy, MSFT/NVDA partners), and the DOE AI-energy summit is TODAY - detail may drop this afternoon. It spiked +7.6% then faded to the $44.7 base (the lower-risk entry), no own earnings to Aug 18, structurally insulated from tonight's GOOGL/TSLA/IBM/TXN capex binary. 25-analyst 12-mo PT $86.50 (~90% upside). Wide $39 stop under the base (~$92 max risk on ~$715). Paper already owns 300 sh, stop $43.",
  "premortem":"OKLO already round-tripped a +7.6% spike today, so momentum has cooled - a 'sell-the-summit' fade could drag it toward the $41-42 base (stop sits below at $39, ~-13%, ~$92 max risk). Entering on the base rather than the spike is the risk-managed way in, and the multi-day government catalyst + wide stop justify the swing. The real failure mode remains a 7th session of lazy live cash while the theme runs without us. If OKLO gaps well past $48 don't chase - wait for the next base.",
  "expires":"2026-07-22T16:00:00-04:00"
}
tt = TICKET + ".tmp"
with open(tt, "w") as f:
    json.dump(ticket, f, ensure_ascii=False, indent=2)
os.replace(tt, TICKET)
print("ticket refreshed:", TICKET)
