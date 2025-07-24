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
        # Try multiple approaches to save the analysis
        approaches = [
            # Approach 1: Simple structure with just essential fields
            {
                "user_id": user_id,
                "filename": analysis_data.get("filename", "Unknown"),
                "score": analysis_data.get("overall_score", 0),
                "date": datetime.now().isoformat()
            },
            # Approach 2: With analysis_data JSON column
            {
                "user_id": user_id,
                "filename": analysis_data.get("filename", "Unknown"),
                "analysis_data": json.dumps(analysis_data),
                "created_at": datetime.now().isoformat()
            },
            # Approach 3: Individual columns
            {
                "user_id": user_id,
                "filename": analysis_data.get("filename", "Unknown"),
                "score": analysis_data.get("score", 0),
                "readability_score": analysis_data.get("readability_score", 0),
                "sentiment": analysis_data.get("sentiment", "neutral"),
                "grade": analysis_data.get("grade", "N/A"),
                "overall_score": analysis_data.get("overall_score", 0),
                "strengths": json.dumps(analysis_data.get("strengths", [])),
                "weaknesses": json.dumps(analysis_data.get("weaknesses", [])),
                "tips": json.dumps(analysis_data.get("tips", [])),
                "keywords": json.dumps(analysis_data.get("keywords", [])),
                "created_at": datetime.now().isoformat()
            }
        ]
        
        for i, data in enumerate(approaches):
            try:
                res = self.sb.table("analyses").insert(data).execute()
                if res.data and len(res.data) > 0:
                    print(f"Analysis saved successfully using approach {i+1}")
                    return True
            except Exception as e:
                print(f"Approach {i+1} failed: {e}")
                continue
        
        print("All save approaches failed")
        return False

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