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
    initial_sidebar_state="collapsed"
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
    
    function toggleTheme() {
        // Find and click the theme toggle button in the sidebar
        const themeButton = window.parent.document.querySelector('[data-testid="stSidebar"] [key="theme_toggle"]');
        if (themeButton) {
            themeButton.click();
        }
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
        st.markdown("""
        <div style="background: #F0F9FF; border: 1px solid #BAE6FD; border-radius: 8px; padding: 16px; margin: 20px 0;">
            <h3 style="margin-top: 0; font-size: 16px; color: #0369A1;">New to PitchPerfect?</h3>
            <p style="margin-bottom: 10px; font-size: 14px; color: #0C4A6E;">
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

# --- Load Supabase client ---
supabase_config = config.get_supabase_config()
sb: Client = create_client(supabase_config["url"], supabase_config["key"])

# --- Initialize Services ---
auth = AuthHandler(sb)
db_service = DatabaseService(sb)

# --- Initialize Theme State ---
if 'dark_mode' not in st.session_state:
    st.session_state.dark_mode = False

# Apply responsive styles and theme-specific styles
apply_responsive_styles()

# Add global theme styles with Indigo & Slate palette
dark_mode = st.session_state.get('dark_mode', False)
# Dark Mode Palette (Futuristic & Luxurious)
if dark_mode:
    bg_color = "#0F172A"  # Deep navy slate — stylish, easy on eyes
    text_color = "#F1F5F9"  # Very light gray — for high contrast
    text_secondary = "#94A3B8"  # Muted cool gray — subtle and elegant
    card_bg = "#1E293B"  # Slightly raised, matte container look
    border_color = "#334155"  # Muted navy-gray for subtle dividers
    accent_color = "#6366F1"  # Soft lavender blue — pops beautifully
    button_hover = "#4F46E5"  # Deeper indigo for interaction
    success_color = "#22C55E"  # Powerful green shade that stands out
    error_color = "#F87171"  # Soft coral red — less harsh than pure red
# Light Mode Palette (Elegant & Sleek)
else:
    bg_color = "#F9FAFB"  # Very light gray; relaxing, not pure white
    text_color = "#1F2937"  # Dark slate — calm but strong readability
    text_secondary = "#6B7280"  # Cool gray — for subtle descriptions
    card_bg = "#FFFFFF"  # Pure white for a clean, layered look
    border_color = "#E5E7EB"  # Light gray for subtle separation
    accent_color = "#4F46E5"  # Premium indigo — for CTAs, links, focus
    button_hover = "#4338CA"  # Slightly darker indigo for interaction
    success_color = "#10B981"  # Vibrant green for success messages
    error_color = "#EF4444"  # Stylish red for warnings/errors

st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

/* Global theme styles with Indigo & Slate palette */
* {{
    font-family: 'Inter', sans-serif;
}}

.stApp {{
    background-color: {bg_color} !important;
    color: {text_color} !important;
}}

/* Make sure theme toggle is always visible */
button[kind="secondary"] {{
    z-index: 1000 !important;
    position: relative !important;
    color: white !important;
    border: none !important;
    background-color: {accent_color} !important;
    font-weight: 600 !important;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1) !important;
    transition: all 0.2s ease !important;
}}

button[kind="secondary"]:hover {{
    background-color: {button_hover} !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 6px 8px rgba(0, 0, 0, 0.15) !important;
}}

/* File uploader styling */
.stFileUploader {{
    background-color: {card_bg} !important;
    border: 2px dashed {accent_color} !important;
    border-radius: 12px !important;
    padding: 24px !important;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.06) !important;
    transition: all 0.2s ease !important;
}}

.stFileUploader:hover {{
    border-color: {button_hover} !important;
    box-shadow: 0 6px 16px rgba(0, 0, 0, 0.08) !important;
}}

.stFileUploader > div > div > span {{
    color: {accent_color} !important;
    font-weight: 600 !important;
}}

.stFileUploader > div > div > small {{
    color: {text_secondary} !important;
}}

/* Error message styling */
.stAlert {{
    background-color: {card_bg} !important;
    color: {error_color} !important;
    border-left: 4px solid {error_color} !important;
    border-radius: 4px !important;
    padding: 16px !important;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.06) !important;
}}

/* Success message styling */
.stSuccess {{
    background-color: {card_bg} !important;
    color: {success_color} !important;
    border-left: 4px solid {success_color} !important;
    border-radius: 4px !important;
    padding: 16px !important;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.06) !important;
}}

/* Info message styling */
.stInfo {{
    background-color: {card_bg} !important;
    color: {accent_color} !important;
    border-left: 4px solid {accent_color} !important;
    border-radius: 4px !important;
    padding: 16px !important;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.06) !important;
}}

/* Warning message styling */
.stWarning {{
    background-color: {card_bg} !important;
    color: {"#F59E0B" if dark_mode else "#B45309"} !important;
    border-left: 4px solid {"#F59E0B" if dark_mode else "#F59E0B"} !important;
    border-radius: 4px !important;
    padding: 16px !important;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.06) !important;
}}

/* Code block styling */
.stCodeBlock {{
    background-color: {card_bg} !important;
    color: {text_color} !important;
    border: 1px solid {border_color} !important;
    border-radius: 8px !important;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.06) !important;
}}

/* Expander styling */
.st-emotion-cache-1gulkj5 {{
    background-color: {card_bg} !important;
    color: {text_color} !important;
    border: 1px solid {border_color} !important;
    border-radius: 8px !important;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.06) !important;
}}

/* Ensure all text is visible */
p, h1, h2, h3, h4, h5, h6, span, div {{
    color: {text_color} !important;
}}

/* Ensure all alerts are visible */
.stAlert p {{
    color: inherit !important;
}}

/* Make "Drag and drop file here" text more visible */
.css-1aehpvj, .css-50ug3q, .css-1v0mbdj {{
    color: {accent_color} !important;
    font-weight: 600 !important;
}}

/* Make theme toggle button more visible */
[data-testid="stSidebar"] [data-testid="stButton"] {{
    background-color: {accent_color} !important;
    color: white !important;
    border: none !important;
    border-radius: 8px !important;
    padding: 12px 16px !important;
    font-weight: 600 !important;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1) !important;
    transition: all 0.2s ease !important;
}}

[data-testid="stSidebar"] [data-testid="stButton"]:hover {{
    background-color: {button_hover} !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 6px 8px rgba(0, 0, 0, 0.15) !important;
}}

/* Add more sophisticated styling */
.stSelectbox, .stTextInput {{
    border-radius: 8px !important;
}}

.stSelectbox > div > div, .stTextInput > div > div > input {{
    background-color: {card_bg} !important;
    border: 1px solid {border_color} !important;
    border-radius: 8px !important;
    color: {text_color} !important;
    font-weight: 500 !important;
}}

/* Add subtle transitions */
button, .stSelectbox, .stTextInput, .stFileUploader {{
    transition: all 0.2s ease !important;
}}

/* Use generous spacing */
.main .block-container {{
    padding: 2rem !important;
}}

/* Add subtle shadows to cards */
.stExpander {{
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.06) !important;
    border-radius: 8px !important;
    overflow: hidden !important;
}}
</style>
""", unsafe_allow_html=True)

# --- Auth State ---
if 'auth_mode' not in st.session_state:
    st.session_state.auth_mode = 'login'

# --- Figma-based Auth Forms ---
def login_form():
    # Store auth handler in session state
    st.session_state.auth_handler = auth
    
    # Render Figma login form
    render_figma_login_form()

def signup_form():
    # Store auth handler in session state
    st.session_state.auth_handler = auth
    
    # Render Figma signup form
    render_figma_signup_form()

# --- Initialize authentication state ---
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False

# --- Check for logout request ---
params = st.query_params
if 'logout' in params and params['logout'] == 'true':
    auth.logout()
    st.query_params.clear()
    st.rerun()

# --- Main App Flow ---
if not auth.require_auth():
    if st.session_state.auth_mode == 'login':
        login_form()
    else:
        signup_form()
    st.stop()

# --- Get Current User ---
try:
    current_user = auth.get_current_user()
    st.session_state.current_user = current_user
except Exception as e:
    st.error(f"Error getting current user: {str(e)}")
    current_user = None
    st.session_state.current_user = None

# --- Get User Data ---
try:
    user_id = current_user.id if current_user and hasattr(current_user, 'id') else None
    analyses = db_service.get_user_analyses(user_id) if user_id else []
except Exception as e:
    st.error(f"Error getting user data: {str(e)}")
    user_id = None
    analyses = []

# Store whether user has analyses (handle None case)
st.session_state.has_analyses = len(analyses) > 0 if analyses is not None else False

# Welcome tour removed as requested

# --- Render Navigation Bar ---
# Import and render navbar at the top with error handling
try:
    from figma_ui_fixed import render_navigation_bar
    render_navigation_bar(current_user)
except Exception as e:
    st.error(f"Navigation bar error: {str(e)}")
    # Fallback navigation
    st.markdown("## PitchPerfect AI")

# --- Render Sidebar ---
# Import and render sidebar directly here to avoid import errors
try:
    from sidebar import render_figma_sidebar
    # Ensure analyses is never None before passing to sidebar
    analyses_to_render = analyses if analyses is not None else []
    render_figma_sidebar(current_user, analyses_to_render)
except Exception as e:
    st.error(f"Sidebar error: {str(e)}")
    # Continue without sidebar

# --- File Upload Section ---
uploaded_file = st.file_uploader("Upload your pitch deck", type=["pdf", "pptx", "docx", "txt"])

# Show sample analysis option for new users
show_sample_analysis = show_sample_analysis_option()

if uploaded_file:
    # Validate uploaded file
    is_valid, error_msg, safe_filename = validate_file_upload(uploaded_file)
    
    if not is_valid:
        st.error(f"❌ File validation failed: {error_msg}")
        st.stop()
    
    if error_msg and "Warning" in error_msg:
        st.warning(error_msg)
    
    # File info with theme support
    filetype = os.path.splitext(safe_filename)[1].lower()
    filesize = uploaded_file.size / 1024
    
    # Get current theme
    dark_mode = st.session_state.get('dark_mode', False)
    
    # Set theme-based colors
    bg_color = "#1F2937" if dark_mode else "#FFFFFF"
    text_color = "#F9FAFB" if dark_mode else "#1E293B"
    text_secondary = "#D1D5DB" if dark_mode else "#64748B"
    border_color = "#374151" if dark_mode else "#E2E8F0"
    
    st.markdown(f"""
    <div style='background: {bg_color}; border-radius: 12px; padding: 1.5rem; margin: 1rem 0; border: 1px solid {border_color}; box-shadow: 0 2px 8px rgba(0, 0, 0, {0.2 if dark_mode else 0.04});'>
        <div style='display: flex; align-items: center; gap: 1rem;'>
            <div style='font-size: 2rem; color: #6366F1;'>📄</div>
            <div>
                <div style='font-weight: 600; color: {text_color}; font-size: 1rem;'>{safe_filename}</div>
                <div style='color: {text_secondary}; font-size: 0.875rem;'>{filetype.upper()} • {filesize:.1f} KB</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Extract text from file
    with tempfile.NamedTemporaryFile(delete=False, suffix=filetype) as tmp_file:
        tmp_file.write(uploaded_file.read())
        tmp_path = tmp_file.name
    
    text = extract_text(tmp_path, filetype)
    os.unlink(tmp_path)
    
    if not text:
        st.error("❌ Could not extract text from the uploaded file.")
    else:
        # Figma loading animation
        loading_placeholder = st.empty()
        with loading_placeholder.container():
            render_figma_loading()
        
        # Basic analysis with caching
        try:
            # Use cached analysis if available
            analysis_results = analyze_text_cached(text)
            score = analysis_results['score']
            strengths = analysis_results['strengths']
            weaknesses = analysis_results['weaknesses']
            tips = analysis_results['tips']
            section_scores = analysis_results['section_scores']
            read_score = analysis_results['read_score']
            sentiment = analysis_results['sentiment']
            keywords = analysis_results['keywords']
        except Exception:
            # Fallback to direct analysis if caching fails
            score, strengths, weaknesses, tips, section_scores = analyze_sections(text)
            read_score = readability_score(text)
            sentiment = sentiment_scores(text)
            keywords = extract_keywords(text)
        
        # Advanced analysis
        advanced_results = advanced_analyzer.calculate_pitch_quality_score(text)
        grade = advanced_results.get('grade', 'B+')
        
        # Clear loading animation
        loading_placeholder.empty()
        
        # Navigation bar is handled in the main content area
        
        # Show text preview
        with st.expander("📄 View Extracted Text", expanded=False):
            st.code(text[:2000] + ("..." if len(text) > 2000 else ""), language=None)
        
        # Render interactive dashboard with tooltips
        render_interactive_dashboard(
            score, read_score, sentiment, grade, 
            advanced_results.get('overall_score', 75),
            strengths, weaknesses, tips, keywords,
            advanced_results.get('recommendations', [])
        )
        
        # AI Recommendations with theme support
        recommendations = advanced_results.get('recommendations', [])
        if recommendations:
            # Get current theme
            dark_mode = st.session_state.get('dark_mode', False)
            
            # Set theme-based colors
            bg_color = "#1F2937" if dark_mode else "#FFFFFF"
            text_color = "#F9FAFB" if dark_mode else "#1E293B"
            border_color = "#374151" if dark_mode else "#E2E8F0"
            card_bg = "#111827" if dark_mode else "#F8FAFC"
            text_secondary = "#D1D5DB" if dark_mode else "#475569"
            
            st.markdown(f"""
            <div style='background: {bg_color}; border-radius: 16px; padding: 2rem; margin: 2rem 0; border: 1px solid {border_color}; box-shadow: 0 4px 20px rgba(0, 0, 0, {0.2 if dark_mode else 0.08});'>
                <div style='font-size: 1.5rem; font-weight: 700; color: {text_color}; margin-bottom: 1.5rem; display: flex; align-items: center; gap: 0.75rem;'>
                    🤖 AI Recommendations
                </div>
            """, unsafe_allow_html=True)
            
            for i, rec in enumerate(recommendations, 1):
                st.markdown(f"""
                <div style='background: {card_bg}; border-left: 4px solid #6366F1; padding: 1rem; margin: 0.75rem 0; border-radius: 0 8px 8px 0; border: 1px solid {border_color};'>
                    <strong style='color: {text_color};'>{i}.</strong> <span style='color: {text_secondary};'>{rec}</span>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown("</div>", unsafe_allow_html=True)
        
        # Create analysis data dictionary
        analysis_data = {
            'filename': safe_filename,
            'score': score,
            'readability': read_score,
            'sentiment': sentiment,
            'strengths': strengths,
            'weaknesses': weaknesses,
            'tips': tips,
            'keywords': keywords,
            'section_scores': section_scores,
            'advanced_results': advanced_results
        }
        
        # Display PDF download button
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            display_download_button(analysis_data, safe_filename)
        
        # Add summary to analysis data
        summary = f"PitchPerfect Analysis for {safe_filename}\n\nOverall Grade: {grade} ({advanced_results.get('overall_score', 75)}/100)\nSection Coverage: {score}/10\nReadability: {read_score:.1f}\nSentiment: {sentiment}\n\nStrengths: {', '.join(strengths)}\nWeaknesses: {', '.join(weaknesses)}\nRecommendations: {', '.join(recommendations)}\nKeywords: {', '.join(keywords)}\n"
        analysis_data['summary'] = summary
        
        # Save to database using the database service
        try:
            if db_service.save_analysis(user_id, analysis_data):
                render_figma_success("Analysis Complete!", "Your pitch deck has been analyzed and saved to your history!")
            else:
                # Show success message even if database save fails
                render_figma_success("Analysis Complete!", "Your pitch deck has been analyzed successfully!")
        except Exception:
            # Show success message even if database save fails
            render_figma_success("Analysis Complete!", "Your pitch deck has been analyzed successfully!")
        
elif show_sample_analysis:
    # Show sample analysis for new users
    # Ensure navbar is visible for sample analysis
    from figma_ui_fixed import render_navigation_bar
    render_navigation_bar(current_user)
    
    st.markdown("### 📊 Sample Analysis")
    st.info("This is a sample analysis to help you understand how PitchPerfect works.")
    
    # Load sample data
    sample_score = 8
    sample_read_score = 75.5
    sample_sentiment = "Positive"
    sample_grade = "A-"
    sample_overall_score = 85
    sample_strengths = ["Clear problem statement", "Strong value proposition", "Compelling market analysis"]
    sample_weaknesses = ["Financial projections need more detail", "Competition analysis is limited"]
    sample_tips = ["Add more specific metrics", "Include customer testimonials", "Clarify go-to-market strategy"]
    sample_keywords = ["SaaS", "B2B", "Market Fit", "Scalability", "Innovation", "Growth"]
    sample_recommendations = ["Strengthen your financial section with more detailed projections", 
                            "Add competitive analysis with direct comparisons", 
                            "Include more visuals to support key points"]
    
    # Render interactive dashboard with sample data
    render_interactive_dashboard(
        sample_score, sample_read_score, sample_sentiment, sample_grade, 
        sample_overall_score, sample_strengths, sample_weaknesses, 
        sample_tips, sample_keywords, sample_recommendations
    )
    # Navigation bar is handled in the main content area
else:
    # Show main content area when no file is uploaded
    render_figma_main_content(current_user)
