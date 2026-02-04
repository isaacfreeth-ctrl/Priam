"""
Corporate Subsidiary Mapper
Uses Companies House API for UK companies.
OpenCorporates support coming soon.
"""

import streamlit as st
import requests
import pandas as pd
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Border, Side
from io import BytesIO
from datetime import datetime
import base64
import time

# =============================================================================
# PAGE CONFIG
# =============================================================================
st.set_page_config(
    page_title="Corporate Subsidiary Mapper",
    page_icon="🏢",
    layout="wide"
)

# =============================================================================
# API CONFIGURATION
# =============================================================================

def get_ch_api_key():
    """Get Companies House API key from secrets."""
    try:
        return st.secrets["COMPANIES_HOUSE_API_KEY"]
    except:
        return None

def ch_headers():
    """Get headers for Companies House API."""
    api_key = get_ch_api_key()
    if api_key:
        # Companies House uses HTTP Basic Auth with API key as username, empty password
        credentials = base64.b64encode(f"{api_key}:".encode()).decode()
        return {"Authorization": f"Basic {credentials}"}
    return {}

# =============================================================================
# COMPANIES HOUSE API FUNCTIONS
# =============================================================================

def search_companies_house(query):
    """Search Companies House for companies."""
    api_key = get_ch_api_key()
    if not api_key:
        st.error("Companies House API key not configured. Add it to Streamlit secrets.")
        return []
    
    try:
        response = requests.get(
            "https://api.company-information.service.gov.uk/search/companies",
            params={"q": query, "items_per_page": 30},
            headers=ch_headers(),
            timeout=30
        )
        
        if response.status_code == 200:
            return response.json().get("items", [])
        elif response.status_code == 401:
            st.error("Invalid Companies House API key. Please check your secrets.")
            return []
        elif response.status_code == 429:
            st.warning("Rate limit reached. Please wait a moment.")
            return []
        else:
            st.error(f"API error: {response.status_code}")
            return []
            
    except requests.exceptions.RequestException as e:
        st.error(f"Request failed: {e}")
        return []


def get_company_details(company_number):
    """Get full company details."""
    try:
        response = requests.get(
            f"https://api.company-information.service.gov.uk/company/{company_number}",
            headers=ch_headers(),
            timeout=30
        )
        if response.status_code == 200:
            return response.json()
        return None
    except:
        return None


def get_company_officers(company_number):
    """Get company officers/directors."""
    try:
        response = requests.get(
            f"https://api.company-information.service.gov.uk/company/{company_number}/officers",
            headers=ch_headers(),
            timeout=30
        )
        if response.status_code == 200:
            return response.json().get("items", [])
        return []
    except:
        return []


def get_company_pscs(company_number):
    """Get Persons with Significant Control."""
    try:
        response = requests.get(
            f"https://api.company-information.service.gov.uk/company/{company_number}/persons-with-significant-control",
            headers=ch_headers(),
            timeout=30
        )
        if response.status_code == 200:
            return response.json().get("items", [])
        return []
    except:
        return []


def search_subsidiaries(company_name):
    """Search for potential subsidiaries by name variations."""
    all_results = []
    seen = set()
    
    # Get the core name (first 1-2 significant words)
    words = [w for w in company_name.upper().split() if w not in 
             ["LIMITED", "LTD", "PLC", "UK", "HOLDINGS", "GROUP", "THE", "AND", "&"]]
    
    search_terms = [company_name]
    if words:
        search_terms.append(words[0])  # Just the main word
        if len(words) > 1:
            search_terms.append(" ".join(words[:2]))  # First two words
    
    progress = st.progress(0)
    status = st.empty()
    
    for i, term in enumerate(search_terms):
        status.text(f"Searching: {term}...")
        progress.progress((i + 1) / len(search_terms))
        
        results = search_companies_house(term)
        
        for company in results:
            number = company.get("company_number", "")
            if number and number not in seen:
                seen.add(number)
                all_results.append(company)
        
        if i < len(search_terms) - 1:
            time.sleep(0.3)  # Rate limiting
    
    progress.empty()
    status.empty()
    
    return all_results


