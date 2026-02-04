# Corporate Subsidiary Mapper 🏢

A Streamlit web application for mapping corporate structures and subsidiaries across jurisdictions. Supports both **Companies House (UK)** with free API access and **OpenCorporates (Global)** for international coverage.

## Overview

This tool helps investigators quickly identify corporate relationships and generate Excel reports of company structures. It's designed for tracking corporate influence across European politics by revealing subsidiary networks, shared officer relationships, and group structures.

## Features

### Core Functionality
- **Multi-source search**: Companies House (UK) and OpenCorporates (Global)
- **Relationship mapping**: Identifies subsidiaries and related entities
- **Officer analysis**: Finds group structures through shared directors
- **Excel export**: Formatted reports with hierarchical structure
- **Direct source links**: Clickable URLs to registry profiles

### Excel Reports Include
- Hierarchical company structure with indentation
- Jurisdiction and registration details
- Company status and type
- Relationship/connection type
- Direct links to official sources
- Summary statistics

## Data Sources

### Companies House (UK) - **RECOMMENDED**
- **Status**: Free, requires API key
- **Coverage**: All UK registered companies
- **Data**: Real-time from official UK register
- **API Key**: Free from [Companies House Developer Hub](https://developer.company-information.service.gov.uk/get-started)
- **Rate Limit**: 600 requests/5 minutes
- **Documentation**: [Companies House API Docs](https://developer-specs.company-information.service.gov.uk/)

### OpenCorporates (Global)
- **Status**: Requires paid subscription (~$400/month)
- **Coverage**: 200+ jurisdictions worldwide
- **Data**: Aggregated from multiple registers
- **API Key**: [OpenCorporates Pricing](https://opencorporates.com/info/pricing)
- **Rate Limit**: Varies by plan
- **Documentation**: [OpenCorporates API Reference](https://api.opencorporates.com/documentation/API-Reference)

## Installation

### Prerequisites
- Python 3.8+
- Git
- API key(s) - see Data Sources section above

### Local Setup

1. **Clone repository**:
```bash
git clone https://github.com/yourusername/subsidiary-mapper.git
cd subsidiary-mapper
```

2. **Install dependencies**:
```bash
pip install -r requirements.txt
```

3. **Configure API keys**:

Create `.streamlit/secrets.toml`:
```toml
# For UK companies (RECOMMENDED - it's free!)
COMPANIES_HOUSE_API_KEY = "your_companies_house_key"

# For global coverage (optional - requires paid subscription)
OPENCORPORATES_API_KEY = "your_opencorporates_key"
```

**Get Companies House API key** (free):
1. Go to [Companies House Developer Hub](https://developer.company-information.service.gov.uk/get-started)
2. Register for an account
3. Create an application
4. Copy your API key

4. **Run the application**:
```bash
# Use enhanced version with Companies House support (recommended)
streamlit run subsidiary_mapper_enhanced.py

# Or basic OpenCorporates-only version
streamlit run subsidiary_mapper.py
```

The app will open at `http://localhost:8501`

## Deployment to Streamlit Cloud

### Quick Deploy

1. **Push to GitHub**:
```bash
git init
git add .
git commit -m "Initial commit: subsidiary mapper"
git branch -M main
git remote add origin https://github.com/yourusername/subsidiary-mapper.git
git push -u origin main
```

2. **Deploy on Streamlit Cloud**:
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Click "New app"
   - Select repository: `yourusername/subsidiary-mapper`
   - Main file: `subsidiary_mapper_enhanced.py` (or `subsidiary_mapper.py`)
   - Click "Advanced settings"
   - Add secrets (see below)
   - Click "Deploy"

3. **Configure Secrets** in Streamlit Cloud:
```toml
COMPANIES_HOUSE_API_KEY = "your_key_here"
# Optionally:
OPENCORPORATES_API_KEY = "your_key_here"
```

4. **Your app will be live** at: `https://yourusername-subsidiary-mapper.streamlit.app`

## Usage Guide

### Searching Companies

**For UK companies** (recommended):
1. Select "Companies House (UK)" as data source
2. Enter company name
3. Click "Search"
4. Click "Map" on your target company
5. Wait for officer analysis to complete
6. Download Excel report

**For international companies**:
1. Select "OpenCorporates (Global)"
2. Enter company name
3. Optionally specify jurisdiction (e.g., "us_de", "nl")
4. Requires OpenCorporates API key

### Understanding Results

**Companies House mapping**:
- Level 0: Root company
- Level 1+: Related entities identified through shared officers
- Connection Type: Shows relationship (e.g., "Shared officer: John Smith")

**Note**: Officer-based relationships indicate *potential* group structures but should be verified through official filings or financial statements.

### Common Jurisdiction Codes
- `gb` - United Kingdom
- `us_de` - Delaware, USA
- `us_ca` - California, USA  
- `nl` - Netherlands
- `ie` - Ireland
- `lu` - Luxembourg

[Full list](https://api.opencorporates.com/documentation/API-Reference#jurisdictions)

## API Rate Limits

### Companies House
- **Free tier**: 600 requests per 5 minutes
- **Applies to**: Search, company profiles, officer lookups
- **Handling**: Built-in delays between requests

### OpenCorporates
- **Varies by plan**: 500-5000+ requests/month
- **Status 401**: API key required
- **Status 403**: Rate limit exceeded

## Project Structure

```
subsidiary-mapper/
├── subsidiary_mapper.py          # Basic OpenCorporates version
├── subsidiary_mapper_enhanced.py # Enhanced with Companies House
├── requirements.txt              # Python dependencies
├── .gitignore                   # Git ignore rules
├── README.md                    # This file
└── .streamlit/
    └── secrets.toml             # API keys (not committed)
```

## Technical Details

### Key Functions

**Companies House Integration**:
- `search_companies_house()` - Company name search
- `get_ch_company_profile()` - Full company details
- `get_ch_officers()` - Director/officer list
- `find_related_companies_by_officers()` - Group structure analysis

**OpenCorporates Integration**:
- `search_opencorporates()` - Global company search
- `get_company_details()` - Company profile
- `get_company_network()` - Subsidiary relationships

**Excel Export**:
- `create_excel_export()` - Formatted workbook creation
- Professional styling with headers
- Hierarchical indentation
- Clickable source links

### Error Handling
- API timeout management
- Rate limit detection
- Missing data graceful fallbacks
- Authentication error messages

## Integration with Investigative Platform

This tool complements your other projects:

1. **Campaign Finance Tracker**: Link donations to parent companies
2. **Lobbying Register Tool**: Identify which subsidiaries lobby
3. **EU Procurement**: Map contract winners to corporate groups

**Example workflow**:
1. Find company in lobbying register
2. Map subsidiaries with this tool
3. Check if subsidiaries also appear in:
   - Campaign donations
   - Government contracts
   - Other lobbying registrations

## Limitations & Considerations

### Companies House Approach
- **Relationship inference**: Uses shared officers as proxy for group structure
- **Verification needed**: Official confirmation from filings recommended
- **UK only**: Limited to UK-registered entities
- **Corporate officers**: Best indicator of group relationships

### OpenCorporates Approach  
- **Data completeness**: Varies by jurisdiction
- **Update frequency**: May lag behind official registers
- **Premium required**: Full features need paid subscription
- **Subsidiary data**: Not always available even with API key

### General Notes
- **Complex structures**: Multi-tier groups may require manual research
- **Offshore entities**: Often lack publicly available subsidiary data
- **Holding companies**: May not be linked in public registers
- **Ultimate beneficial owners**: Rarely disclosed in basic company data

## Alternative Data Sources

For comprehensive corporate structure research:

1. **SEC EDGAR** (US companies)
   - Exhibit 21 of 10-K filings lists significant subsidiaries
   - Free access at [sec.gov/edgar](https://www.sec.gov/edgar/search/)

2. **National business registers**
   - Germany: [handelsregister.de](https://www.handelsregister.de/)
   - Netherlands: [kvk.nl](https://www.kvk.nl/)
   - France: [infogreffe.fr](https://www.infogreffe.fr/)

3. **Bloomberg/Refinitiv** (paid)
   - Comprehensive ownership trees
   - Historical changes
   - Beneficial ownership

4. **Company annual reports**
   - Often list major subsidiaries
   - Usually in notes to financial statements

## Future Enhancements

Potential additions:
- [ ] SEC EDGAR exhibit 21 parser
- [ ] Multiple register data merging
- [ ] Ownership percentage tracking
- [ ] Ultimate beneficial owner chains
- [ ] Visual network graphs
- [ ] Historical structure changes
- [ ] Cross-border entity matching
- [ ] Integration with procurement databases

## Troubleshooting

**"API key not configured"**
- Check `.streamlit/secrets.toml` exists and has correct key name
- For Streamlit Cloud: Verify secrets in app settings

**"No related entities found"**
- Company may be standalone
- Officers may use different structures
- Try searching parent company instead

**"Rate limit exceeded"**
- Wait 5 minutes for Companies House reset
- Reduce number of simultaneous searches

**"Search returned no results"**
- Check company name spelling
- Try partial name (e.g., "Google" not "Google LLC")
- Verify jurisdiction code if using

## Contributing

Part of the European Political Influence Platform project.

## License

[Your license]

## Resources

### Documentation
- [Companies House API Guide](https://developer.company-information.service.gov.uk/)
- [OpenCorporates API Docs](https://api.opencorporates.com/documentation/)
- [Streamlit Documentation](https://docs.streamlit.io/)

### Related Tools
- [EU Transparency Register](https://transparency-register.europa.eu/)
- [OpenOwnership](https://www.openownership.org/) - Beneficial ownership data
- [OCCRP Aleph](https://aleph.occrp.org/) - Investigative database

### Background Reading
- [Corporate Structures in Europe](https://www.oecd.org/corporate/) - OECD guidelines
- [Investigative Journalism Manual](https://helpdesk.gijn.org/) - GIJN resources
