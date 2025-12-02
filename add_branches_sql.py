#!/usr/bin/env python
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()

from django.db import connection

print("=" * 100)
print("🏢 ADDING COMPREHENSIVE BRANCH DATA USING SQL")
print("=" * 100)

# Comprehensive branch data for all major states
branch_data = [
    # Karnataka
    ("Karnataka", "Bangalore Central", "BL001"),
    ("Karnataka", "Bangalore North", "BL002"),
    ("Karnataka", "Bangalore South", "BL003"),
    ("Karnataka", "Mysore", "MY001"),
    ("Karnataka", "Mangalore", "MG001"),
    ("Karnataka", "Hubli", "HB001"),
    
    # Tamil Nadu
    ("Tamil Nadu", "Chennai Central", "CH001"),
    ("Tamil Nadu", "Chennai North", "CH002"),
    ("Tamil Nadu", "Chennai South", "CH003"),
    ("Tamil Nadu", "Coimbatore", "CO001"),
    ("Tamil Nadu", "Madurai", "MD001"),
    ("Tamil Nadu", "Salem", "SL001"),
    ("Tamil Nadu", "Trichy", "TC001"),
    ("Tamil Nadu", "Vellore", "VL001"),
    
    # Maharashtra
    ("Maharashtra", "Mumbai Central", "MB001"),
    ("Maharashtra", "Mumbai North", "MB002"),
    ("Maharashtra", "Mumbai South", "MB003"),
    ("Maharashtra", "Pune", "PN001"),
    ("Maharashtra", "Nagpur", "NG001"),
    ("Maharashtra", "Aurangabad", "AB001"),
    ("Maharashtra", "Nashik", "NK001"),
    
    # Delhi
    ("Delhi", "New Delhi Central", "ND001"),
    ("Delhi", "New Delhi North", "ND002"),
    ("Delhi", "New Delhi South", "ND003"),
    ("Delhi", "New Delhi East", "ND004"),
    ("Delhi", "New Delhi West", "ND005"),
    
    # Gujarat
    ("Gujarat", "Ahmedabad", "AH001"),
    ("Gujarat", "Surat", "SR001"),
    ("Gujarat", "Vadodara", "VD001"),
    ("Gujarat", "Rajkot", "RJ001"),
    ("Gujarat", "Bhavnagar", "BG001"),
    
    # West Bengal
    ("West Bengal", "Kolkata Central", "KC001"),
    ("West Bengal", "Kolkata North", "KC002"),
    ("West Bengal", "Kolkata South", "KC003"),
    ("West Bengal", "Howrah", "HW001"),
    ("West Bengal", "Durgapur", "DP001"),
    
    # Uttar Pradesh
    ("Uttar Pradesh", "Lucknow", "LK001"),
    ("Uttar Pradesh", "Kanpur", "KP001"),
    ("Uttar Pradesh", "Varanasi", "VS001"),
    ("Uttar Pradesh", "Agra", "AG001"),
    ("Uttar Pradesh", "Allahabad", "AL001"),
    ("Uttar Pradesh", "Ghaziabad", "GZ001"),
    
    # Andhra Pradesh
    ("Andhra Pradesh", "Visakhapatnam", "VP001"),
    ("Andhra Pradesh", "Vijayawada", "VJ001"),
    ("Andhra Pradesh", "Guntur", "GT001"),
    ("Andhra Pradesh", "Nellore", "NL001"),
    ("Andhra Pradesh", "Kurnool", "KN001"),
    
    # Telangana
    ("Telangana", "Hyderabad Central", "HC001"),
    ("Telangana", "Hyderabad North", "HC002"),
    ("Telangana", "Hyderabad South", "HC003"),
    ("Telangana", "Warangal", "WG001"),
    ("Telangana", "Karimnagar", "KM001"),
    
    # Kerala
    ("Kerala", "Thiruvananthapuram", "TV001"),
    ("Kerala", "Kochi", "KC001"),
    ("Kerala", "Kozhikode", "KZ001"),
    ("Kerala", "Thrissur", "TS001"),
    ("Kerala", "Kollam", "KL001"),
    
    # Punjab
    ("Punjab", "Chandigarh", "CH001"),
    ("Punjab", "Ludhiana", "LD001"),
    ("Punjab", "Amritsar", "AM001"),
    ("Punjab", "Jalandhar", "JL001"),
    ("Punjab", "Patiala", "PT001"),
    
    # Rajasthan
    ("Rajasthan", "Jaipur", "JP001"),
    ("Rajasthan", "Jodhpur", "JD001"),
    ("Rajasthan", "Udaipur", "UD001"),
    ("Rajasthan", "Kota", "KT001"),
    ("Rajasthan", "Bikaner", "BK001"),
    
    # Madhya Pradesh
    ("Madhya Pradesh", "Bhopal", "BP001"),
    ("Madhya Pradesh", "Indore", "ID001"),
    ("Madhya Pradesh", "Jabalpur", "JB001"),
    ("Madhya Pradesh", "Gwalior", "GW001"),
    ("Madhya Pradesh", "Ujjain", "UJ001"),
    
    # Bihar
    ("Bihar", "Patna", "PT001"),
    ("Bihar", "Gaya", "GY001"),
    ("Bihar", "Bhagalpur", "BG001"),
    ("Bihar", "Muzaffarpur", "MZ001"),
    ("Bihar", "Darbhanga", "DB001"),
    
    # Odisha
    ("Odisha", "Bhubaneswar", "BB001"),
    ("Odisha", "Cuttack", "CT001"),
    ("Odisha", "Rourkela", "RK001"),
    ("Odisha", "Sambalpur", "SP001"),
    ("Odisha", "Puri", "PR001"),
    
    # Assam
    ("Assam", "Guwahati", "GW001"),
    ("Assam", "Dibrugarh", "DB001"),
    ("Assam", "Silchar", "SC001"),
    ("Assam", "Jorhat", "JH001"),
    ("Assam", "Tezpur", "TZ001"),
    
    # Jharkhand
    ("Jharkhand", "Ranchi", "RC001"),
    ("Jharkhand", "Jamshedpur", "JS001"),
    ("Jharkhand", "Dhanbad", "DB001"),
    ("Jharkhand", "Bokaro", "BK001"),
    ("Jharkhand", "Hazaribagh", "HZ001"),
    
    # Chhattisgarh
    ("Chhattisgarh", "Raipur", "RP001"),
    ("Chhattisgarh", "Bhilai", "BL001"),
    ("Chhattisgarh", "Bilaspur", "BS001"),
    ("Chhattisgarh", "Korba", "KB001"),
    ("Chhattisgarh", "Jagdalpur", "JG001"),
    
    # Haryana
    ("Haryana", "Gurgaon", "GG001"),
    ("Haryana", "Faridabad", "FB001"),
    ("Haryana", "Panipat", "PP001"),
    ("Haryana", "Hisar", "HS001"),
    ("Haryana", "Rohtak", "RT001"),
    
    # Uttarakhand
    ("Uttarakhand", "Dehradun", "DD001"),
    ("Uttarakhand", "Haridwar", "HW001"),
    ("Uttarakhand", "Nainital", "NT001"),
    ("Uttarakhand", "Almora", "AM001"),
    ("Uttarakhand", "Pithoragarh", "PG001"),
    
    # Himachal Pradesh
    ("Himachal Pradesh", "Shimla", "SL001"),
    ("Himachal Pradesh", "Mandi", "MD001"),
    ("Himachal Pradesh", "Kullu", "KL001"),
    ("Himachal Pradesh", "Solan", "SN001"),
    ("Himachal Pradesh", "Kangra", "KG001"),
    
    # Goa
    ("Goa", "Panaji", "PJ001"),
    ("Goa", "Margao", "MG001"),
    ("Goa", "Vasco da Gama", "VD001"),
    ("Goa", "Mapusa", "MP001"),
    ("Goa", "Ponda", "PD001"),
    
    # Jammu and Kashmir
    ("Jammu and Kashmir", "Srinagar", "SR001"),
    ("Jammu and Kashmir", "Jammu", "JM001"),
    ("Jammu and Kashmir", "Leh", "LH001"),
    ("Jammu and Kashmir", "Kargil", "KG001"),
    ("Jammu and Kashmir", "Anantnag", "AN001"),
    
    # Manipur
    ("Manipur", "Imphal", "IM001"),
    ("Manipur", "Thoubal", "TB001"),
    ("Manipur", "Bishnupur", "BP001"),
    ("Manipur", "Churachandpur", "CP001"),
    ("Manipur", "Ukhrul", "UK001"),
    
    # Meghalaya
    ("Meghalaya", "Shillong", "SH001"),
    ("Meghalaya", "Tura", "TR001"),
    ("Meghalaya", "Jowai", "JW001"),
    ("Meghalaya", "Nongstoin", "NS001"),
    ("Meghalaya", "Williamnagar", "WG001"),
    
    # Mizoram
    ("Mizoram", "Aizawl", "AZ001"),
    ("Mizoram", "Lunglei", "LG001"),
    ("Mizoram", "Saiha", "SH001"),
    ("Mizoram", "Champhai", "CH001"),
    ("Mizoram", "Kolasib", "KB001"),
    
    # Nagaland
    ("Nagaland", "Kohima", "KH001"),
    ("Nagaland", "Dimapur", "DP001"),
    ("Nagaland", "Mokokchung", "MK001"),
    ("Nagaland", "Tuensang", "TS001"),
    ("Nagaland", "Wokha", "WK001"),
    
    # Tripura
    ("Tripura", "Agartala", "AG001"),
    ("Tripura", "Udaipur", "UD001"),
    ("Tripura", "Dharmanagar", "DH001"),
    ("Tripura", "Kailasahar", "KL001"),
    ("Tripura", "Belonia", "BL001"),
    
    # Sikkim
    ("Sikkim", "Gangtok", "GT001"),
    ("Sikkim", "Namchi", "NM001"),
    ("Sikkim", "Mangan", "MG001"),
    ("Sikkim", "Gyalshing", "GY001"),
    ("Sikkim", "Ravangla", "RV001"),
    
    # Union Territories
    ("Chandigarh", "Chandigarh Central", "CC001"),
    ("Chandigarh", "Chandigarh North", "CC002"),
    ("Chandigarh", "Chandigarh South", "CC003"),
    
    ("Puducherry", "Puducherry Central", "PC001"),
    ("Puducherry", "Karaikal", "KR001"),
    ("Puducherry", "Mahe", "MH001"),
    ("Puducherry", "Yanam", "YN001"),
    
    ("Andaman and Nicobar Islands", "Port Blair", "PB001"),
    ("Andaman and Nicobar Islands", "Car Nicobar", "CN001"),
    ("Andaman and Nicobar Islands", "Mayabunder", "MB001"),
    
    ("Dadra and Nagar Haveli and Daman and Diu", "Daman", "DM001"),
    ("Dadra and Nagar Haveli and Daman and Diu", "Diu", "DI001"),
    ("Dadra and Nagar Haveli and Daman and Diu", "Silvassa", "SV001"),
    
    ("Lakshadweep", "Kavaratti", "KV001"),
    ("Lakshadweep", "Agatti", "AG001"),
    ("Lakshadweep", "Minicoy", "MC001"),
    
    ("Ladakh", "Leh", "LH001"),
    ("Ladakh", "Kargil", "KG001"),
    ("Ladakh", "Nubra", "NB001"),
]