def categorize_entities(entities, parent_name):
    """Categorize entities based on name matching."""
    parent_lower = parent_name.lower()
    
    # Extract key words from parent name
    skip_words = {"limited", "ltd", "plc", "uk", "holdings", "group", "the", "and", "&", "inc", "corp"}
    parent_words = [w for w in parent_lower.split() if w not in skip_words and len(w) > 2]
    
    categories = {
        "likely_subsidiaries": [],
        "related": [],
        "other": []
    }
    
    for entity in entities:
        name = entity.get("title", entity.get("company_name", "")).lower()
        
        # Check for strong match (parent name appears in entity name)
        if parent_lower in name or all(w in name for w in parent_words[:2]):
            categories["likely_subsidiaries"].append(entity)
        # Check for partial match (main keyword appears)
        elif parent_words and parent_words[0] in name:
            categories["related"].append(entity)
        else:
            categories["other"].append(entity)
    
    return categories


def create_excel(company_name, entities, categories):
    """Create Excel report."""
    wb = Workbook()
    
    # Styles
    header_font = Font(bold=True, color="FFFFFF")
    header_fill = PatternFill("solid", fgColor="2F5496")
    border = Border(
        left=Side(style='thin'),
        right=Side(style='thin'),
        top=Side(style='thin'),
        bottom=Side(style='thin')
    )
    
    # --- Summary Sheet ---
    ws = wb.active
    ws.title = "Summary"
    
    ws['A1'] = f"Corporate Structure: {company_name}"
    ws['A1'].font = Font(bold=True, size=14)
    ws['A2'] = f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}"
    ws['A3'] = "Data Source: UK Companies House"
    
    ws['A5'] = "Category"
    ws['B5'] = "Count"
    ws['A5'].font = header_font
    ws['A5'].fill = header_fill
    ws['B5'].font = header_font
    ws['B5'].fill = header_fill
    
    row = 6
    for cat, items in categories.items():
        ws[f'A{row}'] = cat.replace('_', ' ').title()
        ws[f'B{row}'] = len(items)
        row += 1
    
    ws[f'A{row}'] = "TOTAL"
    ws[f'B{row}'] = len(entities)
    ws[f'A{row}'].font = Font(bold=True)
    ws[f'B{row}'].font = Font(bold=True)
    
    ws.column_dimensions['A'].width = 25
    ws.column_dimensions['B'].width = 10
    
    # --- All Entities Sheet ---
    ws2 = wb.create_sheet("All Entities")
    
    headers = ["Company Name", "Company Number", "Status", "Type", "Incorporated", "Address", "Category", "Companies House URL"]
    for col, h in enumerate(headers, 1):
        cell = ws2.cell(row=1, column=col, value=h)
        cell.font = header_font
        cell.fill = header_fill
        cell.border = border
    
    row = 2
    for cat, items in categories.items():
        for e in items:
            company_number = e.get("company_number", "N/A")
            ws2.cell(row=row, column=1, value=e.get("title", e.get("company_name", "N/A")))
            ws2.cell(row=row, column=2, value=company_number)
            ws2.cell(row=row, column=3, value=e.get("company_status", "N/A"))
            ws2.cell(row=row, column=4, value=e.get("company_type", "N/A"))
            ws2.cell(row=row, column=5, value=e.get("date_of_creation", "N/A"))
            
            # Address
            addr = e.get("address", {}) or e.get("registered_office_address", {})
            if isinstance(addr, dict):
                addr_str = ", ".join(filter(None, [
                    addr.get("address_line_1", ""),
                    addr.get("locality", ""),
                    addr.get("postal_code", "")
                ]))
            else:
                addr_str = str(addr) if addr else "N/A"
            ws2.cell(row=row, column=6, value=addr_str)
            
            ws2.cell(row=row, column=7, value=cat.replace('_', ' ').title())
            ws2.cell(row=row, column=8, value=f"https://find-and-update.company-information.service.gov.uk/company/{company_number}")
            
            for col in range(1, 9):
                ws2.cell(row=row, column=col).border = border
            row += 1
    
    # Column widths
    ws2.column_dimensions['A'].width = 50
    ws2.column_dimensions['B'].width = 15
    ws2.column_dimensions['C'].width = 12
    ws2.column_dimensions['D'].width = 20
    ws2.column_dimensions['E'].width = 12
    ws2.column_dimensions['F'].width = 40
    ws2.column_dimensions['G'].width = 20
    ws2.column_dimensions['H'].width = 60
    
    # --- Likely Subsidiaries Sheet ---
    ws3 = wb.create_sheet("Likely Subsidiaries")
    
    headers_sub = ["Company Name", "Company Number", "Status", "Type", "Incorporated"]
    for col, h in enumerate(headers_sub, 1):
        cell = ws3.cell(row=1, column=col, value=h)
        cell.font = header_font
        cell.fill = header_fill
        cell.border = border
    
    row = 2
    for e in categories.get("likely_subsidiaries", []):
        ws3.cell(row=row, column=1, value=e.get("title", e.get("company_name", "N/A")))
        ws3.cell(row=row, column=2, value=e.get("company_number", "N/A"))
        ws3.cell(row=row, column=3, value=e.get("company_status", "N/A"))
        ws3.cell(row=row, column=4, value=e.get("company_type", "N/A"))
        ws3.cell(row=row, column=5, value=e.get("date_of_creation", "N/A"))
        
        for col in range(1, 6):
            ws3.cell(row=row, column=col).border = border
        row += 1
    
    ws3.column_dimensions['A'].width = 50
    ws3.column_dimensions['B'].width = 15
    ws3.column_dimensions['C'].width = 12
    ws3.column_dimensions['D'].width = 20
    ws3.column_dimensions['E'].width = 12
    
    buffer = BytesIO()
    wb.save(buffer)
    buffer.seek(0)
    return buffer


