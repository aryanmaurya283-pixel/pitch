# PitchPerfect - AI-Powered Pitch Deck Analyzer
import streamlit as st
import os
import tempfile
from text_extractor import extract_text
from nlp_utils import analyze_sections, readability_score, sentiment_scores, extract_keywords
from file_validator import validate_file_upload
from auth_handler import AuthHandler
from figma_ui_fixed import (
    render_figma_main_content, render_figma_analysis_results,
    render_figma_loading, render_figma_success
)
from login_form import render_figma_login_form
from signup_form import render_figma_signup_form
from database_service import DatabaseService
from advanced_analytics import advanced_analyzer
from supabase import create_client, Client
from datetime import datetime
from config import config
# Import additional libraries for enhanced features
import matplotlib.pyplot as plt
import numpy as np
import io
import base64

# --- Page Configuration ---
st.set_page_config(
    page_title="PitchPerfect - AI Pitch Analyzer", 
    layout="wide",
    initial_sidebar_state="expanded"  # Sidebar always visible
)

# --- Helper Functions for Enhanced UI ---
def apply_responsive_styles():
    """Apply responsive design styles to improve mobile experience."""
    # Get current theme state
    dark_mode = st.session_state.get('dark_mode', False)
    
    st.markdown("""
    <style>
    /* Mobile Responsive Design */
    @media (max-width: 768px) {
        /* Adjust main content padding */
        .main .block-container {
            padding: 1rem !important;
        }
        
        /* Make sidebar collapsible on mobile */
        [data-testid="stSidebar"] {
            width: 100% !important;
            min-width: 100% !important;
            max-width: 100% !important;
            margin-left: -100%;
            position: fixed;
            top: 0;
            z-index: 1000;
            height: 100vh;
            transition: transform 0.3s ease;
        }
        
        /* Show sidebar when expanded */
        [data-testid="stSidebar"][aria-expanded="true"] {
            margin-left: 0 !important;
            transform: translateX(0);
        }
        
        /* Adjust main content when sidebar is expanded */
        [data-testid="stSidebar"][aria-expanded="true"] ~ .main {
            margin-left: 0 !important;
        }
        
        /* Mobile sidebar toggle button */
        .sidebar-toggle {
            display: block !important;
            position: fixed;
            top: 0.5rem;
            left: 0.5rem;
            z-index: 1001;
            background: rgba(255, 255, 255, 0.8);
            backdrop-filter: blur(5px);
            border-radius: 50%;
            width: 40px;
            height: 40px;
            text-align: center;
            line-height: 40px;
            box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);
        }
        
        /* Adjust metrics grid for mobile */
        .metrics-grid {
            grid-template-columns: 1fr !important;
        }
        
        /* Make buttons larger for touch */
        .stButton > button {
            min-height: 48px !important;
            font-size: 16px !important;
        }
        
        /* Adjust file upload area */
        .upload-area {
            padding: 40px 20px !important;
        }
        
        /* Adjust card padding */
        .figma-card {
            padding: 20px !important;
        }
    }
    
    /* Tablet Responsive Design */
    @media (min-width: 769px) and (max-width: 1024px) {
        .metrics-grid {
            grid-template-columns: repeat(2, 1fr) !important;
        }
    }
    
    /* Hide mobile sidebar toggle by default */
    .sidebar-toggle {
        display: none;
    }
    
    /* Tooltip Styles */
    .tooltip-container {
        position: relative;
        display: inline-block;
    }
    
    .tooltip-content {
        cursor: help;
        border-bottom: 1px dashed #999;
    }
    
    .tooltip {
        visibility: hidden;
        position: absolute;
        bottom: 125%;
        left: 50%;
        transform: translateX(-50%);
        background-color: rgba(0, 0, 0, 0.8);
        color: white;
        text-align: center;
        padding: 8px 12px;
        border-radius: 6px;
        z-index: 1000;
        width: max-content;
        max-width: 250px;
        font-size: 12px;
        opacity: 0;
        transition: opacity 0.3s;
    }
    
    .tooltip::after {
        content: "";
        position: absolute;
        top: 100%;
        left: 50%;
        margin-left: -5px;
        border-width: 5px;
        border-style: solid;
        border-color: rgba(0, 0, 0, 0.8) transparent transparent transparent;
    }
    
    .tooltip-container:hover .tooltip {
        visibility: visible;
        opacity: 1;
    }
    </style>
    
    <!-- Mobile sidebar toggle button -->
    <div class="sidebar-toggle" onclick="toggleSidebar()">
        <span>☰</span>
    </div>
    
    <script>
    function toggleSidebar() {
        const sidebar = window.parent.document.querySelector('[data-testid="stSidebar"]');
        const currentState = sidebar.getAttribute('aria-expanded');
        sidebar.setAttribute('aria-expanded', currentState === 'true' ? 'false' : 'true');
    }
    </script>
    """, unsafe_allow_html=True)
    
