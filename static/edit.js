'use strict';

const statusText  = document.getElementById('status-text');
const generateBtn = document.getElementById('generate-btn');
const openBtn     = document.getElementById('open-btn');
const slider      = document.getElementById('thumb-slider');
const sizeLabel   = document.getElementById('thumb-size-label');

slider.addEventListener('input', () => {
  document.documentElement.style.setProperty('--thumb-w', `${slider.value}px`);
  sizeLabel.textContent = `${slider.value}px`;
});

async function generate() {
  const title = document.getElementById('title-input').value.trim();
  const memos = {};
  document.querySelectorAll('.edit-memo').forEach(el => {
    if (el.value.trim()) {
      memos[el.dataset.index] = el.value;
    }
  });

  generateBtn.disabled = true;
  statusText.textContent = 'HTML生成中...';

  try {
    const r = await fetch('/api/generate', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ title, memos }),
    });
    const data = await r.json();
    if (!r.ok) throw new Error(data.error);
    statusText.textContent = `生成完了: ${data.html}`;
    openBtn.disabled = false;
  } catch (e) {
    statusText.textContent = `エラー: ${e.message}`;
    generateBtn.disabled = false;
  }
}

function openPreview() {
  const title = document.getElementById('title-input').value.trim() || 'プレビュー';
  const thumbW = slider.value;

  let body = '';
  document.querySelectorAll('.edit-row').forEach((row, i) => {
    const src = row.querySelector('.edit-thumb').src;
    const memo = row.querySelector('.edit-memo').value;
    if (memo.trim()) {
      const escaped = memo
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;');
      body += `  <p class="lyric">${escaped}</p>\n`;
    }
    body += `  <img class="score-img" src="${src}" alt="${i + 1}">\n`;
  });

  const html = `<!DOCTYPE html>
<html lang="ja">
<head>
  <meta charset="utf-8">
  <title>${title}</title>
  <style>
    body { margin: 0; font-family: sans-serif; }
    h1 { margin: 16px 0 16px 24px; font-size: 2rem; }
    .score-img { width: 100%; vertical-align: top; display: block; }
    .lyric { margin: 8px 24px; font-size: 1rem; color: #333; white-space: pre-wrap; }
  </style>
</head>
<body>
  <h1>${title}</h1>
${body}</body>
</html>`;

  document.getElementById('preview-iframe').srcdoc = html;
  document.getElementById('preview-modal').style.display = 'flex';
}

function closePreview() {
  document.getElementById('preview-modal').style.display = 'none';
}

async function openHtml() {
  try {
    const r = await fetch('/api/open_html');
    const d = await r.json();
    if (!r.ok) throw new Error(d.error);
    statusText.textContent = '印刷 (Ctrl+P) からPDF保存できます';
  } catch (e) {
    statusText.textContent = `エラー: ${e.message}`;
  }
}