# =============================================================================
# MAIN APP
# =============================================================================

st.title("🏢 Corporate Subsidiary Mapper")
st.markdown("Find UK subsidiaries and related companies using Companies House data")

# Check for API key
if not get_ch_api_key():
    st.error("⚠️ Companies House API key not found!")
    st.markdown("""
    **To fix this:**
    1. Go to your Streamlit Cloud app settings
    2. Click **Secrets**
    3. Add:
    ```
    COMPANIES_HOUSE_API_KEY = "your_api_key_here"
    ```
    4. Save and refresh this page
    """)
    st.stop()

# Sidebar
with st.sidebar:
    st.header("About")
    st.markdown("""
    This tool searches UK Companies House for 
    companies matching your search and identifies
    potential subsidiaries by name patterns.
    
    **Current Coverage:** 🇬🇧 UK only
    
    **Coming Soon:** Global coverage via OpenCorporates
    
    **Note:** Results require manual verification.
    """)
    
    st.markdown("---")
    st.markdown("✅ Companies House API connected")

st.markdown("---")

# Step 1: Search
st.subheader("1. Search for a company")
search_term = st.text_input("Company name:", placeholder="e.g., Google, Tesco, Barclays")

if st.button("🔍 Search", type="primary"):
    if search_term:
        with st.spinner("Searching Companies House..."):
            results = search_companies_house(search_term)
        
        if results:
            st.session_state['search_results'] = results
            st.session_state['search_term'] = search_term
            st.success(f"Found {len(results)} UK companies")
        else:
            st.warning("No UK companies found. Try a different search term.")
            if 'search_results' in st.session_state:
                del st.session_state['search_results']
    else:
        st.warning("Please enter a company name")

