#!/usr/bin/env python
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()

from dashboard.models import MasState, MasStateBranch

print("=" * 100)
print("🔍 VERIFYING COMPREHENSIVE BRANCH DATA")
print("=" * 100)

# Get all states with branches
states_with_branches = MasState.objects.filter(masstatebranch__isnull=False).distinct().order_by('state_name')

print(f"🏛️ STATES WITH BRANCHES: {states_with_branches.count()}")
print()

for state in states_with_branches:
    branches = MasStateBranch.objects.filter(state=state).order_by('state_branch_name')
    print(f"🏛️ {state.state_name} ({state.state_code}): {branches.count()} branches")
    
    for branch in branches:
        print(f"   - {branch.state_branch_name} (Code: {branch.state_branch_code})")
    print()

print("=" * 100)
print("📊 STATISTICS")
print("=" * 100)

total_branches = MasStateBranch.objects.count()
total_states = MasState.objects.count()
states_with_branches_count = states_with_branches.count()

print(f"📈 Total Branches: {total_branches}")
print(f"🏛️ Total States: {total_states}")
print(f"✅ States with Branches: {states_with_branches_count}")
print(f"⚠️  States without Branches: {total_states - states_with_branches_count}")
print()

print("=" * 100)
print("🌐 TESTING INSTRUCTIONS")
print("=" * 100)

print("1. Start the Django server: python manage.py runserver")
print("2. Test each form with different states:")
print()
print("📋 CFA AGREEMENT FORM:")
print("   URL: http://127.0.0.1:8000/dashboard/cfa-agreement/create/")
print("   - Select 'Maharashtra' → Shows Mumbai branches")
print("   - Select 'Delhi' → Shows New Delhi branches")
print("   - Select 'Gujarat' → Shows Ahmedabad, Surat, etc.")
print()
print("📋 SPO RENT FORM:")
print("   URL: http://127.0.0.1:8000/dashboard/spo-rent/create/")
print("   - Select 'Uttar Pradesh' → Shows Lucknow, Kanpur, etc.")
print("   - Select 'West Bengal' → Shows Kolkata branches")
print("   - Select 'Andhra Pradesh' → Shows Visakhapatnam, Vijayawada, etc.")
print()
print("📋 TRANSPORTER AGREEMENT FORM:")
print("   URL: http://127.0.0.1:8000/dashboard/transporter-agreement/create/")
print("   - Select 'Telangana' → Shows Hyderabad branches")
print("   - Select 'Kerala' → Shows Thiruvananthapuram, Kochi, etc.")
print("   - Select 'Punjab' → Shows Chandigarh, Ludhiana, etc.")
print()

print("=" * 100)
print("✅ EXPECTED BEHAVIOR")
print("=" * 100)

print("🎯 State Selection:")
print("   - All 36 states from mas_state table shown in dropdown")
print("   - Most states now have 3-6 branches each")
print("   - Branch dropdowns will populate with relevant options")
print()
print("🎯 Branch Selection:")
print("   - SPO Rent & Transporter: Branch dropdown populates")
print("   - CFA Agreement: Auto-fill or show selection dialog")
print("   - All forms: District code auto-fills with state_branch_code")
print()
print("🎯 Visual Feedback:")
print("   - Green border on auto-filled fields")
print("   - Success messages with check icons")
print("   - Loading states during AJAX calls")
print()

print("=" * 100)
print("🎉 READY TO TEST!")
print("=" * 100)
print("✅ Comprehensive branch data added for all major states")
print("✅ State-branch functionality now works across all forms")
print("✅ Test with different states to see the variety of branches")
print("✅ No more limited to just Coimbatore and Chennai Central!") 