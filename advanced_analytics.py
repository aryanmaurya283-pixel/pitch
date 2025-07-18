import re
import numpy as np
from typing import Dict, List, Tuple, Any
from collections import Counter
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import textstat
from config import config

class AdvancedPitchAnalyzer:
    """Advanced AI-powered pitch deck analyzer with comprehensive insights."""
    
    def __init__(self):
        try:
            self.stop_words = set(stopwords.words('english'))
        except:
            self.stop_words = set()
        self.setup_analysis_patterns()
    
    def setup_analysis_patterns(self):
        """Setup regex patterns for advanced analysis."""
        self.financial_patterns = {
            'revenue': [
                r'\$[\d,]+(?:\.\d+)?[kmb]?\s*(?:revenue|sales|income|earnings)',
                r'(?:revenue|sales|income|earnings).*?\$[\d,]+(?:\.\d+)?[kmb]?',
                r'[\d,]+(?:\.\d+)?\s*(?:million|billion|k)\s*(?:revenue|sales|income)'
            ],
            'users': [
                r'[\d,]+(?:\.\d+)?[kmb]?\s*(?:users|customers|subscribers|clients)',
                r'(?:users|customers|subscribers|clients).*?[\d,]+(?:\.\d+)?[kmb]?'
            ],
            'growth': [
                r'[\d,]+(?:\.\d+)?%\s*(?:growth|increase|yoy|mom)',
                r'(?:growth|increase|grew|increased).*?[\d,]+(?:\.\d+)?%'
            ],
            'funding': [
                r'\$[\d,]+(?:\.\d+)?[kmb]?\s*(?:funding|investment|raised|round)',
                r'(?:raised|funding|investment|round).*?\$[\d,]+(?:\.\d+)?[kmb]?'
            ]
        }
    
    def extract_financial_metrics(self, text: str) -> Dict[str, List[str]]:
        """Extract financial metrics with improved accuracy."""
        metrics = {key: [] for key in self.financial_patterns.keys()}
        
        for category, patterns in self.financial_patterns.items():
            for pattern in patterns:
                matches = re.findall(pattern, text, re.IGNORECASE)
                metrics[category].extend([match.strip() for match in matches])
        
        # Clean and deduplicate
        for category in metrics:
            metrics[category] = list(set(metrics[category]))[:3]
        
        return metrics
    
    def calculate_pitch_quality_score(self, text: str) -> Dict[str, Any]:
        """Calculate comprehensive pitch quality score."""
        # Get basic analysis
        from nlp_utils import analyze_sections, readability_score, sentiment_scores
        
        try:
            section_score, strengths, weaknesses, tips, section_scores = analyze_sections(text)
            readability = readability_score(text)
            sentiment = sentiment_scores(text)
        except:
            # Fallback values
            section_score = 5.0
            strengths = []
            weaknesses = []
            tips = []
            section_scores = {}
            readability = 50.0
            sentiment = {'compound': 0.0}
        
        # Get advanced analysis
        financial = self.extract_financial_metrics(text)
        
        # Calculate scores
        scores = {
            'section_coverage': (section_score / 10) * 100,
            'readability': max(0, min(100, readability)),
            'sentiment': (sentiment.get('compound', 0) + 1) * 50,
            'financial_metrics': 50 if any(financial.values()) else 20
        }
        
        # Calculate overall score
        overall_score = np.mean(list(scores.values()))
        
        # Generate letter grade
        if overall_score >= 90:
            grade = "A+"
        elif overall_score >= 85:
            grade = "A"
        elif overall_score >= 80:
            grade = "A-"
        elif overall_score >= 75:
            grade = "B+"
        elif overall_score >= 70:
            grade = "B"
        elif overall_score >= 65:
            grade = "B-"
        elif overall_score >= 60:
            grade = "C+"
        elif overall_score >= 55:
            grade = "C"
        elif overall_score >= 50:
            grade = "C-"
        else:
            grade = "D"
        
        return {
            'overall_score': round(overall_score, 1),
            'grade': grade,
            'individual_scores': scores,
            'financial_metrics': financial,
            'recommendations': self.generate_recommendations(scores, financial)
        }
    
    def generate_recommendations(self, scores: Dict, financial: Dict) -> List[str]:
        """Generate personalized recommendations."""
        recommendations = []
        
        if scores['section_coverage'] < 70:
            recommendations.append("📋 Include all essential pitch sections")
        
        if not any(financial.values()):
            recommendations.append("💰 Add key financial metrics and traction data")
        
        if scores['readability'] < 60:
            recommendations.append("📝 Simplify language for better readability")
        
        if scores['sentiment'] < 60:
            recommendations.append("✨ Use more positive, confident language")
        
        return recommendations[:5]

# Global instance
advanced_analyzer = AdvancedPitchAnalyzer()