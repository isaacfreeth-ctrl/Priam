# Subsidiary Mapper - Quick Start Guide

## 🎯 What You Have

Two versions of the subsidiary mapper tool:

1. **subsidiary_mapper_enhanced.py** (RECOMMENDED)
   - Supports Companies House (UK) - FREE API
   - Supports OpenCorporates (Global) - Paid API
   - Uses officer analysis to find group structures
   - More comprehensive for UK entities

2. **subsidiary_mapper.py** (Basic)
   - OpenCorporates only
   - Requires paid API subscription
   - Global coverage

## ⚡ Quick Deploy to Streamlit Cloud

### Step 1: Get a FREE Companies House API Key (5 minutes)

1. Go to https://developer.company-information.service.gov.uk/get-started
2. Click "Register"
3. Fill in your details
4. Confirm your email
5. Create an application
6. Copy your API key (looks like: `abc123def456-abc123def456-abc123def456`)

### Step 2: Push to GitHub (2 minutes)

```bash
cd /path/to/your/folder
git init
git add .
git commit -m "Initial commit: subsidiary mapper"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/subsidiary-mapper.git
git push -u origin main
```

### Step 3: Deploy to Streamlit Cloud (3 minutes)

1. Go to https://share.streamlit.io
2. Sign in with GitHub
3. Click "New app"
4. Select your repo: `YOUR_USERNAME/subsidiary-mapper`
5. Main file: **subsidiary_mapper_enhanced.py**
6. Click "Advanced settings"
7. In "Secrets" section, paste:
```toml
COMPANIES_HOUSE_API_KEY = "your_api_key_here"
```
8. Click "Deploy"

**Your app will be live in ~2 minutes!**

## 🔧 Local Testing (Optional)

```bash
# Install dependencies
pip install -r requirements.txt

# Create secrets file
mkdir .streamlit
cat > .streamlit/secrets.toml << EOF
COMPANIES_HOUSE_API_KEY = "your_key_here"
EOF

# Run locally
streamlit run subsidiary_mapper_enhanced.py
```

## 📊 How to Use

1. **Search for a company**
   - Enter name in sidebar (e.g., "Tesco", "BP", "HSBC")
   - Click "Search"

2. **Map the structure**
   - Click "Map" button on your target company
   - Wait 10-30 seconds for officer analysis
   - View related entities

3. **Download Excel report**
   - Click "Download Excel Report"
   - Opens in Excel with:
     - Corporate Structure sheet
     - Summary statistics
     - Clickable links to sources

## 💡 Tips

**For UK companies:**
- Use Companies House source (free!)
- Results show related entities via shared officers
- Best for publicly traded and large private companies

**Understanding the results:**
- Level 0 = Your searched company (root)
- Level 1 = Related entities
- "Connection Type" shows relationship (e.g., shared director)

**Verification:**
- Officer-based relationships indicate *potential* group membership
- Always verify with official filings for critical investigations
- Check company annual reports for confirmed subsidiaries

## 🎯 Integration Ideas

Use this with your other tools:

1. **Find company in lobbying register** → Map subsidiaries → Check if subsidiaries also lobby
2. **See political donation** → Map company group → Check for multiple donations from group
3. **See procurement contract** → Map winner's structure → Identify all contracts to group

## ⚠️ Important Notes

**Companies House API:**
- FREE with no credit card required
- 600 requests per 5 minutes (very generous)
- UK companies only
- Real-time official data

**OpenCorporates API:**
- Requires paid subscription (~$400/month)
- Global coverage
- Not required if focusing on UK

## 🐛 Troubleshooting

**"No API key configured"**
- Check `.streamlit/secrets.toml` has correct format
- Key name must be exactly `COMPANIES_HOUSE_API_KEY`
- No spaces in TOML file

**"No related entities found"**
- Company might be standalone
- Try searching the parent company instead
- Some groups use different officer structures

**App not loading on Streamlit Cloud**
- Check secrets are saved in app settings
- Verify file name is `subsidiary_mapper_enhanced.py`
- Check app logs for errors

## 📚 Next Steps

1. Deploy to Streamlit Cloud
2. Test with a few known UK companies
3. Export some Excel reports
4. Integrate findings with your lobbying/donation trackers
5. Document any interesting corporate structures you discover

## 🔗 Useful Links

- [Companies House Developer Hub](https://developer.company-information.service.gov.uk/)
- [Companies House Search](https://find-and-update.company-information.service.gov.uk/)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [Your GitHub Repo](https://github.com/YOUR_USERNAME/subsidiary-mapper)

---

**Questions?** Check the full README.md for detailed documentation.
