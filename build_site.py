
# Read existing index.html to extract scripts we need to keep
with open('index.html', 'r', encoding='utf-8') as f:
    existing = f.read()

# Extract pixel script
import re
pixel_script = re.search(r'<script>\s*window\.pixelId.*?</script>', existing, re.DOTALL)
pixel_html = pixel_script.group(0) if pixel_script else ''

clarity_script = re.search(r'<script>\s*\(function\(c,l,a,r,i,t,y\).*?</script>', existing, re.DOTALL)
clarity_html = clarity_script.group(0) if clarity_script else ''

utm_tracking = re.search(r'<script>\s*\(function\(\).*?window\._ppUtms.*?\}\)\(\);\s*</script>', existing, re.DOTALL)
utm_html = utm_tracking.group(0) if utm_tracking else ''

modal_html = re.search(r'<!-- MODAL SUPER DESCONTO -->.*?</div>\s*\n\n<script>', existing, re.DOTALL)
modal_content = modal_html.group(0).replace('\n\n<script>','') if modal_html else ''

# ── PAPER IMAGE URLS ──────────────────────
papers = [
    'https://i.ibb.co/KjxzKgKC/PAPER-01-3-P.webp',
    'https://i.ibb.co/TBCgR7TY/PAPER-02-P.webp',
    'https://i.ibb.co/hxVtvyX4/PAPER-03-P.webp',
    'https://i.ibb.co/sp7snLBR/PAPER-04-P.webp',
    'https://i.ibb.co/VpMzPqCD/PAPER-05-P.webp',
    'https://i.ibb.co/r2KDPYQs/PAPER-06-P.webp',
    'https://i.ibb.co/0yVgwmwv/PAPER-07-P.webp',
    'https://i.ibb.co/Dfd9Hdtj/PAPER-08-P.webp',
    'https://i.ibb.co/1f6vSzdv/PAPER-09-P.webp',
    'https://i.ibb.co/Gv0c1X6J/PAPER-10-P.webp',
    'https://i.ibb.co/gMZs85JP/PAPER-11-P.webp',
    'https://i.ibb.co/LXDR6779/PAPER-12-P.webp',
    'https://i.ibb.co/whPg9DBk/PAPER-13-P.webp',
    'https://i.ibb.co/xy7Y0q8/PAPER-14-P.webp',
    'https://i.ibb.co/WvfXR2z1/PAPER-15-P.webp',
    'https://i.ibb.co/Z1kv7Rb3/PAPER-16-P.webp',
    'https://i.ibb.co/qLSw3KD2/PAPER-17-P.webp',
    'https://i.ibb.co/WvzVPDnW/PAPER-18-P.webp',
    'https://i.ibb.co/tpYvwD8D/PAPER-19-P.webp',
]
provas = [
    'https://i.ibb.co/SDyybVhn/PROVA-01-P.webp',
    'https://i.ibb.co/HfhmZXcF/PROVA-02-P.webp',
    'https://i.ibb.co/v4RZ2DFg/PROVA-03-P.webp',
    'https://i.ibb.co/5gRQ9Ymb/PROVA-04-P.webp',
    'https://i.ibb.co/4ngSgGCK/PROVA-05-P.webp',
]
modulos = [
    'https://i.ibb.co/hxycsjjP/MODULO-01-VAI-RECEBER-P.webp',
    'https://i.ibb.co/vxRjrGrk/MODULO-02-VAI-RECEBER-P.webp',
    'https://i.ibb.co/TB4fV8h2/MODULO-03-VAI-RECEBER-P.webp',
]

def thumb(url, alt='', cls=''):
    return f'<img src="{url}" alt="{alt}" class="w-full h-full object-cover {cls}" loading="lazy">'

# Build gallery grid items
def gallery_item(url, i):
    return f'''<div class="relative overflow-hidden rounded-lg group cursor-pointer" style="aspect-ratio:1;">
<img src="{url}" alt="Papercraft {i+1}" class="w-full h-full object-cover transition-transform duration-500 group-hover:scale-110" loading="lazy">
<div class="absolute inset-0 bg-gradient-to-t from-black/40 to-transparent opacity-0 group-hover:opacity-100 transition-opacity"></div>
</div>'''

gallery_items = '\n'.join([gallery_item(p, i) for i, p in enumerate(papers)])

thumbnail_items = '\n'.join([f'<div class="flex-shrink-0 w-24 h-24 md:w-28 md:h-28 rounded-xl overflow-hidden border-2 border-white/20 shadow-lg"><img src="{p}" alt="papercraft" class="w-full h-full object-cover"></div>' for p in papers[:8]])

prova_items = '\n'.join([f'<div class="rounded-2xl overflow-hidden shadow-xl border-2 border-white/10"><img src="{p}" alt="Prova Social {i+1}" class="w-full h-auto" loading="lazy"></div>' for i, p in enumerate(provas)])

bonus_list = [
    ('🦁', 'Zoológico de Papercraft', '29,90'),
    ('🦸', 'Heróis', '35,00'),
    ('⚡', 'Animes e Mangás', '27,00'),
    ('🚗', 'Garagem de Carros', '27,00'),
    ('👑', 'Área de Membros Premium', '57,00'),
    ('🎧', 'Suporte Prioritário', '97,00'),
    ('📸', 'Galeria da Comunidade', '27,00'),
]

