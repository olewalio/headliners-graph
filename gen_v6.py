#!/usr/bin/env python3
"""Pyramid graph v6 - comprehensive entities + tools, 3 levels with click info."""
import re, json

W, H = 1200, 850

LEVELS = [
    ("", 60),  # Level 0: Каналы (no label)
    ("", 300),  # Level 1: Инфраструктура
    ("", 550),  # Level 2: Инструменты
]

COLORS = {
    'main':'#00d4aa','competitor':'#c084fc',
    'infra':'#667799','tool':'#ffd93d','exchange':'#f87171'
}

# Level 0: КАНАЛЫ (Headliners + all competitors)
L0 = [
    # Main
    ('Headliners','Хедлайнеры','main',38),
    ('Nikita_Anufriev','Никита Ануфриев','main',26),
    # Major competitors (size 30)
    ('Kirill_Evans','Kirill Evans','competitor',30),
    ('Roman_Tomera','Roman Tomera','competitor',30),
    ('PRO_BLOCKCHAIN','PRO BLOCKCHAIN','competitor',30),
    ('SLEZY_SATOSHI','SLEZY SATOSHI','competitor',30),
    ('RDeni','RDeni','competitor',30),
    # Medium competitors (size 26)
    ('SerCrypto','SerCrypto','competitor',26),
    ('Crypto_Falcon','Crypto Falcon','competitor',26),
    ('Cryptology','Cryptology','competitor',26),
    ('DOUBLETOP','DOUBLETOP','competitor',26),
    ('ForkLog','ForkLog','competitor',26),
    ('Wyckoff_Company','Wyckoff Company','competitor',26),
    ('Gerchik_Trading','Gerchik Trading','competitor',26),
    # Small competitors (size 22)
    ('Prometheus','Prometheus','competitor',22),
    ('Дневник_активов','Дневник активов','competitor',22),
    ('CryptoFateev','CryptoFateev','competitor',22),
    ('CryptoInside','CryptoInside','competitor',22),
    ('Cryptology_Edu','Cryptology Edu','competitor',22),
    ('CRYPTUS_MEDIA','CRYPTUS MEDIA','competitor',22),
    ('CRYPTOR_BLOG','CRYPTOR BLOG','competitor',22),
    ('Mamkin_Trader','Mamkin Trader','competitor',22),
    ('Bondar_Scalp','Bondar Scalp','competitor',22),
    ('Tomas_Kralov','Tomas Kralov','competitor',22),
    ('Drazor','Drazor','competitor',22),
    ('INSTARDING','INSTARDING','competitor',22),
]

# Level 1: ИНФРАСТРУКТУРА (Telegram, YT, bots, subdomains)
L1 = [
    # YouTube
    ('YT_Headliners','📺 YouTube 330K','infra',22),
    ('YT_KirillEvans','📺 YT Kirill Evans','infra',20),
    ('YT_RomanTomera','📺 YT Roman Tomera','infra',20),
    ('YT_PROBlockchain','📺 YT PRO BLOCKCHAIN','infra',18),
    # Main Telegram
    ('TG_nainspire','💬 @nainspire 41.5K','infra',20),
    ('TG_headliners_bd','💬 @headliners_bd','infra',16),
    ('TG_traders_bot','🤖 @traders_bot','infra',16),
    ('TG_Evans','💬 @Evans_Crypto_TG','infra',16),
    ('TG_CrypTomera','💬 @CrypTomera_TG','infra',16),
    ('TG_SleziSato','💬 @SleziSatoshi_TG','infra',16),
    ('TG_Rostik','💬 @crypto_rostik_TG','infra',14),
    # Bots
    ('bot_MicronCrypto','🤖 MicronCryptoBot','infra',14),
    ('bot_ProBlock','🤖 Pro_Block_Bot','infra',14),
    ('bot_XXXHunters','🤖 XXXHunters_bot','infra',14),
    # Other
    ('CoinW_TG','📦 CoinW Telegram','infra',14),
    ('nainspire_TG','📦 nainspire TG','infra',14),
    ('headIinersadmin','📦 headIinersadmin','infra',12),
    ('cryptocommunity','🌐 cryptocommunity.ai','infra',14),
    ('kirillevans_com','🌐 kirillevans.com','infra',14),
    ('dust_link','🔗 dust.link','infra',12),
    ('headlinerslinks','🔗 headlinerslinks.com','infra',12),
    ('VK','📱 VK 19.2K','infra',18),
]

