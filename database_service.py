import streamlit as st
from supabase import Client
from datetime import datetime
from typing import List, Dict, Optional, Any
from error_handler import handle_database_errors

class DatabaseService:
    """Handle all database operations with Supabase."""
    
    def __init__(self, supabase_client: Client):
        self.sb = supabase_client
    
    @handle_database_errors
    def save_analysis(self, user_id: str, analysis_data: Dict[str, Any]) -> bool:
        """Save pitch analysis to database with improved error handling."""
        if not user_id:
            st.warning("Analysis completed but couldn't save to history: User not logged in.")
            return False
            
        try:
            # Convert complex data types to JSON-compatible strings
            import json
            
            # Format the date properly
            current_date = datetime.now()
            formatted_date = current_date.strftime("%Y-%m-%d %H:%M:%S")
            
            # Prepare data for insertion
            data_to_insert = {
                'user_id': user_id,
                'filename': analysis_data.get('filename', ''),
                'date': formatted_date,
                'summary': analysis_data.get('summary', ''),
                'score': analysis_data.get('score', 0),
                'readability': analysis_data.get('readability', 0),
                'sentiment': json.dumps(analysis_data.get('sentiment', {})),
                'strengths': json.dumps(analysis_data.get('strengths', [])),
                'weaknesses': json.dumps(analysis_data.get('weaknesses', [])),
                'tips': json.dumps(analysis_data.get('tips', [])),
                'keywords': json.dumps(analysis_data.get('keywords', [])),
                'section_scores': json.dumps(analysis_data.get('section_scores', {})),
                'advanced_results': json.dumps(analysis_data.get('advanced_results', {}))
            }
            
            # Insert data into Supabase
            result = self.sb.table('analyses').insert(data_to_insert).execute()
            
            if result.data:
                return True
            else:
                st.warning("Analysis completed but couldn't save to history: No data returned.")
                return False
                
        except Exception as e:
            st.warning(f"Analysis completed but couldn't save to history: {str(e)}")
            return False
    
    @handle_database_errors
    def get_user_analyses(self, user_id: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Get user's past analyses."""
        try:
            result = self.sb.table('analyses').select('*').eq('user_id', user_id).order('date', desc=True).limit(limit).execute()
            return result.data if result.data else []
        except Exception:
            return []
    
    @handle_database_errors
    def delete_analysis(self, user_id: str, analysis_id: str) -> bool:
        """Delete a specific analysis."""
        try:
            result = self.sb.table('analyses').delete().eq('user_id', user_id).eq('id', analysis_id).execute()
            return True
        except Exception:
            return False
    
    @handle_database_errors
    def get_user_stats(self, user_id: str) -> Dict[str, Any]:
        """Get user statistics."""
        try:
            analyses = self.get_user_analyses(user_id, limit=100)
            if not analyses:
                return {'total_analyses': 0, 'avg_score': 0, 'best_score': 0}
            
            scores = [float(a.get('score', 0)) for a in analyses]
            return {
                'total_analyses': len(analyses),
                'avg_score': round(sum(scores) / len(scores), 1) if scores else 0,
                'best_score': max(scores) if scores else 0,
                'recent_analyses': analyses[:5]
            }
        except Exception:
            return {'total_analyses': 0, 'avg_score': 0, 'best_score': 0}