import streamlit as st
from typing import Dict, List, Any

def apply_global_styles(dark_mode=False):
    """
    Applies global CSS styles to hide Streamlit defaults, set fonts, 
    and most importantly, fix the main content padding to accommodate the fixed navbar.
    """
    if dark_mode:
        bg_color = "#0F172A"
        text_primary = "#F1F5F9"
        accent_color = "#6366F1"
        border_color = "#334155"
    else:
        bg_color = "#F8FAFC"
        text_primary = "#1F2937"
        accent_color = "#4F46E5"
        border_color = "#E5E7EB"

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

        /*
        --- CRITICAL LAYOUT FIX ---
        This targets the main container that holds the page content and forces a top padding
        to prevent it from being hidden behind our fixed navbar.
        
        This is more robust than targeting '.block-container'.
        */
        [data-testid="stAppViewContainer"] > section {{
            padding-top: 90px !important;
        }}

        /* --- Custom Logout Button Styling --- */
        /* We style the custom button directly, not the hidden Streamlit one */
        .navbar-logout-btn {{
            background: #EF4444;
            color: white !important;
            border: none;
            border-radius: 8px;
            padding: 10px 18px;
            font-size: 14px;
            font-weight: 600;
            cursor: pointer;
            transition: background-color 0.2s ease;
        }}
        .navbar-logout-btn:hover {{
            background-color: #DC2626;
        }}
        
        /* This is the REAL streamlit button that we will hide and trigger with JS */
        div[data-testid="stVerticalBlock"] > div:has(button[data-testid="baseButton-secondary"]) {{
            display: none;
        }}
    
    /* Main Content Area */
    .main-content {{
        margin-left: 280px;
        min-height: 100vh;
        background: {main_bg};
        padding: 40px;
    }}
    
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
        border-color: {accent_color};
        background: {"rgba(79, 126, 255, 0.05)" if not dark_mode else "rgba(79, 126, 255, 0.1)"};
    }}
    
    .upload-icon {{
        width: 48px;
        height: 48px;
        background: {accent_color};
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
        border-color: {accent_color};
        color: {accent_color};
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
    </style>
    """, unsafe_allow_html=True)

def extract_user_data_safely(current_user):
    """Safely extract user data with fallback values."""
    try:
        if current_user and hasattr(current_user, 'user_metadata') and current_user.user_metadata:
            user_name = current_user.user_metadata.get('name', 'User')
        else:
            user_name = 'User'
        
        if current_user and hasattr(current_user, 'email') and current_user.email:
            user_email = current_user.email
        else:
            user_email = 'user@example.com'
            
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

def render_navigation_bar(current_user=None):
    """Render a clean, consistent navbar with company logo, user info, and logout button."""
    try:
        dark_mode = st.session_state.get('dark_mode', False)
        
        # Get user info safely with error handling
        user_data = extract_user_data_safely(current_user)
        user_name = user_data['name']
        user_email = user_data['email']
        user_initial = user_data['initial']
        
        # Set theme-based colors
        if dark_mode:
            bg_color = "#0F172A"
            text_color = "#F1F5F9"
            accent_color = "#6366F1"
            border_color = "#334155"
        else:
            bg_color = "#FFFFFF"
            text_color = "#111827"
            accent_color = "#4F46E5"
            border_color = "#E5E7EB"
        
        # Apply navbar styles
        st.markdown(f"""
    <style>
    /* Navbar Container */
    .navbar-container {{
        background: {bg_color};
        border-bottom: 1px solid {border_color};
        height: 70px;
        width: 100%;
        position: fixed;
        top: 0;
        left: 0;
        z-index: 9999;
        box-shadow: 0 8px 32px rgba(0,0,0,0.12);
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 0 40px;
        backdrop-filter: blur(20px);
        border-radius: 0 0 16px 16px;
    }}
    
    /* Logo Section */
    .navbar-logo {{
        display: flex;
        align-items: center;
        gap: 16px;
        font-size: 24px;
        font-weight: 800;
        color: {text_color};
        flex: 1;
        letter-spacing: -0.5px;
        cursor: pointer;
        transition: all 0.3s ease;
    }}
    
    .navbar-logo:hover {{
        transform: translateY(-1px);
    }}
    
    .navbar-logo-icon {{
        width: 40px;
        height: 40px;
        background: linear-gradient(135deg, {accent_color} 0%, {accent_color}80 100%);
        border-radius: 12px;
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        font-size: 20px;
        box-shadow: 0 4px 12px rgba(99, 102, 241, 0.3);
        transition: all 0.3s ease;
    }}
    
    .navbar-logo:hover .navbar-logo-icon {{
        transform: scale(1.05);
        box-shadow: 0 6px 20px rgba(99, 102, 241, 0.4);
    }}
    
    /* User Info Section */
    .navbar-user-section {{
        display: flex;
        align-items: center;
        gap: 16px;
        margin-right: 0px;
        padding: 8px 16px;
        background: {"rgba(99, 102, 241, 0.05)" if not dark_mode else "rgba(99, 102, 241, 0.1)"};
        border-radius: 12px;
        border: 1px solid {"rgba(99, 102, 241, 0.1)" if not dark_mode else "rgba(99, 102, 241, 0.2)"};
        transition: all 0.3s ease;
    }}
    
    .navbar-user-section:hover {{
        background: {"rgba(99, 102, 241, 0.08)" if not dark_mode else "rgba(99, 102, 241, 0.15)"};
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(99, 102, 241, 0.15);
    }}
    
    .navbar-user-avatar {{
        width: 42px;
        height: 42px;
        background: linear-gradient(135deg, {accent_color} 0%, {accent_color}80 100%);
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        font-weight: 700;
        font-size: 18px;
        box-shadow: 0 4px 12px rgba(99, 102, 241, 0.3);
        border: 2px solid {"rgba(255, 255, 255, 0.2)" if not dark_mode else "rgba(255, 255, 255, 0.1)"};
    }}
    
    .navbar-user-details {{
        display: flex;
        flex-direction: column;
        align-items: flex-end;
    }}
    
    .navbar-user-name {{
        font-size: 16px;
        font-weight: 700;
        color: {text_color};
        margin: 0;
        line-height: 1.2;
        letter-spacing: -0.2px;
    }}
    
    .navbar-user-email {{
        font-size: 13px;
        color: {"#6B7280" if not dark_mode else "#9CA3AF"};
        margin: 0;
        line-height: 1.2;
        font-weight: 500;
    }}
    
    /* Logout Button Styling */
    .stButton > button[data-testid="baseButton-secondary"] {{
        background: linear-gradient(135deg, #EF4444 0%, #DC2626 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 12px 20px !important;
        font-size: 14px !important;
        font-weight: 700 !important;
        cursor: pointer !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 12px rgba(239, 68, 68, 0.3) !important;
        min-height: 44px !important;
        letter-spacing: 0.2px !important;
        margin-left: 20px !important;
    }}
    
    .stButton > button[data-testid="baseButton-secondary"]:hover {{
        background: linear-gradient(135deg, #DC2626 0%, #B91C1C 100%) !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(239, 68, 68, 0.4) !important;
    }}
    
    .stButton > button[data-testid="baseButton-secondary"]:active {{
        transform: translateY(0) !important;
    }}
    
    /* Hide the Streamlit logout button since we're using custom HTML button */
    .stButton > button[data-testid="baseButton-secondary"] {{
        display: none !important;
    }}
    
    /* Navbar Logout Container */
    .navbar-logout-container {{
        display: flex;
        align-items: center;
        margin-left: 16px;
    }}
    
    /* Navbar Logout Button */
    .navbar-logout-btn {{
        background: linear-gradient(135deg, #EF4444 0%, #DC2626 100%);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 12px 20px;
        font-size: 14px;
        font-weight: 700;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: 0 4px 12px rgba(239, 68, 68, 0.3);
        min-height: 44px;
        letter-spacing: 0.2px;
        margin-left: 0px;
    }}
    
    .navbar-logout-btn:hover {{
        background: linear-gradient(135deg, #DC2626 0%, #B91C1C 100%);
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(239, 68, 68, 0.4);
    }}
    
    .navbar-logout-btn:active {{
        transform: translateY(0);
    }}
    
    /* Responsive Design */
    @media (max-width: 768px) {{
        .navbar-container {{
            padding: 0 20px;
            height: 60px;
        }}
        .navbar-logo {{
            font-size: 18px;
            gap: 12px;
        }}
        .navbar-logo-icon {{
            width: 32px;
            height: 32px;
            font-size: 16px;
        }}
        .navbar-user-section {{
            padding: 6px 12px;
            gap: 12px;
        }}
        .navbar-user-avatar {{
            width: 36px;
            height: 36px;
            font-size: 16px;
        }}
        .navbar-user-details {{
            display: none;
        }}
        .stButton > button[data-testid="baseButton-secondary"] {{
            padding: 8px 16px !important;
            font-size: 13px !important;
            min-height: 36px !important;
        }}
    }}
    
    /* Ensure main content doesn't overlap navbar */
    .main .block-container {{
        padding-top: 90px !important;
    }}
    </style>
        """, unsafe_allow_html=True)
        
        # Create complete navbar with all elements inside
        st.markdown(f"""
    <div class="navbar-container">
        <div class="navbar-logo">
            <div class="navbar-logo-icon">🚀</div>
            <span>PitchPerfect AI</span>
        </div>
        
        <div style="flex: 1;"></div>
        
        <div style="display: flex; align-items: center; gap: 0;">
            <div class="navbar-user-section">
                <div class="navbar-user-avatar">{user_initial}</div>
                <div class="navbar-user-details">
                    <div class="navbar-user-name">{user_name}</div>
                    <div class="navbar-user-email">{user_email}</div>
                </div>
            </div>
            
            <div class="navbar-logout-container">
                <button class="navbar-logout-btn" onclick="handleLogout()">Logout</button>
            </div>
        </div>
    </div>
    
    <script>
    function handleLogout() {{
        // Trigger the hidden Streamlit button
        const logoutBtn = document.querySelector('[data-testid="baseButton-secondary"]');
        if (logoutBtn) {{
            logoutBtn.click();
        }}
    }}
    </script>
        """, unsafe_allow_html=True)
        
        # Hidden Streamlit button for logout functionality
        if st.button("Logout", key="navbar_logout_btn", help="Sign out of your account", type="secondary"):
            # Import auth handler and perform logout
            try:
                from auth_handler import AuthHandler
                auth_handler = st.session_state.get('auth_handler')
                if auth_handler:
                    auth_handler.logout()
                else:
                    # Clear session state manually if auth handler not available
                    for key in list(st.session_state.keys()):
                        if key not in ['dark_mode']:  # Keep theme preference
                            del st.session_state[key]
                st.success("You have been logged out successfully!")
                st.rerun()
            except Exception as e:
                st.error(f"Logout failed: {str(e)}")
                st.rerun()
    
    except Exception as e:
        # Error boundary for navigation bar
        st.error(f"Navigation bar error: {str(e)}")
        # Render minimal fallback navigation
        st.markdown("""
        <div style="background: #FFFFFF; padding: 10px; border-bottom: 1px solid #E5E7EB;">
            <h3>PitchPerfect AI</h3>
        </div>
        """, unsafe_allow_html=True)

def render_figma_main_content(current_user=None):
    """Render main content area based on Figma design."""
    dark_mode = st.session_state.get('dark_mode', False)
    # Define color variables used in this function
    warning_orange = "#F59E0B"
    accent_color = "#4F46E5" if not dark_mode else "#6366F1"
    card_bg = "#FFFFFF" if not dark_mode else "#181F2A"
    border_color = "#E5E7EB" if not dark_mode else "#334155"
    text_color = "#1F2937" if not dark_mode else "#F1F5F9"
    secondary_text = "#6B7280" if not dark_mode else "#CBD5E1"

    # Set theme-based colors
    if dark_mode:
        # Dark theme - modern dark colors with vibrant accents
        bg_color = "#111827"  # Dark slate gray
        text_color = "#F9FAFB"  # White
        secondary_text = "#D1D5DB"  # Light gray
        card_bg = "#1F2937"  # Dark blue-gray
        border_color = "#374151"  # Medium gray
        button_bg = "#2D3748"  # Dark blue-gray
        button_text = "#F9FAFB"  # White
        accent_color = "#4F46E5"  # Indigo
        highlight_color = "#6366F1"  # Indigo
        drag_drop_text = "#A5B4FC"  # Light indigo for better visibility
        drag_drop_border = "#4F46E5"  # Indigo for better visibility
    else:
        # Light theme - clean whites with vibrant accents
        bg_color = "#F9FAFB"  # Very light gray
        text_color = "#111827"  # Very dark gray
        secondary_text = "#4B5563"  # Gray
        card_bg = "#FFFFFF"  # Pure white
        border_color = "#E5E7EB"  # Light gray
        button_bg = "#EDF2F7"  # Light blue-gray
        button_text = "#2D3748"  # Dark gray
        accent_color = "#4F46E5"  # Indigo
        highlight_color = "#6366F1"  # Indigo
        drag_drop_text = "#4338CA"  # Darker indigo for better visibility
        drag_drop_border = "#4F46E5"  # Indigo for better visibility

    # Add main content CSS
    st.markdown(f"""
    <style>
    .main-content-wrapper {{
        padding: 40px;
        padding-top: 100px;
        max-width: 1200px;
        margin: 0 auto;
        position: relative;
        background: {"linear-gradient(135deg, rgba(79, 70, 229, 0.02) 0%, rgba(139, 92, 246, 0.02) 100%)" if not dark_mode else "linear-gradient(135deg, rgba(79, 70, 229, 0.05) 0%, rgba(139, 92, 246, 0.05) 100%)"};
        border-radius: 16px;
        margin-top: 20px;
    }}
    
    @media (max-width: 768px) {{
        .main-content-wrapper {{
            padding: 20px;
            padding-top: 100px;
        }}
    }}
    
    /* Ensure the main content area has proper spacing */
    .main .block-container {{
        padding-top: 80px !important;
        max-width: 100% !important;
    }}
    
    /* Hide any error messages that might appear */
    .stAlert[data-baseweb="notification"] {{
        display: none !important;
    }}
    
    /* Improve overall page styling */
    .stApp {{
        background-color: {bg_color if dark_mode else "#F8FAFC"} !important;
    }}
    
    /* Style the file uploader - make it visible but styled */
    .stFileUploader {{
        margin: 20px 0;
    }}
    
    /* Dashboard theme toggle button removed */

    .upload-icon-container {{
        width: 48px;
        height: 48px;
        background: {accent_color};
        border-radius: 8px;
        display: flex;
        align-items: center;
        justify-content: center;
        margin: 0 auto 16px auto;
        color: white;
        font-size: 20px;
        transition: all 0.2s ease;
    }}
    
    .upload-area-container:hover .upload-icon-container {{
        transform: scale(1.05);
        box-shadow: 0 4px 12px rgba(79, 70, 229, 0.3);
    }}

    .upload-area-container {{
        background: {card_bg};
        border: 2px dashed {accent_color};
        border-radius: 12px;
        padding: 60px 40px;
        text-align: center;
        transition: all 0.2s ease;
        margin-bottom: 24px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
    }}

    .upload-area-container:hover {{
        border-color: {accent_color};
        background: {"rgba(79, 70, 229, 0.02)" if not dark_mode else "rgba(79, 70, 229, 0.05)"};
        transform: translateY(-2px);
        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.1);
    }}

    .browse-files-btn {{
        background: {accent_color};
        color: white;
        border: none;
        border-radius: 8px;
        padding: 12px 24px;
        font-weight: 600;
        font-size: 14px;
        cursor: pointer;
        transition: all 0.2s ease;
        margin-top: 16px;
        display: inline-block;
        box-shadow: 0 4px 12px rgba(79, 70, 229, 0.3);
    }}

    .browse-files-btn:hover {{
        background: {"#4338CA" if not dark_mode else "#5B21B6"};
        transform: translateY(-2px);
        box-shadow: 0 6px 16px rgba(79, 70, 229, 0.4);
    }}

    .supported-formats-container {{
        background: {card_bg};
        border: 1px solid {border_color};
        border-left: 4px solid #F59E0B;
        border-radius: 8px;
        padding: 16px;
        margin-top: 32px;
        display: flex;
        align-items: center;
        gap: 12px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
    }}

    .format-icon-container {{
        color: {"#D97706" if not st.session_state.get('dark_mode', False) else "#F59E0B"};
        font-size: 20px;
    }}
    </style>
    """, unsafe_allow_html=True)

    # Main content
    st.markdown(f"""
    <div class="main-content-wrapper">
        <div style="text-align: center; margin-bottom: 40px; margin-top: 20px;">
            <div class="upload-icon-container"><span style="font-size: 24px;">🚀</span></div>
            <h1 style="font-size: 28px; font-weight: 700; color: {text_color}; margin-bottom: 12px;">
                Welcome to PitchPerfect AI
            </h1>
            <p style="font-size: 16px; color: {secondary_text}; max-width: 600px; margin: 0 auto;">
                Upload your pitch deck and get AI-powered insights instantly. Our advanced analysis will help you improve your presentation and increase your chances of success.
            </p>
        </div>
        <!-- Info box with improved contrast for dark mode -->
        <div style="background: {'#23293a' if dark_mode else '#eaf6fd'}; color: {'#F1F5F9' if dark_mode else '#1A1A1A'}; padding: 24px; border-radius: 12px; margin-bottom: 24px; font-size: 16px; text-align: left;">
            <b>New to PitchPerfect?</b><br/>
            See how our AI analysis works by checking out a sample pitch deck analysis.
        </div>
        
        <!-- Upload area with dynamic theme colors -->
        <div class="upload-area-container" style="background-color: {card_bg}; border: 2px dashed {accent_color};">
            <div class="upload-icon-container" style="margin: 0 auto 20px auto; background-color: {accent_color};">
                <span style="font-size: 24px;">📤</span>
            </div>
            <h3 style="font-size: 18px; font-weight: 600; color: {text_color}; margin-bottom: 8px;">
                Drag and drop file here
            </h3>
            <p style="font-size: 14px; color: {secondary_text}; margin-bottom: 20px;">
                or
            </p>
            <div class="browse-files-btn" style="background-color: {accent_color}; color: white; border-radius: 8px; padding: 12px 24px; font-weight: 600; display: inline-block; cursor: pointer; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);">
                Browse Files
            </div>
        </div>
        
        <!-- Supported formats with dynamic theme colors -->
        <div class="supported-formats-container" style="background-color: {card_bg}; border: 1px solid {border_color}; border-left: 4px solid #F59E0B; margin-top: 20px;">
            <div class="format-icon-container" style="color: {warning_orange};">⚠️</div>
            <div>
                <div style="font-weight: 600; color: {text_color}; margin-bottom: 4px;">Supported formats:</div>
                <div style="color: {secondary_text};">PDF, PPTX, DOCX, TXT files up to 50MB</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_figma_analysis_results(score, read_score, sentiment, grade, overall_score, strengths, weaknesses, tips, keywords, recommendations):
    """Render analysis results in new design."""
    dark_mode = st.session_state.get('dark_mode', False)
    
    # Add CSS for proper spacing with navigation bar
    st.markdown("""
    <style>
    .main-content {
        padding-top: 60px; /* Add space for the navigation bar */
    }
    </style>
    """, unsafe_allow_html=True)
    
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

def render_figma_loading():
    """Render loading animation based on Figma design."""
    dark_mode = st.session_state.get('dark_mode', False)
    
    bg_color = "#1A1A1A" if dark_mode else "#FFFFFF"
    text_color = "#FFFFFF" if dark_mode else "#1A1A1A"
    
    st.markdown(f"""
    <div style="display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 60px 0;">
        <div style="width: 60px; height: 60px; border: 4px solid {'#333333' if dark_mode else '#E5E7EB'}; border-top: 4px solid {'#4F7EFF' if dark_mode else '#3B82F6'}; border-radius: 50%; animation: spin 1s linear infinite;"></div>
        <div style="margin-top: 24px; font-size: 18px; font-weight: 600; color: {text_color};">Analyzing your pitch deck...</div>
        <div style="margin-top: 8px; font-size: 14px; color: {'#A0A0A0' if dark_mode else '#6B7280'};">This may take a moment</div>
    </div>
    
    <style>
    @keyframes spin {{
        0% {{ transform: rotate(0deg); }}
        100% {{ transform: rotate(360deg); }}
    }}
    </style>
    """, unsafe_allow_html=True)

def render_figma_success(title="Success!", message="Analysis completed successfully"):
    """Render success message based on Figma design."""
    # Get current theme
    dark_mode = st.session_state.get('dark_mode', False)
    
    # Set theme-based colors
    bg_gradient = "linear-gradient(135deg, #10B981, #059669)"
    text_color = "white"
    shadow_color = f"rgba(16, 185, 129, {0.3 if dark_mode else 0.2})"
    
    # Add CSS for success card
    st.markdown(f"""
    <style>
    .success-card {{
        text-align: center;
        background: {bg_gradient};
        color: {text_color};
        border: none;
        border-radius: 16px;
        padding: 40px;
        box-shadow: 0 10px 25px {shadow_color};
        z-index: 1000;
        position: relative;
    }}
    
    @keyframes fadeIn {{
        from {{ opacity: 0; transform: translateY(20px); }}
        to {{ opacity: 1; transform: translateY(0); }}
    }}
    
    .fade-in {{
        animation: fadeIn 0.6s ease-out;
    }}
    </style>
    """, unsafe_allow_html=True)
    
    # Render success card
    st.markdown(f"""
    <div class="success-card fade-in">
        <div style="font-size: 48px; margin-bottom: 16px;">✅</div>
        <h2 style="font-size: 24px; font-weight: 700; margin-bottom: 12px;">{title}</h2>
        <p style="font-size: 16px; opacity: 0.9;">{message}</p>
    </div>
    """, unsafe_allow_html=True)