# Level 2: ИНСТРУМЕНТЫ (exchanges, props, trading)
L2 = [
    # Exchanges (size 30-22)
    ('Binance','Binance','exchange',30),
    ('Bybit','Bybit','exchange',30),
    ('OKX','OKX','exchange',28),
    ('CoinW','CoinW','exchange',24),
    ('BingX','BingX','exchange',24),
    ('Bitget','Bitget','exchange',24),
    ('WhiteBIT','WhiteBIT','exchange',24),
    ('UTEX','UTEX','exchange',22),
    ('Gate_io','Gate.io','exchange',22),
    # Prop firms & Tools
    ('HashHedge','🔧 HashHedge (проп)','tool',22),
    ('TradeLab','📚 Trade Lab (обуч.)','tool',20),
    ('AltcoinSignals','💹 Altcoin Signals','tool',18),
    ('CryptoSignals','💹 Crypto Signals','tool',18),
    ('CryptoSignalHub','💹 CryptoSignal Hub','tool',18),
    ('Crypto_Scalp','📊 Crypto Scalp','tool',16),
    ('ProBoy','💹 ProBoy Signals','tool',16),
    ('BondarCScalp','📊 Bondar CScalp','tool',16),
    ('SkalpingDIGAHKA','⚡ Скальпинг DIGAHKA','tool',16),
    ('TAIP_Trade','💹 TAIP Trade','tool',16),
    ('Peersynth','💹 Peersynth Trader','tool',16),
]

ALL = [(n,l,g,s,0) for n,l,g,s in L0] + \
      [(n,l,g,s,1) for n,l,g,s in L1] + \
      [(n,l,g,s,2) for n,l,g,s in L2]

# Info for ALL nodes
INFO = {}
def add_info(nid, p, s, m):
    INFO[nid] = {'p': p, 's': s, 'm': m}

for n,l,g,s in L0:
    add_info(n, f'🎙 {l}', 'Канал', 'Партнёрства')
for n,l,g,s in L1:
    add_info(n, f'📡 {l}', 'Инфраструктура', '')
for n,l,g,s in L2:
    t = 'Биржа' if g=='exchange' else 'Инструмент'
    add_info(n, f'🏛 {l}', t, '')

# Override specific info
add_info('Headliners','🎙 Подкасты, интервью, трейдинг','YT 330K / TG 41.5K / VK 19.2K','Trade Lab, CoinW/HashHedge/UTEX')
add_info('Nikita_Anufriev','👤 Основатель Хедлайнеров','YT 330K','Хедлайнеры, HashHedge')
add_info('Kirill_Evans','📚 Обучение криптотрейдингу','Крупный блогер','Binance партнёр')
add_info('Roman_Tomera','🎙 Подкасты, интервью','Крупный блогер','Binance/Bybit/OKX партнёр')
add_info('PRO_BLOCKCHAIN','📰 Новости, дайджесты','Крупный канал','Bybit/BingX партнёр')
add_info('SerCrypto','💹 Трейдинг, сигналы','Крупный сигнальный канал','Bybit (307 упоминаний)')
add_info('Cryptology','📚 Обучение + 💹 сигналы','Крупный канал','OKX (148 упоминаний)')
add_info('Binance','🏛 Крупнейшая криптобиржа','Глобальная','Реф. программы, +50 упоминаний')
add_info('Bybit','🏛 Биржа #1 по партнёрствам','Глобальная','339 упоминаний в каналах')
add_info('OKX','🏛 Биржа, партнёр Cryptology','Глобальная','156 упоминаний')
add_info('HashHedge','🔧 Проп-фирма, партнёр Headliners','Активная','Совместные продукты')

