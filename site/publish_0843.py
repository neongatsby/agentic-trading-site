import json, os, tempfile, shutil, datetime

SITE = os.path.dirname(os.path.abspath(__file__))
F = os.path.join(SITE, "engine-data.json")
TS = "2026-07-22T08:43:00-04:00"

with open(F) as fh:
    d = json.load(fh)

# --- backup current good state first ---
bak = os.path.join(SITE, "engine-data.backup-2026-07-22-0843.json")
with open(bak, "w") as fh:
    json.dump(d, fh, indent=1, ensure_ascii=False)

# --- per-ticker updates: chg_pct, projection, updated, thesis, hold_reason ---
chg = {"NVDA":"-1.3%","AMD":"-2.4%","SMR":"-0.9%","OKLO":"+1.7%","VRT":"-3.2%",
       "CEG":"-0.8%","MU":"-4.0%","BE":"-2.0%","RGTI":"-2.0%","IONQ":"-2.0%",
       "RKLB":"-1.5%","TSLA":"+0.2%","SOXL":"-5.5%","TQQQ":"-2.7%"}

proj = {
 "OKLO": (3.0,"high","DOE nuclear-for-AI leader; green as chips fade",1),
 "SMR":  (1.0,"med","nuclear sympathy; small-cap RS ~flat pre-open",2),
 "CEG":  (0.5,"med","nuclear utility bid; steady into risk-off",3),
 "NVDA": (-0.5,"med","laggard re-entry; chips fading into tonight's binary",4),
 "AMD":  (-1.5,"low","giving back 2-day rip; event digested, Aug print ahead",5),
 "VRT":  (-2.0,"low","data-center power giving back on risk-off open",6),
 "RKLB": (-1.5,"low","space beta; sells with risk-off tape",7),
 "TSLA": (0.0,"med","reports after close - the move is tonight",8),
 "IONQ": (-2.0,"low","quantum high-beta; cools risk-off",9),
 "RGTI": (-2.0,"low","quantum high-beta; sells risk-off tape",10),
 "TQQQ": (-2.7,"low","3x Nasdaq powder; awaits 20-day reclaim",11),
 "BE":   (-3.0,"med","spent parabolic after +16%; give-back risk",12),
 "MU":   (-4.0,"med","giving back the +12.8% rip; extended",13),
 "SOXL": (-5.5,"med","3x semis unwinding the rip; gate vindicated",14),
}

thesis = {
 "NVDA":"**The group's biggest laggard on the 2-day rip (+1.9% vs MU/AMD +8-12%) - the catch-up name, -1.3% pre-open into a cheaper re-entry.** Micron's HBM blowout reads straight through to NVDA GPUs; least-extended AI leader with NO own earnings binary this week (GOOGL/TSLA print tonight, NVDA late-Aug). $186 stop under the late-June base. Also the live swing - armed to fire at today's open.",
 "AMD":"**Tuesday's owned leader (+8.1% on the 2-day semi rip) now giving back -2.4% pre-open - digesting, not broken.** 'Advancing AI 2026' event is underway (7/22-23); Q2 earnings aren't until Aug 4, so no print binary this week - hold 30 sh through the event on a wide $490 stop rather than trim into weakness.",
 "SMR":"**Relative-strength leader of the nuclear-for-AI-power group (+9.3% Tue), roughly flat (-0.9%) pre-open as chips fade.** Built to 700 sh; volatile small-cap so the stop's wide at $7.50.",
 "OKLO":"**FRESH CATALYST holding: OKLO in the Trump/DOE $200M program to fast-track nuclear reactors for AI data centers - the lone watchlist name GREEN pre-open (+1.7%) as semis give back.** 200 sh from $43.92, +2% and RS-leading; $39 stop. pop_rank 1.",
 "VRT":"**Datacenter power & cooling, giving back -3.2% pre-open with the risk-off tape - less extended than the chips, which is why we own it.** 30 sh; $282 stop below structure; the AI-capex read-through from tonight's mega-cap prints is the tell.",
 "CEG":"**Nuclear utility signing deals to power AI datacenters, -0.8% pre-open - the steady, defensive leg of the nuclear-for-AI book.** Longer-term hold; $236 stop.",
 "MU":"**Tuesday's engine (+12.8% on the Anthropic memory deal + BofA $1,550), giving back -4.0% pre-open - extended.** The super-cycle read-through we play via AMD/NVDA rather than chasing a $930 stock after a parabolic day.",
 "BE":"**+16% Tuesday on the fuel-cell-power-for-AI squeeze; indicated -2% pre-open - a spent parabolic into the earnings-heavy tape.** Correctly not chasing; watching for a real base, not the high.",
}

