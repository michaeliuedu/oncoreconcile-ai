"""OncoReconcile AI - Streamlit Frontend

Interactive web interface for variant reconciliation and expert review
"""

import streamlit as st
import requests
import json
import os
from datetime import datetime

# Configure page
st.set_page_config(
    page_title="OncoReconcile AI",
    page_icon="🧬",
    layout="wide"
)

# Sidebar navigation
st.sidebar.title("OncoReconcile AI")
st.sidebar.markdown("Human-Governed AI for Precision Oncology")

page = st.sidebar.radio(
    "Navigate to:",
    ["Home", "Reconcile Variant", "Review Queue", "Audit Log"]
)

# API endpoint - use Docker service name if in container, else localhost
API_URL = os.getenv("API_URL", "http://api:8000")


def page_home():
    """Home page"""
    st.title("🧬 OncoReconcile AI")
    st.markdown("**Human-Governed AI Agent System for Precision Oncology Semantic Interoperability**")
    
    st.info(
        "⚠️ **Disclaimer**: This is a research and educational prototype. "
        "It does NOT make clinical claims, provide diagnosis, or recommend treatment."
    )
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Genes Supported", "6", "EGFR, BRAF, KRAS, ALK, MET, HER2")
    
    with col2:
        st.metric("Processing Time", "~6 seconds", "End-to-end workflow")
    
    with col3:
        st.metric("KB Version", "0.1", "MVP reference data")
    
    st.markdown("---")
    
    st.subheader("Quick Start")
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **Step 1: Submit Variant**
        - Go to "Reconcile Variant" tab
        - Enter raw variant string
        - Specify tissue type
        
        **Step 2: System Processing**
        - Extraction: Parse variant
        - Normalization: Map to canonical form
        - Retrieval: Find similar variants
        - Reasoning: Analyze clinical context
        - Confidence: Score match quality
        - Review: Queue for expert
        """)
    
    with col2:
        st.markdown("""
        **Step 3: Expert Review**
        - Go to "Review Queue" tab
        - Expert examines system reasoning
        - Reviews approval history
        - Approves/rejects reconciliation
        
        **Step 4: KB Update**
        - Variant added to KB (if approved)
        - KB version incremented
        - Audit trail logged
        - Full provenance maintained
        """)
    
    st.markdown("---")
    
    st.subheader("System Workflow")
    st.graphviz_chart(
        """
        digraph {
            graph [rankdir=LR, bgcolor="transparent", pad="0.2", nodesep="0.45", ranksep="0.55"];
            node [shape=box, style="rounded,filled", fillcolor="#eef2ff", color="#4f46e5", fontname="Helvetica", fontsize=11, margin="0.12,0.08"];
            edge [color="#6b7280", arrowsize=0.7];

            input [label="Raw Input"];
            gene [label="Gene\\nReconciliation"];
            extract [label="Variant\\nExtraction"];
            normalize [label="Normalization"];
            retrieve [label="Candidate\\nRetrieval"];
            score [label="Confidence\\nScoring"];
            review [label="Human\\nReview"];
            audit [label="Audit\\nTrail"];

            input -> gene -> extract -> normalize -> retrieve -> score -> review -> audit;
        }
        """,
        use_container_width=True,
    )
    st.caption("Multi-agent variant reconciliation pipeline")


def page_reconcile():
    """Variant reconciliation page"""
    st.title("🔄 Reconcile Variant")
    
    with st.form("reconcile_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            raw_variant = st.text_input(
                "Raw Variant",
                placeholder="e.g., EGFR Ex19del",
                help="Variant string from your lab report"
            )
            
            source = st.selectbox(
                "Source",
                ["local_lab", "research_cohort", "institutional_db", "other"]
            )
        
        with col2:
            tissue = st.selectbox(
                "Tissue Type",
                ["lung_nsclc", "lung_sclc", "breast", "melanoma", "colorectal", "other"]
            )
            
            vaf = st.slider("VAF (%)", 0, 100, 50) / 100
        
        submitted = st.form_submit_button("Submit for Reconciliation")
    
    if submitted and raw_variant:
        # Make API request
        try:
            with st.spinner("Processing variant..."):
                response = requests.post(
                    f"{API_URL}/reconcile",
                    json={
                        "raw_variant": raw_variant,
                        "source": source,
                        "tissue": tissue,
                        "vaf": vaf
                    },
                    timeout=30
                )
            
            if response.status_code == 200:
                result = response.json()
                
                st.success("✓ Reconciliation complete!")
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric("Reconciliation ID", result.get("reconciliation_id", "N/A")[:12])
                
                with col2:
                    st.metric("Confidence", f"{result.get('confidence_score', 0):.1%}", 
                              result.get("confidence_category", "N/A"))
                
                with col3:
                    st.metric("Review Queue", result.get("queue_type", "N/A"))
                
                st.markdown("---")
                
                st.subheader("Results")
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write(f"**Input Variant**: {result.get('input_variant')}")
                    st.write(f"**Canonical Variant**: `{result.get('canonical_variant', 'Not found')}`")
                    st.write(f"**Status**: {result.get('status')}")
                
                with col2:
                    st.write(f"**Assigned to**: Expert Review")
                    st.write(f"**Estimated Review**: {result.get('estimated_review_time_minutes', 'N/A')} min")
                    st.write(f"**Review ID**: {result.get('review_id', 'N/A')[:12]}")
                
                st.info("✓ Variant queued for expert review. You will be notified when reviewed.")
            
            else:
                st.error(f"Error: {response.text}")
        
        except requests.exceptions.ConnectionError:
            st.error("❌ Cannot connect to API. Is the server running on port 8000?")
        except Exception as e:
            st.error(f"Error: {str(e)}")


def page_review_queue():
    """Review queue page"""
    st.title("📋 Review Queue")
    
    try:
        response = requests.get(f"{API_URL}/review-queue", timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Total Pending", data.get("total_pending", 0))
            
            with col2:
                st.metric("Fast Track", data.get("queue_counts", {}).get("fast_track", 0))
            
            with col3:
                st.metric("Standard", data.get("queue_counts", {}).get("standard", 0))
            
            with col4:
                st.metric("Escalation", data.get("queue_counts", {}).get("escalation", 0))
            
            st.markdown("---")
            
            st.subheader("Reviewer Workload")
            for reviewer_id, load_info in data.get("reviewer_loads", {}).items():
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.write(f"**{reviewer_id}**: {load_info['utilization']}")
                with col2:
                    utilization = load_info['load'] / load_info['capacity']
                    st.progress(utilization)
            
            st.markdown("---")
            
            st.info("Mock review queue data. Real queue populated when variants are submitted.")
        
        else:
            st.error("Error fetching review queue")
    
    except requests.exceptions.ConnectionError:
        st.error("❌ Cannot connect to API")


def page_audit_log():
    """Audit log page"""
    st.title("📜 Audit Log")
    
    st.info("Audit trail showing all reconciliation decisions")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        date_from = st.date_input("From Date")
    
    with col2:
        date_to = st.date_input("To Date")
    
    with col3:
        reviewer_filter = st.text_input("Filter by Reviewer (optional)")
    
    if st.button("Fetch Audit Log"):
        try:
            response = requests.get(f"{API_URL}/audit-log", timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                
                if data.get("entries"):
                    st.dataframe(data.get("entries", []))
                else:
                    st.info("No audit log entries found")
            
            else:
                st.error("Error fetching audit log")
        
        except requests.exceptions.ConnectionError:
            st.error("❌ Cannot connect to API")


# Render page
if page == "Home":
    page_home()
elif page == "Reconcile Variant":
    page_reconcile()
elif page == "Review Queue":
    page_review_queue()
elif page == "Audit Log":
    page_audit_log()

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: #888; font-size: 0.8em'>
    OncoReconcile AI | Research & Educational Prototype | v0.1.0
    </div>
    """,
    unsafe_allow_html=True
)
