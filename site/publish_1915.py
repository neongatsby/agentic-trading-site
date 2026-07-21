import json, os

SRC = 'engine-data.json'
d = json.load(open(SRC))

TS = "2026-07-21T19:15:00-04:00"

# --- top-level updated ---
d['updated'] = TS

# --- pulse: prepend one, keep 15 ---
pulse_text = ("7:15p after-hours heartbeat - independently re-verified both books at the broker; "
 "nothing changed since the 6:43p check. LIVE flat $810.32 cash (6th session, nothing naked); "
 "PAPER's 6 names all green and all GTC-stopped, zero naked. Confirmed the settled close (S&P +0.89% "
 "to a record 7,509; Nasdaq +1.29%, chips led) and computed QQQ's 20-day at $714.67 - QQQ $708.97 is "
 "-0.8% under it, so 3x stays gated while the 1x NVDA swing (the gate re-entry) is justified. "
 "After-hours quiet, NVDA ~$207 right at the entry. Not adding fresh size into extended semis ahead of "
 "Wed's GOOGL+TSLA+IBM+TXN after-close binary; NVDA armed to fire at tomorrow's open. Grade stays final D+.")
pulse_hype = ("Late check, all quiet - every stop's good, nothing's naked, and NVDA's parked right at "
 "tomorrow's buy. Not chasing the hot chips into Wed's Google + Tesla earnings; the NVDA swing's armed for the open.")
d['pulse'] = [{"ts": TS, "text": pulse_text, "hype": pulse_hype}] + d.get('pulse', [])
d['pulse'] = d['pulse'][:15]

# --- feed: prepend one activity, keep 40 ---
feed_text = ("7:15pm after-hours heartbeat - independently re-verified both books at the broker, nothing "
 "changed since 6:43p. LIVE flat $810.32 cash / nothing naked (6th session); PAPER 6/6 GTC-stopped "
 "(AMD/SMR/OKLO/VRT/CEG/NVDA), zero naked. Settled close confirmed (S&P +0.89% record, Nasdaq +1.29%); "
 "QQQ 20-day computed $714.67, QQQ -0.8% under = 3x gated, NVDA 1x swing armed for the open. No new size "
 "into extended semis ahead of Wed's GOOGL/TSLA binary. Grade final D+.")
d['feed'] = [{"type": "activity", "ts": TS, "text": feed_text}] + d.get('feed', [])
d['feed'] = d['feed'][:40]

# --- status: refresh Evening ---
for s in d.get('status', []):
    if s.get('session') == 'Evening':
        s['text'] = "After-hours quiet; NVDA armed for open"

# --- coverage: refresh the 'updated' label to show this run; keep 7/22 projections ---
for c in d.get('coverage', []):
    c['updated'] = "7/21 7:15p (7/22 plan)"

# --- accountability stays FINAL D+ (do not re-grade); assert it ---
assert d['accountability']['final'] is True
assert d['accountability']['grade'] == 'D+'
assert d['accountability']['date'] == '2026-07-21'

# --- pending_tickets: NVDA swing stays staged; assert ---
assert any(t.get('symbol') == 'NVDA' and t.get('id') == '2026-07-21-1' for t in d.get('pending_tickets', []))

# --- atomic write ---
tmp = SRC + '.tmp'
with open(tmp, 'w') as f:
    json.dump(d, f, ensure_ascii=False, indent=1)
os.replace(tmp, SRC)
print("WROTE", SRC, os.path.getsize(SRC), "bytes")
