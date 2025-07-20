import re
import string
import nltk
import numpy as np
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.sentiment import SentimentIntensityAnalyzer
import textstat
from typing import Dict, List, Tuple
from config import config

# Download required NLTK data
nltk.download('stopwords', quiet=True)
nltk.download('wordnet', quiet=True)
nltk.download('omw-1.4', quiet=True)
nltk.download('vader_lexicon', quiet=True)
nltk.download('punkt', quiet=True)
nltk.download('averaged_perceptron_tagger', quiet=True)

# --- Preprocessing ---
def preprocess_text(text):
    text = text.lower()
    text = re.sub(r"\s+", " ", text)
    text = text.translate(str.maketrans('', '', string.punctuation))
    stop_words = set(stopwords.words('english'))
    lemmatizer = WordNetLemmatizer()
    words = text.split()
    words = [lemmatizer.lemmatize(w) for w in words if w not in stop_words]
    return ' '.join(words)

# --- Keyword Extraction ---
def extract_keywords(text, top_n=15):
    try:
        vectorizer = TfidfVectorizer(max_features=top_n, stop_words='english')
        X = vectorizer.fit_transform([text])
        keywords = vectorizer.get_feature_names_out()
        return list(keywords)
    except Exception:
        return []

# --- Sentiment Analysis ---
def sentiment_scores(text):
    sia = SentimentIntensityAnalyzer()
    scores = sia.polarity_scores(text)
    return scores  # dict: {'neg':..., 'neu':..., 'pos':..., 'compound':...}

# --- Readability ---
def readability_score(text):
    try:
        # Fix the function name to match the actual textstat API
        return textstat.flesch_reading_ease(text)
    except Exception as e:
        # Fallback calculation if textstat fails
        words = len(text.split())
        sentences = len([s for s in text.split('.') if s.strip()])
        if sentences == 0:
            return 50.0
        avg_sentence_length = words / sentences
        return max(0, min(100, 100 - (avg_sentence_length - 15) * 2))
# --- Enhanced Analysis Functions ---

def extract_financial_metrics(text: str) -> Dict[str, List[str]]:
    """Extract financial metrics and numbers from text."""
    metrics = {
        'revenue': [],
        'users': [],
        'growth': [],
        'funding': []
    }
    
    # Revenue patterns
    revenue_patterns = [
        r'\$[\d,]+(?:\.\d+)?[kmb]?\s*(?:revenue|sales|income)',
        r'[\d,]+(?:\.\d+)?\s*(?:million|billion|k)\s*(?:revenue|sales|income)',
        r'(?:revenue|sales|income).*?\$[\d,]+(?:\.\d+)?[kmb]?'
    ]
    
    # User patterns
    user_patterns = [
        r'[\d,]+(?:\.\d+)?[kmb]?\s*(?:users|customers|subscribers)',
        r'(?:users|customers|subscribers).*?[\d,]+(?:\.\d+)?[kmb]?'
    ]
    
    # Growth patterns
    growth_patterns = [
        r'[\d,]+(?:\.\d+)?%\s*(?:growth|increase)',
        r'(?:growth|increase).*?[\d,]+(?:\.\d+)?%',
        r'(?:grew|increased).*?[\d,]+(?:\.\d+)?%'
    ]
    
    # Funding patterns
    funding_patterns = [
        r'\$[\d,]+(?:\.\d+)?[kmb]?\s*(?:funding|investment|raised)',
        r'(?:raised|funding|investment).*?\$[\d,]+(?:\.\d+)?[kmb]?'
    ]
    
    for pattern_list, key in [(revenue_patterns, 'revenue'), (user_patterns, 'users'), 
                             (growth_patterns, 'growth'), (funding_patterns, 'funding')]:
        for pattern in pattern_list:
            matches = re.findall(pattern, text, re.IGNORECASE)
            metrics[key].extend(matches)
    
    return metrics

def analyze_pitch_structure(text: str) -> Dict[str, float]:
    """Analyze the structure and flow of the pitch."""
    sentences = nltk.sent_tokenize(text)
    
    structure_score = {
        'clarity': 0.0,
        'flow': 0.0,
        'completeness': 0.0,
        'engagement': 0.0
    }
    
    # Clarity: Average sentence length (shorter = clearer)
    avg_sentence_length = np.mean([len(sentence.split()) for sentence in sentences])
    structure_score['clarity'] = max(0, 100 - (avg_sentence_length - 15) * 2)  # Optimal ~15 words
    
    # Flow: Transition words and connectors
    transition_words = ['however', 'therefore', 'furthermore', 'moreover', 'consequently', 
                       'additionally', 'meanwhile', 'subsequently', 'thus', 'hence']
    transition_count = sum(1 for word in transition_words if word in text.lower())
    structure_score['flow'] = min(100, (transition_count / len(sentences)) * 100 * 10)
    
    # Completeness: Based on section coverage
    _, _, _, _, section_scores = analyze_sections(text)
    structure_score['completeness'] = (sum(section_scores.values()) / len(section_scores)) * 100
    
    # Engagement: Action words and emotional language
    action_words = ['achieve', 'deliver', 'create', 'build', 'develop', 'launch', 'scale', 'grow']
    emotional_words = ['excited', 'passionate', 'innovative', 'revolutionary', 'breakthrough']
    
    action_count = sum(1 for word in action_words if word in text.lower())
    emotional_count = sum(1 for word in emotional_words if word in text.lower())
    
    structure_score['engagement'] = min(100, ((action_count + emotional_count) / len(sentences)) * 100 * 5)
    
    return structure_score

