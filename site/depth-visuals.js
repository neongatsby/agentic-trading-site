/* depth-visuals.js — depth-layer visual engine for Agentic Trading
   <bot-head>       real Three.js robot head — deep frosted-chrome, black-reflective eyes, mouse-follow
   <decision-flow>  the BRAIN: hand-placed L→R decision graph, driven by setModel().
   Framework-agnostic vanilla web components (same split as slot-visuals.js).

   <decision-flow>
     el.setModel(model)   // shape = DEPTH-LAYER-BRIEF §1 (+ terminals may carry `detail:[...]`)
     attrs: variant "flow"|"schematic" · accent · down · idle · metal · rims · height
     Tap a node OR a terminal → focuses it in-graph (lifts, expands its context beside it,
     lights its path, dims the rest). No blur, no side sheet. Tap empty space to clear.
*/
(() => {
  if (customElements.get('decision-flow')) return;

  const STYLE_ID = 'df-styles';
  if (!document.getElementById(STYLE_ID)) {
    const s = document.createElement('style');
    s.id = STYLE_ID;
    s.textContent = `
      @keyframes dfDash { to { stroke-dashoffset: -1000; } }
      @keyframes dfBubbleIn { 0% { opacity:0; transform: translateY(10px) scale(.9);} 12% { opacity:1; transform: translateY(0) scale(1);} 82%{opacity:1;transform:translateY(-4px) scale(1);} 100%{opacity:0; transform: translateY(-16px) scale(.98);} }
      @keyframes dfPanelIn { 0%{opacity:0; transform: translate(var(--dfpx,0),-50%) scale(.96);} 100%{opacity:1; transform: translate(0,-50%) scale(1);} }
      .df-node { transition: transform .28s cubic-bezier(.3,1.3,.4,1), box-shadow .28s, border-color .28s, opacity .28s; }
      .df-edge { transition: opacity .3s ease, stroke-width .3s ease; }
      .df-elabel { transition: opacity .3s ease; }
    `;
    document.head.appendChild(s);
  }

  const NS = 'http://www.w3.org/2000/svg';
  const mk = (t, a) => { const e = document.createElementNS(NS, t); if (a) for (const k in a) e.setAttribute(k, a[k]); return e; };
  const rgba = (hex, a) => {
    if (!hex) return `rgba(200,210,225,${a})`;
    if (hex[0] !== '#') return hex.replace(/rgba?\(([^)]+)\)/, (m, i) => { const p = i.split(',').map(s => s.trim()); return `rgba(${p[0]},${p[1]},${p[2]},${a})`; });
    let h = hex.slice(1); if (h.length === 3) h = h.split('').map(x => x + x).join('');
    const n = parseInt(h, 16); return `rgba(${(n >> 16) & 255},${(n >> 8) & 255},${n & 255},${a})`;
  };

  /* ───────────────── shared Three.js ───────────────── */
  let threeP = null;
  const loadThree = () => {
    if (window.THREE) return Promise.resolve();
    if (!threeP) threeP = new Promise((res, rej) => { const s = document.createElement('script'); s.src = 'https://unpkg.com/three@0.128.0/build/three.min.js'; s.onload = res; s.onerror = rej; document.head.appendChild(s); });
    return threeP;
  };
  let gltfP = null;
  const loadGLTF = () => {
    if (window.THREE && THREE.GLTFLoader) return Promise.resolve();
    if (!gltfP) gltfP = new Promise((res, rej) => { const s = document.createElement('script'); s.src = 'https://unpkg.com/three@0.128.0/examples/js/loaders/GLTFLoader.js'; s.onload = res; s.onerror = rej; document.head.appendChild(s); });
    return gltfP;
  };
  function makeEnv(renderer, rims, metalHex) {
    const W = 1024, H = 512, c = document.createElement('canvas'); c.width = W; c.height = H;
    const g = c.getContext('2d'), m = new THREE.Color(metalHex || '#ffffff');
    const tint = (l, mix) => { const col = new THREE.Color(l, l, l).lerp(new THREE.Color(m.r * l * 2.2, m.g * l * 2.2, m.b * l * 2.2), mix); return '#' + col.getHexString(); };
    const grad = g.createLinearGradient(0, 0, 0, H);
    grad.addColorStop(0, tint(0.01, 0.5)); grad.addColorStop(0.44, tint(0.03, 0.6));
    grad.addColorStop(0.5, tint(0.09, 0.7)); grad.addColorStop(0.56, tint(0.03, 0.6)); grad.addColorStop(1, tint(0.006, 0.5));
    g.fillStyle = grad; g.fillRect(0, 0, W, H);
    const panel = (x, y, w, h, color, a) => { g.save(); g.translate(x, y); g.scale(w, h); const rg = g.createRadialGradient(0, 0, 0, 0, 0, 1); rg.addColorStop(0, color); rg.addColorStop(0.5, color); rg.addColorStop(1, 'rgba(0,0,0,0)'); g.globalAlpha = a; g.fillStyle = rg; g.beginPath(); g.arc(0, 0, 1, 0, 7); g.fill(); g.restore(); g.globalAlpha = 1; };
    rims.forEach((col, i) => { const x = (0.06 + (i / Math.max(1, rims.length)) * 0.94) * W; panel(x, H * (i % 2 ? 0.08 : 0.92), 230, 66, col, 1); panel(W - x, H * (i % 2 ? 0.95 : 0.05), 180, 52, col, 0.9); });
    const tex = new THREE.CanvasTexture(c); tex.mapping = THREE.EquirectangularReflectionMapping;
    const pm = new THREE.PMREMGenerator(renderer); const env = pm.fromEquirectangular(tex).texture; pm.dispose(); tex.dispose();
    return env;
  }
  const rrShape = (w, h, r) => { const s = new THREE.Shape(), x = -w / 2, y = -h / 2; s.moveTo(x + r, y); s.lineTo(x + w - r, y); s.quadraticCurveTo(x + w, y, x + w, y + r); s.lineTo(x + w, y + h - r); s.quadraticCurveTo(x + w, y + h, x + w - r, y + h); s.lineTo(x + r, y + h); s.quadraticCurveTo(x, y + h, x, y + h - r); s.lineTo(x, y + r); s.quadraticCurveTo(x, y, x + r, y); return s; };

  /* ───────────────── <bot-head> ───────────────── */
  class BotHead extends HTMLElement {
    static get observedAttributes() { return ['accent', 'metal', 'rims', 'model']; }
    connectedCallback() {
      if (this._init) return; this._init = true;
      Object.assign(this.style, { display: 'block', position: 'relative' });
      this._canvas = document.createElement('canvas');
      Object.assign(this._canvas.style, { width: '100%', height: '100%', display: 'block' });
      this.appendChild(this._canvas);
      this._bloom = document.createElement('canvas');
      Object.assign(this._bloom.style, { position: 'absolute', inset: '0', width: '100%', height: '100%', pointerEvents: 'none', mixBlendMode: 'plus-lighter', filter: 'blur(6px) brightness(1.12) contrast(1.5)' });
      this.appendChild(this._bloom);
      this._look = { x: 0, y: 0 }; this._lookAt = 0;
      this._onMove = (e) => { const r = this.getBoundingClientRect(); if (!r.width) return; const cx = r.left + r.width / 2, cy = r.top + r.height / 2; this._look = { x: Math.max(-1, Math.min(1, (e.clientX - cx) / (r.width * 2))), y: Math.max(-1, Math.min(1, (e.clientY - cy) / (r.height * 2))) }; this._lookAt = performance.now(); };
      window.addEventListener('pointermove', this._onMove, { passive: true });
      this._boot();
      this._blink = setInterval(() => { this._doBlink = performance.now(); }, 3800 + Math.random() * 2600);
    }
    disconnectedCallback() { cancelAnimationFrame(this._raf); clearInterval(this._blink); window.removeEventListener('pointermove', this._onMove); if (this._r) { this._r.dispose(); this._r.forceContextLoss && this._r.forceContextLoss(); this._r = null; } this._init = false; }
    setLook(nx, ny) { this._look = { x: nx, y: ny }; this._lookAt = performance.now(); }
    _accent() { return this.getAttribute('accent') || '#34d399'; }
    _rims() { return (this.getAttribute('rims') || '#34d399,#ffffff,#2dd4bf,#e6b45a').split(',').map(s => s.trim()); }
    async _boot() {
      try {
        await loadThree();
        const r = new THREE.WebGLRenderer({ canvas: this._canvas, antialias: true, alpha: true });
        r.setPixelRatio(Math.min(devicePixelRatio || 1, 1.75)); r.outputEncoding = THREE.sRGBEncoding;
        r.toneMapping = THREE.ACESFilmicToneMapping; r.toneMappingExposure = 1.02; this._r = r;
        const S = this._scene = new THREE.Scene();
        this._cam = new THREE.PerspectiveCamera(30, 1, 0.1, 100); this._cam.position.set(0, 0, 5.6);
        const env = makeEnv(r, this._rims(), this.getAttribute('metal') || '#ffffff');
        const acc = new THREE.Color(this._accent());
        r.localClippingEnabled = true;
        this._clip = new THREE.Plane(new THREE.Vector3(0, 1, 0), 1e6);
        const G = this._g = new THREE.Group(); S.add(G);
        this._eyes = []; this._pupils = [];
        if (this.getAttribute('model')) {
          // real uploaded GLB head (frosted-chrome finish, clipped to just the head)
          this._loadModel(G, env, acc);
        } else {
        // frosted chrome exterior
        const chrome = new THREE.MeshStandardMaterial({ color: new THREE.Color(this.getAttribute('metal') || '#eef2f7'), metalness: 1, roughness: 0.17, envMap: env, envMapIntensity: 1.4 });
        // black reflective material (visor + pupils + detailing)
        const black = new THREE.MeshStandardMaterial({ color: new THREE.Color('#05060a'), metalness: 1, roughness: 0.05, envMap: env, envMapIntensity: 1.15 });
        // deep boxy head — extruded rounded-rect, DEEP so it reads as a 3D square head
        const head = new THREE.Mesh(new THREE.ExtrudeGeometry(rrShape(2.35, 2.16, 0.34), { depth: 1.5, bevelEnabled: true, bevelThickness: 0.14, bevelSize: 0.12, bevelSegments: 4, curveSegments: 14 }), chrome);
        head.geometry.translate(0, 0, -0.75); G.add(head);
        // black reflective visor bar across the eyes
        const visor = new THREE.Mesh(new THREE.ExtrudeGeometry(rrShape(1.98, 0.72, 0.32), { depth: 0.16, bevelEnabled: true, bevelThickness: 0.05, bevelSize: 0.05, bevelSegments: 3, curveSegments: 12 }), black);
        visor.position.set(0, 0.14, 0.66); G.add(visor);
        // eyes — glowing frosted outer + BLACK REFLECTIVE pupil inside
        const eyeMat = new THREE.MeshStandardMaterial({ color: acc, emissive: acc, emissiveIntensity: 1.6, metalness: 0.3, roughness: 0.35 });
        [-0.45, 0.45].forEach(x => {
          const eye = new THREE.Mesh(new THREE.SphereGeometry(0.185, 28, 28), eyeMat.clone()); eye.position.set(x, 0.16, 0.86); G.add(eye); this._eyes.push(eye);
          const pup = new THREE.Mesh(new THREE.SphereGeometry(0.108, 24, 24), black); pup.position.set(x, 0.16, 0.99); pup._bx = x; pup._by = 0.16; G.add(pup); this._pupils.push(pup);
        });
        // mouth — black reflective bar
        const mouth = new THREE.Mesh(new THREE.BoxGeometry(0.8, 0.09, 0.14), black); mouth.position.set(0, -0.58, 0.7); G.add(mouth);
        // cheek detailing (black reflective studs)
        [-0.92, 0.92].forEach(x => { const d = new THREE.Mesh(new THREE.CylinderGeometry(0.08, 0.08, 0.14, 20), black); d.rotation.x = Math.PI / 2; d.position.set(x, -0.15, 0.6); G.add(d); });
        // antenna
        const ant = new THREE.Mesh(new THREE.CylinderGeometry(0.04, 0.05, 0.42, 12), chrome); ant.position.set(0, 1.34, 0); G.add(ant);
        this._bulb = new THREE.Mesh(new THREE.SphereGeometry(0.11, 20, 20), new THREE.MeshStandardMaterial({ color: acc, emissive: acc, emissiveIntensity: 1.9, roughness: 0.4 })); this._bulb.position.set(0, 1.6, 0); G.add(this._bulb);
        }
        // lighting: orbiting rim (matches hero) + a low cool frontal fill so features read
        this._orbit = this._rims().map((c, i) => { const L = new THREE.PointLight(new THREE.Color(c), 12, 0); S.add(L); return { L, phase: (i / 4) * Math.PI * 2, sp: 0.14 + 0.05 * (i % 3), rad: 5 + (i % 2) * 2, y: [2.4, -2, 3, -2.6][i % 4] }; });
        const fill = new THREE.PointLight(0xbcd0e6, 0.55, 0); fill.position.set(0.6, 0.8, 4.2); S.add(fill);
        S.add(new THREE.AmbientLight(0x1a1f2b, 0.5));
        this._t0 = performance.now(); this._resize();
        this._ro = new ResizeObserver(() => this._resize()); this._ro.observe(this);
        const loop = () => {
          this._raf = requestAnimationFrame(loop);
          this._fc = ((this._fc || 0) + 1) % 20;
          if (this._fc === 1) { const b = this.getBoundingClientRect(); this._vis = b.bottom > -80 && b.top < innerHeight + 80 && b.width > 0; }
          if (!this._vis) return;
          const t = (performance.now() - this._t0) / 1000;
          const recent = this._lookAt && (performance.now() - this._lookAt < 2600);
          const ty = recent ? this._look.x * 0.62 : -Math.sin(t * 0.35) * 0.13;
          const tx = recent ? this._look.y * 0.46 : (-0.03 + Math.sin(t * 0.24) * 0.05);
          this._g.rotation.y += (ty - this._g.rotation.y) * 0.09;
          this._g.rotation.x += (tx - this._g.rotation.x) * 0.09;
          const br = 1 + Math.sin(t * 1.4) * 0.018; this._g.scale.setScalar(br);
          if (recent) this._pupils.forEach(p => { p.position.x += (p._bx + this._look.x * 0.055 - p.position.x) * 0.15; p.position.y += (p._by - this._look.y * 0.045 - p.position.y) * 0.15; });
          else this._pupils.forEach(p => { p.position.x += (p._bx - p.position.x) * 0.1; p.position.y += (p._by - p.position.y) * 0.1; });
          for (const o of this._orbit) { const a = o.phase + t * o.sp; o.L.position.set(Math.sin(a) * o.rad, o.y + Math.sin(t * 0.2 + o.phase) * 1.1, -(1 + o.rad * (0.4 + 0.4 * Math.cos(a)))); }
          let ei = 1.4 + Math.sin(t * 2.1) * 0.35;
          if (this._doBlink) { const p = (performance.now() - this._doBlink) / 150; if (p < 1) { const sy = Math.abs(Math.cos(p * Math.PI)); this._eyes.forEach(e => e.scale.y = Math.max(0.08, sy)); this._pupils.forEach(e => e.scale.y = Math.max(0.08, sy)); } else { this._eyes.forEach(e => e.scale.y = 1); this._pupils.forEach(e => e.scale.y = 1); this._doBlink = 0; } }
          this._eyes.forEach(e => e.material.emissiveIntensity = ei);
          r.render(S, this._cam);
          if (!(this._fc & 1)) { const bw = Math.max(1, this.clientWidth / 2 | 0), bh = Math.max(1, this.clientHeight / 2 | 0); if (this._bloom.width !== bw) { this._bloom.width = bw; this._bloom.height = bh; } const bg = this._bloom.getContext('2d'); bg.clearRect(0, 0, bw, bh); bg.globalAlpha = 0.5; bg.drawImage(this._canvas, 0, 0, bw, bh); }
        };
        loop();
      } catch (e) { console.warn('bot-head fallback', e); this._fallback(); }
    }
    _resize() { if (!this._r) return; const w = this.clientWidth || 130, h = this.clientHeight || 120; this._r.setSize(w, h, false); this._cam.aspect = w / h; this._cam.updateProjectionMatrix(); }
    _loadModel(G, env, acc) {
      loadGLTF().then(() => {
        new THREE.GLTFLoader().load(this.getAttribute('model'), (g) => {
          const root = g.scene;
          root.traverse(o => { if (o.isMesh && o.material) { const arr = Array.isArray(o.material) ? o.material : [o.material]; arr.forEach(m => { m.envMap = env; m.envMapIntensity = 1.45; m.metalness = 1; m.roughness = 0.2; if (m.map) { m.emissiveMap = m.map; m.emissive = new THREE.Color(0xffffff); m.emissiveIntensity = 0.34; } m.needsUpdate = true; }); o.material.clippingPlanes = [this._clip]; } });
          const box = new THREE.Box3().setFromObject(root), size = box.getSize(new THREE.Vector3()), c = box.getCenter(new THREE.Vector3());
          const s = 1.46 / size.y; root.scale.setScalar(s);
          const faceLocalY = c.y + size.y * 0.16;               // bigger in frame, less headroom
          root.position.set(-c.x * s, -faceLocalY * s, -c.z * s);
          this._clip.constant = 1e6;                             // no hard clip — the porthole box crops the body (window effect)
          G.add(root);
          this._cam.fov = 30; this._cam.position.set(0, 0, 3.0); this._cam.lookAt(0, 0, 0); this._cam.updateProjectionMatrix();
          this._modelRoot = root;
        }, undefined, () => this._fallback());
      }).catch(() => this._fallback());
    }
    _fallback() {
      const c = this._accent(); this.innerHTML = '';
      const f = document.createElement('div');
      Object.assign(f.style, { width: '100%', height: '100%', borderRadius: '22px', border: '1.5px solid ' + rgba(c, 0.5), background: 'linear-gradient(160deg,#eef4f8,#8a94a6 55%,#dfe7ee)', boxShadow: '0 0 30px ' + rgba(c, 0.3), display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '20px' });
      [0, 1].forEach(() => { const e = document.createElement('div'); Object.assign(e.style, { width: '15px', height: '15px', borderRadius: '50%', background: c, boxShadow: '0 0 12px ' + c }); f.appendChild(e); });
      this.appendChild(f);
    }
  }
  customElements.define('bot-head', BotHead);

  /* ───────────────── <decision-flow> ───────────────── */
  class DecisionFlow extends HTMLElement {
    static get observedAttributes() { return ['variant', 'accent', 'down', 'idle', 'metal', 'rims']; }
    connectedCallback() {
      if (this._init) return; this._init = true;
      Object.assign(this.style, { display: 'block', position: 'relative', width: '100%', overflow: 'hidden' });
      if (this.getAttribute('height')) this.style.height = this.getAttribute('height') + 'px';
      this._svg = mk('svg', { width: '100%', height: '100%', preserveAspectRatio: 'none' });
      Object.assign(this._svg.style, { position: 'absolute', inset: '0', overflow: 'visible', pointerEvents: 'none' });
      this._edgeG = mk('g'); this._svg.appendChild(this._edgeG); this.appendChild(this._svg);
      this._nodeLayer = document.createElement('div'); Object.assign(this._nodeLayer.style, { position: 'absolute', inset: '0', pointerEvents: 'none' }); this.appendChild(this._nodeLayer);
      this._avatarLayer = document.createElement('div'); Object.assign(this._avatarLayer.style, { position: 'absolute', inset: '0', pointerEvents: 'none' }); this.appendChild(this._avatarLayer);
      this._bubbleLayer = document.createElement('div'); Object.assign(this._bubbleLayer.style, { position: 'absolute', inset: '0', pointerEvents: 'none', overflow: 'hidden' }); this.appendChild(this._bubbleLayer);
      this._model = this._pending || this._defaultModel(); this._pending = null; this._sel = null;
      this._buildAvatar();
      this.addEventListener('click', () => this._select(null));
      this._ro = new ResizeObserver(() => this._build()); this._ro.observe(this);
      this._build();
      this._t0 = performance.now(); this._loop();
      this._scheduleBubble(1400);
    }
    attributeChangedCallback() { if (this._init) { this._syncAvatar(); this._build(); } }
    disconnectedCallback() { cancelAnimationFrame(this._raf); this._ro && this._ro.disconnect(); clearTimeout(this._bubbleTimer); this._init = false; }
    setModel(model) { if (!model) return; if (!this._init) { this._pending = model; return; } this._model = model; this._syncAvatar(); this._build(); }

    _col() { return { accent: this.getAttribute('accent') || '#34d399', down: this.getAttribute('down') || '#f87171', idle: this.getAttribute('idle') || 'rgba(200,210,225,0.5)', metal: this.getAttribute('metal') || '#cfe0ea' }; }
    _isSchem() { return this.getAttribute('variant') === 'schematic'; }
    _kindColor(k) { const c = this._col(); return k === 'stop' ? c.down : k === 'idle' ? c.idle : k === 'trunk' ? c.metal : c.accent; }
    _itemById(id) { const m = this._model; return (m.nodes || []).find(n => n.id === id) || (m.terminals || []).find(t => t.id === id) || null; }
    // selection now only re-applies focus styling — DOM is NOT rebuilt, so it animates cleanly
    _select(id) { const next = (id === this._sel) ? null : id; if (next === this._sel) return; this._sel = next; this._applyFocus(); }

    /* layout: hand-placed columns + barycenter terminal ordering + fan-in/out (auto de-tangle) */
    _build() {
      const W = this._W = this.clientWidth || 900, H = this._H = this.clientHeight || 700; if (!W || !H) return;
      const m = this._model, colX = { 0: 0.12, 1: 0.335, 2: 0.575, 3: 0.86 };
      const pos = this._pos = {}, top = 74, bot = H - 74, span = Math.max(1, bot - top);
      const yAt = (i, n) => n <= 1 ? H * 0.5 : top + span * i / (n - 1);
      pos.__root = { x: W * colX[0], y: H * 0.5 }; pos.__gate = { x: W * colX[1], y: H * 0.5 };
      const held = (m.nodes || []).filter(n => n.kind !== 'armed'), armed = (m.nodes || []).filter(n => n.kind === 'armed');
      const nodes = held.concat(armed);
      nodes.forEach((n, i) => { pos[n.id] = { x: W * colX[2], y: yAt(i, nodes.length) }; });
      pos.__closed = { x: W * colX[1], y: bot };
      const rank = { up: 0, stop: 1, idle: 2 };
      const terms = (m.terminals || []).slice();
      terms.forEach(t => { const ys = (m.edges || []).filter(e => e.to === t.id && pos[e.from]).map(e => pos[e.from].y); t._b = ys.length ? ys.reduce((a, b) => a + b) / ys.length : H / 2; });
      terms.sort((a, b) => a._b - b._b || (rank[a.kind] || 0) - (rank[b.kind] || 0));
      terms.forEach((t, i) => { pos[t.id] = { x: W * colX[3], y: yAt(i, terms.length) }; });
      const bySrc = {}, byTgt = {}; (m.edges || []).forEach(e => { (bySrc[e.from] = bySrc[e.from] || []).push(e); (byTgt[e.to] = byTgt[e.to] || []).push(e); });
      for (const k in bySrc) bySrc[k].sort((a, b) => (pos[a.to] ? pos[a.to].y : 0) - (pos[b.to] ? pos[b.to].y : 0));
      for (const k in byTgt) byTgt[k].sort((a, b) => (pos[a.from] ? pos[a.from].y : 0) - (pos[b.from] ? pos[b.from].y : 0));
      this._ep = {}; const nH = 88, tH = 74, fan = 13;
      (m.edges || []).forEach(e => { const a = pos[e.from], b = pos[e.to]; if (!a || !b) return; const so = bySrc[e.from], si = so.indexOf(e), to = byTgt[e.to], ti = to.indexOf(e); this._ep[e.from + '>' + e.to] = { a: { x: a.x + nH, y: a.y + (si - (so.length - 1) / 2) * fan }, b: { x: b.x - tH, y: b.y + (ti - (to.length - 1) / 2) * fan } }; });
      this._renderEdges(m, pos);
      this._renderNodes(m, pos);
      this._positionAvatar(pos.__root);
      this._applyFocus();
    }

    _connected() {
      const m = this._model, sel = this._sel; if (!sel) return null;
      const ids = new Set(['__root', '__gate', sel]); const ek = new Set(['__root>__gate']);
      const isTerm = (m.terminals || []).some(t => t.id === sel);
      if (isTerm) { (m.edges || []).forEach(e => { if (e.to === sel) { ids.add(e.from); ek.add('__gate>' + e.from); ek.add(e.from + '>' + sel); } }); }
      else { ek.add('__gate>' + sel); (m.edges || []).forEach(e => { if (e.from === sel) { ids.add(e.to); ek.add(e.from + '>' + e.to); } }); }
      return { ids, ek };
    }

    /* ---- build DOM once per layout (base styles); refs kept for focus ---- */
    _renderNodes(m, pos) {
      const c = this._col(), schem = this._isSchem();
      this._nodeLayer.innerHTML = ''; this._nodeRefs = []; this._panelEl = null;
      const add = (o) => { const el = this._chip(o); this._nodeLayer.appendChild(el); this._nodeRefs.push({ id: o.refId, el, color: o.color, faint: !!o.faint, baseShadow: el.style.boxShadow }); return el; };
      add({ refId: '__gate', pos: pos.__gate, title: 'Market', sub: m.marketOpen ? 'OPEN' : 'CLOSED', color: m.marketOpen ? c.accent : c.idle, schem, glow: m.marketOpen, w: 122 });
      add({ refId: '__closed', pos: pos.__closed, title: 'closed', sub: 'hold · wait', color: c.idle, dashed: true, schem, faint: true, w: 116 });
      (m.nodes || []).forEach(n => add({ refId: n.id, id: n.id, node: n, pos: pos[n.id], title: n.label, sub: n.sub, color: n.kind === 'armed' ? c.accent : c.metal, dashed: n.kind === 'armed', schem, w: schem ? 178 : 170, tall: true, tag: n.kind === 'armed' ? 'ARMED' : 'HELD' }));
      (m.terminals || []).forEach(t => add({ refId: t.id, id: t.id, node: t, pos: pos[t.id], title: t.label, color: this._kindColor(t.kind), schem, terminal: true, w: schem ? 152 : 148 }));
    }

    _chip(o) {
      const el = document.createElement('div'); el.className = 'df-node';
      const radius = o.schem ? '9px' : (o.terminal ? '999px' : '16px');
      const bg = o.faint ? 'rgba(255,255,255,0.02)' : o.terminal ? rgba(o.color, 0.14) : 'linear-gradient(180deg, rgba(255,255,255,0.06), rgba(255,255,255,0.02))';
      Object.assign(el.style, {
        position: 'absolute', left: o.pos.x + 'px', top: o.pos.y + 'px', transform: 'translate(-50%,-50%) scale(1)',
        width: o.w + 'px', boxSizing: 'border-box', padding: o.terminal ? '11px 16px' : (o.tall ? '12px 16px' : '10px 15px'), borderRadius: radius,
        border: (o.dashed ? '1.5px dashed ' : '1.5px solid ') + rgba(o.color, o.faint ? 0.35 : 0.6), background: bg,
        backdropFilter: 'blur(8px)', WebkitBackdropFilter: 'blur(8px)', color: '#eef4f8', pointerEvents: o.id ? 'auto' : 'none', cursor: o.id ? 'pointer' : 'default',
        boxShadow: o.glow ? '0 0 22px ' + rgba(o.color, 0.35) + ', inset 0 1px 0 rgba(255,255,255,0.14)' : 'inset 0 1px 0 rgba(255,255,255,0.1), 0 10px 26px rgba(0,0,0,0.35)',
        zIndex: 5,
      });
      const rows = [];
      if (o.tag) rows.push(`<div style="font:700 8.5px/1 ui-monospace,Menlo,monospace;letter-spacing:1.5px;color:${o.color};margin-bottom:5px">${o.tag}</div>`);
      rows.push(`<div style="font:700 ${o.terminal ? 13 : 17}px/1 'Avenir Next Condensed','Avenir Next',system-ui,sans-serif;letter-spacing:.4px;color:${o.terminal ? o.color : '#f3f8fb'};text-transform:${o.terminal ? 'uppercase' : 'none'}">${o.title}</div>`);
      if (o.sub) rows.push(`<div style="font:500 12px/1.3 system-ui,sans-serif;color:rgba(238,244,248,.55);margin-top:3px">${o.sub}</div>`);
      el.innerHTML = rows.join('');
      if (o.id) el.addEventListener('click', (e) => { e.stopPropagation(); this._select(o.id); this.dispatchEvent(new CustomEvent('flow-node', { bubbles: true, detail: { id: o.id, node: o.node } })); });
      return el;
    }

    _renderEdges(m, pos) {
      const schem = this._isSchem();
      this._edgeG.innerHTML = ''; this._edgeRefs = []; this._labelRefs = [];
      const path = (a, b) => schem ? this._elbow(a, b) : this._curve(a, b);
      const addEdge = (a, b, kind, key, opt = {}) => {
        const col = this._kindColor(kind), d = path(a, b);
        const glow = mk('path', { class: 'df-edge', d, fill: 'none', stroke: col, 'stroke-width': 5, 'stroke-linecap': 'round', opacity: 0.1 }); glow.style.filter = 'blur(3px)'; this._edgeG.appendChild(glow);
        const p = mk('path', { class: 'df-edge', d, fill: 'none', stroke: col, 'stroke-width': opt.thick ? 2.6 : 1.8, 'stroke-linecap': 'round', opacity: kind === 'idle' ? 0.45 : 0.85 });
        p.setAttribute('stroke-dasharray', kind === 'idle' || opt.dashed ? '2 7' : '9 10');
        p.style.animation = `dfDash ${opt.hot ? 9 : kind === 'idle' ? 34 : 20}s linear infinite`;
        this._edgeG.appendChild(p);
        this._edgeRefs.push({ key, kind, glow, p, hot: !!opt.hot, thick: !!opt.thick, baseDim: !!opt.dim });
      };
      addEdge({ x: pos.__root.x + 92, y: pos.__root.y }, { x: pos.__gate.x - 62, y: pos.__gate.y }, 'trunk', '__root>__gate', { thick: true });
      addEdge({ x: pos.__gate.x, y: pos.__gate.y + 20 }, { x: pos.__closed.x, y: pos.__closed.y }, 'idle', '__gate>__closed', { dim: true, dashed: true });
      const nodes = (m.nodes || []);
      nodes.forEach((n, i) => addEdge({ x: pos.__gate.x + 62, y: pos.__gate.y + (i - (nodes.length - 1) / 2) * (schem ? 0 : 9) }, { x: pos[n.id].x - 88, y: pos[n.id].y }, 'trunk', '__gate>' + n.id, { dim: !m.marketOpen }));
      (m.edges || []).forEach(e => { const ep = this._ep[e.from + '>' + e.to]; if (!ep) return; const key = e.from + '>' + e.to; addEdge(ep.a, ep.b, e.kind, key, { hot: !!e.hot }); if (e.cond) this._edgeLabel(e.cond, ep.a, ep.b, this._kindColor(e.kind), e.hot, key); });
    }

    /* ---- the only thing selection touches: styling, not DOM ---- */
    _applyFocus() {
      const con = this._connected();
      (this._nodeRefs || []).forEach(o => {
        const sel = this._sel === o.id, lit = !con || con.ids.has(o.id);
        let op = 1; if (o.faint) op = con ? 0.14 : 0.55; else if (con && !lit) op = 0.2;
        o.el.style.opacity = op;
        o.el.style.transform = `translate(-50%,-50%) scale(${sel ? 1.09 : 1})`;
        o.el.style.borderColor = rgba(o.color, sel ? 0.95 : (o.faint ? 0.35 : 0.6));
        o.el.style.boxShadow = sel ? '0 0 34px ' + rgba(o.color, 0.6) + ', inset 0 1px 0 rgba(255,255,255,0.22)' : o.baseShadow;
        o.el.style.zIndex = sel ? 8 : 5;
      });
      this._hotPaths = [];
      (this._edgeRefs || []).forEach(o => {
        const lit = !con || con.ek.has(o.key), dim = o.baseDim || (con && !lit), strong = lit && con;
        o.glow.style.opacity = dim ? 0.03 : (o.hot || strong ? 0.3 : 0.1);
        o.glow.setAttribute('stroke-width', strong || o.hot ? 7 : 5);
        o.p.style.opacity = dim ? 0.06 : (o.kind === 'idle' ? 0.45 : 0.85);
        o.p.setAttribute('stroke-width', (strong || o.thick) ? 2.6 : 1.8);
        if ((o.hot && !con) || (strong && o.kind === 'up')) this._hotPaths.push({ path: o.p, col: this._kindColor(o.kind) });
      });
      (this._labelRefs || []).forEach(o => { o.el.style.opacity = con && !con.ek.has(o.key) ? 0.1 : (o.hot ? 1 : 0.95); });
      if (this._avatarWrap) this._avatarWrap.style.opacity = this._sel ? 0.3 : 1;
      if (this._panelEl) { this._panelEl.remove(); this._panelEl = null; }
      if (this._sel) { const item = this._itemById(this._sel); if (item && this._pos[this._sel]) { this._panelEl = this._panel(item, this._pos[this._sel]); this._nodeLayer.appendChild(this._panelEl); } }
      this._buildHotBeads();
    }

    _panel(item, p) {
      const c = this._col(), W = this._W, H = this._H;
      const el = document.createElement('div'); el.className = 'df-panel';
      const wdt = 312, placeRight = p.x + 118 + wdt < W - 8, x = placeRight ? p.x + 118 : p.x - 118 - wdt;
      el.style.setProperty('--dfpx', (placeRight ? -10 : 10) + 'px');
      Object.assign(el.style, { position: 'absolute', left: Math.max(8, x) + 'px', top: '50%', transform: 'translate(0,-50%)', width: wdt + 'px', maxHeight: (H - 36) + 'px', overflowY: 'auto', boxSizing: 'border-box', padding: '20px 22px', borderRadius: '16px', border: '1px solid ' + rgba(c.accent, 0.35), background: 'linear-gradient(180deg, rgba(17,25,25,0.97), rgba(10,15,17,0.97))', boxShadow: '0 24px 60px rgba(0,0,0,0.55), 0 0 30px ' + rgba(c.accent, 0.15), backdropFilter: 'blur(14px)', WebkitBackdropFilter: 'blur(14px)', pointerEvents: 'auto', zIndex: 9, animation: 'dfPanelIn .3s cubic-bezier(.3,1.2,.4,1)' });
      el.addEventListener('click', (e) => e.stopPropagation());
      const chip = (txt, col) => `<span style="font:600 10.5px/1 ui-monospace,Menlo,monospace;letter-spacing:1px;color:${col || 'rgba(255,255,255,.6)'};background:${col ? rgba(col, 0.14) : 'rgba(255,255,255,0.06)'};border:1px solid ${col ? rgba(col, 0.4) : 'rgba(255,255,255,0.1)'};padding:6px 9px;border-radius:7px;white-space:nowrap">${txt}</span>`;
      const head = `<div style="display:flex;align-items:baseline;justify-content:space-between;gap:10px"><div style="font:700 24px/1 'Avenir Next Condensed','Avenir Next',system-ui,sans-serif;color:#f3f8fb;text-transform:${item.detail ? 'uppercase' : 'none'}">${item.label}</div><div style="font:600 12px/1 system-ui;color:${rgba(c.accent, .8)};cursor:pointer" class="df-x">clear ✕</div></div>`;
      let html = head;
      if (item.detail) { // terminal outcome
        const kl = item.kind === 'stop' ? 'STOP OUTCOME' : item.kind === 'idle' ? 'IDLE OUTCOME' : 'UPSIDE OUTCOME';
        html += `<div style="display:flex;gap:7px;flex-wrap:wrap;margin:13px 0 15px">${chip(kl, this._kindColor(item.kind))}</div>`;
        item.detail.forEach(w => { html += `<div style="font:400 13.5px/1.6 system-ui;color:rgba(238,244,248,.75);margin-bottom:11px">${w}</div>`; });
      } else { // held / armed node
        if (item.name) html += `<div style="font:500 13px/1.3 system-ui;color:rgba(238,244,248,.55);margin-top:5px">${item.name}</div>`;
        const vcol = item.verdict === 'held' ? c.metal : c.accent;
        html += `<div style="display:flex;gap:7px;flex-wrap:wrap;margin:13px 0 15px">${chip((item.verdict || '').toUpperCase(), vcol)}${item.size ? chip(item.size) : ''}${item.level ? chip(item.level) : ''}</div>`;
        (item.why || []).forEach(w => { html += `<div style="font:400 13.5px/1.6 system-ui;color:rgba(238,244,248,.75);margin-bottom:11px">${w}</div>`; });
      }
      el.innerHTML = html;
      const x2 = el.querySelector('.df-x'); if (x2) x2.addEventListener('click', (e) => { e.stopPropagation(); this._select(null); });
      return el;
    }

    _curve(a, b) { const dx = (b.x - a.x) * 0.5; return `M ${a.x} ${a.y} C ${a.x + dx} ${a.y}, ${b.x - dx} ${b.y}, ${b.x} ${b.y}`; }
    _elbow(a, b) { const mx = (a.x + b.x) / 2, r = Math.min(14, Math.abs(b.y - a.y) / 2, Math.abs(b.x - a.x) / 2); if (Math.abs(a.y - b.y) < 2) return `M ${a.x} ${a.y} L ${b.x} ${b.y}`; const d = b.y > a.y ? 1 : -1; return `M ${a.x} ${a.y} L ${mx - r} ${a.y} Q ${mx} ${a.y} ${mx} ${a.y + d * r} L ${mx} ${b.y - d * r} Q ${mx} ${b.y} ${mx + r} ${b.y} L ${b.x} ${b.y}`; }
    _edgeLabel(text, a, b, color, hot, key) {
      const el = document.createElement('div'); el.className = 'df-elabel';
      const mx = a.x + (b.x - a.x) * 0.42, my = a.y + (b.y - a.y) * 0.42;
      Object.assign(el.style, { position: 'absolute', left: mx + 'px', top: my + 'px', transform: 'translate(-50%,-50%)', font: '600 10.5px/1.25 ui-monospace,Menlo,monospace', color: '#e8f0f4', background: 'rgba(10,14,20,0.82)', border: '1px solid ' + rgba(color, hot ? 0.7 : 0.3), padding: '4px 8px', borderRadius: '7px', maxWidth: '190px', textAlign: 'center', pointerEvents: 'none', boxShadow: hot ? '0 0 16px ' + rgba(color, 0.4) : 'none', zIndex: 4 });
      el.textContent = text; this._nodeLayer.appendChild(el); this._labelRefs.push({ key, el, hot });
    }
    _buildHotBeads() {
      [...this._edgeG.querySelectorAll('.df-bead')].forEach(b => b.remove());
      this._beads = (this._hotPaths || []).map(({ path, col }) => { const b = mk('circle', { r: 4, fill: '#fff' }); b.setAttribute('class', 'df-bead'); b.style.filter = 'drop-shadow(0 0 7px ' + col + ')'; this._edgeG.appendChild(b); return { bead: b, path, len: path.getTotalLength ? path.getTotalLength() : 0 }; });
    }
    _loop() { const step = () => { this._raf = requestAnimationFrame(step); if (!this.clientWidth) return; const t = (performance.now() - this._t0) / 1000; if (this._beads) for (const b of this._beads) { if (!b.len) b.len = b.path.getTotalLength ? b.path.getTotalLength() : 0; const u = (t * 0.42) % 1, pt = b.len ? b.path.getPointAtLength(u * b.len) : null; if (pt) { b.bead.setAttribute('cx', pt.x); b.bead.setAttribute('cy', pt.y); b.bead.style.opacity = (u < 0.06 || u > 0.94) ? 0 : 1; } } }; step(); }

    _buildAvatar() {
      const wrap = this._avatarWrap = document.createElement('div');
      Object.assign(wrap.style, { position: 'absolute', width: '162px', transform: 'translate(-50%,-50%)', textAlign: 'center', pointerEvents: 'none', transition: 'opacity .26s' });
      const head = document.createElement('bot-head');
      Object.assign(head.style, { display: 'block', width: '140px', height: '128px', margin: '0 auto' });
      head.setAttribute('accent', this._col().accent);
      head.setAttribute('rims', this.getAttribute('rims') || '#34d399,#ffffff,#2dd4bf,#e6b45a');
      head.setAttribute('metal', '#eef2f7');
      const bm = this.getAttribute('bot-model') || 'uploads/uploads_files_6072204_sleek+and+modern+cute+robot+glossy+white+body+glowing+blue+eyes.glb';
      if (bm) {
        head.setAttribute('model', bm);
        // contain the head in a little rounded porthole so the clipped neck never reads as a raw cut
        Object.assign(head.style, { width: '164px', height: '164px', margin: '0' });
        const box = document.createElement('div');
        const acc = this._col().accent;
        Object.assign(box.style, { position: 'relative', width: '150px', height: '132px', margin: '0 auto', borderRadius: '22px', overflow: 'hidden', border: '1px solid ' + rgba(acc, 0.28), background: 'radial-gradient(80% 70% at 50% 34%, ' + rgba(acc, 0.12) + ', rgba(255,255,255,0.02) 70%)', boxShadow: 'inset 0 1px 0 rgba(255,255,255,0.14), inset 0 -18px 26px rgba(0,0,0,0.5), 0 10px 26px rgba(0,0,0,0.4)' });
        Object.assign(head.style, { position: 'absolute', left: '50%', top: '2px', transform: 'translateX(-50%)' });
        const fade = document.createElement('div');
        Object.assign(fade.style, { position: 'absolute', left: '0', right: '0', bottom: '0', height: '34px', pointerEvents: 'none', background: 'linear-gradient(180deg, rgba(0,0,0,0) 0%, rgba(8,11,17,0.55) 100%)' });
        box.appendChild(head); box.appendChild(fade);
        wrap.appendChild(box);
      } else {
        wrap.appendChild(head);
      }
      this._avatarLabel = document.createElement('div'); wrap.appendChild(this._avatarLabel);
      this._avatarLayer.appendChild(wrap); this._avatarYOffset = bm ? 4 : 0; this._syncAvatar();
    }
    _syncAvatar() {
      if (!this._avatarLabel) return; const c = this._col(), root = (this._model && this._model.root) || {};
      this._avatarLabel.innerHTML = `<div style="font:800 19px/1 'Avenir Next Condensed','Avenir Next',system-ui,sans-serif;letter-spacing:.5px;color:#f3f8fb;margin-top:12px">${root.label || ''}</div>` + (root.sub ? `<div style="font:600 11px/1.2 ui-monospace,Menlo,monospace;letter-spacing:1px;color:${rgba(c.accent, .85)};margin-top:5px;text-transform:uppercase">${root.sub}</div>` : '') + `<div style="font:600 9px/1 ui-monospace,Menlo,monospace;letter-spacing:2px;color:rgba(238,244,248,.4);margin-top:7px">THE&nbsp;ENGINE</div>`;
    }
    _positionAvatar(p) { if (!this._avatarWrap) return; this._avatarWrap.style.left = p.x + 'px'; this._avatarWrap.style.top = (p.y + (this._avatarYOffset || 0)) + 'px'; }

    _scheduleBubble(delay) { clearTimeout(this._bubbleTimer); this._bubbleTimer = setTimeout(() => { this._popBubble(); this._scheduleBubble(4400 + Math.random() * 2600); }, delay); }
    _popBubble() {
      if (!this.clientWidth || !this._pos || !this._pos.__root || this._sel) return;
      const th = (this._model && this._model.thoughts) || []; if (!th.length) return;
      this._bi = ((this._bi || 0) + 1) % th.length; const c = this._col(), p = this._pos.__root;
      const fill = 'linear-gradient(180deg, ' + rgba(c.accent, 0.2) + ', ' + rgba(c.accent, 0.08) + ')', bd = '1px solid ' + rgba(c.accent, 0.42);
      // classic thought bubble: rounded body centred over the robot + two puffs trailing DOWN to its head
      const wrap = document.createElement('div');
      Object.assign(wrap.style, { position: 'absolute', left: p.x + 'px', bottom: (this.clientHeight - (p.y - 96)) + 'px', top: 'auto', transform: 'translateX(-50%)', pointerEvents: 'none', zIndex: 7 });
      const inner = document.createElement('div');   // animation lives here so it can't clobber the wrap's translateX(-50%) centering
      Object.assign(inner.style, { display: 'flex', flexDirection: 'column', alignItems: 'center', animation: 'dfBubbleIn 5.4s ease forwards' });
      const b = document.createElement('div');
      Object.assign(b.style, { maxWidth: '184px', font: '500 12.5px/1.4 system-ui,sans-serif', textAlign: 'center', color: '#eef4f8', background: fill, border: bd, borderRadius: '16px', padding: '10px 14px', boxShadow: '0 8px 24px rgba(0,0,0,0.4), 0 0 20px ' + rgba(c.accent, 0.18), backdropFilter: 'blur(10px)', WebkitBackdropFilter: 'blur(10px)' });
      b.textContent = th[this._bi];
      const puff = (d, mt) => { const q = document.createElement('div'); Object.assign(q.style, { width: d + 'px', height: d + 'px', marginTop: mt + 'px', borderRadius: '50%', background: fill, border: bd, boxShadow: '0 0 10px ' + rgba(c.accent, 0.18), backdropFilter: 'blur(10px)', WebkitBackdropFilter: 'blur(10px)' }); return q; };
      wrap.appendChild(inner); inner.appendChild(b); inner.appendChild(puff(14, 6)); inner.appendChild(puff(8, 4));
      this._bubbleLayer.appendChild(wrap); setTimeout(() => wrap.remove(), 5500);
    }

    _defaultModel() {
      return { root: { label: '$1,437', sub: '85% deployed' }, marketOpen: true,
        thoughts: ['TQQQ trailing stop sits at $68.50 — 2% below spot. Comfortable.', 'SOXL is a hair under its trigger. Finger hovering, not pressing.', 'Cash is 15% — enough dry powder for one more entry.'],
        nodes: [
          { id: 'tqqq', col: 2, kind: 'held', label: 'TQQQ', sub: '3× core · $743', name: 'ProShares UltraPro QQQ', verdict: 'held', size: '$743 · 3× core', level: 'stop $68.50', why: ['The beta dial — how it presses when the tape is risk-on above the 50-day.', 'Trailing a hard stop at $68.50. Rides the trend, carried out on the break.'] },
          { id: 'ionq', col: 2, kind: 'held', label: 'IONQ', sub: 'quantum · $312', name: 'IonQ Inc', verdict: 'buy', size: '$312 · conviction', level: 'stop $39.20', why: ['Fresh DoD award, bookings tripling. A momentum story it will pay up for.', 'Wide stop by design — a conviction hold, not a rental.'] },
          { id: 'soxl', col: 2, kind: 'armed', label: 'SOXL', sub: 'waiting · $150', name: 'Direxion Semi Bull 3×', verdict: 'buy', size: 'would deploy $150', level: 'trigger $31.20', why: ['Armed for a clean cross of $31.20 with the semis tape confirming.', 'On trigger a stop attaches at $27.00 — risk defined before entry.'] },
        ],
        edges: [
          { from: 'tqqq', to: 'trail', kind: 'up', cond: 'holds > $68.50 → trail', hot: true }, { from: 'tqqq', to: 'stop', kind: 'stop', cond: 'breaks $68.50 → flat' },
          { from: 'ionq', to: 'trail', kind: 'up', cond: 'holds > $39.20' }, { from: 'ionq', to: 'stop', kind: 'stop', cond: 'breaks $39.20 → flat' },
          { from: 'soxl', to: 'buy', kind: 'up', cond: 'crosses $31.20 → BUY $150' }, { from: 'soxl', to: 'cash', kind: 'idle', cond: 'no trigger → cash' },
        ],
        terminals: [
          { id: 'buy', kind: 'up', label: 'NEW HIGH / add', detail: ['A fresh high confirms strength — the engine adds to the winner and ratchets the trailing stop up behind it.', 'e.g. SOXL clears $31.20 → BUY $150, protective stop set at $27.00.'] },
          { id: 'trail', kind: 'up', label: 'keep trailing', detail: ['Holding above its stop — nothing to do but let it run. The stop ratchets up under the rising price, locking in gains.', 'e.g. TQQQ stop lifted to $69.10, up +4.2% on the position and climbing.'] },
          { id: 'stop', kind: 'stop', label: 'STOPPED OUT', detail: ['Price broke the line — the position closes flat, automatically, no debate.', 'e.g. TQQQ breaks $68.50 → exit; the clipped move cost the book about −1.4%.'] },
          { id: 'cash', kind: 'idle', label: 'SITTING CASH', detail: ['No trigger hit, so capital stays in cash rather than force a trade.', 'Dry powder is a position — ~15% held back, ready for the next setup.'] },
        ],
      };
    }
  }
  customElements.define('decision-flow', DecisionFlow);
})();