# Step 2: Select company
if 'search_results' in st.session_state and st.session_state['search_results']:
    st.markdown("---")
    st.subheader("2. Select a company")
    
    results = st.session_state['search_results']
    
    # Build options
    options = []
    for c in results:
        name = c.get("title", "Unknown")
        status = c.get("company_status", "?")
        number = c.get("company_number", "")
        options.append(f"{name} ({number}) - {status}")
    
    selection = st.selectbox("Choose:", options)
    selected_idx = options.index(selection)
    selected_company = results[selected_idx]
    
    # Show details
    with st.expander("Company details", expanded=True):
        col1, col2 = st.columns(2)
        with col1:
            st.write(f"**Name:** {selected_company.get('title', 'N/A')}")
            st.write(f"**Number:** {selected_company.get('company_number', 'N/A')}")
            st.write(f"**Status:** {selected_company.get('company_status', 'N/A')}")
        with col2:
            st.write(f"**Type:** {selected_company.get('company_type', 'N/A')}")
            st.write(f"**Incorporated:** {selected_company.get('date_of_creation', 'N/A')}")
            
            # Link to Companies House
            number = selected_company.get('company_number', '')
            if number:
                st.markdown(f"[View on Companies House](https://find-and-update.company-information.service.gov.uk/company/{number})")
    
    # Step 3: Map
    st.markdown("---")
    st.subheader("3. Map subsidiaries")
    
    if st.button("🗺️ Map Subsidiaries", type="primary"):
        company_name = selected_company.get("title", "")
        
        with st.spinner(f"Finding related companies for '{company_name}'..."):
            entities = search_subsidiaries(company_name)
            categories = categorize_entities(entities, company_name)
        
        st.session_state['mapping_results'] = {
            'company_name': company_name,
            'entities': entities,
            'categories': categories
        }

# Step 4: Results
if 'mapping_results' in st.session_state and st.session_state['mapping_results']:
    st.markdown("---")
    st.subheader("4. Results")
    
    data = st.session_state['mapping_results']
    company_name = data['company_name']
    entities = data['entities']
    categories = data['categories']
    
    st.success(f"Found {len(entities)} related UK entities for **{company_name}**")
    
    # Metrics
    col1, col2, col3 = st.columns(3)
    col1.metric("Likely Subsidiaries", len(categories['likely_subsidiaries']))
    col2.metric("Related", len(categories['related']))
    col3.metric("Other Matches", len(categories['other']))
    
    # Results tabs
    tab1, tab2, tab3 = st.tabs(["Likely Subsidiaries", "Related", "All Entities"])
    
    with tab1:
        subs = categories['likely_subsidiaries']
        if subs:
            for e in subs:
                name = e.get("title", e.get("company_name", "N/A"))
                number = e.get("company_number", "")
                status = e.get("company_status", "")
                st.write(f"**{name}**")
                st.caption(f"{number} | {status} | [View](https://find-and-update.company-information.service.gov.uk/company/{number})")
        else:
            st.info("No clear subsidiaries identified by name matching. Check 'Related' or 'All Entities'.")
    
    with tab2:
        related = categories['related']
        if related:
            for e in related:
                name = e.get("title", e.get("company_name", "N/A"))
                number = e.get("company_number", "")
                status = e.get("company_status", "")
                st.write(f"**{name}**")
                st.caption(f"{number} | {status} | [View](https://find-and-update.company-information.service.gov.uk/company/{number})")
        else:
            st.info("No related companies found.")
    
    with tab3:
        df = pd.DataFrame([{
            'Name': e.get("title", e.get("company_name", "")),
            'Number': e.get("company_number", ""),
            'Status': e.get("company_status", ""),
            'Type': e.get("company_type", ""),
            'Incorporated': e.get("date_of_creation", "")
        } for e in entities])
        st.dataframe(df, use_container_width=True)
    
    # Export
    st.markdown("---")
    st.subheader("5. Export")
    
    excel_data = create_excel(company_name, entities, categories)
    safe_name = "".join(c if c.isalnum() or c in " -_" else "_" for c in company_name)
    filename = f"{safe_name}_uk_subsidiaries.xlsx"
    
    st.download_button(
        "📥 Download Excel Report",
        data=excel_data,
        file_name=filename,
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

# Footer
st.markdown("---")
st.caption("Data: UK Companies House | Subsidiary identification by name matching - verify manually")
