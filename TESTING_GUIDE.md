# Testing Guide for Version 1.3

## Quick Testing Checklist

Use this guide to verify that the new features are working correctly.

### ✅ Test 1: FEE Operations Are Negative

**What to Check:**
Look for any rows where the `operation` column says "FEE"

**Expected Result:**
- Both `Token Amount` and `USD Value` should be **negative numbers**
- Example: `-0.05` for Token Amount, `-125.50` for USD Value

**How to Test:**
1. Upload your CSV file
2. In the processed output, filter/search for "FEE" in the operation column
3. Verify all FEE rows have negative values

---

### ✅ Test 2: Only Material Transactions Appear (≥$3,000)

**What to Check:**
Review the Transaction IDs in the final output

**Expected Result:**
- Every Transaction ID group should have at least one row with absolute USD Value ≥ $3,000
- Entire transaction groups are included (not just individual rows)

**How to Test:**
1. Upload your CSV file
2. Note the original number of transactions before processing
3. Note the processed number of transactions after processing
4. Manually check a few Transaction ID groups:
   - Look at all rows for that Transaction ID
   - At least one row should have |USD Value| ≥ $3,000

**Example Check:**
```
Transaction ID: ABC123
Row 1: USD Value = $200    ← Below threshold
Row 2: USD Value = $5,000  ← MEETS threshold ✓
Row 3: USD Value = -$150   ← Below threshold

Result: All 3 rows included because Row 2 meets the criteria
```

---

### ✅ Test 3: Transaction Groups Stay Together

**What to Check:**
Transactions should never be split up

**Expected Result:**
- If a transaction has 5 rows and qualifies, all 5 rows appear
- If a transaction doesn't qualify, none of its rows appear

**How to Test:**
1. Pick a Transaction ID from the output
2. Count how many rows it has
3. Verify no rows are missing (check blank row separators)

---

### ✅ Test 4: Small Transactions Are Excluded

**What to Check:**
Transactions where ALL rows have |USD Value| < $3,000 should be excluded

**Expected Result:**
- Small transactions don't appear in output
- The processed file should have fewer transactions than the original

**How to Test:**
1. Compare the "Unique Transactions" stat before and after processing
2. The processed file should have fewer unique transactions
3. Manually verify that excluded transactions all had values under $3,000

---

## Common Scenarios

### Scenario 1: Large Positive Value
```
Transaction: XYZ456
Row 1: USD Value = $10,000
Result: ✅ Included (exceeds $3,000)
```

### Scenario 2: Large Negative Value
```
Transaction: XYZ789
Row 1: USD Value = -$8,500
Result: ✅ Included (absolute value $8,500 exceeds $3,000)
```

### Scenario 3: Mixed Values, One Large
```
Transaction: ABC999
Row 1: USD Value = $50
Row 2: USD Value = $3,200
Row 3: USD Value = -$100
Result: ✅ All 3 rows included (Row 2 meets threshold)
```

### Scenario 4: All Small Values
```
Transaction: DEF111
Row 1: USD Value = $500
Row 2: USD Value = $1,200
Row 3: USD Value = -$800
Result: ❌ Entire transaction excluded (no row meets threshold)
```

### Scenario 5: Exactly $3,000
```
Transaction: GHI222
Row 1: USD Value = $3,000
Result: ✅ Included (equals threshold)
```

---

## Troubleshooting

### Issue: FEE operations still showing as positive

**Check:**
- Verify you uploaded the new version (1.3) of the Python file
- If running locally, restart the Streamlit app
- If on Streamlit Cloud, ensure GitHub repo is updated and redeployed

### Issue: Transactions under $3,000 appearing in output

**Check:**
- Look at ALL rows for that Transaction ID
- One row might have a value ≥ $3,000 that you missed
- Remember to use absolute value (negative values count too)

### Issue: Transactions over $3,000 not appearing

**Check:**
- Verify the transaction was "Uncategorized" in the original file
- Check if the transaction was in the uploaded CSV at all

---

## Expected Statistics Changes

After implementing these changes, you should see:

📉 **Fewer Transactions:** The filtered output will have fewer unique transactions  
📉 **Fewer Rows:** Only material transactions remain  
✅ **Negative FEEs:** All FEE operations show negative values  
✅ **Consistent Data:** Transaction groups stay intact  

---

## Questions to Answer While Testing

1. ✅ Are all FEE operations showing as negative?
2. ✅ Do all remaining transactions have at least one row ≥ $3,000?
3. ✅ Are transaction groups staying together (not split)?
4. ✅ Is the output file smaller/more focused than before?

If you can answer "yes" to all four questions, the implementation is working correctly!

---

**Version:** 1.3.0  
**Last Updated:** November 12, 2025
