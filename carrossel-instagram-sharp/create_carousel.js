const sharp = require('sharp');
const fs = require('fs');
const path = require('path');

const W = 1080;
const H = 1350;
const contentPath = path.resolve(process.env.CONTENT_FILE || 'conteudo.json');
const outputDir = path.resolve(process.env.OUTPUT_DIR || 'saida');

if (!fs.existsSync(contentPath)) {
  throw new Error(`Arquivo de conteúdo não encontrado: ${contentPath}`);
}

const content = JSON.parse(fs.readFileSync(contentPath, 'utf8'));
const palette = content.palette;
const fonts = content.fonts || {};
const sans = fonts.sans || 'Arial, Helvetica, DejaVu Sans, sans-serif';
const serif = fonts.serif || 'Georgia, Times New Roman, DejaVu Serif, serif';
const totalPages = String(content.totalPages || 9).padStart(2, '0');

fs.mkdirSync(outputDir, { recursive: true });

function esc(value) {
  return String(value)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;');
}

function color(value) {
  return palette[value] || value;
}

function defs() {
  return `
    <defs>
      <filter id="grain" x="0" y="0" width="100%" height="100%">
        <feTurbulence type="fractalNoise" baseFrequency="0.72" numOctaves="3" seed="29" result="noise"/>
        <feColorMatrix in="noise" type="saturate" values="0" result="mono"/>
        <feComponentTransfer in="mono" result="faint">
          <feFuncA type="table" tableValues="0 0.045"/>
        </feComponentTransfer>
        <feBlend in="SourceGraphic" in2="faint" mode="soft-light"/>
      </filter>
      <linearGradient id="wineGlow" x1="0" y1="0" x2="1" y2="1">
        <stop offset="0" stop-color="${palette.wine}" stop-opacity="0.96"/>
        <stop offset="1" stop-color="${palette.wineDark}" stop-opacity="0.5"/>
      </linearGradient>
    </defs>`;
}

function footer(page, onLight = false, extra = '') {
  const ink = onLight ? palette.black : palette.ivory;
  const quiet = onLight ? palette.wine : palette.taupe;
  return `
    <line x1="76" y1="1246" x2="1004" y2="1246" stroke="${quiet}" stroke-width="2" opacity="0.62"/>
    <text x="76" y="1290" fill="${ink}" font-family="${sans}" font-size="20" font-weight="700" letter-spacing="3.4">${esc(content.brand)}</text>
    <text x="1004" y="1290" text-anchor="end" fill="${quiet}" font-family="${sans}" font-size="19" font-weight="700" letter-spacing="2">${esc(page)} / ${totalPages}</text>
    ${extra}`;
}

function grainRect(fill) {
  return `<rect width="${W}" height="${H}" fill="${fill}" filter="url(#grain)"/>`;
}

function baseSvg(background, page, body, onLight = false) {
  return `<?xml version="1.0" encoding="UTF-8"?>
  <svg xmlns="http://www.w3.org/2000/svg" width="${W}" height="${H}" viewBox="0 0 ${W} ${H}">
    ${defs()}
    ${grainRect(background)}
    ${body}
    ${footer(page, onLight)}
  </svg>`;
}

function textLine(x, y, text, opts = {}) {
  const {
    size = 76,
    fill = palette.ivory,
    weight = 700,
    family = sans,
    anchor = 'start',
    spacing = -1.6,
    style = 'normal',
    opacity = 1,
  } = opts;
  return `<text x="${x}" y="${y}" text-anchor="${anchor}" fill="${fill}" opacity="${opacity}" font-family="${family}" font-size="${size}" font-weight="${weight}" font-style="${style}" letter-spacing="${spacing}">${esc(text)}</text>`;
}

function kicker(text, onLight = false, x = 80, y = 126, accent = palette.wine) {
  const ink = onLight ? palette.wine : palette.taupe;
  return `
    <rect x="${x}" y="${y - 26}" width="52" height="5" rx="2.5" fill="${accent}"/>
    <text x="${x + 70}" y="${y - 15}" fill="${onLight ? ink : accent}" font-family="${sans}" font-size="21" font-weight="700" letter-spacing="3.8">${esc(text)}</text>`;
}

function numberGhost(number, onLight = false) {
  const fill = onLight ? palette.wine : palette.ivory;
  return `<text x="70" y="475" fill="${fill}" opacity="0.07" font-family="${sans}" font-size="390" font-weight="700" letter-spacing="-18">${esc(number)}</text>`;
}

