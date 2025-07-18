import streamlit as st
from typing import Dict, Any
from dataclasses import dataclass

@dataclass
class FileConfig:
    """File processing configuration."""
    MAX_FILE_SIZE: int = 50 * 1024 * 1024  # 50MB
    MIN_FILE_SIZE: int = 100  # 100 bytes
    ALLOWED_EXTENSIONS: list = None
    ALLOWED_MIME_TYPES: Dict[str, list] = None
    
    def __post_init__(self):
        if self.ALLOWED_EXTENSIONS is None:
            self.ALLOWED_EXTENSIONS = ['.pdf', '.docx', '.pptx', '.txt']
        
        if self.ALLOWED_MIME_TYPES is None:
            self.ALLOWED_MIME_TYPES = {
                '.pdf': ['application/pdf'],
                '.docx': ['application/vnd.openxmlformats-officedocument.wordprocessingml.document'],
                '.pptx': ['application/vnd.openxmlformats-officedocument.presentationml.presentation'],
                '.txt': ['text/plain', 'text/x-python', 'application/octet-stream']
            }

@dataclass
class UIConfig:
    """UI configuration."""
    APP_TITLE: str = "Pitch Analyzer"
    APP_LAYOUT: str = "wide"
    THEME_PRIMARY_COLOR: str = "#3b82f6"
    THEME_SECONDARY_COLOR: str = "#10b981"
    THEME_ACCENT_COLOR: str = "#f59e0b"
    THEME_ERROR_COLOR: str = "#ef4444"
    MAX_TEXT_PREVIEW: int = 2000
    MAX_HISTORY_ITEMS: int = 10

@dataclass
class CacheConfig:
    """Caching configuration."""
    TEXT_EXTRACTION_TTL: int = 3600  # 1 hour
    TEXT_EXTRACTION_MAX_ENTRIES: int = 50
    NLP_ANALYSIS_TTL: int = 3600  # 1 hour
    NLP_ANALYSIS_MAX_ENTRIES: int = 100
    USER_ANALYSES_TTL: int = 1800  # 30 minutes
    USER_ANALYSES_MAX_ENTRIES: int = 20

@dataclass
class SecurityConfig:
    """Security configuration."""
    SESSION_TIMEOUT_HOURS: int = 24
    MAX_LOGIN_ATTEMPTS: int = 5
    PASSWORD_MIN_LENGTH: int = 8
    ENABLE_EMAIL_VERIFICATION: bool = True

@dataclass
class AnalysisConfig:
    """Analysis configuration."""
    MIN_TEXT_LENGTH: int = 50
    MAX_TEXT_LENGTH: int = 1000000  # 1M characters
    READABILITY_THRESHOLD: int = 60
    SENTIMENT_THRESHOLD: float = 0.1
    MAX_KEYWORDS: int = 15
    SECTION_CRITERIA: list = None
    
    def __post_init__(self):
        if self.SECTION_CRITERIA is None:
            self.SECTION_CRITERIA = [
                {
                    'name': 'The Problem',
                    'keywords': ['problem', 'challenge', 'pain point', 'unmet need'],
                    'tip': 'Clearly state the problem or unmet need your startup addresses.'
                },
                {
                    'name': 'The Solution',
                    'keywords': ['solution', 'product', 'platform', 'our technology', 'we solve'],
                    'tip': 'Describe your solution and how it addresses the problem.'
                },
                {
                    'name': 'Market Size (TAM/SAM/SOM)',
                    'keywords': ['market size', 'tam', 'sam', 'som', 'billion', 'million', 'industry'],
                    'tip': 'Quantify the market opportunity (TAM/SAM/SOM).'
                },
                {
                    'name': 'Product/Demo',
                    'keywords': ['how it works', 'demo', 'product features', 'technology'],
                    'tip': 'Showcase your product, demo, or technology.'
                },
                {
                    'name': 'Traction & Metrics',
                    'keywords': ['traction', 'users', 'revenue', 'growth', 'mrr', 'arr', 'kpi', 'metrics'],
                    'tip': 'Highlight traction, growth, and key metrics.'
                },
                {
                    'name': 'Business Model',
                    'keywords': ['business model', 'monetization', 'pricing', 'how we make money'],
                    'tip': 'Explain how your startup makes money.'
                },
                {
                    'name': 'Competitive Landscape',
                    'keywords': ['competitors', 'competition', 'unique advantage', 'moat', 'differentiator'],
                    'tip': 'Describe your competitors and your unique advantage.'
                },
                {
                    'name': 'The Team',
                    'keywords': ['team', 'founders', 'ceo', 'cto', 'advisors', 'experience'],
                    'tip': 'Introduce your core team and their expertise.'
                },
                {
                    'name': 'The Ask & Use of Funds',
                    'keywords': ['ask', 'seeking', 'raising', 'investment', 'use of funds'],
                    'tip': 'State your funding ask and how you will use the funds.'
                }
            ]

class AppConfig:
    """Main application configuration."""
    
    def __init__(self):
        self.file = FileConfig()
        self.ui = UIConfig()
        self.cache = CacheConfig()
        self.security = SecurityConfig()
        self.analysis = AnalysisConfig()
        self.debug_mode = self._get_debug_mode()
    
    def _get_debug_mode(self) -> bool:
        """Get debug mode from secrets or environment."""
        try:
            return st.secrets.get("debug_mode", False)
        except:
            return False
    
    def get_supabase_config(self) -> Dict[str, str]:
        """Get Supabase configuration."""
        try:
            return {
                "url": st.secrets["supabase"]["url"],
                "key": st.secrets["supabase"]["key"]
            }
        except Exception as e:
            raise ValueError(f"Supabase configuration not found: {e}")
    
    def validate_config(self) -> bool:
        """Validate configuration values."""
        try:
            # Validate file config
            assert self.file.MAX_FILE_SIZE > self.file.MIN_FILE_SIZE
            assert len(self.file.ALLOWED_EXTENSIONS) > 0
            
            # Validate UI config
            assert len(self.ui.APP_TITLE) > 0
            assert self.ui.MAX_TEXT_PREVIEW > 0
            
            # Validate cache config
            assert self.cache.TEXT_EXTRACTION_TTL > 0
            assert self.cache.NLP_ANALYSIS_TTL > 0
            
            # Validate security config
            assert self.security.SESSION_TIMEOUT_HOURS > 0
            assert self.security.PASSWORD_MIN_LENGTH >= 6
            
            # Validate analysis config
            assert self.analysis.MIN_TEXT_LENGTH > 0
            assert self.analysis.MAX_TEXT_LENGTH > self.analysis.MIN_TEXT_LENGTH
            assert len(self.analysis.SECTION_CRITERIA) > 0
            
            return True
        except AssertionError as e:
            raise ValueError(f"Invalid configuration: {e}")

# Global configuration instance
config = AppConfig()

# Validate configuration on import
try:
    config.validate_config()
except ValueError as e:
    st.error(f"Configuration Error: {e}")
    st.stop()