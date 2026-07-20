import json, os, shutil, tempfile

P = "engine-data.json"
TS = "2026-07-20T13:15:00-04:00"
d = json.load(open(P))

# ---------- fresh market data (1:11pm ET pull) ----------
chg = {"NVDA":0.3,"AMD":2.7,"SOXL":4.7,"VRT":1.4,"SQQQ":-1.9,"INTC":3.7,"PLTR":1.4,
       "CEG":0.9,"TQQQ":1.8,"FNGU":3.7,"SOXS":-5.1,"IONQ":0.4,"TSLA":-2.2,"RKLB":-1.5,"BE":-5.9}
proj = {
 "SQQQ":(0.5,"med","failed chip pop fades into the close (proven ASML/TSMC pattern); held paper - IN the call",1),
 "PLTR":(2.3,"med","AI-software RS leader holding its highs while chips fade; not chip-derate exposed",2),
 "NVDA":(0.8,"med","1x AI bellwether - RS but capped under the 20-day; GOOGL/TSLA Wed",3),
 "INTC":(4.0,"med","Q2 earnings this week + Google Cloud AI deal; holding its gains best",4),
 "AMD":(2.7,"low","MSFT/Helios deal but extended off the +5% open",5),
 "SOXL":(4.7,"low","biggest raw mover but GATED 3x under the 20-day",6),
 "VRT":(2.0,"low","AI-power capex; faded from +4%, reports 7/29",7),
 "CEG":(1.0,"low","AI-power anchor, held paper",8),
 "TQQQ":(1.8,"low","gated 3x Nasdaq",9),
 "FNGU":(3.7,"low","gated 3x FANG bounce",10),
 "IONQ":(0.7,"low","quantum beta, lagging the semis",11),
 "SOXS":(-4.5,"low","inverse semis - pops only if chips finally roll red",12),
 "RKLB":(-1.0,"low","cut the paper laggard; red on a bounce day",13),
 "TSLA":(-1.5,"med","red into Wed earnings",14),
 "BE":(-5.5,"high","short-attacked, fresh 90-day lows, cutting the camp",15),
}
# light text refresh for the key held/cut names
refresh_thesis = {
 "NVDA":"**Held in paper (90 sh @ $209.23, $186 GTC stop) - the book's gate-compliant 1x way to own the AI tape.** NVDA faded to ~flat (+0.3%) with the broader semi pop but holds relative strength above $203; it's where freed live cash + paper powder go FIRST on a confirmed QQQ $716 reclaim. Alphabet + hyperscaler earnings Wed are the AI-capex read. Not adding here under the 20-day - own it 1x, don't lever it.",
 "PLTR":"**Held in paper (50 sh @ $135.22, $121.50 GTC stop) - the cleanest AI-SOFTWARE relative-strength leader.** PLTR is +1.4% and holding its highs while the chip complex fades - it isn't exposed to the semi derate that broke QQQ, so it's the RS tell and a redeploy magnet on a $716 reclaim. Wide stop below structure; add on confirmation, not into the chop.",
 "SQQQ":"**Held in paper (310 sh @ $42.36, $38 GTC stop) - the deliberate sub-20-day / Iran hedge.** It bleeds (-1.9%) while the tape is green but is recovering off its low as the chip pop fades; it's the largest single conviction position because the base case is the failed bounce rolls over into the close. Press it on a confirmed QQQ $698 break; cut it fast on a $716 reclaim.",
 "BE":"**Cutting (live 3 sh @ $222.64, $188 GTC stop; sell ticket 2026-07-20-1 staged for the tap).** BE printed fresh 90-day lows ($195.22) and its $195->$204 bounce already failed back to ~$202 on a day semis were GREEN - it can't hold a bid with its group. Fundamentals are strong (Q1 blowout, $25B Brookfield deal, 7/28 earnings) but a $188 stop can't protect a binary 7/28 gap, and this is an accidental all-in from a top-tick entry, not a sized catalyst bet. Cut frees ~$607 to concentrate on confirmation; keeps the option to re-enter with defined risk near 7/28.",
}
refresh_hold = {
 "NVDA":"NVDA is the cleanest 1x way to own the AI-compute tape and has no near-term earnings binary (late-Aug), so it's the account's redeploy magnet. We hold 90 paper shares behind a wide $186 GTC stop. We add the rest on a QQQ $716 reclaim and would trim if it loses ~$198 or the AI-capex story cracks.",
 "PLTR":"PLTR is our AI-software relative-strength anchor - it's green and holding highs while the chips fade, which is exactly the tell we watch. We hold 50 paper shares behind a wide $121.50 GTC stop. We'd add on a QQQ $716 reclaim and only sell if it loses its rising shelf.",
 "SQQQ":"SQQQ is the intentional hedge that lets the paper book lean short while QQQ sits under its 20-day with Iran headline risk. We hold 310 paper shares behind a $38 GTC stop. It drags on green days by design; we press it if QQQ loses $698 and cut it fast on a $716 reclaim.",
 "CEG":"CEG is our AI-power/nuclear anchor - a lower-beta way to own the datacenter-demand theme. We hold 16 paper shares behind a $236 GTC stop. We hold it as ballast and would only sell on a clean break of that stop.",
}

