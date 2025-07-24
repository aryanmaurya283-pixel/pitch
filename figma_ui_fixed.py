import streamlit as st
from typing import Dict, Any
import requests

# --- 1. CORE STYLING AND LAYOUT CORRECTION ---
def apply_global_styles(dark_mode=False):
    """
    Applies global CSS styles to hide Streamlit defaults, set fonts, 
    and fix the main content padding to accommodate the fixed navbar.
    """
    if dark_mode:
        bg_color = "#0F172A"
        text_primary = "#F1F5F9"
    else:
        bg_color = "#F8FAFC"
        text_primary = "#1F2937"

    st.markdown(f"""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;700;800&display=swap');
        
        /* --- Basic Reset and Font --- */
        html, body, [class*="st-"] {{
            font-family: 'Plus Jakarta Sans', sans-serif !important;
            -webkit-font-smoothing: antialiased;
            color: {text_primary};
        }}

        /* --- Hide Streamlit's default elements --- */
        #MainMenu, footer, header, .stDeployButton {{
            display: none !important;
            visibility: hidden !important;
        }}

        /* --- Main App Styling --- */
        .stApp {{
            background-color: {bg_color} !important;
        }}

        /* --- CRITICAL LAYOUT FIX --- */
        [data-testid="stAppViewContainer"] > section {{
            padding-top: 90px !important;
        }}
        

    </style>
    """, unsafe_allow_html=True)

def extract_user_data_safely(current_user):
    """Safely extract user data with fallback values."""
    try:
        if current_user and hasattr(current_user, 'user_metadata') and current_user.user_metadata:
            user_name = current_user.user_metadata.get('name', 'User')
        else:
            user_name = current_user.get('name', 'User') if current_user else 'User'
        
        if current_user and hasattr(current_user, 'email') and current_user.email:
            user_email = current_user.email
        else:
            user_email = current_user.get('email', 'user@example.com') if current_user else 'user@example.com'
            
        # Ensure user_name is a string and not empty
        if not isinstance(user_name, str) or not user_name.strip():
            user_name = 'User'
            
        user_initial = user_name[0].upper() if user_name else 'U'
        
        return {
            'name': user_name,
            'email': user_email,
            'initial': user_initial
        }
    except Exception as e:
        # Fallback to default values on any error
        return {
            'name': 'User',
            'email': 'user@example.com',
            'initial': 'U'
        }

