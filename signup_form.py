import streamlit as st

def render_figma_signup_form():
    """Render signup form based on new Figma design."""
    # Set page config
    dark_mode = st.session_state.get('dark_mode', False)
    
    # Dark theme colors
    if dark_mode:
        bg_color = "#121212"
        text_color = "#FFFFFF"
        input_bg = "#2A2A2A"
        input_border = "#444444"
        title_color = "#FFFFFF"
        caption_color = "#CCCCCC"
        label_color = "#E0E0E0"
        card_bg = "#1E1E1E"
        accent_color = "#4F7EFF"
        button_color = "#4F7EFF"
        button_hover = "#3B6EFF"
        error_color = "#FF5252"
        success_color = "#4CAF50"
    # Light theme colors - updated for better visibility
    else:
        bg_color = "#F5F7FA"  # Light background
        text_color = "#1A202C"  # Very dark text for high contrast
        input_bg = "#FFFFFF"
        input_border = "#CBD5E0"
        title_color = "#2C5282"  # Darker blue for titles
        caption_color = "#4A5568"
        label_color = "#2D3748"  # Dark label text
        card_bg = "#FFFFFF"
        accent_color = "#3182CE"  # Vibrant blue accent
        button_color = "#3182CE"
        button_hover = "#2B6CB0"
        error_color = "#E53E3E"
        success_color = "#38A169"
    
    st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    * {{
        font-family: 'Inter', sans-serif;
    }}
    
    .main .block-container {{
        padding: 2rem;
        max-width: 800px;
        margin: 0 auto;
    }}
    
    .stApp {{
        background-color: {bg_color};
        background-image: {'' if dark_mode else 'linear-gradient(120deg, #F5F7FA 0%, #EBF4FF 100%)'};
    }}
    
    /* Card styling for auth form */
    .auth-card {{
        background-color: {card_bg};
        border-radius: 16px;
        padding: 2rem;
        box-shadow: {'' if dark_mode else '0 10px 25px rgba(0, 0, 0, 0.05), 0 5px 10px rgba(0, 0, 0, 0.02)'};
        margin-top: 2rem;
        border: 1px solid {input_border};
    }}
    
    /* Text colors for all elements */
    .stMarkdown, .stMarkdown p, .stMarkdown span, h1, h2, h3, h4, h5, h6, .stSubheader, .stHeader {{
        color: {text_color} !important;
    }}
    
    /* Input labels */
    .stTextInput label, .stSelectbox label {{
        color: {label_color} !important;
        font-weight: 500 !important;
        font-size: 14px !important;
    }}
    
    /* Caption color */
    .stCaption {{
        color: {caption_color} !important;
    }}
    
    /* Input fields */
    .stTextInput > div > div > input {{
        background-color: {input_bg} !important;
        color: {text_color} !important;
        border: 2px solid {input_border} !important;
        border-radius: 8px !important;
        padding: 12px 16px !important;
        font-size: 15px !important;
        transition: all 0.2s ease !important;
        box-shadow: {'' if dark_mode else '0 2px 5px rgba(0, 0, 0, 0.05)'} !important;
    }}
    
    .stTextInput > div > div > input:focus {{
        border-color: {accent_color} !important;
        box-shadow: 0 0 0 2px {accent_color}30 !important;
    }}
    
    /* Buttons */
    .stButton > button {{
        background-color: {button_color} !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 12px 16px !important;
        font-weight: 600 !important;
        transition: all 0.2s ease !important;
        box-shadow: {'' if dark_mode else '0 4px 6px rgba(49, 130, 206, 0.15)'} !important;
    }}
    
    .stButton > button:hover {{
        background-color: {button_hover} !important;
        transform: translateY(-1px) !important;
        box-shadow: {'' if dark_mode else '0 6px 8px rgba(49, 130, 206, 0.2)'} !important;
    }}
    
    /* Error and success messages */
    .element-container .stAlert {{
        background-color: {error_color}20 !important;
        color: {error_color} !important;
        border: 1px solid {error_color} !important;
        border-radius: 8px !important;
        padding: 10px 16px !important;
    }}
    
    .element-container .stAlert.success {{
        background-color: {success_color}20 !important;
        color: {success_color} !important;
        border: 1px solid {success_color} !important;
    }}
    
    /* Hide Streamlit elements */
    #MainMenu, footer, header, .stDeployButton {{
        visibility: hidden !important;
        height: 0 !important;
    }}
    </style>
    """, unsafe_allow_html=True)
    
    # Center everything
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        # Logo and title
        st.markdown(f"""
        <div style="display: flex; justify-content: center; margin-bottom: 20px;">
            <div style="width: 64px; height: 64px; background: {accent_color}; border-radius: 12px; display: flex; align-items: center; justify-content: center; box-shadow: 0 8px 16px rgba(49, 130, 206, 0.2);">
                <span style="color: white; font-size: 32px;">🚀</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown(f"<h1 style='color: {title_color}; text-align: center; font-weight: 700; font-size: 32px; margin-bottom: 8px;'>PitchPerfect AI</h1>", unsafe_allow_html=True)
        st.markdown(f"<p style='color: {caption_color}; text-align: center; font-size: 16px; margin-bottom: 30px;'>AI-powered pitch deck analysis</p>", unsafe_allow_html=True)
                
        # Form fields
        st.markdown(f"<h3 style='color: {title_color}; font-weight: 700; font-size: 24px; margin-bottom: 20px;'>Sign Up</h3>", unsafe_allow_html=True)
        name = st.text_input("Full Name")
        email = st.text_input("Email Address")
        password = st.text_input("Password", type="password")
        
        # Sign Up button
        if st.button("Sign Up", use_container_width=True):
            if name and email and password:
                if len(password) < 6:
                    st.error("Password must be at least 6 characters long")
                else:
                    auth_handler = st.session_state.get('auth_handler')
                    if auth_handler:
                        with st.spinner("Creating your account..."):
                            success, message = auth_handler.signup(name, email, password)
                            if success:
                                st.success("Account created successfully!")
                                if "logged in" in message.lower():
                                    st.rerun()
                            else:
                                st.error(message)
                    else:
                        st.error("Authentication service not available")
            else:
                st.error("Please fill in all fields")
        
        # Switch to login
        if st.button("Already have an account? Sign In", use_container_width=True):
            st.session_state.auth_mode = 'login'
            st.rerun()
        
        # Close auth card container
        st.markdown("""
        </div>
        """, unsafe_allow_html=True)