def bonus_card(icon, name, price, is_modal=False):
    rotate = 'rotate-1' if not is_modal else '-rotate-1'
    return f'''<div class="relative bg-white p-3 md:p-4 rounded-[4px] shadow-2xl border-2 border-white/20 transform transition-transform duration-300 hover:scale-[1.02] flex items-center gap-4 md:gap-6 group {rotate}">
  <div class="absolute h-6 w-20 shadow-sm backdrop-blur-[1px] z-20 bg-red-100/80 border-l-2 border-r-2 border-white/50 -top-3 left-1/2 -translate-x-1/2 opacity-90"></div>
  <div class="relative w-20 h-20 md:w-28 md:h-28 flex-shrink-0 rounded-sm overflow-hidden">
    <div class="w-full h-full bg-slate-100 flex items-center justify-center text-4xl">{icon}</div>
  </div>
  <div class="flex flex-col flex-grow text-left">
    <h3 class="text-lg md:text-xl font-marker text-slate-900 leading-tight mb-2 tracking-wide uppercase">{name}</h3>
    <div class="flex items-center justify-between mt-auto">
      <div class="flex flex-col md:flex-row md:items-center md:gap-1">
        <span class="text-[10px] text-slate-400 font-bold uppercase tracking-tighter opacity-70 leading-tight">Vendido por</span>
        <span class="text-[10px] text-slate-400 font-bold uppercase tracking-tighter line-through opacity-70 leading-tight">R$ {price}</span>
      </div>
      <div class="text-[#22C55E] flex items-center justify-center gap-1.5 transform -rotate-1 font-bold">
        <span class="text-sm">✓</span>
        <span class="font-marker text-[10px] md:text-xs tracking-wider uppercase">BÔNUS KIT MESTRE</span>
      </div>
    </div>
  </div>
</div>'''

bonus_cards = '\n'.join([bonus_card(b[0], b[1], b[2]) for b in bonus_list])

faq_items = [
    ('O papercraft é difícil de montar?', 'Não! Nossos moldes são projetados para todos os níveis. Cada peça vem com numeração e guia de encaixe. Mesmo iniciantes conseguem montar desde o primeiro dia.'),
    ('Preciso de algum material especial?', 'Apenas papel cartão (180–240g/m²), cola, tesoura e um estilete. Tudo disponível em papelaria por poucos reais.'),
    ('Vou receber os moldes fisicamente?', 'Não, o acesso é 100% digital. Você baixa os arquivos em PDF, imprime em qualquer gráfica ou impressora colorida e começa a montar.'),
    ('E se eu não conseguir montar?', 'Tem nossa garantia de 7 dias! Se não conseguir ou não gostar, devolvemos 100% do seu dinheiro sem perguntas.'),
    ('Quantos moldes estão inclusos?', 'São mais de 3.500 moldes divididos em categorias: personagens, animais, veículos, objetos e muito mais. Acesso vitalício.'),
    ('Como funciona o acesso?', 'Após a compra você recebe o acesso imediato à área de membros com todos os downloads disponíveis 24 horas por dia.'),
]

def faq_item(q, a, i):
    return f'''<div class="border-b border-slate-100 last:border-0" x-data="{{ open: false }}">
  <button class="faq-btn w-full flex items-center justify-between py-5 px-1 text-left gap-4" onclick="toggleFaq(this)">
    <span class="font-semibold text-slate-800 text-sm md:text-base">{q}</span>
    <svg class="faq-icon w-5 h-5 text-slate-400 flex-shrink-0 transition-transform duration-300" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"/></svg>
  </button>
  <div class="faq-answer overflow-hidden max-h-0 transition-all duration-300">
    <p class="text-slate-600 text-sm leading-relaxed pb-5 px-1">{a}</p>
  </div>
</div>'''

faq_html = '\n'.join([faq_item(q, a, i) for i, (q, a) in enumerate(faq_items)])

