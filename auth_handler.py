import streamlit as st
from supabase import Client
from datetime import datetime, timedelta
import hashlib
import secrets
from error_handler import handle_auth_errors, error_handler

class AuthHandler:
    def __init__(self, supabase_client: Client):
        self.sb = supabase_client
        
    def _generate_session_token(self) -> str:
        """Generate a secure session token."""
        return secrets.token_urlsafe(32)
    
    def _hash_session_token(self, token: str) -> str:
        """Hash session token for storage."""
        return hashlib.sha256(token.encode()).hexdigest()
    
    def validate_session(self) -> bool:
        """Validate current session with persistence across page refreshes."""
        # First check if we have a valid Supabase session
        try:
            user_response = self.sb.auth.get_user()
            if user_response and user_response.user:
                # Update session state with current user info
                st.session_state.user = user_response.user
                st.session_state.session_token = self._generate_session_token()
                st.session_state.session_expires = datetime.now() + timedelta(hours=24)
                
                # Store session info in browser storage for persistence
                self._store_session_in_browser(user_response.user)
                return True
        except Exception:
            pass
        
        # Check browser storage for session persistence
        if self._restore_session_from_browser():
            return True
        
        # Fallback to session state check
        if 'user' not in st.session_state or st.session_state.user is None:
            return False
            
        # Check session expiration if it exists
        if 'session_expires' in st.session_state:
            if datetime.now() > st.session_state.session_expires:
                self.logout()
                return False
                
        return True
    
    def _store_session_in_browser(self, user):
        """Store session info in browser localStorage for persistence."""
        try:
            # Instead of trying to use localStorage directly, we'll use Streamlit's session state
            # and rely on the user to stay on the same browser tab
            
            # Store user info in session state
            st.session_state.user = user
            st.session_state.session_expires = datetime.now() + timedelta(hours=24)
            
            # For a more robust solution, you could use cookies with streamlit-cookies-manager
            # but that would require additional setup
        except Exception as e:
            print(f"Error storing session: {e}")
            pass  # Ignore storage errors
    
    def _restore_session_from_browser(self) -> bool:
        """Check if we have a valid session in Streamlit's session state."""
        try:
            # Check if we have a user in session state
            if 'user' in st.session_state and st.session_state.user:
                # Check if session is expired
                if 'session_expires' in st.session_state:
                    if datetime.now() > st.session_state.session_expires:
                        # Session expired, clear it
                        self.logout()
                        return False
                return True
            
            return False
        except Exception as e:
            print(f"Error restoring session: {e}")
            return False
    
    @handle_auth_errors
    def login(self, email: str, password: str) -> tuple[bool, str]:
        """Authenticate user and create session."""
        res = self.sb.auth.sign_in_with_password({
            "email": email, 
            "password": password
        })
        
        if res.user:
            # Create secure session
            session_token = self._generate_session_token()
            session_expires = datetime.now() + timedelta(hours=24)
            
            # Store in session state
            st.session_state.user = res.user
            st.session_state.session_token = session_token
            st.session_state.session_expires = session_expires
            
            return True, "Login successful"
        else:
            error_msg = getattr(res, 'error', None)
            if error_msg and 'message' in error_msg:
                return False, f"Login failed: {error_msg['message']}"
            else:
                return False, "Login failed. Please check your credentials."
    
    @handle_auth_errors
    def signup(self, name: str, email: str, password: str) -> tuple[bool, str]:
        """Register new user."""
        res = self.sb.auth.sign_up({
            "email": email, 
            "password": password, 
            "options": {"data": {"name": name}}
        })
        
        if res.user:
            # Check if user is confirmed
            confirmed = getattr(res.user, 'confirmed_at', None) or getattr(res.user, 'confirmed', None)
            
            if confirmed:
                # Auto-login after signup
                session_token = self._generate_session_token()
                session_expires = datetime.now() + timedelta(hours=24)
                
                st.session_state.user = res.user
                st.session_state.session_token = session_token
                st.session_state.session_expires = session_expires
                
                return True, "Account created and logged in successfully!"
            else:
                return True, "Account created! Please check your email for verification."
        else:
            error_msg = getattr(res, 'error', None)
            if error_msg and 'message' in error_msg:
                return False, f"Sign up failed: {error_msg['message']}"
            else:
                return False, "Sign up failed. Try a different email."
    
    def logout(self):
        """Logout user and clear session."""
        try:
            self.sb.auth.sign_out()
        except:
            pass  # Continue even if server logout fails
            
        # Clear all session data
        keys_to_clear = ['user', 'session_token', 'session_expires']
        for key in keys_to_clear:
            if key in st.session_state:
                del st.session_state[key]
    
    def get_current_user(self):
        """Get current authenticated user."""
        if self.validate_session():
            return st.session_state.user
        return None
    
    def require_auth(self):
        """Decorator-like function to require authentication."""
        if not self.validate_session():
            return False
        return True