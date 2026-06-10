#!/usr/bin/env python3
"""Fix Mermaid node IDs: replace spaces with underscores in node IDs only.
    
Only matches lines that are node definitions (indent + ID["Label"]).
"""
import re, sys

def fix_file(path):
    with open(path, 'r') as f:
        lines = f.readlines()
    
    # Step 1: Find all node IDs with spaces from node definitions
    # Pattern: "    Some Name["Some Label"]"
    replacements = {}
    for line in lines:
        m = re.match(r'^    ([A-Za-zА-Яа-я0-9_ \-]+)\[".*"\]\s*$', line)
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
    
    # Step 2: Apply fixes line by line
    fixed = []
    for line in lines:
        # Only modify node definitions and references (indented lines and subgraph content)
        stripped = line.rstrip('\n')
        
        # Handle node definition: "    Old Name["Label"]"
        m = re.match(r'^    ([A-Za-zА-Яа-я0-9_ \-]+)(\[".*"\])\s*$', stripped)
        if m:
            node_id = m.group(1).strip()
            rest = m.group(2)
            if node_id in replacements:
                stripped = f'    {replacements[node_id]}{rest}'
                fixed.append(stripped + '\n')
                continue
        
        # Handle edge from: "    Old Name -->|label| Target"
        m = re.match(r'^    ([A-Za-zА-Яа-я0-9_ \-]+)(\s*\-\->\|.*)$', stripped)
        if m:
            node_id = m.group(1).strip()
            rest = m.group(2)
            if node_id in replacements:
                stripped = f'    {replacements[node_id]}{rest}'
                fixed.append(stripped + '\n')
                continue
        
        # Handle edge to: "    Src -->|label| Old Name"
        m = re.match(r'^(    [A-Za-zА-Яа-я0-9_ \-]+\s*\-\->\|[^|]*\|\s*)([A-Za-zА-Яа-я0-9_ \-]+)\s*$', stripped)
        if m:
            prefix = m.group(1)
            target_id = m.group(2).strip()
            if target_id in replacements:
                stripped = f'{prefix}{replacements[target_id]}'
                fixed.append(stripped + '\n')
                continue
        
        # Handle class statement: "    class Old Name className"
        m = re.match(r'^    (class\s+)([A-Za-zА-Яа-я0-9_ \-]+)(\s+\w+)\s*$', stripped)
        if m:
            prefix = m.group(1)
            node_id = m.group(2).strip()
            suffix = m.group(3)
            if node_id in replacements:
                stripped = f'    {prefix}{replacements[node_id]}{suffix}'
                fixed.append(stripped + '\n')
                continue
        
        fixed.append(stripped + '\n')
    
    with open(path, 'w') as f:
        f.writelines(fixed)
    
    print(f"Fixed {path}")

if __name__ == '__main__':
    for path in ['mermaid.txt', 'docs/mermaid.txt']:
        try:
            fix_file(path)
        except FileNotFoundError:
            print(f"Not found: {path}")
