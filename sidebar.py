import streamlit as st

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

def render_figma_sidebar(current_user=None, analyses=None):
    """Render sidebar based on Figma design."""
    try:
        dark_mode = st.session_state.get('dark_mode', False)
        
        # Get user info safely
        user_data = extract_user_data_safely(current_user)
        user_name = user_data['name']
        user_email = user_data['email']
        user_initial = user_data['initial']
        
        # Safely handle analyses data
        analyses = analyses if analyses is not None else []
        
        # Theme-based colors with Indigo & Slate palette
        if dark_mode:
            # Dark Mode Palette (Futuristic & Luxurious)
            bg_color = "#0F172A"  # Deep navy slate — stylish, easy on eyes
            text_color = "#F1F5F9"  # Very light gray — for high contrast
            secondary_text = "#94A3B8"  # Muted cool gray — subtle and elegant
            card_bg = "#1E293B"  # Slightly raised, matte container look
            border_color = "#334155"  # Muted navy-gray for subtle dividers
            accent_color = "#6366F1"  # Soft lavender blue — pops beautifully
            hover_bg = "#1E293B"  # Slightly raised, matte container look
            badge_bg = "#22C55E"  # Powerful green shade that stands out
            badge_text = "#F1F5F9"  # Very light gray for text
        else:
            # Light Mode Palette (Elegant & Sleek)
            bg_color = "#F9FAFB"  # Very light gray; relaxing, not pure white
            text_color = "#1F2937"  # Dark slate — calm but strong readability
            secondary_text = "#6B7280"  # Cool gray — for subtle descriptions
            card_bg = "#FFFFFF"  # Pure white for a clean, layered look
            border_color = "#E5E7EB"  # Light gray for subtle separation
            accent_color = "#4F46E5"  # Premium indigo — for CTAs, links, focus
            hover_bg = "#F1F5F9"  # Very light gray for hover
            badge_bg = "#10B981"  # Vibrant green for success messages
            badge_text = "#FFFFFF"  # White for text
        
        # Apply styles for sidebar with responsive design
        st.markdown(f"""
    <style>
    /* Desktop sidebar */
    @media (min-width: 992px) {{
        section.main > div:first-child {{
            padding-left: 280px;
        }}
        
        [data-testid="stSidebar"] {{
            width: 280px;
            background-color: {bg_color};
            border-right: 1px solid {border_color};
        }}
    }}
    
    /* Tablet sidebar */
    @media (min-width: 768px) and (max-width: 991px) {{
        section.main > div:first-child {{
            padding-left: 240px;
        }}
        
        [data-testid="stSidebar"] {{
            width: 240px;
            background-color: {bg_color};
            border-right: 1px solid {border_color};
        }}
    }}
    
    /* Mobile sidebar - overlay style */
    @media (max-width: 767px) {{
        section.main > div:first-child {{
            padding-left: 0;
        }}
        
        [data-testid="stSidebar"] {{
            width: 100%;
            background-color: {bg_color};
            border-right: none;
        }}
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
            
            # Theme toggle with Indigo & Slate palette
            st.markdown(f"""
            <style>
            /* Ensure theme toggle button is always visible and attractive */
            [data-testid="baseButton-secondary"] {{
                z-index: 1000 !important;
                position: relative !important;
            }}
            
            /* Custom theme toggle button styling with Indigo & Slate palette */
            .theme-toggle-button {{
                background-color: {"#6366F1" if dark_mode else "#4F46E5"};
                color: white;
                border: none;
                border-radius: 8px;
                padding: 12px 16px;
                font-weight: 600;
                font-size: 14px;
                cursor: pointer;
                width: 100%;
                text-align: center;
                box-shadow: 0 4px 6px {"rgba(99, 102, 241, 0.4)" if dark_mode else "rgba(79, 70, 229, 0.2)"};
                transition: all 0.2s ease;
                display: flex;
                align-items: center;
                justify-content: center;
                gap: 8px;
            }}
            
            .theme-toggle-button:hover {{
                background-color: {"#4F46E5" if dark_mode else "#4338CA"};
                transform: translateY(-1px);
                box-shadow: 0 6px 8px {"rgba(99, 102, 241, 0.5)" if dark_mode else "rgba(79, 70, 229, 0.3)"};
            }}
            
            /* Make sure the theme toggle button is always visible and prominent */
            [data-testid="stSidebar"] button[kind="secondary"] {{
                background-color: {"#6366F1" if dark_mode else "#4F46E5"} !important;
                color: white !important;
                border: none !important;
                border-radius: 8px !important;
                padding: 12px 16px !important;
                font-weight: 600 !important;
                margin-top: 16px !important;
                margin-bottom: 16px !important;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1) !important;
                transition: all 0.2s ease !important;
                z-index: 1000 !important;
                position: relative !important;
                display: flex !important;
                align-items: center !important;
                justify-content: center !important;
                width: 100% !important;
                font-size: 16px !important;
            }}
            
            [data-testid="stSidebar"] button[kind="secondary"]:hover {{
                background-color: {"#4F46E5" if dark_mode else "#4338CA"} !important;
                transform: translateY(-1px) !important;
                box-shadow: 0 6px 8px rgba(0, 0, 0, 0.15) !important;
            }}
            </style>
            """, unsafe_allow_html=True)
            
            # Use the standard rectangular theme toggle button
            theme_icon = "🌙" if dark_mode else "☀️"
            theme_text = f"{theme_icon} {'Light' if dark_mode else 'Dark'} Theme"
            
            if st.button(theme_text, key="theme_toggle", use_container_width=True, help="Switch between light and dark mode"):
                # Update the theme state
                st.session_state.dark_mode = not dark_mode
                # Force a complete page reload
                st.rerun()
    
    except Exception as e:
        # Error boundary for sidebar
        st.sidebar.error(f"Sidebar error: {str(e)}")
        # Render minimal fallback sidebar
        st.sidebar.markdown("### PitchPerfect AI")
        st.sidebar.markdown("Navigation temporarily unavailable")