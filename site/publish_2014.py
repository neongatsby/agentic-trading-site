#!/usr/bin/env python3
# Per-run publish (unique name, atomic write, verify-after) per OPS-ALERT-engine-data-clobber-2026-07-20.
import json, os, tempfile

SITE = os.path.dirname(os.path.abspath(__file__))
FP = os.path.join(SITE, "engine-data.json")

with open(FP) as f:
    d = json.load(f)

TS = "2026-07-21T20:14:00-04:00"

# --- archive current latest_recap, set fresh one ---
if "latest_recap" in d:
    d["_latest_recap_2014"] = d["latest_recap"]

d["latest_recap"] = (
    "8:14p 7/21 evening verify (market CLOSED, next open 7/22 09:30) - a light ~34-min heartbeat on from the "
    "7:40 run; grade stays final:true D+ (NOT re-graded, and deliberately NOT inflated off the thin after-hours mark "
    "per the 7/15 data-integrity rule - the ~$90.8k paper AH print runs hot vs the ~$90.0k RTH close I graded on). "
    "Fresh news + broker pass, nothing broke after the close: get_news empty since 6pm ET; web-search confirms the "
    "AI-infra/semis theme intact (NVDA up on new Vera CPU detail, AMD +6%, SMCI jumped AH on a rising order backlog, "
    "INTC up on job cuts) - no adverse NVDA headline. Both books == broker: LIVE flat $810.32 cash / 0 positions-orders "
    "(nothing naked, 6th straight cash session); PAPER 6 names ALL GTC-stopped + verified (AMD $490 / SMR $7.50 / "
    "OKLO $39 / VRT $282 / CEG $236 / NVDA $186), zero naked, each clear of its stop. NVDA ~$207 AH = right at the swing "
    "entry, so live ticket 2026-07-21-1 (3 sh, ~$207, $186 stop) stays ARMED for the 7/22 open - approve anytime, fills "
    "at the open, 0/3 day-trades. Regime re-entry criteria now essentially MET (2 green risk-on days + QQQ $708.8 within "
    "~0.8% of its $714.7 20-day + theme up on real memory/AI-capex catalysts) = firing NVDA at the open IS the re-entry. "
    "Wed 7/22 binary wall CONFIRMED: GOOGL + TSLA (+ IBM) report after the close; AMD 'Advancing AI 2026' runs daytime = "
    "AMD is tomorrow's pop_rank-1 (owned in paper, NOT chased live into the binary). Nothing to change tonight."
)

# --- prepend one pulse entry (newest first), keep ~15 ---
pulse_entry = {
    "ts": TS,
    "text": (
        "8:14p evening verify - one more fresh news + broker pass, nothing broke after the close. LIVE flat $810.32 cash "
        "(6th session, nothing naked); PAPER 6 names all GTC-stopped, zero naked. No adverse NVDA news (new Vera CPU detail; "
        "SMCI backlog up, INTC job cuts = theme tailwind); NVDA ~$207 AH is right at the swing entry, so ticket 2026-07-21-1 "
        "stays armed for the 7/22 open (approve anytime -> fills at the open, 0/3 day-trades). Grade stays final D+ - not "
        "re-graded, and I won't inflate it off a thin after-hours mark. Tomorrow's board: AMD 'Advancing AI' daytime = "
        "pop_rank 1; GOOGL + TSLA report after Wed's close."
    ),
    "hype": "One last look tonight - books clean, nothing broke. NVDA's armed to buy at tomorrow's open.",
}
d["pulse"] = [pulse_entry] + d.get("pulse", [])
d["pulse"] = d["pulse"][:15]

# --- prepend one feed activity entry (newest first), keep ~40 ---
feed_entry = {
    "type": "activity",
    "ts": TS,
    "text": (
        "8:14pm evening verify - fresh news + broker re-check, plan holds. LIVE flat $810 cash / nothing naked (6th "
        "session); PAPER 6/6 GTC-stopped, zero naked. No adverse after-hours news; NVDA ~$207 = at entry, ticket armed "
        "for the 7/22 open. Grade stays final D+."
    ),
}
d["feed"] = [feed_entry] + d.get("feed", [])
d["feed"] = d["feed"][:40]

# --- refresh Evening status card (keep Morning/Afternoon) ---
for s in d.get("status", []):
    if s.get("session") == "Evening":
        s["text"] = "Verified clean; NVDA armed for open"

# --- bump updated ---
d["updated"] = TS

# accountability, score, coverage, pending_tickets, equity curves: intentionally UNCHANGED.

# --- atomic write ---
fd, tmp = tempfile.mkstemp(dir=SITE, prefix=".engine-data-", suffix=".tmp")
with os.fdopen(fd, "w") as f:
    json.dump(d, f, indent=1, ensure_ascii=False)
os.replace(tmp, FP)

# --- verify readback ---
with open(FP) as f:
    v = json.load(f)
assert v["updated"] == TS, ("updated mismatch", v["updated"])
assert v["accountability"]["final"] is True and v["accountability"]["grade"] == "D+", "accountability drift"
assert [t["id"] for t in v["pending_tickets"]] == ["2026-07-21-1"], "pending drift"
assert v["pulse"][0]["ts"] == TS and len(v["pulse"]) == 15, "pulse issue"
assert v["feed"][0]["ts"] == TS and len(v["feed"]) == 40, "feed issue"
assert len(v["coverage"]) == 14, "coverage len changed"
print("OK  updated=%s  grade=%s(final=%s)  pending=%s  pulse=%d  feed=%d  coverage=%d"
      % (v["updated"], v["accountability"]["grade"], v["accountability"]["final"],
         [t["id"] for t in v["pending_tickets"]], len(v["pulse"]), len(v["feed"]), len(v["coverage"])))