html = f'''<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1"/>
<title>Paper Prime</title>
<meta name="description" content="Monte bonecos incríveis de papel em 3D com mais de 3500 moldes"/>
<link rel="icon" href="https://paperprime.vercel.app/favicon.ico" type="image/x-icon" sizes="16x16"/>
<script src="https://cdn.tailwindcss.com"></script>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Permanent+Marker&family=Caveat:wght@400;500;600;700&family=Inter:wght@300;400;500;600;700;800;900&display=swap" rel="stylesheet">
<link rel="preconnect" href="https://i.ibb.co"/>
<script src="https://cdn.utmify.com.br/scripts/utms/latest.js" data-utmify-prevent-xcod-sck data-utmify-prevent-subids async defer></script>
{pixel_html}
{clarity_html}
<style>
  * {{ font-family: 'Inter', sans-serif; }}
  .font-marker {{ font-family: 'Permanent Marker', cursive !important; }}
  .font-handwritten {{ font-family: 'Caveat', cursive !important; }}
  html {{ scroll-behavior: smooth; }}
  .hero-bg {{ background: linear-gradient(135deg, #0a1628 0%, #0f2347 40%, #0d3b1a 100%); }}
  .green-section {{ background: linear-gradient(160deg, #0d2a0d 0%, #0f3a10 50%, #0d2a0d 100%); }}
  @keyframes float {{ 0%,100%{{transform:translateY(0)}} 50%{{transform:translateY(-10px)}} }}
  .float-anim {{ animation: float 3s ease-in-out infinite; }}
  @keyframes pulse-ring {{ 0%{{transform:scale(0.95);opacity:0.8}} 50%{{transform:scale(1.05);opacity:1}} 100%{{transform:scale(0.95);opacity:0.8}} }}
  .pulse {{ animation: pulse-ring 2s ease-in-out infinite; }}
  .faq-answer {{ transition: max-height 0.3s ease, padding 0.3s; }}
  .faq-answer.open {{ max-height: 500px !important; }}
  .faq-icon.open {{ transform: rotate(180deg); }}
  @media (max-width:640px) {{
    .banner-text-1 {{ font-size:11px !important; }}
    .banner-text-2 {{ font-size:9.5px !important; padding:2px 8px !important; }}
    .modal-box {{ max-width:95% !important; }}
    .modal-body {{ padding:20px 18px 16px !important; }}
    .modal-price {{ font-size:2rem !important; }}
  }}
</style>
{utm_html}
</head>
<body class="antialiased bg-white overflow-x-hidden">

<!-- TOP BANNER -->
<div style="background:linear-gradient(to right,#1d4ed8,#2563eb);color:#fff;text-align:center;padding:10px 16px;position:relative;z-index:50;">
  <div style="max-width:1200px;margin:0 auto;display:flex;flex-direction:row;align-items:center;justify-content:center;gap:10px;flex-wrap:wrap;">
    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" style="flex-shrink:0;opacity:0.9;"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>
    <span style="font-size:13px;font-weight:800;text-transform:uppercase;letter-spacing:0.07em;white-space:nowrap;">OPORTUNIDADE ÚNICA:</span>
    <span id="banner-date-text" style="background:rgba(255,255,255,0.18);padding:3px 14px;border-radius:5px;font-size:12px;font-weight:700;text-transform:uppercase;letter-spacing:0.06em;white-space:nowrap;"></span>
  </div>
</div>

<!-- HERO SECTION -->
<section class="hero-bg text-white relative overflow-hidden">
  <div class="absolute inset-0 opacity-10" style="background-image:url('data:image/svg+xml,<svg xmlns=%22http://www.w3.org/2000/svg%22 width=%2260%22 height=%2260%22><rect width=%2260%22 height=%2260%22 fill=%22none%22/><path d=%22M0 30h60M30 0v60%22 stroke=%22white%22 stroke-width=%220.5%22/></svg>');"></div>
  <div class="absolute top-0 left-0 w-64 h-64 bg-blue-500/10 rounded-full blur-3xl -translate-x-1/2 -translate-y-1/2"></div>
  <div class="absolute bottom-0 right-0 w-96 h-96 bg-green-500/10 rounded-full blur-3xl translate-x-1/3 translate-y-1/3"></div>
  <div class="max-w-6xl mx-auto px-6 py-16 md:py-24 flex flex-col md:flex-row items-center gap-12 md:gap-16 relative z-10">
    <div class="flex-1 text-center md:text-left">
      <div class="inline-flex items-center gap-2 bg-blue-500/20 border border-blue-400/30 rounded-full px-4 py-1.5 mb-6">
        <span class="w-2 h-2 bg-green-400 rounded-full pulse"></span>
        <span class="text-blue-200 text-xs font-semibold uppercase tracking-widest">Acceso Imediato</span>
      </div>
      <h1 class="font-marker text-4xl md:text-5xl lg:text-6xl leading-tight mb-6 text-white uppercase">
        Monte Bonecos<br>Incríveis de<br><span style="color:#38d9a9;">Papel em 3D</span>
      </h1>
      <p class="text-slate-300 text-lg md:text-xl font-medium max-w-lg mb-8 leading-relaxed">
        Acesso imediato a <strong class="text-white">+3.500 moldes</strong> de papercraft prontos para imprimir e montar — sem experiência necessária!
      </p>
      <div class="flex flex-col sm:flex-row gap-4 justify-center md:justify-start">
        <a href="https://www.ggcheckout.com/checkout/v5/Oy2bpEcoiZANY89cwzEs" class="font-marker text-xl md:text-2xl bg-[#1A93FA] text-white px-8 py-4 rounded-2xl uppercase tracking-wider shadow-[0_6px_0_#0066cc] hover:shadow-[0_3px_0_#0066cc] hover:translate-y-1 transition-all text-center border-2 border-black">
          QUERO MEUS MOLDES AGORA
        </a>
      </div>
      <div class="mt-6 flex items-center justify-center md:justify-start gap-3 text-slate-400 text-sm">
        <svg class="w-4 h-4 text-green-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>
        <span>Garantia de 7 dias — devolução total sem perguntas</span>
      </div>
    </div>
    <div class="flex-1 flex justify-center items-center">
      <div class="relative float-anim">
        <div class="absolute inset-0 bg-blue-400/20 rounded-3xl blur-2xl scale-110"></div>
        <img src="{papers[0]}" alt="Papercraft" class="relative w-full max-w-md rounded-2xl shadow-2xl border border-white/10" style="max-height:480px;object-fit:cover;">
      </div>
    </div>
  </div>
  <!-- Thumbnails strip -->
  <div class="border-t border-white/10 py-6 overflow-hidden">
    <div class="flex gap-3 px-6 overflow-x-auto pb-2 scrollbar-hide justify-start md:justify-center">
      {thumbnail_items}
    </div>
  </div>
</section>

<!-- POR QUE SECTION -->
<section class="bg-white py-16 md:py-20">
  <div class="max-w-5xl mx-auto px-6">
    <div class="text-center mb-12">
      <p class="text-blue-600 font-semibold text-sm uppercase tracking-widest mb-3">Nossa Metodologia</p>
      <h2 class="font-marker text-3xl md:text-4xl text-slate-900 uppercase leading-tight">Por que alguém de primeira hora consegue<br class="hidden md:block"> montar sem dificuldades?</h2>
    </div>
    <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
      <div class="text-center p-6 rounded-2xl bg-slate-50 border border-slate-100">
        <div class="w-16 h-16 bg-blue-100 rounded-2xl flex items-center justify-center mx-auto mb-4 text-3xl">🎯</div>
        <h3 class="font-marker text-xl text-slate-900 uppercase mb-3">Moldes Numerados</h3>
        <p class="text-slate-600 text-sm leading-relaxed">Cada parte tem número e letra de encaixe. Impossível errar a montagem.</p>
      </div>
      <div class="text-center p-6 rounded-2xl bg-slate-50 border border-slate-100">
        <div class="w-16 h-16 bg-green-100 rounded-2xl flex items-center justify-center mx-auto mb-4 text-3xl">📐</div>
        <h3 class="font-marker text-xl text-slate-900 uppercase mb-3">Linhas de Dobra</h3>
        <p class="text-slate-600 text-sm leading-relaxed">Linhas tracejadas indicam exatamente onde dobrar — resultado profissional garantido.</p>
      </div>
      <div class="text-center p-6 rounded-2xl bg-slate-50 border border-slate-100">
        <div class="w-16 h-16 bg-purple-100 rounded-2xl flex items-center justify-center mx-auto mb-4 text-3xl">🚀</div>
        <h3 class="font-marker text-xl text-slate-900 uppercase mb-3">Do Iniciante ao Pro</h3>
        <p class="text-slate-600 text-sm leading-relaxed">Modelos de todos os níveis — do simples ao impressionante em 3D gigante.</p>
      </div>
    </div>
  </div>
</section>

<!-- O QUE VOCÊ PODE CRIAR -->
<section class="bg-slate-50 py-16 md:py-20">
  <div class="max-w-6xl mx-auto px-6">
    <div class="text-center mb-12">
      <p class="text-blue-600 font-semibold text-sm uppercase tracking-widest mb-3">Catálogo Completo</p>
      <h2 class="font-marker text-3xl md:text-4xl text-slate-900 uppercase">O que você pode criar</h2>
      <p class="text-slate-600 mt-3 max-w-xl mx-auto">Mais de 3.500 moldes nas categorias mais pedidas. Novos adicionados mensalmente.</p>
    </div>
    <div class="grid grid-cols-3 sm:grid-cols-4 md:grid-cols-5 lg:grid-cols-6 gap-3">
      {gallery_items}
    </div>
  </div>
</section>

<!-- COMO SÃO OS MOLDES -->
<section class="bg-white py-16 md:py-20">
  <div class="max-w-5xl mx-auto px-6">
    <div class="text-center mb-12">
      <p class="text-blue-600 font-semibold text-sm uppercase tracking-widest mb-3">Pronto para Imprimir</p>
      <h2 class="font-marker text-3xl md:text-4xl text-slate-900 uppercase leading-tight">Pronto para você<br>imprimir como está</h2>
      <p class="text-slate-600 mt-4 max-w-2xl mx-auto text-base">Cada arquivo é um PDF otimizado. Imprima em qualquer impressora colorida, recorte, dobre e cole. Em minutos você tem um boneco incrível nas mãos.</p>
    </div>
    <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mt-8">
      <div class="flex flex-col items-center text-center gap-3 p-6 rounded-2xl border border-slate-100 bg-slate-50">
        <div class="w-12 h-12 bg-blue-500 text-white rounded-full flex items-center justify-center font-marker text-xl">1</div>
        <h3 class="font-semibold text-slate-900">Baixe o PDF</h3>
        <p class="text-slate-500 text-sm">Acesse a área de membros e baixe o modelo que quiser</p>
      </div>
      <div class="flex flex-col items-center text-center gap-3 p-6 rounded-2xl border border-slate-100 bg-slate-50">
        <div class="w-12 h-12 bg-blue-500 text-white rounded-full flex items-center justify-center font-marker text-xl">2</div>
        <h3 class="font-semibold text-slate-900">Imprima e Recorte</h3>
        <p class="text-slate-500 text-sm">Papel cartão 180–240g/m², tesoura e estilete são suficientes</p>
      </div>
      <div class="flex flex-col items-center text-center gap-3 p-6 rounded-2xl border border-slate-100 bg-slate-50">
        <div class="w-12 h-12 bg-blue-500 text-white rounded-full flex items-center justify-center font-marker text-xl">3</div>
        <h3 class="font-semibold text-slate-900">Monte e Exiba</h3>
        <p class="text-slate-500 text-sm">Siga os números e dobre pelas linhas. Resultado profissional!</p>
      </div>
    </div>
  </div>
</section>

<!-- PROVA SOCIAL -->
<section class="bg-slate-50 py-16 md:py-20">
  <div class="max-w-5xl mx-auto px-6">
    <div class="text-center mb-10">
      <h2 class="font-marker text-3xl md:text-4xl text-slate-900 uppercase">Já foi criado por nossos alunos</h2>
      <p class="text-slate-500 mt-3">Veja o que outros estão fazendo usando os nossos moldes</p>
    </div>
    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
      {prova_items}
    </div>
  </div>
</section>

<!-- MÓDULOS (GREEN SECTION) -->
<section class="green-section text-white py-16 md:py-24 relative overflow-hidden">
  <div class="absolute inset-0 opacity-5" style="background-image:url('data:image/svg+xml,<svg xmlns=%22http://www.w3.org/2000/svg%22 width=%2260%22 height=%2260%22><path d=%22M0 30h60M30 0v60%22 stroke=%22white%22 stroke-width=%220.5%22/></svg>');"></div>
  <div class="max-w-5xl mx-auto px-6 relative z-10">
    <div class="text-center mb-16">
      <span class="inline-block bg-yellow-400 text-black text-xs font-black uppercase tracking-widest px-4 py-1.5 rounded-full mb-4">VOCÊ VAI RECEBER</span>
      <h2 class="font-marker text-3xl md:text-5xl uppercase leading-tight mb-4">VEJA O QUE VOCÊ PODE<br>GANHAR AO ENTRAR AGORA</h2>
      <p class="text-white/70 text-base max-w-xl mx-auto">Tudo que você precisa para começar hoje mesmo e criar bonecos incríveis</p>
    </div>
    <div class="grid grid-cols-1 md:grid-cols-3 gap-8 mb-16">
      <div class="bg-white/10 backdrop-blur-sm border border-white/20 rounded-2xl overflow-hidden flex flex-col">
        <div class="aspect-video overflow-hidden"><img src="{modulos[0]}" alt="Módulo 01" class="w-full h-full object-cover hover:scale-105 transition-transform duration-500"></div>
        <div class="p-5 flex-1">
          <span class="text-xs font-bold text-green-400 uppercase tracking-widest">MÓDULO 01</span>
          <h3 class="font-marker text-xl mt-1 uppercase">Coleção Principal</h3>
          <p class="text-white/70 text-sm mt-2">Mais de 1.000 moldes das categorias mais populares premium</p>
        </div>
      </div>
      <div class="bg-white/10 backdrop-blur-sm border border-white/20 rounded-2xl overflow-hidden flex flex-col">
        <div class="aspect-video overflow-hidden"><img src="{modulos[1]}" alt="Módulo 02" class="w-full h-full object-cover hover:scale-105 transition-transform duration-500"></div>
        <div class="p-5 flex-1">
          <span class="text-xs font-bold text-blue-400 uppercase tracking-widest">MÓDULO 02</span>
          <h3 class="font-marker text-xl mt-1 uppercase">Coleção Avançada</h3>
          <p class="text-white/70 text-sm mt-2">Moldes 3D gigantes, lowpoly, detalhados com técnicas avançadas</p>
        </div>
      </div>
      <div class="bg-white/10 backdrop-blur-sm border border-white/20 rounded-2xl overflow-hidden flex flex-col">
        <div class="aspect-video overflow-hidden"><img src="{modulos[2]}" alt="Módulo 03" class="w-full h-full object-cover hover:scale-105 transition-transform duration-500"></div>
        <div class="p-5 flex-1">
          <span class="text-xs font-bold text-purple-400 uppercase tracking-widest">MÓDULO 03</span>
          <h3 class="font-marker text-xl mt-1 uppercase">Updates Mensais</h3>
          <p class="text-white/70 text-sm mt-2">Novos moldes toda semana. Acesso vitalício sem mensalidades</p>
        </div>
      </div>
    </div>
    <!-- BONUS KIT MESTRE -->
    <div class="bg-white/5 border-2 border-yellow-400/30 rounded-3xl p-8 md:p-10">
      <div class="text-center mb-8">
        <span class="inline-block bg-yellow-400 text-black text-xs font-black uppercase tracking-widest px-4 py-1 rounded-full mb-3">+ BÔNUS EXCLUSIVOS</span>
        <h3 class="font-marker text-2xl md:text-3xl uppercase text-white">Bônus que só o Kit Mestre possui</h3>
      </div>
      <div class="space-y-4">
        {bonus_cards}
      </div>
    </div>
  </div>
</section>

<!-- PRICING SECTION -->
<section class="bg-white py-16 md:py-24" id="comprar">
  <div class="max-w-5xl mx-auto px-6">
    <div class="text-center mb-12">
      <h2 class="font-marker text-3xl md:text-5xl text-slate-900 uppercase">Escolha Seu Kit</h2>
      <p class="text-slate-500 mt-3 text-base">Acesso imediato após o pagamento. Sem mensalidade.</p>
    </div>
    <div class="grid grid-cols-1 md:grid-cols-2 gap-8 max-w-4xl mx-auto items-start">
      <!-- KIT INICIANTE -->
      <div class="border-2 border-slate-200 rounded-3xl p-8 flex flex-col">
        <div class="mb-6">
          <span class="text-xs font-black uppercase tracking-widest text-slate-400">PLANO BÁSICO</span>
          <h3 class="font-marker text-2xl text-slate-900 uppercase mt-1">Kit Iniciante</h3>
        </div>
        <div class="mb-6">
          <span class="text-4xl font-black text-slate-900">R$ <span class="text-5xl">10</span><span class="text-2xl">,00</span></span>
          <p class="text-slate-400 text-sm mt-1">pagamento único</p>
        </div>
        <ul class="space-y-3 mb-8 text-sm text-slate-700 flex-grow">
          <li class="flex items-center gap-2"><span style="color:#00C347;font-weight:900;">✔</span> Acesso a 500 Moldes</li>
          <li class="flex items-center gap-2"><span style="color:#00C347;font-weight:900;">✔</span> Acesso Vitalício</li>
          <li class="flex items-center gap-2"><span style="color:#00C347;font-weight:900;">✔</span> Personagens</li>
          <li class="flex items-center gap-2"><span style="color:#00C347;font-weight:900;">✔</span> Animais</li>
          <li class="flex items-center gap-2"><span style="color:#00C347;font-weight:900;">✔</span> Objetos</li>
          <li class="flex items-center gap-2 text-slate-300"><span style="color:#cbd5e1;font-weight:900;">✘</span> Bônus Exclusivos</li>
          <li class="flex items-center gap-2 text-slate-300"><span style="color:#cbd5e1;font-weight:900;">✘</span> Área de Membros Premium</li>
          <li class="flex items-center gap-2 text-slate-300"><span style="color:#cbd5e1;font-weight:900;">✘</span> Suporte Prioritário</li>
        </ul>
        <a href="https://www.ggcheckout.com/checkout/v5/KT3V3LhJz6DttxgTybFl" onclick="openModal(event)" class="block w-full py-4 rounded-2xl border-2 border-slate-800 text-slate-800 font-marker text-lg uppercase text-center hover:bg-slate-50 transition-all">QUERO SÓ O BÁSICO</a>
        <div class="mt-4 flex items-center justify-center gap-2 text-slate-400 text-xs font-semibold uppercase tracking-wider">
          <svg class="w-4 h-4 text-green-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>
          Garantia de 7 dias total
        </div>
      </div>
      <!-- KIT MESTRE -->
      <div class="border-2 border-blue-500 rounded-3xl p-8 flex flex-col relative shadow-2xl shadow-blue-100 scale-[1.02]">
        <div class="absolute -top-4 left-1/2 -translate-x-1/2 bg-[#1A93FA] text-white text-xs font-black uppercase tracking-widest px-5 py-1.5 rounded-full shadow-lg">MAIS POPULAR</div>
        <div class="mb-6">
          <span class="text-xs font-black uppercase tracking-widest text-blue-500">MELHOR CUSTO-BENEFÍCIO</span>
          <h3 class="font-marker text-2xl text-slate-900 uppercase mt-1">Kit Mestre</h3>
        </div>
        <div class="mb-6 flex items-end gap-3">
          <div>
            <span class="text-slate-400 line-through text-sm font-semibold">R$ 67,90</span>
            <div class="text-4xl font-black text-slate-900">R$ <span class="text-5xl">24</span><span class="text-2xl">,90</span></div>
            <p class="text-slate-400 text-sm mt-1">pagamento único</p>
          </div>
          <span class="mb-2 inline-block bg-green-500 text-white text-xs font-black px-3 py-1 rounded-full">-63% OFF</span>
        </div>
        <ul class="space-y-3 mb-4 text-sm font-bold text-slate-900 flex-grow">
          <li class="flex items-center gap-2"><span style="color:#00C347;font-weight:900;">✔</span> Acesso a +3500 Moldes</li>
          <li class="flex items-center gap-2"><span style="color:#00C347;font-weight:900;">✔</span> Acesso Vitalício</li>
          <li class="flex items-center gap-2"><span style="color:#00C347;font-weight:900;">✔</span> Personagens</li>
          <li class="flex items-center gap-2"><span style="color:#00C347;font-weight:900;">✔</span> Plantas</li>
          <li class="flex items-center gap-2"><span style="color:#00C347;font-weight:900;">✔</span> Objetos</li>
          <li class="flex items-center gap-2"><span style="color:#00C347;font-weight:900;">✔</span> Diversos</li>
          <li class="flex items-center gap-2"><span style="color:#00C347;font-weight:900;">✔</span> Moldes Gigantes (3D)</li>
          <li class="flex items-center gap-2"><span style="color:#00C347;font-weight:900;">✔</span> Alfabeto Lowpoly</li>
          <li class="flex items-center gap-2"><span style="color:#00C347;font-weight:900;">✔</span> Castelos · Dragões · Geek</li>
          <li class="flex items-center gap-2"><span style="color:#00C347;font-weight:900;">✔</span> Espaço · Esportes · Mitologia</li>
          <!-- BONUS BLOCK -->
          <li class="pt-3 block">
            <div class="bg-yellow-50 border-2 border-dashed border-yellow-400 rounded-2xl p-4 relative mt-2" style="border-color:#FDC700!important;background:#FEFCE8!important;">
              <span class="absolute -top-3 left-1/2 -translate-x-1/2 bg-yellow-400 text-black px-4 py-0.5 rounded-lg text-xs font-black uppercase shadow-sm" style="background:#FDC700!important;">+ BÔNUS</span>
              <ul class="space-y-2 mt-1">
                <li class="flex items-center gap-2"><span class="text-lg">🎁</span> Zoológico de Papercraft</li>
                <li class="flex items-center gap-2"><span class="text-lg">🎁</span> Heróis</li>
                <li class="flex items-center gap-2"><span class="text-lg">🎁</span> Animes e Mangás</li>
                <li class="flex items-center gap-2"><span class="text-lg">🎁</span> Garagem de Carros</li>
                <li class="flex items-center gap-2"><span class="text-lg">🎁</span> Área de Membros Premium</li>
                <li class="flex items-center gap-2"><span class="text-lg">🎁</span> Suporte Prioritário</li>
                <li class="flex items-center gap-2"><span class="text-lg">🎁</span> Galeria da Comunidade</li>
              </ul>
            </div>
          </li>
        </ul>
        <a href="https://www.ggcheckout.com/checkout/v5/Oy2bpEcoiZANY89cwzEs" class="block w-full py-5 rounded-2xl bg-[#1A93FA] text-white font-marker text-2xl uppercase text-center shadow-[0_6px_0_#0066cc] hover:shadow-[0_3px_0_#0066cc] hover:translate-y-1 transition-all border-2 border-black mt-4" style="background-color:#1A93FA!important;">
          SIM! EU QUERO TUDO
        </a>
        <div class="mt-4 flex items-center justify-center gap-2 text-slate-500 text-xs font-semibold uppercase tracking-wider">
          <svg class="w-4 h-4 text-green-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>
          Garantia de 7 dias total
        </div>
      </div>
    </div>
  </div>
</section>

<!-- TRUST ICONS -->
<section class="bg-slate-50 py-12 border-t border-slate-100">
  <div class="max-w-5xl mx-auto px-6">
    <div class="grid grid-cols-1 md:grid-cols-3 gap-8 mb-16">
      <div class="flex flex-col items-center text-center group">
        <div class="w-16 h-16 rounded-full border border-slate-100 bg-white shadow-sm flex items-center justify-center mb-4">
          <svg xmlns="http://www.w3.org/2000/svg" class="w-7 h-7 text-slate-800" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/><path d="m9 12 2 2 4-4"/></svg>
        </div>
        <h3 class="text-slate-700 font-bold text-sm tracking-widest uppercase">Compra 100% Segura</h3>
      </div>
      <div class="flex flex-col items-center text-center group">
        <div class="w-16 h-16 rounded-full border border-slate-100 bg-white shadow-sm flex items-center justify-center mb-4">
          <svg xmlns="http://www.w3.org/2000/svg" class="w-7 h-7 text-slate-800" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" y1="15" x2="12" y2="3"/></svg>
        </div>
        <h3 class="text-slate-700 font-bold text-sm tracking-widest uppercase">Download Imediato</h3>
      </div>
      <div class="flex flex-col items-center text-center group">
        <div class="w-16 h-16 rounded-full border border-slate-100 bg-white shadow-sm flex items-center justify-center mb-4">
          <svg xmlns="http://www.w3.org/2000/svg" class="w-7 h-7 text-slate-800" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M14 9V5a3 3 0 0 0-3-3l-4 9v11h11.28a2 2 0 0 0 2-1.7l1.38-9a2 2 0 0 0-2-2.3zM7 22H4a2 2 0 0 1-2-2v-7a2 2 0 0 1 2-2h3"/></svg>
        </div>
        <h3 class="text-slate-700 font-bold text-sm tracking-widest uppercase">Garantia de Satisfação</h3>
      </div>
    </div>

    <!-- GARANTIA BOX -->
    <div class="mt-4 bg-white rounded-xl relative max-w-4xl mx-auto">
      <div class="relative bg-white border-2 border-dashed border-[#E2E8F0] rounded-sm p-8 md:p-12 shadow-[0_20px_50px_rgba(0,0,0,0.05)]">
        <div class="absolute -top-10 -right-4 md:-top-12 md:-right-8 z-20">
          <div class="bg-[#0188fa] text-white w-20 h-20 md:w-28 md:h-28 rounded-full flex flex-col items-center justify-center transform rotate-12 shadow-lg border-4 border-white">
            <span class="font-marker text-[10px] md:text-xs leading-none uppercase">Garantia</span>
            <span class="font-marker text-xl md:text-3xl leading-none my-0.5">7</span>
            <span class="font-marker text-[10px] md:text-xs leading-none uppercase">Dias</span>
          </div>
        </div>
        <div class="flex flex-col md:flex-row items-start gap-6 md:gap-10">
          <div class="flex-shrink-0">
            <div class="w-16 h-16 md:w-24 md:h-24 rounded-2xl bg-slate-50 border-2 border-dashed border-[#E2E8F0] flex items-center justify-center">
              <svg xmlns="http://www.w3.org/2000/svg" class="w-10 h-10 md:w-14 md:h-14 text-slate-800" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24"><path d="M20 13c0 5-3.5 7.5-7.66 8.95a1 1 0 0 1-.67-.01C7.5 20.5 4 18 4 13V6a1 1 0 0 1 1-1c2 0 4.5-1.2 6.24-2.72a1.17 1.17 0 0 1 1.52 0C14.51 3.81 17 5 19 5a1 1 0 0 1 1 1z"/><path d="m9 12 2 2 4-4"/></svg>
            </div>
          </div>
          <div class="flex-grow text-left">
            <h2 class="font-marker text-2xl md:text-3xl text-[#0F172A] mb-4 uppercase tracking-tight">RISCO ZERO: TESTE POR 7 DIAS</h2>
            <div class="space-y-4 text-[#475569] leading-relaxed">
              <p class="text-base md:text-lg font-medium">Temos tanta certeza que você vai amar os moldes que oferecemos uma garantia incondicional.</p>
              <p class="text-sm md:text-base">Se você não conseguir montar, não gostar dos modelos ou simplesmente mudar de ideia, nós devolvemos <span class="font-bold text-[#0F172A]">100% do seu dinheiro</span>. Sem perguntas, sem letras miúdas. Basta um e-mail.</p>
            </div>
            <div class="mt-8 flex flex-col md:flex-row md:items-center justify-between gap-4 border-t border-slate-100 pt-6">
              <span class="font-handwritten text-2xl md:text-3xl text-slate-400">Paper Prime Team</span>
              <span class="text-[10px] font-black uppercase tracking-[0.2em] text-slate-400 opacity-50">Authorized Signature</span>
            </div>
          </div>
        </div>
        <div class="absolute -bottom-3 left-1/2 -translate-x-1/2 w-48 h-2 bg-slate-100/50 blur-sm rounded-full"></div>
      </div>
      <div class="absolute -z-10 top-4 left-4 w-full h-full bg-slate-100/50 rounded-sm transform translate-x-2 translate-y-2"></div>
    </div>
  </div>
</section>

<!-- FAQ -->
<section class="bg-white py-16 md:py-20">
  <div class="max-w-3xl mx-auto px-6">
    <div class="text-center mb-10">
      <h2 class="font-marker text-3xl md:text-4xl text-slate-900 uppercase">Dúvidas?</h2>
      <p class="text-slate-500 mt-2">Perguntas mais frequentes</p>
    </div>
    <div class="bg-white border border-slate-200 rounded-2xl divide-y divide-slate-100 shadow-sm">
      {faq_html}
    </div>
  </div>
</section>

<!-- FOOTER -->
<footer class="bg-slate-900 text-white py-12">
  <div class="max-w-5xl mx-auto px-6 text-center">
    <div class="font-marker text-2xl text-white mb-2">Paper Prime</div>
    <p class="text-slate-400 text-sm mb-6">© 2024 Paper Prime. Todos os direitos reservados.</p>
    <div class="flex items-center justify-center gap-6 text-slate-400 text-xs">
      <a href="#" class="hover:text-white transition-colors">Termos de Uso</a>
      <span>·</span>
      <a href="#" class="hover:text-white transition-colors">Política de Privacidade</a>
      <span>·</span>
      <a href="https://api.whatsapp.com/send?phone=5519998292609&text=Ol%C3%A1%21%20Tenho%20interesse%20nos%20moldes%20de%20papercraft." class="hover:text-white transition-colors">Contato</a>
    </div>
  </div>
</footer>

{modal_content}

<!-- WhatsApp Floating Button -->
<a href="https://api.whatsapp.com/send?phone=5519998292609&text=Ol%C3%A1%21%20Tenho%20interesse%20nos%20moldes%20de%20papercraft." target="_blank" rel="noopener noreferrer" style="position:fixed;bottom:25px;right:25px;z-index:9999;width:55px;height:55px;display:block;" onmouseover="this.style.transform='scale(1.08)'" onmouseout="this.style.transform='scale(1)'">
  <img src="whatsapp.png" alt="WhatsApp" style="width:100%;height:100%;display:block;"/>
</a>

<script>
// Banner date
(function(){{
  var d=new Date();
  var m=['JANEIRO','FEVEREIRO','MARÇO','ABRIL','MAIO','JUNHO','JULHO','AGOSTO','SETEMBRO','OUTUBRO','NOVEMBRO','DEZEMBRO'];
  document.getElementById('banner-date-text').textContent='PROMOÇÃO VÁLIDA SOMENTE ATÉ HOJE, '+String(d.getDate()).padStart(2,'0')+' DE '+m[d.getMonth()]+' DE '+d.getFullYear();
}})();

// FAQ Toggle
function toggleFaq(btn) {{
  var answer = btn.nextElementSibling;
  var icon = btn.querySelector('.faq-icon');
  answer.classList.toggle('open');
  icon.classList.toggle('open');
}}

// MODAL
var timeLeft = 264;
var timerId = null;

function openModal(e) {{
  if(e) e.preventDefault();
  var modal = document.getElementById('discountModal');
  if(modal) {{ modal.style.display='flex'; startTimer(); }}
}}
function closeModal() {{
  var modal = document.getElementById('discountModal');
  if(modal) modal.style.display='none';
  if(timerId) {{ clearInterval(timerId); timerId=null; }}
}}
function startTimer() {{
  if(timerId) return;
  var el = document.getElementById('timer');
  timerId = setInterval(function(){{
    if(timeLeft<=0){{clearInterval(timerId);timerId=null;if(el)el.textContent='0:00';return;}}
    timeLeft--;
    var m=Math.floor(timeLeft/60), s=timeLeft%60;
    if(el) el.textContent=m+':'+(s<10?'0':'')+s;
  }},1000);
}}
</script>
</body></html>'''

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print(f"index.html written: {len(html)} chars, {html.count(chr(10))+1} lines")