async function renderSvg(filename, svg, composites = []) {
  const finalPath = path.join(outputDir, filename);
  const tempPath = `${finalPath}.tmp-${process.pid}.png`;
  const image = sharp(Buffer.from(svg));
  if (composites.length) image.composite(composites);
  const rendered = await image.ensureAlpha().raw().toBuffer({ resolveWithObject: true });
  await sharp(rendered.data, {
    raw: {
      width: rendered.info.width,
      height: rendered.info.height,
      channels: rendered.info.channels,
    },
  }).png({ compressionLevel: 9 }).toFile(tempPath);
  fs.renameSync(tempPath, finalPath);
}

function orderedNames() {
  return [
    content.cover.filename,
    ...content.slides.map((slide) => slide.filename),
    content.final.filename,
  ];
}

async function createPreview() {
  const names = orderedNames();
  const thumbW = 216;
  const thumbH = 270;
  const gap = 20;
  const previewW = thumbW * 3 + gap * 4;
  const previewH = thumbH * 3 + gap * 4;
  const composites = [];

  for (let index = 0; index < names.length; index += 1) {
    const input = await sharp(path.join(outputDir, names[index]))
      .resize(thumbW, thumbH)
      .png()
      .toBuffer();
    composites.push({
      input,
      left: gap + (index % 3) * (thumbW + gap),
      top: gap + Math.floor(index / 3) * (thumbH + gap),
    });
  }

  await sharp({
    create: {
      width: previewW,
      height: previewH,
      channels: 4,
      background: '#D8D1C8',
    },
  }).composite(composites).png().toFile(path.join(outputDir, 'preview.png'));
}

function effectSlide(slide) {
  const background = color(slide.background);
  const accent = color(slide.accent || 'wine');
  const main = slide.onLight ? palette.black : palette.ivory;
  const lines = slide.lines;
  const lineStart = lines.length === 3 ? 548 : lines.length === 4 ? 500 : 455;
  const lineGap = lines.length >= 5 ? 90 : 102;
  let body = kicker(slide.kickerText || 'EFEITO COLATERAL', slide.onLight, 80, 126, accent);
  body += numberGhost(slide.number, slide.onLight);
  body += `<circle cx="946" cy="180" r="92" fill="none" stroke="${slide.onLight ? palette.wine : palette.taupe}" stroke-width="2" opacity="0.35"/>`;
  body += `<path d="M900 220 C970 170, 1018 178, 1065 120" fill="none" stroke="${accent}" stroke-width="10" opacity="0.92"/>`;

  lines.forEach((line, index) => {
    body += textLine(80, lineStart + index * lineGap, line.text, {
      size: line.size || 73,
      fill: line.accent ? accent : main,
      weight: line.weight || 700,
      spacing: line.spacing ?? -1.8,
      family: line.serif ? serif : sans,
      style: line.italic ? 'italic' : 'normal',
    });
  });

  return baseSvg(background, slide.page, body, slide.onLight);
}

function coverSvg() {
  const cover = content.cover;
  return `<?xml version="1.0" encoding="UTF-8"?>
    <svg xmlns="http://www.w3.org/2000/svg" width="${W}" height="${H}" viewBox="0 0 ${W} ${H}">
      ${defs()}
      ${grainRect(palette.black)}
      <rect x="0" y="0" width="22" height="1350" fill="${palette.wine}"/>
      <rect x="760" y="0" width="320" height="1350" fill="${palette.wineDark}" opacity="0.78"/>
      <circle cx="920" cy="200" r="118" fill="none" stroke="${palette.taupe}" stroke-width="2" opacity="0.4"/>
      <circle cx="920" cy="200" r="82" fill="none" stroke="${palette.taupe}" stroke-width="2" opacity="0.22"/>
      <text x="1035" y="1060" text-anchor="end" fill="${palette.ivory}" opacity="0.10" font-family="${sans}" font-size="820" font-weight="700" letter-spacing="-40">${esc(cover.number)}</text>
      <text x="78" y="95" fill="${palette.taupe}" font-family="${sans}" font-size="20" font-weight="700" letter-spacing="3.6">${esc(cover.topline)}</text>
      <text x="1002" y="95" text-anchor="end" fill="${palette.taupe}" font-family="${sans}" font-size="19" font-weight="700" letter-spacing="2">01 / ${totalPages}</text>
      <text x="76" y="305" fill="${palette.wine}" font-family="${sans}" font-size="103" font-weight="700" letter-spacing="-5">${esc(cover.titleLine1)}</text>
      <text x="76" y="420" fill="${palette.ivory}" font-family="${sans}" font-size="97" font-weight="700" letter-spacing="-5">${esc(cover.titleLine2)}</text>
      <line x1="78" y1="485" x2="680" y2="485" stroke="${palette.taupe}" stroke-width="3" opacity="0.8"/>
      <text x="80" y="560" fill="${palette.taupe}" font-family="${sans}" font-size="35" font-weight="700" letter-spacing="1.2">${esc(cover.preTitle)}</text>
      <text x="76" y="700" fill="${palette.ivory}" font-family="${serif}" font-size="104" font-weight="700" font-style="italic" letter-spacing="-3">${esc(cover.subjectLine1)}</text>
      <text x="76" y="808" fill="${palette.ivory}" font-family="${serif}" font-size="104" font-weight="700" font-style="italic" letter-spacing="-3">${esc(cover.subjectLine2)}</text>
      <text x="80" y="960" fill="${palette.taupe}" font-family="${sans}" font-size="27" font-weight="700" letter-spacing="1.4">${esc(cover.subtitleLine1)}</text>
      <text x="80" y="1003" fill="${palette.taupe}" font-family="${sans}" font-size="27" font-weight="700" letter-spacing="1.4">${esc(cover.subtitleLine2)}</text>
      <line x1="76" y1="1246" x2="1004" y2="1246" stroke="${palette.taupe}" stroke-width="2" opacity="0.62"/>
      <text x="76" y="1290" fill="${palette.ivory}" font-family="${sans}" font-size="20" font-weight="700" letter-spacing="3.4">${esc(content.brand)}</text>
      <text x="1004" y="1290" text-anchor="end" fill="${palette.taupe}" font-family="${sans}" font-size="19" font-weight="700" letter-spacing="2.2">${esc(cover.cta)}</text>
    </svg>`;
}

