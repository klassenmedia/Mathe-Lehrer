// node render.js 0,4,8   -> build/clips/NN.mp4 (stumm) je Szene;  node render.js 3 still 6.5 -> Standbild
const { chromium } = require('/opt/node22/lib/node_modules/playwright');
const { spawn } = require('child_process');
const http = require('http'), fs = require('fs'), path = require('path');
const FPS = 24, ROOT = path.resolve(__dirname, '..');
const ids = process.argv[2].split(',').map(Number);
const still = process.argv[3] === 'still' ? parseFloat(process.argv[4]) : null;
const mime = { '.html': 'text/html', '.js': 'text/javascript', '.json': 'application/json', '.woff2': 'font/woff2' };
const srv = http.createServer((q, r) => {
  const f = path.join(ROOT, decodeURIComponent(q.url.split('?')[0]).replace(/^\/+/, ''));
  if (!f.startsWith(ROOT) || !fs.existsSync(f)) { r.writeHead(404); return r.end(); }
  r.writeHead(200, { 'Content-Type': mime[path.extname(f)] || 'application/octet-stream' }); fs.createReadStream(f).pipe(r);
});
(async () => {
  await new Promise(r => srv.listen(0, r));
  const br = await chromium.launch({ args: ['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'] });
  const pg = await br.newPage({ viewport: { width: 1280, height: 720 } });
  pg.on('pageerror', e => console.error('PAGEERR', e.message));
  await pg.goto(`http://localhost:${srv.address().port}/rubiks/player.html`);
  await pg.evaluate(() => loadScenes());
  fs.mkdirSync(path.join(__dirname, 'build/clips'), { recursive: true });
  for (const i of ids) {
    const dur = await pg.evaluate(i => loadScene(i), i);
    if (still !== null) { await pg.evaluate(t => renderAt(t), still); await pg.screenshot({ path: path.join(__dirname, `build/still_${i}.png`) }); continue; }
    const out = path.join(__dirname, `build/clips/${String(i).padStart(2, '0')}.mp4`);
    const ff = spawn('ffmpeg', ['-y', '-loglevel', 'error', '-f', 'image2pipe', '-framerate', String(FPS), '-i', '-', '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '20', '-pix_fmt', 'yuv420p', out]);
    const frames = Math.round(dur * FPS);
    for (let f = 0; f < frames; f++) {
      await pg.evaluate(t => renderAt(t), f / FPS);
      const buf = await pg.screenshot({ type: 'jpeg', quality: 93 });
      if (!ff.stdin.write(buf)) await new Promise(r => ff.stdin.once('drain', r));
    }
    ff.stdin.end(); await new Promise(r => ff.on('close', r));
    console.log(`Szene ${i}: ${frames} Bilder`);
  }
  await br.close(); srv.close();
})();
