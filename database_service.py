import streamlit as st
from supabase import Client
from datetime import datetime
from typing import List, Dict, Optional, Any
from error_handler import handle_database_errors
import json

class DatabaseService:
    """Handle all database operations with Supabase."""
    
    def __init__(self, supabase_client: Client):
        self.sb = supabase_client
    
    def save_analysis(self, user_id, analysis_data):
        """Save a user's analysis to the 'analyses' table."""
        data = {
            "user_id": user_id,
            "filename": analysis_data.get("filename"),
            "analysis_data": json.dumps(analysis_data),
            "date": datetime.now().isoformat()
        }
        res = self.sb.table("analyses").insert(data).execute()
        return res

    def get_user_analyses(self, user_id):
        """Fetch all analyses for a user from the 'analyses' table."""
        res = self.sb.table("analyses").select("*").eq("user_id", user_id).order("date", desc=True).execute()
        if hasattr(res, 'data'):
            # Parse analysis_data JSON for each record
            for row in res.data:
                if isinstance(row.get("analysis_data"), str):
                    try:
                        row["analysis_data"] = json.loads(row["analysis_data"])
                    except Exception:
                        pass
            return res.data
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