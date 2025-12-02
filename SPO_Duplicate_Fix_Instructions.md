# SPO Rent Records - Fix Duplicate Records Issue

## Problem
The SPO Rent Records module is currently showing multiple rows for the same `spo_id`, causing duplicate entries in the table.

## Root Cause
This typically happens when:
1. There are multiple records in the database with the same `spo_id`
2. The query includes joins that create duplicate rows
3. The query doesn't use `distinct()` to ensure unique records

## Solution

### Step 1: Locate the spo_rent_list function
Open `dashboard/views.py` and find the `spo_rent_list` function.

### Step 2: Find the main query
Look for a line similar to:
```python
records = SPORentRecord.objects.select_related('state', 'branch').all()
```

### Step 3: Update the query
Replace the query with one of these options:

#### Option A: Using distinct('id') (Recommended for PostgreSQL)
```python
records = SPORentRecord.objects.select_related('state', 'branch').distinct('id').order_by('id')
```

#### Option B: Using distinct() with values() (Works with all databases)
```python
# Get unique IDs first
unique_ids = SPORentRecord.objects.values('id').distinct()
records = SPORentRecord.objects.select_related('state', 'branch').filter(
    id__in=unique_ids.values_list('id', flat=True)
).order_by('id')
```

#### Option C: Add distinct at the end of the function
If you can't find the initial query, add this line before pagination:
```python
# Ensure unique records per spo_id before pagination
records = records.distinct('id').order_by('id')
```

### Step 4: Alternative approach using raw SQL
If the above doesn't work, you can use raw SQL:
```python
from django.db import connection

with connection.cursor() as cursor:
    cursor.execute("""
        SELECT DISTINCT ON (spo_id) *
        FROM dashboard_sporentrecord
        ORDER BY spo_id, id DESC
    """)
    records = cursor.fetchall()
```

## Testing the Fix

1. **Save the file** after making changes
2. **Restart the Django server**
3. **Navigate to** `http://127.0.0.1:8000/dashboard/spo-rent/`
4. **Verify** that each `spo_id` appears only once in the table

## Expected Result
- Each SPO should appear only once in the table
- All related data (state, branch, owner info) should still be displayed
- Pagination should work correctly
- Filters should continue to work

## Troubleshooting

### If distinct('id') doesn't work:
- Your database might not support `distinct('id')`
- Use Option B or C instead

### If you still see duplicates:
- Check if there are actual duplicate records in the database
- Verify the `spo_id` field is properly indexed
- Consider adding a unique constraint to the model

### If performance is slow:
- Add database indexes on `spo_id` and `id` fields
- Consider using `only()` to select specific fields
- Use `prefetch_related()` instead of `select_related()` if needed

## Database Index Recommendation
Add this to your model or create a migration:
```python
class Meta:
    indexes = [
        models.Index(fields=['spo_id']),
        models.Index(fields=['id']),
    ]
```

## Final Notes
- The `distinct('id')` approach is the most efficient for PostgreSQL
- For MySQL, use Option B or C
- Always test with a small dataset first
- Monitor query performance after the change 