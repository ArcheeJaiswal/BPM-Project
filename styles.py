"""
========================================================================================
UI Styles & Layout Helper Components
========================================================================================
High-contrast, compact CSS styling for Streamlit:
  - Global base typography, headings, and compact cards
  - High-contrast badges (compliant, violation, info)
  - Result banners (pass, fail)
  - Custom navbar and sidebar card styling
========================================================================================
"""

import streamlit as st


def apply_custom_css():
    """Injects high-contrast custom CSS styling into the Streamlit app."""
    st.markdown("""
    <style>
        /* Global Base */
        .stApp {
            background-color: #F8FAFC !important;
        }
        
        /* Compact typography */
        .stApp, .stApp p, .stApp li, .stApp span, .stApp div,
        .stMarkdown, .stMarkdown p, .stMarkdown li, .stMarkdown span,
        label, td, th {
            color: #0F172A !important;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            font-size: 0.88rem;
        }

        /* Headings */
        h1 {
            color: #1E3A8A !important;
            font-size: 1.35rem !important;
            font-weight: 800 !important;
            margin-bottom: 2px !important;
        }
        h2 {
            color: #1E3A8A !important;
            font-size: 1.15rem !important;
            font-weight: 700 !important;
            margin-bottom: 4px !important;
        }
        h3 {
            color: #1E3A8A !important;
            font-size: 1.0rem !important;
            font-weight: 700 !important;
            margin-top: 10px !important;
            margin-bottom: 6px !important;
        }
        h4 {
            color: #1E3A8A !important;
            font-size: 0.9rem !important;
            font-weight: 700 !important;
            margin-bottom: 4px !important;
        }

        /* Compact Cards */
        .compact-card {
            background-color: #FFFFFF !important;
            border: 1px solid #E2E8F0 !important;
            border-radius: 6px !important;
            padding: 8px 14px !important;
            margin-bottom: 8px !important;
            font-size: 0.86rem !important;
        }

        /* Small Status Badges */
        .badge-compliant {
            display: inline-block;
            padding: 2px 8px;
            background-color: #DCFCE7 !important;
            color: #166534 !important;
            border: 1px solid #86EFAC !important;
            border-radius: 12px;
            font-weight: 700;
            font-size: 0.74rem;
        }

        .badge-violation {
            display: inline-block;
            padding: 2px 8px;
            background-color: #FEE2E2 !important;
            color: #991B1B !important;
            border: 1px solid #FCA5A5 !important;
            border-radius: 12px;
            font-weight: 700;
            font-size: 0.74rem;
        }

        .badge-info {
            display: inline-block;
            padding: 2px 8px;
            background-color: #EFF6FF !important;
            color: #1E40AF !important;
            border: 1px solid #BFDBFE !important;
            border-radius: 4px;
            font-weight: 600;
            font-size: 0.75rem;
        }

        /* Result Banners */
        .banner-pass {
            background-color: #ECFDF5 !important;
            border-left: 4px solid #10B981 !important;
            padding: 8px 12px !important;
            border-radius: 4px !important;
            margin: 6px 0 10px 0 !important;
            font-size: 0.88rem !important;
            color: #065F46 !important;
        }
        
        .banner-fail {
            background-color: #FEF2F2 !important;
            border-left: 4px solid #EF4444 !important;
            padding: 8px 12px !important;
            border-radius: 4px !important;
            margin: 6px 0 10px 0 !important;
            font-size: 0.88rem !important;
            color: #991B1B !important;
        }

        /* Path Row */
        .path-row {
            background-color: #FFFFFF !important;
            border: 1px solid #E2E8F0 !important;
            border-radius: 5px !important;
            padding: 8px 12px !important;
            margin-bottom: 6px !important;
            font-size: 0.84rem !important;
        }

        /* Sidebar Styling */
        section[data-testid="stSidebar"] {
            background-color: #F8FAFC !important;
            border-right: 1.5px solid #CBD5E1 !important;
        }
        section[data-testid="stSidebar"] * {
            color: #0F172A !important;
            font-size: 0.86rem !important;
        }
        section[data-testid="stSidebar"] h3 {
            font-size: 1.05rem !important;
            font-weight: 800 !important;
        }
        section[data-testid="stSidebar"] div[data-baseweb="select"] > div {
            background-color: #FFFFFF !important;
            border: 1.5px solid #94A3B8 !important;
            border-radius: 5px !important;
            min-height: 34px !important;
        }
        section[data-testid="stSidebar"] button {
            background-color: #FFFFFF !important;
            color: #1E40AF !important;
            border: 1.5px solid #94A3B8 !important;
            font-weight: 700 !important;
            border-radius: 5px !important;
        }

        .sidebar-card {
            background-color: #FFFFFF !important;
            border: 1px solid #CBD5E1 !important;
            border-radius: 6px !important;
            padding: 10px 12px !important;
            margin-top: 8px !important;
            margin-bottom: 8px !important;
            font-size: 0.84rem !important;
        }

        /* Table */
        table {
            font-size: 0.82rem !important;
        }
        th, td {
            padding: 5px 8px !important;
        }

        /* Hide Streamlit Deploy and Menu */
        #MainMenu, 
        .stDeployButton, 
        div[data-testid="stDeployButton"], 
        [data-testid="stToolbar"], 
        footer,
        [data-testid="stDecoration"],
        [data-testid="stStatusWidget"] {
            display: none !important;
            visibility: hidden !important;
            height: 0 !important;
            width: 0 !important;
        }

        header[data-testid="stHeader"] {
            background: transparent !important;
            height: 1.2rem !important;
        }

        .block-container {
            padding-top: 1.2rem !important;
            padding-bottom: 2rem !important;
        }

        /* Navbar */
        .custom-navbar {
            display: flex;
            justify-content: space-between;
            align-items: center;
            background-color: #FFFFFF !important;
            border: 1px solid #E2E8F0 !important;
            border-radius: 8px !important;
            padding: 10px 16px !important;
            margin-bottom: 12px !important;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04) !important;
        }
    </style>
    """, unsafe_allow_html=True)

