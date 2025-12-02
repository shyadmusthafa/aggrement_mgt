#!/usr/bin/env python
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()

from dashboard.models import CFAAgreement, MasState, MasStateBranch

print("=" * 80)
print("COMPLETE CFA AGREEMENT TABLE DATA")
print("=" * 80)

# Get all CFA Agreement records
cfa_records = CFAAgreement.objects.all().select_related('state')

print(f"Total CFA Agreement Records: {cfa_records.count()}")
print()

if cfa_records.count() == 0:
    print("❌ No CFA Agreement records found in the database!")
    print()
    print("Available related tables:")
    print(f"- MasState records: {MasState.objects.count()}")
    print(f"- MasStateBranch records: {MasStateBranch.objects.count()}")
else:
    # Display each record in detail
    for i, record in enumerate(cfa_records, 1):
        print(f"📋 RECORD #{i}")
        print("-" * 50)
        
        # Basic Information
        print(f"🆔 ID: {record.id}")
        print(f"📝 CFA Code: {record.cfa_code}")
        print(f"🏢 CFA Name: {record.cfa_name}")
        print(f"📧 Email: {record.cfa_mail_id}")
        print(f"📱 Phone: {record.cfa_phone}")
        print(f"🌐 Website: {record.cfa_website}")
        
        # SPO Information
        print(f"🏷️ SPO Code: {record.spo_code}")
        print(f"🏷️ SPO Name: {record.spo_name}")
        
        # Location Information
        print(f"🏛️ State: {record.state.state_name if record.state else 'N/A'}")
        print(f"🏛️ State Code: {record.state.state_code if record.state else 'N/A'}")
        print(f"🏢 Branch: {record.branch_name}")
        print(f"🏢 Branch Code: {record.branch_code}")
        print(f"🏘️ District Code: {record.district_code}")
        print(f"🏘️ District Name: {record.district_name}")
        
        # Address Information
        print(f"📍 Godown Address: {record.godown_address}")
        print(f"📍 CFA Address: {record.cfa_address}")
        
        # Owner Information
        print(f"👤 Owner Name: {record.owner_name}")
        print(f"📞 Owner Contact: {record.owner_contact}")
        print(f"📧 Owner Email: {record.owner_email}")
        
        # Business Information
        print(f"🏢 Structure Group: {record.stru_grp}")
        print(f"📊 CFA Status: {record.cfa_status}")
        print(f"📋 Agreement Type: {record.agreement_renewal}")
        print(f"📅 Inception Date: {record.inception_date}")
        print(f"📅 Agreement From Date: {record.agreement_from_date}")
        print(f"📅 Agreement To Date: {record.agreement_to_date}")
        
        # Financial Information
        print(f"💰 Security Deposit: {record.security_deposit}")
        print(f"🏦 Bank Account Name: {record.bank_account_name}")
        print(f"🏦 Bank Account No: {record.bank_account_no}")
        print(f"🏦 Bank Name: {record.bank_name}")
        print(f"🏦 Bank Branch: {record.bank_branch}")
        print(f"🏦 Bank IFSC: {record.bank_ifsc}")
        
        # Tax Information
        print(f"🧾 GST No: {record.gst_no}")
        print(f"🧾 PAN No: {record.pan_no}")
        
        # Other Information
        print(f"🎯 Destination Code: {record.destination_code}")
        print(f"📝 Remarks: {record.remarks}")
        print(f"📊 Status: {record.status}")
        
        # Document Attachments
        print(f"📄 CFA Agreement: {'✅ Yes' if record.cfa_agreement else '❌ No'}")
        print(f"📄 Closure Letter: {'✅ Yes' if record.closure_letter else '❌ No'}")
        print(f"📄 Closure Acceptance: {'✅ Yes' if record.closure_acceptance_letter else '❌ No'}")
        print(f"📄 F&F Letter & Calc: {'✅ Yes' if record.ff_letter_calc else '❌ No'}")
        print(f"📄 Security Deposit Doc: {'✅ Yes' if record.security_deposit else '❌ No'}")
        
        # Timestamps
        print(f"📅 Created: {record.created_at}")
        print(f"📅 Updated: {record.updated_at}")
        
        print()
        print("=" * 80)
        print()

# Show table statistics
print("📊 TABLE STATISTICS")
print("-" * 30)
print(f"Total Records: {cfa_records.count()}")
print(f"Active Records: {cfa_records.filter(status__iexact='active').count()}")
print(f"Inactive Records: {cfa_records.exclude(status__iexact='active').count()}")
print(f"Records with Email: {cfa_records.exclude(cfa_mail_id__isnull=True).exclude(cfa_mail_id='').count()}")
print(f"Records with Phone: {cfa_records.exclude(cfa_phone__isnull=True).exclude(cfa_phone='').count()}")

# Show related table data
print()
print("🔗 RELATED TABLES")
print("-" * 20)

# MasState data
print(f"📋 MasState Records: {MasState.objects.count()}")
for state in MasState.objects.all():
    print(f"  - {state.state_name} (Code: {state.state_code})")

print()
print(f"🏢 MasStateBranch Records: {MasStateBranch.objects.count()}")
for branch in MasStateBranch.objects.all()[:10]:  # Show first 10
    print(f"  - {branch.branch_name} (Code: {branch.branch_code})")
if MasStateBranch.objects.count() > 10:
    print(f"  ... and {MasStateBranch.objects.count() - 10} more branches")

print()
print("=" * 80)
print("✅ Data export complete!") 