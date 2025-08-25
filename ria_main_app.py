import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
import time

# Page config
st.set_page_config(
    page_title="AURA Platform",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for professional styling with responsive design and dark mode support
st.markdown("""
<style>
    /* CSS Variables for Light and Dark Mode */
    :root {
        --bg-primary: #ffffff;
        --bg-secondary: #f8fafc;
        --text-primary: #1e293b;
        --text-secondary: #64748b;
        --border-color: #e2e8f0;
        --card-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        --card-hover-shadow: 0 12px 24px rgba(0, 0, 0, 0.15);
    }
    
    @media (prefers-color-scheme: dark) {
        :root {
            --bg-primary: #1e293b;
            --bg-secondary: #334155;
            --text-primary: #f1f5f9;
            --text-secondary: #cbd5e1;
            --border-color: #475569;
            --card-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.3);
            --card-hover-shadow: 0 12px 24px rgba(0, 0, 0, 0.4);
        }
    }
    
    .stApp {
        background-color: var(--bg-secondary);
        color: var(--text-primary);
    }
    
    /* Sticky Header */
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.2rem 2rem;
        border-radius: 16px;
        color: white;
        margin-bottom: 2rem;
        box-shadow: 0 8px 32px rgba(102, 126, 234, 0.25);
        display: flex;
        align-items: center;
        justify-content: space-between;
    }
    
    .logo-section {
        display: flex;
        align-items: center;
        gap: 1rem;
        font-size: 2.2rem;
        font-weight: 800;
    }
    
    .header-fullform {
        font-size: 1.4rem;
        font-weight: 600;
        opacity: 0.95;
    }
    
    /* Responsive Header */
    @media (max-width: 768px) {
        .main-header {
            flex-direction: column;
            text-align: center;
            gap: 0.5rem;
            padding: 1rem;
        }
        
        .logo-section {
            font-size: 1.8rem;
        }
        
        .header-fullform {
            font-size: 1.1rem;
        }
    }
    
    /* Remove sidebar fullform */
    .css-1d391kg p {
        display: none !important;
    }
    
    /* Tool Cards Container - Fixed Layout */
    .tools-section {
        margin-bottom: 3rem;
    }
    
    .tools-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
        gap: 2rem;
        margin-bottom: 2rem;
    }
    
    /* Tool Cards Styling - Improved */
    .tool-card-container {
        background: var(--bg-primary);
        border: 2px solid var(--border-color);
        border-radius: 16px;
        padding: 2rem;
        box-shadow: var(--card-shadow);
        transition: all 0.3s ease;
        cursor: pointer;
        height: 100%;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        min-height: 420px;
        position: relative;
        overflow: hidden;
    }
    
    .tool-card-container:hover {
        transform: translateY(-6px);
        box-shadow: var(--card-hover-shadow);
        border-color: #667eea;
    }
    
    .tool-card-icon {
        font-size: 3.5rem;
        margin-bottom: 1.5rem;
        display: block;
        text-align: center;
    }
    
    .tool-card-title {
        font-size: 1.6rem;
        font-weight: 700;
        margin-bottom: 0.75rem;
        color: var(--text-primary);
        text-align: center;
    }
    
    .tool-card-subtitle {
        font-weight: 600;
        color: var(--text-secondary);
        margin-bottom: 1.5rem;
        font-size: 1rem;
        text-align: center;
    }
    
    .tool-card-description {
        color: var(--text-secondary);
        line-height: 1.6;
        margin-bottom: 1.5rem;
        flex-grow: 1;
        text-align: center;
    }
    
    .tool-card-features {
        list-style: none;
        padding: 0;
        margin: 0;
    }
    
    .tool-card-features li {
        margin: 0.75rem 0;
        color: var(--text-secondary);
        padding-left: 0.5rem;
        text-align: left;
    }
    
    /* Color coding for different tools */
    .ria-card {
        border-left: 6px solid #dc2626;
    }
    .ria-card .tool-card-title {
        color: #dc2626;
    }
    
    .rise-card {
        border-left: 6px solid #f59e0b;
    }
    .rise-card .tool-card-title {
        color: #f59e0b;
    }
    
    .prism-card {
        border-left: 6px solid #16a34a;
    }
    .prism-card .tool-card-title {
        color: #16a34a;
    }
    
    /* Button Styling for Cards */
    .tool-launch-btn {
        margin-top: 1rem;
        width: 100%;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 0.75rem 1rem;
        border-radius: 8px;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    
    .tool-launch-btn:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
    }
    
    /* Section styling */
    .section-header {
        background: var(--bg-primary);
        border: 1px solid var(--border-color);
        border-radius: 12px;
        padding: 1.5rem;
        margin: 2rem 0 1.5rem 0;
        border-left: 4px solid #667eea;
        box-shadow: var(--card-shadow);
    }
    
    .section-header h3 {
        margin: 0;
        color: var(--text-primary);
    }
    
    .section-header p {
        margin: 0.5rem 0 0 0;
        color: var(--text-secondary);
    }
    
    /* Activity and Alerts styling */
    .activity-section, .alerts-section {
        background: var(--bg-primary);
        border-radius: 12px;
        padding: 1.5rem;
        box-shadow: var(--card-shadow);
        border: 1px solid var(--border-color);
        margin-bottom: 2rem;
    }
    
    .section-title {
        font-size: 1.3rem;
        font-weight: 700;
        color: var(--text-primary);
        margin-bottom: 1rem;
    }
    
    .activity-item {
        background: var(--bg-secondary);
        border-radius: 8px;
        padding: 1rem;
        margin: 0.5rem 0;
        display: flex;
        justify-content: space-between;
        align-items: center;
        border: 1px solid var(--border-color);
    }
    
    .alert-item {
        border-radius: 8px;
        padding: 1rem;
        margin: 0.5rem 0;
        border-left: 4px solid;
    }
    
    .alert-high {
        background: linear-gradient(135deg, #fef2f2, #fee2e2);
        border-color: #dc2626;
        color: #7f1d1d;
    }
    
    .alert-medium {
        background: linear-gradient(135deg, #fffbeb, #fef3c7);
        border-color: #f59e0b;
        color: #78350f;
    }
    
    @media (prefers-color-scheme: dark) {
        .alert-high {
            background: #1f1717;
            color: #fca5a5;
        }
        
        .alert-medium {
            background: #1f1a0d;
            color: #fcd34d;
        }
    }
    
    /* Document sections */
    .document-section {
        background: var(--bg-secondary);
        border: 1px solid var(--border-color);
        border-radius: 8px;
        padding: 1rem;
        margin: 1rem 0;
    }
    
    .highlight-text {
        background-color: #fef08a;
        padding: 0.2rem 0.4rem;
        border-radius: 4px;
        font-weight: 600;
        color: #854d0e;
    }
    
    .diff-added {
        background: #dcfce7;
        border-left: 4px solid #16a34a;
        padding: 0.5rem;
        margin: 0.25rem 0;
        border-radius: 0 6px 6px 0;
    }
    
    .diff-removed {
        background: #fef2f2;
        border-left: 4px solid #dc2626;
        padding: 0.5rem;
        margin: 0.25rem 0;
        border-radius: 0 6px 6px 0;
        text-decoration: line-through;
        opacity: 0.7;
    }
    
    @media (prefers-color-scheme: dark) {
        .highlight-text {
            background-color: #713f12;
            color: #fde68a;
        }
        
        .diff-added {
            background: #14532d;
            color: #bbf7d0;
        }
        
        .diff-removed {
            background: #581c1c;
            color: #fecaca;
        }
    }
    
    /* Lifecycle badges */
    .lifecycle-badge {
        display: inline-block;
        padding: 0.4rem 1rem;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
        color: white;
        margin: 0.25rem;
    }
    
    .rd { background: #8b5cf6; }
    .clinical { background: #3b82f6; }
    .regulatory { background: #dc2626; }
    .pharmacovigilance { background: #ea580c; }
    .cmc { background: #16a34a; }
    .quality { background: #0891b2; }
    .manufacturing { background: #4338ca; }
    .commercial { background: #be123c; }
    .medical { background: #059669; }
    .corporate { background: #374151; }
    
    /* Workflow milestones */
    .milestone {
        background: var(--bg-primary);
        border-left: 4px solid;
        padding: 1rem;
        margin: 0.5rem 0;
        border-radius: 0 8px 8px 0;
        box-shadow: var(--card-shadow);
    }
    
    .milestone-completed {
        border-color: #16a34a;
        background: linear-gradient(135deg, #f0fdf4, #dcfce7);
    }
    
    .milestone-active {
        border-color: #f59e0b;
        background: linear-gradient(135deg, #fffbeb, #fef3c7);
    }
    
    .milestone-pending {
        border-color: #6b7280;
        opacity: 0.8;
    }
    
    @media (prefers-color-scheme: dark) {
        .milestone-completed {
            background: #14532d;
            color: #bbf7d0;
        }
        
        .milestone-active {
            background: #1f1a0d;
            color: #fcd34d;
        }
    }
    
    /* Clear float utility */
    .clearfix::after {
        content: "";
        display: table;
        clear: both;
    }
    
    /* Remove default streamlit spacing */
    .block-container {
        padding-top: 1rem;
        padding-bottom: 0rem;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'current_page' not in st.session_state:
    st.session_state.current_page = 'Home'
if 'ria_nav' not in st.session_state:
    st.session_state.ria_nav = 'Updates Feed'
if 'rise_nav' not in st.session_state:
    st.session_state.rise_nav = 'Active Workflows'
if 'prism_nav' not in st.session_state:
    st.session_state.prism_nav = 'Product Portfolio'
if 'show_source_doc' not in st.session_state:
    st.session_state.show_source_doc = False
if 'show_external_comparison' not in st.session_state:
    st.session_state.show_external_comparison = False
if 'show_ai_document' not in st.session_state:
    st.session_state.show_ai_document = False
if 'show_priority_logic' not in st.session_state:
    st.session_state.show_priority_logic = False

# Sample data
@st.cache_data
def load_sample_data():
    products_data = [
        {
            'id': 'PRD001', 'name': 'CardioX', 'category': 'Clinical Operations and Medical Affairs',
            'therapeutic_area': 'Cardiovascular', 'target_markets': ['US', 'EU', 'Japan'],
            'recent_approvals': ['FDA NDA Approval (2024)', 'EMA MAA Under Review'],
            'variations': ['Labeling Update Q1 2025', 'Manufacturing Site Change']
        },
        {
            'id': 'PRD002', 'name': 'OncoMax', 'category': 'Clinical Operations and Medical Affairs',
            'therapeutic_area': 'Oncology', 'target_markets': ['US', 'EU', 'LATAM'],
            'recent_approvals': ['Phase III Completed', 'FDA Fast Track Designation'],
            'variations': ['Dosing Schedule Optimization', 'Pediatric Indication Study']
        },
        {
            'id': 'PRD003', 'name': 'NeuroHeal', 'category': 'Pharmacovigilance & Drug Safety',
            'therapeutic_area': 'Neurology', 'target_markets': ['US', 'EU', 'India'],
            'recent_approvals': ['EU Approval (2024)', 'US Query Response Submitted'],
            'variations': ['REMS Update', 'Post-Marketing Study Protocol']
        },
        {
            'id': 'PRD004', 'name': 'DiabeSure', 'category': 'Regulatory Affairs',
            'therapeutic_area': 'Endocrinology', 'target_markets': ['US', 'EU', 'China'],
            'recent_approvals': ['US Approval (2023)', 'EU Submission Q4 2024'],
            'variations': ['Price Variation EU', 'New Strength Development']
        },
        {
            'id': 'PRD005', 'name': 'Respira', 'category': 'Manufacturing and Supply Chain',
            'therapeutic_area': 'Respiratory', 'target_markets': ['US', 'EU', 'Middle East'],
            'recent_approvals': ['Generic Pathway Approval', 'Bio-equivalence Study'],
            'variations': ['Manufacturing Scale-up', 'Quality Specification Update']
        }
    ]
    
    workflow_stages = [
        'Pre-Submission', 'Dossier Preparation', 'Submission Assembly and Dispatch',
        'Regulatory Agency Review', 'Approval & Launch', 'Post Approval'
    ]
    
    recent_activities = [
        {'time': '2 hours ago', 'activity': 'FDA guidance document updated for CardioX', 'type': 'regulatory', 'icon': '📋'},
        {'time': '4 hours ago', 'activity': 'OncoMax Phase III data analysis completed', 'type': 'clinical', 'icon': '🧪'},
        {'time': '6 hours ago', 'activity': 'NeuroHeal REMS document approved by team', 'type': 'safety', 'icon': '🛡️'},
        {'time': '1 day ago', 'activity': 'DiabeSure pricing submission to EU authorities', 'type': 'commercial', 'icon': '💼'},
        {'time': '2 days ago', 'activity': 'Respira manufacturing site inspection passed', 'type': 'quality', 'icon': '✅'}
    ]
    
    critical_alerts = [
        {'priority': 'HIGH', 'message': 'FDA requires immediate response for CardioX safety update', 'deadline': '3 days'},
        {'priority': 'MEDIUM', 'message': 'EMA requesting additional OncoMax clinical data', 'deadline': '14 days'},
        {'priority': 'HIGH', 'message': 'DiabeSure labeling changes due to new FDA guidance', 'deadline': '7 days'}
    ]
    
    return products_data, workflow_stages, recent_activities, critical_alerts

# Sidebar navigation
def render_sidebar():
    with st.sidebar:
        st.markdown("""
        <div style="background: linear-gradient(180deg, #667eea 0%, #764ba2 100%); padding: 2rem; border-radius: 16px; margin-bottom: 1.5rem; text-align: center;">
            <div style="font-size: 3rem; margin-bottom: 1rem;">🤖</div>
            <h2 style="color: white; margin: 0; font-size: 2rem; font-weight: 800;">AURA</h2>
        </div>
        """, unsafe_allow_html=True)
        
        pages = ['🏠 Home', '🕵️ RIA Detective', '🧭 RISE Guider', '📚 PRISM Keeper']
        
        for page in pages:
            page_key = page.split(' ', 1)[1]
            if st.button(page, use_container_width=True, key=f"nav_{page_key}"):
                st.session_state.current_page = page_key
                st.rerun()
        
        st.markdown("---")
        
        if st.button("🔔 Notifications", use_container_width=True):
            st.info("Notifications panel opened")
        
        if st.button("⚙️ Settings", use_container_width=True):
            st.info("Settings panel opened")
        
        st.markdown("---")
        
        st.markdown("### 📊 Quick Stats")
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Active Alerts", "15", delta="2")
        with col2:
            st.metric("Products", "142", delta="3")
        
        st.metric("Compliance", "98.2%", delta="0.3%")
        st.metric("On-Time", "94.1%", delta="-1.2%")

# Header component
def render_header(page_title):
    st.markdown("""
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 1.2rem 2rem; border-radius: 16px; color: white; margin-bottom: 2rem; box-shadow: 0 8px 32px rgba(102, 126, 234, 0.25); display: flex; align-items: center; justify-content: space-between;">
        <div style="display: flex; align-items: center; gap: 1rem; font-size: 2.2rem; font-weight: 800;">
            <span>🤖</span>
            <span>AURA</span>
        </div>
        <div style="font-size: 1.4rem; font-weight: 600; opacity: 0.95;">
            Automated Unified Regulatory Assistant
        </div>
    </div>
    """, unsafe_allow_html=True)

# Replace the render_home function's tool cards section with this corrected version:
def render_home():
    render_header("Dashboard")
    
    # Platform Tools Section
    st.markdown("## 🚀 Platform Tools")
    
    # Create three columns for the cards
    col1, col2, col3 = st.columns(3, gap="large")
    
    # RIA Card
    with col1:
        st.markdown("""
        <div class="tool-card-container ria-card">
            <div class="tool-card-icon">🕵️</div>
            <h3 class="tool-card-title">RIA - The Detective</h3>
            <p class="tool-card-subtitle">Regulatory Impact Analyzer</p>
            <p class="tool-card-description">AI-powered monitoring and analysis of regulatory updates, guidelines, and changes across global markets.</p>
            <ul class="tool-card-features">
                <li>📈 Updates Feed</li>
                <li>🔍 Sources Monitoring</li>
                <li>📊 Analytics Dashboard</li>
                <li>🚨 Alert Settings</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    # RISE Card
    with col2:
        st.markdown("""
        <div class="tool-card-container rise-card">
            <div class="tool-card-icon">🧭</div>
            <h3 class="tool-card-title">RISE - The Guide</h3>
            <p class="tool-card-subtitle">Regulatory Integration & Submission Engine</p>
            <p class="tool-card-description">Workflow management and timeline tracking for regulatory submissions and milestone management.</p>
            <ul class="tool-card-features">
                <li>⚡ Active Workflows</li>
                <li>📅 Timeline View</li>
                <li>🔗 Dependencies</li>
                <li>📋 Reports</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    # PRISM Card  
    with col3:
        st.markdown("""
        <div class="tool-card-container prism-card">
            <div class="tool-card-icon">📚</div>
            <h3 class="tool-card-title">PRISM - The Librarian</h3>
            <p class="tool-card-subtitle">Product Regulatory Information & Submission Management</p>
            <p class="tool-card-description">Comprehensive product portfolio and regulatory information management system.</p>
            <ul class="tool-card-features">
                <li>🧬 Product Portfolio</li>
                <li>✅ Approvals & Renewals</li>
                <li>🔄 Variations Tracker</li>
                <li>📊 Compliance Dashboard</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    # Launch buttons in a clean row
    col1, col2, col3 = st.columns(3, gap="large")
    
    with col1:
        if st.button("Launch RIA Detective", use_container_width=True, key="launch_ria", type="primary"):
            st.session_state.current_page = 'RIA Detective'
            st.rerun()
    
    with col2:
        if st.button("Launch RISE Guider", use_container_width=True, key="launch_rise", type="primary"):
            st.session_state.current_page = 'RISE Guider'
            st.rerun()
    
    with col3:
        if st.button("Launch PRISM Keeper", use_container_width=True, key="launch_prism", type="primary"):
            st.session_state.current_page = 'PRISM Keeper'
            st.rerun()
    
    # Add separator before next section
    st.markdown("---")
    
    # Recent activity and critical alerts
    _, _, recent_activities, critical_alerts = load_sample_data()
    
    col1, col2 = st.columns(2, gap="large")
    
    with col1:
        st.markdown("### 📈 Recent Activity")
        with st.container():
            for activity in recent_activities:
                st.markdown(f"""
                    <div class="activity-item">
                        <div>
                            <span>{activity['icon']}</span>
                            <span style="margin-left: 0.5rem;">{activity['activity']}</span>
                        </div>
                        <small style="color: var(--text-secondary);">{activity['time']}</small>
                    </div>
                """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("### 🚨 Critical Alerts")
        with st.container():
            for alert in critical_alerts:
                alert_class = f"alert-{alert['priority'].lower()}"
                
                st.markdown(f"""
                    <div class="alert-item {alert_class}">
                        <div style="display: flex; justify-content: space-between; align-items: flex-start; gap: 1rem;">
                            <div>
                                <div style="font-weight: bold; margin-bottom: 0.5rem;">
                                    ⚠️ {alert['priority']} PRIORITY
                                </div>
                                <div>{alert['message']}</div>
                            </div>
                            <div style="background: rgba(0,0,0,0.1); padding: 0.25rem 0.75rem; border-radius: 12px; font-size: 0.8rem; font-weight: 600; white-space: nowrap;">
                                {alert['deadline']}
                            </div>
                        </div>
                    </div>
                """, unsafe_allow_html=True)
                
# RIA Detective page with fixed document rendering
def render_ria_detective():
    render_header("RIA Detective")
    
    st.markdown("""
    <div class="section-header">
        <h3>🕵️ RIA - Regulatory Impact Analyzer</h3>
        <p>AI-powered regulatory monitoring and impact analysis system</p>
    </div>
    """, unsafe_allow_html=True)
    
    nav_options = ['Updates Feed', 'Sources', 'Analytics', 'Alert Settings']
    cols = st.columns(len(nav_options))
    
    for i, option in enumerate(nav_options):
        with cols[i]:
            if st.button(option, use_container_width=True, key=f"ria_nav_{option}"):
                st.session_state.ria_nav = option
    
    st.markdown("### 🔍 Filters")
    col1, col2, col3, col4, col5 = st.columns([2, 1, 1, 1, 1])
    
    with col1:
        search_query = st.text_input("Search", placeholder="Search regulatory updates...")
    with col2:
        source_filter = st.selectbox("Sources", ["All Sources", "FDA", "EMA", "CDSCO", "PMDA"])
    with col3:
        region_filter = st.selectbox("Regions", ["All Regions", "US", "EU", "India", "Japan"])
    with col4:
        product_filter = st.selectbox("Products", ["All Products", "CardioX", "OncoMax", "NeuroHeal"])
    with col5:
        type_filter = st.selectbox("Types", ["All Types", "Guidance", "Safety", "Labeling", "Manufacturing"])
    
    if st.session_state.ria_nav == 'Updates Feed':
        st.markdown("## 📈 Regulatory Updates")
        
        updates = [
            {
                'id': 'update_1',
                'title': 'FDA Issues New Diabetes Drug Labeling Guidance',
                'source': 'FDA.gov',
                'date': '2025-08-22',
                'priority': 'HIGH',
                'products_affected': ['DiabeSure'],
                'countries': ['US'],
                'summary': 'New labeling requirements for diabetes medications including cardiovascular risk disclosures.',
                'source_url': 'https://www.fda.gov/drugs/guidance-regulation-page/diabetes-labeling-guidance-2025'
            },
            {
                'id': 'update_2',
                'title': 'EMA Updates Cardiovascular Safety Assessment',
                'source': 'EMA.europa.eu',
                'date': '2025-08-21',
                'priority': 'MEDIUM',
                'products_affected': ['CardioX', 'NeuroHeal'],
                'countries': ['EU', 'UK'],
                'summary': 'Updated guidance on cardiovascular safety evaluation for new drug applications.',
                'source_url': 'https://www.ema.europa.eu/en/cardiovascular-safety-assessment-2025'
            }
        ]
        
        for update in updates:
            with st.expander(f"{update['title']} - {update['priority']} Priority"):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown(f"""
                    **Source:** {update['source']}  
                    **Date:** {update['date']}  
                    **Priority:** {update['priority']}  
                    **Products Affected:** {', '.join(update['products_affected'])}
                    """)
                
                with col2:
                    st.markdown(f"""
                    **Applicable Countries:** {', '.join(update['countries'])}  
                    **Not Applicable:** Other regions (analysis shows no impact)  
                    **Timeline:** 30 days for implementation
                    """)
                
                st.markdown(f"**Summary:** {update['summary']}")
                
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    if st.button("📄 Source Document", key=f"source_{update['id']}"):
                        st.session_state.show_source_doc = update['id']
                
                with col2:
                    if st.button("🔄 External Comparison", key=f"compare_{update['id']}"):
                        st.session_state.show_external_comparison = update['id']
                
                with col3:
                    if st.button("🤖 AI Modified Document", key=f"ai_doc_{update['id']}"):
                        st.session_state.show_ai_document = update['id']
                
                with col4:
                    if st.button("⚡ Priority Logic", key=f"priority_{update['id']}"):
                        st.session_state.show_priority_logic = update['id']
                
                # Show source document
                if st.session_state.show_source_doc == update['id']:
                    st.markdown("### 📄 Source Document")
                    st.info(f"**Document URL:** {update['source_url']}")
                    st.markdown("**Document Summary:** This guidance document provides updated requirements for diabetes drug labeling with emphasis on cardiovascular risk assessment and disclosure requirements.")
                
                # Show external comparison using text formatting
                if st.session_state.show_external_comparison == update['id']:
                    st.markdown("### 🔄 External Comparison")
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.markdown("**Current Database Requirements:**")
                        st.markdown("""
                        - Standard diabetes labeling format
                        - Basic efficacy data required
                        - Limited cardiovascular warnings
                        - Standard adverse event reporting
                        """)
                    
                    with col2:
                        st.markdown("**New External Requirements:**")
                        st.markdown("""
                        - **Enhanced cardiovascular risk section** ⚠️
                        - **Detailed cardiac monitoring protocols** ⚠️
                        - **Patient counseling requirements** ⚠️
                        - **Updated contraindications list** ⚠️
                        """)
                
                # Show AI modified document using safe components
                if st.session_state.show_ai_document == update['id']:
                    st.markdown("### 🤖 AI Modified Document")
                    st.markdown("#### DiabeSure Product Labeling - Updated Version")
                    st.markdown("##### Section 5: WARNINGS AND PRECAUTIONS")
                    
                    # Added content
                    st.success("""
                    **5.1 CARDIOVASCULAR RISK ASSESSMENT (NEW)**  
                    Prior to initiating DiabeSure therapy, conduct comprehensive cardiovascular risk assessment including:
                    - Baseline ECG evaluation
                    - Assessment of cardiovascular risk factors  
                    - Patient history of cardiac events
                    """)
                    
                    # Removed content
                    st.error("""
                    ~~5.1 General Safety Information~~  
                    ~~Standard diabetes medication precautions apply.~~
                    """)
                    
                    # Additional new content
                    st.success("""
                    **5.2 CARDIAC MONITORING REQUIREMENTS (NEW)**  
                    Regular cardiac monitoring is required for patients with:
                    - Pre-existing cardiovascular conditions
                    - Age > 65 years
                    - Multiple cardiovascular risk factors
                    """)
                    
                    st.markdown("##### Section 17: PATIENT COUNSELING INFORMATION")
                    
                    st.success("""
                    **17.3 CARDIOVASCULAR RISK COUNSELING (NEW)**  
                    Inform patients about potential cardiovascular risks and advise to:
                    - Report chest pain, shortness of breath, or palpitations immediately
                    - Maintain regular cardiac monitoring appointments
                    - Understand signs and symptoms of cardiac events
                    """)
                
                # Show priority logic
                if st.session_state.show_priority_logic == update['id']:
                    st.markdown("### ⚡ Priority Determination Logic")
                    st.markdown("**Priority Score: HIGH (85/100)**")
                    
                    st.markdown("**Scoring Factors:**")
                    col1, col2 = st.columns(2)
                    with col1:
                        st.success("- Regulatory Authority Impact: FDA (25/25) ✅")
                        st.success("- Product Impact: DiabeSure directly affected (20/20) ✅")
                        st.success("- Compliance Risk: High non-compliance penalty (15/15) ✅")
                    
                    with col2:
                        st.warning("- Timeline Urgency: 30 days implementation (15/20) ⚠️")
                        st.warning("- Business Impact: Major labeling changes required (20/25) ⚠️")
                    
                    st.info("**Recommendation:** Immediate action required for compliance team")
    
    elif st.session_state.ria_nav == 'Sources':
        st.markdown("## 🔍 Source Monitoring")
        
        sources_data = {
            'Source': ['FDA', 'EMA', 'CDSCO', 'PMDA', 'Health Canada', 'TGA'],
            'Status': ['Active', 'Active', 'Active', 'Active', 'Active', 'Active'],
            'Last Update': ['2 hours ago', '4 hours ago', '1 day ago', '6 hours ago', '8 hours ago', '12 hours ago'],
            'Documents Found': [15, 8, 3, 5, 2, 4]
        }
        
        df = pd.DataFrame(sources_data)
        st.dataframe(df, use_container_width=True)
    
    elif st.session_state.ria_nav == 'Analytics':
        st.markdown("## 📊 Analytics Dashboard")
        
        col1, col2 = st.columns(2)
        
        with col1:
            source_counts = [15, 8, 5, 3, 2, 1]
            sources = ['FDA', 'EMA', 'CDSCO', 'PMDA', 'Health Canada', 'TGA']
            
            fig = px.bar(x=sources, y=source_counts, title="Updates by Source (Last 30 Days)")
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            priorities = ['HIGH', 'MEDIUM', 'LOW']
            priority_counts = [5, 12, 18]
            
            fig = px.pie(values=priority_counts, names=priorities, title="Priority Distribution")
            st.plotly_chart(fig, use_container_width=True)
    
    elif st.session_state.ria_nav == 'Alert Settings':
        st.markdown("## 🚨 Alert Configuration")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### Notification Preferences")
            st.checkbox("Email Notifications", value=True)
            st.checkbox("Teams Integration", value=True)
            st.checkbox("SMS Alerts for Critical", value=False)
            st.selectbox("Notification Frequency", ["Immediate", "Daily Digest", "Weekly Summary"])
        
        with col2:
            st.markdown("### Threshold Settings")
            st.slider("High Priority Threshold", 70, 100, 85)
            st.slider("Medium Priority Threshold", 40, 69, 55)
            st.multiselect("Monitor Sources", ["FDA", "EMA", "CDSCO", "PMDA"], default=["FDA", "EMA"])

# RISE Guider page
def render_rise_guider():
    render_header("RISE Guider")
    
    st.markdown("""
    <div class="section-header">
        <h3>🧭 RISE - Regulatory Integration & Submission Engine</h3>
        <p>Workflow management and regulatory milestone tracking system</p>
    </div>
    """, unsafe_allow_html=True)
    
    nav_options = ['Active Workflows', 'Timeline View', 'Dependencies', 'Reports']
    cols = st.columns(len(nav_options))
    
    for i, option in enumerate(nav_options):
        with cols[i]:
            if st.button(option, use_container_width=True, key=f"rise_nav_{option}"):
                st.session_state.rise_nav = option
    
    products_data, workflow_stages, _, _ = load_sample_data()
    product_names = [p['name'] for p in products_data]
    
    if st.session_state.rise_nav == 'Active Workflows':
        st.markdown("## ⚡ Active Workflows")
        
        col1, col2 = st.columns(2)
        with col1:
            diabesure_index = product_names.index('DiabeSure') if 'DiabeSure' in product_names else 0
            selected_product = st.selectbox("Select Product", product_names, index=diabesure_index)
        with col2:
            selected_region = st.selectbox("Select Region", ["US", "EU", "Japan", "India", "China"])
        
        st.markdown(f"### 📋 Workflow Milestones - {selected_product} ({selected_region})")
        
        current_stage_index = 2
        
        for i, stage in enumerate(workflow_stages):
            if i < current_stage_index:
                status_class = "milestone-completed"
                status_icon = "✅"
                status_text = "Completed"
            elif i == current_stage_index:
                status_class = "milestone-active"
                status_icon = "🔄"
                status_text = "In Progress"
            else:
                status_class = "milestone-pending"
                status_icon = "⏳"
                status_text = "Pending"
            
            ria_impact = ""
            if stage == "Dossier Preparation" and selected_product == "DiabeSure":
                ria_impact = "⚠️ HIGH Priority: FDA labeling changes detected - requires immediate update"
            
            st.markdown(f"""
            <div class="milestone {status_class}">
                <h4>{status_icon} {stage}</h4>
                <p>Status: {status_text}</p>
                {f'<div style="color: #dc2626; font-weight: bold; margin-top: 0.5rem;">{ria_impact}</div>' if ria_impact else ''}
            </div>
            """, unsafe_allow_html=True)
    
    elif st.session_state.rise_nav == 'Timeline View':
        st.markdown("## 📅 Timeline View")
        
        fig = go.Figure()
        
        stages_timeline = [
            {'stage': 'Pre-Submission', 'start': '2025-08-01', 'end': '2025-08-15', 'status': 'completed'},
            {'stage': 'Dossier Preparation', 'start': '2025-08-10', 'end': '2025-09-10', 'status': 'completed'},
            {'stage': 'Submission Assembly', 'start': '2025-09-05', 'end': '2025-09-25', 'status': 'in-progress'},
            {'stage': 'Agency Review', 'start': '2025-09-26', 'end': '2025-12-26', 'status': 'pending'},
            {'stage': 'Approval & Launch', 'start': '2025-12-27', 'end': '2026-02-15', 'status': 'pending'}
        ]
        
        colors = {'completed': '#16a34a', 'in-progress': '#f59e0b', 'pending': '#6b7280'}
        
        for i, stage in enumerate(stages_timeline):
            fig.add_trace(go.Scatter(
                x=[stage['start'], stage['end']],
                y=[i, i],
                mode='lines+markers',
                line=dict(color=colors[stage['status']], width=10),
                name=stage['status'],
                text=stage['stage'],
                hovertemplate=f"<b>{stage['stage']}</b><br>Start: {stage['start']}<br>End: {stage['end']}<extra></extra>"
            ))
        
        fig.update_layout(
            title="Product Regulatory Timeline",
            xaxis_title="Timeline",
            yaxis=dict(tickmode='array', tickvals=list(range(len(stages_timeline))), 
                      ticktext=[s['stage'] for s in stages_timeline]),
            height=400,
            showlegend=False
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    elif st.session_state.rise_nav == 'Dependencies':
        st.markdown("## 🔗 Dependencies Management")
        
        dependencies_data = {
            'Task': ['Dossier Review', 'Translation Services', 'Quality Review', 'Legal Clearance', 'Submission Portal'],
            'Depends On': ['Clinical Data Lock', 'Dossier Completion', 'Manufacturing Data', 'Regulatory Strategy', 'Final Documents'],
            'Status': ['Completed', 'In Progress', 'Pending', 'In Progress', 'Pending'],
            'Due Date': ['2025-08-25', '2025-09-05', '2025-09-10', '2025-09-15', '2025-09-20']
        }
        
        df = pd.DataFrame(dependencies_data)
        st.dataframe(df, use_container_width=True)
    
    elif st.session_state.rise_nav == 'Reports':
        st.markdown("## 📋 Reports")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 📊 Performance Metrics")
            st.metric("On-Time Completion", "94%", delta="2%")
            st.metric("Average Timeline", "180 days", delta="-15 days")
            st.metric("Active Workflows", "12", delta="3")
        
        with col2:
            st.markdown("### 📈 Monthly Progress")
            months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug']
            completions = [5, 8, 6, 10, 7, 9, 11, 8]
            
            fig = px.line(x=months, y=completions, title="Monthly Workflow Completions")
            st.plotly_chart(fig, use_container_width=True)

# PRISM Keeper page
def render_prism_keeper():
    render_header("PRISM Keeper")
    
    st.markdown("""
    <div class="section-header">
        <h3>📚 PRISM - Product Regulatory Information & Submission Management</h3>
        <p>Comprehensive product portfolio and regulatory information management</p>
    </div>
    """, unsafe_allow_html=True)
    
    nav_options = ['Product Portfolio', 'Approvals & Renewals', 'Variations Tracker', 'Compliance Dashboard']
    cols = st.columns(len(nav_options))
    
    for i, option in enumerate(nav_options):
        with cols[i]:
            if st.button(option, use_container_width=True, key=f"prism_nav_{option}"):
                st.session_state.prism_nav = option
    
    products_data, _, _, _ = load_sample_data()
    
    if st.session_state.prism_nav == 'Product Portfolio':
        st.markdown("## 🧬 Product Portfolio")
        
        lifecycle_stages = {
            'R&D': 'rd',
            'Clinical Operations and Medical Affairs': 'clinical',
            'Regulatory Affairs': 'regulatory',
            'Pharmacovigilance & Drug Safety': 'pharmacovigilance',
            'CMC': 'cmc',
            'Quality Management': 'quality',
            'Manufacturing and Supply Chain': 'manufacturing',
            'Commercial & Marketing': 'commercial',
            'Medical Info & Scientific Communications': 'medical',
            'Corporate and Strategic Functions': 'corporate'
        }
        
        grouped_products = {}
        for product in products_data:
            category = product['category']
            if category not in grouped_products:
                grouped_products[category] = []
            grouped_products[category].append(product)
        
        for category, products in grouped_products.items():
            st.markdown(f"### {category}")
            st.markdown(f'<span class="lifecycle-badge {lifecycle_stages.get(category, "corporate")}">{category}</span>', unsafe_allow_html=True)
            
            for product in products:
                with st.expander(f"{product['name']} - {product['therapeutic_area']}"):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.markdown(f"""
                        **Product ID:** {product['id']}  
                        **Therapeutic Area:** {product['therapeutic_area']}  
                        **Target Markets:** {', '.join(product['target_markets'])}
                        """)
                    
                    with col2:
                        st.markdown("**Recent Approvals:**")
                        for approval in product['recent_approvals']:
                            st.markdown(f"• {approval}")
                        
                        st.markdown("**Product Variations:**")
                        for variation in product['variations']:
                            st.markdown(f"• {variation}")
                    
                    if product['name'] == 'DiabeSure':
                        st.markdown("---")
                        st.markdown("### 📄 Document Management")
                        
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            if st.button("📋 Current Document", key=f"current_doc_{product['id']}"):
                                st.session_state[f"show_current_{product['id']}"] = True
                        
                        with col2:
                            if st.button("🤖 AI Updated Document", key=f"ai_updated_doc_{product['id']}"):
                                st.session_state[f"show_ai_updated_{product['id']}"] = True
                        
                        if st.session_state.get(f"show_current_{product['id']}", False):
                            st.markdown("#### 📋 Current DiabeSure Labeling Document")
                            
                            with st.container():
                                st.markdown("##### Section 5: WARNINGS AND PRECAUTIONS")
                                st.info("""
                                **5.1 General Safety Information**  
                                Standard diabetes medication precautions apply. Monitor blood glucose levels regularly.
                                
                                **5.2 Hypoglycemia Risk**  
                                Risk of hypoglycemia, especially when combined with other antidiabetic agents.
                                """)
                                
                                st.markdown("##### Section 17: PATIENT COUNSELING INFORMATION")
                                st.info("""
                                **17.1 General Information**  
                                Inform patients about proper administration and monitoring requirements.
                                
                                **17.2 Side Effects**  
                                Discuss common side effects and when to contact healthcare provider.
                                """)
                        
                        if st.session_state.get(f"show_ai_updated_{product['id']}", False):
                            st.markdown("#### 🤖 AI Updated DiabeSure Labeling Document")
                            
                            with st.container():
                                st.markdown("##### Section 5: WARNINGS AND PRECAUTIONS")
                                
                                st.success("""
                                **5.1 CARDIOVASCULAR RISK ASSESSMENT (UPDATED)**  
                                Prior to initiating DiabeSure therapy, conduct comprehensive cardiovascular risk assessment including baseline ECG evaluation, assessment of cardiovascular risk factors, and patient history of cardiac events.
                                """)
                                
                                st.error("""
                                ~~**5.1 General Safety Information**~~  
                                ~~Standard diabetes medication precautions apply. Monitor blood glucose levels regularly.~~
                                """)
                                
                                st.info("""
                                **5.2 Hypoglycemia Risk**  
                                Risk of hypoglycemia, especially when combined with other antidiabetic agents.
                                """)
                                
                                st.success("""
                                **5.3 CARDIAC MONITORING REQUIREMENTS (NEW)**  
                                Regular cardiac monitoring is required for patients with pre-existing cardiovascular conditions, age > 65 years, or multiple cardiovascular risk factors.
                                """)
                                
                                st.markdown("##### Section 17: PATIENT COUNSELING INFORMATION")
                                
                                st.info("""
                                **17.1 General Information**  
                                Inform patients about proper administration and monitoring requirements.
                                
                                **17.2 Side Effects**  
                                Discuss common side effects and when to contact healthcare provider.
                                """)
                                
                                st.success("""
                                **17.3 CARDIOVASCULAR RISK COUNSELING (NEW)**  
                                Inform patients about potential cardiovascular risks and advise to report chest pain, shortness of breath, or palpitations immediately. Maintain regular cardiac monitoring appointments and understand signs and symptoms of cardiac events.
                                """)
                            
                            col1, col2 = st.columns(2)
                            with col1:
                                if st.button("💾 Accept AI Changes", key=f"accept_changes_{product['id']}", type="primary"):
                                    st.success("✅ AI changes have been accepted and document updated!")
                            with col2:
                                if st.button("❌ Reject Changes", key=f"reject_changes_{product['id']}", type="secondary"):
                                    st.warning("⚠️ AI changes have been rejected. Current document maintained.")
    
    elif st.session_state.prism_nav == 'Approvals & Renewals':
        st.markdown("## ✅ Approvals & Renewals")
        
        approvals_data = {
            'Product': ['CardioX', 'OncoMax', 'NeuroHeal', 'DiabeSure', 'Respira'],
            'Market': ['US', 'EU', 'EU', 'US', 'US'],
            'Type': ['NDA', 'MAA', 'MAA', 'NDA', 'ANDA'],
            'Status': ['Approved', 'Under Review', 'Approved', 'Approved', 'Submitted'],
            'Approval Date': ['2024-12-15', 'TBD', '2024-11-20', '2023-08-10', 'TBD'],
            'Renewal Due': ['2029-12-15', 'N/A', '2029-11-20', '2028-08-10', 'N/A']
        }
        
        df = pd.DataFrame(approvals_data)
        st.dataframe(df, use_container_width=True)
        
        st.markdown("### 📅 Upcoming Renewals")
        renewal_products = ['CardioX (US)', 'NeuroHeal (EU)', 'DiabeSure (US)']
        renewal_dates = ['2029-12-15', '2029-11-20', '2028-08-10']
        
        fig = go.Figure(data=go.Bar(x=renewal_products, y=[5, 5, 3], name='Years Until Renewal'))
        fig.update_layout(title="Years Until Next Renewal", yaxis_title="Years")
        st.plotly_chart(fig, use_container_width=True)
    
    elif st.session_state.prism_nav == 'Variations Tracker':
        st.markdown("## 🔄 Variations Tracker")
        
        variations_data = {
            'Product': ['CardioX', 'OncoMax', 'NeuroHeal', 'DiabeSure', 'Respira'],
            'Variation Type': ['Labeling Update', 'Dosing Schedule', 'REMS Update', 'Price Variation', 'Manufacturing'],
            'Market': ['US', 'EU', 'US', 'EU', 'US'],
            'Status': ['Submitted', 'Planning', 'Approved', 'Under Review', 'Draft'],
            'Submission Date': ['2025-08-01', 'TBD', '2025-07-15', '2025-08-10', 'TBD'],
            'Expected Approval': ['2025-10-01', 'TBD', '2025-08-15', '2025-09-10', 'TBD']
        }
        
        df = pd.DataFrame(variations_data)
        st.dataframe(df, use_container_width=True)
        
        status_counts = df['Status'].value_counts()
        fig = px.pie(values=status_counts.values, names=status_counts.index, title="Variation Status Distribution")
        st.plotly_chart(fig, use_container_width=True)
    
    elif st.session_state.prism_nav == 'Compliance Dashboard':
        st.markdown("## 📊 Compliance Dashboard")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Overall Compliance", "98.2%", delta="0.5%")
        with col2:
            st.metric("On-Time Submissions", "94.1%", delta="-1.2%")
        with col3:
            st.metric("Active Products", "142", delta="3")
        with col4:
            st.metric("Pending Actions", "8", delta="-2")
        
        regions = ['US', 'EU', 'Japan', 'India', 'China']
        compliance_scores = [99.1, 98.5, 97.8, 96.9, 95.2]
        
        fig = go.Figure(data=go.Bar(x=regions, y=compliance_scores, marker_color='#16a34a'))
        fig.update_layout(title="Compliance Score by Region", yaxis_title="Compliance %")
        st.plotly_chart(fig, use_container_width=True)

# Main app routing
def main():
    render_sidebar()
    
    if st.session_state.current_page == 'Home':
        render_home()
    elif st.session_state.current_page == 'RIA Detective':
        render_ria_detective()
    elif st.session_state.current_page == 'RISE Guider':
        render_rise_guider()
    elif st.session_state.current_page == 'PRISM Keeper':
        render_prism_keeper()
    
    # Footer
    st.markdown("---")
    st.markdown(f"""
    <div style="text-align: center; padding: 2rem; background: var(--bg-primary); border-radius: 12px; margin-top: 2rem; border: 1px solid var(--border-color);">
        <p style="margin: 0; color: var(--text-primary); font-weight: 600;">
            🤖 <strong>AURA Platform</strong> | 
            Automated Unified Regulatory Assistant | 
            <a href="https://indegene.com" target="_blank" style="color: #667eea;">Indegene Solutions</a>
        </p>
        <p style="margin: 0.5rem 0 0 0; font-size: 0.9rem; color: var(--text-secondary);">
            Last Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | 
            Version: 3.0.0 | 
            Status: 🟢 All Systems Operational
        </p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
