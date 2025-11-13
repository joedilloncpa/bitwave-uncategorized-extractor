# Version 1.3 Before & After Examples

## Example 1: FEE Operations

### BEFORE Version 1.3 ❌
```csv
dateTime,Wallet,Transaction ID,operation,assetTicker,Token Amount,USD Value
10/29/25,Trading Wallet,TX001,FEE,SOL,0.05,125.50
```

### AFTER Version 1.3 ✅
```csv
dateTime,Wallet,Transaction ID,operation,assetTicker,Token Amount,USD Value
10/29/25,Trading Wallet,TX001,FEE,SOL,-0.05,-125.50
```

**What Changed:** FEE operations now show as negative values (like WITHDRAW and SELL)

---

## Example 2: Material Transaction (Kept)

### Input Data:
```csv
Transaction ID: TX789
Row 1: USD Value = $500
Row 2: USD Value = $8,500  ← Exceeds $3,000 threshold
Row 3: USD Value = -$200
```

### BEFORE Version 1.3 ❌
**Result:** All 3 rows included (no filtering)

### AFTER Version 1.3 ✅
**Result:** All 3 rows included (one row meets threshold)

**Why:** At least one row has |USD Value| ≥ $3,000, so entire transaction is kept

---

## Example 3: Small Transaction (Excluded)

### Input Data:
```csv
Transaction ID: TX456
Row 1: USD Value = $150
Row 2: USD Value = $800
Row 3: USD Value = -$95
```

### BEFORE Version 1.3 ❌
**Result:** All 3 rows included (no filtering)

### AFTER Version 1.3 ✅
**Result:** All 3 rows excluded (below threshold)

**Why:** No row has |USD Value| ≥ $3,000, so entire transaction is filtered out

---

## Example 4: Complete Transaction Processing

### Original CSV (uploaded):
```csv
dateTime,operation,assetAmount,assetvalueInBaseCurrency,categorizationStatus,walletId,parenttransactionId
2025-10-29T03:00:05.000Z,DEPOSIT,100,5200,Uncategorized,nv6cqu6esAEqzXQSzTI6,TX001
2025-10-29T03:00:05.000Z,FEE,0.05,125,Uncategorized,nv6cqu6esAEqzXQSzTI6,TX001
2025-10-30T14:22:10.000Z,WITHDRAW,50,150,Uncategorized,aoLqhYqvv7a2wild8WNs,TX002
```

### BEFORE Version 1.3 ❌

**Processed Output:**
```csv
dateTime,Wallet,Transaction ID,operation,assetTicker,Token Amount,USD Value
10/29/25,FB - Working Capital - SOL Wallet 1 (nbEB),TX001,DEPOSIT,SOL,100,5200
10/29/25,FB - Working Capital - SOL Wallet 1 (nbEB),TX001,FEE,SOL,0.05,125

10/30/25,Payments to ME,TX002,WITHDRAW,SOL,-50,-150
```

**Issues:**
- ✅ TX001 included (DEPOSIT ≥ $3k)
- ❌ FEE is positive (should be negative)
- ❌ TX002 included (but only $150, below threshold)

### AFTER Version 1.3 ✅

**Processed Output:**
```csv
dateTime,Wallet,Transaction ID,operation,assetTicker,Token Amount,USD Value
10/29/25,FB - Working Capital - SOL Wallet 1 (nbEB),TX001,DEPOSIT,SOL,100,5200
10/29/25,FB - Working Capital - SOL Wallet 1 (nbEB),TX001,FEE,SOL,-0.05,-125
```

**Improvements:**
- ✅ TX001 included (DEPOSIT ≥ $3k) 
- ✅ FEE is now negative
- ✅ TX002 excluded (only $150, below threshold)

---

## Example 5: Edge Case - Exactly $3,000

### Input Data:
```csv
Transaction ID: TX999
Row 1: USD Value = $3,000  ← Exactly at threshold
```

### BEFORE Version 1.3 ❌
**Result:** Included (no filtering)

### AFTER Version 1.3 ✅
**Result:** Included (meets threshold with ≥ operator)

**Note:** The threshold is **inclusive** - values of exactly $3,000 qualify

---

