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
        flex-direction: column;
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
        margin-bottom: 20px;
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
    
    .form-container {
        background: #3A3A3A;
        border-radius: 16px;
        padding: 32px;
        width: 100%;
        max-width: 400px;
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
    </div>
    """, unsafe_allow_html=True)