#!/usr/bin/env python3
"""Fix hardcoded paths for deployment"""
import os
import re

def fix_file(filepath):
    """Fix hardcoded paths in a file"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Replace hardcoded paths with relative paths
    original = content
    content = re.sub(r'', '', content)
    
    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✅ Fixed: {filepath}")
        return True
    return False

# Fix all Python files
fixed_count = 0
for root, dirs, files in os.walk('.'):
    # Skip hidden directories
    dirs[:] = [d for d in dirs if not d.startswith('.')]
    
    for file in files:
        if file.endswith('.py'):
            filepath = os.path.join(root, file)
            if fix_file(filepath):
                fixed_count += 1

print(f"\n🎉 Fixed {fixed_count} files")