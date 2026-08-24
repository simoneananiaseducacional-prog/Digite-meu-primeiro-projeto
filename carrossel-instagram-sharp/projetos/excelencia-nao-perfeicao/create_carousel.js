const fs = require('fs');
const path = require('path');
const sharp = require('sharp');

const W = 1080, H = 1350;
const BG = '#050505', WHITE = '#F4F3EF', ORANGE = '#F2A21A', MUTED = '#A8A8A8';
const FONT = 'DejaVu Sans, Arial, Helvetica, sans-serif';
const OUT = path.join(__dirname, 'saida');
fs.mkdirSync(OUT, { recursive: true });
const data = JSON.parse(fs.readFileSync(path.join(__dirname, 'conteudo.json'), 'utf8'));

const esc = s => String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;');
const t = (x,y,text,size=64,opts={}) => `<text x="${x}" y="${y}" font-family="${FONT}" font-size="${size}" font-weight="${opts.weight||500}" fill="${opts.fill||WHITE}" ${opts.anchor?`text-anchor="${opts.anchor}"`:''} ${opts.italic?'font-style="italic"':''}>${esc(text)}</text>`;
const base = (kicker, page) => `
  <rect width="1080" height="1350" fill="${BG}"/>
  ${t(78,120,'“',108,{weight:800,fill:ORANGE})}
  ${t(82,195,kicker,28,{weight:700,fill:ORANGE})}
  <line x1="82" y1="1190" x2="998" y2="1190" stroke="${ORANGE}" stroke-width="4"/>
  ${t(82,1238,data.brand,24,{weight:600,fill:WHITE})}
  ${t(998,1238,String(page).padStart(2,'0'),22,{weight:600,fill:MUTED,anchor:'end'})}
`;

function textSlide(slide, page){
  let y = 380;
  const parts = [base(slide.kicker,page)];
  const n = slide.lines.length;
  for (const line of slide.lines){
    const size = line.tiny ? 34 : line.small ? 48 : (n>=7 ? 66 : 74);
    const gap = line.tiny ? 54 : line.small ? 66 : 88;
    parts.push(t(82,y,line.text,size,{weight:line.weight||500,fill:line.accent?ORANGE:WHITE}));
    y += gap;
  }
  if (slide.footnote) parts.push(t(82,1125,slide.footnote,26,{weight:500,fill:MUTED}));
  if (slide.cta) parts.push(t(82,1118,slide.cta,24,{weight:700,fill:ORANGE}));
  return svg(parts.join('\n'));
}

function contrastSlide(slide,page){
  const p=[base(slide.kicker,page)];
  p.push(`<line x1="540" y1="330" x2="540" y2="1030" stroke="#2B2B2B" stroke-width="2"/>`);
  p.push(t(82,360,slide.left.title,48,{weight:800,fill:WHITE}));
  p.push(t(582,360,slide.right.title,48,{weight:800,fill:ORANGE}));
  let y=465;
  slide.left.items.forEach((it,i)=>{ p.push(t(82,y,'•',40,{weight:800,fill:ORANGE})); p.push(t(120,y,it,34,{weight:i===0?700:500,fill:WHITE})); y+=145; });
  y=465;
  slide.right.items.forEach((it,i)=>{ p.push(t(582,y,'•',40,{weight:800,fill:ORANGE})); p.push(t(620,y,it,34,{weight:i===0?700:500,fill:WHITE})); y+=145; });
  p.push(t(82,1055,'Perfeição tenta impedir o erro.',30,{weight:500,fill:MUTED}));
  p.push(t(82,1105,'Excelência usa o erro para ajustar.',30,{weight:700,fill:WHITE}));
  return svg(p.join('\n'));
}

function stepsSlide(slide,page){
  const p=[base(slide.kicker,page)];
  let y=390;
  slide.steps.forEach(([num,a,b])=>{
    p.push(`<circle cx="130" cy="${y-20}" r="47" fill="${ORANGE}"/>`);
    p.push(t(130,y-6,num,28,{weight:800,fill:BG,anchor:'middle'}));
    p.push(t(215,y-34,a,43,{weight:500,fill:WHITE}));
    p.push(t(215,y+22,b,43,{weight:800,fill:WHITE}));
    y += 220;
  });
  p.push(t(82,1080,'Avançar também é uma decisão.',32,{weight:700,fill:ORANGE}));
  return svg(p.join('\n'));
}

function demoSlide(slide,page){
  const p=[base(slide.kicker,page)];
  p.push(t(82,365,'PERFEIÇÃO',34,{weight:800,fill:MUTED}));
  p.push(`<rect x="82" y="405" rx="22" ry="22" width="916" height="235" fill="#151515" stroke="#2B2B2B"/>`);
  p.push(t(125,495,'“Só publico quando',48,{weight:500,fill:WHITE}));
  p.push(t(125,560,'estiver impecável.”',48,{weight:800,fill:WHITE}));
  p.push(t(82,745,'EXCELÊNCIA',34,{weight:800,fill:ORANGE}));
  p.push(`<rect x="82" y="785" rx="22" ry="22" width="916" height="300" fill="#12100B" stroke="${ORANGE}" stroke-width="2"/>`);
  p.push(t(125,875,'“Publico quando estiver',44,{weight:500,fill:WHITE}));
  p.push(t(125,935,'sólido, revisado e útil.',44,{weight:800,fill:WHITE}));
  p.push(t(125,995,'Depois aprimoro.”',44,{weight:800,fill:ORANGE}));
  return svg(p.join('\n'));
}

function svg(inner){ return Buffer.from(`<svg xmlns="http://www.w3.org/2000/svg" width="${W}" height="${H}">${inner}</svg>`); }

(async()=>{
  const outputs=[];
  for(let i=0;i<data.slides.length;i++){
    const s=data.slides[i];
    let buf;
    if(s.mode==='contrast') buf=contrastSlide(s,i+1);
    else if(s.mode==='steps') buf=stepsSlide(s,i+1);
    else if(s.mode==='demo') buf=demoSlide(s,i+1);
    else buf=textSlide(s,i+1);
    const dest=path.join(OUT,s.file);
    await sharp(buf).png().toFile(dest);
    outputs.push(dest);
  }
  const thumbW=360, thumbH=450;
  const canvas=sharp({create:{width:1080,height:1350,channels:4,background:'#111'}});
  const comps=[];
  for(let i=0;i<outputs.length;i++){
    const thumb=await sharp(outputs[i]).resize(thumbW,thumbH,{fit:'cover'}).png().toBuffer();
    comps.push({input:thumb,left:(i%3)*thumbW,top:Math.floor(i/3)*thumbH});
  }
  await canvas.composite(comps).png().toFile(path.join(OUT,'preview.png'));
  console.log('Gerados:', outputs.length, 'cards');
})();
