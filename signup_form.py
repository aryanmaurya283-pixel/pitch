import streamlit as st

def render_figma_signup_form():
    """Render signup form based on new Figma design."""
    # Set page config
    st.markdown("""
    <style>
    .main .block-container {
        padding: 2rem;
        max-width: 800px;
        margin: 0 auto;
    }
    
    .stApp {
        background-color: #0A0A0A;
    }
    
    .stTextInput > div > div > input {
        background-color: #1A1A1A !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
    }
    
    .stButton > button {
        background-color: #4A90E2 !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
    }
    
    /* Hide Streamlit elements */
    #MainMenu, footer, header, .stDeployButton {
        visibility: hidden !important;
        height: 0 !important;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Center everything
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        # Logo and title
        st.markdown("""
        <div style="display: flex; justify-content: center; margin-bottom: 20px;">
            <div style="width: 64px; height: 64px; background: #4A90E2; border-radius: 8px; display: flex; align-items: center; justify-content: center;">
                <span style="color: white; font-size: 32px;">🚀</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        st.title("PitchPerfect AI")
        st.caption("AI-powered pitch deck analysis")
        
        # Form fields
        st.subheader("Sign Up")
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
            
        # Theme toggle button
        col1, col2, col3 = st.columns([3, 2, 3])
        with col2:
            if st.button("🌙 Light Theme", key="theme_toggle_btn", use_container_width=True):
                # Toggle theme
                if 'dark_mode' in st.session_state:
                    st.session_state.dark_mode = not st.session_state.dark_mode
                else:
                    st.session_state.dark_mode = False
                st.rerun()