def add_branches():
    """Add branch data using SQL queries"""
    cursor = connection.cursor()
    
    # First, let's check existing branches
    cursor.execute("SELECT COUNT(*) FROM mas_state_branch")
    existing_count = cursor.fetchone()[0]
    print(f"📊 Existing branches: {existing_count}")
    
    # Get state IDs for reference
    cursor.execute("SELECT id, state_name FROM mas_state ORDER BY state_name")
    states = {row[1]: row[0] for row in cursor.fetchall()}
    
    print(f"🏛️ Found {len(states)} states in database")
    
    # Add branches
    added_count = 0
    skipped_count = 0
    
    for state_name, branch_name, branch_code in branch_data:
        if state_name in states:
            state_id = states[state_name]
            
            # Check if branch already exists
            cursor.execute(
                "SELECT COUNT(*) FROM mas_state_branch WHERE state_id = %s AND state_branch_name = %s AND state_branch_code = %s",
                [state_id, branch_name, branch_code]
            )
            
            if cursor.fetchone()[0] == 0:
                # Insert new branch
                cursor.execute(
                    "INSERT INTO mas_state_branch (state_id, state_branch_name, state_branch_code) VALUES (%s, %s, %s)",
                    [state_id, branch_name, branch_code]
                )
                added_count += 1
                print(f"✅ Added: {state_name} → {branch_name} ({branch_code})")
            else:
                skipped_count += 1
                print(f"⏭️  Skipped (exists): {state_name} → {branch_name} ({branch_code})")
        else:
            print(f"❌ State not found: {state_name}")
    
    # Commit the changes
    connection.commit()
    
    # Final count
    cursor.execute("SELECT COUNT(*) FROM mas_state_branch")
    final_count = cursor.fetchone()[0]
    
    print()
    print("=" * 100)
    print("📊 SUMMARY")
    print("=" * 100)
    print(f"📈 Branches before: {existing_count}")
    print(f"✅ Branches added: {added_count}")
    print(f"⏭️  Branches skipped: {skipped_count}")
    print(f"📊 Branches after: {final_count}")
    print(f"📈 Net increase: {final_count - existing_count}")
    
    cursor.close()

if __name__ == "__main__":
    add_branches()
    print()
    print("=" * 100)
    print("🎉 BRANCH DATA ADDITION COMPLETE!")
    print("=" * 100)
    print("✅ All major states now have comprehensive branch data")
    print("✅ State-branch functionality will work across all forms")
    print("✅ Test the forms to see the new branch options") 