# Edges
EDGES = [
    # === FOUNDER ===
    ('Nikita_Anufriev','Headliners'),
    
    # === CHANNELS -> INFRASTRUCTURE ===
    ('Headliners','YT_Headliners'),('Headliners','TG_nainspire'),
    ('Headliners','TG_headliners_bd'),('Headliners','TG_traders_bot'),
    ('Headliners','VK'),('Headliners','headlinerslinks'),
    
    ('Kirill_Evans','YT_KirillEvans'),('Kirill_Evans','TG_Evans'),
    ('Kirill_Evans','kirillevans_com'),('Kirill_Evans','dust_link'),
    ('Kirill_Evans','cryptocommunity'),('Kirill_Evans','bot_MicronCrypto'),
    
    ('Roman_Tomera','YT_RomanTomera'),('Roman_Tomera','TG_CrypTomera'),
    ('PRO_BLOCKCHAIN','YT_PROBlockchain'),('PRO_BLOCKCHAIN','bot_ProBlock'),
    ('PRO_BLOCKCHAIN','bot_XXXHunters'),
    ('SLEZY_SATOSHI','TG_SleziSato'),
    ('RDeni','TG_Rostik'),
    
    # === CHANNELS -> EXCHANGE PARTNERS ===
    # Bybit network (marketing analysis)
    ('Bybit','SerCrypto'),('Bybit','Crypto_Falcon'),
    ('Bybit','PRO_BLOCKCHAIN'),('Bybit','Roman_Tomera'),
    ('Bybit','Дневник_активов'),('Bybit','Gerchik_Trading'),
    
    # OKX network
    ('OKX','Cryptology'),('OKX','Roman_Tomera'),
    ('OKX','Cryptology_Edu'),
    
    # Binance network
    ('Binance','Kirill_Evans'),('Binance','Roman_Tomera'),
    ('Binance','Prometheus'),('Binance','Дневник_активов'),
    ('Binance','CryptoFateev'),('Binance','CryptoInside'),
    ('Binance','DOUBLETOP'),
    
    # Exchange partnerships
    ('CoinW','Headliners'),
    ('BingX','Headliners'),('BingX','PRO_BLOCKCHAIN'),
    ('UTEX','Headliners'),
    ('Bitget','SLEZY_SATOSHI'),
    ('WhiteBIT','RDeni'),
    ('Gate_io','PRO_BLOCKCHAIN'),('Gate_io','Cryptology'),
    
    # === EXCHANGES -> TOOLS ===
    ('Binance','HashHedge'),
    ('CoinW','TradeLab'),
    
    # === TOOLS -> CHANNELS ===
    ('HashHedge','Headliners'),
    ('TradeLab','Headliners'),
    ('AltcoinSignals','Kirill_Evans'),
    ('CryptoSignals','SerCrypto'),
    ('CryptoSignalHub','SerCrypto'),
    ('Crypto_Scalp','SerCrypto'),
    ('ProBoy','Crypto_Falcon'),
    ('BondarCScalp','Crypto_Falcon'),
    ('SkalpingDIGAHKA','SerCrypto'),
    ('TAIP_Trade','Roman_Tomera'),
    ('Peersynth','Roman_Tomera'),
]

