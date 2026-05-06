'use strict';

window.addEventListener('DOMContentLoaded', loadScoreFolders);

function loadScoreFolders() {
  fetch('/api/score_folders')
    .then(r => r.json())
    .then(data => {
      const list = document.getElementById('score-list');
      if (data.folders.length === 0) {
        list.innerHTML = '<li class="score-list-empty">保存済みの楽譜はありません</li>';
        return;
      }
      list.innerHTML = data.folders.map(f =>
        `<li class="score-list-item">
          <a class="score-list-link" href="/edit?folder=${encodeURIComponent(f.folder)}">${f.name}</a>
        </li>`
      ).join('');
    });
}

let _previewScale = 1;
let _roi = null;
let _drawing = false;
let _startX = 0, _startY = 0;
let _ctx = null, _img = null, _canvas = null;

function loadSource() {
  const source = document.getElementById('source-input').value.trim();
  if (!source) return;

  const btn = document.getElementById('load-btn');
  const statusEl = document.getElementById('load-status');
  btn.disabled = true;
  statusEl.textContent = '読み込み中... (YouTube URLの場合はダウンロードに時間がかかります)';
  document.getElementById('roi-section').style.display = 'none';

  fetch('/api/load', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ source }),
  })
    .then(r => r.json())
    .then(data => {
      if (data.error) throw new Error(data.error);
      _previewScale = data.orig_w / data.display_w;
      statusEl.textContent = `読み込み完了: ${data.title}`;
      setupCanvas(data.display_w, data.display_h);
    })
    .catch(e => {
      statusEl.textContent = `エラー: ${e.message}`;
    })
    .finally(() => { btn.disabled = false; });
}

function setupCanvas(w, h) {
  _canvas = document.getElementById('preview-canvas');
  _canvas.width  = w;
  _canvas.height = h;
  _canvas.style.maxWidth = '100%';
  _ctx = _canvas.getContext('2d');

  _img = new Image();
  _img.onload = () => {
    _ctx.drawImage(_img, 0, 0);
    _roi = null;
    document.getElementById('start-btn').disabled = true;
    document.getElementById('roi-info').textContent = '範囲未選択';
  };
  _img.src = `/api/preview?t=${Date.now()}`;

  _canvas.onmousedown = onMouseDown;
  _canvas.onmousemove = onMouseMove;
  _canvas.onmouseup   = onMouseUp;

  document.getElementById('roi-section').style.display = 'block';
}

function toCanvasCoords(e) {
  const r = _canvas.getBoundingClientRect();
  return {
    x: (e.clientX - r.left)  * (_canvas.width  / r.width),
    y: (e.clientY - r.top)   * (_canvas.height / r.height),
  };
}

function onMouseDown(e) {
  const p = toCanvasCoords(e);
  _startX = p.x; _startY = p.y;
  _drawing = true;
  _roi = null;
}

function onMouseMove(e) {
  if (!_drawing) return;
  const p = toCanvasCoords(e);
  _roi = {
    x: Math.min(_startX, p.x),
    y: Math.min(_startY, p.y),
    w: Math.abs(p.x - _startX),
    h: Math.abs(p.y - _startY),
  };
  redraw();
}

function onMouseUp() {
  _drawing = false;
  if (_roi && _roi.w > 5 && _roi.h > 5) {
    document.getElementById('start-btn').disabled = false;
    updateRoiInfo();
  } else {
    _roi = null;
  }
}

function redraw() {
  _ctx.clearRect(0, 0, _canvas.width, _canvas.height);
  _ctx.drawImage(_img, 0, 0);
  if (!_roi) return;

  const { x, y, w, h } = _roi;
  const cw = _canvas.width, ch = _canvas.height;

  // 選択外を暗くする（4方向の矩形）
  _ctx.fillStyle = 'rgba(0,0,0,0.45)';
  _ctx.fillRect(0,     0,  cw,    y);
  _ctx.fillRect(0,   y+h,  cw,    ch - y - h);
  _ctx.fillRect(0,     y,  x,     h);
  _ctx.fillRect(x+w,   y,  cw-x-w, h);

  // 選択枠
  _ctx.strokeStyle = '#00e5ff';
  _ctx.lineWidth = 2;
  _ctx.strokeRect(x, y, w, h);
}

function updateRoiInfo() {
  if (!_roi) return;
  const s = _previewScale;
  const x1 = Math.round(_roi.x * s),       y1 = Math.round(_roi.y * s);
  const x2 = Math.round((_roi.x+_roi.w)*s), y2 = Math.round((_roi.y+_roi.h)*s);
  document.getElementById('roi-info').textContent =
    `選択範囲 (元解像度): (${x1}, ${y1}) → (${x2}, ${y2})`;
}

function startProcessing() {
  if (!_roi) return;
  const pos1 = [Math.round(_roi.x), Math.round(_roi.y)];
  const pos2 = [Math.round(_roi.x + _roi.w), Math.round(_roi.y + _roi.h)];

  fetch('/api/start', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ pos1, pos2 }),
  }).then(() => {
    window.location.href = '/viewer';
  });
}
