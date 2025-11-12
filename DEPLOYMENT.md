# Quick Deployment Guide for Streamlit Cloud

## Step-by-Step Instructions

### 1. Create a GitHub Repository

1. Go to [github.com](https://github.com)
2. Click the "+" icon in the top right → "New repository"
3. Name it something like `crypto-transaction-processor`
4. Set to Public or Private
5. Click "Create repository"

### 2. Upload Your Files

Upload these files to your GitHub repository:
- `crypto_transaction_processor.py` (main application)
- `requirements.txt` (dependencies)
- `README.md` (documentation)

You can either:
- Use GitHub's web interface to upload files
- Or use git commands:
  ```bash
  git clone https://github.com/yourusername/crypto-transaction-processor.git
  cd crypto-transaction-processor
  # Copy your files here
  git add .
  git commit -m "Initial commit"
  git push
  ```

### 3. Deploy to Streamlit Cloud

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Sign in with your GitHub account
3. Click "New app"
4. Fill in the form:
   - **Repository**: Select your `crypto-transaction-processor` repo
   - **Branch**: main (or master)
   - **Main file path**: `crypto_transaction_processor.py`
5. Click "Deploy!"

### 4. Wait for Deployment

- The app will take 1-2 minutes to deploy
- You'll see build logs in real-time
- Once complete, you'll get a public URL like: `https://yourappname.streamlit.app`

### 5. Share Your App

- Your app is now live and accessible to anyone with the URL
- You can share this URL with team members or clients
- The app will automatically update when you push changes to GitHub

## Streamlit Cloud Features

✅ **Free tier includes:**
- 1 GB memory
- 2 CPU cores
- Unlimited public apps
- Auto-sleep after inactivity (wakes up on visit)

✅ **Private apps available** with paid plans

## Updating Your App

To update your deployed app:

1. Make changes to your code locally
2. Push changes to GitHub:
   ```bash
   git add .
   git commit -m "Update description"
   git push
   ```
3. Streamlit Cloud will automatically detect changes and redeploy

## Alternative: Local Deployment

If you prefer to run locally:

```bash
# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run crypto_transaction_processor.py
```

The app will open in your browser at `http://localhost:8501`

## Need Help?

- [Streamlit Documentation](https://docs.streamlit.io)
- [Streamlit Community Forum](https://discuss.streamlit.io)
- [Streamlit Cloud Help](https://docs.streamlit.io/streamlit-community-cloud)
