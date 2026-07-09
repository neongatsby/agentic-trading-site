// Netlify Function — PIN-gated owner approval straight from the web app.
// Commits site/approvals/<id>-<ts>.json into the repo the Mac poller pulls every ~60s.
// The poller relays it into the fast-lane (approve now / pre-arm buy-stop / skip).
//
// SECURITY: the PIN is checked HERE and is never written into the committed file, so no
// secret ever touches the public repo. A committed approval is therefore already authorized.
// Zero npm dependencies — uses the Node 18+ global fetch on Netlify's runtime.
//
// Required env vars (set once in Netlify → Site settings → Environment variables):
//   APPROVE_PIN  — the shared PIN you type in the UI
//   GH_TOKEN     — a fine-grained GitHub token with Contents: Read/Write on the site repo
//   GH_REPO      — "owner/repo" (e.g. neongatsby/agentic-trading-site)
//   GH_BRANCH    — optional, defaults to "main"

const J = (code, obj) => ({
  statusCode: code,
  headers: {
    'content-type': 'application/json',
    'access-control-allow-origin': '*',
    'access-control-allow-methods': 'POST, OPTIONS',
    'access-control-allow-headers': 'content-type',
    'cache-control': 'no-store',
  },
  body: JSON.stringify(obj),
});

exports.handler = async (event) => {
  if (event.httpMethod === 'OPTIONS') return J(204, {});
  if (event.httpMethod !== 'POST') return J(405, { error: 'POST only' });

  const PIN = process.env.APPROVE_PIN;
  const TOKEN = process.env.GH_TOKEN;
  const REPO = process.env.GH_REPO;
  const BRANCH = process.env.GH_BRANCH || 'main';
  if (!PIN || !TOKEN || !REPO)
    return J(503, { error: 'approval endpoint not configured', need: ['APPROVE_PIN', 'GH_TOKEN', 'GH_REPO'] });

  let b;
  try { b = JSON.parse(event.body || '{}'); } catch { return J(400, { error: 'bad json' }); }
  if (String(b.pin || '') !== String(PIN)) return J(401, { error: 'wrong PIN' });

  const id = String(b.id || '').replace(/[^0-9A-Za-z_.-]/g, '').slice(0, 64);
  if (!id) return J(400, { error: 'missing id' });
  const action = b.action === 'skip' ? 'skip' : 'approve';
  const mode = b.mode === 'prearm' ? 'prearm' : 'now';
  const ts = new Date().toISOString();
  const rec = { id, action, mode, symbol: String(b.symbol || '').slice(0, 12), source: 'web', ts };

  const path = `site/approvals/${id}-${Date.now()}.json`;
  const url = `https://api.github.com/repos/${REPO}/contents/${path}`;
  const content = Buffer.from(JSON.stringify(rec, null, 2)).toString('base64');

  let gh;
  try {
    gh = await fetch(url, {
      method: 'PUT',
      headers: {
        authorization: `Bearer ${TOKEN}`,
        accept: 'application/vnd.github+json',
        'user-agent': 'agentic-trading-approve',
        'content-type': 'application/json',
      },
      body: JSON.stringify({ message: `web ${action}/${mode} ${id}`, content, branch: BRANCH }),
    });
  } catch (e) {
    return J(502, { error: 'commit request failed', detail: String(e).slice(0, 200) });
  }
  if (!gh.ok) {
    const txt = await gh.text().catch(() => '');
    return J(502, { error: 'commit failed', status: gh.status, detail: txt.slice(0, 200) });
  }
  return J(200, { ok: true, id, action, mode });
};
