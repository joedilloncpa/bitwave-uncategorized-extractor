import streamlit as st
import pandas as pd
from datetime import datetime
import io

def process_crypto_transactions(df):
    """
    Process cryptocurrency transactions according to specified rules
    """
    # Filter for only "Uncategorized" rows
    df = df[df['categorizationStatus'] == 'Uncategorized'].copy()
    
    # Delete specified columns (removed walletId from the list)
    columns_to_delete = [
        'categorizationStatus', 'ordID', 'runId', 'dateTimeSEC', 
        'assetbitwaveId', 'exchangeRateSource', 'exchangeRate', 
        'reconciliationStatus', 'contactId', 'categoryId', 
        'description', 'transactionMetadata', 'linetransactionId',
        'orgId'
    ]
    
    # Only delete columns that exist in the dataframe
    columns_to_delete = [col for col in columns_to_delete if col in df.columns]
    df = df.drop(columns=columns_to_delete)
    
    # Convert dateTime to mm/dd/yy format
    df['dateTime'] = pd.to_datetime(df['dateTime']).dt.strftime('%m/%d/%y')
    
    # Process feeAmount column - remove quotes and convert to number
    if 'feeAmount' in df.columns:
        df['feeAmount'] = df['feeAmount'].astype(str).str.replace('"', '').replace('', '0')
        df['feeAmount'] = pd.to_numeric(df['feeAmount'], errors='coerce').fillna(0)
    
    # Process FEE operations - move feeAmount to assetAmount and feeAsset to assetTicker
    fee_mask = df['operation'] == 'FEE'
    if fee_mask.any():
        df.loc[fee_mask, 'assetAmount'] = df.loc[fee_mask, 'feeAmount']
        df.loc[fee_mask, 'assetTicker'] = df.loc[fee_mask, 'feeAsset']
    
    # Delete feeAmount and feeAsset columns after processing
    if 'feeAmount' in df.columns:
        df = df.drop(columns=['feeAmount'])
    if 'feeAsset' in df.columns:
        df = df.drop(columns=['feeAsset'])
    
    # Convert WITHDRAW and SELL operations to negative values
    withdraw_sell_mask = df['operation'].isin(['WITHDRAW', 'SELL'])
    if withdraw_sell_mask.any():
        # Only convert positive values to negative (don't reverse already negative values)
        df.loc[withdraw_sell_mask & (df['assetAmount'] > 0), 'assetAmount'] = -df.loc[withdraw_sell_mask & (df['assetAmount'] > 0), 'assetAmount']
        df.loc[withdraw_sell_mask & (df['assetvalueInBaseCurrency'] > 0), 'assetvalueInBaseCurrency'] = -df.loc[withdraw_sell_mask & (df['assetvalueInBaseCurrency'] > 0), 'assetvalueInBaseCurrency']
    
    # Insert Wallet column (empty for now - user will populate)
    df.insert(0, 'Wallet', '')
    
    # Rename columns
    df = df.rename(columns={
        'assetvalueInBaseCurrency': 'USD Value',
        'assetAmount': 'Token Amount',
        'parenttransactionId': 'Transaction ID'
    })
    
    # Sort by Transaction ID (oldest first - ascending by dateTime, then by Transaction ID)
    df['dateTime_sort'] = pd.to_datetime(df['dateTime'], format='%m/%d/%y')
    df = df.sort_values(['dateTime_sort', 'Transaction ID'])
    df = df.drop(columns=['dateTime_sort'])
    
    # Insert blank rows between different Transaction IDs
    result_rows = []
    prev_transaction_id = None
    
    for idx, row in df.iterrows():
        current_transaction_id = row['Transaction ID']
        
        # Add blank row if transaction ID changes (except for the first row)
        if prev_transaction_id is not None and current_transaction_id != prev_transaction_id:
            # Create a blank row with same columns
            blank_row = pd.Series(['' for _ in range(len(row))], index=row.index)
            result_rows.append(blank_row)
        
        result_rows.append(row)
        prev_transaction_id = current_transaction_id
    
    # Create new dataframe from rows
    df = pd.DataFrame(result_rows)
    
    # Reorder columns to specified order
    column_order = [
        'dateTime', 'walletId', 'Wallet', 'Transaction ID', 'operation', 
        'assetTicker', 'Token Amount', 'USD Value', 
        'fromAddress', 'toAddress'
    ]
    
    # Only include columns that exist in the dataframe
    column_order = [col for col in column_order if col in df.columns]
    
    # Add any remaining columns not in the specified order
    remaining_cols = [col for col in df.columns if col not in column_order]
    final_column_order = column_order + remaining_cols
    
    df = df[final_column_order]
    
    # Reset index
    df = df.reset_index(drop=True)
    
    return df