hold = {
 "NVDA":"Our core AI position and the group's laggard - 140 sh from ~$208 (about flat), -1.3% pre-open. The catalyst is real (SEC filing: NVDA lifted its Nebius stake to 9.3%, ~$5B; Micron's HBM blowout reads through to NVDA GPUs), so we read it as the catch-up name, not a broken one. It's also the live swing we're trying to own, armed to fill at today's open. The $186 stop is our line if the whole AI trade rolls over.",
 "AMD":"Our best-owned leader - up ~8% on the 2-day semi rip, now giving back ~2% pre-open into its Advancing AI 2026 developer event (underway 7/22-23), which is the catalyst (earnings aren't until Aug 4, so no print risk this week). We hold 30 sh from ~$528, ~flat. Keeping the stop wide ($490) to ride the event rather than get shaken out on the give-back; we'd only sell if the whole AI trade rolls over.",
 "SMR":"NuScale - small modular reactors, a pure play on powering AI datacenters. We built to 700 sh (~$8.63) as it led the nuclear group +9% Tuesday; roughly flat pre-open as chips fade. Volatile small-cap so the stop's wide at $7.50; watching whether the nuclear-for-AI bid follows through today on the DOE headline.",
 "OKLO":"Nuclear/AI-power name we own (200 sh from ~$43.92, +2%, $39 stop). The catalyst is live: the Trump administration/DOE tapped OKLO + X-Energy for a $200M program to speed nuclear reactors for AI data centers. It's the lone watchlist name green pre-open (+1.7%) while semis give back - the relative-strength tell. Holding to let the government-backed theme run; the $39 stop is our line if the pop fades.",
 "VRT":"Vertiv - datacenter power and cooling, the 'picks-and-shovels' of the AI-capex build. 30 sh ~$305, giving back ~3% pre-open with the risk-off tape; less extended than the chips, which is why we like it. $282 stop; watching the datacenter-capex read-through from tonight's mega-cap earnings.",
 "CEG":"Constellation - the nuclear utility literally signing deals to power AI datacenters. Longer-term hold, 16 sh from ~$261, ~flat (-0.8% pre-open). $236 stop. The steady, defensive leg of our nuclear-for-AI book; watching the AI-power-demand narrative re-rating the group.",
}

for c in d["coverage"]:
    t = c["ticker"]
    if t in chg: c["chg_pct"] = chg[t]
    if t in proj:
        tp,conf,basis,pr = proj[t]
        pj = c.get("projection") or {}
        pj["target_pct"] = tp; pj["confidence"] = conf; pj["basis"] = basis; pj["pop_rank"] = pr
        c["projection"] = pj
    if t in thesis: c["thesis"] = thesis[t]
    if t in hold and c.get("hold_reason"): c["hold_reason"] = hold[t]
    c["updated"] = TS

# --- status ---
d["status"] = [{"session":"Pre-market","text":"Risk-off open; NVDA armed"}]

