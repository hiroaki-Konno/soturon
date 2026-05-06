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
