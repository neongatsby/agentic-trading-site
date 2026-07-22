import json, os, tempfile

P = "engine-data.json"
d = json.load(open(P))
TS = "2026-07-22T13:22:00-04:00"

pulse_text = ("1:22p - Held the book into tonight's GOOGL/TSLA/IBM/TXN capex binary; nothing to chase 35 min "
  "after the last trail. Paper cooled with the tape (+0.86% now vs +1.3% midday) as NVDA/AMD eased off their "
  "highs pre-print - all 6 names stay GTC-stopped near breakeven (capped downside), ~21% ($19k) powder kept DRY "
  "to deploy into the confirmed post-binary direction (not into a coin-flip with oil +4% on the Iran overhang). "
  "Verified the OKLO/DOE nuclear-for-AI catalyst is live (Bloomberg 7/21) and refreshed the live one-tap at the "
  "$44.6 base - the binary-insulated way to finally end a 7th session of live cash. Honest: we own the day's "
  "leaders (CEG +3.9% new highs, NVDA +3.2%, RKLB +3.8%) but the blend trails the best held mover and live's "
  "still 0% in cash - C+ running, 0/3 day-trades.")
pulse_hype = ("Sitting tight before Google/Tesla earnings tonight - our stuff's up and stop-protected, and I'm "
  "keeping a fifth of the paper account in cash to pounce once it breaks. Live's still in cash (7th day, annoying) "
  "but the OKLO one-tap's refreshed at the base - the nuclear name tonight's print won't whipsaw.")
d["pulse"] = [{"ts": TS, "text": pulse_text, "hype": pulse_hype}] + d.get("pulse", [])[:15]

d["status"] = [
  {"session": "Morning", "text": "Rotated laggard into RKLB mover"},
  {"session": "Afternoon", "text": "Held; powder dry into tonight's binary"},
]

d["headlines"] = [
  "Mega-cap capex test tonight: GOOGL + TSLA (plus IBM, TXN) after the close - the season's biggest AI-spend read",
  "Risk-off overhang: oil +4% as US strikes Iran an 11th night; Nasdaq futures slipped into the print",
  "OKLO/X-Energy formally in the Trump/DOE $200M nuclear-for-AI program (MSFT/NVDA) - Bloomberg-confirmed; DOE summit the catalyst window",
  "Nuclear-for-AI leadership = CEG +3.9% at new highs; OKLO coils on its $44.6 base into the DOE catalyst",
  "Semis stay bid but cool pre-binary: NVDA +3.2%, AMD +2.4%, SOXL +4.3%",
  "SMCI holds a +23% moonshot on a record AI-server order haul + margin guide-up",
  "RKLB +3.8% holds its $266M Space Force win; space/defense RS firm",
  "Extended high-beta rolls over: PLTR -5.3%, SOFI -2.9% as money rotates to catalyst names",
]

proj = {
  "OKLO": {"chg": "+1.1%", "t": 3.5,  "c": "med", "b": "DOE nuclear-for-AI catalyst window open; coiled on base, binary-insulated", "r": 1, "path": [1.1, 2.3, 3.5]},
  "CEG":  {"chg": "+3.9%", "t": 4.5,  "c": "med", "b": "nuclear-for-AI RS leader breaking to new highs", "r": 2, "path": [3.9, 4.2, 4.5]},
  "NVDA": {"chg": "+3.2%", "t": 3.5,  "c": "low", "b": "AI leader but hostage to tonight's GOOGL capex read", "r": 3},
  "RKLB": {"chg": "+3.8%", "t": 4.0,  "c": "med", "b": "space/defense RS; $266M Space Force win", "r": 4},
  "AMD":  {"chg": "+2.4%", "t": 2.5,  "c": "low", "b": "semis bid but cooling pre-binary; own print 8/4", "r": 5},
  "SMCI": {"chg": "+23.4%","t": 22.0, "c": "low", "b": "+23% AI-server gap already run; don't chase into binary", "r": 6},
  "SMR":  {"chg": "-0.8%", "t": 0.5,  "c": "low", "b": "small-reactor laggard; could catch DOE-summit sympathy", "r": 7},
  "SOXL": {"chg": "+4.3%", "t": 4.0,  "c": "low", "b": "3x semis - regime-gated, round-trips in chop", "r": 8},
  "IONQ": {"chg": "+0.4%", "t": 0.5,  "c": "low", "b": "quantum beta, quiet ahead of the binary", "r": 9},
  "RGTI": {"chg": "+1.1%", "t": 1.0,  "c": "low", "b": "quantum beta, mild bid", "r": 10},
  "TSLA": {"chg": "-0.2%", "t": -0.5, "c": "low", "b": "reports tonight - binary; drifting into the print", "r": 11},
  "VRT":  {"chg": "-1.1%", "t": -1.0, "c": "low", "b": "AI-power infra soft; sold from paper into RKLB", "r": 12},
  "SOFI": {"chg": "-2.9%", "t": -3.0, "c": "low", "b": "high-beta fintech rolling over", "r": 13},
  "PLTR": {"chg": "-5.3%", "t": -5.5, "c": "med", "b": "extended, rolling over hard - worst watchlist name", "r": 14},
}
for c in d.get("coverage", []):
    t = c.get("ticker")
    if t in proj:
        p = proj[t]
        c["chg_pct"] = p["chg"]
        np = {"target_pct": p["t"], "confidence": p["c"], "basis": p["b"], "pop_rank": p["r"]}
        if "path" in p: np["path_pct"] = p["path"]
        c["projection"] = np
        c["updated"] = TS