# --- headlines ---
d["headlines"] = [
 "BINARY tonight: GOOGL + TSLA report after the close (IBM, TXN, ServiceNow, AT&T too) - the first Mag-7 AI-capex test; Alphabet's '26 capex guide is the number for our book",
 "Risk-off open: Nasdaq-100 futures -0.6%, S&P -0.2%, Dow -0.1% into the earnings wall",
 "First 7/22 pre-market prints in: chips giving back the 2-day rip - NVDA -1.3%, AMD -2.4%, MU -4.0%; OKLO +1.7% the lone watchlist green",
 "OKLO the RS leader (pop_rank 1) on the confirmed Trump/DOE $200M nuclear-for-AI program (OKLO + X-Energy)",
 "QQQ ~$702 pre-market = ~-1.8% under its $714.7 20-day (softer than Tue's -0.8% close) - 3x still gated",
 "Oil elevated (~$95, Iran tensions) capping otherwise-strong earnings; 88% of S&P Q2 reporters beating",
 "NVDA live swing armed for the 9:30 open (3 sh, $186 stop, approve-anytime) to end a 6-session cash camp",
 "AMD 'Advancing AI 2026' event underway (7/22-23) - owned 30 sh into it, giving back -2.4% pre-open",
]

# --- pulse prepend ---
pulse_new = {
 "ts": TS,
 "text": "8:43a pre-market - heartbeat ~47 min from the open. Both books re-reconciled clean at the broker: LIVE flat $810.32 cash (6th session, 0/3 day-trades), PAPER 6/6 GTC-stopped (AMD/CEG/NVDA/OKLO/SMR/VRT), zero naked. First real 7/22 pre-market prints now on the feed confirm the risk-off open - NVDA -1.3%, AMD -2.4%, MU -4.0%, VRT -3.2% (chips giving back the 2-day rip) while OKLO +1.7% holds green on its DOE nuclear-for-AI catalyst (kept pop_rank 1). QQQ ~$702 pre-market slipped to ~-1.8% under its 20-day (was -0.8% at Tue's close), so the tape's softer into tonight's GOOGL/TSLA/IBM/TXN binary. NVDA live ticket 2026-07-21-1 (3 sh, $211 marketable-limit, $186 stop) stays armed -> fires at the 9:30 open on your tap. No pre-market execution by design; the NVDA re-entry + paper NVDA->nuclear trim run at the OPEN with real prices.",
 "hype": "Chips are fading pre-open, OKLO's the one holding green. Nothing to do till the bell - the NVDA buy's still armed for the open, one tap and it fills."
}
d["pulse"] = [pulse_new] + d.get("pulse", [])
d["pulse"] = d["pulse"][:15]

# --- feed prepend ---
feed_new = {
 "type":"activity","ts":TS,
 "text":"8:43a pre-market - heartbeat. Re-reconciled both books independently at the broker: LIVE flat $810.32 cash (zero positions/orders, nothing naked, 6th session, 0/3 day-trades); PAPER 6/6 GTC-stopped (AMD $490 / CEG $236 / NVDA $186 / OKLO $39 / SMR $7.50 / VRT $282), zero naked, equity ~$89.0k. First real 7/22 pre-market prints confirm the risk-off open - NVDA -1.3%, AMD -2.4%, MU -4.0%, VRT -3.2%; OKLO +1.7% the lone watchlist green on its DOE catalyst (pop_rank 1). QQQ ~$702 = ~-1.8% under its 20-day (softer than Tue's -0.8%). NVDA live ticket 2026-07-21-1 armed -> fires at the 9:30 open on approval. No pre-market execution by design (bad fills into a risk-off open before tonight's GOOGL/TSLA binary); NVDA re-entry + paper NVDA->nuclear trim run at the OPEN with real prices/stops."
}
d["feed"] = [feed_new] + d.get("feed", [])
d["feed"] = d["feed"][:40]

