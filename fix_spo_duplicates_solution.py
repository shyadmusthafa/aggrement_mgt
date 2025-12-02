#!/usr/bin/env python
"""
Solution to fix duplicate SPO records showing multiple rows for the same spo_id
"""

# SOLUTION 1: Update the spo_rent_list view in dashboard/views.py

def update_spo_rent_list_view():
    """
    Find the spo_rent_list function in dashboard/views.py and update the query
    """
    
    # CURRENT QUERY (causing duplicates):
    # records = SPORentRecord.objects.select_related('state', 'branch').all()
    
    # UPDATED QUERY (fixes duplicates):
    # records = SPORentRecord.objects.select_related('state', 'branch').distinct('id').order_by('id')
    
    # ALTERNATIVE QUERY (if distinct('id') not supported):
    # records = SPORentRecord.objects.select_related('state', 'branch').order_by('spo_id', 'id').distinct('spo_id')
    
    pass

# SOLUTION 2: Alternative approach using subquery

def alternative_subquery_solution():
    """
    Alternative solution using subquery to ensure unique records per spo_id
    """
    
    # In dashboard/views.py, replace the query with:
    """
    from django.db.models import Subquery, OuterRef
    
    # Get the latest record for each spo_id
    latest_records = SPORentRecord.objects.filter(
        spo_id=OuterRef('spo_id')
    ).order_by('-id').values('id')[:1]
    
    # Get the actual records
    records = SPORentRecord.objects.select_related('state', 'branch').filter(
        id=Subquery(latest_records)
    ).order_by('spo_id')
    """
    
    pass

# SOLUTION 3: Using values() and distinct()

def values_distinct_solution():
    """
    Solution using values() and distinct() to get unique spo_ids
    """
    
    # In dashboard/views.py, replace the query with:
    """
    # First get unique spo_ids
    unique_spo_ids = SPORentRecord.objects.values_list('spo_id', flat=True).distinct()
    
    # Then get the records for those spo_ids (latest record per spo_id)
    records = []
    for spo_id in unique_spo_ids:
        latest_record = SPORentRecord.objects.select_related('state', 'branch').filter(
            spo_id=spo_id
        ).order_by('-id').first()
        if latest_record:
            records.append(latest_record)
    """
    
    pass

# SOLUTION 4: Raw SQL approach

def raw_sql_solution():
    """
    Raw SQL solution for maximum control
    """
    
    # In dashboard/views.py, replace the query with:
    """
    from django.db import connection
    
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT DISTINCT ON (spo_id) *
            FROM dashboard_sporentrecord
            ORDER BY spo_id, id DESC
        """)
        records = cursor.fetchall()
    """
    
    pass

# RECOMMENDED IMPLEMENTATION:

def recommended_solution():
    """
    Step-by-step implementation guide
    """
    
    steps = """
    STEP 1: Open dashboard/views.py
    
    STEP 2: Find the spo_rent_list function (around line 150-200)
    
    STEP 3: Locate the query that looks like:
        records = SPORentRecord.objects.select_related('state', 'branch').all()
    
    STEP 4: Replace it with:
        records = SPORentRecord.objects.select_related('state', 'branch').distinct('id').order_by('id')
    
    STEP 5: If you get an error about distinct('id') not being supported, use:
        records = SPORentRecord.objects.select_related('state', 'branch').order_by('spo_id', 'id').distinct('spo_id')
    
    STEP 6: Save the file and restart Django server
    
    STEP 7: Test the SPO Rent Records page to verify duplicates are gone
    """
    
    return steps

# ADDITIONAL CONSIDERATIONS:

def additional_considerations():
    """
    Additional considerations for the fix
    """
    
    considerations = """
    CONSIDERATIONS:
    
    1. Database Support: 
       - distinct('id') works in PostgreSQL
       - For MySQL, use distinct('spo_id') instead
       - For SQLite, use the subquery approach
    
    2. Performance:
       - Add database indexes on spo_id and id columns
       - Consider pagination for large datasets
    
    3. Data Integrity:
       - Ensure you're getting the correct record per spo_id
       - Consider which record to show if multiple exist (latest, oldest, etc.)
    
    4. Related Data:
       - Partner data will still be accessible through relationships
       - Consider if you need to aggregate partner information
    """
    
    return considerations

if __name__ == "__main__":
    print("SPO Duplicate Records Fix - Complete Solution")
    print("=" * 50)
    print(recommended_solution())
    print("\n" + "=" * 50)
    print(additional_considerations()) 