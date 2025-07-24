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
    """Render an improved sidebar with user info and better signout button."""
    # Get theme and user data
    dark_mode = st.session_state.get('dark_mode', False)
    user_data = extract_user_data_safely(current_user)
    
    # Theme colors
    if dark_mode:
        sidebar_bg = "#1E293B"
        card_bg = "#334155"
        text_primary = "#F1F5F9"
        text_secondary = "#CBD5E1"
        border_color = "#475569"
        accent_color = "#6366F1"
    else:
        sidebar_bg = "#FFFFFF"
        card_bg = "#F8FAFC"
        text_primary = "#1F2937"
        text_secondary = "#6B7280"
        border_color = "#E5E7EB"
        accent_color = "#4F46E5"
    
    st.sidebar.markdown(f"""
    <style>
    [data-testid="stSidebar"] {{
        background: {sidebar_bg} !important;
        margin-top: 70px !important;
        padding: 0 !important;
        height: calc(100vh - 70px);
        border-right: 2px solid {border_color};
        box-shadow: 4px 0 12px rgba(0,0,0,0.1);
        position: relative;
    }}
    
    .sidebar-content {{
        height: 100%;
        display: flex;
        flex-direction: column;
        padding-bottom: 120px;
        overflow-y: auto;
    }}
    
    .sidebar-header {{
        padding: 28px 24px;
        background: linear-gradient(135deg, {accent_color}08 0%, {accent_color}03 100%);
        border-bottom: 2px solid {border_color};
        margin-bottom: 0;
    }}
    
    .user-profile {{
        display: flex;
        align-items: center;
        gap: 16px;
        margin-bottom: 20px;
        padding: 16px;
        background: {card_bg};
        border-radius: 16px;
        border: 1px solid {border_color};
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
    }}
    
    .user-avatar {{
        width: 56px;
        height: 56px;
        background: linear-gradient(135deg, {accent_color} 0%, {accent_color}DD 100%);
        border-radius: 16px;
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        font-weight: 800;
        font-size: 24px;
        box-shadow: 0 6px 16px {accent_color}40;
        border: 3px solid {sidebar_bg};
    }}
    
    .user-info {{
        flex: 1;
        min-width: 0;
    }}
    
    .user-name {{
        font-size: 18px;
        font-weight: 800;
        color: {text_primary};
        margin: 0 0 6px 0;
        line-height: 1.2;
        letter-spacing: -0.3px;
    }}
    
    .user-email {{
        font-size: 13px;
        color: {text_secondary};
        margin: 0;
        line-height: 1.2;
        opacity: 0.8;
    }}
    
    .stats-grid {{
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 16px;
        margin-top: 20px;
    }}
    
    .stat-item {{
        background: {card_bg};
        border: 2px solid {border_color};
        border-radius: 12px;
        padding: 16px 12px;
        text-align: center;
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }}
    
    .stat-item::before {{
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: linear-gradient(90deg, {accent_color} 0%, {accent_color}80 100%);
    }}
    
    .stat-item:hover {{
        transform: translateY(-2px);
        box-shadow: 0 8px 20px rgba(0,0,0,0.1);
        border-color: {accent_color};
    }}
    
    .stat-number {{
        font-size: 24px;
        font-weight: 800;
        color: {accent_color};
        margin: 0 0 6px 0;
        line-height: 1;
    }}
    
    .stat-label {{
        font-size: 11px;
        color: {text_secondary};
        margin: 0;
        text-transform: uppercase;
        letter-spacing: 0.8px;
        font-weight: 600;
    }}
    
    .sidebar-section {{
        padding: 20px 24px;
        border-bottom: 1px solid {border_color};
        flex: 1;
        overflow-y: auto;
        margin-bottom: 20px;
    }}
    
    .section-title {{
        font-size: 13px;
        font-weight: 700;
        color: {text_secondary};
        margin: 0 0 16px 0;
        text-transform: uppercase;
        letter-spacing: 1px;
        display: flex;
        align-items: center;
        gap: 8px;
    }}
    
    .section-title::before {{
        content: '';
        width: 3px;
        height: 16px;
        background: {accent_color};
        border-radius: 2px;
    }}
    
    .sidebar-signout {{
        position: absolute;
        bottom: 20px;
        left: 20px;
        right: 20px;
        z-index: 1000;
        background: {sidebar_bg};
        padding-top: 16px;
        border-top: 2px solid {border_color};
    }}
    
    .signout-btn {{
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 12px;
        background: linear-gradient(135deg, #EF4444 0%, #DC2626 100%);
        color: white !important;
        padding: 18px 24px;
        border-radius: 16px;
        font-weight: 700;
        font-size: 16px;
        text-decoration: none !important;
        box-shadow: 0 6px 20px rgba(239, 68, 68, 0.3);
        transition: all 0.3s ease;
        border: none;
        width: 100%;
        position: relative;
        overflow: hidden;
    }}
    
    .signout-btn::before {{
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
        transition: left 0.5s;
    }}
    
    .signout-btn:hover::before {{
        left: 100%;
    }}
    
    .signout-btn:hover {{
        background: linear-gradient(135deg, #DC2626 0%, #B91C1C 100%);
        transform: translateY(-3px);
        box-shadow: 0 8px 25px rgba(239, 68, 68, 0.4);
    }}
    
    .signout-btn:active {{
        transform: translateY(-1px);
    }}
    
    .recent-analyses {{
        max-height: 280px;
        overflow-y: auto;
        padding-right: 8px;
    }}
    
    .recent-analyses::-webkit-scrollbar {{
        width: 4px;
    }}
    
    .recent-analyses::-webkit-scrollbar-track {{
        background: {border_color};
        border-radius: 2px;
    }}
    
    .recent-analyses::-webkit-scrollbar-thumb {{
        background: {accent_color};
        border-radius: 2px;
    }}
    
    .analysis-item {{
        background: {card_bg};
        border: 1px solid {border_color};
        border-radius: 12px;
        padding: 16px;
        margin-bottom: 12px;
        transition: all 0.3s ease;
        cursor: pointer;
        position: relative;
        overflow: hidden;
    }}
    
    .analysis-item::before {{
        content: '';
        position: absolute;
        left: 0;
        top: 0;
        bottom: 0;
        width: 4px;
        background: {accent_color};
        transform: scaleY(0);
        transition: transform 0.3s ease;
    }}
    
    .analysis-item:hover {{
        transform: translateX(4px);
        box-shadow: 0 6px 16px rgba(0,0,0,0.1);
        border-color: {accent_color};
    }}
    
    .analysis-item:hover::before {{
        transform: scaleY(1);
    }}
    
    .analysis-header {{
        display: flex;
        align-items: center;
        gap: 10px;
        margin-bottom: 8px;
    }}
    
    .analysis-icon {{
        font-size: 16px;
        opacity: 0.7;
    }}
    
    .analysis-filename {{
        font-size: 14px;
        font-weight: 700;
        color: {text_primary};
        margin: 0;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
        flex: 1;
    }}
    
    .analysis-meta {{
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-top: 8px;
    }}
    
    .analysis-date {{
        font-size: 11px;
        color: {text_secondary};
        margin: 0;
        opacity: 0.8;
    }}
    
    .analysis-score {{
        font-size: 12px;
        font-weight: 600;
        color: {accent_color};
        background: {accent_color}15;
        padding: 2px 8px;
        border-radius: 12px;
    }}
    
    .empty-state {{
        text-align: center;
        padding: 32px 16px;
        color: {text_secondary};
        opacity: 0.7;
    }}
    
    .empty-icon {{
        font-size: 32px;
        margin-bottom: 12px;
        opacity: 0.5;
    }}
    </style>
    
    <div class="sidebar-content">
        <div class="sidebar-header">
            <div class="user-profile">
                <div class="user-avatar">{user_data['initial']}</div>
                <div class="user-info">
                    <div class="user-name">{user_data['name']}</div>
                    <div class="user-email">{user_data['email']}</div>
                </div>
            </div>
            <div class="stats-grid">
                <div class="stat-item">
                    <div class="stat-number">{len(analyses) if analyses else 0}</div>
                    <div class="stat-label">Analyses</div>
                </div>
                <div class="stat-item">
                    <div class="stat-number">Pro</div>
                    <div class="stat-label">Plan</div>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # Recent analyses section
    st.sidebar.markdown("""
    <div class="sidebar-section">
        <div class="section-title">Recent Analyses</div>
        <div class="recent-analyses">
    """, unsafe_allow_html=True)
    
    # Add refresh button
    if st.sidebar.button("Refresh", help="Refresh analyses", key="refresh_analyses"):
        if 'analyses' in st.session_state:
            del st.session_state.analyses
        st.rerun()
    
    # Display analyses or empty state
    if analyses and len(analyses) > 0:
        for analysis in analyses[:5]:  # Show only last 5
            # Get filename and truncate if too long
            filename = analysis.get('filename', 'Unknown File')
            if len(filename) > 20:
                filename = filename[:17] + '...'
            
            # Format date
            date = analysis.get('created_at', analysis.get('date', 'Unknown'))
            formatted_date = 'Unknown'
            if date and date != 'Unknown':
                try:
                    from datetime import datetime
                    if 'T' in str(date):
                        parsed_date = datetime.fromisoformat(str(date).replace('Z', '+00:00'))
                        formatted_date = parsed_date.strftime('%b %d')
                    elif len(str(date)) >= 10:
                        parsed_date = datetime.strptime(str(date)[:10], '%Y-%m-%d')
                        formatted_date = parsed_date.strftime('%b %d')
                    else:
                        formatted_date = str(date)[:10]
                except:
                    formatted_date = str(date)[:10] if len(str(date)) > 10 else str(date)
            
            # Get score
            score = "N/A"
            try:
                if isinstance(analysis.get('analysis_data'), dict):
                    score_val = analysis['analysis_data'].get('overall_score')
                    if score_val is not None:
                        score = int(score_val) if isinstance(score_val, (int, float)) else score_val
                elif analysis.get('overall_score') is not None:
                    score_val = analysis.get('overall_score')
                    score = int(score_val) if isinstance(score_val, (int, float)) else score_val
            except:
                score = "N/A"
            
            # File icon - using simple text to avoid emoji encoding issues
            file_icon = "DOC"
            if filename.lower().endswith('.pdf'):
                file_icon = "PDF"
            elif filename.lower().endswith(('.ppt', '.pptx')):
                file_icon = "PPT"
            elif filename.lower().endswith(('.doc', '.docx')):
                file_icon = "📝"
            
            st.sidebar.markdown(f"""
            <div class="analysis-item">
                <div class="analysis-header">
                    <div class="analysis-icon">{file_icon}</div>
                    <div class="analysis-filename">{filename}</div>
                </div>
                <div class="analysis-meta">
                    <div class="analysis-date">{formatted_date}</div>
                    <div class="analysis-score">{score}%</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.sidebar.markdown("""
        <div class="empty-state">
            <div class="empty-icon">📭</div>
            <div>No analyses yet</div>
            <div style="font-size: 11px; margin-top: 4px;">Upload a pitch deck to get started</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Close the recent-analyses and sidebar-section divs
    st.sidebar.markdown("""
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Close the main sidebar-content div
    st.sidebar.markdown("""
    </div>
    """, unsafe_allow_html=True)
    
    # Signout button at bottom
    st.sidebar.markdown("""
    <div class="sidebar-signout">
        <a href="?logout=1" target="_self" class="signout-btn">
            <span>🚪</span>
            <span>Sign Out</span>
        </a>
    </div>
    """, unsafe_allow_html=True)