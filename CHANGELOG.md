# Change Log

## Version 1.1 - November 12, 2025

### Changes Made:

1. **Date Format Changed**
   - OLD: dd/mm/yy format (e.g., 29/10/25)
   - NEW: mm/dd/yy format (e.g., 10/29/25)

2. **Transaction Sorting Changed**
   - OLD: Sorted by Transaction ID only
   - NEW: Sorted with oldest transactions at the top (chronological order)

3. **walletId Column Retained**
   - OLD: walletId was deleted during processing
   - NEW: walletId is kept in the output and appears as the second column

### Updated Column Order:

1. dateTime (mm/dd/yy format)
2. walletId ⭐ NEW
3. Wallet (empty - for manual entry)
4. Transaction ID
5. operation
6. assetTicker
7. Token Amount
8. USD Value
9. fromAddress
10. toAddress

### Testing Results:

✅ Sample file processed successfully
✅ Date format: 10/02/25 (mm/dd/yy)
✅ Oldest transactions appear first
✅ walletId column present with values
✅ All other processing steps working correctly

---

## Version 1.0 - November 12, 2025

Initial release with core processing features.
