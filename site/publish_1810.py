import json, os, tempfile

path = "engine-data.json"
with open(path) as f:
    d = json.load(f)

new_pulse = {
    "ts": "2026-07-21T18:10:00-04:00",
    "text": "6:10p after-hours heartbeat - grade stays final D+ (not re-graded), tomorrow's plan unchanged. 3rd evening verify, both books == broker: LIVE flat $810.32 cash / 0 positions / nothing naked (6th straight session); PAPER 6 names all GTC-stopped (AMD $490 / SMR $7.50 / OKLO $39 / VRT $282 / CEG $236 / NVDA $186), zero naked, equity ~$90.5k (+0.95%). Checked the AH news: today's memory-led semi rip reads as a hedge-fund-de-risking WASHOUT now reversing (MU +12%, SanDisk +14%, DRAM ETF +12%), and SMCI popped after-hours on a rising order backlog - all theme tailwinds, nothing dents the NVDA thesis. NVDA sits ~$207 AH, right at the swing entry. No trade (post-close/illiquid, one-core rule, and I won't add beta right before Wed's GOOGL+TSLA+IBM after-close binary wall). NVDA live ticket 2026-07-21-1 stays armed for the 7/22 open - the gate re-entry.",
    "hype": "Late check - all stops good, nothing naked, and NVDA's holding right where tomorrow's buy fires. Today's chip pop looks like real re-buying, not a head-fake, so the open swing's still on."
}
d["pulse"].insert(0, new_pulse)
d["pulse"] = d["pulse"][:15]

new_feed = {
    "type": "activity",
    "ts": "2026-07-21T18:10:00-04:00",
    "text": "6:10pm evening heartbeat - books verified clean a 3rd time (LIVE flat $810 cash, nothing naked; PAPER 6/6 GTC-stopped, zero naked). AH news confirms the semi rip is a positioning-washout reversal - SMCI popped after-hours on a rising backlog; nothing dents the NVDA thesis. No trade (post-close, don't add beta into Wed's GOOGL/TSLA/IBM binary). NVDA swing stays armed for the 7/22 open."
}
d["feed"].insert(0, new_feed)

d["latest_recap"] = ("6:10p 7/21 after-hours heartbeat (market CLOSED, next open 7/22 09:30) - verify-and-hold ~27 min on from the 5:43 run; grade stays final:true D+ (NOT re-graded). 3rd independent broker re-check of the evening, both books == broker: LIVE flat $810.32 cash, 0 positions/orders (nothing naked, 6th straight cash session); PAPER 6 names ALL GTC-stopped + verified (AMD $490 / SMR $7.50 / OKLO $39 / VRT $282 / CEG $236 / NVDA $186), zero naked, each clear of its stop, equity $90,465.70 (+0.95% vs prior close $89,617.78). Fresh get_news + web-search: today's +8-15% memory-led semi rebound reads as a hedge-fund-de-risking WASHOUT now reversing (MU +12.0% $970, SanDisk +14%, Roundhill DRAM ETF +12%, Nasdaq-100 +1.9% past 29,000, SMH +5.2%, S&P record $748), and SMCI jumped after-hours on a rising order backlog = theme tailwind. NO adverse NVDA news (mkt cap $5.01T; Nebius 9.3% stake + Micron HBM read-through intact). NVDA ~$207 AH = right at the swing entry. Wed 7/22 binary wall CONFIRMED: GOOGL + TSLA + IBM all report after the close (options imply ~5.9% TSLA / ~5.4% IBM) and AMD 'Advancing AI 2026' runs Wed daytime (MI355X/MI400) - AMD = tomorrow's pop_rank-1 (owned in paper; NOT chased live at +8% extended). Gate still shut: QQQ $708.8 ~0.8% under its $714.7 20-day, ~$16k 3x powder parked for a confirmed reclaim past Wed's prints. NO trade this run (post-close, illiquid AH, one-core rule, don't add beta into the binary). NVDA live swing ticket 2026-07-21-1 (3 sh, $211 marketable limit, $186 GTC stop) stays armed + pinged for the 7/22 open - the gate re-entry. Published engine-data.json only (no data.json, no git). Backup engine-data.backup-2026-07-21-1810.json.")

d["updated"] = "2026-07-21T18:10:00-04:00"

# atomic write: temp file in same dir -> os.replace
fd, tmp = tempfile.mkstemp(dir=".", prefix=".engine-data-tmp-", suffix=".json")
with os.fdopen(fd, "w") as f:
    json.dump(d, f, indent=1, ensure_ascii=True)
os.replace(tmp, path)

# verify read-back
with open(path) as f:
    v = json.load(f)
assert v["updated"] == "2026-07-21T18:10:00-04:00", "updated mismatch"
assert v["accountability"]["final"] is True and v["accountability"]["grade"] == "D+", "grade changed!"
assert [t["symbol"] for t in v["pending_tickets"]] == ["NVDA"], "pending changed!"
assert v["pulse"][0]["ts"] == "2026-07-21T18:10:00-04:00", "pulse not prepended"
assert v["feed"][0]["ts"] == "2026-07-21T18:10:00-04:00", "feed not prepended"
print("VERIFIED OK | updated", v["updated"], "| grade", v["accountability"]["grade"], "final", v["accountability"]["final"],
      "| pending", [t["symbol"] for t in v["pending_tickets"]],
      "| pulse0", v["pulse"][0]["ts"], "len", len(v["pulse"]),
      "| feed0", v["feed"][0]["ts"], "len", len(v["feed"]),
      "| coverage", len(v["coverage"]))
