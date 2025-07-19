import streamlit as st
import traceback
import logging
from typing import Optional, Callable, Any
from functools import wraps
from datetime import datetime

class ErrorHandler:
    """Centralized error handling for the application."""
    
    def __init__(self):
        self.setup_logging()
    
    def setup_logging(self):
        """Setup logging configuration."""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('app.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def handle_error(self, error: Exception, context: str = "", user_message: str = None):
        """Handle errors with logging and user feedback."""
        error_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Log the error
        self.logger.error(f"Error {error_id} in {context}: {str(error)}")
        self.logger.error(f"Traceback: {traceback.format_exc()}")
        
        # Show user-friendly message
        if user_message:
            st.error(f"❌ {user_message}")
        else:
            st.error(f"❌ Something went wrong. Error ID: {error_id}")
        
        # In development, show more details
        if st.secrets.get("debug_mode", False):
            with st.expander("🔍 Debug Information"):
                st.code(f"Error: {str(error)}\n\nTraceback:\n{traceback.format_exc()}")
    
    def safe_execute(self, func: Callable, *args, context: str = "", user_message: str = None, **kwargs) -> Optional[Any]:
        """Safely execute a function with error handling."""
        try:
            return func(*args, **kwargs)
        except Exception as e:
            self.handle_error(e, context, user_message)
            return None
    
    def error_boundary(self, context: str = "", user_message: str = None):
        """Decorator for error boundary around functions."""
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    self.handle_error(e, context or func.__name__, user_message)
                    return None
            return wrapper
        return decorator

# Global error handler instance
error_handler = ErrorHandler()

# Convenience decorators
def safe_operation(context: str = "", user_message: str = None):
    """Decorator for safe operations."""
    return error_handler.error_boundary(context, user_message)

def handle_file_processing_errors(func):
    """Specific decorator for file processing operations."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            error_handler.handle_error(
                e, 
                "File Processing", 
                "Failed to process the uploaded file. Please check the file format and try again."
            )
            return None
    return wrapper

def handle_database_errors(func):
    """Specific decorator for database operations."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
            # Ensure we always return a valid value, not None
            if func.__name__ == 'get_user_analyses' and result is None:
                return []
            return result
        except Exception as e:
            error_handler.handle_error(
                e, 
                "Database Operation", 
                "Database operation failed. Your analysis was completed but may not be saved to history."
            )
            # Return appropriate default values based on function name
            if func.__name__ == 'get_user_analyses':
                return []
            elif func.__name__ == 'save_analysis':
                return False
            return None
    return wrapper

def handle_auth_errors(func):
    """Specific decorator for authentication operations."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            error_handler.handle_error(
                e, 
                "Authentication", 
                "Authentication failed. Please check your credentials and try again."
            )
            return False, "Authentication error occurred."
    return wrapper

def handle_nlp_errors(func):
    """Specific decorator for NLP processing operations."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            error_handler.handle_error(
                e, 
                "NLP Analysis", 
                "Text analysis encountered an issue. Some features may be limited."
            )
            # Return default values for NLP analysis
            return {
                'score': 5,
                'strengths': ["Basic structure"],
                'weaknesses': ["Analysis incomplete"],
                'tips': ["Try again with a different text format"],
                'section_scores': {},
                'read_score': 50,
                'sentiment': {'compound': 0, 'neg': 0, 'neu': 1, 'pos': 0},
                'keywords': ["pitch", "analysis"]
            }
    return wrapper