const sharp = require('sharp');
const fs = require('fs');

const SRC = '/work/headshot-src.jpg';
const ROOT = '/work';
const IMG = '/work/img';
fs.rmSync(IMG, { recursive: true, force: true });
fs.mkdirSync(IMG, { recursive: true });
sharp.cache(false);

const widths = [400, 600, 800, 1000, 1280, 1600];

(async () => {
  const meta = await sharp(SRC).rotate().metadata();
  console.log('source (oriented):', meta.width, 'x', meta.height);

  // ---- responsive portrait set (full-frame 2:3) ----
  for (const w of widths) {
    const pipe = () => sharp(SRC).rotate().resize({ width: w, withoutEnlargement: true });
    await pipe().avif({ quality: 58, effort: 6 }).toFile(`${IMG}/headshot-${w}.avif`);
    await pipe().webp({ quality: 82, effort: 6 }).toFile(`${IMG}/headshot-${w}.webp`);
    await pipe().jpeg({ quality: 82, mozjpeg: true, progressive: true }).toFile(`${IMG}/headshot-${w}.jpg`);
  }

  // ---- canonical portrait at root (JSON-LD Person.image, plain fallback) ----
  await sharp(SRC).rotate().resize({ width: 1000 })
    .jpeg({ quality: 86, mozjpeg: true, progressive: true }).toFile(`${ROOT}/headshot.jpg`);

  // ---- 1200x630 share card, LIGHT EDITORIAL ----
  const cardW = 1200, cardH = 630, faceW = 440;
  const face = await sharp(SRC).rotate()
    .resize({ width: faceW, height: cardH, fit: 'cover', position: 'top' }).toBuffer();
  const scrim = Buffer.from(
    `<svg width="${faceW}" height="${cardH}" xmlns="http://www.w3.org/2000/svg">
       <defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="0">
         <stop offset="0" stop-color="#F5F3EC" stop-opacity="1"/>
         <stop offset="0.38" stop-color="#F5F3EC" stop-opacity="0"/>
       </linearGradient></defs>
       <rect width="100%" height="100%" fill="url(#g)"/>
     </svg>`);
  const facePanel = await sharp(face).composite([{ input: scrim, left: 0, top: 0 }]).toBuffer();

  const text = Buffer.from(
    `<svg width="${cardW}" height="${cardH}" xmlns="http://www.w3.org/2000/svg">
       <rect width="100%" height="100%" fill="#F5F3EC"/>
       <rect x="0" y="0" width="6" height="${cardH}" fill="#002349"/>
       <text x="92" y="150" font-family="'DejaVu Sans', Arial, sans-serif" font-size="24" letter-spacing="6" fill="#002349">IT SYSTEMS ENGINEER</text>
       <text x="88" y="298" font-family="'DejaVu Sans', Arial, sans-serif" font-size="100" font-weight="300" fill="#1A1D24">Arly Trenck</text>
       <text x="92" y="360" font-family="'DejaVu Sans', Arial, sans-serif" font-size="34" fill="#454A54">Infrastructure Architect</text>
       <text x="92" y="470" font-family="'DejaVu Sans', Arial, sans-serif" font-size="22" letter-spacing="3" fill="#8C877A">TRENCK.NET</text>
     </svg>`);

  await sharp({ create: { width: cardW, height: cardH, channels: 3, background: '#F5F3EC' } })
    .composite([
      { input: text, left: 0, top: 0 },
      { input: facePanel, left: cardW - faceW, top: 0 },
    ])
    .jpeg({ quality: 88, mozjpeg: true }).toFile(`${ROOT}/og-card.jpg`);

  const list = (d, f) => fs.readdirSync(d).filter(x => x.startsWith(f))
    .map(x => `${x} ${(fs.statSync(`${d}/${x}`).size / 1024).toFixed(0)}K`);
  console.log('img/:', list(IMG, 'headshot').join('  '));
  console.log('root:', list(ROOT, 'headshot').join(' '), '|', list(ROOT, 'og-card').join(' '));
})().catch(e => { console.error(e); process.exit(1); });
