#!/usr/bin/env python3
"""Fix remaining Mermaid node IDs with spaces - handle dots in node names too."""
import re

def fix_file(path):
    with open(path, 'r') as f:
        lines = f.readlines()
    
    # Find node IDs with spaces
    replacements = {}
    for line in lines:
        m = re.match(r'^    ([A-Za-zА-Яа-я0-9_. \-]+)\[".*"\]\s*$', line)
        if m:
            node_id = m.group(1).strip()
            if ' ' in node_id:
                replacements[node_id] = node_id.replace(' ', '_')
    
    print(f"Found {len(replacements)} multi-word node IDs:")
    for old, new in sorted(replacements.items()):
        print(f"  '{old}' -> '{new}'")
    
    if not replacements:
        print("Nothing to fix!")
        return
    
    # Character class matching any node ID char (incl. dots, underscores, Cyrillic)
    NODE_CHARS = r'[A-Za-zА-Яа-я0-9_.\-\u0400-\u04FF]+'
    
    fixed = []
    for line in lines:
        stripped = line.rstrip('\n')
        orig = stripped
        
        # 1. Node definition: "    Old Name["Label"]"
        m = re.match(r'^(    )(' + NODE_CHARS + r')(\[".*"\])\s*$', stripped)
        if m:
            indent = m.group(1)
            node_id = m.group(2)
            rest = m.group(3)
            if node_id in replacements:
                stripped = f'{indent}{replacements[node_id]}{rest}'
                fixed.append(stripped + '\n')
                continue
        
        # 2. Edge from + to in one line: "    Src -->|label| Tgt"
        m = re.match(
            r'^(    )(' + NODE_CHARS + r')(\s*\-\->\|[^|]*\|\s*)(' + NODE_CHARS + r')\s*$',
            stripped
        )
        if m:
            indent = m.group(1)
            src = m.group(2)
            arrow = m.group(3)
            tgt = m.group(4)
            if src in replacements:
                src = replacements[src]
            if tgt in replacements:
                tgt = replacements[tgt]
            stripped = f'{indent}{src}{arrow}{tgt}'
            fixed.append(stripped + '\n')
            continue
        
        # 3. Class statement: "    class NodeID className"
        m = re.match(r'^(    class\s+)(' + NODE_CHARS + r')(\s+\w+)\s*$', stripped)
        if m:
            prefix = m.group(1)
            node_id = m.group(2)
            suffix = m.group(3)
            if node_id in replacements:
                stripped = f'{prefix}{replacements[node_id]}{suffix}'
                fixed.append(stripped + '\n')
                continue
        
        fixed.append(stripped + '\n')
    
    with open(path, 'w') as f:
        f.writelines(fixed)
    
    # Check for remaining issues
    remaining = 0
    for line in fixed:
        m = re.match(r'^    (' + NODE_CHARS + r')(\[".*"\])\s*$', line)
        if m and ' ' in m.group(1):
            print(f"  STILL BROKEN: {m.group(1)}")
            remaining += 1
    
    print(f"Fixed {path} (remaining broken: {remaining})")

if __name__ == '__main__':
    for path in ['mermaid.txt', 'docs/mermaid.txt']:
        try:
            fix_file(path)
        except FileNotFoundError:
            print(f"Not found: {path}")
