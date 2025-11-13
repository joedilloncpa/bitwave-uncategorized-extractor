# Change Log

## Version 1.3 - November 12, 2025

### Two Major Updates:

**1. FEE Operations Now Negative:**
- FEE operations now have negative values in both Token Amount and USD Value columns
- Previously, FEE operations remained positive
- This aligns FEE operations with WITHDRAW and SELL operations for consistent accounting

**2. Transaction Filtering by USD Value:**
- New filtering logic added: Only includes transactions where at least one row has an absolute USD Value ≥ $3,000
- If ANY row within a transaction group meets the $3,000 threshold, ALL rows for that transaction are included
- This helps focus on material transactions while keeping transaction groups complete
- Example: If a transaction has 3 rows with values of $50, $4,500, and $100, all 3 rows are kept because one row exceeds $3,000

### Updated Processing Logic:
âœ… FEE operations converted to negative (Token Amount and USD Value)  
âœ… Transactions filtered to include only those with USD Value ≥ $3,000 (absolute value)  
âœ… Transaction grouping preserved - all rows with same Transaction ID kept together  

---

## Version 1.2 - November 12, 2025

### Major Feature Added: Automatic Wallet Lookup

**New Functionality:**
- **Wallet Column Auto-Population**: The Wallet column is now automatically filled using a built-in lookup table
- **280+ Wallet Mappings**: Includes comprehensive wallet ID to name mappings
- **WalletId Column Removed**: After lookup, walletId is deleted from final output for cleaner results

### How It Works:
1. App reads walletId from uploaded CSV
2. Matches walletId against internal lookup table
3. Populates Wallet column with the corresponding wallet name
4. Removes walletId column from final output

### Updated Column Order:
1. dateTime (mm/dd/yy format)
2. Wallet (auto-populated from lookup) ⭐ UPDATED
3. Transaction ID
4. operation
5. assetTicker
6. Token Amount
7. USD Value
8. fromAddress
9. toAddress

### Testing Results:
✅ Wallet lookup working perfectly  
✅ walletId column removed from output  
✅ Sample wallets populated: "Payments to ME", "FB - Working Capital - SOL Wallet 1", etc.  
✅ All other processing steps working correctly  

---

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

4. **walletName Column Removed**
   - walletName column is now deleted during processing for cleaner output

---

## Version 1.0 - November 12, 2025

Initial release with core processing features.