# --- latest_recap ---
d["latest_recap"] = "8:43a 7/22 pre-market (market CLOSED, opens 9:30) - heartbeat ~28 min on from the 8:15a run; plan unchanged. Both books re-reconciled clean at the broker: LIVE flat $810.32 cash (6th session, 0/3 day-trades) with NVDA live ticket 2026-07-21-1 (3 sh, marketable-limit $211, $186 stop) ARMED to fill at the 9:30 open - approve anytime, PDT-free swing; PAPER 6 names ALL GTC-stopped (AMD $490 / SMR $7.50 / OKLO $39 / VRT $282 / CEG $236 / NVDA $186), each clear of its stop, equity ~$89.0k ($16.4k cash). NEW THIS RUN: first real 7/22 pre-market prints are on the IEX feed (SIP block cleared) - chips giving back the 2-day rip (NVDA -1.3%, AMD -2.4%, MU -4.0%, VRT -3.2%) while OKLO +1.7% holds green on its confirmed Trump/DOE nuclear-for-AI catalyst -> chg_pct repopulated with live pre-market moves (was 0.0% at 8:15). Regime softened a touch pre-open: QQQ ~$702 = ~-1.8% under its $714.7 20-day (vs -0.8% at Tue's close) - 3x stays gated. Catalyst wall unchanged: GOOGL + TSLA + IBM + TXN + ServiceNow + AT&T after the close (Alphabet's AI-capex guide the key number). AT THE OPEN: fire NVDA live + trim the ~32%-of-book paper NVDA anchor toward the nuclear movers (OKLO/SMR/CEG) with real prices, NOT chasing the extended pop; no fresh semis into the binary. Grade running: pre-open (TBD). pop_rank 1 = OKLO."

# --- accountability (running, pre-open) ---
a = d["accountability"]
a["date"] = "2026-07-22"; a["final"] = False; a["grade"] = "TBD (pre-open)"
a["headline"] = "Pre-market (8:43a): heartbeat ~47 min from the open - both books re-reconciled clean (LIVE flat $810.32 cash, PAPER 6/6 GTC-stopped, zero naked). First real 7/22 pre-market prints confirm the 2-day semi rip is giving back (NVDA -1.3%, AMD -2.4%, MU -4.0%) while OKLO +1.7% holds green on its DOE nuclear-for-AI catalyst - vindicating the gate that keeps live out of 3x semis. QQQ ~$702 slipped to ~-1.8% under its 20-day (softer than Tue's -0.8%). Plan armed for the OPEN: fire the staged NVDA re-entry to end the 6-session cash camp, trim the paper NVDA anchor toward the nuclear movers, add NO fresh semi size into tonight's GOOGL/TSLA binary."
a["capture"] = {"bestName":"TBD - pre-open (OKLO leads the watchlist +1.7% on the confirmed DOE nuclear-for-AI catalyst)","bestPct":"-","capturedPct":"-","rate":"pre-open"}
a["missed"] = []
a["saved"] = [
 {"note":"Zero naked into the open - all 6 paper positions GTC-stopped (independently re-verified at the broker this run); live flat.","delta":"risk bounded"},
 {"note":"Gate keeping live OUT of 3x semis vindicated again pre-open - chips (NVDA/AMD/MU) giving back the 2-day rip; OKLO the lone green.","delta":"fade dodged"},
]
a["best"] = {"name":"-","note":"TBD (pre-open)","delta":"-"}
a["worst"] = {"name":"-","note":"TBD (pre-open)","delta":"-"}
a["applying"] = "Gate RE-ENTRY rule (7/21 lesson): 2 green sessions (7/20+7/21) + QQQ within ~1% of its 20-day + theme on a real, corroborated catalyst (nuclear-for-AI) -> re-enter the leader at the OPEN. Firing the staged NVDA swing ends the 6-session cash camp; the wide $186 stop bounds it."
a["adjust"] = "Weight to the MOVER not the anchor AND don't chase extension: at the open trim the ~32%-of-book paper NVDA anchor and redeploy into relative strength that ISN'T parabolic (OKLO green but already extended - buy a reclaim, not the high); keep live to the risk-managed NVDA core, no fresh semi size into tonight's GOOGL/TSLA binary."

# --- paper equity ---
d["paper"]["equity"] = 89020.31
d["paper"]["updated"] = TS
d["paper"]["equity_note"] = "Paper ~$89.0k (pre-market mark, -1.1% vs Tue's $89,976 close) - chips giving back the 2-day rip (NVDA/AMD/VRT/MU soft) partly offset by OKLO's +1.7% DOE nuclear catalyst; 6/6 GTC-stopped, zero naked."

# --- atomic write ---
fd, tmp = tempfile.mkstemp(dir=SITE, suffix=".tmp")
with os.fdopen(fd, "w") as fh:
    json.dump(d, fh, indent=1, ensure_ascii=False)
os.replace(tmp, F)
print("WROTE", F)
