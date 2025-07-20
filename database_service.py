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
            return False
            
        try:
            # Convert complex data types to JSON-compatible strings
            import json
            
            # Format the date properly
            current_date = datetime.now()
            formatted_date = current_date.strftime("%Y-%m-%d %H:%M:%S")
            
            # Prepare data for insertion - only include columns that exist in the database
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
                'keywords': json.dumps(analysis_data.get('keywords', []))
                # Removed 'section_scores' and 'advanced_results' as they don't exist in the database schema
            }
            
            # Insert data into Supabase - handle potential schema issues
            try:
                # First try with all fields
                result = self.sb.table('analyses').insert(data_to_insert).execute()
                
                if result.data:
                    return True
                else:
                    return False
            except Exception as schema_error:
                # If there's a schema error, try with only essential fields
                essential_data = {
                    'user_id': user_id,
                    'filename': analysis_data.get('filename', ''),
                    'date': formatted_date,
                    'score': analysis_data.get('score', 0),
                    'rility': analysis_data.get('readability', 0)
                }
                
                try:
                    result = self.sb.table('analyses').insert(essential_data).execute()
                    if result.data:
                        return True
                    else:
                        st.warning("Analysis completed but couldn't save to history: No data returned.")
                        return False
                except Exception as e:
                    # Log the error but don't show it to the user
                    import logging
                    logging.warning(f"Database save error: {str(e)}")
                    return False
                
        except Exception as e:
            # Log the error but don't show it to the user
            import logging
            logging.warning(f"Database save error: {str(e)}")
            return False
    
    @handle_database_errors
    def get_user_analyses(self, user_id: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Get user's past analyses."""
        if not user_id:
            return []
            
        try:
            # Use the cached version if available
            from performance_optimizer import get_user_analyses_cached
            result = get_user_analyses_cached(user_id, self.sb)
            # Ensure we always return a list, even if the result is None
            return result if result is not None else []
        except ImportError:
            # Fallback to direct query if optimizer not available
            try:
                result = self.sb.table('analyses').select('*').eq('user_id', user_id).order('date', desc=True).limit(limit).execute()
                return result.data if result.data else []
            except Exception:
                return []
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