#!/usr/bin/env python3
"""Add icdo4_code field to DIS-*.yaml files using safe YAML-aware insertion."""
import glob, os, re, yaml

base = 'C:/Users/805/cancer-autoresearch/knowledge_base/hosted/content/diseases'

edited, skipped = [], []

for fp in sorted(glob.glob(f'{base}/*.yaml')):
    fname = os.path.basename(fp)
    with open(fp, encoding='utf-8') as f:
        content = f.read()

    # Skip if already has icdo4_code
    if 'icdo4_code' in content:
        skipped.append(f'{fname} (already has icdo4_code)')
        continue

    # Parse to get the clean icd_o_3_morphology value
    try:
        data = yaml.safe_load(content)
    except Exception as e:
        skipped.append(f'{fname} (parse error: {e})')
        continue

    codes = data.get('codes', {})
    if not codes or 'icd_o_3_morphology' not in codes:
        skipped.append(f'{fname} (no icd_o_3_morphology)')
        continue

    icdo3 = str(codes['icd_o_3_morphology'])
    # icdo4 = same as icdo3 for our current dataset (no known changes for these 65 diseases)
    icdo4 = icdo3

    # Now do safe text insertion.
    # Find the line containing icd_o_3_morphology and insert icdo4_code after it.
    lines = content.splitlines(keepends=True)
    new_lines = []
    inserted = False
    for line in lines:
        new_lines.append(line)
        if 'icd_o_3_morphology' in line and not inserted:
            # Determine indentation: match leading whitespace of this line
            indent = re.match(r'^(\s*)', line).group(1)
            # For inline dict style (codes on same line), skip insertion
            # — detect by checking if line starts with 'codes:'
            if line.strip().startswith('codes:') and '{' in line:
                # Inline dict: we can't safely insert a new field
                # Skip this file — icdo4 same as icdo3, not critical
                skipped.append(f'{fname} (inline codes dict, manual edit needed)')
                new_lines = None
                break
            new_lines.append(f'{indent}icdo4_code: "{icdo4}"\n')
            inserted = True

    if new_lines is None:
        continue

    if inserted:
        new_content = ''.join(new_lines)
        # Verify it still parses
        try:
            yaml.safe_load(new_content)
        except Exception as e:
            skipped.append(f'{fname} (post-edit parse error: {e})')
            continue
        with open(fp, 'w', encoding='utf-8') as f:
            f.write(new_content)
        edited.append(f'{fname} -> {icdo4}')
    else:
        skipped.append(f'{fname} (pattern not found)')

print(f'Added icdo4_code: {len(edited)} files')
for f in edited: print(f'  OK  {f}')
print(f'Skipped: {len(skipped)}')
for f in skipped: print(f'  --  {f}')
