import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
import time

# Page config
st.set_page_config(
    page_title="RIA - Regulatory Impact Analyzer",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for professional styling
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #1e40af 0%, #3b82f6 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    .metric-card {
        background: white;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #3b82f6;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        margin: 0.5rem 0;
    }
    
    .alert-card {
        padding: 1rem;
        border-radius: 8px;
        margin: 0.5rem 0;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }
    
    .high-priority { background: #fef2f2; border-left: 4px solid #dc2626; }
    .medium-priority { background: #fffbeb; border-left: 4px solid #f59e0b; }
    .low-priority { background: #f0fdf4; border-left: 4px solid #16a34a; }
    
    .status-bar {
        background: #f8fafc;
        padding: 1rem;
        border-radius: 8px;
        margin-bottom: 1rem;
        display: flex;
        justify-content: space-around;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
    }
    
    .workflow-phase {
        padding: 0.5rem 1rem;
        margin: 0.25rem;
        border-radius: 20px;
        color: white;
        text-align: center;
        font-size: 0.9rem;
    }
    
    .completed { background-color: #16a34a; }
    .in-progress { background-color: #f59e0b; }
    .pending { background-color: #6b7280; }
    
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #1e40af 0%, #3b82f6 100%);
    }
    
    .product-card {
        background: white;
        border: 1px solid #e5e7eb;
        border-radius: 8px;
        padding: 1rem;
        margin: 0.5rem;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
        transition: all 0.3s ease;
    }
    
    .product-card:hover {
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
        transform: translateY(-2px);
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'current_page' not in st.session_state:
    st.session_state.current_page = 'RIA Monitor'

if 'selected_alert' not in st.session_state:
    st.session_state.selected_alert = None

if 'selected_product' not in st.session_state:
    st.session_state.selected_product = None

# Sample data
@st.cache_data
def load_sample_data():
    alerts_data = [
        {
            'id': 'AL001',
            'title': 'FDA: New Diabetes Labeling Requirements',
            'priority': 'HIGH',
            'source': 'FDA.gov',
            'published': '2025-03-15',
            'impact': 3,
            'timeline': 30,
            'priority_score': 85,
            'therapeutic_area': 'Endocrinology',
            'status': 'Active'
        },
        {
            'id': 'AL002', 
            'title': 'EMA: Cardiovascular Risk Assessment Update',
            'priority': 'MEDIUM',
            'source': 'EMA.europa.eu',
            'published': '2025-03-14',
            'impact': 2,
            'timeline': 60,
            'priority_score': 65,
            'therapeutic_area': 'Cardiology',
            'status': 'In Progress'
        },
        {
            'id': 'AL003',
            'title': 'CDSCO: Generic Drug Manufacturing Guidelines',
            'priority': 'LOW',
            'source': 'CDSCO.gov.in',
            'published': '2025-03-12',
            'impact': 1,
            'timeline': 90,
            'priority_score': 35,
            'therapeutic_area': 'Generic Manufacturing',
            'status': 'Active'
        }
    ]
    
    products_data = [
        {
            'id': 'PRD001',
            'name': 'CardioX',
            'therapeutic_area': 'Cardiovascular',
            'markets': ['US', 'EU', 'Japan'],
            'submissions': {
                'US': {'type': 'NDA', 'status': 'Approved', 'progress': 100},
                'EU': {'type': 'MAA', 'status': 'Review', 'progress': 75},
                'Japan': {'type': 'PMDA', 'status': 'Draft', 'progress': 45}
            }
        },
        {
            'id': 'PRD002',
            'name': 'OncoMax',
            'therapeutic_area': 'Oncology',
            'markets': ['US', 'EU', 'LATAM'],
            'submissions': {
                'US': {'type': 'BLA', 'status': 'Submitted', 'progress': 85},
                'EU': {'type': 'MAA', 'status': 'Review', 'progress': 60},
                'LATAM': {'type': 'ANVISA', 'status': 'Draft', 'progress': 30}
            }
        },
        {
            'id': 'PRD003',
            'name': 'NeuroHeal',
            'therapeutic_area': 'Neurology',
            'markets': ['US', 'EU', 'India'],
            'submissions': {
                'US': {'type': 'NDA', 'status': 'Query', 'progress': 90},
                'EU': {'type': 'MAA', 'status': 'Approved', 'progress': 100},
                'India': {'type': 'CDSCO', 'status': 'Review', 'progress': 70}
            }
        },
        {
            'id': 'PRD004',
            'name': 'DiabeSure',
            'therapeutic_area': 'Metabolic/Diabetes',
            'markets': ['US', 'EU', 'China'],
            'submissions': {
                'US': {'type': 'NDA', 'status': 'Approved', 'progress': 100},
                'EU': {'type': 'MAA', 'status': 'Submitted', 'progress': 80},
                'China': {'type': 'NMPA', 'status': 'Draft', 'progress': 25}
            }
        },
        {
            'id': 'PRD005',
            'name': 'Respira',
            'therapeutic_area': 'Respiratory',
            'markets': ['US', 'EU', 'Middle East'],
            'submissions': {
                'US': {'type': 'ANDA', 'status': 'Review', 'progress': 65},
                'EU': {'type': 'Generic App', 'status': 'Draft', 'progress': 40},
                'Middle East': {'type': 'GCC', 'status': 'Planning', 'progress': 15}
            }
        }
    ]
    
    workflows_data = [
        {
            'id': 'WF001',
            'alert_id': 'AL001',
            'title': 'FDA Diabetes Labeling Update',
            'priority': 'HIGH',
            'timeline': 30,
            'remaining_days': 25,
            'current_phase': 'Dossier Preparation',
            'milestones': [
                {'phase': 'Pre-Submission', 'milestone': 'Regulatory change detected', 'status': 'completed', 'assigned_to': 'System', 'due_date': '2025-03-15'},
                {'phase': 'Pre-Submission', 'milestone': 'Impact analysis completed', 'status': 'completed', 'assigned_to': 'AI Engine', 'due_date': '2025-03-15'},
                {'phase': 'Pre-Submission', 'milestone': 'Products identified', 'status': 'completed', 'assigned_to': 'System', 'due_date': '2025-03-16'},
                {'phase': 'Dossier Preparation', 'milestone': 'Module authoring', 'status': 'in-progress', 'assigned_to': 'Sarah.Johnson@indegene.com', 'due_date': '2025-03-25'},
                {'phase': 'Dossier Preparation', 'milestone': 'Cross-functional review', 'status': 'pending', 'assigned_to': 'Review Team', 'due_date': '2025-03-28'},
                {'phase': 'Assembly', 'milestone': 'eCTD publishing', 'status': 'pending', 'assigned_to': 'Publishing Team', 'due_date': '2025-04-05'}
            ]
        }
    ]
    
    return alerts_data, products_data, workflows_data

# Sidebar navigation
def render_sidebar():
    with st.sidebar:
        st.markdown("""
        <div style="background: linear-gradient(180deg, #1e40af 0%, #3b82f6 100%); padding: 1rem; border-radius: 10px; margin-bottom: 1rem;">
            <h2 style="color: white; text-align: center; margin: 0;">🔍 RIA Platform</h2>
            <p style="color: #e0e7ff; text-align: center; margin: 0.5rem 0 0 0;">Regulatory Intelligence & Automation</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Navigation buttons
        pages = ['🔍 RIA Monitor', '📊 Internal Database', '⚙️ RISE Workflows']
        
        for page in pages:
            if st.button(page, use_container_width=True, key=page):
                st.session_state.current_page = page.split(' ', 1)[1]
                st.rerun()
        
        st.markdown("---")
        
        # Quick stats
        st.markdown("### 📈 Live Stats")
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Active Alerts", "20", delta="3")
        with col2:
            st.metric("Products", "156", delta="5")
        
        st.metric("Compliance Rate", "98%", delta="2%")
        st.metric("Avg Response", "12m", delta="-3m")

# Main header
def render_header():
    st.markdown(f"""
    <div class="main-header">
        <h1>🔍 RIA - Regulatory Impact Analyzer</h1>
        <p>AI-Powered Regulatory Intelligence & Compliance Automation Platform</p>
        <p><strong>Current Module:</strong> {st.session_state.current_page}</p>
    </div>
    """, unsafe_allow_html=True)

# Status bar
def render_status_bar():
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div style="text-align: center; padding: 1rem; background: #fef2f2; border-radius: 8px; border: 1px solid #fecaca;">
            <h3 style="color: #dc2626; margin: 0;">🚨 Alerts</h3>
            <p style="margin: 0;"><span style="color: #dc2626;">●</span> High (3) <span style="color: #f59e0b;">●</span> Medium (5) <span style="color: #16a34a;">●</span> Low (12)</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="text-align: center; padding: 1rem; background: #f0f9ff; border-radius: 8px; border: 1px solid #bae6fd;">
            <h3 style="color: #0369a1; margin: 0;">📊 KPIs</h3>
            <p style="margin: 0;">Response: 12m | Compliance: 98% | On-time: 94%</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style="text-align: center; padding: 1rem; background: #f0fdf4; border-radius: 8px; border: 1px solid #bbf7d0;">
            <h3 style="color: #16a34a; margin: 0;">🔧 Performance</h3>
            <p style="margin: 0;">Sources: 52 | Products: 156 | Docs: 1,247</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div style="text-align: center; padding: 1rem; background: #fefce8; border-radius: 8px; border: 1px solid #fef3c7;">
            <h3 style="color: #ca8a04; margin: 0;">🔗 Integration</h3>
            <p style="margin: 0;">Teams ✅ | Cortex ✅ | Active: 8 workflows</p>
        </div>
        """, unsafe_allow_html=True)

# RIA Monitor page
def render_ria_monitor():
    alerts_data, _, _ = load_sample_data()
    
    st.markdown("## 🔍 Regulatory Alert Monitoring")
    
    # Priority filter
    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        priority_filter = st.selectbox("Filter by Priority:", ["All", "HIGH", "MEDIUM", "LOW"])
    with col2:
        if st.button("🔄 Refresh Alerts", use_container_width=True):
            st.success("Alerts refreshed!")
    with col3:
        if st.button("📤 Export Data", use_container_width=True):
            st.info("Export functionality activated!")
    
    # Filter alerts
    if priority_filter != "All":
        filtered_alerts = [alert for alert in alerts_data if alert['priority'] == priority_filter]
    else:
        filtered_alerts = alerts_data
    
    # Alert cards
    for alert in filtered_alerts:
        priority_class = f"{alert['priority'].lower()}-priority"
        priority_emoji = {"HIGH": "🔴", "MEDIUM": "🟡", "LOW": "🟢"}
        
        with st.container():
            st.markdown(f"""
            <div class="alert-card {priority_class}" onclick="selectAlert('{alert['id']}')">
                <div style="display: flex; justify-content: between; align-items: center;">
                    <div style="flex: 1;">
                        <h4>{priority_emoji[alert['priority']]} {alert['priority']} | {alert['title']}</h4>
                        <p><strong>Source:</strong> {alert['source']} | <strong>Published:</strong> {alert['published']} | <strong>Impact:</strong> {alert['impact']} products | <strong>Timeline:</strong> {alert['timeline']} days</p>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                if st.button(f"📋 View Details", key=f"details_{alert['id']}"):
                    st.session_state.selected_alert = alert['id']
            with col2:
                if st.button(f"📄 Generate Doc", key=f"doc_{alert['id']}"):
                    st.success(f"Document generated for {alert['title']}")
            with col3:
                if st.button(f"👥 Assign Team", key=f"team_{alert['id']}"):
                    st.info(f"Team assignment for {alert['title']}")
            with col4:
                if st.button(f"🚀 Create Workflow", key=f"workflow_{alert['id']}"):
                    st.session_state.current_page = 'RISE Workflows'
                    st.rerun()
    
    # Alert detail view
    if st.session_state.selected_alert:
        selected = next((a for a in alerts_data if a['id'] == st.session_state.selected_alert), None)
        if selected:
            st.markdown("---")
            st.markdown("### 📋 Alert Details")
            
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"""
                **Alert ID:** {selected['id']}  
                **Title:** {selected['title']}  
                **Priority Score:** {selected['priority_score']}/100  
                **Therapeutic Area:** {selected['therapeutic_area']}  
                **Status:** {selected['status']}
                """)
            
            with col2:
                st.markdown(f"""
                **Source:** [{selected['source']}](https://example.com)  
                **Published:** {selected['published']}  
                **Products Affected:** {selected['impact']}  
                **Compliance Timeline:** {selected['timeline']} days
                """)
            
            # Priority breakdown
            st.markdown("#### 🎯 Priority Score Breakdown")
            fig = go.Figure(go.Bar(
                x=['Urgency Keywords', 'Deadline Proximity', 'Products Affected', 'Authority Weight'],
                y=[30, 25, 20, 10],
                marker_color=['#dc2626', '#f59e0b', '#16a34a', '#3b82f6']
            ))
            fig.update_layout(height=300, showlegend=False)
            st.plotly_chart(fig, use_container_width=True)

# Internal Database page
def render_internal_database():
    _, products_data, _ = load_sample_data()
    
    st.markdown("## 📊 Internal Database System")
    
    # Action buttons
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        if st.button("📥 Import Data", use_container_width=True):
            st.success("Data import initiated!")
    with col2:
        if st.button("📤 Export Data", use_container_width=True):
            st.success("Data exported successfully!")
    with col3:
        if st.button("📄 Add Document", use_container_width=True):
            st.info("Document upload interface opened!")
    with col4:
        if st.button("🔄 Version Control", use_container_width=True):
            st.info("Version control panel accessed!")
    
    # Product portfolio carousel
    st.markdown("### 🧬 Product Portfolio")
    
    # Create carousel effect with columns
    cols = st.columns(3)
    for i, product in enumerate(products_data[:3]):
        with cols[i % 3]:
            st.markdown(f"""
            <div class="product-card">
                <h4>🧬 {product['name']}</h4>
                <p><strong>Therapeutic Area:</strong> {product['therapeutic_area']}</p>
                <p><strong>Markets:</strong> {', '.join(product['markets'])}</p>
                <div style="margin-top: 1rem;">
                    <small><strong>Submission Status:</strong></small>
            """, unsafe_allow_html=True)
            
            for market, details in product['submissions'].items():
                progress_color = "#16a34a" if details['progress'] == 100 else "#f59e0b" if details['progress'] > 50 else "#dc2626"
                st.markdown(f"""
                    <div style="margin: 0.25rem 0; background: #f8fafc; padding: 0.5rem; border-radius: 4px;">
                        <span style="font-weight: bold;">{market}</span> - {details['type']} - {details['status']}
                        <div style="background: #e5e7eb; height: 8px; border-radius: 4px; margin-top: 4px;">
                            <div style="background: {progress_color}; height: 8px; width: {details['progress']}%; border-radius: 4px;"></div>
                        </div>
                    </div>
                """, unsafe_allow_html=True)
            
            st.markdown("</div></div>", unsafe_allow_html=True)
            
            if st.button(f"View Details", key=f"product_{product['id']}"):
                st.session_state.selected_product = product['id']
    
    # Show more products button
    if len(products_data) > 3:
        if st.button("🔄 Show More Products"):
            # Display remaining products in next row
            cols = st.columns(2)
            for i, product in enumerate(products_data[3:]):
                with cols[i % 2]:
                    st.markdown(f"""
                    <div class="product-card">
                        <h4>🧬 {product['name']}</h4>
                        <p><strong>Therapeutic Area:</strong> {product['therapeutic_area']}</p>
                        <p><strong>Markets:</strong> {', '.join(product['markets'])}</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    if st.button(f"View Details", key=f"product_extra_{product['id']}"):
                        st.session_state.selected_product = product['id']
    
    # Document repository
    st.markdown("### 📁 Document Repository")
    
    doc_cols = st.columns(3)
    repositories = [
        {"name": "📋 FDA Files", "count": 245, "color": "#3b82f6"},
        {"name": "📋 EMA Dossiers", "count": 156, "color": "#16a34a"}, 
        {"name": "📋 CDSCO Apps", "count": 89, "color": "#f59e0b"}
    ]
    
    for i, repo in enumerate(repositories):
        with doc_cols[i]:
            st.markdown(f"""
            <div style="background: white; border: 2px solid {repo['color']}; border-radius: 8px; padding: 1rem; text-align: center; cursor: pointer;">
                <h3 style="color: {repo['color']}; margin: 0;">{repo['name']}</h3>
                <h2 style="margin: 0.5rem 0;">{repo['count']}</h2>
                <p style="margin: 0;">Documents</p>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button(f"Browse {repo['name']}", key=f"repo_{i}"):
                st.success(f"Opened {repo['name']} repository")
    
    # Product detail view
    if st.session_state.selected_product:
        selected_product = next((p for p in products_data if p['id'] == st.session_state.selected_product), None)
        if selected_product:
            st.markdown("---")
            st.markdown(f"### 📋 Product Details: {selected_product['name']}")
            
            tab1, tab2, tab3, tab4 = st.tabs(["📊 Overview", "📋 Submissions", "📄 Documents", "🤝 Commitments"])
            
            with tab1:
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown(f"""
                    **Product Name:** {selected_product['name']}  
                    **Therapeutic Area:** {selected_product['therapeutic_area']}  
                    **Markets:** {', '.join(selected_product['markets'])}  
                    **Total Submissions:** {len(selected_product['submissions'])}
                    """)
                
                with col2:
                    # Submission status chart
                    statuses = [details['status'] for details in selected_product['submissions'].values()]
                    status_counts = {status: statuses.count(status) for status in set(statuses)}
                    
                    fig = px.pie(values=list(status_counts.values()), names=list(status_counts.keys()), 
                               title="Submission Status Distribution")
                    st.plotly_chart(fig, use_container_width=True)
            
            with tab2:
                st.markdown("#### Market-wise Submissions")
                for market, details in selected_product['submissions'].items():
                    status_color = {"Approved": "#16a34a", "Review": "#f59e0b", "Draft": "#6b7280", "Submitted": "#3b82f6", "Query": "#dc2626"}
                    
                    col1, col2, col3, col4 = st.columns([2, 1, 1, 2])
                    with col1:
                        st.write(f"**{market}** - {details['type']}")
                    with col2:
                        st.markdown(f"<span style='color: {status_color.get(details['status'], '#6b7280')};'>●</span> {details['status']}", unsafe_allow_html=True)
                    with col3:
                        st.write(f"{details['progress']}%")
                    with col4:
                        st.progress(details['progress']/100)
            
            with tab3:
                st.markdown("#### Document Management")
                st.markdown("""
                | Document | Version | Status | Last Modified | Actions |
                |----------|---------|--------|---------------|---------|
                | Product_Dossier_US.pdf | v2.1 | Current | 2025-03-10 | 📥 📄 📝 📊 |
                | Label_Text_EU.docx | v1.8 | Draft | 2025-03-08 | 📥 📄 📝 📊 |
                | Safety_Update.pdf | v3.0 | Approved | 2025-03-05 | 📥 📄 📝 📊 |
                """)
                
                if st.button("📤 Upload New Document"):
                    st.info("Document upload interface opened!")
            
            with tab4:
                st.markdown("#### Regulatory Commitments")
                st.markdown("""
                | Commitment | Due Date | Owner | Status |
                |------------|----------|--------|--------|
                | Annual Safety Report | 2025-04-15 | Safety Team | 🟡 In Progress |
                | Post-Marketing Study | 2025-06-30 | Clinical Team | 🟢 On Track |
                | Risk Management Update | 2025-05-20 | Regulatory Team | 🔴 Overdue |
                """)

# RISE Workflows page
def render_rise_workflows():
    _, _, workflows_data = load_sample_data()
    
    st.markdown("## ⚙️ RISE - Regulatory Integration & Submission Engine")
    
    # Workflow overview
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Active Workflows", "8", delta="2")
    with col2:
        st.metric("Completed This Month", "12", delta="3")
    with col3:
        st.metric("On-Time Completion", "94%", delta="2%")
    with col4:
        st.metric("Avg Completion Time", "18 days", delta="-2 days")
    
    # Active workflow details
    workflow = workflows_data[0]
    
    st.markdown(f"### 🚀 Active Workflow: {workflow['title']}")
    st.markdown(f"**Priority:** {workflow['priority']} | **Timeline:** {workflow['timeline']} days | **Remaining:** {workflow['remaining_days']} days")
    
    # Progress visualization
    phases = {}
    for milestone in workflow['milestones']:
        phase = milestone['phase']
        if phase not in phases:
            phases[phase] = {'total': 0, 'completed': 0}
        phases[phase]['total'] += 1
        if milestone['status'] == 'completed':
            phases[phase]['completed'] += 1
    
    st.markdown("#### 📊 Phase Progress")
    phase_cols = st.columns(len(phases))
    for i, (phase, data) in enumerate(phases.items()):
        with phase_cols[i]:
            progress = (data['completed'] / data['total']) * 100
            st.metric(phase.replace('-', ' ').title(), f"{data['completed']}/{data['total']}", f"{progress:.0f}%")
            st.progress(progress/100)
    
    # Milestone timeline
    st.markdown("#### 🎯 Regulatory Milestones")
    
    for milestone in workflow['milestones']:
        status_emoji = {"completed": "✅", "in-progress": "🔄", "pending": "⏳"}
        status_class = {"completed": "completed", "in-progress": "in-progress", "pending": "pending"}
        
        col1, col2, col3, col4 = st.columns([3, 2, 2, 2])
        with col1:
            st.markdown(f"""
            <div class="workflow-phase {status_class[milestone['status']]}">
                {status_emoji[milestone['status']]} {milestone['milestone']}
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.write(f"**Phase:** {milestone['phase'].replace('-', ' ').title()}")
        
        with col3:
            st.write(f"**Due:** {milestone['due_date']}")
        
        with col4:
            st.write(f"**Owner:** {milestone['assigned_to'].split('@')[0] if '@' in milestone['assigned_to'] else milestone['assigned_to']}")
    
    # Integration status
    st.markdown("#### 🔗 Team Integration Status")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
        <div style="background: #f0fdf4; padding: 1rem; border-radius: 8px; border-left: 4px solid #16a34a;">
            <h4 style="color: #16a34a; margin: 0;">📧 Microsoft Teams</h4>
            <p style="margin: 0.5rem 0 0 0;">✅ Connected | Last notification: 5 mins ago</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="background: #f0fdf4; padding: 1rem; border-radius: 8px; border-left: 4px solid #16a34a;">
            <h4 style="color: #16a34a; margin: 0;">🔗 Indegene Cortex</h4>
            <p style="margin: 0.5rem 0 0 0;">✅ Connected | Sync active</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style="background: #f0fdf4; padding: 1rem; border-radius: 8px; border-left: 4px solid #16a34a;">
            <h4 style="color: #16a34a; margin: 0;">📋 Workflow Engine</h4>
            <p style="margin: 0.5rem 0 0 0;">✅ Running 12 workflows</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Live notification example
    st.markdown("#### 💬 Live Teams Notification Preview")
    st.info("🚨 HIGH: FDA diabetes labeling affects DiabeSure. Sarah Johnson assigned. Due: Mar 25. [Review Doc] [Update]")
    
    # Workflow actions
    st.markdown("#### ⚡ Workflow Actions")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("🚀 Create New Workflow", use_container_width=True):
            st.success("New workflow creation initiated!")
    
    with col2:
        if st.button("📊 Generate Report", use_container_width=True):
            st.success("Workflow report generated!")
    
    with col3:
        if st.button("👥 Assign Tasks", use_container_width=True):
            st.info("Task assignment interface opened!")
    
    with col4:
        if st.button("🔔 Send Alerts", use_container_width=True):
            st.success("Team alerts sent successfully!")
    
    # Workflow timeline visualization
    st.markdown("#### 📈 Workflow Timeline")
    
    # Create timeline chart
    timeline_data = []
    for milestone in workflow['milestones']:
        timeline_data.append({
            'Task': milestone['milestone'],
            'Phase': milestone['phase'],
            'Status': milestone['status'],
            'Start': datetime.strptime(milestone['due_date'], '%Y-%m-%d') - timedelta(days=7),
            'Finish': datetime.strptime(milestone['due_date'], '%Y-%m-%d'),
            'Assignee': milestone['assigned_to'].split('@')[0] if '@' in milestone['assigned_to'] else milestone['assigned_to']
        })
    
    # Create Gantt-like chart
    fig = go.Figure()
    
    colors = {'completed': '#16a34a', 'in-progress': '#f59e0b', 'pending': '#6b7280'}
    
    for i, task in enumerate(timeline_data):
        fig.add_trace(go.Scatter(
            x=[task['Start'], task['Finish']],
            y=[i, i],
            mode='lines+markers',
            line=dict(color=colors[task['Status']], width=10),
            name=task['Status'].replace('-', ' ').title(),
            text=task['Task'],
            hovertemplate=f"<b>{task['Task']}</b><br>Phase: {task['Phase']}<br>Assignee: {task['Assignee']}<br>Status: {task['Status']}<extra></extra>"
        ))
    
    fig.update_layout(
        title="Regulatory Milestone Timeline",
        xaxis_title="Date",
        yaxis_title="Milestones",
        yaxis=dict(tickmode='array', tickvals=list(range(len(timeline_data))), 
                  ticktext=[t['Task'][:30] + '...' if len(t['Task']) > 30 else t['Task'] for t in timeline_data]),
        height=400,
        showlegend=False
    )
    
    st.plotly_chart(fig, use_container_width=True)

# Main app logic
def main():
    render_header()
    render_status_bar()
    render_sidebar()
    
    # Route to appropriate page
    if st.session_state.current_page == 'RIA Monitor':
        render_ria_monitor()
    elif st.session_state.current_page == 'Internal Database':
        render_internal_database()
    elif st.session_state.current_page == 'RISE Workflows':
        render_rise_workflows()
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; padding: 1rem; background: #f8fafc; border-radius: 8px; margin-top: 2rem;">
        <p style="margin: 0; color: #6b7280;">
            🔍 <strong>RIA - Regulatory Impact Analyzer</strong> | 
            Powered by AI & Advanced Analytics | 
            <a href="https://indegene.com" target="_blank">Indegene Solutions</a>
        </p>
        <p style="margin: 0.5rem 0 0 0; font-size: 0.9rem; color: #9ca3af;">
            Last Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | 
            Version: 2.1.0 | 
            Status: 🟢 All Systems Operational
        </p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