# Streamlit App
st.set_page_config(page_title="Crypto Transaction Processor", page_icon="💰", layout="wide")

st.title("🔄 Cryptocurrency Transaction Processor")
st.markdown("---")

st.markdown("""
### Instructions:
1. Upload your CSV file containing cryptocurrency transaction data
2. The app will automatically process the data according to predefined rules
3. Review the processed data in the preview below
4. Download the processed CSV file

### Processing Steps:
- Filters for "Uncategorized" transactions only
- Removes unnecessary columns (keeps walletId)
- Converts dates to mm/dd/yy format
- Processes FEE operations
- Converts WITHDRAW/SELL amounts to negative values
- Adds a "Wallet" column for manual population
- Groups transactions by Transaction ID with blank row separators
- Sorts with oldest transactions at the top
- Reorders columns for optimal readability
""")

st.markdown("---")

# File uploader
uploaded_file = st.file_uploader("Upload CSV File", type=['csv'])

if uploaded_file is not None:
    try:
        # Read the CSV file
        df = pd.read_csv(uploaded_file)
        
        st.success(f"✅ File uploaded successfully! Found {len(df)} total rows.")
        
        # Show original data summary
        with st.expander("📊 Original Data Summary"):
            st.write(f"**Total Rows:** {len(df)}")
            st.write(f"**Columns:** {', '.join(df.columns.tolist())}")
            uncategorized_count = len(df[df['categorizationStatus'] == 'Uncategorized'])
            st.write(f"**Uncategorized Rows:** {uncategorized_count}")
        
        # Process the data
        with st.spinner("Processing transactions..."):
            processed_df = process_crypto_transactions(df)
        
        st.success(f"✅ Processing complete! {len(processed_df)} rows in processed file (including blank separators).")
        
        # Display processed data
        st.markdown("### 📋 Processed Data Preview")
        st.dataframe(processed_df, use_container_width=True, height=400)
        
        # Prepare download
        csv_buffer = io.StringIO()
        processed_df.to_csv(csv_buffer, index=False)
        csv_data = csv_buffer.getvalue()
        
        # Download button
        st.markdown("---")
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.download_button(
                label="⬇️ Download Processed CSV",
                data=csv_data,
                file_name=f"processed_transactions_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv",
                use_container_width=True
            )
        
        # Show statistics
        st.markdown("---")
        st.markdown("### 📈 Transaction Statistics")
        col1, col2, col3, col4 = st.columns(4)
        
        # Filter out blank rows for statistics
        stats_df = processed_df[processed_df['Transaction ID'] != ''].copy()
        
        with col1:
            unique_transactions = stats_df['Transaction ID'].nunique()
            st.metric("Unique Transactions", unique_transactions)
        
        with col2:
            operation_counts = stats_df['operation'].value_counts()
            st.metric("Most Common Operation", 
                     f"{operation_counts.index[0]} ({operation_counts.values[0]})" if len(operation_counts) > 0 else "N/A")
        
        with col3:
            total_usd = stats_df['USD Value'].sum()
            st.metric("Total USD Value", f"${total_usd:,.2f}")
        
        with col4:
            unique_assets = stats_df['assetTicker'].nunique()
            st.metric("Unique Assets", unique_assets)
        
    except Exception as e:
        st.error(f"❌ Error processing file: {str(e)}")
        st.exception(e)

else:
    st.info("👆 Please upload a CSV file to begin processing.")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: gray;'>
    <small>Crypto Transaction Processor | Built with Streamlit</small>
</div>
""", unsafe_allow_html=True)
