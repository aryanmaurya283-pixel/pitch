import streamlit as st
from typing import Dict, List, Any

def render_figma_styles(dark_mode=False):
    """Render styles based on Figma design system."""
    # Figma design colors
    primary_blue = "#4F7EFF"
    primary_purple = "#7C3AED"
    success_green = "#10B981"
    warning_orange = "#F59E0B"
    error_red = "#EF4444"
    
    # Theme colors from Figma - exact match
    bg_color = "#1A1A1A" if dark_mode else "#F8F9FA"
    text_primary = "#FFFFFF" if dark_mode else "#1A1A1A"
    text_secondary = "#A0A0A0" if dark_mode else "#6B7280"
    card_bg = "#2A2A2A" if dark_mode else "#FFFFFF"
    border_color = "#3A3A3A" if dark_mode else "#E5E7EB"
    sidebar_bg = "#1F1F1F" if dark_mode else "#FFFFFF"
    main_bg = "#1A1A1A" if dark_mode else "#F8F9FA"
    
    st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');
    
    * {{
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }}
    
    .stApp {{
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
        background: {main_bg} !important;
        color: {text_primary} !important;
        line-height: 1.6 !important;
        -webkit-font-smoothing: antialiased !important;
    }}
    
    .main .block-container {{
        padding: 0 !important;
        max-width: none !important;
    }}
    
    /* Hide Streamlit elements */
    #MainMenu, footer, header, .stDeployButton {{
        visibility: hidden !important;
        height: 0 !important;
    }}
    
    /* Sidebar Layout */
    .sidebar {{
        position: fixed;
        left: 0;
        top: 0;
        width: 280px;
        height: 100vh;
        background: {sidebar_bg};
        border-right: 1px solid {border_color};
        padding: 24px;
        z-index: 1000;
        overflow-y: auto;
    }}
    
    .main-content {{
        margin-left: 280px;
        min-height: 100vh;
        background: {main_bg};
        padding: 40px;
    }}
    
    /* Logo Section */
    .logo-section {{
        display: flex;
        align-items: center;
        gap: 12px;
        margin-bottom: 32px;
    }}
    
    .logo-icon {{
        width: 32px;
        height: 32px;
        background: {primary_blue};
        border-radius: 8px;
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        font-size: 16px;
    }}
    
    .logo-text {{
        font-size: 18px;
        font-weight: 700;
        color: {text_primary};
    }}
    
    .logo-subtitle {{
        font-size: 12px;
        color: {text_secondary};
        margin-top: 2px;
    }}
    
    /* Upload Button */
    .upload-btn {{
        width: 100%;
        background: {primary_blue};
        color: white;
        border: none;
        border-radius: 8px;
        padding: 12px 16px;
        font-weight: 600;
        font-size: 14px;
        cursor: pointer;
        margin-bottom: 32px;
        display: flex;
        align-items: center;
        gap: 8px;
        transition: all 0.2s ease;
    }}
    
    .upload-btn:hover {{
        background: #3B6EFF;
        transform: translateY(-1px);
    }}
    
    /* Past Analyses Section */
    .past-analyses {{
        margin-bottom: 32px;
    }}
    
    .section-title {{
        font-size: 14px;
        font-weight: 600;
        color: {text_primary};
        margin-bottom: 16px;
        display: flex;
        align-items: center;
        gap: 8px;
    }}
    
    .analysis-item {{
        background: {card_bg};
        border: 1px solid {border_color};
        border-radius: 8px;
        padding: 12px;
        margin-bottom: 8px;
        cursor: pointer;
        transition: all 0.2s ease;
    }}
    
    .analysis-item:hover {{
        border-color: {primary_blue};
        transform: translateY(-1px);
    }}
    
    .analysis-name {{
        font-size: 14px;
        font-weight: 600;
        color: {text_primary};
        margin-bottom: 4px;
    }}
    
    .analysis-date {{
        font-size: 12px;
        color: {text_secondary};
    }}
    
    .analysis-score {{
        background: {success_green};
        color: white;
        font-size: 10px;
        font-weight: 600;
        padding: 2px 6px;
        border-radius: 4px;
        float: right;
        margin-top: -20px;
    }}
    
    /* User Profile */
    .user-profile {{
        position: absolute;
        bottom: 24px;
        left: 24px;
        right: 24px;
        display: flex;
        align-items: center;
        gap: 12px;
        padding: 12px;
        background: {card_bg};
        border: 1px solid {border_color};
        border-radius: 8px;
    }}
    
    .user-avatar {{
        width: 32px;
        height: 32px;
        background: {primary_blue};
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        font-weight: 600;
        font-size: 14px;
    }}
    
    .user-info {{
        flex: 1;
    }}
    
    .user-name {{
        font-size: 14px;
        font-weight: 600;
        color: {text_primary};
    }}
    
    .user-email {{
        font-size: 12px;
        color: {text_secondary};
    }}
    
    /* Theme Toggle */
    .theme-toggle {{
        background: none;
        border: none;
        color: {text_secondary};
        cursor: pointer;
        padding: 8px;
        border-radius: 6px;
        transition: all 0.2s ease;
    }}
    
    .theme-toggle:hover {{
        background: {border_color};
        color: {text_primary};
    }}
    
    /* Sign Out */
    .sign-out {{
        background: none;
        border: none;
        color: {text_secondary};
        cursor: pointer;
        padding: 8px 12px;
        border-radius: 6px;
        font-size: 14px;
        transition: all 0.2s ease;
        display: flex;
        align-items: center;
        gap: 8px;
        width: 100%;
        margin-top: 16px;
    }}
    
    .sign-out:hover {{
        background: {border_color};
        color: {text_primary};
    }}
    
    /* Main Content Area */
    .upload-area {{
        background: {card_bg};
        border: 2px dashed {border_color};
        border-radius: 12px;
        padding: 80px 40px;
        text-align: center;
        transition: all 0.2s ease;
        margin-bottom: 24px;
    }}
    
    .upload-area:hover {{
        border-color: {primary_blue};
        background: {"rgba(79, 126, 255, 0.05)" if not dark_mode else "rgba(79, 126, 255, 0.1)"};
    }}
    
    .upload-icon {{
        width: 48px;
        height: 48px;
        background: {primary_blue};
        border-radius: 8px;
        display: flex;
        align-items: center;
        justify-content: center;
        margin: 0 auto 16px auto;
        color: white;
        font-size: 20px;
    }}
    
    .upload-title {{
        font-size: 18px;
        font-weight: 600;
        color: {text_primary};
        margin-bottom: 8px;
    }}
    
    .upload-subtitle {{
        font-size: 14px;
        color: {text_secondary};
        margin-bottom: 16px;
    }}
    
    .browse-btn {{
        background: none;
        border: 1px solid {border_color};
        color: {text_primary};
        padding: 8px 16px;
        border-radius: 6px;
        font-size: 14px;
        cursor: pointer;
        transition: all 0.2s ease;
    }}
    
    .browse-btn:hover {{
        border-color: {primary_blue};
        color: {primary_blue};
    }}
    
    /* Supported Formats */
    .supported-formats {{
        background: {"rgba(245, 158, 11, 0.1)" if not dark_mode else "rgba(245, 158, 11, 0.2)"};
        border: 1px solid {"rgba(245, 158, 11, 0.2)" if not dark_mode else "rgba(245, 158, 11, 0.3)"};
        border-radius: 8px;
        padding: 12px 16px;
        margin-top: 24px;
        display: flex;
        align-items: center;
        gap: 8px;
    }}
    
    .format-icon {{
        color: {warning_orange};
        font-size: 16px;
    }}
    
    .format-text {{
        font-size: 14px;
        font-weight: 600;
        color: {text_primary};
    }}
    
    .format-list {{
        font-size: 14px;
        color: {text_secondary};
    }}
    
    /* Figma Button Styles */
    .stButton > button {{
        background: {primary_blue} !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 12px 24px !important;
        font-weight: 600 !important;
        font-size: 14px !important;
        transition: all 0.2s ease !important;
        cursor: pointer !important;
        min-height: 40px !important;
        width: 100% !important;
    }}
    
    .stButton > button:hover {{
        background: #3B6EFF !important;
        transform: translateY(-1px) !important;
    }}
    
    /* Figma Input Styles */
    .stTextInput > div > div > input {{
        background: {card_bg} !important;
        border: 2px solid {border_color} !important;
        border-radius: 12px !important;
        color: {text_primary} !important;
        padding: 16px 20px !important;
        font-size: 16px !important;
        font-weight: 500 !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04) !important;
    }}
    
    .stTextInput > div > div > input:focus {{
        border-color: {primary_blue} !important;
        box-shadow: 0 0 0 4px rgba(37, 99, 235, 0.1) !important;
        outline: none !important;
    }}
    
    .stTextInput > div > div > input::placeholder {{
        color: {text_secondary} !important;
    }}
    
    /* File Uploader */
    .stFileUploader > div > div {{
        border: 2px dashed {primary_blue} !important;
        border-radius: 16px !important;
        background: {card_bg} !important;
        padding: 3rem 2rem !important;
        text-align: center !important;
        transition: all 0.3s ease !important;
    }}
    
    .stFileUploader > div > div:hover {{
        border-color: {primary_purple} !important;
        background: rgba(37, 99, 235, 0.05) !important;
    }}
    
    /* Progress Bar */
    .stProgress > div > div > div {{
        background: linear-gradient(90deg, {primary_blue}, {primary_purple}) !important;
        border-radius: 8px !important;
    }}
    
    /* Alerts */
    .stSuccess {{
        background: linear-gradient(135deg, {success_green}, #059669) !important;
        color: white !important;
        border-radius: 12px !important;
        border: none !important;
        padding: 16px 20px !important;
    }}
    
    .stError {{
        background: linear-gradient(135deg, {error_red}, #DC2626) !important;
        color: white !important;
        border-radius: 12px !important;
        border: none !important;
        padding: 16px 20px !important;
    }}
    
    /* Animations */
    @keyframes fadeIn {{
        from {{ opacity: 0; transform: translateY(20px); }}
        to {{ opacity: 1; transform: translateY(0); }}
    }}
    
    @keyframes slideIn {{
        from {{ opacity: 0; transform: translateX(-20px); }}
        to {{ opacity: 1; transform: translateX(0); }}
    }}
    
    .fade-in {{
        animation: fadeIn 0.6s ease-out;
    }}
    
    .slide-in {{
        animation: slideIn 0.6s ease-out;
    }}
    
    /* Figma Card Styles */
    .figma-card {{
        background: {card_bg} !important;
        border: 1px solid {border_color} !important;
        border-radius: 16px !important;
        padding: 32px !important;
        box-shadow: 0 4px 20px rgba(0, 0, 0, {"0.2" if dark_mode else "0.08"}) !important;
        transition: all 0.3s ease !important;
    }}
    
    .figma-card:hover {{
        transform: translateY(-4px) !important;
        box-shadow: 0 12px 40px rgba(0, 0, 0, {"0.3" if dark_mode else "0.15"}) !important;
    }}
    
    /* Typography */
    .figma-title {{
        font-size: 48px !important;
        font-weight: 800 !important;
        line-height: 1.1 !important;
        background: linear-gradient(135deg, {primary_blue}, {primary_purple}) !important;
        -webkit-background-clip: text !important;
        -webkit-text-fill-color: transparent !important;
        margin-bottom: 16px !important;
    }}
    
    .figma-subtitle {{
        font-size: 20px !important;
        color: {text_secondary} !important;
        font-weight: 500 !important;
        margin-bottom: 32px !important;
    }}
    
    .figma-section-title {{
        font-size: 24px !important;
        font-weight: 700 !important;
        color: {text_primary} !important;
        margin-bottom: 20px !important;
    }}
    
    /* Metrics Cards */
    .metric-card {{
        background: {card_bg} !important;
        border: 1px solid {border_color} !important;
        border-radius: 16px !important;
        padding: 24px !important;
        text-align: center !important;
        transition: all 0.3s ease !important;
        position: relative !important;
        overflow: hidden !important;
    }}
    
    .metric-card::before {{
        content: '' !important;
        position: absolute !important;
        top: 0 !important;
        left: 0 !important;
        right: 0 !important;
        height: 4px !important;
        background: linear-gradient(90deg, {primary_blue}, {primary_purple}) !important;
    }}
    
    .metric-value {{
        font-size: 32px !important;
        font-weight: 800 !important;
        color: {primary_blue} !important;
        margin: 12px 0 8px 0 !important;
    }}
    
    .metric-label {{
        font-size: 14px !important;
        color: {text_secondary} !important;
        font-weight: 600 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.5px !important;
    }}
    
    /* Tags */
    .figma-tag {{
        display: inline-block !important;
        padding: 8px 16px !important;
        border-radius: 24px !important;
        font-size: 14px !important;
        font-weight: 600 !important;
        margin: 4px !important;
        transition: all 0.3s ease !important;
    }}
    
    .tag-primary {{
        background: rgba(37, 99, 235, 0.1) !important;
        color: {primary_blue} !important;
        border: 1px solid rgba(37, 99, 235, 0.2) !important;
    }}
    
    .tag-success {{
        background: rgba(16, 185, 129, 0.1) !important;
        color: {success_green} !important;
        border: 1px solid rgba(16, 185, 129, 0.2) !important;
    }}
    
    .tag-warning {{
        background: rgba(245, 158, 11, 0.1) !important;
        color: {warning_orange} !important;
        border: 1px solid rgba(245, 158, 11, 0.2) !important;
    }}
    
    .tag-error {{
        background: rgba(239, 68, 68, 0.1) !important;
        color: {error_red} !important;
        border: 1px solid rgba(239, 68, 68, 0.2) !important;
    }}
    
    /* Loading Spinner */
    .figma-spinner {{
        width: 48px !important;
        height: 48px !important;
        border: 4px solid {border_color} !important;
        border-top: 4px solid {primary_blue} !important;
        border-radius: 50% !important;
        animation: spin 1s linear infinite !important;
        margin: 0 auto 20px auto !important;
    }}
    
    @keyframes spin {{
        0% {{ transform: rotate(0deg); }}
        100% {{ transform: rotate(360deg); }}
    }}
    
    /* Responsive Design */
    @media (max-width: 768px) {{
        .figma-title {{
            font-size: 32px !important;
        }}
        
        .figma-card {{
            padding: 20px !important;
        }}
        
        .stButton > button {{
            padding: 12px 20px !important;
            font-size: 14px !important;
        }}
    }}
    </style>
    """, unsafe_allow_html=True)

def render_figma_sidebar(current_user=None, analyses=None):
    """Render sidebar based on Figma design."""
    dark_mode = st.session_state.get('dark_mode', False)
    render_figma_styles(dark_mode)
    
    user_name = current_user.user_metadata.get('name', 'User') if current_user else 'User'
    user_email = current_user.email if current_user else 'user@example.com'
    user_initial = user_name[0].upper() if user_name else 'U'
    
    st.markdown(f"""
    <div class="sidebar">
        <!-- Logo Section -->
        <div class="logo-section">
            <div class="logo-icon">🚀</div>
            <div>
                <div class="logo-text">PitchPerfect AI</div>
                <div class="logo-subtitle">AI-powered pitch deck analysis</div>
            </div>
        </div>
        
        <!-- Upload Button -->
        <button class="upload-btn" onclick="document.querySelector('input[type=file]').click()">
            📤 Upload New Deck
        </button>
        
        <!-- Past Analyses -->
        <div class="past-analyses">
            <div class="section-title">
                📁 Past Analyses
                <div style="margin-left: auto;">
                    <svg width="16" height="16" viewBox="0 0 16 16" fill="currentColor">
                        <path d="M8 2a.5.5 0 0 1 .5.5v5h5a.5.5 0 0 1 0 1h-5v5a.5.5 0 0 1-1 0v-5h-5a.5.5 0 0 1 0-1h5v-5A.5.5 0 0 1 8 2z"/>
                    </svg>
                </div>
            </div>
    """, unsafe_allow_html=True)
    
    # Show past analyses
    if analyses:
        for analysis in analyses[:5]:  # Show only first 5
            score = analysis.get('score', 0)
            score_color = "#10B981" if score >= 7 else "#F59E0B" if score >= 5 else "#EF4444"
            
            st.markdown(f"""
            <div class="analysis-item">
                <div class="analysis-name">{analysis['filename'][:20]}{'...' if len(analysis['filename']) > 20 else ''}</div>
                <div class="analysis-date">{analysis['date'][:16]}</div>
                <div class="analysis-score" style="background: {score_color};">{score}/10</div>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown(f"""
        </div>
        
        <!-- User Profile -->
        <div class="user-profile">
            <div class="user-avatar">{user_initial}</div>
            <div class="user-info">
                <div class="user-name">{user_name}</div>
                <div class="user-email">{user_email}</div>
            </div>
        </div>
        
        <!-- Theme Toggle -->
        <button class="theme-toggle" onclick="toggleTheme()">
            {'🌙 Light Theme' if dark_mode else '☀️ Dark Theme'}
        </button>
        
        <!-- Sign Out -->
        <button class="sign-out" onclick="signOut()">
            🚪 Sign Out
        </button>
    </div>
    
    <script>
    function toggleTheme() {{
        // This will be handled by Streamlit
        window.parent.postMessage({{type: 'theme_toggle'}}, '*');
    }}
    
    function signOut() {{
        window.parent.postMessage({{type: 'sign_out'}}, '*');
    }}
    </script>
    """, unsafe_allow_html=True)

def render_figma_login_form():
    """Render login form based on new Figma design."""
    # Full-screen dark background
    st.markdown("""
    <style>
    .main .block-container {
        padding: 0 !important;
        max-width: none !important;
    }
    
    .auth-container {
        min-height: 100vh;
        background: #2A2A2A;
        display: flex;
        align-items: center;
        justify-content: center;
        padding: 40px 20px;
        position: relative;
    }
    
    .auth-card {
        background: #3A3A3A;
        border-radius: 16px;
        padding: 48px 40px;
        width: 100%;
        max-width: 400px;
        text-align: center;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
    }
    
    .logo-container {
        width: 64px;
        height: 64px;
        background: #4A90E2;
        border-radius: 12px;
        display: flex;
        align-items: center;
        justify-content: center;
        margin: 0 auto 24px auto;
    }
    
    .app-title {
        font-size: 24px;
        font-weight: 700;
        color: #FFFFFF;
        margin: 0 0 8px 0;
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    }
    
    .app-subtitle {
        font-size: 14px;
        color: #A0A0A0;
        margin: 0 0 32px 0;
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    }
    
    .auth-tabs {
        display: flex;
        background: #2A2A2A;
        border-radius: 8px;
        padding: 4px;
        margin-bottom: 32px;
    }
    
    .auth-tab {
        flex: 1;
        padding: 12px 16px;
        border: none;
        background: transparent;
        color: #A0A0A0;
        font-size: 14px;
        font-weight: 500;
        border-radius: 6px;
        cursor: pointer;
        transition: all 0.2s ease;
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    }
    
    .auth-tab.active {
        background: #4A90E2;
        color: #FFFFFF;
    }
    
    .form-group {
        margin-bottom: 20px;
        text-align: left;
    }
    
    .form-label {
        display: block;
        font-size: 14px;
        font-weight: 500;
        color: #FFFFFF;
        margin-bottom: 8px;
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    }
    
    .form-input {
        width: 100%;
        padding: 12px 16px;
        background: #2A2A2A;
        border: 1px solid #4A4A4A;
        border-radius: 8px;
        color: #FFFFFF;
        font-size: 14px;
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
        box-sizing: border-box;
    }
    
    .form-input::placeholder {
        color: #A0A0A0;
    }
    
    .form-input:focus {
        outline: none;
        border-color: #4A90E2;
        box-shadow: 0 0 0 3px rgba(74, 144, 226, 0.1);
    }
    
    .sign-in-btn {
        width: 100%;
        padding: 14px 16px;
        background: #4A90E2;
        border: none;
        border-radius: 8px;
        color: #FFFFFF;
        font-size: 14px;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.2s ease;
        margin-top: 24px;
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    }
    
    .sign-in-btn:hover {
        background: #357ABD;
    }
    
    .theme-toggle {
        position: absolute;
        bottom: 32px;
        left: 50%;
        transform: translateX(-50%);
        display: flex;
        align-items: center;
        gap: 8px;
        color: #A0A0A0;
        font-size: 14px;
        cursor: pointer;
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    }
    
    .theme-toggle:hover {
        color: #FFFFFF;
    }
    
    /* Override Streamlit styles */
    .stTextInput > div > div > input {
        background: #2A2A2A !important;
        border: 1px solid #4A4A4A !important;
        border-radius: 8px !important;
        color: #FFFFFF !important;
        padding: 12px 16px !important;
        font-size: 14px !important;
    }
    
    .stTextInput > div > div > input::placeholder {
        color: #A0A0A0 !important;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #4A90E2 !important;
        box-shadow: 0 0 0 3px rgba(74, 144, 226, 0.1) !important;
    }
    
    .stButton > button {
        width: 100% !important;
        padding: 14px 16px !important;
        background: #4A90E2 !important;
        border: none !important;
        border-radius: 8px !important;
        color: #FFFFFF !important;
        font-size: 14px !important;
        font-weight: 600 !important;
        margin-top: 24px !important;
    }
    
    .stButton > button:hover {
        background: #357ABD !important;
        transform: none !important;
        box-shadow: none !important;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Create a container for the entire login page
    container = st.container()
    
    with container:
        # Main auth container with form fields inside
        st.markdown("""
        <div class="auth-container">
            <div class="auth-card">
                <div class="logo-container">
                    <svg width="32" height="32" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                        <path d="M12 2L13.09 8.26L22 9L13.09 9.74L12 16L10.91 9.74L2 9L10.91 8.26L12 2Z" fill="white"/>
                    </svg>
                </div>
                <h1 class="app-title">PitchPerfect AI</h1>
                <p class="app-subtitle">AI-powered pitch deck analysis</p>
                
                <div class="auth-tabs">
                    <div class="auth-tab active">Sign In</div>
                    <div class="auth-tab">Sign Up</div>
                </div>
            </div>
            
            <div style="max-width: 320px; margin: 0 auto; padding-top: 20px;">
        """, unsafe_allow_html=True)
        
        # Form fields
            st.markdown('<div class="form-group"><label class="form-label">Email Address</label></div>', unsafe_allow_html=True)
            email = st.text_input(
                "Email", 
                key="login_email", 
                placeholder="Enter your email",
                label_visibility="collapsed"
            )
            
            st.markdown('<div class="form-group"><label class="form-label">Password</label></div>', unsafe_allow_html=True)
            password = st.text_input(
                "Password", 
                type="password",
                key="login_password", 
                placeholder="Enter your password",
                label_visibility="collapsed"
            )
            
            # Sign In button
            if st.button("🔒 Sign In", key="login_btn", use_container_width=True):
                if email and password:
                    auth_handler = st.session_state.get('auth_handler')
                    if auth_handler:
                        with st.spinner("Signing you in..."):
                            success, message = auth_handler.login(email, password)
                            if success:
                                st.success("✅ Welcome back!")
                                st.rerun()
                            else:
                                st.error(f"❌ {message}")
                    else:
                        st.error("❌ Authentication service not available")
                else:
                    st.error("❌ Please fill in all fields")
            
            # Handle tab switching
            if st.button("Create New Account", key="switch_to_signup", use_container_width=True):
                st.session_state.auth_mode = 'signup'
                st.rerun()
        
        # Theme toggle at bottom
        st.markdown("""
        <div class="theme-toggle">
            <span>🌙</span>
            <span>Light Theme</span>
        </div>
        """, unsafe_allow_html=True)

def render_figma_signup_form():
    """Render signup form based on new Figma design."""
    # Use same styles as login
    st.markdown("""
    <style>
    .main .block-container {
        padding: 0 !important;
        max-width: none !important;
    }
    
    .auth-container {
        min-height: 100vh;
        background: #2A2A2A;
        display: flex;
        align-items: center;
        justify-content: center;
        padding: 40px 20px;
        position: relative;
    }
    
    .auth-card {
        background: #3A3A3A;
        border-radius: 16px;
        padding: 48px 40px;
        width: 100%;
        max-width: 400px;
        text-align: center;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
    }
    
    .logo-container {
        width: 64px;
        height: 64px;
        background: #4A90E2;
        border-radius: 12px;
        display: flex;
        align-items: center;
        justify-content: center;
        margin: 0 auto 24px auto;
    }
    
    .app-title {
        font-size: 24px;
        font-weight: 700;
        color: #FFFFFF;
        margin: 0 0 8px 0;
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    }
    
    .app-subtitle {
        font-size: 14px;
        color: #A0A0A0;
        margin: 0 0 32px 0;
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    }
    
    .auth-tabs {
        display: flex;
        background: #2A2A2A;
        border-radius: 8px;
        padding: 4px;
        margin-bottom: 32px;
    }
    
    .auth-tab {
        flex: 1;
        padding: 12px 16px;
        border: none;
        background: transparent;
        color: #A0A0A0;
        font-size: 14px;
        font-weight: 500;
        border-radius: 6px;
        cursor: pointer;
        transition: all 0.2s ease;
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    }
    
    .auth-tab.active {
        background: #4A90E2;
        color: #FFFFFF;
    }
    
    .form-group {
        margin-bottom: 20px;
        text-align: left;
    }
    
    .form-label {
        display: block;
        font-size: 14px;
        font-weight: 500;
        color: #FFFFFF;
        margin-bottom: 8px;
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    }
    
    .theme-toggle {
        position: absolute;
        bottom: 32px;
        left: 50%;
        transform: translateX(-50%);
        display: flex;
        align-items: center;
        gap: 8px;
        color: #A0A0A0;
        font-size: 14px;
        cursor: pointer;
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    }
    
    .theme-toggle:hover {
        color: #FFFFFF;
    }
    
    /* Override Streamlit styles */
    .stTextInput > div > div > input {
        background: #2A2A2A !important;
        border: 1px solid #4A4A4A !important;
        border-radius: 8px !important;
        color: #FFFFFF !important;
        padding: 12px 16px !important;
        font-size: 14px !important;
    }
    
    .stTextInput > div > div > input::placeholder {
        color: #A0A0A0 !important;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #4A90E2 !important;
        box-shadow: 0 0 0 3px rgba(74, 144, 226, 0.1) !important;
    }
    
    .stButton > button {
        width: 100% !important;
        padding: 14px 16px !important;
        background: #4A90E2 !important;
        border: none !important;
        border-radius: 8px !important;
        color: #FFFFFF !important;
        font-size: 14px !important;
        font-weight: 600 !important;
        margin-top: 24px !important;
    }
    
    .stButton > button:hover {
        background: #357ABD !important;
        transform: none !important;
        box-shadow: none !important;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Create a container for the entire signup page
    container = st.container()
    
    with container:
        # Main auth container
        st.markdown("""
        <div class="auth-container">
            <div class="auth-card">
                <div class="logo-container">
                    <svg width="32" height="32" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                        <path d="M12 2L13.09 8.26L22 9L13.09 9.74L12 16L10.91 9.74L2 9L10.91 8.26L12 2Z" fill="white"/>
                    </svg>
                </div>
                <h1 class="app-title">PitchPerfect AI</h1>
                <p class="app-subtitle">AI-powered pitch deck analysis</p>
                
                <div class="auth-tabs">
                    <div class="auth-tab">Sign In</div>
                    <div class="auth-tab active">Sign Up</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Form fields
        col1, col2, col3 = st.columns([1, 3, 1])
        with col2:
            st.markdown('<div class="form-group"><label class="form-label">Full Name</label></div>', unsafe_allow_html=True)
            name = st.text_input(
                "Full Name", 
                key="signup_name", 
                placeholder="Enter your full name",
                label_visibility="collapsed"
            )
            
            st.markdown('<div class="form-group"><label class="form-label">Email Address</label></div>', unsafe_allow_html=True)
            email = st.text_input(
                "Email", 
                key="signup_email", 
                placeholder="Enter your email",
                label_visibility="collapsed"
            )
            
            st.markdown('<div class="form-group"><label class="form-label">Password</label></div>', unsafe_allow_html=True)
            password = st.text_input(
                "Password", 
                type="password",
                key="signup_password", 
                placeholder="Enter your password",
                label_visibility="collapsed"
            )
            
            # Sign Up button
            if st.button("🚀 Sign Up", key="signup_btn", use_container_width=True):
                if name and email and password:
                    if len(password) < 6:
                        st.error("❌ Password must be at least 6 characters long")
                    else:
                        auth_handler = st.session_state.get('auth_handler')
                        if auth_handler:
                            with st.spinner("Creating your account..."):
                                success, message = auth_handler.signup(name, email, password)
                                if success:
                                    st.success("✅ Account created successfully!")
                                    if "logged in" in message.lower():
                                        st.rerun()
                                else:
                                    st.error(f"❌ {message}")
                        else:
                            st.error("❌ Authentication service not available")
                else:
                    st.error("❌ Please fill in all fields")
            
            # Handle tab switching
            if st.button("Already have an account? Sign In", key="switch_to_login", use_container_width=True):
                st.session_state.auth_mode = 'login'
                st.rerun()
        
        # Theme toggle at bottom
        st.markdown("""
        <div class="theme-toggle">
            <span>🌙</span>
            <span>Light Theme</span>
        </div>
        """, unsafe_allow_html=True)

def render_figma_main_content():
    """Render main content area based on Figma design."""
    dark_mode = st.session_state.get('dark_mode', False)
    
    st.markdown(f"""
    <div class="main-content">
        <div style="text-align: center; margin-bottom: 40px;">
            <div class="upload-icon">📤</div>
            <h1 style="font-size: 24px; font-weight: 700; color: {'#FFFFFF' if dark_mode else '#1A1A1A'}; margin-bottom: 8px;">
                PitchPerfect AI - Your Personal Pitch Deck Analyst
            </h1>
            <p style="font-size: 16px; color: {'#A0A0A0' if dark_mode else '#6B7280'};">
                Upload your deck and get AI-powered insights instantly
            </p>
        </div>
        
        <div class="upload-area">
            <div class="upload-icon">📤</div>
            <div class="upload-title">Drop your pitch deck here</div>
            <div class="upload-subtitle">or</div>
            <button class="browse-btn">Browse Files</button>
        </div>
        
        <div class="supported-formats">
            <div class="format-icon">⚠️</div>
            <div>
                <div class="format-text">Supported formats:</div>
                <div class="format-list">PDF, PPTX, DOCX, TXT files up to 50MB</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_figma_analysis_results(score, read_score, sentiment, grade, overall_score, strengths, weaknesses, tips, keywords, recommendations):
    """Render analysis results in new design."""
    dark_mode = st.session_state.get('dark_mode', False)
    
    st.markdown(f"""
    <div class="main-content">
        <div style="margin-bottom: 32px;">
            <h2 style="font-size: 24px; font-weight: 700; color: {'#FFFFFF' if dark_mode else '#1A1A1A'}; margin-bottom: 24px;">
                📊 Analysis Results
            </h2>
            
            <!-- Metrics Grid -->
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
            
            <!-- Insights Section -->
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 24px;">
                <div style="background: {'#2A2A2A' if dark_mode else '#FFFFFF'}; border: 1px solid {'#3A3A3A' if dark_mode else '#E5E7EB'}; border-radius: 12px; padding: 24px;">
                    <h3 style="font-size: 18px; font-weight: 600; color: {'#FFFFFF' if dark_mode else '#1A1A1A'}; margin-bottom: 16px; display: flex; align-items: center; gap: 8px;">
                        ✨ Strengths
                    </h3>
                    <div style="display: flex; flex-wrap: wrap; gap: 8px;">
    """, unsafe_allow_html=True)
    
    for strength in strengths:
        st.markdown(f'<span class="figma-tag tag-success">{strength}</span>', unsafe_allow_html=True)
    
    st.markdown(f"""
                    </div>
                </div>
                
                <div style="background: {'#2A2A2A' if dark_mode else '#FFFFFF'}; border: 1px solid {'#3A3A3A' if dark_mode else '#E5E7EB'}; border-radius: 12px; padding: 24px;">
                    <h3 style="font-size: 18px; font-weight: 600; color: {'#FFFFFF' if dark_mode else '#1A1A1A'}; margin-bottom: 16px; display: flex; align-items: center; gap: 8px;">
                        ⚠️ Areas to Improve
                    </h3>
                    <div style="display: flex; flex-wrap: wrap; gap: 8px;">
    """, unsafe_allow_html=True)
    
    for weakness in weaknesses:
        st.markdown(f'<span class="figma-tag tag-error">{weakness}</span>', unsafe_allow_html=True)
    
    st.markdown(f"""
                    </div>
                </div>
                
                <div style="background: {'#2A2A2A' if dark_mode else '#FFFFFF'}; border: 1px solid {'#3A3A3A' if dark_mode else '#E5E7EB'}; border-radius: 12px; padding: 24px;">
                    <h3 style="font-size: 18px; font-weight: 600; color: {'#FFFFFF' if dark_mode else '#1A1A1A'}; margin-bottom: 16px; display: flex; align-items: center; gap: 8px;">
                        💡 Recommendations
                    </h3>
                    <div style="display: flex; flex-wrap: wrap; gap: 8px;">
    """, unsafe_allow_html=True)
    
    for tip in tips:
        st.markdown(f'<span class="figma-tag tag-warning">{tip}</span>', unsafe_allow_html=True)
    
    st.markdown(f"""
                    </div>
                </div>
                
                <div style="background: {'#2A2A2A' if dark_mode else '#FFFFFF'}; border: 1px solid {'#3A3A3A' if dark_mode else '#E5E7EB'}; border-radius: 12px; padding: 24px;">
                    <h3 style="font-size: 18px; font-weight: 600; color: {'#FFFFFF' if dark_mode else '#1A1A1A'}; margin-bottom: 16px; display: flex; align-items: center; gap: 8px;">
                        🔑 Key Terms
                    </h3>
                    <div style="display: flex; flex-wrap: wrap; gap: 8px;">
    """, unsafe_allow_html=True)
    
    for keyword in keywords:
        st.markdown(f'<span class="figma-tag tag-primary">{keyword}</span>', unsafe_allow_html=True)
    
    st.markdown("""
                    </div>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_figma_metrics(score: float, read_score: float, sentiment: dict, grade: str = "B+", overall_score: float = 75):
    """Render metrics based on Figma design."""
    sentiment_score = sentiment.get('compound', 0) if isinstance(sentiment, dict) else 0
    sentiment_label = "Positive" if sentiment_score > 0.1 else "Negative" if sentiment_score < -0.1 else "Neutral"
    
    st.markdown("""
    <div style='padding: 40px 60px; max-width: 1200px; margin: 0 auto;'>
        <h2 class='figma-section-title'>📊 Analysis Results</h2>
    </div>
    """, unsafe_allow_html=True)
    
    # Metrics grid
    col1, col2, col3, col4 = st.columns(4)
    
    metrics = [
        ("Section Coverage", f"{score}/10", "tag-success" if score >= 7 else "tag-warning" if score >= 5 else "tag-error"),
        ("Readability Score", f"{read_score:.0f}", "tag-success" if read_score >= 70 else "tag-warning" if read_score >= 50 else "tag-error"),
        ("Sentiment", sentiment_label, "tag-success" if sentiment_score > 0.1 else "tag-error" if sentiment_score < -0.1 else "tag-warning"),
        ("Overall Score", f"{overall_score}/100", "tag-success" if overall_score >= 80 else "tag-warning" if overall_score >= 60 else "tag-error")
    ]
    
    cols = [col1, col2, col3, col4]
    for i, (label, value, status) in enumerate(metrics):
        with cols[i]:
            st.markdown(f"""
            <div style='padding: 0 15px;'>
                <div class='metric-card slide-in'>
                    <div class='metric-label'>{label}</div>
                    <div class='metric-value'>{value}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    # Grade card
    st.markdown(f"""
    <div style='padding: 40px 60px; max-width: 1200px; margin: 0 auto;'>
        <div style='text-align: center; margin: 40px 0;'>
            <div style='background: linear-gradient(135deg, #2563EB, #7C3AED); border-radius: 24px; padding: 40px; color: white; display: inline-block; box-shadow: 0 20px 60px rgba(37, 99, 235, 0.3);'>
                <div style='font-size: 72px; font-weight: 900; margin-bottom: 12px;'>{grade}</div>
                <div style='font-size: 20px; opacity: 0.9;'>Overall Grade</div>
                <div style='margin-top: 16px;'>
                    {"⭐" * min(5, max(1, int(overall_score / 20)))}
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_figma_insights(strengths: List[str], weaknesses: List[str], tips: List[str], keywords: List[str]):
    """Render insights based on Figma design."""
    st.markdown("""
    <div style='padding: 40px 60px; max-width: 1200px; margin: 0 auto;'>
        <h2 class='figma-section-title'>💡 Key Insights</h2>
    </div>
    """, unsafe_allow_html=True)
    
    # Insights categories
    categories = [
        ("✨ Strengths", strengths, "tag-success"),
        ("⚠️ Areas to Improve", weaknesses, "tag-error"),
        ("💡 Recommendations", tips, "tag-warning"),
        ("🔑 Key Terms", keywords, "tag-primary")
    ]
    
    for title, items, tag_class in categories:
        if items:
            st.markdown(f"""
            <div style='padding: 0 60px; max-width: 1200px; margin: 0 auto 32px auto;'>
                <div class='figma-card slide-in'>
                    <h3 style='font-size: 20px; font-weight: 700; margin-bottom: 20px;'>{title}</h3>
                    <div style='display: flex; flex-wrap: wrap; gap: 12px;'>
            """, unsafe_allow_html=True)
            
            for item in items:
                st.markdown(f'<span class="figma-tag {tag_class}">{item}</span>', unsafe_allow_html=True)
            
            st.markdown("</div></div></div>", unsafe_allow_html=True)

def render_figma_loading():
    """Render loading animation based on Figma design."""
    st.markdown("""
    <div style='display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 80px 40px; text-align: center;'>
        <div class='figma-spinner'></div>
        <h3 style='font-size: 24px; font-weight: 700; margin-bottom: 12px; color: #2563EB;'>Analyzing Your Pitch Deck</h3>
        <p style='font-size: 16px; color: #64748B;'>Our AI is processing your presentation...</p>
    </div>
    """, unsafe_allow_html=True)

def render_figma_success(title="Success!", message="Analysis completed successfully"):
    """Render success message based on Figma design."""
    st.markdown(f"""
    <div style='padding: 40px 60px; max-width: 1200px; margin: 0 auto;'>
        <div class='figma-card fade-in' style='text-align: center; background: linear-gradient(135deg, #10B981, #059669); color: white; border: none;'>
            <div style='font-size: 64px; margin-bottom: 24px;'>🎉</div>
            <h2 style='font-size: 32px; font-weight: 800; margin-bottom: 12px;'>{title}</h2>
            <p style='font-size: 18px; opacity: 0.9;'>{message}</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_figma_history(analyses: List[Dict[str, Any]]):
    """Render analysis history based on Figma design."""
    if not analyses:
        return
    
    st.markdown("""
    <div style='padding: 40px 60px; max-width: 1200px; margin: 0 auto;'>
        <h2 class='figma-section-title'>📚 Your Analysis History</h2>
    </div>
    """, unsafe_allow_html=True)
    
    for analysis in analyses[:5]:
        st.markdown(f"""
        <div style='padding: 0 60px; max-width: 1200px; margin: 0 auto 20px auto;'>
            <div class='figma-card slide-in'>
                <div style='display: flex; justify-content: space-between; align-items: start; margin-bottom: 16px;'>
                    <h3 style='font-size: 18px; font-weight: 700; margin: 0;'>{analysis['filename']}</h3>
                    <span style='font-size: 14px; color: #64748B;'>{analysis['date'][:16]}</span>
                </div>
                <p style='font-size: 16px; color: #64748B; margin-bottom: 16px; line-height: 1.5;'>
                    {analysis['summary'][:150]}{'...' if len(analysis['summary'])>150 else ''}
                </p>
                <div style='display: flex; gap: 12px; flex-wrap: wrap;'>
                    <span class='figma-tag tag-primary'>Score: {analysis.get('score', 'N/A')}/10</span>
                    <span class='figma-tag tag-success'>Readability: {float(analysis.get('readability', 0)):.0f}</span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)