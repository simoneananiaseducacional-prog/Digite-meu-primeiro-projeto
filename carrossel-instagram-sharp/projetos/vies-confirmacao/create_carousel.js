const sharp = require('sharp');
const fs = require('fs');
const path = require('path');

const W = 1080;
const H = 1350;
const OUT = path.resolve('saida');
const content = JSON.parse(fs.readFileSync(path.resolve('conteudo.json'), 'utf8'));
const P = content.palette;
const SANS = 'DejaVu Sans, Arial, Helvetica, sans-serif';
const SERIF = 'DejaVu Serif, Georgia, Times New Roman, serif';

fs.mkdirSync(OUT, { recursive: true });

const esc = (value) => String(value)
  .replace(/&/g, '&amp;')
  .replace(/</g, '&lt;')
  .replace(/>/g, '&gt;')
  .replace(/"/g, '&quot;');

function defs() {
  return `<defs>
    <filter id="grain" x="0" y="0" width="100%" height="100%">
      <feTurbulence type="fractalNoise" baseFrequency="0.76" numOctaves="3" seed="37" result="noise"/>
      <feColorMatrix in="noise" type="saturate" values="0" result="mono"/>
      <feComponentTransfer in="mono" result="faint"><feFuncA type="table" tableValues="0 0.05"/></feComponentTransfer>
      <feBlend in="SourceGraphic" in2="faint" mode="soft-light"/>
    </filter>
    <linearGradient id="wineGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="${P.wine}"/>
      <stop offset="1" stop-color="${P.wineDark}"/>
    </linearGradient>
    <marker id="arrowIvory" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto" markerUnits="strokeWidth">
      <path d="M0,0 L0,6 L9,3 z" fill="${P.ivory}"/>
    </marker>
    <marker id="arrowWine" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto" markerUnits="strokeWidth">
      <path d="M0,0 L0,6 L9,3 z" fill="${P.wine}"/>
    </marker>
  </defs>`;
}

function grain(fill) {
  return `<rect width="${W}" height="${H}" fill="${fill}" filter="url(#grain)"/>`;
}

function txt(x, y, text, opts = {}) {
  const {
    size = 60,
    fill = P.ivory,
    weight = 700,
    family = SANS,
    anchor = 'start',
    spacing = -1.2,
    style = 'normal',
    opacity = 1,
  } = opts;
  return `<text x="${x}" y="${y}" text-anchor="${anchor}" fill="${fill}" opacity="${opacity}" font-family="${family}" font-size="${size}" font-weight="${weight}" font-style="${style}" letter-spacing="${spacing}">${esc(text)}</text>`;
}

function multiline(lines, x, y, gap, opts = {}) {
  return lines.map((line, i) => txt(x, y + i * gap, line, opts)).join('');
}

function kicker(label, page, light = false) {
  const main = light ? P.wine : P.wine;
  const quiet = light ? P.black : P.taupe;
  return `
    <rect x="76" y="75" width="52" height="6" rx="3" fill="${main}"/>
    ${txt(146, 84, label, { size: 20, fill: quiet, weight: 700, spacing: 3.7 })}
    ${txt(1004, 84, `${String(page).padStart(2, '0')} / 09`, { size: 18, fill: quiet, weight: 700, spacing: 2.2, anchor: 'end' })}`;
}

function footer(light = false, extra = '') {
  const main = light ? P.black : P.ivory;
  const quiet = light ? P.wine : P.taupe;
  return `
    <line x1="76" y1="1244" x2="1004" y2="1244" stroke="${quiet}" stroke-width="2" opacity="0.62"/>
    ${txt(76, 1288, content.handle, { size: 18, fill: quiet, weight: 700, spacing: 2.1 })}
    ${txt(1004, 1288, content.brand, { size: 18, fill: main, weight: 700, spacing: 2.1, anchor: 'end' })}
    ${extra}`;
}

function svg(background, body, light = false) {
  return `<?xml version="1.0" encoding="UTF-8"?><svg xmlns="http://www.w3.org/2000/svg" width="${W}" height="${H}" viewBox="0 0 ${W} ${H}">${defs()}${grain(background)}${body}${footer(light)}</svg>`;
}

function ghostNumber(number, x = 70, y = 500, light = false) {
  return txt(x, y, String(number).padStart(2, '0'), {
    size: 350,
    fill: light ? P.wine : P.ivory,
    weight: 700,
    opacity: 0.055,
    spacing: -20,
  });
}

function card1(card) {
  let body = `
    <rect x="760" y="0" width="320" height="1350" fill="${P.wineDark}" opacity="0.86"/>
    <circle cx="910" cy="268" r="112" fill="none" stroke="${P.taupe}" stroke-width="2" opacity="0.4"/>
    <circle cx="910" cy="268" r="70" fill="none" stroke="${P.taupe}" stroke-width="2" opacity="0.25"/>
    <circle cx="910" cy="268" r="16" fill="${P.wine}"/>
    <path d="M760 650 C860 570, 965 710, 1080 610" fill="none" stroke="${P.wine}" stroke-width="16" opacity="0.9"/>
    ${kicker(card.angle, 1)}
    ${txt(76, 310, 'A VERDADE', { size: 26, fill: P.taupe, weight: 700, spacing: 5 })}
    ${multiline(card.title, 74, 470, 108, { size: 86, fill: P.ivory, family: SERIF, weight: 700, spacing: -3 })}
    <line x1="76" y1="660" x2="665" y2="660" stroke="${P.taupe}" stroke-width="3" opacity="0.65"/>
    ${multiline(card.subtitle, 78, 750, 78, { size: 52, fill: P.wine, family: SERIF, weight: 700, style: 'italic', spacing: -1.6 })}
    ${txt(1004, 1195, card.cta, { size: 20, fill: P.ivory, weight: 700, spacing: 3, anchor: 'end' })}`;
  return svg(P.black, body);
}

function card2(card) {
  let body = kicker(card.angle, 2) + ghostNumber(1, 55, 430);
  body += `
    <g transform="translate(680 260)">
      <path d="M0 0 L190 70 L190 250 C190 380 100 455 0 500 C-100 455 -190 380 -190 250 L-190 70 Z" fill="url(#wineGrad)"/>
      <path d="M-52 248 L-8 292 L82 180" fill="none" stroke="${P.ivory}" stroke-width="22" stroke-linecap="round" stroke-linejoin="round"/>
      <path d="M-330 100 L-205 130" stroke="${P.ivory}" stroke-width="9" opacity="0.85" marker-end="url(#arrowIvory)"/>
      <path d="M-350 230 L-210 230" stroke="${P.ivory}" stroke-width="9" opacity="0.85" marker-end="url(#arrowIvory)"/>
      <path d="M-330 360 L-205 330" stroke="${P.ivory}" stroke-width="9" opacity="0.85" marker-end="url(#arrowIvory)"/>
      <circle cx="-350" cy="100" r="13" fill="${P.ivory}"/>
      <circle cx="-370" cy="230" r="13" fill="${P.ivory}"/>
      <circle cx="-350" cy="360" r="13" fill="${P.ivory}"/>
    </g>
    ${multiline(card.title, 76, 825, 100, { size: 86, fill: P.ivory, family: SERIF, weight: 700, spacing: -3 })}
    ${multiline(card.body, 78, 1075, 44, { size: 29, fill: P.taupe, weight: 600, spacing: -0.7 })}`;
  return svg(P.blackSoft, body);
}

function card3(card) {
  let body = kicker(card.angle, 3, true) + ghostNumber(2, 710, 420, true);
  body += `
    <path d="M80 440 H390 M125 440 V930 M345 440 V930 M95 930 H375" fill="none" stroke="${P.wine}" stroke-width="6" opacity="0.55"/>
    <path d="M88 440 Q235 300 382 440" fill="none" stroke="${P.wine}" stroke-width="6" opacity="0.55"/>
    ${multiline(card.intro, 470, 330, 62, { size: 41, fill: P.black, weight: 700, spacing: -1.4 })}
    ${txt(425, 640, '“', { size: 250, fill: P.wine, family: SERIF, opacity: 0.18 })}
    ${multiline(card.quote, 470, 640, 79, { size: 55, fill: P.black, family: SERIF, weight: 700, style: 'italic', spacing: -2 })}
    ${txt(470, 1015, card.source, { size: 25, fill: P.wine, family: SERIF, weight: 700, style: 'italic' })}`;
  return svg(P.ivory, body, true);
}

function card4(card) {
  let body = kicker(card.angle, 4) + ghostNumber(3, 710, 415);
  body += `
    ${multiline(card.title, 76, 265, 83, { size: 73, fill: P.ivory, family: SERIF, weight: 700, spacing: -2.5 })}
    <g transform="translate(540 560)">
      <circle cx="-350" cy="-80" r="25" fill="${P.ivory}"/>
      <circle cx="-230" cy="-130" r="25" fill="${P.wine}"/>
      <circle cx="-90" cy="-75" r="25" fill="${P.ivory}"/>
      <circle cx="50" cy="-140" r="25" fill="${P.wine}"/>
      <circle cx="200" cy="-70" r="25" fill="${P.ivory}"/>
      <circle cx="335" cy="-125" r="25" fill="${P.wine}"/>
      <path d="M-420 0 H420 L160 300 H-160 Z" fill="none" stroke="${P.taupe}" stroke-width="8"/>
      <path d="M-160 300 H160 V430 H-160 Z" fill="${P.wineDark}"/>
      <circle cx="-70" cy="365" r="22" fill="${P.wine}"/>
      <circle cx="0" cy="365" r="22" fill="${P.wine}"/>
      <circle cx="70" cy="365" r="22" fill="${P.wine}"/>
      <path d="M-320 -30 L-225 65" stroke="${P.ivory}" stroke-width="5" opacity="0.35"/>
      <path d="M-210 -65 L-120 40" stroke="${P.wine}" stroke-width="7"/>
      <path d="M70 -80 L60 45" stroke="${P.wine}" stroke-width="7"/>
      <path d="M310 -60 L175 70" stroke="${P.wine}" stroke-width="7"/>
    </g>
    ${multiline(card.body, 76, 1020, 43, { size: 29, fill: P.ivorySoft, weight: 600, spacing: -0.7 })}
    ${txt(76, 1175, card.source, { size: 22, fill: P.taupe, family: SERIF, weight: 700, style: 'italic' })}`;
  return svg(P.black, body);
}

function card5(card) {
  let body = kicker(card.angle, 5) + ghostNumber(4, 55, 410);
  body += `
    <g transform="translate(775 385)">
      <ellipse cx="0" cy="0" rx="190" ry="255" fill="none" stroke="${P.ivory}" stroke-width="8" opacity="0.75"/>
      <ellipse cx="0" cy="0" rx="145" ry="205" fill="none" stroke="${P.taupe}" stroke-width="3" opacity="0.45"/>
      <path d="M-72 -15 Q0 -88 72 -15 Q0 58 -72 -15 Z" fill="none" stroke="${P.ivory}" stroke-width="9"/>
      <circle cx="0" cy="-15" r="27" fill="${P.ivory}"/>
      <path d="M-70 150 Q0 95 70 150" fill="none" stroke="${P.taupe}" stroke-width="6" opacity="0.7"/>
    </g>
    ${multiline(card.title, 76, 600, 105, { size: 91, fill: P.ivory, family: SERIF, weight: 700, spacing: -3 })}
    ${multiline(card.body, 78, 890, 63, { size: 44, fill: P.ivorySoft, weight: 700, spacing: -1.3 })}`;
  return svg(P.wineDark, body);
}

function card6(card) {
  let body = `
    <rect width="540" height="1350" fill="${P.black}" filter="url(#grain)"/>
    <rect x="540" width="540" height="1350" fill="${P.ivory}" filter="url(#grain)"/>
    <rect x="76" y="75" width="52" height="6" rx="3" fill="${P.wine}"/>
    ${txt(146, 84, card.angle, { size: 20, fill: P.taupe, weight: 700, spacing: 3.7 })}
    ${txt(1004, 84, '06 / 09', { size: 18, fill: P.wine, weight: 700, spacing: 2.2, anchor: 'end' })}
    <g transform="translate(270 360)">
      <path d="M-105 0 A105 105 0 1 1 45 95" fill="none" stroke="${P.wine}" stroke-width="16" marker-end="url(#arrowWine)"/>
      <circle cx="0" cy="0" r="22" fill="${P.ivory}"/>
    </g>
    <g transform="translate(810 360)">
      <circle cx="0" cy="0" r="112" fill="none" stroke="${P.wine}" stroke-width="9"/>
      <path d="M-58 32 L-10 78 L78 -45" fill="none" stroke="${P.wine}" stroke-width="16" stroke-linecap="round" stroke-linejoin="round"/>
    </g>
    ${txt(76, 620, card.left.title, { size: 47, fill: P.wine, weight: 800, spacing: 2 })}
    ${multiline(card.left.question, 76, 735, 76, { size: 48, fill: P.ivory, family: SERIF, weight: 700, spacing: -1.8 })}
    ${txt(590, 620, card.right.title, { size: 47, fill: P.wine, weight: 800, spacing: 2 })}
    ${multiline(card.right.question, 590, 735, 76, { size: 48, fill: P.black, family: SERIF, weight: 700, spacing: -1.8 })}
    <line x1="540" y1="170" x2="540" y2="1165" stroke="${P.taupe}" stroke-width="2" opacity="0.45"/>
    <line x1="76" y1="1244" x2="1004" y2="1244" stroke="${P.taupe}" stroke-width="2" opacity="0.62"/>
    ${txt(76, 1288, content.handle, { size: 18, fill: P.taupe, weight: 700, spacing: 2.1 })}
    ${txt(1004, 1288, content.brand, { size: 18, fill: P.black, weight: 700, spacing: 2.1, anchor: 'end' })}`;
  return `<?xml version="1.0" encoding="UTF-8"?><svg xmlns="http://www.w3.org/2000/svg" width="${W}" height="${H}" viewBox="0 0 ${W} ${H}">${defs()}${body}</svg>`;
}

function card7(card) {
  let body = kicker(card.angle, 7, true) + ghostNumber(6, 700, 420, true);
  body += `${txt(76, 255, card.title, { size: 66, fill: P.black, family: SERIF, weight: 700, spacing: -2.2 })}`;
  const positions = [430, 610, 790, 970];
  body += `<line x1="132" y1="430" x2="132" y2="970" stroke="${P.taupe}" stroke-width="6" opacity="0.7"/>`;
  card.steps.forEach((step, i) => {
    const y = positions[i];
    body += `<circle cx="132" cy="${y}" r="58" fill="${i % 2 ? P.wineDark : P.wine}"/>`;
    body += txt(132, y + 18, String(i + 1).padStart(2, '0'), { size: 50, fill: P.ivory, weight: 800, spacing: -2, anchor: 'middle' });
    if (i === 2) {
      body += multiline(['Defina o que mudaria', 'sua conclusão.'], 235, y - 12, 47, { size: 35, fill: P.black, weight: 700, spacing: -1.1 });
    } else {
      body += txt(235, y + 14, step, { size: 39, fill: P.black, weight: 700, spacing: -1.2 });
    }
  });
  body += `${txt(76, 1170, card.source, { size: 21, fill: P.wine, family: SERIF, weight: 700, style: 'italic' })}`;
  return svg(P.ivory, body, true);
}

function card8(card) {
  let body = kicker(card.angle, 8) + ghostNumber(7, 700, 410);
  body += `
    ${txt(76, 255, 'CRENÇA INICIAL', { size: 22, fill: P.taupe, weight: 800, spacing: 3.5 })}
    <rect x="76" y="300" width="928" height="135" rx="18" fill="${P.wineDark}"/>
    ${txt(540, 387, card.belief, { size: 57, fill: P.ivory, family: SERIF, weight: 700, style: 'italic', spacing: -2, anchor: 'middle' })}
    <path d="M540 435 V525 M540 525 H270 V590 M540 525 H810 V590" fill="none" stroke="${P.taupe}" stroke-width="6"/>
    <rect x="76" y="590" width="388" height="175" rx="18" fill="${P.blackSoft}" stroke="${P.wine}" stroke-width="5"/>
    <rect x="616" y="590" width="388" height="175" rx="18" fill="${P.blackSoft}" stroke="${P.taupe}" stroke-width="5"/>
    ${txt(270, 655, card.evidenceA, { size: 29, fill: P.ivory, weight: 700, anchor: 'middle' })}
    ${txt(270, 715, 'CONTA COMO PROVA ✓', { size: 20, fill: P.wine, weight: 800, spacing: 2, anchor: 'middle' })}
    ${txt(810, 655, card.evidenceB, { size: 27, fill: P.ivory, weight: 700, anchor: 'middle' })}
    ${txt(810, 715, 'VIRA “EXCEÇÃO” ×', { size: 20, fill: P.taupe, weight: 800, spacing: 2, anchor: 'middle' })}
    <path d="M270 765 V875 H540 M810 765 V875 H540 V935" fill="none" stroke="${P.taupe}" stroke-width="6"/>
    <rect x="210" y="935" width="660" height="145" rx="72" fill="${P.wine}"/>
    ${txt(540, 1025, card.result, { size: 38, fill: P.ivory, weight: 800, spacing: 2.5, anchor: 'middle' })}`;
  return svg(P.black, body);
}

function card9(card) {
  let body = kicker(card.angle, 9) + `
    ${txt(920, 470, '?', { size: 520, fill: P.ivory, family: SERIF, weight: 700, opacity: 0.055, anchor: 'middle' })}
    <path d="M850 90 C970 150 1010 260 1060 430" fill="none" stroke="${P.wine}" stroke-width="18" opacity="0.8"/>
    ${multiline(card.question, 76, 330, 96, { size: 71, fill: P.ivory, family: SERIF, weight: 700, spacing: -2.7 })}
    <rect x="0" y="805" width="1080" height="300" fill="${P.wineDark}"/>
    ${multiline(card.closing, 540, 925, 73, { size: 42, fill: P.ivory, family: SERIF, weight: 700, style: 'italic', spacing: -1.5, anchor: 'middle' })}
    ${txt(540, 1165, card.cta, { size: 21, fill: P.taupe, weight: 800, spacing: 4.2, anchor: 'middle' })}`;
  return svg(P.black, body);
}

const renderers = [card1, card2, card3, card4, card5, card6, card7, card8, card9];

async function render(filename, source) {
  const target = path.join(OUT, filename);
  const temporary = `${target}.tmp-${process.pid}.png`;
  await sharp(Buffer.from(source)).png({ compressionLevel: 9 }).toFile(temporary);
  fs.renameSync(temporary, target);
}

async function validate() {
  if (content.cards.length !== 9) throw new Error(`Esperados 9 cards; encontrados ${content.cards.length}.`);
  for (const card of content.cards) {
    const file = path.join(OUT, card.filename);
    if (!fs.existsSync(file)) throw new Error(`Arquivo ausente: ${file}`);
    const metadata = await sharp(file).metadata();
    if (metadata.width !== W || metadata.height !== H) {
      throw new Error(`${card.filename}: ${metadata.width}x${metadata.height}; esperado ${W}x${H}.`);
    }
  }
  console.log('OK: 9 cards válidos em 1080x1350.');
}

async function preview() {
  const thumbW = 270;
  const thumbH = 338;
  const gap = 22;
  const canvasW = thumbW * 3 + gap * 4;
  const canvasH = thumbH * 3 + gap * 4;
  const inputs = [];
  for (let i = 0; i < content.cards.length; i += 1) {
    const input = await sharp(path.join(OUT, content.cards[i].filename)).resize(thumbW, thumbH).png().toBuffer();
    inputs.push({ input, left: gap + (i % 3) * (thumbW + gap), top: gap + Math.floor(i / 3) * (thumbH + gap) });
  }
  await sharp({ create: { width: canvasW, height: canvasH, channels: 4, background: '#D8D1C8' } })
    .composite(inputs)
    .png()
    .toFile(path.join(OUT, 'preview.png'));
}

async function main() {
  if (process.argv.includes('--validate-only')) {
    await validate();
    return;
  }
  for (let i = 0; i < content.cards.length; i += 1) {
    await render(content.cards[i].filename, renderers[i](content.cards[i]));
  }
  await validate();
  await preview();
  console.log(`Carrossel gerado em ${OUT}`);
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
