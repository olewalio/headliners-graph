#!/usr/bin/env python3
"""Fix all Mermaid node IDs with spaces - handles any char in node IDs."""
import re

def fix_file(path):
    with open(path, 'r') as f:
        content = f.read()
    
    # Step 1: Build replacement map from node definitions
    # Match: "    Some Node Name["Any Label"]"
    replacements = {}
    for m in re.finditer(r'^    ([^\[]+)\[".*"\]', content, re.MULTILINE):
        node_id = m.group(1).strip()
        if ' ' in node_id:
            new_id = node_id.replace(' ', '_')
            replacements[node_id] = new_id
            print(f"  '{node_id}' -> '{new_id}'")
    
    print(f"Found {len(replacements)} multi-word node IDs")
    
    if not replacements:
        print("Nothing to fix!")
        return
    
    # Step 2: Build a sorted list (longest first) to avoid partial replacements
    old_ids = sorted(replacements.keys(), key=len, reverse=True)
    
    # Step 3: Apply replacements line by line
    lines = content.split('\n')
    fixed_lines = []
    changed = 0
    
    for line in lines:
        stripped = line.rstrip('\n')
        
        # Only process indented lines (graph content, not headers)
        if not stripped.startswith('    '):
            fixed_lines.append(stripped)
            continue
        
        # For each old ID, try to replace it inline
        new_line = stripped
        for old_id in old_ids:
            new_id = replacements[old_id]
            if old_id in new_line:
                # Be careful: only replace ID positions, not inside label text
                # Node definition: "    Old Name["..."]" -> "   New_Name["..."]"
                new_line = re.sub(
                    r'^    ' + re.escape(old_id) + r'(\[".*"\])',
                    f'    {new_id}\\1',
                    new_line
                )
                # After arrow: "    Src -->|label| Old Name"
                new_line = re.sub(
                    r'(\-\->\|[^|]*\|\s*)' + re.escape(old_id) + r'\s*$',
                    f'\\1{new_id}',
                    new_line
                )
                # In class: "    class Old Name className"
                new_line = re.sub(
                    r'(^    class\s+)' + re.escape(old_id) + r'(\s+\w+\s*$)',
                    f'\\1{new_id}\\2',
                    new_line
                )
                # Before arrow: "    Old Name -->|..."
                new_line = re.sub(
                    r'^    ' + re.escape(old_id) + r'(\s*\-\->)',
                    f'    {new_id}\\1',
                    new_line
                )
        
        if new_line != stripped:
            changed += 1
        fixed_lines.append(new_line)
    
    # Write back
    result = '\n'.join(fixed_lines)
    with open(path, 'w') as f:
        f.write(result)
    
    # Step 4: Verify - check for remaining spaces in node definitions
    remaining = 0
    for m in re.finditer(r'^    ([^\[]+)\[".*"\]', result, re.MULTILINE):
        node_id = m.group(1).strip()
        if ' ' in node_id:
            print(f"  REMAINING: {node_id}")
            remaining += 1
    
    print(f"Fixed {path}: {changed} lines changed, {remaining} remaining broken IDs")

if __name__ == '__main__':
    for path in ['mermaid.txt', 'docs/mermaid.txt']:
        try:
            print(f"\n=== {path} ===")
            fix_file(path)
        except FileNotFoundError:
            print(f"Not found: {path}")
