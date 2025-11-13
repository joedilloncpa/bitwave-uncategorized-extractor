# Version 1.3 Changes Summary

## 🎯 What Changed

Your crypto transaction processor has been updated with two important improvements:

### 1. ✅ FEE Operations Now Show as Negative Values

**Problem Fixed:**
- Previously, rows with "FEE" in the operation column had positive values
- This was inconsistent with how WITHDRAW and SELL operations were handled

**Solution:**
- FEE operations now have negative values in both **Token Amount** and **USD Value** columns
- This makes accounting more consistent - all outflows are now negative

**Example:**
```
Before: operation=FEE, Token Amount=10, USD Value=50
After:  operation=FEE, Token Amount=-10, USD Value=-50
```

### 2. 🔍 Transaction Filtering by USD Value

**New Feature Added:**
- The app now filters to only include transactions where at least one row has an absolute USD Value ≥ $3,000
- **Important:** If ANY row in a transaction meets the $3,000 threshold, ALL rows for that transaction are included

**How It Works:**
1. The app examines each Transaction ID group
2. It looks for any row with absolute USD Value ≥ $3,000
3. If found, the entire transaction (all rows) is kept
4. If no rows meet the threshold, the entire transaction is excluded

**Example Scenario:**

Transaction ABC123 has 3 rows:
- Row 1: USD Value = $50
- Row 2: USD Value = $4,500 ✅ (meets threshold)
- Row 3: USD Value = -$100

**Result:** All 3 rows are included in the final output because Row 2 exceeds $3,000

Transaction XYZ789 has 2 rows:
- Row 1: USD Value = $500
- Row 2: USD Value = -$200

**Result:** Both rows are excluded because neither meets the $3,000 threshold (absolute values: $500 and $200)

Transaction DEF456 has 1 row:
- Row 1: USD Value = -$5,500

**Result:** Row is included because absolute value ($5,500) exceeds $3,000

**Important:** The filter uses **absolute value**, so both large positive values (≥$3,000) AND large negative values (≤-$3,000) will include the transaction.

### 3. 📊 Benefits

**For FEE Operations:**
- ✅ Consistent accounting treatment
- ✅ All outflows (WITHDRAW, SELL, FEE) are now negative
- ✅ Makes reconciliation easier

**For USD Value Filtering:**
- ✅ Focus on material transactions
- ✅ Reduces noise from small transactions
- ✅ Maintains transaction integrity (keeps related rows together)
- ✅ Saves time reviewing output files

## 🔄 Updated Processing Flow

The complete processing flow is now:

1. Filter for "Uncategorized" transactions
2. Remove unnecessary columns
3. Format dates to mm/dd/yy
4. Process FEE operations (merge fee data)
5. **Convert WITHDRAW/SELL/FEE to negative values** ⭐ UPDATED
6. Populate Wallet column from lookup table
7. **Filter for transactions with USD Value ≥ $3,000** ⭐ NEW
8. Sort by oldest transactions first
9. Group by Transaction ID with blank row separators
10. Reorder columns

## 📁 Updated Files

All documentation has been updated to reflect these changes:

- ✅ `crypto_transaction_processor.py` - Main application with new logic
- ✅ `README.md` - Updated processing steps and notes
- ✅ `CHANGELOG.md` - Version 1.3 documented
- ✅ This summary document

## 🚀 Next Steps

1. **Upload to GitHub:** Replace your existing files with these updated ones
2. **Test with Real Data:** Upload a file to verify the filtering works as expected
3. **Monitor Output:** Check that only material transactions (≥$3,000) appear in results

## ⚠️ Important Notes

- The $3,000 threshold uses **absolute value**, so both +$3,000 and -$3,000 count
- Transaction grouping is preserved - you'll never see partial transactions
- All rows with the same Transaction ID stay together (or are excluded together)

## 💡 Future Considerations

If you need to adjust the $3,000 threshold in the future, you can easily modify line 358 in the Python file:

```python
# Current:
qualifying_transactions = transaction_max_values[transaction_max_values >= 3000].index

# To change threshold to $5,000:
qualifying_transactions = transaction_max_values[transaction_max_values >= 5000].index
```

---

**Version:** 1.3.0  
**Date:** November 12, 2025  
**Changes:** FEE operations negative + USD Value filtering
