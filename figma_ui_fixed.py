import streamlit as st
from typing import Dict, List, Any

def render_figma_styles(dark_mode=False):
    """Render styles based on Figma design system."""
    # Modern color palette with vibrant accents
    primary_blue = "#3B82F6"  # Bright blue
    primary_purple = "#8B5CF6"  # Vibrant purple
    success_green = "#10B981"  # Emerald green
    warning_orange = "#F59E0B"  # Amber
    error_red = "#EF4444"  # Red
    
    # Theme colors - improved for better contrast and visual appeal
    if dark_mode:
        # Dark theme - rich dark colors with vibrant accents
        bg_color = "#0F172A"  # Deep blue-black
        text_primary = "#F8FAFC"  # Almost white
        text_secondary = "#CBD5E1"  # Light gray
        card_bg = "#1E293B"  # Dark blue-gray
        border_color = "#334155"  # Medium blue-gray
        sidebar_bg = "#0F172A"  # Deep blue-black
        main_bg = "#0F172A"  # Deep blue-black
        label_color = "#E2E8F0"  # Light gray-blue
        accent_color = "#3B82F6"  # Bright blue
        gradient_start = "#3B82F6"  # Blue
        gradient_end = "#8B5CF6"  # Purple
        shadow_color = "rgba(0, 0, 0, 0.3)"
    else:
        # Light theme - clean whites with vibrant accents
        bg_color = "#F8FAFC"  # Very light blue-gray
        text_primary = "#0F172A"  # Deep blue-black
        text_secondary = "#475569"  # Gray-blue
        card_bg = "#FFFFFF"  # Pure white
        border_color = "#E2E8F0"  # Light gray-blue
        sidebar_bg = "#FFFFFF"  # Pure white
        main_bg = "#F8FAFC"  # Very light blue-gray
        label_color = "#334155"  # Medium blue-gray
        accent_color = "#3B82F6"  # Bright blue
        gradient_start = "#3B82F6"  # Blue
        gradient_end = "#8B5CF6"  # Purple
        shadow_color = "rgba(0, 0, 0, 0.1)"
    
    st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');
    
    * {{
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }}
    
    .stApp {{
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif !important;
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
    
    /* Metrics Cards */
    .metric-card {{
        background: {card_bg} !important;
        border: none !important;
        border-radius: 16px !important;
        padding: 28px 24px !important;
        text-align: center !important;
        transition: all 0.3s ease !important;
        position: relative !important;
        overflow: hidden !important;
        box-shadow: 0 4px 20px {shadow_color} !important;
    }}
    
    .metric-card::before {{
        content: '' !important;
        position: absolute !important;
        top: 0 !important;
        left: 0 !important;
        right: 0 !important;
        height: 4px !important;
        background: linear-gradient(90deg, {gradient_start}, {gradient_end}) !important;
    }}
    
    .metric-card:hover {{
        transform: translateY(-5px) !important;
        box-shadow: 0 8px 30px {shadow_color} !important;
    }}
    
    .metric-value {{
        font-size: 36px !important;
        font-weight: 800 !important;
        background: linear-gradient(90deg, {gradient_start}, {gradient_end}) !important;
        -webkit-background-clip: text !important;
        -webkit-text-fill-color: transparent !important;
        margin: 12px 0 8px 0 !important;
        line-height: 1.2 !important;
    }}
    
    .metric-label {{
        font-size: 13px !important;
        color: {text_secondary} !important;
        font-weight: 600 !important;
        text-transform: uppercase !important;
        letter-spacing: 1px !important;
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
    </style>
    """, unsafe_allow_html=True)

def render_figma_main_content():
    """Render main content area based on Figma design."""
    dark_mode = st.session_state.get('dark_mode', False)
    
    # Set theme-based colors
    if dark_mode:
        bg_color = "#1A1A1A"
        text_color = "#FFFFFF"
        secondary_text = "#A0A0A0"
        card_bg = "#2A2A2A"
        border_color = "#3A3A3A"
        button_bg = "#2D3748"
        button_text = "#FFFFFF"
        accent_color = "#4F7EFF"
    else:
        bg_color = "#F8F9FA"
        text_color = "#1A1A1A"
        secondary_text = "#6B7280"
        card_bg = "#FFFFFF"
        border_color = "#E5E7EB"
        button_bg = "#EDF2F7"
        button_text = "#2D3748"
        accent_color = "#3182CE"
    
    # Add main content CSS
    st.markdown(f"""
    <style>
    .main-content-wrapper {{
        padding: 40px;
        max-width: 1200px;
        margin: 0 auto;
    }}
    
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
    }}
    
    .upload-area-container {{
        background: {card_bg};
        border: 2px dashed {border_color};
        border-radius: 12px;
        padding: 60px 40px;
        text-align: center;
        margin-bottom: 24px;
    }}
    
    .format-info-box {{
        background: {"rgba(245, 158, 11, 0.1)" if not dark_mode else "rgba(245, 158, 11, 0.2)"};
        border: 1px solid {"rgba(245, 158, 11, 0.2)" if not dark_mode else "rgba(245, 158, 11, 0.3)"};
        border-radius: 8px;
        padding: 12px 16px;
        margin-top: 24px;
        display: flex;
        align-items: center;
        gap: 8px;
    }}
    
    .theme-toggle-btn {{
        position: fixed;
        top: 20px;
        right: 20px;
        background: {button_bg};
        color: {button_text};
        border: 1px solid {border_color};
        border-radius: 8px;
        padding: 8px 16px;
        font-size: 14px;
        cursor: pointer;
        z-index: 1000;
        display: flex;
        align-items: center;
        gap: 8px;
        transition: all 0.2s ease;
    }}
    
    .theme-toggle-btn:hover {{
        background: {accent_color};
        color: white;
    }}
    </style>
    """, unsafe_allow_html=True)
    
    # Add theme toggle button to the top right
    theme_text = "🌙 Light Mode" if dark_mode else "☀️ Dark Mode"
    st.markdown(f"""
    <button class="theme-toggle-btn" id="theme-toggle-main" onclick="toggleTheme()">
        {theme_text}
    </button>
    
    <script>
    function toggleTheme() {{
        // Toggle the theme state
        const themeToggleBtn = document.querySelector('[data-testid="stSidebar"] button[kind="secondary"]');
        if (themeToggleBtn) {{
            themeToggleBtn.click();
        }}
    }}
    </script>
    """, unsafe_allow_html=True)
    
    # Create a container for the main content
    main_container = st.container()
    
    with main_container:
        # Title section
        st.markdown(f"""
        <div class="main-content-wrapper">
            <div style="text-align: center; margin-bottom: 40px;">
                <div class="upload-icon-container">
                    <span style="font-size: 24px;">📤</span>
                </div>
                <h1 style="font-size: 24px; font-weight: 700; color: {text_color}; margin-bottom: 8px;">
                    PitchPerfect AI - Your Personal Pitch Deck Analyst
                </h1>
                <p style="font-size: 16px; color: {secondary_text};">
                    Upload your deck and get AI-powered insights instantly
                </p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Upload area
        col1, col2, col3 = st.columns([1, 3, 1])
        with col2:
            st.markdown(f"""
            <div class="upload-area-container">
                <div class="upload-icon-container" style="margin: 0 auto 20px auto;">
                    <span style="font-size: 24px;">📤</span>
                </div>
                <h3 style="font-size: 18px; font-weight: 600; color: {text_color}; margin-bottom: 8px;">
                    Drop your pitch deck here
                </h3>
                <p style="font-size: 14px; color: {secondary_text}; margin-bottom: 16px;">
                    or
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            # The actual file uploader is in app.py, this is just for display
            
            # Format information
            st.markdown(f"""
            <div class="format-info-box">
                <div style="color: #F59E0B; font-size: 16px;">⚠️</div>
                <div>
                    <div style="font-size: 14px; font-weight: 600; color: {text_color};">Supported formats:</div>
                    <div style="font-size: 14px; color: {secondary_text};">PDF, PPTX, DOCX, TXT files up to 50MB</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

def render_figma_analysis_results(score, read_score, sentiment, grade, overall_score, strengths, weaknesses, tips, keywords, recommendations):
    """Render analysis results in new design."""
    dark_mode = st.session_state.get('dark_mode', False)
    
    # Set theme-based colors
    if dark_mode:
        bg_color = "#1A1A1A"
        text_color = "#FFFFFF"
        secondary_text = "#A0A0A0"
        card_bg = "#2A2A2A"
        border_color = "#3A3A3A"
    else:
        bg_color = "#F8F9FA"
        text_color = "#1A1A1A"
        secondary_text = "#6B7280"
        card_bg = "#FFFFFF"
        border_color = "#E5E7EB"
    
    # Add CSS for analysis results
    st.markdown(f"""
    <style>
    .results-container {{
        padding: 20px;
        max-width: 1200px;
        margin: 0 auto;
    }}
    
    .metric-card {{
        background: {card_bg};
        border: 1px solid {border_color};
        border-radius: 16px;
        padding: 24px;
        text-align: center;
        position: relative;
        overflow: hidden;
        height: 100%;
    }}
    
    .metric-card::before {{
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(90deg, #4F7EFF, #7C3AED);
    }}
    
    .metric-value {{
        font-size: 32px;
        font-weight: 800;
        color: #4F7EFF;
        margin: 12px 0 8px 0;
    }}
    
    .metric-label {{
        font-size: 14px;
        color: {secondary_text};
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }}
    
    .insight-card {{
        background: {card_bg};
        border: none;
        border-radius: 16px;
        padding: 28px;
        height: 100%;
        box-shadow: 0 4px 20px {shadow_color};
        transition: all 0.3s ease;
    }}
    
    .insight-card:hover {{
        transform: translateY(-5px);
        box-shadow: 0 8px 30px {shadow_color};
    }}
    
    .insight-title {{
        font-size: 18px;
        font-weight: 700;
        color: {text_color};
        margin-bottom: 20px;
        display: flex;
        align-items: center;
        gap: 10px;
        position: relative;
        padding-bottom: 12px;
    }}
    
    .insight-title::after {{
        content: '';
        position: absolute;
        bottom: 0;
        left: 0;
        width: 40px;
        height: 3px;
        background: linear-gradient(90deg, {gradient_start}, {gradient_end});
        border-radius: 3px;
    }}
    
    .tag {{
        display: inline-block;
        padding: 8px 16px;
        border-radius: 100px;
        font-size: 13px;
        font-weight: 600;
        margin: 4px;
        transition: all 0.2s ease;
        box-shadow: 0 2px 5px {shadow_color};
    }}
    
    .tag:hover {{
        transform: translateY(-2px);
        box-shadow: 0 4px 8px {shadow_color};
    }}
    
    .tag-primary {{
        background: {'rgba(59, 130, 246, 0.15)' if dark_mode else 'rgba(59, 130, 246, 0.1)'};
        color: #3B82F6;
        border: none;
    }}
    
    .tag-success {{
        background: {'rgba(16, 185, 129, 0.15)' if dark_mode else 'rgba(16, 185, 129, 0.1)'};
        color: #10B981;
        border: none;
    }}
    
    .tag-warning {{
        background: {'rgba(245, 158, 11, 0.15)' if dark_mode else 'rgba(245, 158, 11, 0.1)'};
        color: #F59E0B;
        border: none;
    }}
    
    .tag-error {{
        background: {'rgba(239, 68, 68, 0.15)' if dark_mode else 'rgba(239, 68, 68, 0.1)'};
        color: #EF4444;
        border: none;
    }}
    
    .ai-rec-container {{
        background: {card_bg};
        border-radius: 20px;
        padding: 2.5rem;
        border: none;
        box-shadow: 0 8px 30px {shadow_color};
        margin: 50px 0;
        transition: all 0.3s ease;
    }}
    
    .ai-rec-container:hover {{
        transform: translateY(-5px);
        box-shadow: 0 12px 40px {shadow_color};
    }}
    
    .ai-rec-title {{
        font-size: 1.75rem;
        font-weight: 800;
        background: linear-gradient(90deg, {gradient_start}, {gradient_end});
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 2rem;
        display: flex;
        align-items: center;
        gap: 1rem;
        position: relative;
        padding-bottom: 15px;
    }}
    
    .ai-rec-title::after {{
        content: '';
        position: absolute;
        bottom: 0;
        left: 0;
        width: 60px;
        height: 4px;
        background: linear-gradient(90deg, {gradient_start}, {gradient_end});
        border-radius: 4px;
    }}
    
    .ai-rec-item {{
        background: {'#1A2234' if dark_mode else '#F1F5F9'};
        border-left: 4px solid {gradient_start};
        padding: 1.25rem;
        margin: 1rem 0;
        border-radius: 0 12px 12px 0;
        border: none;
        box-shadow: 0 4px 12px {shadow_color};
        transition: all 0.2s ease;
    }}
    
    .ai-rec-item:hover {{
        transform: translateX(5px);
        box-shadow: 0 6px 15px {shadow_color};
    }}
    
    .theme-toggle-btn {{
        position: fixed;
        top: 20px;
        right: 20px;
        background: {'rgba(59, 130, 246, 0.15)' if dark_mode else 'rgba(255, 255, 255, 0.9)'};
        color: {'#FFFFFF' if dark_mode else '#3B82F6'};
        border: none;
        border-radius: 100px;
        padding: 10px 20px;
        font-size: 14px;
        font-weight: 600;
        cursor: pointer;
        z-index: 1000;
        display: flex;
        align-items: center;
        gap: 8px;
        transition: all 0.3s ease;
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        box-shadow: 0 4px 15px {shadow_color};
    }}
    
    .theme-toggle-btn:hover {{
        background: {'rgba(59, 130, 246, 0.3)' if dark_mode else 'rgba(59, 130, 246, 0.1)'};
        transform: translateY(-3px);
        box-shadow: 0 8px 25px {shadow_color};
    }}
    </style>
    """, unsafe_allow_html=True)
    
    # Add theme toggle button to the top right
    theme_text = "🌙 Light Mode" if dark_mode else "☀️ Dark Mode"
    st.markdown(f"""
    <button class="theme-toggle-btn" id="theme-toggle-results" onclick="toggleTheme()">
        {theme_text}
    </button>
    
    <script>
    function toggleTheme() {{
        // Toggle the theme state
        const themeToggleBtn = document.querySelector('[data-testid="stSidebar"] button[kind="secondary"]');
        if (themeToggleBtn) {{
            themeToggleBtn.click();
        }}
    }}
    </script>
    """, unsafe_allow_html=True)
    
    # Title
    st.markdown(f"""
    <div class="results-container">
        <h2 style="font-size: 24px; font-weight: 700; color: {text_color}; margin-bottom: 24px;">
            📊 Analysis Results
        </h2>
    </div>
    """, unsafe_allow_html=True)
    
    # Metrics Grid using Streamlit columns
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Section Coverage</div>
            <div class="metric-value">{score}/10</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Readability</div>
            <div class="metric-value">{read_score:.0f}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Overall Score</div>
            <div class="metric-value">{overall_score}/100</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Grade</div>
            <div class="metric-value">{grade}</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Add some spacing
    st.markdown("<div style='height: 30px;'></div>", unsafe_allow_html=True)
    
    # Insights section - first row
    col1, col2 = st.columns(2)
    
    # Strengths
    with col1:
        st.markdown(f"""
        <div class="insight-card">
            <div class="insight-title">✨ Strengths</div>
            <div style="display: flex; flex-wrap: wrap; gap: 8px;">
        """, unsafe_allow_html=True)
        
        for strength in strengths:
            st.markdown(f'<span class="tag tag-success">{strength}</span>', unsafe_allow_html=True)
        
        st.markdown("</div></div>", unsafe_allow_html=True)
    
    # Areas to improve
    with col2:
        st.markdown(f"""
        <div class="insight-card">
            <div class="insight-title">⚠️ Areas to Improve</div>
            <div style="display: flex; flex-wrap: wrap; gap: 8px;">
        """, unsafe_allow_html=True)
        
        for weakness in weaknesses:
            st.markdown(f'<span class="tag tag-error">{weakness}</span>', unsafe_allow_html=True)
        
        st.markdown("</div></div>", unsafe_allow_html=True)
    
    # Add some spacing
    st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
    
    # Insights section - second row
    col3, col4 = st.columns(2)
    
    # Recommendations
    with col3:
        st.markdown(f"""
        <div class="insight-card">
            <div class="insight-title">💡 Recommendations</div>
            <div style="display: flex; flex-wrap: wrap; gap: 8px;">
        """, unsafe_allow_html=True)
        
        for tip in tips:
            st.markdown(f'<span class="tag tag-warning">{tip}</span>', unsafe_allow_html=True)
        
        st.markdown("</div></div>", unsafe_allow_html=True)
    
    # Key Terms
    with col4:
        st.markdown(f"""
        <div class="insight-card">
            <div class="insight-title">🔑 Key Terms</div>
            <div style="display: flex; flex-wrap: wrap; gap: 8px;">
        """, unsafe_allow_html=True)
        
        for keyword in keywords:
            st.markdown(f'<span class="tag tag-primary">{keyword}</span>', unsafe_allow_html=True)
        
        st.markdown("</div></div>", unsafe_allow_html=True)
    
    # AI Recommendations
    if recommendations:
        st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="results-container">
            <div class="ai-rec-container">
                <div class="ai-rec-title">
                    🤖 AI Recommendations
                </div>
        """, unsafe_allow_html=True)
        
        for i, rec in enumerate(recommendations, 1):
            st.markdown(f"""
            <div class="ai-rec-item">
                <strong style="color: {text_color};">{i}.</strong> <span style="color: {secondary_text};">{rec}</span>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("</div></div>", unsafe_allow_html=True)

def render_figma_loading():
    """Render loading animation based on Figma design."""
    # Add CSS for spinner
    st.markdown("""
    <style>
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    .loading-spinner {
        width: 48px;
        height: 48px;
        border: 4px solid #E2E8F0;
        border-top: 4px solid #2563EB;
        border-radius: 50%;
        animation: spin 1s linear infinite;
        margin: 0 auto 20px auto;
    }
    
    .loading-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        padding: 80px 40px;
        text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Loading content
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("""
        <div class="loading-container">
            <div class="loading-spinner"></div>
            <h3 style="font-size: 24px; font-weight: 700; margin-bottom: 12px; color: #2563EB;">Analyzing Your Pitch Deck</h3>
            <p style="font-size: 16px; color: #64748B;">Our AI is processing your presentation...</p>
        </div>
        """, unsafe_allow_html=True)

def render_figma_success(title="Success!", message="Analysis completed successfully"):
    """Render success message based on Figma design."""
    # Add CSS for success card
    st.markdown("""
    <style>
    .success-card {
        text-align: center;
        background: linear-gradient(135deg, #10B981, #059669);
        color: white;
        border: none;
        border-radius: 16px;
        padding: 40px;
        box-shadow: 0 10px 25px rgba(16, 185, 129, 0.2);
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .fade-in {
        animation: fadeIn 0.6s ease-out;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Success content
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown(f"""
        <div class="success-card fade-in">
            <div style="font-size: 64px; margin-bottom: 24px;">🎉</div>
            <h2 style="font-size: 32px; font-weight: 800; margin-bottom: 12px;">{title}</h2>
            <p style="font-size: 18px; opacity: 0.9;">{message}</p>
        </div>
        """, unsafe_allow_html=True)