# ---------- coverage ----------
for c in d.get("coverage", []):
    t = c.get("ticker")
    if t in chg: c["chg_pct"] = chg[t]
    if t in proj:
        tp,cf,ba,pr = proj[t]
        c["projection"] = {"target_pct":tp,"confidence":cf,"basis":ba,"pop_rank":pr}
    if t in refresh_thesis: c["thesis"] = refresh_thesis[t]
    if t in refresh_hold: c["hold_reason"] = refresh_hold[t]
    c["updated"] = TS
# NVDA size_note is stale ("added +20 today") - keep size, clear the note to today's truth
for c in d.get("coverage", []):
    if c.get("ticker")=="NVDA":
        c["size"]="$18.3k paper (90 sh)"; c["size_pct"]="~20% paper"; c["size_note"]="held; adds on a $716 reclaim"; c["plan_usd"]="add the rest on a QQQ $716 reclaim"

# ---------- pulse ----------
pulse_text = ("1:15pm: The morning chip pop kept fading - SOXL round-tripped from +10% to +4.7%, AMD +5%->+2.7%, "
 "and QQQ slid back to ~$700 near its day low, still ~2.4% under its 20-day ($717), while SPY sits near record highs "
 "(so the weakness stays chip-specific). Gate stays SHUT. Held both books unchanged: the BE-cut ticket is still staged "
 "for your tap (frees ~$607), paper's 4 names + the SQQQ hedge are all stopped, and live $201 + paper ~$47k stay dry. "
 "I did NOT add to the hedge into $698 support that's held 3x today with SPY at highs - that's shorting an unconfirmed "
 "break. Waiting for a real $698 break (press the fade) or a $716 reclaim (flip long into PLTR/NVDA/VRT). "
 "5/5 stops verified, zero naked. Live day-trade budget 0/3.")
pulse_hype = ("Chips faded even more and the Nasdaq slid back near its lows, but it's holding a line that SPY's record highs "
 "keep defending - so I'm not shorting into it or chasing the leveraged names. Holding steady with the hedge on, Bloom's "
 "still queued to cut, and I move the second it breaks either way.")
d["pulse"] = [{"ts":TS,"text":pulse_text,"hype":pulse_hype}] + d.get("pulse",[])
d["pulse"] = d["pulse"][:15]

# ---------- status ----------
d["status"] = [
 {"session":"Morning","text":"QQQ held $698, bounced; gate ON"},
 {"session":"Afternoon","text":"Chip pop fades; held light, dry"},
]

# ---------- headlines ----------
d["headlines"] = [
 "Nasdaq slides back to ~$700 (+0.7%), near its day low and ~2.4% under its 20-day; SPY near record highs - a chip-specific derate",
 "The morning chip pop keeps fading (SOXL +10%->+4.7%, AMD +5%->+2.7%) - the same 'sell-by-lunch' pattern as ASML/TSMC last week",
 "AMD +2.7% on the expanded Microsoft/Helios deal - off its +5% open high",
 "Intel +3.7% on Q2 earnings this week + a Google Cloud AI partnership - holding its gains best",
 "Inverses recover off the lows (SQQQ -3.5%->-1.9%, SOXS off -11%) as the bounce fades",
 "US airstrikes on Iran, a service member killed - but oil eases to ~$81 on diplomacy hopes",
 "Big-tech earnings week: GOOGL, TSLA, INTC, TXN report Wed-Thu; VRT 7/29, BE 7/28",
 "Record $46B into semiconductor ETFs in 2026 as the AI-capex bid persists",
]

# ---------- feed (prepend activity) ----------
feed_item = {"ts":TS,"type":"activity","text":(
 "1:15pm reconcile: chip pop fading further (SOXL +10%->+4.7%), QQQ back near its $698 day low, still ~2.4% under its "
 "20-day - gate ON. Held both books unchanged; did NOT short into thrice-held $698 support with SPY at record highs. "
 "BE-cut ticket still staged; 5/5 stops verified, zero naked; live $201 + paper ~$47k dry for a confirmed $698 break or $716 reclaim.")}
d["feed"] = [feed_item] + d.get("feed",[])
d["feed"] = d["feed"][:40]

# ---------- score ----------
d["score"] = {"alphaPts":"-12.9","benchmark":"-6.3%","bestDay":"+3.2%",
 "bestDayName":"Day 9 - CPI chip rally (settled)","winRate":"40%","tradeCount":5}

