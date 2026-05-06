'use strict';

const frames   = [];          // {index, isPeak, distance}
let currentIdx = 0;
const selected = new Set();

const grid          = document.getElementById('grid');
const detailImg     = document.getElementById('detail-img');
const frameLabel    = document.getElementById('frame-label');
const peakLabel     = document.getElementById('peak-label');
const distLabel     = document.getElementById('dist-label');
const toggleBtn     = document.getElementById('toggle-btn');
const selectionCount = document.getElementById('selection-count');
const statusText    = document.getElementById('status-text');
const spinner       = document.getElementById('spinner');
const saveBtn       = document.getElementById('save-btn');

// SSE 接続
const es = new EventSource('/api/events');
es.onmessage = e => handleEvent(JSON.parse(e.data));
es.onerror   = () => statusText.textContent = 'SSE接続エラー';

function handleEvent(ev) {
  switch (ev.type) {
    case 'frame_added':
      addThumb(ev.index);
      break;

    case 'trimming_done':
      statusText.textContent =
        `トリミング完了 (${ev.total} 枚) — 類似度を計算中...`;
      break;

    case 'comparison_start':
      spinner.classList.add('active');
      break;

    case 'comparison_progress':
      statusText.textContent = `類似度を計算中... ${ev.current}/${ev.total}`;
      break;

    case 'frame_classified':
      classifyFrame(ev.index, ev.is_peak, ev.distance);
      break;

    case 'comparison_done':
      spinner.classList.remove('active');
      statusText.textContent = '処理完了';
      saveBtn.disabled = false;
      break;

    case 'error':
      spinner.classList.remove('active');
      statusText.textContent = `エラー: ${ev.message}`;
      break;

    case 'stream_end':
      es.close();
      break;
  }
}

// サムネイル追加
function addThumb(index) {
  frames[index] = { index, isPeak: null, distance: null };

  const item = document.createElement('div');
  item.className = 'thumb-item';
  item.id = `thumb-${index}`;
  item.onclick = () => setActive(index);

  const img = document.createElement('img');
  img.src = `/api/frame/${index}`;
  img.loading = 'lazy';

  const lbl = document.createElement('div');
  lbl.className = 'thumb-label';
  lbl.textContent = index + 1;

  item.appendChild(img);
  item.appendChild(lbl);
  grid.appendChild(item);

  if (index === 0) setActive(0);
}

// ピーク判定結果を反映
function classifyFrame(index, isPeak, distance) {
  if (!frames[index]) return;
  frames[index].isPeak   = isPeak;
  frames[index].distance = distance;

  const item = document.getElementById(`thumb-${index}`);
  if (!isPeak) {
    item.classList.add('non-peak');
  } else {
    // ピーク画像を自動選択
    item.classList.add('peak');
    selected.add(index);
    item.classList.add('selected');
  }

  selectionCount.textContent = `${selected.size} 枚選択中`;

  if (index === currentIdx) updateDetail();
}

// フォーカス移動
function setActive(index) {
  const prev = document.getElementById(`thumb-${currentIdx}`);
  if (prev) prev.classList.remove('active');

  currentIdx = index;
  const item = document.getElementById(`thumb-${index}`);
  if (item) {
    item.classList.add('active');
    item.scrollIntoView({ block: 'nearest' });
  }
  updateDetail();
}

// 詳細パネル更新
function updateDetail() {
  const f = frames[currentIdx];
  if (!f) return;

  detailImg.src = `/api/frame/${currentIdx}?t=${Date.now()}`;
  frameLabel.textContent = `フレーム ${currentIdx + 1} / ${frames.length}`;

  if (f.isPeak === null) {
    peakLabel.textContent = 'ピーク: 計算中...';
    distLabel.textContent  = '';
  } else {
    peakLabel.textContent = `ピーク: ${f.isPeak ? 'はい' : 'いいえ'}`;
    distLabel.textContent  = f.distance !== null
      ? `類似度: ${f.distance.toFixed(2)}`
      : '';
  }

  const isSel = selected.has(currentIdx);
  toggleBtn.textContent    = isSel ? '選択を解除' : '選択に追加';
  toggleBtn.style.background = isSel ? '#f44336' : '#4a9eff';
}

// 選択トグル
function toggleSelection() {
  const item = document.getElementById(`thumb-${currentIdx}`);
  if (selected.has(currentIdx)) {
    selected.delete(currentIdx);
    item.classList.remove('selected');
  } else {
    selected.add(currentIdx);
    item.classList.add('selected');
  }
  selectionCount.textContent = `${selected.size} 枚選択中`;
  updateDetail();
}

// 保存
function saveSelected() {
  if (selected.size === 0) {
    statusText.textContent = '保存するフレームが選択されていません';
    return;
  }
  fetch('/api/save', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ selected: [...selected] }),
  })
    .then(r => r.json())
    .then(data => { statusText.textContent = `保存完了: ${data.folder}`; });
}

// キーボード操作
document.addEventListener('keydown', e => {
  if (e.key === 'ArrowRight') {
    if (currentIdx < frames.length - 1) setActive(currentIdx + 1);
  } else if (e.key === 'ArrowLeft') {
    if (currentIdx > 0) setActive(currentIdx - 1);
  } else if (e.key === ' ') {
    e.preventDefault();
    toggleSelection();
  } else if (e.key === 's' || e.key === 'S') {
    if (!saveBtn.disabled) saveSelected();
  }
});
