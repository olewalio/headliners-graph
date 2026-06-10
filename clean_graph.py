#!/usr/bin/env python3
"""Clean the graph: remove blockchains, competitor relations, and orphans."""
import re, json

with open('index.html', 'r') as f:
    content = f.read()

# Nodes to remove (blockchains + irrelevant)
REMOVE_NODES = {'Bitcoin','Ethereum','Base','Ton','Sui','Solana','Near','Cz','Kraken','Coinbase'}

# Parse current NN and EE
nn_match = re.search(r'var NN=\[(.+?)\];', content, re.DOTALL)
ee_match = re.search(r'var EE=\[(.+?)\];', content, re.DOTALL)

nn_text = nn_match.group(1)
ee_text = ee_match.group(1)

# Parse nodes
nodes = {}
for m in re.finditer(r'\{([^}]+)\}', nn_text):
    nid = m.group(1).split(',')[0].split("'")[1]
    nodes[nid] = m.group(0)

# Parse edges
edges = []
for m in re.finditer(r'\{([^}]+)\}', ee_text):
    parts = {}
    for p in m.group(1).split(','):
        kv = p.strip().split(':')
        if len(kv) == 2:
            k = kv[0].strip()
            v = kv[1].strip().strip("'\"")
            parts[k] = v
    if 'f' in parts:
        edges.append(parts)

# 1. Remove competitor edges involving Headliners
filtered_edges = [e for e in edges if not (
    e.get('l') == 'competitor' and 
    (e.get('f') == 'Headliners' or e.get('t') == 'Headliners')
)]

print(f"Removed {len(edges) - len(filtered_edges)} competitor edges involving Headliners")

# 2. Remove edges involving removed nodes
filtered_edges2 = [e for e in filtered_edges if 
    e['f'] not in REMOVE_NODES and e['t'] not in REMOVE_NODES]

print(f"Removed {len(filtered_edges) - len(filtered_edges2)} edges involving removed nodes")

# 3. Find orphaned nodes (in NN but not in any edge)
active_nodes = set()
for e in filtered_edges2:
    active_nodes.add(e['f'])
    active_nodes.add(e['t'])

# Keep nodes that are in active edges OR are special (exchanges, tools, meanings)
# Also keep Headliners, Nikita_Anufriev, etc.
keep_set = set()
for nid, node_text in nodes.items():
    if nid in active_nodes or nid in REMOVE_NODES:
        continue  # will remove REMOVE_NODES later
    keep_set.add(nid)

# Remove removed nodes from NN
filtered_nodes = {nid: nt for nid, nt in nodes.items() if nid not in REMOVE_NODES}

# Check for orphaned nodes (non-removed but with no edges)
orphans = set(filtered_nodes.keys()) - active_nodes
# Keep certain orphaned special nodes
KEEP_ORPHANS = {'Binance','Bybit','OKX','BingX','Bitget','WhiteBIT','UTEX',
                'CoinW','Gate.io','Headliners','Nikita_Anufriev','HashHedge',
                '_meaning_partner','_meaning_competitor','_meaning_founder',
                '_meaning_subdomain','_meaning_mention','_meaning_account'}
for o in list(orphans):
    if o not in KEEP_ORPHANS:
        orphans.discard(o)
        print(f"Removing orphan: {o}")

filtered_nodes2 = {nid: nt for nid, nt in filtered_nodes.items() if nid not in orphans}

print(f"Nodes: {len(nodes)} → {len(filtered_nodes2)}")
print(f"Edges: {len(edges)} → {len(filtered_edges2)}")

# Regenerate NN text
new_nn = "var NN=[\n"
for nid, nt in sorted(filtered_nodes2.items(), key=lambda x: x[0]):
    new_nn += "  " + nt + ",\n"
new_nn = new_nn.rstrip(',\n') + "\n];"

# Regenerate EE text
new_ee = "var EE=[\n"
for e in filtered_edges2:
    new_ee += f"  {{f:'{e['f']}',t:'{e['t']}',l:'{e['l']}',d:'{e.get('d','')}'}},\n"
new_ee = new_ee.rstrip(',\n') + "\n];"

# Replace in content
content = content[:nn_match.start()] + new_nn + content[nn_match.end():]
content = content[:ee_match.start()] + new_ee + content[ee_match.end():]

with open('index.html', 'w') as f:
    f.write(content)

print("\nDone!")