# ---------- accountability (running) ----------
d["accountability"] = {
 "date":"2026-07-20","final":False,"grade":"C (running)",
 "headline":("Both books flat/red on a green tape that is FADING - SOXL round-tripped +10%->+4.7%, QQQ slid back to its "
  "$698 day low under the 20-day, exactly the 'chip pop sells by lunch' pattern the gate is built for, so the wait keeps "
  "being validated. Live's red is the broken BE camp (cut staged for the tap); paper's is the deliberate SQQQ hedge. No "
  "new trade - I won't short into $698 support that's held 3x today with SPY at record highs (unconfirmed break), and I "
  "won't chase the gated 3x semis. Powder dry for a confirmed break either way."),
 "capture":{"bestName":"SOXL","bestPct":"+4.7% (3x - GATED)","capturedPct":"live -4.5% / paper -1.0%",
  "rate":("low/negative - best OWNABLE, non-extended mover was INTC +3.7% (Q2 earnings, not held) / SMR +3.2%; best held "
   "was PLTR +1.4% (paper). Biggest raw movers (SOXL +4.7%, FNGU +3.7%, TQQQ +1.8%) are gated 3x under the 20-day, correctly skipped.")},
 "missed":[
  {"from":"cash","to":"INTC (Q2 earnings + Google Cloud)","note":("INTC +3.7% on its earnings/Google-Cloud catalyst was a "
    "real ownable 1x name on our board - a sharper open catches it on the news; buying now (already run, +3.7%) would repeat "
    "the 7/17 top-tick mistake, so it's a logged miss, not a should-still-buy."),"delta":"~+$150 on a modest slug, had we caught the open"},
  {"from":"n/a","to":"SOXL +4.7% / FNGU +3.7% / TQQQ +1.8%","note":"the biggest raw movers, but GATED 3x under the 20-day - not chased by design (Earned Rule #1)","delta":"low-capture cost, accepted"}],
 "saved":[
  {"note":"Held the regime gate - no chase of the gated 3x semis into a sub-20-day, Iran-clouded tape that keeps fading its open pop","delta":"avoided the week's #1 mistake"},
  {"note":"Did NOT add short into $698 support that has held 3x today with SPY at record highs - anticipating an unconfirmed break is the whipsaw trap","delta":"discipline > churn"},
  {"note":"BE cut staged (paper already cut @ $196.68) - its $195->$204 bounce failing back on a green semi day confirms sellers own it; a $188 stop can't protect a 7/28 gap","delta":"de-risks the camp"}],
 "best":{"name":"PLTR (paper, held)","note":"+1.4%, the cleanest AI-software RS leader holding its highs while the semis faded - the relative-strength tell","delta":"the RS anchor"},
 "worst":{"name":"BE (cutting)","note":"-5.9% to fresh 90-day lows, can't bounce with the +4.7% semis; strong fundamentals but a broken chart into a binary 7/28","delta":"-$38 live today"},
 "applying":("Regime gate (QQQ ~2.4% under its 20-day -> no leveraged/chip chase) + 'deploy on CONFIRMED, not anticipated' "
  "(don't short thrice-held $698 support) + PLAYBOOK Rule #2 (a $188 stop can't protect a binary 7/28 BE gap -> cut the camp)."),
 "adjust":("Hair-trigger both ways on CONFIRMATION: QQQ loses $698 on volume -> press the fade (paper SOXS/SQQQ; arm a small "
  "live SQQQ once the BE cut frees cash); QQQ reclaims/holds $716 -> cut SQQQ fast + fire freed live cash + paper powder into "
  "the confirmed 1x leader (PLTR/NVDA/VRT). If this week's capture stays ~0 despite obeying the gate, trigger the PLAYBOOK "
  "escalation clause - the problem is the APPROACH (revisit a small structural live inverse), not the sizing.")
}

# ---------- pending_tickets ----------
d["pending_tickets"] = [{
 "id":"2026-07-20-1","symbol":"BE","side":"sell","size":"$607","qty":3,
 "entry":"~$202 market sell-to-close (approve = sell now)","trigger":None,"stop":None,
 "bracket":"n/a - sell-to-close; the fast-lane cancels the $188 GTC stop (b2b62cc5) first, then sells",
 "thesis":("Cut the short-attacked BE - it's the whole live directional book from a bad top-tick entry ($222.64), printing "
  "fresh 90-day lows and unable to hold a bounce ($195->$204 already failed back to $202) on a GREEN semi day. Frees ~$607 to "
  "reset the live book cash-ready for the confirmed 1x leader (PLTR/NVDA/VRT) on a QQQ $716 reclaim, or a small live SQQQ if "
  "QQQ breaks $698. A $188 stop can't protect a binary 7/28 earnings gap; cutting keeps the option to re-enter with defined "
  "risk later. Paper already cut @ $196.68. This is a multi-day exit - it does NOT burn PDT day-trade budget (0/3).")
}]

