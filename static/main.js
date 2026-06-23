const submitBtn = document.getElementById('submit-point');
const startBtn = document.getElementById('start-graph');
const restartBtn = document.getElementById('restart');
const pointInput = document.getElementById('point-input');
const enteredP = document.getElementById('entered');
const startScreen = document.getElementById('start-screen');
const confirmScreen = document.getElementById('confirm-screen');
const graphScreen = document.getElementById('graph-screen');
const restartScreen = document.getElementById('restart-screen');

let point = { x: 0, y: 0 };

function parsePoint(text) {
  const parts = text.split(',');
  if (parts.length !== 2) throw new Error('bad');
  const x = parseInt(parts[0].trim(), 10);
  const y = parseInt(parts[1].trim(), 10);
  if (Number.isNaN(x) || Number.isNaN(y)) throw new Error('bad');
  return { x, y };
}

submitBtn.addEventListener('click', (e) => {
  e.preventDefault();
  try {
    point = parsePoint(pointInput.value);
  } catch (err) {
    alert('Invalid input. Use format: x,y with integers');
    return;
  }
  enteredP.textContent = `You entered: (${point.x}, ${point.y})`;
  startScreen.style.display = 'none';
  confirmScreen.style.display = '';
});

startBtn.addEventListener('click', async (e) => {
  e.preventDefault();
  confirmScreen.style.display = 'none';
  graphScreen.style.display = '';
  await drawGraph(point);
  setTimeout(() => {
    restartScreen.style.display = '';
  }, 3000);
});

restartBtn.addEventListener('click', (e) => {
  e.preventDefault();
  restartScreen.style.display = 'none';
  graphScreen.style.display = 'none';
  startScreen.style.display = '';
  pointInput.value = '0,0';
});

function drawGraph(p) {
  const canvas = document.getElementById('graph');
  const ctx = canvas.getContext('2d');

  // request server-computed canvas coordinates
  return fetch(`/api/plot?x=${p.x}&y=${p.y}`)
    .then((res) => res.json())
    .then((data) => {
      const width = data.width;
      const height = data.height;
      // draw grid
      ctx.clearRect(0, 0, width, height);
      const spacing = data.spacing;
      ctx.lineWidth = 1;
      for (let x = 0; x <= width; x += spacing) {
        ctx.beginPath(); ctx.moveTo(x, 0); ctx.lineTo(x, height); ctx.strokeStyle = 'lightgray'; ctx.stroke();
      }
      for (let y = 0; y <= height; y += spacing) {
        ctx.beginPath(); ctx.moveTo(0, y); ctx.lineTo(width, y); ctx.strokeStyle = 'lightgray'; ctx.stroke();
      }
      // axes
      const cx = width / 2;
      const cy = height / 2;
      ctx.strokeStyle = 'black'; ctx.lineWidth = 2;
      ctx.beginPath(); ctx.moveTo(cx, 0); ctx.lineTo(cx, height); ctx.stroke();
      ctx.beginPath(); ctx.moveTo(0, cy); ctx.lineTo(width, cy); ctx.stroke();

      // draw point (server provided canvas coords)
      const cp = data.canvas_point;
      ctx.beginPath(); ctx.fillStyle = 'red'; ctx.arc(cp.x, cp.y, 6, 0, Math.PI * 2); ctx.fill();

      // draw line
      const c1 = data.line[0];
      const c2 = data.line[1];
      ctx.beginPath(); ctx.strokeStyle = 'blue'; ctx.lineWidth = 2; ctx.moveTo(c1.x, c1.y); ctx.lineTo(c2.x, c2.y); ctx.stroke();
    })
    .catch((err) => {
      alert('Server error drawing graph');
      console.error(err);
    });
}
