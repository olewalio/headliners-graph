#!/usr/bin/env python3
"""Pyramid graph v5 - 3 levels + click info panels."""
import json

W, H = 1000, 750

LEVELS = [
    ("1. 📺 Каналы, сообщества", 60),
    ("2. 🏗️ Инфраструктура", 300),
    ("3. 🛠️ Инструменты (биржи, пропы, обучение)", 530),
]

COLORS = {
    'main': '#00d4aa', 'competitor': '#c084fc',
    'infra': '#667799', 'exchange': '#f87171', 'tool': '#ffd93d',
}

# Channel details for click popup
CHANNEL_INFO = {
    'Headliners': {'positioning': '🎙 Подкасты, интервью, трейдинг, крипта', 'subs': 'YT 330K / TG 41.5K / VK 19.2K', 'monetization': 'Trade Lab, реф. ссылки CoinW/HashHedge/UTEX'},
    'Nikita_Anufriev': {'positioning': '👤 Основатель Хедлайнеров', 'subs': 'YT 330K', 'monetization': 'Хедлайнеры, HashHedge'},
    'Kirill_Evans': {'positioning': '📚 Обучение криптотрейдингу, обзоры', 'subs': 'Крупный крипто-блогер', 'monetization': 'Binance партнёр'},
    'Roman_Tomera': {'positioning': '🎙 Крипто-подкасты, интервью', 'subs': 'Крупный крипто-блогер', 'monetization': 'Binance, Bybit, OKX партнёр'},
    'PRO_BLOCKCHAIN': {'positioning': '📰 Новости, дайджесты, аналитика', 'subs': 'Крупный крипто-канал', 'monetization': 'Bybit, BingX партнёр'},
    'SLEZY_SATOSHI': {'positioning': '📊 Крипто-анализ, разборы', 'subs': 'Крупный крипто-канал', 'monetization': 'Bitget партнёр'},
    'RDeni': {'positioning': '📊 Крипто-аналитика, обзоры рынка', 'subs': 'Крупный аналитический канал', 'monetization': 'WhiteBIT партнёр'},
    'SerCrypto': {'positioning': '💹 Трейдинг, сигналы, обзоры', 'subs': 'Крупный сигнальный канал', 'monetization': 'Bybit (ядро сети, 307 упоминаний)'},
    'Crypto_Falcon': {'positioning': '💹 Трейдинг, сигналы', 'subs': 'Средний канал', 'monetization': 'Bybit партнёр'},
    'Cryptology': {'positioning': '📚 Обучение + 💹 сигналы', 'subs': 'Крупный канал', 'monetization': 'OKX (ядро сети, 148 упоминаний)'},
    'Prometheus': {'positioning': '📊 Аналитика, обзоры', 'subs': 'Средний канал', 'monetization': 'Binance партнёр'},
    'Дневник_активов': {'positioning': '📊 Управление активами, аналитика', 'subs': 'Средний канал', 'monetization': 'Binance, Bybit партнёр'},
}

# Level 0: Каналы
L0 = [
    ('Headliners', 'Хедлайнеры', 'main', 36),
    ('Nikita_Anufriev', 'Никита Ануфриев', 'main', 26),
    ('Kirill_Evans', 'Kirill Evans', 'competitor', 30),
    ('Roman_Tomera', 'Roman Tomera', 'competitor', 30),
    ('PRO_BLOCKCHAIN', 'PRO BLOCKCHAIN', 'competitor', 30),
    ('SLEZY_SATOSHI', 'SLEZY SATOSHI', 'competitor', 30),
    ('RDeni', 'RDeni', 'competitor', 30),
    ('SerCrypto', 'SerCrypto', 'competitor', 28),
    ('Crypto_Falcon', 'Crypto Falcon', 'competitor', 26),
    ('Cryptology', 'Cryptology', 'competitor', 26),
    ('Prometheus', 'Prometheus', 'competitor', 24),
    ('Дневник_активов', 'Дневник активов', 'competitor', 24),
]

# Level 1: Инфраструктура
L1 = [
    ('YouTube', 'YouTube (330K)', 'infra', 22),
    ('TG_nainspire', 'TG @nainspire', 'infra', 20),
    ('TG_traders_bot', 'TG @traders_bot', 'infra', 16),
    ('TG_headliners_bd', 'TG @headliners_bd', 'infra', 16),
    ('VK', 'VK (19.2K)', 'infra', 18),
    ('HashHedge', 'HashHedge', 'infra', 20),
]

# Level 2: Инструменты
L2 = [
    ('Binance', 'Binance', 'exchange', 30),
    ('Bybit', 'Bybit', 'exchange', 30),
    ('OKX', 'OKX', 'exchange', 30),
    ('CoinW', 'CoinW', 'exchange', 24),
    ('BingX', 'BingX', 'exchange', 24),
    ('UTEX', 'UTEX', 'exchange', 22),
    ('Bitget', 'Bitget', 'exchange', 22),
    ('WhiteBIT', 'WhiteBIT', 'exchange', 22),
    ('TradeLab', 'Trade Lab (обуч.)', 'tool', 20),
]

