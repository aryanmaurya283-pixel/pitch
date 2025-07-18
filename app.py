
# PitchPerfect - AI-Powered Pitch Deck Analyzer
import streamlit as st
import os
import tempfile
from text_extractor import extract_text
from nlp_utils import analyze_sections, readability_score, sentiment_scores, extract_keywords
from file_validator import validate_file_upload
from auth_handler import AuthHandler
from figma_ui_fixed import (
    render_figma_main_content, render_figma_analysis_results,
    render_figma_loading, render_figma_success
)
from login_form import render_figma_login_form
from signup_form import render_figma_signup_form
from database_service import DatabaseService
from advanced_analytics import advanced_analyzer
from supabase import create_client, Client
from datetime import datetime
from config import config

# --- Page Configuration ---
st.set_page_config(
    page_title="PitchPerfect - AI Pitch Analyzer", 
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- Load Supabase client ---
supabase_config = config.get_supabase_config()
sb: Client = create_client(supabase_config["url"], supabase_config["key"])

# --- Initialize Services ---
auth = AuthHandler(sb)
db_service = DatabaseService(sb)

# --- Initialize Theme State ---
if 'dark_mode' not in st.session_state:
    st.session_state.dark_mode = False

# --- Auth State ---
if 'auth_mode' not in st.session_state:
    st.session_state.auth_mode = 'login'

# --- Figma-based Auth Forms ---
def login_form():
    # Store auth handler in session state
    st.session_state.auth_handler = auth
    
    # Render Figma login form
    render_figma_login_form()

def signup_form():
    # Store auth handler in session state
    st.session_state.auth_handler = auth
    
    # Render Figma signup form
    render_figma_signup_form()

# --- Main App Flow ---
if not auth.require_auth():
    if st.session_state.auth_mode == 'login':
        login_form()
    else:
        signup_form()
    st.stop()

# --- Get Current User ---
current_user = auth.get_current_user()
st.session_state.current_user = current_user

# --- Get User Data ---
user_id = current_user.id if current_user else None
analyses = db_service.get_user_analyses(user_id) if user_id else []

# --- Render Sidebar ---
# Import and render sidebar directly here to avoid import errors
from sidebar import render_figma_sidebar
render_figma_sidebar(current_user, analyses)

# --- Handle Logout ---
# This is now handled directly in the sidebar.py file

# --- File Upload Section ---
uploaded_file = st.file_uploader("", type=["pdf", "pptx", "docx", "txt"], label_visibility="collapsed")

if uploaded_file:
    # Validate uploaded file
    is_valid, error_msg, safe_filename = validate_file_upload(uploaded_file)
    
    if not is_valid:
        st.error(f"❌ File validation failed: {error_msg}")
        st.stop()
    
    if error_msg and "Warning" in error_msg:
        st.warning(error_msg)
    
    # File info in EXACT Figma style
    filetype = os.path.splitext(safe_filename)[1].lower()
    filesize = uploaded_file.size / 1024
    
    st.markdown(f"""
    <div style='background: #FFFFFF; border-radius: 12px; padding: 1.5rem; margin: 1rem 0; border: 1px solid #E2E8F0; box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);'>
        <div style='display: flex; align-items: center; gap: 1rem;'>
            <div style='font-size: 2rem; color: #6366F1;'>📄</div>
            <div>
                <div style='font-weight: 600; color: #1E293B; font-size: 1rem;'>{safe_filename}</div>
                <div style='color: #64748B; font-size: 0.875rem;'>{filetype.upper()} • {filesize:.1f} KB</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Extract text from file
    with tempfile.NamedTemporaryFile(delete=False, suffix=filetype) as tmp_file:
        tmp_file.write(uploaded_file.read())
        tmp_path = tmp_file.name
    
    text = extract_text(tmp_path, filetype)
    os.unlink(tmp_path)
    
    if not text:
        st.error("❌ Could not extract text from the uploaded file.")
    else:
        # Figma loading animation
        loading_placeholder = st.empty()
        with loading_placeholder.container():
            render_figma_loading()
        
        # Basic analysis
        score, strengths, weaknesses, tips, section_scores = analyze_sections(text)
        read_score = readability_score(text)
        sentiment = sentiment_scores(text)
        keywords = extract_keywords(text)
        
        # Advanced analysis
        advanced_results = advanced_analyzer.calculate_pitch_quality_score(text)
        grade = advanced_results.get('grade', 'B+')
        
        # Clear loading animation
        loading_placeholder.empty()
        
        # Show text preview
        with st.expander("📄 View Extracted Text", expanded=False):
            st.code(text[:2000] + ("..." if len(text) > 2000 else ""), language=None)
        
        # Render new analysis results
        render_figma_analysis_results(
            score, read_score, sentiment, grade, 
            advanced_results.get('overall_score', 75),
            strengths, weaknesses, tips, keywords,
            advanced_results.get('recommendations', [])
        )
        
        # AI Recommendations - EXACT Figma Style
        recommendations = advanced_results.get('recommendations', [])
        if recommendations:
            st.markdown("""
            <div style='background: #FFFFFF; border-radius: 16px; padding: 2rem; margin: 2rem 0; border: 1px solid #E2E8F0; box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);'>
                <div style='font-size: 1.5rem; font-weight: 700; color: #1E293B; margin-bottom: 1.5rem; display: flex; align-items: center; gap: 0.75rem;'>
                    🤖 AI Recommendations
                </div>
            """, unsafe_allow_html=True)
            
            for i, rec in enumerate(recommendations, 1):
                st.markdown(f"""
                <div style='background: #F8FAFC; border-left: 4px solid #6366F1; padding: 1rem; margin: 0.75rem 0; border-radius: 0 8px 8px 0; border: 1px solid #E2E8F0;'>
                    <strong style='color: #1E293B;'>{i}.</strong> <span style='color: #475569;'>{rec}</span>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown("</div>", unsafe_allow_html=True)
        
        # Download button
        summary = f"PitchPerfect Analysis for {safe_filename}\n\nOverall Grade: {grade} ({advanced_results.get('overall_score', 75)}/100)\nSection Coverage: {score}/10\nReadability: {read_score:.1f}\nSentiment: {sentiment}\n\nStrengths: {', '.join(strengths)}\nWeaknesses: {', '.join(weaknesses)}\nRecommendations: {', '.join(recommendations)}\nKeywords: {', '.join(keywords)}\n"
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.download_button(
                "📥 Download Full Analysis", 
                summary, 
                file_name=f"{safe_filename}_analysis.txt", 
                use_container_width=True,
                type="primary"
            )
        
        # Save to database using the database service
        analysis_data = {
            'filename': safe_filename,
            'summary': summary,
            'score': score,
            'readability': read_score,
            'sentiment': sentiment,
            'strengths': strengths,
            'weaknesses': weaknesses,
            'tips': tips,
            'keywords': keywords,
            'section_scores': section_scores,
            'advanced_results': advanced_results
        }
        
        if db_service.save_analysis(user_id, analysis_data):
            render_figma_success("Analysis Complete!", "Your pitch deck has been analyzed and saved to your history!")
        

else:
    # Show main content area when no file is uploaded
    render_figma_main_content()