## Example 6: Negative Large Value

### Input Data:
```csv
Transaction ID: TX888
Row 1: USD Value = -$7,500  ← Large negative value
```

### BEFORE Version 1.3 ❌
**Result:** Included (no filtering)

### AFTER Version 1.3 ✅
**Result:** Included (|-7500| = 7500 ≥ $3,000)

**Note:** Filtering uses **absolute value** - large negative amounts count!

---

## Example 7: Multi-Row Transaction with Mixed Values

### Input Data:
```csv
Transaction ID: TX555
Row 1: operation=DEPOSIT, USD Value = $4,800
Row 2: operation=FEE, USD Value = 120
Row 3: operation=WITHDRAW, USD Value = 2,500
```

### BEFORE Version 1.3:
```csv
10/29/25,Wallet A,TX555,DEPOSIT,SOL,100,4800
10/29/25,Wallet A,TX555,FEE,SOL,0.05,120        ← Positive FEE
10/29/25,Wallet A,TX555,WITHDRAW,SOL,-50,-2500
```

### AFTER Version 1.3:
```csv
10/29/25,Wallet A,TX555,DEPOSIT,SOL,100,4800
10/29/25,Wallet A,TX555,FEE,SOL,-0.05,-120      ← Negative FEE ✅
10/29/25,Wallet A,TX555,WITHDRAW,SOL,-50,-2500
```

**Changes:**
1. ✅ FEE is now negative
2. ✅ All rows kept (Row 1 exceeds $3,000)

---

## Example 8: Statistics Comparison

### Sample Dataset (20 Transactions):

**BEFORE Version 1.3:**
```
Total Transactions: 20
Total Rows: 38 (with blank separators)
Transactions by Size:
  - Under $1,000: 8 transactions
  - $1,000 - $2,999: 5 transactions
  - $3,000+: 7 transactions
```

**AFTER Version 1.3:**
```
Total Transactions: 7
Total Rows: 16 (with blank separators)
Transactions by Size:
  - Under $1,000: 0 transactions (filtered out)
  - $1,000 - $2,999: 0 transactions (filtered out)
  - $3,000+: 7 transactions (kept)
```

**Impact:**
- 65% reduction in transaction count (20 → 7)
- 58% reduction in row count (38 → 16)
- Focus on material transactions only

---

## Example 9: Complex Transaction Group

### Input:
```csv
Transaction ID: TX777
Row 1: DEPOSIT, $100
Row 2: FEE, $25
Row 3: DEPOSIT, $5,000    ← Exceeds threshold
Row 4: FEE, $50
Row 5: WITHDRAW, $200
```

### Processing:

**Step 1 - Check Threshold:**
- Row 3 has $5,000 ✅ → Keep entire transaction

**Step 2 - Apply Negative Logic:**
- Row 2 (FEE): $25 → -$25
- Row 4 (FEE): $50 → -$50
- Row 5 (WITHDRAW): -$200 (already negative)

### Final Output:
```csv
10/29/25,Wallet X,TX777,DEPOSIT,SOL,2,100
10/29/25,Wallet X,TX777,FEE,SOL,-0.01,-25      ← Negative
10/29/25,Wallet X,TX777,DEPOSIT,SOL,100,5000
10/29/25,Wallet X,TX777,FEE,SOL,-0.02,-50      ← Negative
10/29/25,Wallet X,TX777,WITHDRAW,SOL,-4,-200
```

---

## Summary of Changes

### FEE Operations
| Aspect | Before | After |
|--------|--------|-------|
| Token Amount | Positive | **Negative** |
| USD Value | Positive | **Negative** |
| Consistency | Different from WITHDRAW/SELL | Same as WITHDRAW/SELL |

### Transaction Filtering
| Transaction Type | Before | After |
|-----------------|--------|-------|
| All rows < $3,000 | Included | **Excluded** |
| Any row ≥ $3,000 | Included | **Included** |
| Edge case: = $3,000 | Included | **Included** |
| Large negative value | Included | **Included** (uses absolute value) |

---

**Version:** 1.3.0  
**Date:** November 12, 2025  
**Purpose:** Illustrate the practical impact of Version 1.3 changes