ALL = [(n, l, g, s, 0) for n, l, g, s in L0] + \
      [(n, l, g, s, 1) for n, l, g, s in L1] + \
      [(n, l, g, s, 2) for n, l, g, s in L2]

EDGES = [
    ('Nikita_Anufriev', 'Headliners'),
    ('Kirill_Evans', 'Headliners'), ('Roman_Tomera', 'Headliners'),
    ('PRO_BLOCKCHAIN', 'Headliners'), ('SLEZY_SATOSHI', 'Headliners'),
    ('RDeni', 'Headliners'), ('SerCrypto', 'Headliners'),
    ('Crypto_Falcon', 'Headliners'), ('Cryptology', 'Headliners'),
    ('Prometheus', 'Headliners'), ('Дневник_активов', 'Headliners'),
    ('Headliners', 'YouTube'), ('Headliners', 'TG_nainspire'),
    ('Headliners', 'TG_traders_bot'), ('Headliners', 'TG_headliners_bd'),
    ('Headliners', 'VK'), ('Headliners', 'HashHedge'),
    ('Bybit', 'SerCrypto'), ('Bybit', 'Crypto_Falcon'),
    ('Bybit', 'PRO_BLOCKCHAIN'), ('Bybit', 'Roman_Tomera'),
    ('Bybit', 'Дневник_активов'), ('OKX', 'Cryptology'),
    ('OKX', 'Roman_Tomera'), ('Binance', 'Prometheus'),
    ('Binance', 'Kirill_Evans'), ('Binance', 'Roman_Tomera'),
    ('Binance', 'Дневник_активов'), ('CoinW', 'Headliners'),
    ('UTEX', 'Headliners'), ('BingX', 'PRO_BLOCKCHAIN'),
    ('BingX', 'Headliners'), ('WhiteBIT', 'RDeni'), ('Bitget', 'SLEZY_SATOSHI'),
    ('Headliners', 'TradeLab'),
]

