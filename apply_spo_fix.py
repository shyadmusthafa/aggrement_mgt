#!/usr/bin/env python
"""
Script to automatically fix SPO duplicate records issue
"""

import os
import re

def apply_spo_fix():
    """Apply the fix to dashboard/views.py"""
    
    views_file = 'dashboard/views.py'
    
    if not os.path.exists(views_file):
        print(f"Error: {views_file} not found!")
        return False
    
    # Read the file
    with open(views_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Pattern to find the SPORentRecord query
    patterns = [
        r'(\s+records\s*=\s*SPORentRecord\.objects\.select_related\([\'"]state[\'"],\s*[\'"]branch[\'"]\)\.all\(\))',
        r'(\s+records\s*=\s*SPORentRecord\.objects\.all\(\))',
        r'(\s+records\s*=\s*SPORentRecord\.objects\.select_related\([\'"]state[\'"],\s*[\'"]branch[\'"]\))',
    ]
    
    original_content = content
    fix_applied = False
    
    for pattern in patterns:
        match = re.search(pattern, content)
        if match:
            original_line = match.group(1)
            # Replace with fixed version
            fixed_line = original_line.replace('.all()', '.distinct(\'id\').order_by(\'id\')')
            if '.all()' not in original_line:
                fixed_line = original_line + '.distinct(\'id\').order_by(\'id\')'
            
            content = content.replace(original_line, fixed_line)
            fix_applied = True
            print(f"Found and fixed: {original_line.strip()}")
            print(f"Replaced with: {fixed_line.strip()}")
            break
    
    if not fix_applied:
        print("Could not find the SPORentRecord query. Please apply the fix manually.")
        print("\nLook for a line like:")
        print("records = SPORentRecord.objects.select_related('state', 'branch').all()")
        print("\nAnd replace it with:")
        print("records = SPORentRecord.objects.select_related('state', 'branch').distinct('id').order_by('id')")
        return False
    
    # Write the fixed content back
    with open(views_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"\n✅ Successfully applied SPO duplicate fix to {views_file}")
    print("Please restart your Django server for changes to take effect.")
    return True

def create_backup():
    """Create a backup of the views file"""
    views_file = 'dashboard/views.py'
    backup_file = 'dashboard/views_backup.py'
    
    if os.path.exists(views_file):
        import shutil
        shutil.copy2(views_file, backup_file)
        print(f"✅ Created backup: {backup_file}")

if __name__ == "__main__":
    print("SPO Duplicate Records Fix")
    print("=" * 40)
    
    # Create backup
    create_backup()
    
    # Apply fix
    if apply_spo_fix():
        print("\n🎉 Fix applied successfully!")
        print("\nNext steps:")
        print("1. Restart your Django server")
        print("2. Navigate to http://127.0.0.1:8000/dashboard/spo-rent/")
        print("3. Verify that each spo_id appears only once")
    else:
        print("\n❌ Fix could not be applied automatically.")
        print("Please follow the manual instructions in SPO_Duplicate_Fix_Instructions.md") 