# Cryptocurrency Transaction Processor

A Streamlit web application for processing and formatting cryptocurrency transaction CSV files from Bitwave exports.

## Features

- 📤 Upload CSV files with cryptocurrency transaction data
- 🔄 Automatic data processing and transformation
- 📊 Real-time data preview
- 💾 Download processed CSV files
- 📈 Transaction statistics and analytics
- ✨ Clean, user-friendly interface

## Processing Steps

The application automatically performs the following transformations:

1. **Filtering**: Extracts only rows with "Uncategorized" in the categorizationStatus column
2. **Column Deletion**: Removes unnecessary columns (categorizationStatus, ordID, runID, dateTimeSEC, walletName, etc.)
3. **Date Formatting**: Converts dateTime to mm/dd/yy format
4. **Fee Processing**: Removes quotes from feeAmount and converts to number
5. **Fee Operations**: For FEE operations, moves feeAmount → assetAmount and feeAsset → assetTicker
6. **Negative Values**: Converts WITHDRAW and SELL operations to negative values
7. **Wallet Lookup**: Populates "Wallet" column by matching walletId against built-in wallet lookup table
8. **WalletId Removal**: Deletes the walletId column after populating Wallet names
9. **Transaction Sorting**: Sorts transactions with oldest at the top
10. **Transaction Grouping**: Groups by parenttransactionId and inserts blank rows between different transactions
11. **Column Renaming**: 
   - assetvalueInBaseCurrency → USD Value
   - assetAmount → Token Amount
   - parenttransactionId → Transaction ID
12. **Column Reordering**: Organizes columns in optimal reading order

## Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Local Installation

1. Install required packages:

```bash
pip install streamlit pandas
```

2. Run the application:

```bash
streamlit run crypto_transaction_processor.py
```

3. Open your browser to the URL displayed (typically `http://localhost:8501`)

## Deployment

### Streamlit Cloud (Recommended)

1. Push your code to a GitHub repository
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Click "New app"
4. Select your repository, branch, and main file path
5. Click "Deploy"

### Other Deployment Options

- **Heroku**: Follow [Streamlit's Heroku deployment guide](https://docs.streamlit.io/knowledge-base/tutorials/deploy/heroku)
- **AWS/GCP/Azure**: Deploy using container services or compute instances
- **Docker**: Create a Dockerfile and deploy to any container platform

## Usage

1. **Upload File**: Click the "Upload CSV File" button and select your transaction export
2. **Review Data**: The app will display:
   - Original data summary
   - Processed data preview
   - Transaction statistics
3. **Download**: Click "Download Processed CSV" to save the formatted file

## File Format

### Input CSV Format

Your input CSV should contain these columns:
- parenttransactionId
- dateTime
- operation
- assetTicker
- assetAmount
- assetvalueInBaseCurrency
- feeAmount
- feeAsset
- fromAddress
- toAddress
- categorizationStatus
- (and other Bitwave export columns)

### Output CSV Format

The processed CSV will have these columns in order:
1. dateTime (mm/dd/yy format)
2. Wallet (populated from wallet lookup table)
3. Transaction ID
4. operation
5. assetTicker
6. Token Amount
7. USD Value
8. fromAddress
9. toAddress

Note: The walletId column is used for the lookup but is removed from the final output.

## Example

**Before Processing:**
```csv
dateTime,operation,assetAmount,assetvalueInBaseCurrency,categorizationStatus,walletId
2025-10-29T03:00:05.000Z,WITHDRAW,100,200,Uncategorized,nv6cqu6esAEqzXQSzTI6
```

**After Processing:**
```csv
dateTime,Wallet,Transaction ID,operation,assetTicker,Token Amount,USD Value,fromAddress,toAddress
10/29/25,FB - Working Capital - SOL Wallet 1 (nbEB),TX123,WITHDRAW,SOL,-100,-200,ABC...,XYZ...
```

The Wallet column is automatically populated by matching the walletId from your CSV against a built-in lookup table of 280+ wallet names. Transactions are sorted with oldest dates at the top.

## Notes

- The **Wallet column** is automatically populated using a built-in lookup table with 280+ wallet IDs and names
- The **walletId column** is used for matching but is removed from the final output
- Blank rows are inserted between different Transaction IDs for easier reading
- WITHDRAW and SELL operations are automatically converted to negative values
- FEE operations merge fee data into the main transaction columns

## Troubleshooting

**Issue**: File won't upload
- **Solution**: Ensure file is in CSV format and not corrupted

**Issue**: Processing errors
- **Solution**: Verify your CSV has the required column headers

**Issue**: Missing data in output
- **Solution**: Check that your input file has "Uncategorized" status rows

## Support

For issues or questions, please refer to the Streamlit documentation at [docs.streamlit.io](https://docs.streamlit.io)

## Version

Version: 1.0.0  
Last Updated: November 2025
