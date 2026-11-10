# -*- coding: utf-8 -*-
"""Собирает автономный HTML-просмотр/редактор из ROADMAP_0.1.canvas (без Obsidian).

Открывается двойным кликом в браузере: зум колесом, панорама перетаскиванием фона,
двойной клик по карточке — правка текста, ПКМ — статус, кнопка «Скачать .canvas» — экспорт.
Правки хранятся в localStorage браузера.

Запуск: python -X utf8 tools/make_roadmap_html.py
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CANVAS = ROOT / "ROADMAP_0.1.canvas"
OUT = ROOT / "ROADMAP_0.1.html"

TEMPLATE = r"""<!doctype html>
<html lang="ru">
<head>
<meta charset="utf-8">
<title>Three Horizons — ROADMAP 0.1</title>
<style>
  :root {
    --bg:#1e1f23; --fg:#e8e8ee; --dim:#9aa0a8; --line:#3a3c42;
  }
  * { box-sizing: border-box; }
  html, body { margin:0; height:100%; background:var(--bg); color:var(--fg);
    font:14px/1.35 "Segoe UI", system-ui, sans-serif; overflow:hidden; }
  #bar { position:fixed; inset:0 0 auto 0; height:52px; display:flex; gap:10px; align-items:center;
    padding:0 14px; background:#17181b; border-bottom:1px solid var(--line); z-index:50; }
  #bar b { font-size:15px; letter-spacing:.2px; }
  #bar .sp { flex:1; }
  #bar button { background:#25272c; color:var(--fg); border:1px solid var(--line); border-radius:6px;
    padding:7px 11px; cursor:pointer; font-size:13px; }
  #bar button:hover { background:#2d3036; }
  #stats { color:var(--dim); font-size:12.5px; white-space:nowrap; }
  #hint { color:var(--dim); font-size:12.5px; }
  #viewport { position:absolute; inset:52px 0 0 0; overflow:hidden; cursor:grab; }
  #viewport.drag { cursor:grabbing; }
  #stage { position:absolute; left:0; top:0; transform-origin:0 0; }
  svg#edges { position:absolute; left:0; top:0; overflow:visible; pointer-events:none; }
  .group { position:absolute; border:1px solid rgba(255,255,255,.16); border-radius:10px;
    background:rgba(255,255,255,.025); }
  .group .glabel { position:absolute; left:10px; top:6px; font-weight:700; font-size:14px;
    color:#d3d6dd; white-space:nowrap; }
  .card { position:absolute; border-radius:7px; padding:7px 9px; overflow:hidden;
    border:1px solid var(--c, #6b6f78); background:rgba(255,255,255,.045);
    box-shadow:0 1px 0 rgba(0,0,0,.35); cursor:default; }
  .card .txt { white-space:pre-wrap; font-size:12.5px; }
  .card .txt b { font-size:13px; }
  .card code { background:rgba(255,255,255,.09); border-radius:3px; padding:0 3px; font-size:12px; }
  .card .wl { color:#8fd0ff; }
  .card.s1 { border-color:#fb464c; background:rgba(251,70,76,.14); }
  .card.s2 { border-color:#e9973f; background:rgba(233,151,63,.14); }
  .card.s3 { border-color:#e0de71; background:rgba(224,222,113,.13); }
  .card.s4 { border-color:#44cf6e; background:rgba(68,207,110,.13); }
  .card.s5 { border-color:#53dfdd; background:rgba(83,223,221,.12); }
  .card.s6 { border-color:#a882ff; background:rgba(168,130,255,.14); }
  .card.edit { outline:2px solid #8fd0ff; }
  .card textarea { width:100%; height:100%; resize:none; background:#101114; color:var(--fg);
    border:1px solid #8fd0ff; border-radius:5px; font:12.5px/1.3 "Segoe UI", sans-serif; padding:5px; }
  #toast { position:fixed; left:50%; bottom:26px; transform:translateX(-50%); background:#2b2e34;
    border:1px solid var(--line); padding:9px 14px; border-radius:8px; opacity:0; transition:.2s;
    pointer-events:none; font-size:13px; z-index:60; }
  #toast.show { opacity:1; }
</style>
</head>
<body>
<div id="bar">
  <b>THREE HORIZONS · ROADMAP 0.1</b>
  <span id="stats"></span>
  <span class="sp"></span>
  <span id="hint">колесо — зум · фон — панорама · 2 клик — текст · ПКМ — статус</span>
  <button id="btn-reset">Сбросить правки</button>
  <button id="btn-export">Скачать .canvas</button>
  <button id="btn-fit">Вписать</button>
</div>
<div id="viewport"><div id="stage"><svg id="edges"></svg></div></div>
<div id="toast"></div>

<script id="canvas-data" type="application/json">__DATA__</script>
<script>
const RAW = JSON.parse(document.getElementById('canvas-data').textContent);
const STORE = 'th-roadmap-0.1-glass';
const ORDER = ['5','3','4','1','6','2'];
const COLOR_NAME = {'1':'риск/блокер','2':'оранжевый','3':'в работе','4':'готово','5':'не начато','6':'канон'};

let state = load();
const viewport = document.getElementById('viewport');
const stage = document.getElementById('stage');
const svg = document.getElementById('edges');
let scale = 0.6, tx = 40, ty = 40, nodeMap = new Map();

function load() {
  const base = JSON.parse(JSON.stringify(RAW));
  try {
    const saved = JSON.parse(localStorage.getItem(STORE) || 'null');
    if (saved) {
      for (const n of base.nodes) {
        const s = saved[n.id];
        if (!s) continue;
        if (typeof s.text === 'string') n.text = s.text;
        if (typeof s.color === 'string') n.color = s.color;
      }
    }
  } catch (e) { /* ignore */ }
  return base;
}
function save() {
  const out = {};
  for (const n of state.nodes) {
    const b = RAW.nodes.find(x => x.id === n.id);
    if (b && (b.text !== n.text || b.color !== n.color)) out[n.id] = {text: n.text, color: n.color};
  }
  localStorage.setItem(STORE, JSON.stringify(out));
}
function toast(msg) {
  const t = document.getElementById('toast');
  t.textContent = msg; t.classList.add('show');
  clearTimeout(toast._t); toast._t = setTimeout(() => t.classList.remove('show'), 1800);
}
function esc(s) { return s.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;'); }
function renderText(s) {
  let h = esc(s);
  h = h.replace(/\*\*(.+?)\*\*/g, '<b>$1</b>');
  h = h.replace(/`([^`]+)`/g, '<code>$1</code>');
  h = h.replace(/\[\[([^\]]+)\]\]/g, '<span class="wl">🔗 $1</span>');
  return h;
}
function bounds() {
  let x1=1e9,y1=1e9,x2=-1e9,y2=-1e9;
  for (const n of state.nodes) {
    x1=Math.min(x1,n.x); y1=Math.min(y1,n.y);
    x2=Math.max(x2,n.x+n.width); y2=Math.max(y2,n.y+n.height);
  }
  return {x1,y1,x2,y2,w:x2-x1,h:y2-y1};
}
function apply() {
  stage.style.transform = `translate(${tx}px, ${ty}px) scale(${scale})`;
}
function fit() {
  const b = bounds(), vw = viewport.clientWidth, vh = viewport.clientHeight;
  scale = Math.min(vw/(b.w+120), vh/(b.h+120), 1.2);
  tx = (vw - b.w*scale)/2 - b.x1*scale;
  ty = (vh - b.h*scale)/2 - b.y1*scale;
  apply();
}
function build() {
  document.querySelectorAll('.card,.group').forEach(e => e.remove());
  const b = bounds();
  stage.style.width = (b.x2 - b.x1 + 40) + 'px';
  stage.style.height = (b.y2 - b.y1 + 40) + 'px';
  svg.setAttribute('width', b.w + 200); svg.setAttribute('height', b.h + 200);

  nodeMap.clear();
  const cardLayer = document.createElement('div');
  for (const n of state.nodes) {
    if (n.type === 'group') {
      const g = document.createElement('div');
      g.className = 'group';
      g.style.cssText = `left:${n.x}px;top:${n.y}px;width:${n.width}px;height:${n.height}px`;
      const l = document.createElement('div');
      l.className = 'glabel';
      l.textContent = n.label || '';
      g.appendChild(l);
      stage.appendChild(g);
    } else {
      const c = document.createElement('div');
      c.className = 'card s' + (n.color || '0');
      c.style.cssText = `left:${n.x}px;top:${n.y}px;width:${n.width}px;height:${n.height}px`;
      c.dataset.id = n.id;
      const t = document.createElement('div');
      t.className = 'txt';
      t.innerHTML = renderText(n.text || '');
      c.appendChild(t);
      c.addEventListener('dblclick', ev => { ev.stopPropagation(); editCard(n, c); });
      c.addEventListener('contextmenu', ev => { ev.preventDefault(); ev.stopPropagation(); cycleColor(n, c); });
      stage.appendChild(c);
    }
    nodeMap.set(n.id, n);
  }
  drawEdges();
  countStats();
}
function drawEdges() {
  while (svg.firstChild) svg.removeChild(svg.firstChild);
  for (const e of state.edges || []) {
    const a = nodeMap.get(e.fromNode), b = nodeMap.get(e.toNode);
    if (!a || !b) continue;
    const x1 = a.x + a.width, y1 = a.y + Math.min(a.height*0.25, 220);
    const x2 = b.x, y2 = b.y + Math.min(b.height*0.25, 220);
    const mx = (x1 + x2)/2;
    const p = document.createElementNS('http://www.w3.org/2000/svg','path');
    p.setAttribute('d', `M${x1},${y1} H${mx} V${y2} H${x2}`);
    p.setAttribute('fill','none');
    p.setAttribute('stroke', e.color === '1' ? '#fb464c' : '#4c8f9e');
    p.setAttribute('stroke-width','2');
    p.setAttribute('opacity','.75');
    svg.appendChild(p);
    const ah = document.createElementNS('http://www.w3.org/2000/svg','path');
    ah.setAttribute('d', `M${x2},${y2} l-7,-4 v8 z`);
    ah.setAttribute('fill', e.color === '1' ? '#fb464c' : '#4c8f9e');
    svg.appendChild(ah);
  }
}
function editCard(n, el) {
  if (el.querySelector('textarea')) return;
  el.classList.add('edit');
  el.innerHTML = '';
  const ta = document.createElement('textarea');
  ta.value = n.text;
  el.appendChild(ta);
  ta.focus();
  const done = () => {
    n.text = ta.value;
    el.classList.remove('edit');
    el.innerHTML = '';
    const t = document.createElement('div');
    t.className = 'txt';
    t.innerHTML = renderText(n.text);
    el.appendChild(t);
    save(); countStats();
    toast('Сохранено (в браузере). Для файла — «Скачать .canvas»');
  };
  ta.addEventListener('blur', done);
  ta.addEventListener('keydown', ev => {
    if (ev.key === 'Escape') { ta.value = n.text; ta.blur(); }
    if (ev.key === 'Enter' && (ev.ctrlKey || ev.metaKey)) ta.blur();
  });
}
function cycleColor(n, el) {
  const idx = ORDER.indexOf(n.color || '5');
  n.color = ORDER[(idx + 1) % ORDER.length];
  el.className = 'card s' + n.color;
  save(); countStats();
  toast('Статус: ' + (COLOR_NAME[n.color] || n.color));
}
function countStats() {
  const c = {5:0,3:0,4:0,1:0};
  for (const n of state.nodes) if (n.type !== 'group') c[n.color] = (c[n.color]||0)+1;
  document.getElementById('stats').textContent =
    `🟦 ${c['5']||0} · 🟨 ${c['3']||0} · 🟩 ${c['4']||0} · 🟥 ${c['1']||0}`;
}
// панорама
let drag = null;
viewport.addEventListener('mousedown', ev => {
  if (ev.target.closest('.card')) return;
  drag = {x: ev.clientX, y: ev.clientY, tx, ty};
  viewport.classList.add('drag');
});
window.addEventListener('mousemove', ev => {
  if (!drag) return;
  tx = drag.tx + (ev.clientX - drag.x);
  ty = drag.ty + (ev.clientY - drag.y);
  apply();
});
window.addEventListener('mouseup', () => { drag = null; viewport.classList.remove('drag'); });
// зум
viewport.addEventListener('wheel', ev => {
  ev.preventDefault();
  const rect = viewport.getBoundingClientRect();
  const mx = ev.clientX - rect.left, my = ev.clientY - rect.top;
  const k = ev.deltaY < 0 ? 1.12 : 1/1.12;
  const ns = Math.min(Math.max(scale * k, 0.12), 3);
  tx = mx - (mx - tx) * (ns / scale);
  ty = my - (my - ty) * (ns / scale);
  scale = ns;
  apply();
}, {passive:false});
// кнопки
document.getElementById('btn-fit').onclick = fit;
document.getElementById('btn-reset').onclick = () => {
  if (!confirm('Сбросить все правки (тексты и цвета) к исходному роадмапу?')) return;
  localStorage.removeItem(STORE);
  state = load(); build(); fit();
  toast('Правки сброшены');
};
document.getElementById('btn-export').onclick = () => {
  const out = JSON.parse(JSON.stringify(state));
  const blob = new Blob([JSON.stringify(out, null, 1)], {type:'application/json'});
  const a = document.createElement('a');
  a.href = URL.createObjectURL(blob);
  a.download = 'ROADMAP_0.1.canvas';
  a.click();
  URL.revokeObjectURL(a.href);
  toast('Скачан ROADMAP_0.1.canvas — замените файл в проекте');
};
build(); fit();
window.addEventListener('resize', apply);
</script>
</body>
</html>
"""


def main() -> None:
    data = json.loads(CANVAS.read_text(encoding="utf-8"))
    raw = json.dumps(data, ensure_ascii=False).replace("</", "<\\/")
    OUT.write_text(TEMPLATE.replace("__DATA__", raw), encoding="utf-8")
    print(f"OK {OUT} | {(OUT.stat().st_size/1024):.0f} KB | nodes={len(data['nodes'])}")


if __name__ == "__main__":
    main()