# Positions
pos = {}
for lvl_idx, (_, y_base) in enumerate(LEVELS):
    items = [(n,l,g,s) for (n,l,g,s,lv) in ALL if lv == lvl_idx]
    n = len(items)
    sp = min(120, int((W - 60) // max(n, 1)))
    sx = int((W - sp * (n - 1)) / 2) if n > 1 else W//2
    for i, (nid,lbl,grp,sz) in enumerate(items):
        x = sx + i * sp
        y = y_base
        pos[nid] = (x, y, sz, grp, lbl)

# SVG
svg = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" style="width:100%;height:auto;background:#0f0f1a"><defs><style>text{{font-family:sans-serif;fill:#fff;pointer-events:none}}.node{{cursor:pointer}}.node:hover{{opacity:0.8}}</style></defs>'

for src, tgt in EDGES:
    if src in pos and tgt in pos:
        x1,y1,s1,g1,_ = pos[src]; x2,y2,s2,g2,_ = pos[tgt]
        r1,r2 = s1/2, s2/2
        if y2 < y1: x1,y1,x2,y2 = x2,y2,x1,y1; r1,r2 = r2,r1
        color = '#444'
        if 'exchange' in (g1,g2): color = '#ffd93d80'
        if 'main' in (g1,g2): color = '#00d4aa40'
        svg += f'<line x1="{x1}" y1="{y1+r1+2}" x2="{x2}" y2="{y2-r2-2}" stroke="{color}" stroke-width="1.2"/>'

for nid, (x,y,sz,grp,lbl) in pos.items():
    color = COLORS.get(grp, '#888'); r = sz/2
    eid = f'id="n_{nid}" class="node" onclick="showInfo(\'{nid}\')"'
    if grp == 'exchange':
        svg += f'<rect {eid} x="{x-r}" y="{y-r}" width="{sz}" height="{sz}" rx="4" fill="{color}" stroke="#fff" stroke-width="2"/>'
    elif grp == 'main':
        svg += f'<circle {eid} cx="{x}" cy="{y}" r="{r+2}" fill="{color}" stroke="#fff" stroke-width="2.5"/>'
    else:
        svg += f'<circle {eid} cx="{x}" cy="{y}" r="{r}" fill="{color}" stroke="#fff" stroke-width="1.5"/>'
    fs = max(7, min(sz*.35, 11))
    display = lbl if len(lbl) <= 22 else lbl[:20]+'..'
    svg += f'<text x="{x}" y="{y+r+14}" text-anchor="middle" font-size="{fs}" fill="#ccc">{display}</text>'
svg += '</svg>'

# JS info
info_js = '<script>\nvar INFO=' + json.dumps(INFO, ensure_ascii=False) + ';\n'
info_js += '''function showInfo(id){
  var d = INFO[id];
  if(!d) return;
  document.getElementById('infoTitle').textContent = id.replace(/_/g,' ');
  document.getElementById('infoPositioning').textContent = d.p;
  document.getElementById('infoSubs').textContent = d.s;
  document.getElementById('infoMonetization').textContent = d.m;
  document.getElementById('overlay').style.display='block';
  document.getElementById('infoPanel').style.display='block';
}
function closeInfo(){document.getElementById('overlay').style.display='none';document.getElementById('infoPanel').style.display='none';}
</script>'''

html = f'''<!DOCTYPE html><html lang="ru"><head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Хедлайнеры — Пирамида</title>
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
body{{background:#0f0f1a;color:#e0e0e0;font-family:-apple-system,sans-serif}}
.header{{background:#13131e;border-bottom:1px solid #2a2a40;padding:0.65rem 1.5rem;display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:0.5rem}}
.header h1{{font-size:1.05rem;color:#00d4aa}}
.header .sub{{font-size:0.78rem;color:#9494aa}}
.legend{{display:flex;gap:1rem;padding:0.3rem 1.5rem;background:#13131e;border-bottom:1px solid #2a2a40;font-size:0.75rem;flex-wrap:wrap;color:#9494aa}}
.legend .item{{display:flex;align-items:center;gap:0.3rem}}
.legend .dot{{width:10px;height:10px;border-radius:50%;display:inline-block}}
.legend .rect{{width:10px;height:10px;border-radius:2px;display:inline-block}}
.svg-wrap{{padding:0.5rem;max-width:1200px;margin:0 auto}}
#infoPanel{{display:none;position:fixed;top:50%;left:50%;transform:translate(-50%,-50%);background:#1a1a2e;border:1px solid #6c5ce7;border-radius:12px;padding:1.5rem;z-index:100;max-width:400px;width:90%}}
#infoPanel h2{{color:#a29bfe;margin-bottom:0.5rem;font-size:1rem}}
#infoPanel .row{{margin:0.3rem 0;color:#ccc;font-size:0.82rem}}
#infoPanel .label{{color:#888;font-size:0.7rem;text-transform:uppercase}}
#infoClose{{margin-top:0.6rem;padding:0.3rem 1rem;background:#6c5ce7;color:#fff;border:none;border-radius:6px;cursor:pointer;font-size:0.8rem}}
#overlay{{display:none;position:fixed;inset:0;background:rgba(0,0,0,0.6);z-index:99}}
</style></head><body>
<div class="header"><h1>🏛 Хедлайнеры — Пирамида</h1><div class="sub">{len(ALL)} сущностей · {len(EDGES)} связей · кликни на любой узел</div></div>
<div class="legend">
<span class="item"><span class="dot" style="background:#00d4aa"></span> Каналы</span>
<span class="item"><span class="dot" style="background:#667799"></span> Инфраструктура</span>
<span class="item"><span class="rect" style="background:#f87171"></span> Инструменты</span>
</div>
<div class="svg-wrap">{svg}</div>
<div id="overlay" onclick="closeInfo()"></div>
<div id="infoPanel">
  <h2 id="infoTitle"></h2>
  <div class="row"><div class="label">🎯 Позиционирование</div><div id="infoPositioning"></div></div>
  <div class="row"><div class="label">📊 Аудитория</div><div id="infoSubs"></div></div>
  <div class="row"><div class="label">💰 Монетизация</div><div id="infoMonetization"></div></div>
  <button id="infoClose" onclick="closeInfo()">Закрыть</button>
</div>
{info_js}
</body></html>
'''

with open('/tmp/headliners-graph/index.html', 'w') as f:
    f.write(html)

l0 = len(L0); l1 = len(L1); l2 = len(L2)
print(f"{len(html.encode('utf-8'))} байт, {l0+l1+l2} узлов, {len(EDGES)} связей")
print(f"  Каналы: {l0}")
print(f"  Инфраструктура: {l1}")
print(f"  Инструменты: {l2}")
