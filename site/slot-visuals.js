/* slot-visuals.js — web components for the Agentic Trading slot skin
   <hero-3d>       real Three.js extruded metallic number w/ parallax
   <equity-chart>  canvas equity curve with hover detail
   <particle-field> bubbles-up (green day) / ash-down (red day)
*/
(() => {
  if (customElements.get('hero-3d')) return;

  /* ---------- shared three.js loader ---------- */
  const loadScript = (src) => new Promise((res, rej) => {
    const s = document.createElement('script');
    s.src = src; s.onload = res; s.onerror = () => rej(new Error('failed ' + src));
    document.head.appendChild(s);
  });

  let threePromise = null;
  function ensureThree() {
    if (!threePromise) threePromise = (async () => {
      if (!window.THREE) await loadScript('https://unpkg.com/three@0.128.0/build/three.min.js');
      if (!window.opentype) await loadScript('https://unpkg.com/opentype.js@1.3.4/dist/opentype.min.js');
      // light-weight geometric font, parsed to real outlines for extrusion
      const buf = await fetch('https://cdn.jsdelivr.net/npm/@expo-google-fonts/outfit/Outfit_300Light.ttf').then(r => r.arrayBuffer());
      return opentype.parse(buf);
    })();
    return threePromise;
  }

  function makeEnv(renderer, rims, metalHex) {
    const W = 1024, H = 512;
    const c = document.createElement('canvas'); c.width = W; c.height = H;
    const g = c.getContext('2d');
    const m = new THREE.Color(metalHex || '#ffffff');
    const tint = (l, mix) => {
      const col = new THREE.Color(l, l, l).lerp(new THREE.Color(m.r * l * 2.2, m.g * l * 2.2, m.b * l * 2.2), mix);
      return '#' + col.getHexString();
    };
    // near-black backdrop — the band the front faces mirror stays essentially black (silhouette)
    const grad = g.createLinearGradient(0, 0, 0, H);
    grad.addColorStop(0, tint(0.004, 0.5)); grad.addColorStop(0.46, tint(0.02, 0.6));
    grad.addColorStop(0.5, tint(0.055, 0.7)); grad.addColorStop(0.54, tint(0.018, 0.6));
    grad.addColorStop(1, tint(0.002, 0.5));
    g.fillStyle = grad; g.fillRect(0, 0, W, H);
    // soft elliptical light panel (studio softbox)
    const panel = (x, y, w, h, color, a) => {
      g.save(); g.translate(x, y); g.scale(w, h);
      const rg = g.createRadialGradient(0, 0, 0, 0, 0, 1);
      rg.addColorStop(0, color); rg.addColorStop(0.5, color); rg.addColorStop(1, 'rgba(0,0,0,0)');
      g.globalAlpha = a; g.fillStyle = rg;
      g.beginPath(); g.arc(0, 0, 1, 0, 7); g.fill();
      g.restore(); g.globalAlpha = 1;
    };
    // saturated color panels ONLY at the extreme top/bottom bands — caught by bevels and
    // grazing edges, never mirrored by the camera-facing faces
    rims.forEach((col, i) => {
      const x = (0.06 + (i / Math.max(1, rims.length)) * 0.94) * W;
      panel(x, H * (i % 2 ? 0.06 : 0.94), 220, 58, col, 1);
      panel(W - x, H * (i % 2 ? 0.95 : 0.05), 170, 48, col, 0.9);
    });
    const tex = new THREE.CanvasTexture(c);
    tex.mapping = THREE.EquirectangularReflectionMapping;
    const pm = new THREE.PMREMGenerator(renderer);
    const env = pm.fromEquirectangular(tex).texture;
    pm.dispose(); tex.dispose();
    return env;
  }

  /* ---------- <hero-3d> ---------- */
  class Hero3D extends HTMLElement {
    static get observedAttributes() { return ['value', 'metal', 'rims', 'rim1', 'rim2', 'rim3']; }
    _rims() {
      const r = this.getAttribute('rims');
      if (r) return r.split(',').map(s => s.trim()).filter(Boolean);
      return [this.getAttribute('rim1') || '#22d3ee', this.getAttribute('rim2') || '#a78bfa', this.getAttribute('rim3') || '#34d399'];
    }
    connectedCallback() {
      if (this._init) return; this._init = true;
      this.style.display = 'block';
      if (this.getAttribute('height')) this.style.height = this.getAttribute('height') + 'px';
      this.style.position = 'relative';
      this._canvas = document.createElement('canvas');
      Object.assign(this._canvas.style, { width: '100%', height: '100%', display: 'block' });
      this.appendChild(this._canvas);
      // cheap real bloom: half-res blurred additive copy of the render
      this._bloom = document.createElement('canvas');
      const boostAmt = parseFloat(this.getAttribute('boost') || '0');
      Object.assign(this._bloom.style, { position: 'absolute', inset: '0', width: '100%', height: '100%', pointerEvents: 'none', mixBlendMode: 'plus-lighter', filter: boostAmt ? 'blur(11px) brightness(1.4) contrast(1.5)' : 'blur(8px) brightness(1.25) contrast(1.7)' });
      this.appendChild(this._bloom);
      this._lightTarget = { x: 0, y: 1.5 };
      this._lastPointer = 0; this._visible = true;
      this._canvas.addEventListener('webglcontextlost', (e) => { e.preventDefault(); this._releaseGL(); }, false);
      this._watch();
    }
    // GL lifecycle: boot only when near the viewport, release after sustained off-screen time.
    // Keeps concurrent WebGL contexts under the browser cap no matter how many options stack up.
    _watch() {
      const check = () => {
        this._wraf = requestAnimationFrame(check);
        this._wfc = ((this._wfc || 0) + 1) % 30;
        if (this._wfc !== 1) return;
        const rct = this.getBoundingClientRect();
        const vis = rct.bottom > -300 && rct.top < innerHeight + 300 && rct.width > 0;
        if (vis) {
          this._offN = 0;
          if (!this._renderer && !this._booting) this._boot();
        } else if (this._renderer) {
          this._offN = (this._offN || 0) + 1;
          if (this._offN > 14) this._releaseGL(); // ~7s far off-screen → free the context
        }
      };
      check();
    }
    _releaseGL() {
      cancelAnimationFrame(this._raf);
      this._ro && this._ro.disconnect();
      if (this._moveScope && this._onMove) { this._moveScope.removeEventListener('pointermove', this._onMove); this._moveScope = null; }
      if (this._renderer) {
        this._renderer.dispose();
        this._renderer.forceContextLoss && this._renderer.forceContextLoss();
        this._renderer = null;
      }
      this._geoCache = null;
      this._prevText = null;
    }
    async _boot() {
      this._booting = true;
      try {
        const font = await ensureThree();
        this._font = font;
        const r = new THREE.WebGLRenderer({ canvas: this._canvas, antialias: true, alpha: true });
        r.setPixelRatio(Math.min(window.devicePixelRatio || 1, 1.5));
        r.outputEncoding = THREE.sRGBEncoding;
        r.toneMapping = THREE.ACESFilmicToneMapping;
        r.toneMappingExposure = 1.0;
        this._renderer = r;
        this._scene = new THREE.Scene();
        this._camera = new THREE.PerspectiveCamera(32, 2, 0.1, 100);
        this._group = new THREE.Group();
        this._scene.add(this._group);
        this._buildLights();
        this._env = makeEnv(r, this._rims(), this.getAttribute('metal') || '#ffffff');
        this._buildText();
        this._resize();
        this._ro = new ResizeObserver(() => this._resize());
        this._ro.observe(this);
        const scope = this.closest('[data-hero-scope]') || this;
        this._moveScope = scope;
        this._onMove = (e) => {
          const b = this.getBoundingClientRect();
          const px = ((e.clientX - b.left) / b.width) * 2 - 1;
          const py = ((e.clientY - b.top) / b.height) * 2 - 1;
          // mouse drives the sweep light, not the geometry
          this._lightTarget.x = Math.max(-1.4, Math.min(1.4, px)) * 7;
          this._lightTarget.y = -Math.max(-2, Math.min(2, py)) * 3.5;
          this._lastPointer = performance.now();
        };
        scope.addEventListener('pointermove', this._onMove);
        this._t0 = performance.now();
        const loop = () => {
          this._raf = requestAnimationFrame(loop);
          // IntersectionObserver is unreliable under the host's pan/zoom transforms — poll the rect
          this._fcv = ((this._fcv || 0) + 1) % 30;
          if (this._fcv === 1) {
            const rct = this.getBoundingClientRect();
            this._visible = rct.bottom > -120 && rct.top < innerHeight + 120 && rct.width > 0;
          }
          if (!this._visible || !this._renderer) return;
          const t = (performance.now() - this._t0) / 1000;
          // static pose; only a very slow ambient sway so the edges glint
          this._group.rotation.y = Math.sin(t * 0.22) * 0.05;
          this._group.rotation.x = -0.025 + Math.sin(t * 0.16 + 1) * 0.018;
          if (this._orbit) for (const o of this._orbit) {
            const a = o.phase + t * o.speed;
            o.L.position.set(
              Math.sin(a) * o.rad,
              o.y + Math.sin(t * 0.2 + o.phase) * 1.2,
              -(1.0 + o.rad * (0.4 + 0.4 * Math.cos(a))));
          }
          if (this._sweep) {
            const idle = performance.now() - this._lastPointer > 2500;
            const tx = idle ? Math.sin(t * 0.4) * 5 : this._lightTarget.x;
            const ty = idle ? 1.5 + Math.sin(t * 0.27) * 1.5 : this._lightTarget.y;
            this._sweep.position.x += (tx - this._sweep.position.x) * 0.08;
            this._sweep.position.y += (ty - this._sweep.position.y) * 0.08;
          }
          if (this._anims && this._anims.length) {
            const now2 = performance.now();
            this._anims = this._anims.filter((a) => {
              const p = (now2 - a.t0) / a.dur;
              if (p < 0) { a.m.visible = false; return true; }
              a.m.visible = true;
              const dir = this._animDir || 1;
              if (p >= 1) { a.m.rotation.x = 0; a.m.scale.set(1, 1, 1); a.m.position.y = a.m.userData.baseY || 0; return false; }
              const e = 1 + 2.70158 * Math.pow(p - 1, 3) + 1.70158 * Math.pow(p - 1, 2);
              a.m.rotation.x = -dir * 1.35 * (1 - e);
              a.m.position.y = (a.m.userData.baseY || 0) - dir * 0.42 * (1 - e);
              const s2 = 0.85 + 0.15 * e;
              a.m.scale.set(s2, s2, s2);
              return true;
            });
          }
          if (this._flash && this._flashL) {
            const p2 = (performance.now() - this._flash.t0) / this._flash.dur;
            if (p2 >= 1) { this._flashL.intensity = 0; this._flash = null; }
            else this._flashL.intensity = 32 * Math.pow(1 - p2, 2);
          }
          this._renderer.render(this._scene, this._camera);
          window.__hb = performance.now();
          // bloom copy: 30fps, quarter res, no canvas-2d filter — the CSS filter blurs/thresholds on the GPU
          this._fc = (this._fc || 0) + 1;
          if (!(this._fc & 1)) {
            const bw = Math.max(1, (this.clientWidth / 2) | 0), bh = Math.max(1, (this.clientHeight / 2) | 0);
            if (this._bloom.width !== bw || this._bloom.height !== bh) { this._bloom.width = bw; this._bloom.height = bh; }
            const bg2 = this._bloom.getContext('2d');
            bg2.clearRect(0, 0, bw, bh);
            bg2.globalAlpha = 0.8;
            bg2.drawImage(this._canvas, 0, 0, bw, bh);
          }
        };
        loop();
        this._booting = false;
      } catch (err) {
        this._booting = false;
        console.warn('hero-3d fallback:', err);
        this._fallback();
      }
    }
    _buildLights() {
      const S = this._scene;
      // entirely rim-lit: saturated colored lights that slowly ORBIT the text, always behind it
      const cols = this._rims().map(c => new THREE.Color(c));
      const boost = parseFloat(this.getAttribute('boost') || '0');
      this._orbit = [];
      cols.forEach((c, i) => {
        const L = new THREE.PointLight(c, 13 * (1 + boost * 0.4), 0);
        S.add(L);
        this._orbit.push({ L, phase: (i / cols.length) * Math.PI * 2, speed: 0.1 + 0.045 * (i % 3), rad: 6 + (i % 2) * 2, y: [2.2, -1.8, 3.4, -2.8, 1.2][i % 5] });
      });
      if (boost) {
        // outer ring: farther out and farther behind — broad gleam without frontal fill
        cols.forEach((c, i) => {
          const L = new THREE.PointLight(c, 20 * boost, 0);
          S.add(L);
          this._orbit.push({ L, phase: (i / cols.length) * Math.PI * 2 + 0.9, speed: 0.055 + 0.03 * (i % 2), rad: 12 + (i % 3) * 3, y: [4.5, -4, 6, -5.5, 3][i % 5] });
        });
      }
      S.add(new THREE.AmbientLight(0x181c2a, 0.5));
      // mouse sweep light — colored, and BEHIND the text
      this._sweep = new THREE.PointLight(cols[0], 1.6, 0);
      this._sweep.position.set(0, 1.5, -3);
      S.add(this._sweep);
      // tick flash: green/red rim burst behind the text when the value changes
      this._flashL = new THREE.PointLight(new THREE.Color('#34d399'), 0, 0);
      this._flashL.position.set(0, 2.5, -2.5);
      S.add(this._flashL);
    }
    _charGeo(ch) {
      this._geoCache = this._geoCache || {};
      if (this._geoCache[ch]) return this._geoCache[ch];
      const font = this._font;
      const glyph = font.charToGlyph(ch);
      const p = glyph.getPath(0, 0, 1);
      const sp = new THREE.ShapePath();
      for (const c of p.commands) {
        if (c.type === 'M') sp.moveTo(c.x, -c.y);
        else if (c.type === 'L') sp.lineTo(c.x, -c.y);
        else if (c.type === 'C') sp.bezierCurveTo(c.x1, -c.y1, c.x2, -c.y2, c.x, -c.y);
        else if (c.type === 'Q') sp.quadraticCurveTo(c.x1, -c.y1, c.x, -c.y);
      }
      // TrueType convention: after our y-flip, solid contours wind CCW (positive area),
      // holes wind CW. Orientation decides solid/hole (robust to overlapping contours like
      // the $'s bar); containment only assigns each hole to its smallest enclosing solid.
      const entries = sp.subPaths.map((p2) => ({ path: p2, pts: p2.getPoints(12) })).filter((e2) => e2.pts.length > 2);
      const area = (q2) => { let a2 = 0; for (let i = 0; i < q2.length; i++) { const r2 = q2[(i + 1) % q2.length]; a2 += q2[i].x * r2.y - r2.x * q2[i].y; } return a2 / 2; };
      const inside = (pt, poly) => { let c2 = false; for (let i = 0, j = poly.length - 1; i < poly.length; j = i++) { if ((poly[i].y > pt.y) !== (poly[j].y > pt.y) && pt.x < ((poly[j].x - poly[i].x) * (pt.y - poly[i].y)) / (poly[j].y - poly[i].y) + poly[i].x) c2 = !c2; } return c2; };
      const solids = [], holesArr = [];
      let dom = 0;
      entries.forEach((e2) => { e2.area = area(e2.pts); if (Math.abs(e2.area) > Math.abs(dom)) dom = e2.area; });
      // the largest contour is always solid — its winding defines "solid" for this glyph
      entries.forEach((e2) => { ((e2.area > 0) === (dom > 0) ? solids : holesArr).push(e2); });
      if (!solids.length && entries.length) {
        entries.sort((x2, y2) => Math.abs(y2.area) - Math.abs(x2.area));
        solids.push(entries[0]); holesArr.length = 0; entries.slice(1).forEach((e2) => holesArr.push(e2));
      }
      const shapes = solids.map((e2) => { const shp = new THREE.Shape(); shp.curves = e2.path.curves; shp._pts = e2.pts; shp._a = Math.abs(e2.area); return shp; });
      holesArr.forEach((h2) => {
        const cands = shapes.filter((s5) => inside(h2.pts[0], s5._pts));
        if (!cands.length) return;
        cands.sort((x2, y2) => x2._a - y2._a);
        cands[0].holes.push(h2.path);
      });
      const geo = new THREE.ExtrudeGeometry(shapes, { depth: 0.2, bevelEnabled: true, bevelThickness: 0.034, bevelSize: 0.018, bevelSegments: 4, curveSegments: 10 });
      geo.computeBoundingBox();
      const out = { geo, adv: glyph.advanceWidth / font.unitsPerEm };
      this._geoCache[ch] = out;
      return out;
    }
    _buildText() {
      const G = this._group;
      while (G.children.length) G.remove(G.children[0]);
      this._anims = [];
      const text = this.getAttribute('value') || '$0.00';
      const mat = new THREE.MeshStandardMaterial({
        color: new THREE.Color(this.getAttribute('metal') || '#ffffff'),
        metalness: 1.0, roughness: 0.07,
        envMap: this._env, envMapIntensity: 1.5,
      });
      let x = 0; const tracking = 0.02;
      const meshes = [];
      for (const ch of text) {
        if (ch === ' ') { x += 0.3; continue; }
        const { geo, adv } = this._charGeo(ch);
        const mesh = new THREE.Mesh(geo, mat);
        mesh.position.x = x;
        mesh.userData.ch = ch;
        meshes.push(mesh); G.add(mesh);
        x += adv + tracking;
      }
      const total = x - tracking;
      // center group horizontally + vertically on cap height
      const box = new THREE.Box3().setFromObject(G);
      const cy = (box.max.y + box.min.y) / 2;
      meshes.forEach(m => { m.position.x -= total / 2; m.position.y -= cy; m.userData.baseY = m.position.y; });
      this._textWidth = total;
      // reel-roll animation for digits that changed (right-aligned diff, staggered)
      const old = this._prevText; this._prevText = text;
      if (old && old !== text) {
        const num = (s3) => parseFloat(s3.replace(/[^0-9.]/g, '')) || 0;
        const dir = num(text) >= num(old) ? 1 : -1;
        this._animDir = dir;
        const oldR = [...old].filter(c2 => c2 !== ' ').reverse();
        [...meshes].reverse().forEach((m2, i) => {
          if (oldR[i] !== m2.userData.ch) this._anims.push({ m: m2, t0: performance.now() + i * 45, dur: 620 });
        });
        if (this._flashL && this._anims.length) {
          this._flashL.color.set(dir > 0 ? '#34d399' : '#f87171');
          this._flash = { t0: performance.now(), dur: 1500 };
        }
      }
      this._frame();
    }
    _frame() {
      if (!this._camera || !this._textWidth) return;
      const aspect = this._camera.aspect || 2;
      const fov = (this._camera.fov * Math.PI) / 180;
      const halfW = this._textWidth / 2 * 1.01;
      const dist = halfW / (Math.tan(fov / 2) * aspect) + 1.2;
      const minDist = (0.75 / Math.tan(fov / 2)) + 1.2; // don't crop cap-height
      this._camera.position.set(0, 0, Math.max(dist, minDist));
      this._camera.lookAt(0, 0, 0);
    }
    _resize() {
      if (!this._renderer) return;
      const w = this.clientWidth || 300, h = this.clientHeight || 150;
      this._renderer.setSize(w, h, false);
      this._camera.aspect = w / h;
      this._camera.updateProjectionMatrix();
      this._frame();
    }
    attributeChangedCallback(name) {
      if (!this._renderer || !this._font) return;
      if (name === 'value' || name === 'metal') this._buildText();
    }
    _fallback() {
      const v = this.getAttribute('value') || '$0.00';
      this.innerHTML = '';
      const d = document.createElement('div');
      d.textContent = v;
      Object.assign(d.style, {
        width: '100%', height: '100%', display: 'flex', alignItems: 'center', justifyContent: 'center',
        font: '300 96px/1 system-ui,-apple-system,sans-serif', letterSpacing: '2px',
        background: 'linear-gradient(175deg,#fdfdff 8%,#8d95a8 38%,#f4f6fb 50%,#5c6478 62%,#c9cfdd 92%)',
        WebkitBackgroundClip: 'text', backgroundClip: 'text', color: 'transparent',
      });
      this.appendChild(d);
    }
    disconnectedCallback() {
      cancelAnimationFrame(this._raf);
      cancelAnimationFrame(this._wraf);
      this._ro && this._ro.disconnect(); this._io && this._io.disconnect();
      this._releaseGL();
      this._init = false;
    }
  }
  customElements.define('hero-3d', Hero3D);

  /* ---------- seeded rng ---------- */
  function mulberry32(seed) {
    let a = seed >>> 0;
    return () => {
      a |= 0; a = (a + 0x6D2B79F5) | 0;
      let t = Math.imul(a ^ (a >>> 15), 1 | a);
      t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
      return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
    };
  }
  const hashStr = (s) => { let h = 2166136261; for (let i = 0; i < s.length; i++) { h ^= s.charCodeAt(i); h = Math.imul(h, 16777619); } return h >>> 0; };

  /* ---------- <equity-chart> ---------- */
  class EquityChart extends HTMLElement {
    static get observedAttributes() { return ['range', 'trend', 'accent', 'down', 'tracer']; }
    connectedCallback() {
      if (this._init) return; this._init = true;
      this.style.display = 'block';
      if (this.getAttribute('height')) this.style.height = this.getAttribute('height') + 'px';
      this._canvas = document.createElement('canvas');
      Object.assign(this._canvas.style, { width: '100%', height: '100%', display: 'block' });
      this.appendChild(this._canvas);
      this._hover = null;
      this._canvas.addEventListener('pointermove', (e) => {
        const b = this._canvas.getBoundingClientRect();
        this._hover = (e.clientX - b.left) / b.width;
        this._draw();
      });
      this._canvas.addEventListener('pointerleave', () => { this._hover = null; this._draw(); });
      this._ro = new ResizeObserver(() => this._draw());
      this._ro.observe(this);
      this._visible = true;
      this._t0 = performance.now();
      this._gen();
      const loop = () => {
        this._raf = requestAnimationFrame(loop);
        this._fc = (this._fc || 0) + 1;
        if (this._fc % 30 === 1) {
          const rct = this.getBoundingClientRect();
          this._visible = rct.bottom > -120 && rct.top < innerHeight + 120 && rct.width > 0;
        }
        if (this._fc & 1) return; // tracer at 30fps — halves full-chart redraw cost
        if (this._visible && this.getAttribute('tracer')) {
          this._tracerT = ((performance.now() - this._t0) / 15000) % 1;
          this._draw();
        }
      };
      requestAnimationFrame(loop);
      this._draw();
    }
    attributeChangedCallback() { if (this._init) { this._gen(); this._draw(); } }
    // ── REAL-DATA SEAM ──────────────────────────────────────────────
    // Push live equity points: el.setData([1351.2, 1352.0, …], '1D').
    // Pass an array of dollar values (any length ≥2). Re-call on every range switch
    // and whenever new candles arrive. Clears the synthetic fallback.
    setData(points, range) {
      if (!Array.isArray(points) || points.length < 2) return;
      this._real = points.slice();
      if (range != null) this._range = range;
      this._pts = this._real;
      this._static = null;
      if (this._init) this._draw();
    }
    _gen() {
      if (this._real) { this._pts = this._real; this._range = this.getAttribute('range') || this._range || '1D'; this._static = null; return; }
      const range = this.getAttribute('range') || '1D';
      const trend = this.getAttribute('trend') || 'up';
      const rnd = mulberry32(hashStr(range + trend));
      const n = 120, pts = [];
      const drift = trend === 'up' ? 0.9 : -0.9;
      let v = trend === 'up' ? 1351 : 1499;
      for (let i = 0; i < n; i++) {
        v += drift + (rnd() - 0.5) * 14 + Math.sin(i / 9) * 1.6;
        pts.push(v);
      }
      // pin the end to the live value
      const end = 1437.52, off = end - pts[n - 1];
      this._pts = pts.map((p, i) => p + off * (i / (n - 1)));
      this._range = range;
      this._static = null;
    }
    // curve point in the chart's own (unscaled) CSS-pixel space, for particle emitters
    curveLocal(t) {
      if (!this._pts) return null;
      const w = this.clientWidth, h = this.clientHeight;
      if (!w) return null;
      const pts = this._pts, n = pts.length;
      const min = Math.min(...pts), max = Math.max(...pts), pad = (max - min) * 0.14 || 1;
      const i = t * (n - 1), i0 = Math.floor(i), i1 = Math.min(i0 + 1, n - 1), fr = i - i0;
      const v = pts[i0] + (pts[i1] - pts[i0]) * fr;
      const x = (i / (n - 1)) * (w - 4) + 2;
      const y = h - 26 - ((v - (min - pad)) / ((max + pad) - (min - pad))) * (h - 44);
      return { x, y };
    }
    // static layer (axes + area + glow line) cached offscreen — redrawn only on data/size change
    _accent() {
      return this.getAttribute('trend') === 'down'
        ? (this.getAttribute('down') || '#f87171')
        : (this.getAttribute('accent') || '#34d399');
    }
    _geomFns(w, h) {
      const pts = this._pts, n = pts.length;
      const min = Math.min(...pts), max = Math.max(...pts), pad = (max - min) * 0.14 || 1;
      const X = (i) => (i / (n - 1)) * (w - 4) + 2;
      const Y = (v) => h - 26 - ((v - (min - pad)) / ((max + pad) - (min - pad))) * (h - 44);
      return { pts, n, min, max, pad, X, Y };
    }
    _drawStatic(w, h, dpr) {
      const off = document.createElement('canvas');
      off.width = w * dpr; off.height = h * dpr;
      const g = off.getContext('2d');
      g.setTransform(dpr, 0, 0, dpr, 0, 0);
      const accent = this._accent();
      const { pts, n, min, max, pad, X, Y } = this._geomFns(w, h);
      // x-axis time labels
      const XL = {
        '1H': ['10:05', '10:20', '10:35', '10:50', '11:05'],
        '1D': ['9:30', '11:00', '12:30', '2:00', '3:30'],
        '1W': ['Mon', 'Tue', 'Wed', 'Thu', 'Fri'],
        '1M': ['Jun 13', 'Jun 20', 'Jun 27', 'Jul 4', 'Jul 11'],
        '6M': ['Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul'],
        '1Y': ['Aug', 'Oct', 'Dec', 'Feb', 'Apr', 'Jun'],
      }[this._range || '1D'] || [];
      g.font = '400 13px system-ui, sans-serif';
      g.fillStyle = 'rgba(255,255,255,0.32)';
      g.textAlign = 'left'; g.textBaseline = 'alphabetic';
      XL.forEach((lb, i) => {
        g.fillText(lb, 8 + (i / (XL.length - 1)) * (w - 70), h - 6);
      });
      // y-axis dollar labels, right edge
      g.textAlign = 'right';
      [0.8, 0.5, 0.2].forEach((f) => {
        const v = (min - pad) + f * ((max + pad) - (min - pad));
        g.fillText('$' + Math.round(v).toLocaleString('en-US'), w - 6, Y(v) + 4);
      });
      g.textAlign = 'left';
      // area
      const path = new Path2D();
      path.moveTo(X(0), Y(pts[0]));
      for (let i = 1; i < n; i++) {
        const x0 = X(i - 1), y0 = Y(pts[i - 1]), x1 = X(i), y1 = Y(pts[i]);
        path.bezierCurveTo((x0 + x1) / 2, y0, (x0 + x1) / 2, y1, x1, y1);
      }
      const fill = new Path2D(path);
      fill.lineTo(X(n - 1), h); fill.lineTo(X(0), h); fill.closePath();
      const gr = g.createLinearGradient(0, 0, 0, h);
      gr.addColorStop(0, accent + '44'); gr.addColorStop(1, accent + '00');
      g.fillStyle = gr; g.fill(fill);
      // thin, light stroke — keeps the glow but reads higher-resolution
      g.save();
      g.shadowColor = accent; g.shadowBlur = 12;
      g.strokeStyle = accent; g.lineWidth = 1.6; g.lineJoin = 'round'; g.stroke(path);
      g.restore();
      const ex = X(n - 1), ey = Y(pts[n - 1]);
      g.fillStyle = accent; g.beginPath(); g.arc(ex, ey, 4, 0, 7); g.fill();
      g.fillStyle = '#fff'; g.beginPath(); g.arc(ex, ey, 1.8, 0, 7); g.fill();
      this._static = off;
    }
    _draw() {
      if (!this._pts) return;
      const c = this._canvas, dpr = Math.min(window.devicePixelRatio || 1, 2);
      const w = this.clientWidth || 300, h = this.clientHeight || 150;
      if (c.width !== w * dpr || c.height !== h * dpr) { c.width = w * dpr; c.height = h * dpr; this._static = null; }
      if (!this._static) this._drawStatic(w, h, dpr);
      const g = c.getContext('2d');
      g.setTransform(1, 0, 0, 1, 0, 0);
      g.clearRect(0, 0, c.width, c.height);
      g.drawImage(this._static, 0, 0);
      g.setTransform(dpr, 0, 0, dpr, 0, 0);
      const accent = this._accent();
      const { pts, n, X, Y } = this._geomFns(w, h);
      // hover
      if (this._hover != null) {
        const i = Math.round(this._hover * (n - 1));
        const hx = X(i), hy = Y(pts[i]);
        g.strokeStyle = 'rgba(255,255,255,0.25)'; g.setLineDash([4, 5]); g.lineWidth = 1;
        g.beginPath(); g.moveTo(hx, 8); g.lineTo(hx, h - 22); g.stroke(); g.setLineDash([]);
        g.fillStyle = accent; g.beginPath(); g.arc(hx, hy, 5, 0, 7); g.fill();
        const label = '$' + pts[i].toFixed(2);
        g.font = '600 15px ui-monospace, Menlo, monospace';
        const tw = g.measureText(label).width + 20;
        let bx = Math.min(Math.max(hx - tw / 2, 4), w - tw - 4);
        const by = Math.max(hy - 44, 4);
        g.fillStyle = 'rgba(12,14,22,0.92)'; g.strokeStyle = 'rgba(255,255,255,0.14)';
        g.beginPath(); g.roundRect(bx, by, tw, 28, 8); g.fill(); g.stroke();
        g.fillStyle = '#fff'; g.textBaseline = 'middle';
        g.fillText(label, bx + 10, by + 15);
      }
      // tracing point of light crawling the curve
      const tracer = this.getAttribute('tracer');
      if (tracer && this._tracerT != null) {
        const at = (fi) => {
          const i0 = Math.max(0, Math.floor(fi)), i1 = Math.min(i0 + 1, n - 1), fr = fi - i0;
          return [X(i0) + (X(i1) - X(i0)) * fr, Y(pts[i0]) + (Y(pts[i1]) - Y(pts[i0])) * fr];
        };
        const cfg = tracer === 'comet' ? { tail: 26, core: 2.6, glow: 24, head: '#eafcff' }
          : tracer === 'ember' ? { tail: 10, core: 2.4, glow: 20, head: '#fff3d6' }
          : { tail: 8, core: 2.1, glow: 13, head: '#ffffff' };
        const fi = this._tracerT * (n - 1);
        g.save(); g.globalCompositeOperation = 'lighter';
        for (let k = cfg.tail; k >= 1; k--) {
          const j = fi - k * 0.55; if (j < 0) continue;
          const [px, py] = at(j);
          const f = 1 - k / (cfg.tail + 1);
          g.globalAlpha = 0.4 * f * f;
          g.fillStyle = accent;
          g.beginPath(); g.arc(px, py, cfg.core * (0.35 + 0.65 * f) * 2, 0, 7); g.fill();
        }
        const [hx2, hy2] = at(fi);
        const flick = tracer === 'ember' ? 0.7 + Math.random() * 0.3 : 1;
        const gl2 = g.createRadialGradient(hx2, hy2, 0, hx2, hy2, cfg.glow);
        gl2.addColorStop(0, accent); gl2.addColorStop(1, 'rgba(0,0,0,0)');
        g.globalAlpha = 0.5 * flick; g.fillStyle = gl2;
        g.beginPath(); g.arc(hx2, hy2, cfg.glow, 0, 7); g.fill();
        g.globalAlpha = flick; g.fillStyle = cfg.head;
        g.beginPath(); g.arc(hx2, hy2, cfg.core, 0, 7); g.fill();
        // (the back-edge twin lives in the ribbon's 3D scene so the ridge can occlude it)
        g.restore(); g.globalAlpha = 1;
      }
    }
    disconnectedCallback() { cancelAnimationFrame(this._raf); this._ro && this._ro.disconnect(); this._io && this._io.disconnect(); this._init = false; }
  }
  customElements.define('equity-chart', EquityChart);

  /* ---------- <particle-field> ---------- */
  function sprite(color, r) {
    const c = document.createElement('canvas'); c.width = c.height = r * 4;
    const g = c.getContext('2d');
    const gr = g.createRadialGradient(r * 2, r * 2, 0, r * 2, r * 2, r * 2);
    gr.addColorStop(0, '#ffffff'); gr.addColorStop(0.22, color); gr.addColorStop(0.55, color + '66'); gr.addColorStop(1, color + '00');
    g.fillStyle = gr; g.fillRect(0, 0, r * 4, r * 4);
    return c;
  }
  class ParticleField extends HTMLElement {
    static get observedAttributes() { return ['mode', 'density']; }
    connectedCallback() {
      if (this._init) return; this._init = true;
      this.style.display = 'block';
      this.style.width = '100%';
      this.style.height = '100%';
      this.style.pointerEvents = 'none';
      this._canvas = document.createElement('canvas');
      Object.assign(this._canvas.style, { width: '100%', height: '100%', display: 'block' });
      this.appendChild(this._canvas);
      this._visible = true;
      this._ro = new ResizeObserver(() => {
        const w = this.clientWidth || 300, h = this.clientHeight || 300;
        if (Math.abs(w - (this._w || 0)) < 4 && Math.abs(h - (this._h || 0)) < 4) return;   // ignore no-op / sub-pixel resizes → no re-scatter pop
        clearTimeout(this._rt); this._rt = setTimeout(() => { if (this._init) this._reset(); }, 220);
      });
      this._ro.observe(this);
      this._reset();
      // re-lock to the curve once the equity chart has laid out — re-aim only, DON'T re-scatter (that was the pop)
      setTimeout(() => { if (this._init) this._chartEl = undefined; }, 1800);
      setTimeout(() => { if (this._init) this._chartEl = undefined; }, 4500);
      const loop = () => {
        this._raf = requestAnimationFrame(loop);
        this._pvc = ((this._pvc || 0) + 1) % 30;
        if (this._pvc === 1) {
          const rct = this.getBoundingClientRect();
          this._visible = rct.bottom > -120 && rct.top < innerHeight + 120 && rct.width > 0;
          if (!this._up) this._sampleCurve(); // keep the snow line locked to the graph as layout settles
        }
        if (this._visible) this._step();
      };
      loop();
    }
    attributeChangedCallback(name, oldV, newV) { if (this._init && oldV !== newV) this._reset(); }   // only re-scatter on a REAL up/down (or density) change, not on same-value re-sets every poll
    _reset() {
      const w = this.clientWidth || 300, h = this.clientHeight || 300;
      const dpr = Math.min(window.devicePixelRatio || 1, 1);
      this._w = w; this._h = h; this._dpr = dpr;
      this._canvas.width = w * dpr; this._canvas.height = h * dpr;
      const mode = this.getAttribute('mode') || 'up';
      const density = parseFloat(this.getAttribute('density') || '1');
      const up = mode === 'up';
      this._up = up;
      // green day → motes drift UP out of the curve; red day → ash FALLS and piles on the line
      const count = up
        ? Math.round((w * h) / 70000 * density)
        : Math.max(46, Math.round((w * h) / 34000 * density));
      const colors = up ? ['#34d399', '#6ee7b7', '#a7f3d0', '#10b981'] : ['#f87171', '#dc2626', '#ef4444', '#b91c1c'];
      this._sprites = colors.map(c => sprite(c, 8));
      // settled-snow sprites: frostier, lighter reds so the pile reads as accumulation, not more ash
      this._snowSprites = ['#fecaca', '#fca5a5', '#fda4af', '#fecdd3'].map(c => sprite(c, 8));
      // snow accumulation buckets across the width + the flakes resting on them
      this._nb = Math.max(24, Math.round(w / 14));
      this._pile = new Float32Array(this._nb);
      this._settled = [];
      this._chartEl = undefined;
      this._ps = Array.from({ length: count }, () => { const p = {}; this._spawn(p, true); return p; });
      this._sampleCurve();
    }
    _chart() {
      if (this._chartEl === undefined) {
        const scope = this.closest('[data-hero-scope]') || this.parentElement || document;
        this._chartEl = scope.querySelector('equity-chart') || null;
      }
      return this._chartEl;
    }
    // build a field-local polyline of the equity curve, so the snow knows where the line is
    _sampleCurve() {
      const chart = this._chart();
      if (!chart || !chart.curveLocal) { this._curve = null; return; }
      const cr = chart.getBoundingClientRect(), fr = this.getBoundingClientRect();
      if (!cr.width || !fr.width) { this._curve = null; return; }
      const scale = (fr.width / (this.clientWidth || 1)) || 1;
      const ox = (cr.left - fr.left) / scale, oy = (cr.top - fr.top) / scale;
      const N = 96, curve = new Array(N);
      for (let i = 0; i < N; i++) {
        const lp = chart.curveLocal(i / (N - 1));
        if (!lp) { this._curve = null; return; }
        curve[i] = { x: ox + lp.x, y: oy + lp.y };
      }
      this._curve = curve;
      this._cx0 = curve[0].x; this._cx1 = curve[N - 1].x;
    }
    // field-local y of the equity line at field-local x (clamped to the curve span)
    _curveYAt(x) {
      const c = this._curve; if (!c) return this._h * 0.62;
      const n = c.length;
      if (x <= this._cx0) return c[0].y;
      if (x >= this._cx1) return c[n - 1].y;
      const f = (x - this._cx0) / (this._cx1 - this._cx0) * (n - 1);
      const i0 = f | 0, i1 = Math.min(i0 + 1, n - 1), fr = f - i0;
      return c[i0].y + (c[i1].y - c[i0].y) * fr;
    }
    _bucket(x) { return Math.max(0, Math.min(this._nb - 1, (x / this._w * this._nb) | 0)); }
    _pileAt(x) {
      // blend neighbouring buckets so the snow surface is smooth, not stepped
      const b = this._bucket(x), p = this._pile;
      return (p[b] * 2 + p[Math.max(0, b - 1)] + p[Math.min(this._nb - 1, b + 1)]) / 4;
    }
    _spawn(p, initial) {
      const rnd = Math.random, w = this._w, h = this._h;
      if (this._up) {
        // emerge from the equity curve, drift upward (unchanged behaviour)
        let sx = rnd() * w, sy = h * (0.35 + rnd() * 0.4);
        const chart = this._chart();
        if (chart && chart.curveLocal) {
          const lp = chart.curveLocal(rnd());
          if (lp) {
            const cr = chart.getBoundingClientRect(), fr = this.getBoundingClientRect();
            const scale = (fr.width / (this.clientWidth || 1)) || 1;
            sx = (cr.left - fr.left) / scale + lp.x;
            sy = (cr.top - fr.top) / scale + lp.y;
          }
        }
        p.x = sx; p.y = sy - 2;
        if (initial) p.y -= rnd() * Math.max(0, p.y);
        p.r = 0.8 + rnd() * 1.4;
        p.vy = -(0.08 + rnd() * 0.2);
        p.wob = rnd() * Math.PI * 2; p.wobSp = 0.002 + rnd() * 0.006;
        p.drift = (rnd() - 0.5) * 0.14;
        p.a = 0.35 + rnd() * 0.5;
        p.s = (rnd() * this._sprites.length) | 0;
        p.fl = rnd() * Math.PI * 2;
      } else {
        // fall from above the line, gently swaying
        p.x = rnd() * w;
        const surf = this._curveYAt(p.x) - this._pileAt(p.x);
        p.y = initial ? rnd() * Math.max(10, surf - 6) : -8 - rnd() * 46;
        p.r = 1 + rnd() * 1.7;
        p.vy = 1.0 + rnd() * 1.1;
        p.wob = rnd() * Math.PI * 2; p.wobSp = 0.008 + rnd() * 0.02;
        p.sway = 0.28 + rnd() * 0.5;
        p.a = 0.5 + rnd() * 0.42;
        p.s = (rnd() * this._sprites.length) | 0;
      }
    }
    // a falling flake reaches the snow surface: raise the pile and drop a resting flake
    _deposit(x, surfaceY) {
      const b = this._bucket(x);
      const maxPile = Math.min(60, this._h * 0.14);
      const th = 1.6 + Math.random() * 1.4;
      if (this._pile[b] < maxPile) this._pile[b] += th;
      this._settled.push({
        x, y: surfaceY - Math.random() * 2, b, th,
        r: 1.2 + Math.random() * 1.8,
        s: (Math.random() * this._snowSprites.length) | 0,
        born: performance.now(),
        life: 4200 + Math.random() * 4200, // rest, then slowly melt — pile recedes as flakes age out
      });
      if (this._settled.length > 640) { const o = this._settled.shift(); this._pile[o.b] = Math.max(0, this._pile[o.b] - o.th); }
    }
    _step() {
      this._fc = (this._fc || 0) + 1;
      if (this._fc & 1) return; // 30fps is plenty for slow dust
      const g = this._canvas.getContext('2d');
      const { _w: w, _h: h, _dpr: dpr } = this;
      g.setTransform(dpr, 0, 0, dpr, 0, 0);
      g.clearRect(0, 0, w, h);
      if (this._up) this._stepUp(g); else this._stepDown(g);
    }
    _stepUp(g) {
      const { _w: w } = this;
      g.globalCompositeOperation = 'lighter';
      for (const p of this._ps) {
        p.y += p.vy;
        p.wob += p.wobSp;
        p.x += Math.sin(p.wob) * 0.16 + p.drift;
        p.fl += 0.03;
        if (p.y < -10) this._spawn(p, false);
        if (p.x < -20) p.x = w + 20; if (p.x > w + 20) p.x = -20;
        const spr = this._sprites[p.s], d = p.r * 4;
        g.globalAlpha = p.a * 0.35;
        g.drawImage(spr, p.x - d * 1.6, p.y - d * 1.6, d * 3.2, d * 3.2);
        g.globalAlpha = p.a;
        g.drawImage(spr, p.x - d / 2, p.y - d / 2, d, d);
      }
      g.globalAlpha = 1; g.globalCompositeOperation = 'source-over';
    }
    _stepDown(g) {
      const { _w: w, _h: h } = this;
      const now = performance.now();
      // 1) falling ash
      g.globalCompositeOperation = 'source-over';
      for (const p of this._ps) {
        p.vy = Math.min(4.0, p.vy + 0.025); // gentle acceleration
        p.y += p.vy;
        p.wob += p.wobSp;
        p.x += Math.sin(p.wob) * p.sway;
        if (p.x < 0) p.x = 0; else if (p.x > w) p.x = w;
        // land only once the curve is known; before that, fall off-screen and respawn
        const surf = this._curve ? this._curveYAt(p.x) - this._pileAt(p.x) : (h + 20);
        if (p.y >= surf) { this._deposit(p.x, surf); this._spawn(p, false); continue; }
        if (p.y > h + 10) { this._spawn(p, false); continue; }
        const spr = this._sprites[p.s], d = p.r * 4, a = p.a * (0.78 + Math.sin(p.wob) * 0.22);
        g.globalAlpha = a * 0.3;
        g.drawImage(spr, p.x - d, p.y - d, d * 2, d * 2);
        g.globalAlpha = a;
        g.drawImage(spr, p.x - d / 2, p.y - d / 2, d, d);
      }
      // 2) snow CRUST hugging the line — a frosty band from (line − pile) down to the line,
      //    so it visibly collects where ash has landed and recedes as flakes melt
      if (this._curve) {
        const step = Math.max(4, w / 120), top = [];
        for (let x = 0; x <= w; x += step) top.push([x, this._curveYAt(x) - this._pileAt(x)]);
        g.globalCompositeOperation = 'source-over';
        g.beginPath();
        g.moveTo(top[0][0], top[0][1]);
        for (let i = 1; i < top.length; i++) g.lineTo(top[i][0], top[i][1]);
        for (let x = w; x >= 0; x -= step) g.lineTo(x, this._curveYAt(x)); // back along the line → 0-height where no snow
        g.closePath();
        g.save();
        g.shadowColor = 'rgba(255,205,210,0.55)'; g.shadowBlur = 9;
        g.fillStyle = 'rgba(255,232,235,0.5)';
        g.fill();
        g.restore();
      }
      // 3) sparkle: the individual settled flakes on the crust, additive, fading with age
      g.globalCompositeOperation = 'lighter';
      const keep = [];
      for (const f of this._settled) {
        const age = now - f.born;
        if (age > f.life) { this._pile[f.b] = Math.max(0, this._pile[f.b] - f.th); continue; }
        keep.push(f);
        const fade = age < f.life * 0.65 ? 1 : 1 - (age - f.life * 0.65) / (f.life * 0.35);
        const spr = this._snowSprites[f.s], d = f.r * 4;
        g.globalAlpha = 0.6 * fade;
        g.drawImage(spr, f.x - d / 2, f.y - d / 2, d, d);
      }
      this._settled = keep;
      g.globalAlpha = 1; g.globalCompositeOperation = 'source-over';
    }
    disconnectedCallback() {
      cancelAnimationFrame(this._raf);
      this._ro && this._ro.disconnect(); this._io && this._io.disconnect();
      this._init = false;
    }
  }
  customElements.define('particle-field', ParticleField);

  /* ---------- <glass-rim> — liquid-glass edge: chromatic dispersion ring + mouse-tracked specular highlight ---------- */
  class GlassRim extends HTMLElement {
    connectedCallback() {
      if (this._init) return; this._init = true;
      const rad = (this.getAttribute('radius') || '28') + 'px';
      Object.assign(this.style, { position: 'absolute', inset: '0', pointerEvents: 'none', display: 'block', borderRadius: rad, zIndex: 3 });
      const ring = (bg) => {
        const d = document.createElement('div');
        Object.assign(d.style, {
          position: 'absolute', inset: '0', borderRadius: rad, padding: '1px', background: bg,
          WebkitMask: 'linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0)',
          WebkitMaskComposite: 'xor', maskComposite: 'exclude', pointerEvents: 'none',
        });
        this.appendChild(d); return d;
      };
      this._chroma = ring('conic-gradient(from 210deg, rgba(125,211,252,0.4), rgba(232,121,249,0.3), rgba(52,211,153,0.22), rgba(129,140,248,0.35), rgba(125,211,252,0.4))');
      this._chroma.style.opacity = '0.32';
      this._chroma.style.filter = 'blur(1.2px)';
      this._spec = ring('none');
      this._x = 0.5; this._y = -0.1; this._tx = 0.5; this._ty = -0.1;
      this._onMove = (e) => {
        const r = this.getBoundingClientRect();
        if (!r.width) return;
        this._tx = Math.max(-1.5, Math.min(2.5, (e.clientX - r.left) / r.width));
        this._ty = Math.max(-1.5, Math.min(2.5, (e.clientY - r.top) / r.height));
      };
      window.addEventListener('pointermove', this._onMove);
      const loop = () => {
        this._raf = requestAnimationFrame(loop);
        const dx = this._tx - this._x, dy = this._ty - this._y;
        if (Math.abs(dx) + Math.abs(dy) < 0.001) return;
        this._x += dx * 0.07; this._y += dy * 0.07;
        this._spec.style.background = 'radial-gradient(300px circle at ' + (this._x * 100).toFixed(1) + '% ' + (this._y * 100).toFixed(1) + '%, rgba(255,255,255,0.6), rgba(255,255,255,0.04) 62%, transparent 80%)';
      };
      loop();
    }
    disconnectedCallback() {
      cancelAnimationFrame(this._raf);
      window.removeEventListener('pointermove', this._onMove);
      this._init = false;
    }
  }
  customElements.define('glass-rim', GlassRim);

  /* ---------- <value-pill> — P&L pill that morphs width and slides text on live ticks ---------- */
  class ValuePill extends HTMLElement {
    static get observedAttributes() { return ['mode', 'text']; }
    connectedCallback() {
      if (this._init) return; this._init = true;
      this.style.display = 'inline-block';
      const wrap = this._wrap = document.createElement('div');
      Object.assign(wrap.style, {
        display: 'flex', alignItems: 'center', justifyContent: 'center',
        font: '700 16px/1 system-ui, sans-serif', letterSpacing: '1.5px', whiteSpace: 'nowrap',
        padding: this.getAttribute('pad') || '11px 22px', borderRadius: '999px', overflow: 'hidden',
        borderWidth: '1px', borderStyle: 'solid', boxSizing: 'border-box',
        transition: 'background 0.5s, color 0.5s, border-color 0.5s, box-shadow 0.5s, width 0.45s cubic-bezier(0.3, 1.2, 0.4, 1)',
      });
      const row = this._row = document.createElement('span');
      Object.assign(row.style, { display: 'inline-block', whiteSpace: 'pre' });
      wrap.appendChild(row);
      this.appendChild(wrap);
      wrap.style.fontVariantNumeric = 'tabular-nums';
      this._setStatic(this.getAttribute('text') || '');
      this._applyPalette((this.getAttribute('mode') || 'up') !== 'down');
      this._onTick = (e) => {
        if ((this.getAttribute('mode') || 'up') === 'down') return;
        this._update(e.detail.text, e.detail.up);
      };
      window.addEventListener('acct-tick', this._onTick);
    }
    _applyPalette(up) {
      const p = up ? 'up' : 'dn';
      // x-import delivers kebab attrs without hyphens (up-bg → upbg) — accept both
      const at = (n) => this.getAttribute(p + '-' + n) || this.getAttribute(p + n) || '';
      this._wrap.style.background = at('bg');
      this._wrap.style.color = at('fg');
      this._wrap.style.borderColor = at('border');
      if (this.getAttribute('glow')) this._wrap.style.boxShadow = '0 0 30px ' + (at('bg') || 'transparent');
    }
    _setStatic(text) {
      this._text = text;
      this._row.textContent = text;
    }
    _update(text, up) {
      const wrap = this._wrap, row = this._row;
      const old = this._text || '';
      const w0 = wrap.getBoundingClientRect().width;
      wrap.style.width = w0 + 'px';
      this._applyPalette(up);
      // odometer: only changed characters roll — up on gains, down on losses
      row.innerHTML = '';
      const cells = [];
      for (let i = 0; i < text.length; i++) {
        const nc = text[i], oc = old[i] || ' ';
        const s = document.createElement('span');
        s.style.display = 'inline-block';
        s.style.whiteSpace = 'pre';
        s.style.verticalAlign = 'top';
        if (nc === oc) { s.textContent = nc; row.appendChild(s); continue; }
        s.style.overflow = 'hidden';
        s.style.height = '1em';
        const col = document.createElement('span');
        col.style.display = 'inline-flex';
        col.style.flexDirection = 'column';
        const mk = (ch) => { const e = document.createElement('span'); e.textContent = ch; e.style.whiteSpace = 'pre'; e.style.height = '1em'; return e; };
        col.appendChild(mk(up ? oc : nc));
        col.appendChild(mk(up ? nc : oc));
        col.style.transform = up ? 'translateY(0)' : 'translateY(-1em)';
        col.style.transition = 'none';
        s.appendChild(col);
        row.appendChild(s);
        cells.push(col);
      }
      wrap.style.width = 'auto';
      const w1 = wrap.getBoundingClientRect().width;
      wrap.style.width = w0 + 'px';
      void wrap.offsetWidth;
      wrap.style.width = w1 + 'px';
      requestAnimationFrame(() => {
        cells.forEach((col, i) => {
          col.style.transition = 'transform 0.55s cubic-bezier(0.25, 1.1, 0.35, 1) ' + (i * 24) + 'ms';
          col.style.transform = up ? 'translateY(-1em)' : 'translateY(0)';
        });
      });
      this._text = text;
      clearTimeout(this._t1); clearTimeout(this._t2);
      this._t2 = setTimeout(() => { wrap.style.width = 'auto'; this._setStatic(text); }, 1100);
    }
    attributeChangedCallback() {
      if (!this._init) return;
      this._setStatic(this.getAttribute('text') || this._text || '');
      this._applyPalette((this.getAttribute('mode') || 'up') !== 'down');
    }
    disconnectedCallback() {
      window.removeEventListener('acct-tick', this._onTick);
      clearTimeout(this._t1); clearTimeout(this._t2);
      this._init = false;
    }
  }
  customElements.define('value-pill', ValuePill);

  /* ---------- <chrome-frames> — REAL 3D chrome borders around target cards.
     One WebGL scene per skin card (keeps context count low): finds every `.chrome-target`
     inside its parent, builds a beveled extruded rounded-rect ring per target with the
     EXACT hero material (metalness 1, roughness 0.07, same makeEnv), orbiting colored
     lights + bloom pass — genuine geometry, not a 2D effect. ---------- */
  class ChromeFrames extends HTMLElement {
    connectedCallback() {
      if (this._init) return; this._init = true;
      Object.assign(this.style, { display: 'block', position: 'absolute', inset: '0', pointerEvents: 'none', zIndex: 60 });
      this._canvas = document.createElement('canvas');
      Object.assign(this._canvas.style, { width: '100%', height: '100%', display: 'block' });
      this.appendChild(this._canvas);
      this._bloom = document.createElement('canvas');
      Object.assign(this._bloom.style, { position: 'absolute', inset: '0', width: '100%', height: '100%', pointerEvents: 'none', mixBlendMode: 'plus-lighter', filter: 'blur(8px) brightness(1.25) contrast(1.7)' });
      this.appendChild(this._bloom);
      this._canvas.addEventListener('webglcontextlost', (e) => { e.preventDefault(); this._releaseGL(); }, false);
      this._watch();
    }
    _rims() { return (this.getAttribute('rims') || '#a855f7,#f472b6,#2dd4bf').split(',').map(s => s.trim()); }
    _watch() {
      const check = () => {
        this._wraf = requestAnimationFrame(check);
        this._wfc = ((this._wfc || 0) + 1) % 30;
        if (this._wfc !== 1) return;
        const rct = this.getBoundingClientRect();
        const vis = rct.bottom > -300 && rct.top < innerHeight + 300 && rct.width > 0;
        if (vis) { this._offN = 0; if (!this._renderer && !this._booting) this._boot(); }
        else if (this._renderer) { this._offN = (this._offN || 0) + 1; if (this._offN > 14) this._releaseGL(); }
      };
      check();
    }
    _releaseGL() {
      cancelAnimationFrame(this._raf);
      this._ro && this._ro.disconnect();
      if (this._renderer) { this._renderer.dispose(); this._renderer.forceContextLoss && this._renderer.forceContextLoss(); this._renderer = null; }
      this._frameGroup = null;
    }
    _sig() {
      const my = this.getBoundingClientRect();
      if (!my.width) return '';
      const scale = my.width / (this.clientWidth || 1);
      return [...(this.closest('[data-hero-scope]') || this.parentElement || this).querySelectorAll('.chrome-target')].map(el => {
        const r = el.getBoundingClientRect();
        return [(r.left - my.left) / scale, (r.top - my.top) / scale, r.width / scale, r.height / scale].map(v => Math.round(v)).join(',');
      }).join(';');
    }
    async _boot() {
      this._booting = true;
      try {
        await ensureThree();
        const r = new THREE.WebGLRenderer({ canvas: this._canvas, antialias: true, alpha: true });
        r.setPixelRatio(Math.min(window.devicePixelRatio || 1, 1.25));
        r.outputEncoding = THREE.sRGBEncoding;
        r.toneMapping = THREE.ACESFilmicToneMapping;
        this._renderer = r;
        const S = this._scene = new THREE.Scene();
        this._camera = new THREE.OrthographicCamera(-1, 1, 1, -1, -3000, 3000);
        this._env = makeEnv(r, this._rims(), this.getAttribute('metal') || '#ffffff');
        this._mat = new THREE.MeshStandardMaterial({
          color: new THREE.Color(this.getAttribute('metal') || '#ffffff'),
          metalness: 1.0, roughness: 0.07, envMap: this._env, envMapIntensity: 1.5,
        });
        const cols = this._rims().map(c => new THREE.Color(c));
        this._orbit = [];
        cols.forEach((c, i) => {
          const L = new THREE.PointLight(c, 9, 0);
          S.add(L);
          this._orbit.push({ L, phase: (i / cols.length) * Math.PI * 2, speed: 0.09 + 0.04 * (i % 3), rad: (7 + (i % 3) * 3) * 60, y: [3, -2, 4.5, -3.5, 2][i % 5] * 60 });
        });
        S.add(new THREE.AmbientLight(0x181c2a, 0.5));
        this._resize();
        this._ro = new ResizeObserver(() => this._resize());
        this._ro.observe(this);
        this._t0 = performance.now();
        const loop = () => {
          this._raf = requestAnimationFrame(loop);
          if (!this._renderer) return;
          this._fc = (this._fc || 0) + 1;
          if (this._fc % 45 === 2) { const sg = this._sig(); if (sg !== this._lastSig) { this._lastSig = sg; this._buildFrames(); } }
          const t = (performance.now() - this._t0) / 1000;
          for (const o of this._orbit) {
            const a = o.phase + t * o.speed;
            o.L.position.set(Math.sin(a) * o.rad, o.y + Math.sin(t * 0.2 + o.phase) * 90, -180 - 160 * (0.5 + 0.5 * Math.cos(a)));
          }
          this._renderer.render(S, this._camera);
          if (!(this._fc & 1)) {
            const bw = Math.max(1, (this.clientWidth / 2) | 0), bh = Math.max(1, (this.clientHeight / 2) | 0);
            if (this._bloom.width !== bw) { this._bloom.width = bw; this._bloom.height = bh; }
            const bg2 = this._bloom.getContext('2d');
            bg2.clearRect(0, 0, bw, bh);
            bg2.globalAlpha = 0.8;
            bg2.drawImage(this._canvas, 0, 0, bw, bh);
          }
        };
        loop();
        this._booting = false;
      } catch (err) { this._booting = false; console.warn('chrome-frames fallback:', err); }
    }
    _rr(p, cx, cy, w2, h2, r2) {
      const l = cx - w2 / 2, b = cy - h2 / 2, rt = cx + w2 / 2, tp = cy + h2 / 2;
      p.moveTo(l + r2, b);
      p.lineTo(rt - r2, b); p.quadraticCurveTo(rt, b, rt, b + r2);
      p.lineTo(rt, tp - r2); p.quadraticCurveTo(rt, tp, rt - r2, tp);
      p.lineTo(l + r2, tp); p.quadraticCurveTo(l, tp, l, tp - r2);
      p.lineTo(l, b + r2); p.quadraticCurveTo(l, b, l + r2, b);
      return p;
    }
    _buildFrames() {
      if (!this._scene) return;
      if (this._frameGroup) {
        this._scene.remove(this._frameGroup);
        this._frameGroup.traverse(o => o.geometry && o.geometry.dispose());
      }
      const G = this._frameGroup = new THREE.Group();
      const W = this.clientWidth || 300, H = this.clientHeight || 300;
      const my = this.getBoundingClientRect();
      if (!my.width) return;
      const scale = my.width / W;
      const T = 4.5, rad = 18; // band thickness ~4.5px, matches the 16-18px card corners
      (this.closest('[data-hero-scope]') || this.parentElement || this).querySelectorAll('.chrome-target').forEach(el => {
        const rc = el.getBoundingClientRect();
        const rw = rc.width / scale, rh = rc.height / scale;
        const cx = (rc.left - my.left) / scale + rw / 2 - W / 2;
        const cy = H / 2 - ((rc.top - my.top) / scale + rh / 2);
        const shape = this._rr(new THREE.Shape(), cx, cy, rw + T, rh + T, rad + T / 2);
        shape.holes.push(this._rr(new THREE.Path(), cx, cy, rw - T, rh - T, Math.max(4, rad - T / 2)));
        const geo = new THREE.ExtrudeGeometry(shape, { depth: 5, bevelEnabled: true, bevelThickness: 2, bevelSize: 1.6, bevelSegments: 3, curveSegments: 8 });
        G.add(new THREE.Mesh(geo, this._mat));
      });
      this._scene.add(G);
    }
    _resize() {
      if (!this._renderer) return;
      const w = this.clientWidth || 300, h = this.clientHeight || 300;
      this._renderer.setSize(w, h, false);
      this._camera.left = -w / 2; this._camera.right = w / 2;
      this._camera.top = h / 2; this._camera.bottom = -h / 2;
      this._camera.position.set(0, 0, 600);
      this._camera.lookAt(0, 0, 0);
      this._camera.updateProjectionMatrix();
      this._lastSig = null;
    }
    disconnectedCallback() {
      cancelAnimationFrame(this._raf);
      cancelAnimationFrame(this._wraf);
      this._ro && this._ro.disconnect();
      this._releaseGL();
      this._init = false;
    }
  }
  customElements.define('chrome-frames', ChromeFrames);

  /* ---------- <chart-ribbon> — the equity curve as REAL extruded chrome geometry receding into a retrowave grid ---------- */
  class ChartRibbon extends HTMLElement {
    static get observedAttributes() { return ['range', 'trend']; }
    connectedCallback() {
      if (this._init) return; this._init = true;
      this.style.display = 'block';
      // Respect an author-set position. The finals overlay this ridge BEHIND the 2D chart
      // with position:absolute; forcing 'relative' here is what made a live/direct-mount port
      // drop it into normal flow and STACK the ridge above the line instead of overlaying.
      if (!this.style.position) this.style.position = 'relative';
      if (this.getAttribute('height')) this.style.height = this.getAttribute('height') + 'px';
      this._canvas = document.createElement('canvas');
      Object.assign(this._canvas.style, { width: '100%', height: '100%', display: 'block' });
      this.appendChild(this._canvas);
      this._bloom = document.createElement('canvas');
      Object.assign(this._bloom.style, { position: 'absolute', inset: '0', width: '100%', height: '100%', pointerEvents: 'none', mixBlendMode: 'plus-lighter', filter: 'blur(10px) brightness(1.3) contrast(1.6)' });
      this.appendChild(this._bloom);
      this._visible = true;
      this._canvas.addEventListener('webglcontextlost', (e) => { e.preventDefault(); this._releaseGL(); }, false);
      this._watch();
    }
    _watch() {
      const check = () => {
        this._wraf = requestAnimationFrame(check);
        this._wfc = ((this._wfc || 0) + 1) % 30;
        if (this._wfc !== 1) return;
        const rct = this.getBoundingClientRect();
        const vis = rct.bottom > -300 && rct.top < innerHeight + 300 && rct.width > 0;
        if (vis) {
          this._offN = 0;
          if (!this._renderer && !this._booting) this._boot();
        } else if (this._renderer) {
          this._offN = (this._offN || 0) + 1;
          if (this._offN > 14) this._releaseGL();
        }
      };
      check();
    }
    _releaseGL() {
      cancelAnimationFrame(this._raf);
      this._ro && this._ro.disconnect();
      if (this._onMove) { const scope = this.closest('[data-hero-scope]') || this; scope.removeEventListener('pointermove', this._onMove); this._onMove = null; }
      if (this._renderer) {
        this._renderer.dispose();
        this._renderer.forceContextLoss && this._renderer.forceContextLoss();
        this._renderer = null;
      }
      this._mesh = null;
    }
    _rims() { return (this.getAttribute('rims') || '#a855f7,#f472b6,#2dd4bf').split(',').map(s => s.trim()); }
    // overlay=1: transparent companion behind a 2D chart — no grid floor, geometry only
    _isOverlay() { return this.getAttribute('overlay') === '1'; }
    // ── REAL-DATA SEAM ──  el.setData([1351.2, …], '1D')  — same contract as <equity-chart>.
    // In the 1b overlay pairing, call setData on BOTH the chart-ribbon and the equity-chart
    // with the identical array so the 3D ridge and the 2D line stay locked together.
    setData(points, range) {
      if (!Array.isArray(points) || points.length < 2) return;
      this._real = points.slice();
      if (range != null) this._rangeAttr = range;
      if (this._renderer) this._build();
    }
    _gen() {
      if (this._real) { this._pts = this._real; return; }
      const range = this.getAttribute('range') || '1D';
      const trend = this.getAttribute('trend') || 'up';
      const rnd = mulberry32(hashStr(range + trend));
      const n = 120, pts = [];
      const drift = trend === 'up' ? 0.9 : -0.9;
      let v = trend === 'up' ? 1351 : 1499;
      for (let i = 0; i < n; i++) { v += drift + (rnd() - 0.5) * 14 + Math.sin(i / 9) * 1.6; pts.push(v); }
      const end = 1437.52, off = end - pts[n - 1];
      this._pts = pts.map((p, i) => p + off * (i / (n - 1)));
    }
    async _boot() {
      this._booting = true;
      try {
        await ensureThree();
        const bgHex = this.getAttribute('bg') || '#0c081c';
        const r = new THREE.WebGLRenderer({ canvas: this._canvas, antialias: true, alpha: true });
        r.setPixelRatio(Math.min(window.devicePixelRatio || 1, 1.5));
        r.outputEncoding = THREE.sRGBEncoding;
        r.toneMapping = THREE.ACESFilmicToneMapping;
        this._renderer = r;
        const S = this._scene = new THREE.Scene();
        if (!this._isOverlay()) S.fog = new THREE.FogExp2(new THREE.Color(bgHex), 0.05);
        else S.fog = new THREE.Fog(new THREE.Color(bgHex), 1050, 1620); // pixel-space: fade only the deep back
        this._camera = this._isOverlay()
          ? new THREE.PerspectiveCamera(30, 2, 1, 6000)
          : new THREE.PerspectiveCamera(36, 2, 0.1, 200);
        this._ls = this._isOverlay() ? 40 : 1; // light-distance scale for pixel-unit space
        this._env = makeEnv(r, this._rims(), this.getAttribute('metal') || '#cfd8ff');
        // retrowave floor grid — fades into fog
        const gcol1 = new THREE.Color(this._rims()[0]), gcol2 = new THREE.Color(this._rims()[2] || this._rims()[0]);
        const verts = [];
        for (let x = -34; x <= 34; x += 1.7) verts.push(x, 0, 3, x, 0, -60);
        const verts2 = [];
        for (let z = 3; z >= -60; z -= 1.9) verts2.push(-34, 0, z, 34, 0, z);
        const mkGrid = (vv, col, op) => {
          const geo = new THREE.BufferGeometry();
          geo.setAttribute('position', new THREE.Float32BufferAttribute(vv, 3));
          const m2 = new THREE.LineSegments(geo, new THREE.LineBasicMaterial({ color: col, transparent: true, opacity: op }));
          m2.position.y = -0.02; S.add(m2); return m2;
        };
        if (!this._isOverlay()) { mkGrid(verts, gcol1, 0.34); mkGrid(verts2, gcol2, 0.22); }
        // lights: orbiting colored, all behind/above the ribbon crest
        this._orbit = [];
        this._rims().forEach((c, i) => {
          const L = new THREE.PointLight(new THREE.Color(c), this._isOverlay() ? 9 : 16, 0);
          S.add(L);
          this._orbit.push({ L, phase: (i / 3) * Math.PI * 2, speed: 0.07 + 0.04 * (i % 2), rad: (13 + (i % 2) * 4), y: (5 + (i % 3) * 2) });
        });
        S.add(new THREE.AmbientLight(0x14161f, 0.35));
        // traveling crest light + glow bead (non-overlay); overlay gets a BACK-edge tracer instead
        if (!this._isOverlay()) {
          this._crest = new THREE.PointLight(new THREE.Color(this._rims()[1] || '#f472b6'), 5, 8);
          S.add(this._crest);
          this._bead = new THREE.Mesh(new THREE.SphereGeometry(0.09, 12, 12), new THREE.MeshBasicMaterial({ color: 0xffffff }));
          S.add(this._bead);
        } else {
          // back-edge tracer INSIDE the 3D scene — depth-tested, so ridge peaks genuinely occlude it.
          // Matches the front comet's style at 60% size (user-tuned).
          const mkS = (rad, col, op) => new THREE.Mesh(
            new THREE.SphereGeometry(rad, 10, 10),
            new THREE.MeshBasicMaterial({ color: new THREE.Color(col), transparent: op < 1, opacity: op, fog: false }));
          this._bhead = mkS(2.1, '#eafcff', 1); S.add(this._bhead);
          this._bglow = new THREE.PointLight(new THREE.Color(this._rims()[2] || '#2dd4bf'), 2.5, 320);
          S.add(this._bglow);
          this._btrail = [];
          for (let k = 1; k <= 14; k++) {
            const f = 1 - k / 15;
            const m = mkS(1.9 * (0.35 + 0.65 * f) * 2 * 0.6 + 0.6, '#22d3ee', Math.max(0.05, 0.4 * f * f));
            S.add(m); this._btrail.push({ m, k });
          }
        }
        // mouse parallax (overlay): tiny shear on the extrusion behind the pixel-locked front edge —
        // base is 0 so depth recedes straight away from the camera (perspective vanishing), mouse tilts the view
        this._shear = { kx: 0, ky: 0.07, tkx: 0, tky: 0.07 };
        if (this._isOverlay()) {
          const scope = this.closest('[data-hero-scope]') || this;
          this._onMove = (e) => {
            const b = this.getBoundingClientRect();
            if (!b.width) return;
            const px = ((e.clientX - b.left) / b.width) * 2 - 1;
            const py = ((e.clientY - b.top) / b.height) * 2 - 1;
            this._shear.tkx = -px * 0.064;
            this._shear.tky = 0.07 + py * 0.04;
          };
          scope.addEventListener('pointermove', this._onMove);
        }
        this._build();
        this._resize();
        this._ro = new ResizeObserver(() => this._resize());
        this._ro.observe(this);
        this._t0 = performance.now();
        const loop = () => {
          this._raf = requestAnimationFrame(loop);
          this._fcv = ((this._fcv || 0) + 1) % 30;
          if (this._fcv === 1) {
            const rct = this.getBoundingClientRect();
            this._visible = rct.bottom > -120 && rct.top < innerHeight + 120 && rct.width > 0;
          }
          if (!this._visible || !this._renderer) return;
          const t = (performance.now() - this._t0) / 1000;
          const yOff = this._isOverlay() ? -this._chartDims().h * 0.06 : 0;
          for (const o of this._orbit) {
            const a = o.phase + t * o.speed;
            o.L.position.set(Math.sin(a) * o.rad * this._ls, (o.y + Math.sin(t * 0.18 + o.phase) * 1.4) * this._ls * 0.5 + yOff, (-3 - o.rad * (0.35 + 0.35 * Math.cos(a))) * (this._isOverlay() ? 40 : 1));
          }
          // crest bead crawls the top edge
          if (this._crest) {
            const tt = (t / 14) % 1;
            const cp = this._crestPt(tt);
            this._crest.position.set(cp.x, cp.y + 0.25, 0.35);
            this._bead.position.set(cp.x, cp.y + 0.02, 0.14);
            const flick = 0.85 + Math.sin(t * 7) * 0.15;
            this._crest.intensity = 5 * flick;
          }
          if (this._isOverlay()) {
            // ease the shear toward the mouse target — front edge (z=0) never moves
            const sh = this._shear;
            sh.kx += (sh.tkx - sh.kx) * 0.05;
            sh.ky += (sh.tky - sh.ky) * 0.05;
            if (this._mesh) {
              this._mesh.matrixAutoUpdate = false;
              this._mesh.matrix.set(1, 0, sh.kx, 0, 0, 1, sh.ky, 0, 0, 0, 1, 0, 0, 0, 0, 1);
            }
            // back-edge comet: rides the rear crest, sheared with the mesh, occluded by the ridge
            if (this._bhead) {
              const tt = ((performance.now() - this._t0) / 15000) % 1;
              const { n: bn } = this._map();
              const bz = -897;
              const atB = (fr) => { const cp = this._crestPt(Math.max(0, Math.min(1, fr))); return [cp.x + sh.kx * bz, cp.y + sh.ky * bz + 2, bz]; };
              const hp = atB(tt);
              this._bhead.position.set(hp[0], hp[1], hp[2]);
              this._bglow.position.set(hp[0], hp[1] + 18, hp[2] + 40);
              this._bglow.intensity = 2.5 * (0.85 + Math.sin(t * 7) * 0.15);
              for (const tr of this._btrail) {
                const p2 = atB(tt - (tr.k * 0.55) / (bn - 1));
                tr.m.position.set(p2[0], p2[1], p2[2]);
                tr.m.visible = tt - (tr.k * 0.55) / (bn - 1) >= 0;
              }
            }
          } else {
            this._camera.position.x = Math.sin(t * 0.09) * 0.9;
            this._camera.lookAt(0, 1.5, -2);
          }
          this._renderer.render(S, this._camera);
          this._fc = (this._fc || 0) + 1;
          if (!(this._fc & 1)) {
            const bw = Math.max(1, (this.clientWidth / 2) | 0), bh = Math.max(1, (this.clientHeight / 2) | 0);
            if (this._bloom.width !== bw) { this._bloom.width = bw; this._bloom.height = bh; }
            const bg2 = this._bloom.getContext('2d');
            bg2.clearRect(0, 0, bw, bh);
            bg2.globalAlpha = this._isOverlay() ? 0.55 : 0.7;
            bg2.drawImage(this._canvas, 0, 0, bw, bh);
          }
        };
        loop();
        this._booting = false;
      } catch (err) { this._booting = false; console.warn('chart-ribbon fallback:', err); }
    }
    _chartDims() {
      // read the sibling 2D chart's box so the pixel mapping matches it EXACTLY
      const scope = this.closest('[data-hero-scope]') || this.parentElement || document;
      const ch = scope.querySelector('equity-chart');
      return { w: (ch && ch.clientWidth) || this.clientWidth || 300, h: (ch && ch.clientHeight) || this.clientHeight || 150 };
    }
    _map() {
      const pts = this._pts, n = pts.length;
      if (this._isOverlay()) {
        // EXACT pixel-space mapping of <equity-chart>. World-y = −cssY with the camera axis at the
        // element's TOP edge (off-axis frustum below), so depth recedes up-and-away like a ridge.
        const { w, h } = this._chartDims();
        const min = Math.min(...pts), max = Math.max(...pts), pad = (max - min) * 0.14 || 1;
        return {
          X: (i) => ((i / (n - 1)) * (w - 4) + 2) - w / 2,
          Y: (i) => -(h - 26 - ((pts[i] - (min - pad)) / ((max + pad) - (min - pad))) * (h - 44)),
          n,
        };
      }
      const min = Math.min(...pts), max = Math.max(...pts);
      const W = 21, H = 3.1, Y0 = 0.55;
      return { X: (i) => -W / 2 + (i / (n - 1)) * W, Y: (i) => Y0 + ((pts[i] - min) / (max - min || 1)) * H, n };
    }
    _crestPt(t) {
      const { X, Y, n } = this._map();
      const fi = t * (n - 1), i0 = Math.floor(fi), i1 = Math.min(i0 + 1, n - 1), fr = fi - i0;
      return { x: X(i0) + (X(i1) - X(i0)) * fr, y: Y(i0) + (Y(i1) - Y(i0)) * fr };
    }
    _build() {
      this._gen();
      if (this._mesh) { this._scene.remove(this._mesh); this._mesh.geometry.dispose(); }
      const ov = this._isOverlay();
      const { X, Y, n } = this._map();
      const base = ov ? -(this._chartDims().h - 26) : 0;
      const shape = new THREE.Shape();
      if (ov) {
        // extend flat wings far past the frustum so the extrusion's side walls never splay into view
        const wext = this._chartDims().w;
        shape.moveTo(-wext, base);
        shape.lineTo(-wext, Y(0));
        for (let i = 0; i < n; i++) shape.lineTo(X(i), Y(i));
        shape.lineTo(wext, Y(n - 1));
        shape.lineTo(wext, base);
      } else {
        shape.moveTo(X(0), base);
        for (let i = 0; i < n; i++) shape.lineTo(X(i), Y(i));
        shape.lineTo(X(n - 1), base);
      }
      shape.closePath();
      const geo = new THREE.ExtrudeGeometry(shape, ov
        ? { depth: 900, bevelEnabled: true, bevelThickness: 3, bevelSize: 2, bevelSegments: 2, curveSegments: 4 }
        : { depth: 7, bevelEnabled: true, bevelThickness: 0.07, bevelSize: 0.045, bevelSegments: 3, curveSegments: 4 });
      // extrusion runs 0→+depth; translate so the front cap sits exactly at z=0 with correct winding
      if (ov) geo.translate(0, 0, -900);
      const down = this.getAttribute('trend') === 'down';
      const mat = new THREE.MeshStandardMaterial({
        color: new THREE.Color(down ? (ov ? '#8a5560' : '#ffb3c0') : (ov ? '#8f96c4' : (this.getAttribute('metal') || '#cfd8ff'))),
        metalness: 1.0, roughness: ov ? 0.012 : 0.07, envMap: this._env, envMapIntensity: ov ? 1.1 : 1.5,
      });
      const mesh = new THREE.Mesh(geo, mat);
      if (!ov) mesh.position.z = -7;
      this._scene.add(mesh);
      this._mesh = mesh;
    }
    _resize() {
      if (!this._renderer) return;
      const w = this.clientWidth || 300, h = this.clientHeight || 150;
      this._renderer.setSize(w, h, false);
      if (this._isOverlay()) {
        const d = this._chartDims();
        // off-axis frustum: virtual image is 2h tall, we render its BOTTOM half — the camera axis
        // (vanishing point) lands on the element's top edge; z=0 stays exactly 1:1 with CSS pixels
        const fov = 30 * Math.PI / 180;
        const dist = d.h / Math.tan(fov / 2);
        this._camera.fov = 30;
        this._camera.aspect = d.w / (2 * d.h);
        this._camera.setViewOffset(d.w, 2 * d.h, 0, d.h, d.w, d.h);
        this._camera.position.set(0, 0, dist);
        this._camera.lookAt(0, 0, 0);
        this._camera.updateProjectionMatrix();
        if (this._scene.fog && this._scene.fog.isFog) { this._scene.fog.near = dist + 160; this._scene.fog.far = dist + 1150; }
        this._renderer.setSize(d.w, d.h, false);
        Object.assign(this._canvas.style, { width: d.w + 'px', height: d.h + 'px' });
        Object.assign(this._bloom.style, { width: d.w + 'px', height: d.h + 'px' });
        if (this._env) this._build(); // pixel-space geometry depends on size
        return;
      }
      this._camera.aspect = w / h;
      this._camera.updateProjectionMatrix();
      this._camera.position.set(0, 4.6, 13.5);
      this._camera.lookAt(0, 1.5, -2);
    }
    attributeChangedCallback() { if (this._renderer) this._build(); }
    disconnectedCallback() {
      cancelAnimationFrame(this._raf);
      cancelAnimationFrame(this._wraf);
      this._ro && this._ro.disconnect();
      this._releaseGL();
      this._init = false;
    }
  }
  customElements.define('chart-ribbon', ChartRibbon);

  /* ---------- <city-scape> — NYC skyline band: day/night, lit windows, plane + helicopter ---------- */
  class CityScape extends HTMLElement {
    static get observedAttributes() { return ['mode', 'src', 'minimal']; }
    connectedCallback() {
      if (this._init) return; this._init = true;
      this.style.display = 'block';
      this.style.pointerEvents = 'none';
      this._canvas = document.createElement('canvas');
      Object.assign(this._canvas.style, { width: '100%', height: '100%', display: 'block' });
      this.appendChild(this._canvas);
      this._visible = true;
      this._ro = new ResizeObserver(() => { this._static = null; });
      this._ro.observe(this);
      this._t0 = performance.now();
      const loop = () => {
        this._raf = requestAnimationFrame(loop);
        this._pvc = ((this._pvc || 0) + 1) % 30;
        if (this._pvc === 1) {
          const rct = this.getBoundingClientRect();
          this._visible = rct.bottom > -120 && rct.top < innerHeight + 120 && rct.width > 0;
        }
        this._fc = (this._fc || 0) + 1;
        if (this._visible && !(this._fc % 3)) this._draw();
      };
      loop();
    }
    attributeChangedCallback(nm) { if (nm === 'src') this._img = null; this._static = null; }
    _buildStatic(w, h) {
      const night = (this.getAttribute('mode') || 'night') === 'night';
      const minimal = this.getAttribute('minimal') === '1';
      const off = document.createElement('canvas'); off.width = w; off.height = h;
      const g = off.getContext('2d');
      // optional user-provided skyline photo behind everything (src attr → jpg)
      const src = this.getAttribute('src');
      if (src && !this._img) { this._img = new Image(); this._img.onload = () => { this._static = null; }; this._img.src = src; }
      // sky
      const sky = g.createLinearGradient(0, 0, 0, h);
      if (night) { sky.addColorStop(0, '#0b0e19'); sky.addColorStop(0.72, '#101527'); sky.addColorStop(1, '#0b0e15'); }
      else { sky.addColorStop(0, '#31415f'); sky.addColorStop(0.6, '#3d4a66'); sky.addColorStop(1, '#232c42'); }
      g.fillStyle = sky; g.fillRect(0, 0, w, h);
      if (this._img && this._img.complete && this._img.naturalWidth) {
        const iw = this._img.naturalWidth, ih = this._img.naturalHeight;
        const s = Math.max(w / iw, h / ih);
        g.globalAlpha = night ? 0.55 : 0.75;
        g.drawImage(this._img, (w - iw * s) / 2, (h - ih * s) / 2, iw * s, ih * s);
        g.globalAlpha = 1;
        // darken toward the dashboard's mood
        g.fillStyle = night ? 'rgba(8,10,18,0.5)' : 'rgba(20,26,44,0.35)';
        g.fillRect(0, 0, w, h);
      }
      const rnd = mulberry32(night ? 77 : 78);
      if (night) { // stars + moon
        g.fillStyle = 'rgba(255,255,255,0.5)';
        for (let i = 0; i < 70; i++) { const sx = rnd() * w, sy = rnd() * h * 0.55; g.globalAlpha = 0.15 + rnd() * 0.45; g.fillRect(sx, sy, 1.2, 1.2); }
        g.globalAlpha = 1;
        g.fillStyle = '#e8ecf5'; g.beginPath(); g.arc(w * 0.82, h * 0.2, 16, 0, 7); g.fill();
        g.fillStyle = '#101527'; g.beginPath(); g.arc(w * 0.82 + 7, h * 0.2 - 3, 14, 0, 7); g.fill();
      } else { // sun glow
        const sg = g.createRadialGradient(w * 0.8, h * 0.22, 0, w * 0.8, h * 0.22, 90);
        sg.addColorStop(0, 'rgba(255,238,200,0.75)'); sg.addColorStop(1, 'rgba(255,238,200,0)');
        g.fillStyle = sg; g.fillRect(0, 0, w, h);
        g.fillStyle = '#ffeecb'; g.beginPath(); g.arc(w * 0.8, h * 0.22, 15, 0, 7); g.fill();
      }
      // three parallax layers of buildings
      const layer = (baseY, minH, maxH, color, winAlpha, seed) => {
        const r2 = mulberry32(seed);
        let x = -10;
        g.fillStyle = color;
        const wins = [];
        while (x < w + 10) {
          const bw = 26 + r2() * 62, bh = minH + r2() * (maxH - minH);
          g.fillRect(x, baseY - bh, bw, bh + 4);
          if (r2() < 0.25) { g.fillRect(x + bw * 0.32, baseY - bh - 9, bw * 0.36, 9); } // rooftop bulkhead
          if (r2() < 0.12) { g.fillRect(x + bw / 2 - 1, baseY - bh - 22, 2, 22); } // antenna
          // windows
          for (let wy = baseY - bh + 7; wy < baseY - 8; wy += 11) {
            for (let wx = x + 5; wx < x + bw - 6; wx += 9) {
              if (r2() < (night ? 0.34 : 0.1)) wins.push([wx, wy]);
            }
          }
          x += bw + 2 + r2() * 8;
        }
        g.fillStyle = night ? 'rgba(255,220,140,' + winAlpha + ')' : 'rgba(190,205,235,' + winAlpha + ')';
        wins.forEach(([wx, wy]) => g.fillRect(wx, wy, 4, 5));
      };
      if (!minimal) {
        layer(h, h * 0.18, h * 0.42, night ? '#070a12' : '#141b2c', 0.28, 21); // far
        layer(h, h * 0.3, h * 0.62, night ? '#05070c' : '#0e1422', 0.5, 22);   // near
      }
      this._minimal = minimal;
      this._static = off;
      this._night = night;
    }
    _draw() {
      const w = this.clientWidth || 300, h = this.clientHeight || 300;
      const c = this._canvas;
      if (c.width !== w || c.height !== h) { c.width = w; c.height = h; this._static = null; }
      if (!this._static) this._buildStatic(w, h);
      const g = c.getContext('2d');
      g.clearRect(0, 0, w, h);
      g.drawImage(this._static, 0, 0);
      const t = (performance.now() - this._t0) / 1000;
      const night = this._night;
      // plane crossing (loops ~40s)
      const px = ((t * 26) % (w + 300)) - 150, py = h * 0.13 + Math.sin(t * 0.7) * 3;
      g.fillStyle = night ? 'rgba(200,210,230,0.5)' : 'rgba(230,238,252,0.85)';
      g.beginPath(); g.ellipse(px, py, 9, 2.2, 0, 0, 7); g.fill();
      g.fillRect(px - 3, py - 4.5, 6, 4); // tail
      if (night && (t * 2 | 0) % 2) { g.fillStyle = '#ff6b6b'; g.beginPath(); g.arc(px - 8, py, 1.6, 0, 7); g.fill(); }
      // helicopter bobbing (loops ~55s, other direction)
      const hx = w - (((t * 15) % (w + 260)) - 130), hy = h * 0.3 + Math.sin(t * 1.3) * 5;
      g.fillStyle = night ? 'rgba(190,200,225,0.45)' : 'rgba(222,230,248,0.8)';
      g.beginPath(); g.ellipse(hx, hy, 7, 3.4, 0, 0, 7); g.fill();
      g.fillRect(hx + 5, hy - 1.2, 10, 2.2); // tail boom
      g.strokeStyle = g.fillStyle; g.lineWidth = 1.4;
      const rot = Math.sin(t * 26) * 11;
      g.beginPath(); g.moveTo(hx - rot, hy - 5); g.lineTo(hx + rot, hy - 5); g.stroke();
      if (night) { g.fillStyle = '#7dd3fc'; g.beginPath(); g.arc(hx, hy + 4, 1.4, 0, 7); g.fill(); }
      // night: a few windows twinkle (only when the drawn city is present)
      if (night && !this._minimal) {
        const r3 = mulberry32(9000 + ((t / 1.7) | 0));
        g.fillStyle = 'rgba(255,220,140,0.55)';
        for (let i = 0; i < 5; i++) g.fillRect(r3() * w, h * (0.55 + r3() * 0.4), 4, 5);
      }
    }
    disconnectedCallback() { cancelAnimationFrame(this._raf); this._ro && this._ro.disconnect(); this._init = false; }
  }
  customElements.define('city-scape', CityScape);
})();
