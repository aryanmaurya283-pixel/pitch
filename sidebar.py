import streamlit as st

def render_figma_sidebar(current_user=None, analyses=None):
    """Render sidebar based on Figma design."""
    dark_mode = st.session_state.get('dark_mode', False)
    
    # Get user info
    user_name = current_user.user_metadata.get('name', 'User') if current_user else 'User'
    user_email = current_user.email if current_user else 'user@example.com'
    user_initial = user_name[0].upper() if user_name else 'U'
    
    # Theme-based colors - improved for better visibility
    if dark_mode:
        bg_color = "#1A1A1A"
        text_color = "#FFFFFF"
        secondary_text = "#CCCCCC"
        border_color = "#444444"
        card_bg = "#2A2A2A"
        accent_color = "#4F7EFF"
        hover_bg = "#333333"
        badge_bg = "#10B981"
        badge_text = "#FFFFFF"
    else:
        bg_color = "#FFFFFF"
        text_color = "#1A202C"
        secondary_text = "#4A5568"
        border_color = "#E2E8F0"
        card_bg = "#F8FAFC"
        accent_color = "#3182CE"
        hover_bg = "#EDF2F7"
        badge_bg = "#38A169"
        badge_text = "#FFFFFF"
    
    # Apply styles for sidebar
    st.markdown(f"""
    <style>
    section.main > div:first-child {{
        padding-left: 280px;
    }}
    
    [data-testid="stSidebar"] {{
        width: 280px;
        background-color: {bg_color};
        border-right: 1px solid {border_color};
    }}
    
    [data-testid="stSidebar"] > div:first-child {{
        padding: 2rem 1rem;
    }}
    
    .logo-container {{
        display: flex;
        align-items: center;
        gap: 12px;
        margin-bottom: 24px;
    }}
    
    .logo-icon {{
        width: 32px;
        height: 32px;
        background: {accent_color};
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
        color: {text_color};
    }}
    
    .logo-subtitle {{
        font-size: 12px;
        color: {secondary_text};
        margin-top: 2px;
    }}
    
    .custom-button {{
        width: 100%;
        background: {accent_color};
        color: white;
        border: none;
        border-radius: 8px;
        padding: 12px 16px;
        font-weight: 600;
        font-size: 14px;
        cursor: pointer;
        margin-bottom: 24px;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 8px;
        transition: all 0.2s ease;
    }}
    
    .custom-button:hover {{
        background: #3B6EFF;
        transform: translateY(-1px);
    }}
    
    .section-heading {{
        font-size: 14px;
        font-weight: 600;
        color: {text_color};
        margin-bottom: 16px;
    }}
    
    .analysis-card {{
        background: {card_bg};
        border: 1px solid {border_color};
        border-radius: 8px;
        padding: 12px;
        margin-bottom: 8px;
        cursor: pointer;
        transition: all 0.2s ease;
    }}
    
    .analysis-card:hover {{
        border-color: {accent_color};
        transform: translateY(-1px);
    }}
    
    .analysis-title {{
        font-size: 14px;
        font-weight: 600;
        color: {text_color};
        margin-bottom: 4px;
    }}
    
    .analysis-date {{
        font-size: 12px;
        color: {secondary_text};
    }}
    
    .analysis-badge {{
        background: {badge_bg};
        color: {badge_text};
        font-size: 10px;
        font-weight: 600;
        padding: 4px 8px;
        border-radius: 4px;
        float: right;
    }}
    
    .user-card {{
        background: {card_bg};
        border: 1px solid {border_color};
        border-radius: 8px;
        padding: 12px;
        display: flex;
        align-items: center;
        gap: 12px;
        margin-top: 24px;
    }}
    
    .user-avatar {{
        width: 32px;
        height: 32px;
        background: {accent_color};
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
        color: {text_color};
    }}
    
    .user-email {{
        font-size: 12px;
        color: {secondary_text};
    }}
    
    /* Hide default Streamlit elements */
    #MainMenu, footer, header {{
        visibility: hidden;
    }}
    
    /* Hide debug elements */
    .debug-info {{
        display: none !important;
    }}
    </style>
    """, unsafe_allow_html=True)
    
    # Configure the sidebar
    st.sidebar.markdown("""
    <style>
    [data-testid="stSidebarNav"] {
        display: none;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Use Streamlit's sidebar
    with st.sidebar:
        # Logo and title
        st.markdown(f"""
        <div class="logo-container">
            <div class="logo-icon"><span style="font-size: 18px;">🚀</span></div>
            <div>
                <div class="logo-text">PitchPerfect AI</div>
                <div class="logo-subtitle">AI-powered pitch deck analysis</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Upload button - using Streamlit button with custom styling
        st.markdown(f"""
        <button class="custom-button" onclick="document.querySelector('input[type=file]').click()">
            📤 Upload New Deck
        </button>
        """, unsafe_allow_html=True)
        
        # Section title
        st.markdown('<div class="section-heading">📁 Past Analyses</div>', unsafe_allow_html=True)
        
        # Analyses list
        if analyses:
            for i, analysis in enumerate(analyses[:5]):  # Show only first 5
                score = analysis.get('score', 0)
                score_color = "#10B981" if score >= 7 else "#F59E0B" if score >= 5 else "#EF4444"
                filename = analysis.get('filename', 'Untitled')
                date = analysis.get('date', 'No date')
                
                st.markdown(f"""
                <div class="analysis-card">
                    <div class="analysis-badge" style="background: {score_color};">{score}/10</div>
                    <div class="analysis-title">{filename[:20]}{'...' if len(filename) > 20 else ''}</div>
                    <div class="analysis-date">{date[:16] if date else ''}</div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.markdown(f'<div style="color: {secondary_text}; font-size: 13px; text-align: center; padding: 20px 0;">No analyses yet</div>', unsafe_allow_html=True)
        
        # Spacer
        st.markdown("<div style='flex-grow: 1; min-height: 50px;'></div>", unsafe_allow_html=True)
        
        # User profile
        st.markdown(f"""
        <div class="user-card">
            <div class="user-avatar">{user_initial}</div>
            <div class="user-info">
                <div class="user-name">{user_name}</div>
                <div class="user-email">{user_email}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Theme toggle
        theme_text = "🌙 Light Theme" if dark_mode else "☀️ Dark Theme"
        if st.button(theme_text, key="theme_toggle", use_container_width=True):
            st.session_state.dark_mode = not st.session_state.get('dark_mode', False)
            st.rerun()