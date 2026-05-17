async function loadSettings() {
  const res = await fetch('/api/settings');
  const data = await res.json();
  document.getElementById('interval-input').value = data.interval_sec;
  document.getElementById('threshold-input').value = data.similarity_threshold;
}

document.getElementById('settings-form').addEventListener('submit', async (e) => {
  e.preventDefault();
  const status = document.getElementById('settings-status');
  const body = {
    interval_sec: parseInt(document.getElementById('interval-input').value, 10),
    similarity_threshold: parseFloat(document.getElementById('threshold-input').value),
  };
  const res = await fetch('/api/settings', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body),
  });
  const data = await res.json();
  if (data.ok) {
    status.textContent = '保存しました';
    status.style.color = '#4caf50';
  } else {
    status.textContent = data.error || 'エラーが発生しました';
    status.style.color = '#f44336';
  }
  setTimeout(() => { status.textContent = ''; }, 3000);
});

loadSettings();
