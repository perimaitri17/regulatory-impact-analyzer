import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
import time

# Page config
st.set_page_config(
    page_title="RIA Platform",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for professional styling
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #1e3a8a 0%, #3b82f6 100%);
        padding: 1.5rem;
        border-radius: 12px;
        color: white;
        text-align: left;
        margin-bottom: 2rem;
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
        display: flex;
        align-items: center;
        gap: 1rem;
    }
    
    .logo-section {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        font-size: 2rem;
        font-weight: bold;
    }
    
    .tool-card {
        background: white;
        border: 1px solid #e5e7eb;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.08);
        transition: all 0.3s ease;
        cursor: pointer;
        height: 350px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }
    
    .tool-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 30px rgba(0, 0, 0, 0.15);
        border-color: #3b82f6;
    }
    
    .tool-card h3 {
        margin-bottom: 1rem;
    }
    
    .tool-card-content {
        flex-grow: 1;
    }
    
    .section-header {
        background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
        padding: 1rem 1.5rem;
        border-radius: 8px;
        border-left: 4px solid #3b82f6;
        margin: 1rem 0;
    }
    
    .nav-bar {
        background: #f1f5f9;
        border-radius: 8px;
        padding: 0.5rem;
        margin: 1rem 0;
        display: flex;
        gap: 0.5rem;
    }
    
    .nav-item {
        padding: 0.5rem 1rem;
        border-radius: 6px;
        background: white;
        border: 1px solid #d1d5db;
        cursor: pointer;
        transition: all 0.2s ease;
    }
    
    .nav-item:hover {
        background: #3b82f6;
        color: white;
    }
    
    .nav-item.active {
        background: #3b82f6;
        color: white;
    }
    
    .filter-section {
        background: #f8fafc;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
        border: 1px solid #e2e8f0;
    }
    
    .workflow-milestone {
        background: white;
        border-left: 4px solid #e5e7eb;
        padding: 1rem;
        margin: 0.5rem 0;
        border-radius: 0 8px 8px 0;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
    }
    
    .milestone-active {
        border-left-color: #f59e0b;
        background: #fffbeb;
    }
    
    .milestone-completed {
        border-left-color: #16a34a;
        background: #f0fdf4;
    }
    
    .milestone-pending {
        border-left-color: #6b7280;
        background: #f9fafb;
    }
    
    .priority-high { background: #fef2f2; border-left: 4px solid #dc2626; }
    .priority-medium { background: #fffbeb; border-left: 4px solid #f59e0b; }
    .priority-low { background: #f0fdf4; border-left: 4px solid #16a34a; }
    
    .lifecycle-badge {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
        color: white;
        margin: 0.25rem;
    }
    
    .rd { background-color: #7c3aed; }
    .clinical { background-color: #2563eb; }
    .regulatory { background-color: #dc2626; }
    .pharmacovigilance { background-color: #ea580c; }
    .cmc { background-color: #16a34a; }
    .quality { background-color: #0891b2; }
    .manufacturing { background-color: #4338ca; }
    .commercial { background-color: #be123c; }
    .medical { background-color: #059669; }
    .corporate { background-color: #374151; }
    
    .recent-activity {
        background: white;
        border: 1px solid #e5e7eb;
        border-radius: 8px;
        padding: 1rem;
        margin: 0.5rem 0;
    }
    
    .critical-alert {
        background: linear-gradient(135deg, #fef2f2 0%, #fee2e2 100%);
        border: 1px solid #fca5a5;
        border-radius: 8px;
        padding: 1rem;
        margin: 0.5rem 0;
        animation: pulse 2s infinite;
    }
    
    .document-section {
        background: #f8fafc;
        border: 1px solid #e2e8f0;
        border-radius: 8px;
        padding: 1rem;
        margin: 1rem 0;
    }
    
    .highlight-text {
        background-color: #fef08a;
        padding: 0.2rem 0.4rem;
        border-radius: 4px;
        font-weight: bold;
    }
    
    .diff-added {
        background-color: #dcfce7;
        border-left: 3px solid #16a34a;
        padding: 0.5rem;
        margin: 0.25rem 0;
    }
    
    .diff-removed {
        background-color: #fef2f2;
        border-left: 3px solid #dc2626;
        padding: 0.5rem;
        margin: 0.25rem 0;
        text-decoration: line-through;
    }
    
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.8; }
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
    # Product data with lifecycle stages
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
    
    # Workflow data
    workflow_stages = [
        'Pre-Submission', 'Dossier Preparation', 'Submission Assembly and Dispatch',
        'Regulatory Agency Review', 'Approval & Launch', 'Post Approval'
    ]
    
    # Recent activities
    recent_activities = [
        {'time': '2 hours ago', 'activity': 'FDA guidance document updated for CardioX', 'type': 'regulatory'},
        {'time': '4 hours ago', 'activity': 'OncoMax Phase III data analysis completed', 'type': 'clinical'},
        {'time': '6 hours ago', 'activity': 'NeuroHeal REMS document approved by team', 'type': 'safety'},
        {'time': '1 day ago', 'activity': 'DiabeSure pricing submission to EU authorities', 'type': 'commercial'},
        {'time': '2 days ago', 'activity': 'Respira manufacturing site inspection passed', 'type': 'quality'}
    ]
    
    # Critical alerts
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
        <div style="background: linear-gradient(180deg, #1e3a8a 0%, #3b82f6 100%); padding: 1.5rem; border-radius: 12px; margin-bottom: 1rem; text-align: center;">
            <div style="font-size: 2.5rem; margin-bottom: 0.5rem;">🔬</div>
            <h2 style="color: white; margin: 0; font-size: 1.8rem;">RIA</h2>
            <p style="color: #bfdbfe; margin: 0.5rem 0 0 0; font-size: 0.9rem;">Regulatory Intelligence Platform</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Navigation menu
        pages = ['🏠 Home', '🕵️ RIA Detective', '🧭 RISE Guider', '📚 PRISM Keeper']
        
        for page in pages:
            page_key = page.split(' ', 1)[1]
            if st.button(page, use_container_width=True, key=f"nav_{page_key}"):
                st.session_state.current_page = page_key
                st.rerun()
        
        st.markdown("---")
        
        # Additional sections
        if st.button("🔔 Notifications", use_container_width=True):
            st.info("Notifications panel opened")
        
        if st.button("⚙️ Settings", use_container_width=True):
            st.info("Settings panel opened")
        
        st.markdown("---")
        
        # Quick stats
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
    st.markdown(f"""
    <div class="main-header">
        <div class="logo-section">
            <span>🔬</span>
            <span>RIA</span>
        </div>
        <div style="margin-left: auto;">
            <h2 style="margin: 0; font-size: 1.5rem;">{page_title}</h2>
            <p style="margin: 0; opacity: 0.9; font-size: 0.9rem;">Regulatory Intelligence & Automation Platform</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Home page
def render_home():
    render_header("Dashboard")
    
    # Tool sections
    st.markdown("## 🚀 Platform Tools")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("", key="ria_card", help="Click to launch RIA Detective"):
            st.session_state.current_page = 'RIA Detective'
            st.rerun()
        st.markdown("""
        <div class="tool-card">
            <div class="tool-card-content">
                <h3 style="color: #dc2626; margin-bottom: 1rem;">🕵️ RIA - The Detective</h3>
                <p><strong>Regulatory Intelligence Analysis</strong></p>
                <p>AI-powered monitoring and analysis of regulatory updates, guidelines, and changes across global markets.</p>
                <ul>
                    <li>📈 Updates Feed</li>
                    <li>🔍 Sources Monitoring</li>
                    <li>📊 Analytics Dashboard</li>
                    <li>🚨 Alert Settings</li>
                </ul>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        if st.button("", key="rise_card", help="Click to launch RISE Guider"):
            st.session_state.current_page = 'RISE Guider'
            st.rerun()
        st.markdown("""
        <div class="tool-card">
            <div class="tool-card-content">
                <h3 style="color: #f59e0b; margin-bottom: 1rem;">🧭 RISE - The Guide</h3>
                <p><strong>Regulatory Integration & Submission Engine</strong></p>
                <p>Workflow management and timeline tracking for regulatory submissions and milestone management.</p>
                <ul>
                    <li>⚡ Active Workflows</li>
                    <li>📅 Timeline View</li>
                    <li>🔗 Dependencies</li>
                    <li>📋 Reports</li>
                </ul>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        if st.button("", key="prism_card", help="Click to launch PRISM Keeper"):
            st.session_state.current_page = 'PRISM Keeper'
            st.rerun()
        st.markdown("""
        <div class="tool-card">
            <div class="tool-card-content">
                <h3 style="color: #16a34a; margin-bottom: 1rem;">📚 PRISM - The Librarian</h3>
                <p><strong>Product Regulatory Information & Submission Management</strong></p>
                <p>Comprehensive product portfolio and regulatory information management system.</p>
                <ul>
                    <li>🧬 Product Portfolio</li>
                    <li>✅ Approvals & Renewals</li>
                    <li>🔄 Variations Tracker</li>
                    <li>📊 Compliance Dashboard</li>
                </ul>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Recent activity and critical alerts
    col1, col2 = st.columns(2)
    
    _, _, recent_activities, critical_alerts = load_sample_data()
    
    with col1:
        st.markdown("## 📈 Recent Activity")
        for activity in recent_activities:
            activity_types = {
                'regulatory': '📋', 'clinical': '🧪', 'safety': '🛡️', 
                'commercial': '💼', 'quality': '✅'
            }
            icon = activity_types.get(activity['type'], '📌')
            
            st.markdown(f"""
            <div class="recent-activity">
                <div style="display: flex; justify-content: between; align-items: center;">
                    <div>{icon} {activity['activity']}</div>
                    <small style="color: #6b7280;">{activity['time']}</small>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("## 🚨 Critical Alerts")
        for alert in critical_alerts:
            priority_colors = {'HIGH': '#dc2626', 'MEDIUM': '#f59e0b', 'LOW': '#16a34a'}
            priority_color = priority_colors.get(alert['priority'], '#6b7280')
            
            st.markdown(f"""
            <div class="critical-alert">
                <div style="display: flex; justify-content: between; align-items: start; gap: 1rem;">
                    <div>
                        <span style="color: {priority_color}; font-weight: bold;">
                            ⚠️ {alert['priority']}
                        </span>
                        <p style="margin: 0.5rem 0 0 0;">{alert['message']}</p>
                    </div>
                    <div style="background: {priority_color}; color: white; padding: 0.25rem 0.75rem; border-radius: 20px; font-size: 0.8rem;">
                        {alert['deadline']}
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

# RIA Detective page
def render_ria_detective():
    render_header("RIA Detective")
    
    # RIA description section - CORRECTED
    st.markdown("""
    <div class="section-header">
        <h3 style="margin: 0; color: #1e3a8a;">🕵️ RIA - Regulatory Impact Analyzer</h3>
        <p style="margin: 0.5rem 0 0 0; color: #64748b;">AI-powered regulatory monitoring and impact analysis system</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Navigation bar
    nav_options = ['Updates Feed', 'Sources', 'Analytics', 'Alert Settings']
    cols = st.columns(len(nav_options))
    
    for i, option in enumerate(nav_options):
        with cols[i]:
            if st.button(option, use_container_width=True, key=f"ria_nav_{option}"):
                st.session_state.ria_nav = option
    
    # Filters section
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
    
    # Content based on navigation
    if st.session_state.ria_nav == 'Updates Feed':
        st.markdown("## 📈 Regulatory Updates")
        
        # Sample regulatory updates
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
            priority_class = f"priority-{update['priority'].lower()}"
            
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
                
                # Action buttons
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
                
                # Show external comparison
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
                
                # Show AI modified document
                if st.session_state.show_ai_document == update['id']:
                    st.markdown("### 🤖 AI Modified Document")
                    st.markdown("""
                    <div class="document-section">
                        <h4>DiabeSure Product Labeling - Updated Version</h4>
                        
                        <h5>Section 5: WARNINGS AND PRECAUTIONS</h5>
                        
                        <div class="diff-added">
                        <strong>5.1 CARDIOVASCULAR RISK ASSESSMENT (NEW)</strong><br>
                        Prior to initiating DiabeSure therapy, conduct comprehensive cardiovascular risk assessment including:
                        - Baseline ECG evaluation
                        - Assessment of cardiovascular risk factors
                        - Patient history of cardiac events
                        </div>
                        
                        <div class="diff-removed">
                        5.1 General Safety Information
                        Standard diabetes medication precautions apply.
                        </div>
                        
                        <div class="diff-added">
                        <strong>5.2 CARDIAC MONITORING REQUIREMENTS (NEW)</strong><br>
                        Regular cardiac monitoring is required for patients with:
                        - Pre-existing cardiovascular conditions
                        - Age > 65 years
                        - Multiple cardiovascular risk factors
                        </div>
                        
                        <h5>Section 17: PATIENT COUNSELING INFORMATION</h5>
                        
                        <div class="diff-added">
                        <strong>17.3 CARDIOVASCULAR RISK COUNSELING (NEW)</strong><br>
                        Inform patients about potential cardiovascular risks and advise to:
                        - Report chest pain, shortness of breath, or palpitations immediately
                        - Maintain regular cardiac monitoring appointments
                        - Understand signs and symptoms of cardiac events
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                
                # Show priority logic
                if st.session_state.show_priority_logic == update['id']:
                    st.markdown("### ⚡ Priority Determination Logic")
                    st.markdown("""
                    **Priority Score: HIGH (85/100)**
                    
                    **Scoring Factors:**
                    - Regulatory Authority Impact: FDA (25/25) ✅
                    - Product Impact: DiabeSure directly affected (20/20) ✅
                    - Timeline Urgency: 30 days implementation (15/20) ⚠️
                    - Business Impact: Major labeling changes required (20/25) ⚠️
                    - Compliance Risk: High non-compliance penalty (15/15) ✅
                    
                    **Recommendation:** Immediate action required for compliance team
                    """)
    
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
            # Updates by source chart
            source_counts = [15, 8, 5, 3, 2, 1]
            sources = ['FDA', 'EMA', 'CDSCO', 'PMDA', 'Health Canada', 'TGA']
            
            fig = px.bar(x=sources, y=source_counts, title="Updates by Source (Last 30 Days)")
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Priority distribution
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
    
    # RISE description
    st.markdown("""
    <div class="section-header">
        <h3 style="margin: 0; color: #1e3a8a;">🧭 RISE - Regulatory Integration & Submission Engine</h3>
        <p style="margin: 0.5rem 0 0 0; color: #64748b;">Workflow management and regulatory milestone tracking system</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Navigation
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
        
        # Product and region selector - DiabeSure as default
        col1, col2 = st.columns(2)
        with col1:
            diabesure_index = product_names.index('DiabeSure') if 'DiabeSure' in product_names else 0
            selected_product = st.selectbox("Select Product", product_names, index=diabesure_index)
        with col2:
            selected_region = st.selectbox("Select Region", ["US", "EU", "Japan", "India", "China"])
        
        # Workflow stages with current status
        st.markdown(f"### 📋 Workflow Milestones - {selected_product} ({selected_region})")
        
        # Sample current stage (would be dynamic in real implementation)
        current_stage_index = 2  # Submission Assembly and Dispatch
        
        for i, stage in enumerate(workflow_stages):
            if i < current_stage_index:
                status_class = "milestone-completed"
                status_icon = "✅"
            elif i == current_stage_index:
                status_class = "milestone-active"
                status_icon = "🔄"
            else:
                status_class = "milestone-pending"
                status_icon = "⏳"
            
            # RIA impact analysis
            ria_impact = ""
            if stage == "Dossier Preparation" and selected_product == "DiabeSure":
                ria_impact = "⚠️ HIGH Priority: FDA labeling changes detected - requires immediate update"
            elif stage == "Regulatory Agency Review" and selected_product == "CardioX":
                ria_impact = "📋 MEDIUM Priority: EMA cardiovascular assessment updates may affect timeline"
            
            st.markdown(f"""
            <div class="workflow-milestone {status_class}">
                <h4>{status_icon} {stage}</h4>
                <p>Status: {'Completed' if i < current_stage_index else 'In Progress' if i == current_stage_index else 'Pending'}</p>
                {f'<div style="color: #dc2626; font-weight: bold; margin-top: 0.5rem;">{ria_impact}</div>' if ria_impact else ''}
            </div>
            """, unsafe_allow_html=True)
    
    elif st.session_state.rise_nav == 'Timeline View':
        st.markdown("## 📅 Timeline View")
        
        # Timeline visualization
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
    
    # PRISM description
    st.markdown("""
    <div class="section-header">
        <h3 style="margin: 0; color: #1e3a8a;">📚 PRISM - Product Regulatory Information & Submission Management</h3>
        <p style="margin: 0.5rem 0 0 0; color: #64748b;">Comprehensive product portfolio and regulatory information management</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Navigation
    nav_options = ['Product Portfolio', 'Approvals & Renewals', 'Variations Tracker', 'Compliance Dashboard']
    cols = st.columns(len(nav_options))
    
    for i, option in enumerate(nav_options):
        with cols[i]:
            if st.button(option, use_container_width=True, key=f"prism_nav_{option}"):
                st.session_state.prism_nav = option
    
    products_data, _, _, _ = load_sample_data()
    
    if st.session_state.prism_nav == 'Product Portfolio':
        st.markdown("## 🧬 Product Portfolio")
        
        # Lifecycle stages
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
        
        # Group products by category
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
                    
                    # Add document comparison for DiabeSure in Regulatory Affairs
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
                        
                        # Show current document
                        if st.session_state.get(f"show_current_{product['id']}", False):
                            st.markdown("#### 📋 Current DiabeSure Labeling Document")
                            st.markdown("""
                            <div class="document-section">
                                <h5>Section 5: WARNINGS AND PRECAUTIONS</h5>
                                <p><strong>5.1 General Safety Information</strong><br>
                                Standard diabetes medication precautions apply. Monitor blood glucose levels regularly.</p>
                                
                                <p><strong>5.2 Hypoglycemia Risk</strong><br>
                                Risk of hypoglycemia, especially when combined with other antidiabetic agents.</p>
                                
                                <h5>Section 17: PATIENT COUNSELING INFORMATION</h5>
                                <p><strong>17.1 General Information</strong><br>
                                Inform patients about proper administration and monitoring requirements.</p>
                                
                                <p><strong>17.2 Side Effects</strong><br>
                                Discuss common side effects and when to contact healthcare provider.</p>
                            </div>
                            """, unsafe_allow_html=True)
                        
                        # Show AI updated document with highlights
                        if st.session_state.get(f"show_ai_updated_{product['id']}", False):
                            st.markdown("#### 🤖 AI Updated DiabeSure Labeling Document")
                            st.markdown("""
                            <div class="document-section">
                                <h5>Section 5: WARNINGS AND PRECAUTIONS</h5>
                                
                                <div class="diff-added">
                                <p><strong>5.1 CARDIOVASCULAR RISK ASSESSMENT (UPDATED)</strong><br>
                                <span class="highlight-text">Prior to initiating DiabeSure therapy, conduct comprehensive cardiovascular risk assessment including baseline ECG evaluation, assessment of cardiovascular risk factors, and patient history of cardiac events.</span></p>
                                </div>
                                
                                <div class="diff-removed">
                                <p><strong>5.1 General Safety Information</strong><br>
                                Standard diabetes medication precautions apply. Monitor blood glucose levels regularly.</p>
                                </div>
                                
                                <p><strong>5.2 Hypoglycemia Risk</strong><br>
                                Risk of hypoglycemia, especially when combined with other antidiabetic agents.</p>
                                
                                <div class="diff-added">
                                <p><strong>5.3 CARDIAC MONITORING REQUIREMENTS (NEW)</strong><br>
                                <span class="highlight-text">Regular cardiac monitoring is required for patients with pre-existing cardiovascular conditions, age > 65 years, or multiple cardiovascular risk factors.</span></p>
                                </div>
                                
                                <h5>Section 17: PATIENT COUNSELING INFORMATION</h5>
                                <p><strong>17.1 General Information</strong><br>
                                Inform patients about proper administration and monitoring requirements.</p>
                                
                                <p><strong>17.2 Side Effects</strong><br>
                                Discuss common side effects and when to contact healthcare provider.</p>
                                
                                <div class="diff-added">
                                <p><strong>17.3 CARDIOVASCULAR RISK COUNSELING (NEW)</strong><br>
                                <span class="highlight-text">Inform patients about potential cardiovascular risks and advise to report chest pain, shortness of breath, or palpitations immediately. Maintain regular cardiac monitoring appointments and understand signs and symptoms of cardiac events.</span></p>
                                </div>
                            </div>
                            """, unsafe_allow_html=True)
                            
                            if st.button("💾 Accept AI Changes", key=f"accept_changes_{product['id']}"):
                                st.success("✅ AI changes have been accepted and document updated!")
                            
                            if st.button("❌ Reject Changes", key=f"reject_changes_{product['id']}"):
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
        
        # Renewal timeline
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
        
        # Status distribution
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
        
        # Compliance by region
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
    st.markdown("""
    <div style="text-align: center; padding: 1.5rem; background: #f8fafc; border-radius: 12px; margin-top: 2rem;">
        <p style="margin: 0; color: #1e3a8a; font-weight: 600;">
            🔬 <strong>RIA Platform</strong> | 
            Regulatory Intelligence & Automation | 
            <a href="https://indegene.com" target="_blank" style="color: #3b82f6;">Indegene Solutions</a>
        </p>
        <p style="margin: 0.5rem 0 0 0; font-size: 0.9rem; color: #64748b;">
            Last Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | 
            Version: 3.0.0 | 
            Status: 🟢 All Systems Operational
        </p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
