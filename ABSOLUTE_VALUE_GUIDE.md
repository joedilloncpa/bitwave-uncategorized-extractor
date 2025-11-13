# 📊 USD Value Filtering Logic - Visual Guide

## How the $3,000 Threshold Works

### ✅ The Rule (Using Absolute Value)

The app keeps a transaction if **at least one row** has:
- USD Value ≥ **$3,000** (positive), OR
- USD Value ≤ **-$3,000** (negative)

In other words: `|USD Value| ≥ $3,000`

---

## Visual Number Line

```
◄──────────────────────────────────────────────────────────────────►
                EXCLUDE           |        INCLUDE         
    -$2,999 to $2,999            |   ≥$3,000 OR ≤-$3,000
                                 |
        ← TOO SMALL →            |    ← MATERIAL →
                                 |
   -$2,999  -$1,000   $0  $1,000  $2,999 | $3,000  $5,000  $10,000
      ❌       ❌      ❌     ❌      ❌   |   ✅      ✅       ✅
                                         |
  -$10,000 -$5,000  -$3,000             |
      ✅       ✅       ✅              |
                                         |
         INCLUDE ← LARGE NEGATIVE        | LARGE POSITIVE → INCLUDE
```

---

## 📋 Decision Table

| USD Value | Absolute Value | Include? | Reason |
|-----------|----------------|----------|---------|
| $10,000 | $10,000 | ✅ YES | ≥ $3,000 |
| $5,000 | $5,000 | ✅ YES | ≥ $3,000 |
| $3,000 | $3,000 | ✅ YES | = $3,000 (inclusive) |
| $2,999 | $2,999 | ❌ NO | < $3,000 |
| $500 | $500 | ❌ NO | < $3,000 |
| $0 | $0 | ❌ NO | < $3,000 |
| -$500 | $500 | ❌ NO | < $3,000 |
| -$2,999 | $2,999 | ❌ NO | < $3,000 |
| -$3,000 | $3,000 | ✅ YES | = $3,000 (inclusive) |
| -$5,000 | $5,000 | ✅ YES | ≥ $3,000 |
| -$10,000 | $10,000 | ✅ YES | ≥ $3,000 |

---

## 🎯 Real-World Examples

### Example 1: Large Positive Value ✅
```
Transaction: TX001
Row 1: USD Value = $8,500

Calculation: |$8,500| = $8,500
Decision: $8,500 ≥ $3,000 → ✅ INCLUDE
```

### Example 2: Large Negative Value ✅
```
Transaction: TX002
Row 1: USD Value = -$7,200

Calculation: |-$7,200| = $7,200
Decision: $7,200 ≥ $3,000 → ✅ INCLUDE
```

### Example 3: Small Positive Value ❌
```
Transaction: TX003
Row 1: USD Value = $1,500

Calculation: |$1,500| = $1,500
Decision: $1,500 < $3,000 → ❌ EXCLUDE
```

### Example 4: Small Negative Value ❌
```
Transaction: TX004
Row 1: USD Value = -$2,800

Calculation: |-$2,800| = $2,800
Decision: $2,800 < $3,000 → ❌ EXCLUDE
```

### Example 5: Exactly $3,000 ✅
```
Transaction: TX005
Row 1: USD Value = $3,000

Calculation: |$3,000| = $3,000
Decision: $3,000 ≥ $3,000 → ✅ INCLUDE (inclusive threshold)
```

### Example 6: Exactly -$3,000 ✅
```
Transaction: TX006
Row 1: USD Value = -$3,000

Calculation: |-$3,000| = $3,000
Decision: $3,000 ≥ $3,000 → ✅ INCLUDE (inclusive threshold)
```

### Example 7: Mixed Values, One Qualifies ✅
```
Transaction: TX007
Row 1: USD Value = $200
Row 2: USD Value = $4,500  ← This row qualifies!
Row 3: USD Value = -$100

Calculation for Row 2: |$4,500| = $4,500
Decision: $4,500 ≥ $3,000 → ✅ INCLUDE ALL 3 ROWS
```

