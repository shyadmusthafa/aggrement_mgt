#!/usr/bin/env python
"""
Script to check syntax error in dashboard/views.py
"""

import ast
import sys

try:
    with open('dashboard/views.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Try to parse the file
    ast.parse(content)
    print("✅ Syntax is correct!")
    
except SyntaxError as e:
    print(f"❌ Syntax Error at line {e.lineno}: {e.text}")
    print(f"Error: {e.msg}")
    
    # Show the problematic lines
    lines = content.split('\n')
    start = max(0, e.lineno - 3)
    end = min(len(lines), e.lineno + 2)
    
    print(f"\nContext around line {e.lineno}:")
    for i in range(start, end):
        marker = ">>> " if i == e.lineno - 1 else "    "
        print(f"{marker}{i+1:4d}: {lines[i]}")
        
except Exception as e:
    print(f"❌ Error: {e}") 