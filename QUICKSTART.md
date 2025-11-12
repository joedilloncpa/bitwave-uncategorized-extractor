# Quick Start Guide

## 🚀 Get Started in 3 Steps

### Step 1: Deploy to Streamlit Cloud
1. Upload all files to a GitHub repository
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your repo and deploy

**OR Run Locally:**
```bash
pip install -r requirements.txt
streamlit run crypto_transaction_processor.py
```

### Step 2: Upload Your CSV
- Click "Upload CSV File" in the app
- Select your Bitwave transaction export
- Must have "Uncategorized" transactions

### Step 3: Download Processed File
- Review the processed data preview
- Check transaction statistics
- Click "Download Processed CSV"

## 📁 Files Included

| File | Purpose |
|------|---------|
| `crypto_transaction_processor.py` | Main Streamlit application |
| `requirements.txt` | Python dependencies |
| `README.md` | Full documentation |
| `DEPLOYMENT.md` | Deployment instructions |
| `gitignore.txt` | Git ignore file (rename to `.gitignore`) |
| `sample_processed_output.csv` | Example output from your sample data |

## 🔄 What the App Does

✅ Filters for "Uncategorized" transactions  
✅ Removes unnecessary columns  
✅ Formats dates to dd/mm/yy  
✅ Processes FEE operations  
✅ Converts WITHDRAW/SELL to negative values  
✅ Adds blank "Wallet" column  
✅ Groups by Transaction ID with blank row separators  
✅ Reorders columns for easy reading  

## 📊 Sample Output

Your sample file had:
- **41 rows** → processed to **65 rows** (with blank separators)
- **25 unique transactions**
- All operations correctly formatted
- Negative values applied to WITHDRAW operations
- FEE operations properly consolidated

## 💡 Next Steps

1. **Populate Wallet Column**: You mentioned you'll provide instructions for this later
2. **Customize**: Modify the app as needed for your workflow
3. **Share**: Give the URL to team members who need to process transactions

## 🆘 Support

- See `README.md` for detailed documentation
- See `DEPLOYMENT.md` for deployment help
- Check Streamlit docs at [docs.streamlit.io](https://docs.streamlit.io)

---

**Ready to go!** Start by deploying the app or running it locally.