def render_interactive_dashboard(score, read_score, sentiment, grade, overall_score, strengths, weaknesses, tips, keywords, recommendations):
    """Render an interactive dashboard with tooltips and expandable sections."""
    
    # Get the current theme
    dark_mode = st.session_state.get('dark_mode', False)
    
    # Set theme-based colors
    bg_color = "#111827" if dark_mode else "#FFFFFF"
    text_color = "#F9FAFB" if dark_mode else "#111827"
    card_bg = "#1F2937" if dark_mode else "#FFFFFF"
    border_color = "#374151" if dark_mode else "#E5E7EB"
    
    st.markdown(f"""
    <style>
    /* Theme-specific styles for dashboard */
    .dashboard-container {{
        background-color: {bg_color};
        color: {text_color};
        padding-top: 60px; /* Add space for the navigation bar */
    }}
    
    .dashboard-card {{
        background-color: {card_bg};
        border: 1px solid {border_color};
    }}
    </style>
    
    <h2 style="font-size: 24px; font-weight: 700; margin-bottom: 24px; color: {text_color};">📊 Analysis Results</h2>
    """, unsafe_allow_html=True)
    
    # Metrics with tooltips
    col1, col2 = st.columns(2)
    
    with col1:
        color = "#10B981" if score >= 7 else "#F59E0B" if score >= 5 else "#EF4444"
        card_bg = card_bg
        text_secondary = "#D1D5DB" if dark_mode else "#64748B"
        
        st.markdown(f"""
        <div style="background: {card_bg}; border-radius: 12px; padding: 20px; box-shadow: 0 4px 12px rgba(0,0,0,0.1); text-align: center; border: 1px solid {border_color};">
            <div style="color: {text_secondary}; font-size: 14px; font-weight: 600; margin-bottom: 8px;">
                <div class="tooltip-container">
                    <div class="tooltip-content">Section Coverage</div>
                    <div class="tooltip" id="tooltip_1">Measures how well your pitch covers essential sections like Problem, Solution, Market, etc.</div>
                </div>
            </div>
            <div style="font-size: 28px; font-weight: 700; color: {color};">
                {score}/10
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        color = "#10B981" if read_score >= 70 else "#F59E0B" if read_score >= 50 else "#EF4444"
        st.markdown(f"""
        <div style="background: {card_bg}; border-radius: 12px; padding: 20px; box-shadow: 0 4px 12px rgba(0,0,0,0.1); text-align: center; border: 1px solid {border_color};">
            <div style="color: {text_secondary}; font-size: 14px; font-weight: 600; margin-bottom: 8px;">
                <div class="tooltip-container">
                    <div class="tooltip-content">Readability</div>
                    <div class="tooltip" id="tooltip_2">Indicates how easy your content is to read. Higher scores mean better readability.</div>
                </div>
            </div>
            <div style="font-size: 28px; font-weight: 700; color: {color};">
                {read_score:.0f}
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    col3, col4 = st.columns(2)
    
    with col3:
        color = "#10B981" if overall_score >= 80 else "#F59E0B" if overall_score >= 60 else "#EF4444"
        st.markdown(f"""
        <div style="background: {card_bg}; border-radius: 12px; padding: 20px; box-shadow: 0 4px 12px rgba(0,0,0,0.1); text-align: center; border: 1px solid {border_color};">
            <div style="color: {text_secondary}; font-size: 14px; font-weight: 600; margin-bottom: 8px;">
                <div class="tooltip-container">
                    <div class="tooltip-content">Overall Score</div>
                    <div class="tooltip" id="tooltip_3">Combined score based on multiple factors including content, structure, and clarity.</div>
                </div>
            </div>
            <div style="font-size: 28px; font-weight: 700; color: {color};">
                {overall_score}/100
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        color = "#10B981" if grade in ["A+", "A", "A-", "B+"] else "#F59E0B" if grade in ["B", "B-", "C+"] else "#EF4444"
        st.markdown(f"""
        <div style="background: {card_bg}; border-radius: 12px; padding: 20px; box-shadow: 0 4px 12px rgba(0,0,0,0.1); text-align: center; border: 1px solid {border_color};">
            <div style="color: {text_secondary}; font-size: 14px; font-weight: 600; margin-bottom: 8px;">
                <div class="tooltip-container">
                    <div class="tooltip-content">Grade</div>
                    <div class="tooltip" id="tooltip_4">Letter grade representing the overall quality of your pitch deck.</div>
                </div>
            </div>
            <div style="font-size: 28px; font-weight: 700; color: {color};">
                {grade}
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Expandable sections
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Add theme-specific styles for expanders
    st.markdown(f"""
    <style>
    /* Theme-specific styles for expanders */
    .st-emotion-cache-1gulkj5 {{
        background-color: {card_bg} !important;
        color: {text_color} !important;
        border: 1px solid {border_color} !important;
    }}
    
    .st-emotion-cache-1gulkj5 p {{
        color: {text_color} !important;
    }}
    </style>
    """, unsafe_allow_html=True)
    
    with st.expander("✨ Strengths", expanded=True):
        for strength in strengths:
            st.markdown(f"- {strength}")
    
    with st.expander("⚠️ Areas to Improve"):
        for weakness in weaknesses:
            st.markdown(f"- {weakness}")
    
    with st.expander("💡 Recommendations"):
        for tip in tips:
            st.markdown(f"- {tip}")
    
    with st.expander("🔑 Key Terms"):
        # Set tag colors based on theme
        tag_bg = "rgba(79, 126, 255, 0.2)" if dark_mode else "rgba(79, 126, 255, 0.1)"
        tag_color = "#A5B4FC" if dark_mode else "#4F7EFF"
        tag_border = "rgba(79, 126, 255, 0.3)" if dark_mode else "rgba(79, 126, 255, 0.2)"
        
        # Display keywords as tags
        st.markdown(f"""
        <div style="display: flex; flex-wrap: wrap; gap: 8px;">
        """ + "".join([f"""
        <div style="background: {tag_bg}; color: {tag_color}; padding: 6px 12px; 
                border-radius: 16px; font-size: 14px; font-weight: 500; border: 1px solid {tag_border};">
            {keyword}
        </div>
        """ for keyword in keywords]) + """
        </div>
        """, unsafe_allow_html=True)

# Tour functionality removed as requested

def show_sample_analysis_option():
    """Show an option to view a sample analysis for new users."""
    if 'has_analyses' not in st.session_state or not st.session_state.has_analyses:
        # Make the info box theme-aware
        dark_mode = st.session_state.get('dark_mode', False)
        if dark_mode:
            bg_color = "#1E293B"
            border_color = "#334155"
            title_color = "#60A5FA"
            text_color = "#CBD5E1"
        else:
            bg_color = "#F0F9FF"
            border_color = "#BAE6FD"
            title_color = "#1A365D"  # Darker blue for better contrast
            text_color = "#2D3748"   # Much darker text for better visibility
            
        st.markdown(f"""
        <div style="background: {bg_color}; border: 1px solid {border_color}; border-radius: 8px; padding: 16px; margin: 20px 0;">
            <h3 style="margin-top: 0; font-size: 16px; color: {title_color};">New to PitchPerfect?</h3>
            <p style="margin-bottom: 10px; font-size: 14px; color: {text_color};">
                See how our AI analysis works by checking out a sample pitch deck analysis.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Use a regular Streamlit button instead of JavaScript
        if st.button("View Sample Analysis", key="sample_analysis_btn", type="primary"):
            return True
    
    return False

def add_contextual_help():
    """Add contextual help tooltips throughout the application."""
    pass  # This is already handled by the tooltip CSS above

def display_download_button(analysis_data, filename):
    """Display a download button for the analysis report."""
    # Extract data from analysis_data
    summary = analysis_data.get('summary', '')
    
    # # Display download button
    # st.download_button(
    #     label="📥 Download Analysis Report",
    #     data=summary,
    #     file_name=f"{filename.split('.')[0]}_analysis_report.txt",
    #     mime="text/plain",
    #     use_container_width=True
    # )

# Responsive styles already applied above

# --- Session State Initialization (at the very top) ---
if 'sb' not in st.session_state:
    from config import config
    from supabase import create_client
    supabase_config = config.get_supabase_config()
    st.session_state.sb = create_client(supabase_config["url"], supabase_config["key"])
if 'auth' not in st.session_state:
    from auth_handler import AuthHandler
    st.session_state.auth = AuthHandler(st.session_state.sb)
if 'db_service' not in st.session_state:
    from database_service import DatabaseService
    st.session_state.db_service = DatabaseService(st.session_state.sb)
if 'dark_mode' not in st.session_state:
    st.session_state.dark_mode = False
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'page' not in st.session_state:
    st.session_state.page = 'login'
if 'current_user' not in st.session_state:
    st.session_state.current_user = {'name': 'Aryan Maurya'}

# --- ACTION HANDLER ---
def handle_actions():
    query_params = st.query_params.to_dict()
    action = query_params.get("action")
    if action:
        st.query_params.clear()
        if action == "logout":
            st.session_state.logged_in = False
            st.session_state.page = 'login'
            st.session_state.auth.logout()
            st.rerun()
        elif action == "toggle_theme":
            st.session_state.dark_mode = not st.session_state.dark_mode

# --- MAIN APPLICATION CONTROLLER ---
def main():
    import streamlit as st
    from figma_ui_fixed import render_navigation_bar, render_figma_main_content, apply_global_styles
    from sidebar import render_figma_sidebar
    from login_form import render_figma_login_form
    from signup_form import render_figma_signup_form
    st.set_page_config(layout="wide", initial_sidebar_state="expanded")
    from app import apply_responsive_styles
    apply_responsive_styles()
    handle_actions()
    if 'auth_mode' not in st.session_state:
        st.session_state.auth_mode = 'login'
    # Use only session_state.logged_in and session_state.user for auth check
    if not st.session_state.get('logged_in', False) or not st.session_state.get('user'):
        apply_global_styles()
        if st.session_state.auth_mode == 'login':
            st.session_state.auth_handler = st.session_state.auth
            render_figma_login_form()
        else:
            st.session_state.auth_handler = st.session_state.auth
            render_figma_signup_form()
        st.stop()
    current_user = st.session_state.user
    st.session_state.current_user = current_user
    apply_global_styles()
    render_navigation_bar(current_user)
    render_figma_sidebar(current_user)

    # --- Supabase Health Check ---
    db_service = st.session_state.db_service
    try:
        user = st.session_state.current_user
        user_id = user.get('id') if isinstance(user, dict) else getattr(user, 'id', None) if user else None
        if user_id:
            _ = db_service.get_user_analyses(user_id)
        st.success('✅ Supabase API is working!')
    except Exception as e:
        st.error(f'❌ Supabase API error: {e}')

    render_figma_main_content()
    # (Add your file upload/analysis/dashboard logic here)

if __name__ == "__main__":
    main()
