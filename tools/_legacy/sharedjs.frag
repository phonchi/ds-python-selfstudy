/* ============ shared utilities ============ */
const $ = id => document.getElementById(id);

function quizCheck(quizId, optEl) {
  const isCorrect = optEl.dataset.correct === 'true';
  optEl.parentElement.querySelectorAll('.quiz-opt').forEach(o => o.classList.remove('correct','wrong'));
  optEl.classList.add(isCorrect ? 'correct' : 'wrong');
  const fb = $(quizId + 'Feedback');
  fb.classList.remove('correct','wrong');
  fb.classList.add('show', isCorrect ? 'correct' : 'wrong');
  fb.innerHTML = (isCorrect ? '<strong>正確 ✓</strong> ' : '<strong>不對 ✗</strong> ') + (optEl.dataset.fb || '');
}

function hlLine(rootId, n) {
  const root = $(rootId);
  if (!root) return;
  root.querySelectorAll('.line').forEach(l => l.classList.remove('active'));
  if (n != null) {
    const line = root.querySelector(`.line[data-l="${n}"]`);
    if (line) line.classList.add('active');
  }
}

/* step player: frames = [{...}], apply(frame) renders */
class Player {
  constructor({frames, apply, delayInput, onDone}) {
    this.frames = frames; this.apply = apply;
    this.delayInput = delayInput; this.i = -1; this.timer = null;
    this.onDone = onDone || (()=>{});
  }
  step() {
    if (this.i + 1 >= this.frames.length) { this.stop(); this.onDone(); return; }
    this.i += 1; this.apply(this.frames[this.i]);
  }
  play() {
    this.stop();
    const tick = () => {
      if (this.i + 1 >= this.frames.length) { this.stop(); this.onDone(); return; }
      this.step();
      this.timer = setTimeout(tick, this.delayInput ? parseInt(this.delayInput.value,10) : 700);
    };
    tick();
  }
  stop() { if (this.timer) { clearTimeout(this.timer); this.timer = null; } }
  reset() { this.stop(); this.i = -1; if (this.frames.length) this.apply(this.frames[0]); }
}

function setStatus(id, html) {
  const el = $(id); if (el) el.querySelector('.status-text').innerHTML = html;
}

/* vertical box stack renderer (DOM) */
function renderBoxStack(containerId, items, opts={}) {
  const el = $(containerId); if (!el) return;
  const hl = opts.highlight ?? -1;   // index from top (0 = top)
  el.innerHTML = '';
  const label = document.createElement('div');
  label.className = 'bs-toplabel';
  label.textContent = items.length ? 'top ↓' : '(empty)';
  el.appendChild(label);
  items.slice().reverse().forEach((v, idx) => {
    const d = document.createElement('div');
    d.className = 'bs-item' + (idx === hl ? ' bs-hl' : '');
    d.textContent = v;
    el.appendChild(d);
  });
}

/* horizontal queue renderer: front at left */
function renderBoxQueue(containerId, items, opts={}) {
  const el = $(containerId); if (!el) return;
  el.innerHTML = '';
  const front = document.createElement('div');
  front.className = 'bq-label'; front.textContent = items.length ? 'front →' : '(empty)';
  el.appendChild(front);
  items.forEach((v, idx) => {
    const d = document.createElement('div');
    d.className = 'bq-item' + (idx === (opts.highlight ?? -1) ? ' bs-hl' : '');
    d.textContent = v;
    el.appendChild(d);
  });
  const rear = document.createElement('div');
  rear.className = 'bq-label'; rear.textContent = items.length ? '← rear' : '';
  el.appendChild(rear);
}

/* floating nav scroll spy */
(function setupNav() {
  const nav = $('floatNav');
  const links = nav.querySelectorAll('a[data-target]');
  const sections = Array.from(links).map(a => document.getElementById(a.dataset.target)).filter(Boolean);
  function update() {
    const y = window.scrollY + window.innerHeight * 0.3;
    let active = sections[0]?.id;
    for (const s of sections) if (s.offsetTop <= y) active = s.id;
    links.forEach(a => a.classList.toggle('active', a.dataset.target === active));
  }
  window.addEventListener('scroll', update, { passive: true });
  update();
})();