# Positions
pos = {}
for lvl_idx, (_, y_base) in enumerate(LEVELS):
    items = [(n, l, g, s) for (n, l, g, s, lv) in ALL if lv == lvl_idx]
    n = len(items)
    sp = min(140, int((W - 80) // max(n, 1)))
    sx = int((W - sp * (n - 1)) / 2) if n > 1 else W//2
    for i, (nid, lbl, grp, sz) in enumerate(items):
        x = sx + i * sp
        y = y_base
        pos[nid] = (x, y, sz, grp, lbl)

# Build SVG with click handlers
svg = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" style="width:100%;height:auto;background:#0f0f1a">'
svg += '<defs><style>text{font-family:sans-serif;fill:#fff;pointer-events:none}.node{cursor:pointer}.node:hover{opacity:0.8}</style></defs>'

for lvl_idx, (name, y_base) in enumerate(LEVELS):
    svg += f'<text x="15" y="{y_base+30}" fill="#00d4aa" font-size="12" font-weight="bold">{name}</text>'

# Edges
for src, tgt in EDGES:
    if src in pos and tgt in pos:
        x1, y1, s1, g1, _ = pos[src]; x2, y2, s2, g2, _ = pos[tgt]
        r1, r2 = s1/2, s2/2
        if y2 < y1: x1,y1,x2,y2 = x2,y2,x1,y1; r1,r2 = r2,r1
        color = '#444'
        if 'exchange' in (g1, g2): color = '#ffd93d80'
        if 'main' in (g1, g2): color = '#00d4aa40'
        svg += f'<line x1="{x1}" y1="{y1+r1+2}" x2="{x2}" y2="{y2-r2-2}" stroke="{color}" stroke-width="1.5"/>'

# Nodes with click handlers
node_defs = {}
for nid, (x, y, sz, grp, lbl) in pos.items():
    color = COLORS.get(grp, '#888')
    r = sz / 2
    el_id = f'node_{nid}'
    
    if grp == 'exchange':
        svg += f'<rect id="{el_id}" class="node" x="{x-r}" y="{y-r}" width="{sz}" height="{sz}" rx="4" fill="{color}" stroke="#fff" stroke-width="2"/>'
    elif grp == 'main':
        svg += f'<circle id="{el_id}" class="node" cx="{x}" cy="{y}" r="{r+3}" fill="{color}" stroke="#fff" stroke-width="2.5"/>'
    else:
        svg += f'<circle id="{el_id}" class="node" cx="{x}" cy="{y}" r="{r}" fill="{color}" stroke="#fff" stroke-width="1.5"/>'
    
    fs = max(8, min(sz*0.35, 11))
    display = lbl if len(lbl) <= 22 else lbl[:20]+'..'
    svg += f'<text x="{x}" y="{y+r+14}" text-anchor="middle" font-size="{fs}" fill="#ccc">{display}</text>'

svg += '</svg>'

# Generate info panel JS
info_js = '''<script>
function showInfo(id){
  var info = {
'''
for nid, data in CHANNEL_INFO.items():
    p = data['positioning'].replace("'", "\\'")
    s = data['subs'].replace("'", "\\'")
    m = data['monetization'].replace("'", "\\'")
    info_js += f"    '{nid}': {{p:'{p}',s:'{s}',m:'{m}'}},\n"

info_js += '''  };
  var el = document.getElementById('infoPanel');
  var titleEl = document.getElementById('infoTitle');
  if(info[id]) {
    titleEl.textContent = id.replace(/_/g,' ');
    document.getElementById('infoPositioning').textContent = info[id].p;
    document.getElementById('infoSubs').textContent = info[id].s;
    document.getElementById('infoMonetization').textContent = info[id].m;
    el.style.display = 'block';
  }
}
function closeInfo(){ document.getElementById('infoPanel').style.display = 'none'; }

// Add click handlers
document.addEventListener('DOMContentLoaded', function(){
  var nodes = document.querySelectorAll('[id^="node_"]');
  nodes.forEach(function(n){
    n.addEventListener('click', function(){
      var id = this.id.replace('node_','');
      showInfo(id);
    });
  });
  document.getElementById('infoClose').addEventListener('click', closeInfo);
});
</script>
'''

html = f'''<!DOCTYPE html><html lang="ru"><head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Хедлайнеры — Пирамида</title>
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
body{{background:#0f0f1a;color:#e0e0e0;font-family:-apple-system,sans-serif}}
.header{{background:#13131e;border-bottom:1px solid #2a2a40;padding:0.65rem 1.5rem;display:flex;justify-content:space-between;align-items:center}}
.header h1{{font-size:1.05rem;color:#00d4aa}}
.header .sub{{font-size:0.78rem;color:#9494aa}}
.legend{{display:flex;gap:1rem;padding:0.5rem 1.5rem;background:#13131e;border-bottom:1px solid #2a2a40;font-size:0.78rem;flex-wrap:wrap;color:#9494aa}}
.legend .item{{display:flex;align-items:center;gap:0.4rem}}
.legend .dot{{width:10px;height:10px;border-radius:50%;display:inline-block}}
.legend .rect{{width:10px;height:10px;border-radius:2px;display:inline-block}}
.svg-wrap{{padding:1rem;max-width:1100px;margin:0 auto}}
#infoPanel{{display:none;position:fixed;top:50%;left:50%;transform:translate(-50%,-50%);background:#1a1a2e;border:1px solid #6c5ce7;border-radius:12px;padding:1.5rem;z-index:100;max-width:400px;width:90%}}
#infoPanel h2{{color:#a29bfe;margin-bottom:0.5rem;font-size:1rem}}
#infoPanel .row{{margin:0.5rem 0;color:#ccc;font-size:0.85rem}}
#infoPanel .label{{color:#888;font-size:0.72rem;text-transform:uppercase}}
#infoClose{{margin-top:0.8rem;padding:0.4rem 1rem;background:#6c5ce7;color:#fff;border:none;border-radius:6px;cursor:pointer;font-size:0.82rem}}
#overlay{{display:none;position:fixed;inset:0;background:rgba(0,0,0,0.6);z-index:99}}
@media(max-width:700px){{.svg-wrap{{padding:0.3rem}}}}
</style></head><body>
<div class="header"><h1>🏛 Хедлайнеры — Пирамида</h1><div class="sub">{len(ALL)} сущностей · {len(EDGES)} связей · кликни на канал → детали</div></div>
<div class="legend">
<span class="item"><span class="dot" style="background:#00d4aa"></span> Каналы</span>
<span class="item"><span class="dot" style="background:#667799"></span> Инфраструктура</span>
<span class="item"><span class="rect" style="background:#f87171"></span> Инструменты/Биржи</span>
</div>
<div class="svg-wrap">{svg}</div>

<div id="overlay" onclick="closeInfo()"></div>
<div id="infoPanel">
  <h2 id="infoTitle"></h2>
  <div class="row"><div class="label">🎯 Позиционирование</div><div id="infoPositioning"></div></div>
  <div class="row"><div class="label">📊 Аудитория</div><div id="infoSubs"></div></div>
  <div class="row"><div class="label">💰 Монетизация</div><div id="infoMonetization"></div></div>
  <button id="infoClose">Закрыть</button>
</div>
{info_js}
</body></html>
'''

with open('/tmp/headliners-graph/index.html', 'w') as f:
    f.write(html)

print(f"{len(html.encode('utf-8'))} байт, {len(ALL)} узлов, {len(EDGES)} связей")
for lvl_idx, (name, _) in enumerate(LEVELS):
    cnt = len([1 for (_,_,_,_,l) in ALL if l == lvl_idx])
    print(f"  {name}: {cnt}")
