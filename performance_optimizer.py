import streamlit as st
import hashlib
from typing import List, Dict, Any, Optional
from supabase import Client
from nlp_utils import analyze_sections, readability_score, sentiment_scores, extract_keywords
from error_handler import handle_nlp_errors, handle_database_errors

class PerformanceOptimizer:
    """Optimize performance with caching and other techniques."""
    
    def __init__(self):
        pass
    
    @st.cache_data(ttl=3600)  # Cache for 1 hour
    def cached_nlp_analysis(self, text: str, text_hash: str):
        """Cache NLP analysis results."""
        score, strengths, weaknesses, tips, section_scores = analyze_sections(text)
        read_score = readability_score(text)
        sentiment = sentiment_scores(text)
        keywords = extract_keywords(text)
        
        return {
            'score': score,
            'strengths': strengths,
            'weaknesses': weaknesses,
            'tips': tips,
            'section_scores': section_scores,
            'read_score': read_score,
            'sentiment': sentiment,
            'keywords': keywords
        }
    
    @st.cache_data(ttl=300)  # Cache for 5 minutes
    def cached_user_analyses(self, user_id: str, _supabase_client: Client):
        """Cache user analyses with proper handling of unhashable types."""
        if not user_id:
            return []
            
        try:
            result = _supabase_client.table('analyses').select('*').eq('user_id', user_id).order('date', desc=True).limit(10).execute()
            
            # Process the data to ensure it's in the right format
            analyses = []
            for item in result.data:
                try:
                    import json
                    analysis = {
                        'id': item.get('id'),
                        'filename': item.get('filename', ''),
                        'date': item.get('date', ''),
                        'score': item.get('score', 0),
                        'readability': item.get('readability', 0),
                        'sentiment': json.loads(item.get('sentiment', '{}')) if isinstance(item.get('sentiment'), str) else item.get('sentiment', {}),
                        'strengths': json.loads(item.get('strengths', '[]')) if isinstance(item.get('strengths'), str) else item.get('strengths', []),
                        'weaknesses': json.loads(item.get('weaknesses', '[]')) if isinstance(item.get('weaknesses'), str) else item.get('weaknesses', []),
                        'tips': json.loads(item.get('tips', '[]')) if isinstance(item.get('tips'), str) else item.get('tips', []),
                        'keywords': json.loads(item.get('keywords', '[]')) if isinstance(item.get('keywords'), str) else item.get('keywords', [])
                    }
                    analyses.append(analysis)
                except Exception:
                    # Skip problematic items
                    continue
                    
            return analyses
        except Exception:
            return []

# Create a singleton instance
perf_optimizer = PerformanceOptimizer()

@handle_nlp_errors
def analyze_text_cached(text: str):
    """Analyze text with caching."""
    # Create a hash of the text to use as a cache key
    text_hash = hashlib.md5(text.encode()).hexdigest()
    return perf_optimizer.cached_nlp_analysis(text, text_hash)

@handle_database_errors
def get_user_analyses_cached(user_id: str, supabase_client: Client):
    """Get user analyses with caching."""
    return perf_optimizer.cached_user_analyses(user_id, supabase_client)