### Example 8: All Small Values ❌
```
Transaction: TX008
Row 1: USD Value = $500
Row 2: USD Value = -$1,200
Row 3: USD Value = $800

Best row calculation: |-$1,200| = $1,200
Decision: $1,200 < $3,000 → ❌ EXCLUDE ALL 3 ROWS
```

### Example 9: Mixed Positive and Large Negative ✅
```
Transaction: TX009
Row 1: USD Value = $100
Row 2: USD Value = -$8,000  ← This row qualifies!
Row 3: USD Value = $50

Calculation for Row 2: |-$8,000| = $8,000
Decision: $8,000 ≥ $3,000 → ✅ INCLUDE ALL 3 ROWS
```

---

## 🔍 Common Misconceptions

### ❌ WRONG: "Only positive values ≥ $3,000 are included"
This is incorrect. Large negative values also count!

### ✅ CORRECT: "Values with absolute value ≥ $3,000 are included"
Both $3,000+ AND -$3,000- transactions are included.

---

### ❌ WRONG: "A -$5,000 transaction is excluded because it's negative"
This is incorrect. The absolute value is $5,000, which exceeds the threshold.

### ✅ CORRECT: "A -$5,000 transaction is included because |-5000| = $5,000 ≥ $3,000"
Negative signs are ignored when checking the threshold.

---

### ❌ WRONG: "Each row must be ≥ $3,000 to be included"
This is incorrect. Only ONE row needs to meet the threshold.

### ✅ CORRECT: "If ANY row in a transaction meets the threshold, ALL rows are included"
Transaction groups stay together.

---

## 💡 Why Absolute Value?

**Scenario:** A large withdrawal transaction

```
Transaction: WITHDRAWAL_123
Row 1: WITHDRAW, USD Value = -$50,000
Row 2: FEE, USD Value = -$250
```

**Without absolute value logic:**
- -$50,000 < $3,000 → Would be excluded ❌
- This is a VERY material transaction that should be included!

**With absolute value logic:**
- |-$50,000| = $50,000 ≥ $3,000 → Included ✅
- Makes sense - this is a significant transaction!

---

## 📐 The Math Behind It

### Code Implementation:
```python
# Calculate absolute value
df['abs_usd_value'] = df['USD Value'].abs()

# Group by Transaction ID, get max absolute value
transaction_max_values = df.groupby('Transaction ID')['abs_usd_value'].max()

# Keep transactions where max absolute value >= 3000
qualifying_transactions = transaction_max_values[transaction_max_values >= 3000].index
```

### What This Does:
1. Takes absolute value of every USD Value
2. Groups rows by Transaction ID
3. Finds the maximum absolute value within each group
4. Keeps the entire transaction if max ≥ $3,000

---

## 🎓 Quick Quiz

**Question 1:** Transaction has USD Values: $500, -$4,000, $100. Is it included?
<details>
<summary>Click for answer</summary>

✅ **YES** - The -$4,000 row has absolute value of $4,000, which is ≥ $3,000
</details>

**Question 2:** Transaction has USD Values: $2,500, -$1,800, $900. Is it included?
<details>
<summary>Click for answer</summary>

❌ **NO** - Highest absolute value is $2,500, which is < $3,000
</details>

**Question 3:** Transaction has USD Value: -$3,000. Is it included?
<details>
<summary>Click for answer</summary>

✅ **YES** - Absolute value is $3,000, which equals the threshold (inclusive)
</details>

---

## 🔑 Key Takeaways

1. **Threshold is $3,000 ABSOLUTE VALUE**
   - Positive ≥ $3,000 → Included
   - Negative ≤ -$3,000 → Included

2. **Transaction groups stay together**
   - If ONE row qualifies, ALL rows in that transaction are kept

3. **The threshold is inclusive**
   - Exactly $3,000 or -$3,000 counts as meeting the threshold

4. **Large withdrawals/expenses count**
   - A -$10,000 expense is just as material as a $10,000 revenue

5. **Sign doesn't matter for filtering**
   - Only the magnitude (absolute value) matters

---

**This ensures you capture ALL material transactions, regardless of whether they're inflows or outflows!**

**Version:** 1.3.0  
**Last Updated:** November 12, 2025
