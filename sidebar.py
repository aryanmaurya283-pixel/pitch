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

def render_figma_sidebar(current_user=None):
    st.sidebar.markdown("""
    <style>
    [data-testid="stSidebar"] {
        margin-top: 70px !important;
        padding-top: 24px !important;
        height: 100vh;
        display: block;
    }
    .sidebar-premium-btn {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 12px;
        background: linear-gradient(90deg, #6366F1 0%, #4F46E5 100%);
        color: #fff !important;
        padding: 16px 0;
        border-radius: 10px;
        font-weight: 700;
        font-size: 18px;
        margin: 24px 24px 0 24px;
        text-decoration: none !important;
        box-shadow: 0 4px 16px rgba(79,70,229,0.10);
        transition: background 0.2s, transform 0.2s;
        border: none;
        width: calc(100% - 48px);
    }
    .sidebar-premium-btn.logout {
        background: linear-gradient(90deg,#EF4444 0%,#DC2626 100%);
    }
    .sidebar-premium-btn.logout:hover {
        background: linear-gradient(90deg,#F87171 0%,#EF4444 100%);
    }
    </style>
    """, unsafe_allow_html=True)
    st.sidebar.markdown('<a href="?action=logout" target="_self" class="sidebar-premium-btn logout">🚪 Sign Out</a>', unsafe_allow_html=True)