# --- 2. NAVIGATION BAR COMPONENT ---
def render_navigation_bar(current_user: Dict[str, Any]):
    """Renders the fixed navbar with branding and user info only, using the new palette."""
    nav_bg_color = "rgba(255, 255, 255, 0.95)"
    text_color = "#1F2937"
    border_color = "#E5E7EB"
    accent_color = "#6366F1"
    user_bg_color = "rgba(99, 102, 241, 0.08)"
    user_data = extract_user_data_safely(current_user)
    user_initial = user_data['initial']
    user_name = user_data['name']
    st.markdown(f"""
    <style>
    .navbar-container {{
        position: fixed; top: 0; left: 0; width: 100%; height: 70px;
        background-color: {nav_bg_color};
        backdrop-filter: blur(10px); -webkit-backdrop-filter: blur(10px);
        border-bottom: 1px solid {border_color};
        display: flex; justify-content: space-between; align-items: center;
        padding: 0 40px; z-index: 9999;
    }}
    .navbar-left {{ display: flex; align-items: center; }}
    .navbar-logo {{ display: flex; align-items: center; gap: 12px; font-size: 20px; font-weight: 700; color: {text_color}; }}
    .navbar-logo-icon {{ font-size: 24px; }}
    .navbar-right {{ display: flex; align-items: center; gap: 24px; }}
    .navbar-user-section {{ display: flex; align-items: center; gap: 10px; background: {user_bg_color}; border-radius: 24px; padding: 6px 16px; }}
    .navbar-user-avatar {{ width: 32px; height: 32px; background: {accent_color}; border-radius: 50%; display: flex; align-items: center; justify-content: center; color: white; font-weight: 600; font-size: 16px; }}
    .navbar-user-name {{ font-size: 14px; font-weight: 600; color: {text_color}; }}
    @media (max-width: 600px) {{
        .navbar-container {{ flex-direction: column; height: auto; padding: 10px 10px; }}
        .navbar-right {{ gap: 10px; flex-wrap: wrap; }}
        .navbar-user-section {{ padding: 6px 8px; }}
    }}
    </style>
    <div class="navbar-container">
        <div class="navbar-left">
            <div class="navbar-logo"><span class="navbar-logo-icon">🚀</span><span>PitchPerfect AI</span></div>
        </div>
        <div class="navbar-right">
            <div class="navbar-user-section"><div class="navbar-user-avatar">{user_initial}</div><div class="navbar-user-name">{user_name}</div></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def handle_navbar_actions():
    """Handle navbar actions via URL parameters - simple approach."""
    # Initialize dark mode if not set
    if 'dark_mode' not in st.session_state:
        st.session_state.dark_mode = False
    
    # Check URL parameters
    query_params = st.query_params
    
    if 'toggle_theme' in query_params:
        st.session_state.dark_mode = not st.session_state.dark_mode
        # Clear the parameter and rerun
        st.query_params.clear()
        st.rerun()
    
    if 'logout' in query_params:
        st.session_state.authenticated = False
        if 'logged_in' in st.session_state:
            st.session_state.logged_in = False
        # Clear the parameter and rerun
        st.query_params.clear()
        st.rerun()

# --- 3. MAIN CONTENT COMPONENT ---
def render_figma_main_content():
    """
    Renders a visually appealing and integrated main content area for file upload.
    """
    import streamlit as st
    from file_validator import validate_file_upload
    from text_extractor import extract_text
    from nlp_utils import comprehensive_analysis
    from figma_ui_fixed import render_figma_analysis_results, render_figma_success
    from datetime import datetime

    # Get theme from session state
    dark_mode = st.session_state.get('dark_mode', False)
    
    if dark_mode:
        page_bg = "#0F172A"
        card_bg = "#1E293B"
        border_color = "#334155"
        accent_color = "#6366F1"
        text_primary = "#F1F5F9"
        text_secondary = "#CBD5E1"
        upload_bg_hover = "#1E293B"
        shadow = "0 4px 20px rgba(0, 0, 0, 0.3)"
        gradient_bg = "linear-gradient(135deg, #1E293B 0%, #0F172A 100%)"
    else:
        page_bg = "#F8FAFC"
        card_bg = "#FFFFFF"
        border_color = "#E5E7EB"
        accent_color = "#4F46E5"
        text_primary = "#1F2937"
        text_secondary = "#6B7280"
        upload_bg_hover = "#F3F4F6"
        shadow = "0 4px 20px rgba(0, 0, 0, 0.08)"
        gradient_bg = "linear-gradient(135deg, #FFFFFF 0%, #F8FAFC 100%)"

    st.markdown(f"""
    <style>
        body, .main, .block-container {{
            background: {page_bg} !important;
        }}
        .upload-area-outer {{
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            min-height: 60vh;
        }}
        .upload-box {{
            background: {gradient_bg};
            border: 2px dashed {accent_color}40;
            border-radius: 24px;
            padding: 60px 40px;
            text-align: center;
            transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
            cursor: pointer;
            margin: 0 auto;
            box-shadow: {shadow};
            position: relative;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            width: 100%;
            max-width: 600px;
            backdrop-filter: blur(10px);
        }}
        .upload-box:hover {{
            border-color: {accent_color};
            background: {card_bg};
            transform: translateY(-4px) scale(1.02);
            box-shadow: 0 8px 32px {accent_color}20;
        }}
        .upload-icon-folder {{
            font-size: 64px;
            color: {accent_color};
            margin-bottom: 24px;
            display: block;
            filter: drop-shadow(0 4px 8px {accent_color}20);
        }}
        .upload-text-main {{
            font-size: 28px;
            font-weight: 800;
            color: {text_primary};
            margin-bottom: 12px;
            letter-spacing: -0.8px;
            display: block;
        }}
        .upload-text-secondary {{
            font-size: 16px;
            color: {text_secondary};
            margin-top: 4px;
            margin-bottom: 24px;
            display: block;
            line-height: 1.5;
        }}
        .upload-cta-button {{
            background: linear-gradient(135deg, {accent_color} 0%, {accent_color}DD 100%);
            color: white;
            border: none;
            border-radius: 12px;
            padding: 14px 28px;
            font-size: 16px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s ease;
            box-shadow: 0 4px 16px {accent_color}40;
            margin-top: 8px;
        }}
        .upload-cta-button:hover {{
            transform: translateY(-2px);
            box-shadow: 0 6px 20px {accent_color}60;
        }}
        /* Streamlit file uploader custom styles */
        .stFileUploader {{
            background: #fff !important;
            border-radius: 12px !important;
            color: {text_primary} !important;
            box-shadow: none !important;
            border: 1.5px solid {border_color} !important;
            margin-top: 18px;
        }}
        .stFileUploader > div {{
            padding: 0 !important;
            border: none !important;
            background: none !important;
        }}
        .stFileUploader label {{
            display: none !important;
        }}
        .stFileUploader .uploadedFileName {{
            color: {text_primary} !important;
        }}
        .stFileUploader .css-1cpxqw2, .stFileUploader .css-1cpxqw2 input {{
            color: {text_primary} !important;
            font-size: 16px !important;
            font-weight: 600 !important;
        }}
        .stFileUploader .css-1cpxqw2 input[type="file"]::-webkit-file-upload-button {{
            background: {accent_color};
            color: #fff;
            border: none;
            border-radius: 8px;
            padding: 12px 28px;
            font-size: 16px;
            font-weight: 700;
            cursor: pointer;
            margin-top: 8px;
        }}
        .stFileUploader .css-1cpxqw2 input[type="file"]::-ms-browse {{
            background: {accent_color};
            color: #fff;
        }}
        .stFileUploader .css-1cpxqw2 input[type="file"]::-moz-browse {{
            background: {accent_color};
            color: #fff;
        }}
        .stFileUploader .css-1cpxqw2 input[type="file"]::-o-browse {{
            background: {accent_color};
            color: #fff;
        }}
        @media (max-width: 700px) {{
            .upload-box {{ padding: 24px 8px 16px 8px; }}
        }}
    </style>
    <div class="upload-area-outer">
        <div class="upload-box">
            <div class="upload-icon-folder">📁</div>
            <div class="upload-text-main">Upload your pitch deck</div>
            <div class="upload-text-secondary">PDF, PPTX, DOCX, or TXT &bull; Max 200MB</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    with st.container():
        st.markdown(f'<div style="display: flex; flex-direction: column; align-items: center; justify-content: center; margin-top: -180px;">', unsafe_allow_html=True)
        uploaded_file = st.file_uploader(
            "Upload your pitch deck",
            type=["pdf", "pptx", "docx", "txt"],
            label_visibility="collapsed"
        )
        st.markdown("</div>", unsafe_allow_html=True)

    if uploaded_file:
        is_valid, error_message, safe_filename = validate_file_upload(uploaded_file)
        if not is_valid:
            st.error(f"File validation failed: {error_message}")
            return
        filetype = '.' + safe_filename.split('.')[-1].lower()
        with st.spinner("Extracting text from your file..."):
            text = extract_text(uploaded_file, filetype)
        if not text or len(text.strip()) < 50:
            st.error("Could not extract enough text from your file. Please upload a valid pitch deck.")
            return
        with st.spinner("Analyzing your pitch deck with AI..."):
            analysis = comprehensive_analysis(text)
        # --- Save analysis to Supabase ---
        db_service = st.session_state.db_service
        user = st.session_state.current_user
        user_id = user.get('id') if isinstance(user, dict) else getattr(user, 'id', None)
        if user_id and uploaded_file:
            try:
                db_service.save_analysis(user_id, {
                    "filename": uploaded_file.name,
                    "analysis_data": analysis,
                    "date": str(datetime.now())
                })
                st.info("Analysis saved to your history.")
            except Exception as e:
                st.warning(f"Could not save analysis: {e}")
        # --- Render results as before ---
        basic = analysis['basic']
        render_figma_analysis_results(
            basic['score'],
            basic['readability'],
            basic['sentiment'],
            analysis['overall_grade'],
            int((basic['score']/10)*100),
            basic['strengths'],
            basic['weaknesses'],
            basic['tips'],
            basic['keywords'],
            analysis.get('recommendations', [])
        )
        render_figma_success("Analysis Complete!", "Your pitch deck has been analyzed. See the insights above.")
    return uploaded_file

def render_figma_analysis_results(score, read_score, sentiment, grade, overall_score, strengths, weaknesses, tips, keywords, recommendations):
    """Render analysis results with improved design and theme support."""
    # Get theme from session state
    dark_mode = st.session_state.get('dark_mode', False)
    
    if dark_mode:
        main_bg = "#0F172A"
        card_bg = "#1E293B"
        border_color = "#334155"
        text_primary = "#F1F5F9"
        text_secondary = "#CBD5E1"
        accent_color = "#6366F1"
        success_color = "#10B981"
        warning_color = "#F59E0B"
        error_color = "#EF4444"
        info_color = "#3B82F6"
    else:
        main_bg = "#F8FAFC"
        card_bg = "#FFFFFF"
        border_color = "#E5E7EB"
        text_primary = "#1F2937"
        text_secondary = "#6B7280"
        accent_color = "#4F46E5"
        success_color = "#059669"
        warning_color = "#D97706"
        error_color = "#DC2626"
        info_color = "#2563EB"
    st.markdown(f"""
    <style>
    .main-content {{
        padding-top: 80px;
        background: {main_bg} !important;
        min-height: 100vh;
    }}
    .results-header {{
        text-align: center;
        margin-bottom: 40px;
        padding: 32px;
        background: linear-gradient(135deg, {accent_color}10 0%, {accent_color}05 100%);
        border-radius: 20px;
        border: 1px solid {border_color};
    }}
    .metric-card {{ 
        background: {card_bg};
        border: 1px solid {border_color};
        border-radius: 16px;
        padding: 24px;
        text-align: center;
        transition: all 0.3s ease;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
    }}
    .metric-card:hover {{
        transform: translateY(-4px);
        box-shadow: 0 8px 24px rgba(0,0,0,0.1);
        border-color: {accent_color};
    }}
    .metric-label {{ 
        font-size: 14px; 
        color: {text_secondary}; 
        font-weight: 600; 
        margin-bottom: 8px;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }}
    .metric-value {{ 
        font-size: 32px; 
        font-weight: 800; 
        color: {accent_color};
        line-height: 1;
    }}
    .analysis-section {{
        background: {card_bg};
        border: 1px solid {border_color};
        border-radius: 16px;
        padding: 28px;
        margin-bottom: 24px;
        transition: all 0.3s ease;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
    }}
    .analysis-section:hover {{
        transform: translateY(-2px);
        box-shadow: 0 8px 24px rgba(0,0,0,0.1);
    }}
    .analysis-section h3 {{
        font-size: 20px;
        font-weight: 700;
        color: {text_primary};
        margin-bottom: 20px;
        display: flex;
        align-items: center;
        gap: 12px;
        padding-bottom: 12px;
        border-bottom: 2px solid {border_color};
    }}
    .figma-tag {{
        display: inline-block;
        padding: 8px 16px;
        border-radius: 20px;
        font-size: 14px;
        font-weight: 600;
        margin: 4px;
        transition: all 0.2s ease;
    }}
    .tag-success {{
        background: {success_color}15;
        color: {success_color};
        border: 1px solid {success_color}30;
    }}
    .tag-error {{
        background: {error_color}15;
        color: {error_color};
        border: 1px solid {error_color}30;
    }}
    .tag-warning {{
        background: {warning_color}15;
        color: {warning_color};
        border: 1px solid {warning_color}30;
    }}
    .tag-info {{
        background: {info_color}15;
        color: {info_color};
        border: 1px solid {info_color}30;
    }}
    .figma-tag:hover {{
        transform: translateY(-1px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }}
    </style>
    """, unsafe_allow_html=True)
    st.markdown(f"""
    <div class="main-content">
        <div class="results-header">
            <div style="font-size: 48px; margin-bottom: 16px;">🎯</div>
            <h1 style="font-size: 32px; font-weight: 800; color: {text_primary}; margin-bottom: 12px; letter-spacing: -0.5px;">
                Analysis Complete!
            </h1>
            <p style="font-size: 18px; color: {text_secondary}; margin: 0; line-height: 1.5;">
                Here's your comprehensive pitch deck analysis with actionable insights
            </p>
        </div>
        <div style="margin-bottom: 40px;">
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; margin-bottom: 32px;">
                <div class="metric-card">
                    <div class="metric-label">Section Coverage</div>
                    <div class="metric-value">{score}/10</div>
                </div>
                <div class="metric-card">
                    <div class="metric-label">Readability</div>
                    <div class="metric-value">{read_score:.0f}</div>
                </div>
                <div class="metric-card">
                    <div class="metric-label">Overall Score</div>
                    <div class="metric-value">{overall_score}/100</div>
                </div>
                <div class="metric-card">
                    <div class="metric-label">Grade</div>
                    <div class="metric-value">{grade}</div>
                </div>
            </div>
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 24px;">
                <div class="analysis-section">
                    <h3>✨ Strengths</h3>
                    <div style="display: flex; flex-wrap: wrap; gap: 8px;">
    """, unsafe_allow_html=True)
    for strength in strengths:
        st.markdown(f'<span class="figma-tag tag-success">{strength}</span>', unsafe_allow_html=True)
    st.markdown("</div></div>", unsafe_allow_html=True)
    st.markdown(f"""
                <div class="analysis-section">
                    <h3>⚠️ Areas to Improve</h3>
                    <div style="display: flex; flex-wrap: wrap; gap: 8px;">
    """, unsafe_allow_html=True)
    for weakness in weaknesses:
        st.markdown(f'<span class="figma-tag tag-error">{weakness}</span>', unsafe_allow_html=True)
    st.markdown("</div></div>", unsafe_allow_html=True)
    st.markdown(f"""
                <div class="analysis-section">
                    <h3>💡 Recommendations</h3>
                    <div style="display: flex; flex-wrap: wrap; gap: 8px;">
    """, unsafe_allow_html=True)
    for tip in tips:
        st.markdown(f'<span class="figma-tag tag-warning">{tip}</span>', unsafe_allow_html=True)
    st.markdown("</div></div>", unsafe_allow_html=True)
    st.markdown(f"""
                <div class="analysis-section">
                    <h3>🔑 Key Terms</h3>
                    <div style="display: flex; flex-wrap: wrap; gap: 8px;">
    """, unsafe_allow_html=True)
    for keyword in keywords:
        st.markdown(f'<span class="figma-tag tag-info">{keyword}</span>', unsafe_allow_html=True)
    st.markdown("</div></div></div></div></div>", unsafe_allow_html=True)

def render_figma_loading():
    """Render loading animation with Figma design."""
    dark_mode = st.session_state.get('dark_mode', False)
    
    if dark_mode:
        bg_color = "#0F172A"
        text_color = "#F1F5F9"
        accent_color = "#6366F1"
        card_bg = "#1E293B"
    else:
        bg_color = "#F8FAFC"
        text_color = "#1F2937"
        accent_color = "#4F46E5"
        card_bg = "#FFFFFF"
    
    st.markdown(f"""
    <style>
        .loading-container {{
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            min-height: 400px;
            background: {card_bg};
            border-radius: 16px;
            padding: 40px;
            margin: 20px auto;
            max-width: 600px;
        }}
        
        .loading-spinner {{
            width: 60px;
            height: 60px;
            border: 4px solid rgba(99, 102, 241, 0.1);
            border-left: 4px solid {accent_color};
            border-radius: 50%;
            animation: spin 1s linear infinite;
            margin-bottom: 24px;
        }}
        
        @keyframes spin {{
            0% {{ transform: rotate(0deg); }}
            100% {{ transform: rotate(360deg); }}
        }}
        
        .loading-text {{
            font-size: 18px;
            font-weight: 600;
            color: {text_color};
            margin-bottom: 8px;
        }}
        
        .loading-subtext {{
            font-size: 14px;
            color: {text_color}80;
            text-align: center;
            max-width: 400px;
        }}
    </style>
    
    <div class="loading-container">
        <div class="loading-spinner"></div>
        <div class="loading-text">Analyzing your pitch deck...</div>
        <div class="loading-subtext">
            Our AI is examining your presentation structure, content quality, and providing insights to help you succeed.
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_figma_success(title="Success!", message="Operation completed successfully"):
    """Render success message with Figma design."""
    dark_mode = st.session_state.get('dark_mode', False)
    
    if dark_mode:
        bg_color = "#0F172A"
        text_color = "#F1F5F9"
        text_secondary = "#CBD5E1"
        success_color = "#10B981"
        card_bg = "#1E293B"
    else:
        bg_color = "#F8FAFC"
        text_color = "#1F2937"
        text_secondary = "#6B7280"
        success_color = "#10B981"
        card_bg = "#FFFFFF"
    
    st.markdown(f"""
    <style>
        .success-container {{
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            background: {card_bg};
            border: 2px solid {success_color};
            border-radius: 16px;
            padding: 32px;
            margin: 20px auto;
            max-width: 600px;
            text-align: center;
        }}
        
        .success-icon {{
            width: 60px;
            height: 60px;
            background: {success_color};
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 30px;
            color: white;
            margin-bottom: 16px;
        }}
        
        .success-title {{
            font-size: 20px;
            font-weight: 700;
            color: {text_color};
            margin-bottom: 8px;
        }}
        
        .success-message {{
            font-size: 16px;
            color: {text_secondary};
            line-height: 1.5;
        }}
    </style>
    
    <div class="success-container">
        <div class="success-icon">✓</div>
        <div class="success-title">{title}</div>
        <div class="success-message">{message}</div>
    </div>
    """, unsafe_allow_html=True)

# --- 4. MAIN APPLICATION LOGIC ---
def main():
    st.set_page_config(layout="wide")

    # --- Initialize Session State ---
    if 'dark_mode' not in st.session_state:
        st.session_state.dark_mode = False
    if 'current_user' not in st.session_state:
        st.session_state.current_user = {'name': 'Alex Doe', 'email': 'alex.doe@example.com'}
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = True

    # --- Apply Styles and Render Static Components ---
    apply_global_styles(st.session_state.dark_mode)
    
    # --- Main App Flow ---
    if not st.session_state.logged_in:
        st.title("You have been logged out.")
        st.info("Please refresh the page to log back in.")  # In a real app, you'd redirect
        st.stop()

    # Render the navigation bar, passing the current theme state
    render_navigation_bar(st.session_state.current_user)

    # --- Page Content ---
    render_figma_main_content()

if __name__ == "__main__":
    main()