function finalSvg() {
  const final = content.final;
  return `<?xml version="1.0" encoding="UTF-8"?>
    <svg xmlns="http://www.w3.org/2000/svg" width="${W}" height="${H}" viewBox="0 0 ${W} ${H}">
      ${defs()}
      ${grainRect(palette.black)}
      <text x="965" y="330" text-anchor="end" fill="${palette.ivory}" opacity="0.055" font-family="${serif}" font-size="520" font-weight="700">”</text>
      <path d="M820 80 C930 115, 1015 210, 1060 350" fill="none" stroke="${palette.wine}" stroke-width="18" opacity="0.75"/>
      ${kicker(final.kicker, false)}
      <text x="78" y="258" fill="${palette.ivory}" font-family="${sans}" font-size="58" font-weight="700" letter-spacing="-1.2">${esc(final.line1)}</text>
      <text x="78" y="330" fill="${palette.ivory}" font-family="${sans}" font-size="58" font-weight="700" letter-spacing="-1.2">${esc(final.line2)}</text>
      <text x="78" y="455" fill="${palette.taupe}" font-family="${sans}" font-size="49" font-weight="700" letter-spacing="-1">${esc(final.line3)}</text>
      <text x="78" y="605" fill="${palette.wine}" font-family="${serif}" font-size="92" font-weight="700" font-style="italic" letter-spacing="-2.7">${esc(final.line4)}</text>
      <text x="78" y="715" fill="${palette.ivory}" font-family="${sans}" font-size="77" font-weight="700" letter-spacing="-2">${esc(final.line5)}</text>
      <rect x="0" y="820" width="1080" height="326" fill="${palette.wineDark}"/>
      <text x="540" y="967" text-anchor="middle" fill="${palette.ivory}" font-family="${serif}" font-size="72" font-weight="700" font-style="italic" letter-spacing="-1.4">${esc(final.line6)}</text>
      <text x="540" y="1055" text-anchor="middle" fill="${palette.ivory}" font-family="${serif}" font-size="72" font-weight="700" font-style="italic" letter-spacing="-1.4">${esc(final.line7)}</text>
      ${footer(final.page, false)}
    </svg>`;
}

async function validateOutput() {
  const names = orderedNames();
  if (names.length !== content.totalPages) {
    throw new Error(`A configuração declara ${content.totalPages} páginas, mas há ${names.length} arquivos.`);
  }

  for (const name of names) {
    const file = path.join(outputDir, name);
    if (!fs.existsSync(file)) throw new Error(`Arquivo ausente: ${file}`);
    const metadata = await sharp(file).metadata();
    if (metadata.width !== W || metadata.height !== H) {
      throw new Error(`${name} está em ${metadata.width}x${metadata.height}; esperado: ${W}x${H}.`);
    }
    await sharp(file).raw().toBuffer();
  }
  console.log(`OK: ${names.length} cards válidos em ${W}x${H}.`);
}

async function main() {
  if (process.argv.includes('--validate-only')) {
    await validateOutput();
    return;
  }

  await renderSvg(content.cover.filename, coverSvg());
  for (const slide of content.slides) {
    await renderSvg(slide.filename, effectSlide(slide));
  }
  await renderSvg(content.final.filename, finalSvg());
  await validateOutput();
  await createPreview();
  console.log(`Arquivos gerados em: ${outputDir}`);
  console.log(`Prévia geral: ${path.join(outputDir, 'preview.png')}`);
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