def extract_competitive_advantages(text: str) -> List[str]:
    """Extract competitive advantages and unique value propositions."""
    advantages = []
    
    advantage_patterns = [
        r'(?:unique|only|first|exclusive|proprietary).*?(?:advantage|feature|technology|approach)',
        r'(?:competitive advantage|moat|differentiator).*?(?:is|includes|involves).*?[.!]',
        r'(?:unlike|different from|better than).*?competitors.*?[.!]'
    ]
    
    for pattern in advantage_patterns:
        matches = re.findall(pattern, text, re.IGNORECASE | re.DOTALL)
        advantages.extend([match.strip() for match in matches])
    
    return advantages[:5]  # Return top 5

def analyze_market_opportunity(text: str) -> Dict[str, any]:
    """Analyze market opportunity mentions."""
    market_info = {
        'size_mentioned': False,
        'tam_sam_som': False,
        'market_size_value': None,
        'market_growth': None
    }
    
    # Check for market size mentions
    size_patterns = [
        r'market.*?(?:size|worth|valued).*?\$?[\d,]+(?:\.\d+)?[kmb]?',
        r'\$?[\d,]+(?:\.\d+)?[kmb]?\s*(?:billion|million|k).*?market',
        r'tam|sam|som'
    ]
    
    for pattern in size_patterns:
        if re.search(pattern, text, re.IGNORECASE):
            market_info['size_mentioned'] = True
            if 'tam' in pattern or 'sam' in pattern or 'som' in pattern:
                market_info['tam_sam_som'] = True
    
    # Extract market size values
    value_pattern = r'\$?([\d,]+(?:\.\d+)?)\s*([kmb]?)\s*(?:billion|million|k)?.*?market'
    matches = re.findall(value_pattern, text, re.IGNORECASE)
    if matches:
        market_info['market_size_value'] = matches[0]
    
    return market_info

def analyze_sections(text):
    """Enhanced section analysis with improved scoring."""
    strengths = []
    weaknesses = []
    actionable_tips = []
    section_scores = {}
    points = 0
    
    # Use section criteria from config
    section_criteria = config.analysis.SECTION_CRITERIA
    
    for section in section_criteria:
        found = False
        confidence = 0
        
        # Enhanced keyword matching with confidence scoring
        for kw in section['keywords']:
            if (len(kw.split()) == 1 and re.search(r'\b' + re.escape(kw) + r'\b', text, re.IGNORECASE)) or \
               (len(kw.split()) > 1 and kw in text.lower()):
                found = True
                # Calculate confidence based on keyword frequency
                keyword_count = len(re.findall(r'\b' + re.escape(kw) + r'\b', text, re.IGNORECASE))
                confidence += keyword_count * 0.2
        
        # Cap confidence at 1.0
        confidence = min(1.0, confidence)
        
        section_scores[section['name']] = 1 if found else 0
        if found:
            points += confidence  # Use confidence for more nuanced scoring
            strengths.append(section['name'])
        else:
            weaknesses.append(section['name'])
            actionable_tips.append(section['tip'])
    
    # Enhanced scoring with confidence
    score = round((points / len(section_criteria)) * 10, 1)
    return score, strengths, weaknesses, actionable_tips, section_scores

def comprehensive_analysis(text: str) -> Dict[str, any]:
    """Comprehensive pitch analysis with all enhanced features."""
    analysis = {}
    
    # Basic analysis
    score, strengths, weaknesses, tips, section_scores = analyze_sections(text)
    read_score = readability_score(text)
    sentiment = sentiment_scores(text)
    keywords = extract_keywords(text)
    
    # Enhanced analysis
    financial_metrics = extract_financial_metrics(text)
    structure_analysis = analyze_pitch_structure(text)
    competitive_advantages = extract_competitive_advantages(text)
    market_analysis = analyze_market_opportunity(text)
    
    # Compile comprehensive results
    analysis = {
        'basic': {
            'score': score,
            'strengths': strengths,
            'weaknesses': weaknesses,
            'tips': tips,
            'section_scores': section_scores,
            'readability': read_score,
            'sentiment': sentiment,
            'keywords': keywords
        },
        'financial': financial_metrics,
        'structure': structure_analysis,
        'competitive': competitive_advantages,
        'market': market_analysis,
        'overall_grade': calculate_overall_grade(score, read_score, sentiment, structure_analysis)
    }
    
    return analysis

def calculate_overall_grade(section_score: float, readability: float, sentiment: dict, structure: dict) -> str:
    """Calculate overall pitch grade."""
    # Normalize scores to 0-100 scale
    section_normalized = (section_score / 10) * 100
    readability_normalized = max(0, min(100, readability))  # Readability can be negative
    sentiment_normalized = (sentiment.get('compound', 0) + 1) * 50  # Convert -1,1 to 0,100
    structure_avg = np.mean(list(structure.values()))
    
    # Weighted average
    overall_score = (
        section_normalized * 0.4 +  # 40% section coverage
        readability_normalized * 0.2 +  # 20% readability
        sentiment_normalized * 0.2 +  # 20% sentiment
        structure_avg * 0.2  # 20% structure
    )
    
    # Convert to letter grade
    if overall_score >= 90:
        return "A+"
    elif overall_score >= 85:
        return "A"
    elif overall_score >= 80:
        return "A-"
    elif overall_score >= 75:
        return "B+"
    elif overall_score >= 70:
        return "B"
    elif overall_score >= 65:
        return "B-"
    elif overall_score >= 60:
        return "C+"
    elif overall_score >= 55:
        return "C"
    elif overall_score >= 50:
        return "C-"
    else:
        return "D" 