# ---------- live / paper equity ----------
live = d.setdefault("live",{})
live["equity"]=807.88; live["cash"]=201.26; live["updated"]=TS
live["equity_note"]=("Live -4.5% today (~$808). BE still -5.9% to fresh 90-day lows (~$202) on a green semi day - can't "
 "bounce with its group; $188 GTC stop live, BE-cut ticket staged for your tap. $201 cash dry. -19.2% since $1,000 inception.")
for pt in live.get("equity_curve",[]):
    if pt.get("date")=="Jul 20": pt["value"]=807.88
if isinstance(live.get("positions"),list):
    for p in live["positions"]:
        if isinstance(p,dict) and p.get("symbol")=="BE":
            p["current_price"]=202.33; p["chg_pct"]=-5.9; p["unrealized_pl"]=-60.93

paper = d.setdefault("paper",{})
paper["equity"]=89489.28; paper["updated"]=TS
paper["equity_note"]=("Paper -1.0% today - PLTR/CEG/NVDA green, but the 310-sh SQQQ hedge (-1.9%) is the deliberate "
 "sub-20-day/Iran drag on a green tape. 4 names all GTC-stopped, zero naked; ~$47k (~53%) powder held for a confirmed $698 "
 "break (press the fade) or $716 reclaim (flip long). No new trade this run - not shorting into thrice-held support.")
for pt in paper.get("equity_curve",[]):
    if pt.get("date")=="Jul 20": pt["value"]=89489.28

# ---------- activity log (detailed) ----------
act_title = ("Mon 7/20 ~1:15pm ET, REGULAR HOURS (~2h45 to close). Fresh reconcile of BOTH books vs the broker + a regime "
 "re-pull. NO fills since Friday; the live BE-sell ticket (2026-07-20-1, 3 sh, marketable-limit $190) is staged and still "
 "unapproved. REGIME: QQQ ~$699.8 (+0.7%) slid back toward its $698 day low, still ~2.4% under its ~$717 20-day (no reclaim, "
 "gate SHUT); the morning chip pop keeps fading (SOXL +10%->+4.7%, AMD +5%->+2.7%, NVDA +0.3%); SPY ~$744 near record highs so "
 "the weakness stays chip-specific; inverses recovering off the lows (SQQQ -1.9% from -3.5%). DECISION: HOLD both books - no "
 "new trade. Kept the BE-cut staged (frees ~$607); did NOT add short into $698 support that has held 3x today with SPY at "
 "highs (unconfirmed break = the anticipation/whipsaw trap); did NOT chase the gated 3x semis. Live $201 + paper ~$47k held as "
 "dry powder. 5/5 positions (BE live $188; paper NVDA $186, SQQQ $38, CEG $236, PLTR $121.50) carry a live GTC stop - zero "
 "naked. Grade C running - honest low/negative capture (BE camp + SQQQ drag on a green day), but the fade is validating the "
 "gate; the binary test is live this week. Projection pop_rank 1 -> SQQQ (fade-into-close, held). Score alpha -12.9 vs TQQQ "
 "-6.3% since 7/2. Day-trade 0/3. Published engine-data.json only (no data.json, no git). Backup engine-data.backup-2026-07-20-1315.json.")
if isinstance(d.get("activity"),list):
    d["activity"] = [{"ts":TS,"kind":"engine","title":act_title}] + d["activity"]
    d["activity"] = d["activity"][:30]

# ---------- timestamp ----------
d["updated"] = TS

# ---------- atomic write + backup ----------
shutil.copyfile(P, "engine-data.backup-2026-07-20-1315.json")
fd, tmp = tempfile.mkstemp(dir=".", prefix=".ed_", suffix=".json")
with os.fdopen(fd,"w") as f:
    json.dump(d, f, ensure_ascii=False, indent=1)
os.replace(tmp, P)

# ---------- verify ----------
v = json.load(open(P))
assert v["updated"]==TS
assert v["pulse"][0]["ts"]==TS and len(v["pulse"])<=15
ones=[c["ticker"] for c in v["coverage"] if c.get("projection",{}).get("pop_rank")==1]
assert ones==["SQQQ"], ones
assert v["pending_tickets"][0]["id"]=="2026-07-20-1"
assert v["score"]["alphaPts"]=="-12.9"
assert v["accountability"]["date"]=="2026-07-20"
print("PUBLISH-1315-OK | pulse=%d feed=%d coverage=%d pop1=%s | live=%.2f paper=%.2f | alpha=%s bench=%s"%(
 len(v["pulse"]),len(v["feed"]),len(v["coverage"]),ones[0],v["live"]["equity"],v["paper"]["equity"],
 v["score"]["alphaPts"],v["score"]["benchmark"]))