for c in d.get("coverage", []):
    if c.get("ticker") == "OKLO":
        c["verdict"] = "buy"
        c["verdict_label"] = "Buy - live armed one-tap + paper held"
        c["thesis"] = ("**pop_rank 1 as the binary-insulated catalyst swing** - OKLO+X-Energy are formally in the "
          "Trump/DOE $200M program to fast-track advanced reactors for AI data centers (MSFT/NVDA partners), "
          "Bloomberg-confirmed 7/21, with the DOE AI-energy-summit program detail the open catalyst window. "
          "Spiked to $47.48, faded to ~$44.6 and has held the $44.4-44.9 base all session (the lower-risk entry, "
          "not a chase). No own earnings to Aug 18 = it does NOT ride tonight's GOOGL/TSLA capex binary.")
        c["hold_reason"] = ("Small nuclear-reactor company just formally named into the Trump/DOE $200M program to "
          "power AI data centers alongside Microsoft and Nvidia - that government catalyst is what we bought. Paper "
          "owns 300 sh near $44.6 (stop $43) and there's a live one-tap ticket, refreshed at the base, to finally "
          "get the real account in too. It ran +7.6% this morning then gave it back; we hold through the DOE "
          "catalyst window and cut it only if $43/$39 breaks or the summit clearly disappoints.")
        c["size"] = "$13.4k (300 sh paper)"
        c["size_pct"] = 14.7
        c["size_note"] = "pop_rank-1 catalyst swing; paper stop $43; live armed one-tap (stop $39)"
        c["plan_usd"] = "$715 live (armed $48 limit, one tap) / 300 sh paper held"
        c["horizon"] = "swing (multi-day)"

feed_item = {"type": "activity", "ts": TS, "text": (
  "1:22p - HOLD & VERIFY (no churn into tonight's GOOGL/TSLA/IBM/TXN binary): all 6 paper names GTC-stopped near "
  "breakeven (capped downside), ~21% ($19k) powder DRY for the confirmed post-print direction - not pre-positioned "
  "into a coin-flip with oil +4% on Iran. Verified the OKLO/DOE nuclear-for-AI catalyst live (Bloomberg) + refreshed "
  "the live one-tap at the $44.6 base. Paper +0.86%, live flat cash (7th session = the real drag). 0/3 day-trades.")}
d["feed"] = [feed_item] + d.get("feed", [])[:60]

d["accountability"] = {
  "date": "2026-07-22", "final": False, "grade": "C+ (running, ~2.7h to close)",
  "headline": ("Own the day's leaders - CEG/NVDA/RKLB - but paper cooled to +0.86% as the tape de-risked into "
    "tonight's GOOGL/TSLA binary, and LIVE flat cash a 7th session is still the single biggest drag. The OKLO "
    "one-tap is refreshed and live at the base; ~21% paper powder kept DRY for the confirmed post-print move."),
  "capture": {"bestName": "CEG +3.9% (HELD)", "bestPct": "+3.9%", "capturedPct": "paper +0.86% / live flat",
    "rate": "~22% - own the right leaders but the blend is dragged by flat OKLO/SMR + RKLB's top-tick entry; LIVE cash is the real 0% drag"},
  "missed": [{"from": "live cash", "to": "OKLO", "note": "LIVE flat a 7th session; the refreshed OKLO one-tap on a live DOE catalyst is the capture gap", "delta": "needs the tap"}],
  "saved": [
    {"note": "Kept ~21% paper powder DRY rather than pre-position into tonight's coin-flip GOOGL/TSLA binary with oil +4% on the Iran overhang", "delta": "coin-flip dodged"},
    {"note": "Trailed AMD/NVDA/CEG stops to ~breakeven - capped the downside into the binary while keeping the upside", "delta": "gains protected"},
    {"note": "Did NOT chase SMCI's +23% gap into the binary", "delta": "chase dodged"}],
  "avoided": {"worstName": "PLTR", "worstPct": "-5.3%", "note": "PLTR the worst watchlist name (-5.3%, extended, rolling over) alongside SOFI -2.9%; hold none, dodged both", "amount": "none held", "rate": "100% dodged"},
  "best": {"name": "CEG", "note": "nuclear-for-AI RS leader at new highs, held not watched; stop trailed to lock the gain", "delta": "+3.9%"},
  "worst": {"name": "RKLB", "note": "bought the mover near the top tick this morning - right name, entry a touch high (position -1.2% though the stock is +3.8% today)", "delta": "-$109 unrealized"},
  "applying": "Weight to the MOVER + own the biggest name you're tracking (7/21) - we own CEG/NVDA/RKLB, today's movers.",
  "adjust": "Two levers: (1) keep the OKLO one-tap loud + at the base to end the LIVE cash camp; (2) deploy the 21% paper powder AFTER tonight's binary into the confirmed direction - don't pre-position into the coin-flip; scale any add near VWAP, not the top tick (the RKLB ding).",
}

d["score"] = {"alphaPts": "-16.4", "benchmark": "-2.6%", "bestDay": "+3.2%", "bestDayName": "Jul 14 - CPI chip rally (settled)", "winRate": "33%", "tradeCount": 6}

paper = d.get("paper", {})
paper["equity"] = 90751.37; paper["updated"] = TS
paper["equity_note"] = ("Paper $90,751 (+0.86% intraday; cooled from +1.3% midday as NVDA/AMD eased off highs pre-binary). "
  "6 names (AMD/CEG/NVDA/OKLO/RKLB/SMR) all GTC-stopped near breakeven, zero naked; ~21% ($19k) cash held DRY for the confirmed post-binary deploy.")
ec = paper.get("equity_curve", [])
if ec and ec[-1].get("date") == "Jul 22": ec[-1]["value"] = 90751.37
else: ec.append({"date": "Jul 22", "value": 90751.37})
paper["equity_curve"] = ec; d["paper"] = paper

live = d.get("live", {})
live["equity"] = 810.32; live["updated"] = TS
live["equity_note"] = ("Live $810.32, 100% cash a 7th straight session (-19.0% since $1,000 inception) - the real capture drag. "
  "Zero positions/orders, nothing naked, 0/3 day-trades used. OKLO one-tap refreshed at the $44.6 base (16 sh, $48 limit, $39 GTC stop) = the binary-insulated way to finally get working.")
lec = live.get("equity_curve", [])
if lec and lec[-1].get("date") == "Jul 22": lec[-1]["value"] = 810.32
else: lec.append({"date": "Jul 22", "value": 810.32})
live["equity_curve"] = lec; d["live"] = live

d["pending_tickets"] = [{
  "id": "2026-07-22-1", "symbol": "OKLO", "side": "buy", "size": "$715", "qty": 16,
  "entry": ("1:20pm ET - OKLO coiled on its $44.6 base (+1.1%), having faded the morning $47.48 spike and held the "
    "$44.4-44.9 shelf all session. Approve ANYTIME -> the $48 marketable limit fills near the money (~$44.6), the "
    "low-risk base entry (16x$48=$768 reserve < $810 BP, won't reject). Multi-day swing, PDT-free (0/3 day-trades)."),
  "trigger": None, "stop": 39.0,
  "bracket": "stop $39 GTC (below the $40-41 base / 7/17 $39.53 low, ~-13% from ~$44.6)",
  "thesis": ("Ends a 7th session of live cash by owning the nuclear-for-AI name on a live, Bloomberg-confirmed DOE "
    "$200M catalyst (OKLO+X-Energy w/ MSFT/NVDA) INSULATED from tonight's GOOGL/TSLA capex binary - no own earnings "
    "to Aug 18. Coiled on the base = the lower-risk entry. 25-analyst PT ~$86 (~90% upside). Wide $39 stop (~$90 max risk). Paper owns 300 sh, stop $43."),
}]

d["updated"] = TS

fd, tmp = tempfile.mkstemp(dir=".", prefix=".engine-data-", suffix=".tmp")
with os.fdopen(fd, "w") as f:
    json.dump(d, f, ensure_ascii=False, indent=1)
os.replace(tmp, P)
print("WROTE", P)
