from typing import Dict, List, Tuple
import json
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Download required NLTK data
try:
    nltk.data.find('tokenizers/punkt')
    nltk.data.find('corpora/stopwords')
    nltk.data.find('corpora/wordnet')
except LookupError:
    nltk.download('punkt')
    nltk.download('stopwords')
    nltk.download('wordnet')

class MedicalKnowledgeBase:
    def __init__(self):
        self.lemmatizer = WordNetLemmatizer()
        self.stop_words = set(stopwords.words('english'))
        self.vectorizer = TfidfVectorizer()
        
        # Initialize basic symptoms database
        self.symptoms_db = {
            "headache": {
                "description": "Pain or discomfort in the head or upper neck",
                "severity_levels": ["mild", "moderate", "severe"],
                "related_conditions": ["tension", "migraine", "sinusitis"],
                "recommendations": [
                    "Rest in a quiet, dark room",
                    "Stay hydrated",
                    "Try over-the-counter pain relievers"
                ]
            },
            "fever": {
                "description": "Elevated body temperature above normal (98.6°F/37°C)",
                "severity_levels": ["mild (99-100.9°F)", "moderate (101-103°F)", "high (>103°F)"],
                "related_conditions": ["infection", "flu", "covid-19"],
                "recommendations": [
                    "Rest and stay hydrated",
                    "Take over-the-counter fever reducers",
                    "Monitor temperature regularly"
                ]
            },
            "cough": {
                "description": "Sudden expulsion of air from the lungs",
                "severity_levels": ["mild", "moderate", "severe"],
                "related_conditions": ["cold", "flu", "allergies"],
                "recommendations": [
                    "Stay hydrated",
                    "Use honey for soothing",
                    "Consider over-the-counter cough medicine"
                ]
            }
        }
        
        # Emergency symptoms that require immediate attention
        self.emergency_symptoms = {
            "chest pain",
            "difficulty breathing",
            "severe abdominal pain",
            "loss of consciousness"
        }

    def preprocess_text(self, text: str) -> str:
        """Preprocess the input text for analysis."""
        try:
            # Convert to lowercase and tokenize
            tokens = word_tokenize(text.lower())
            # Remove stopwords and lemmatize
            tokens = [self.lemmatizer.lemmatize(token) for token in tokens if token.isalnum()]
            tokens = [token for token in tokens if token not in self.stop_words]
            return " ".join(tokens)
        except Exception as e:
            print(f"Error in preprocess_text: {str(e)}")
            return text.lower()  # Fallback to simple lowercase if processing fails

    def check_emergency(self, text: str) -> Tuple[bool, str]:
        """Check if the symptoms described indicate an emergency."""
        try:
            preprocessed_text = self.preprocess_text(text)
            for emergency in self.emergency_symptoms:
                if emergency in preprocessed_text:
                    return True, f"WARNING: {emergency} detected. Please seek immediate medical attention!"
            return False, ""
        except Exception as e:
            print(f"Error in check_emergency: {str(e)}")
            return False, ""

    def extract_symptoms(self, text: str) -> List[Dict]:
        """Extract symptoms from the text and match with database."""
        try:
            preprocessed_text = self.preprocess_text(text)
            matched_symptoms = []
            
            # Check each symptom in our database
            for symptom, data in self.symptoms_db.items():
                if symptom in preprocessed_text:
                    matched_symptoms.append({
                        "symptom": symptom,
                        "info": data
                    })
            
            return matched_symptoms
        except Exception as e:
            print(f"Error in extract_symptoms: {str(e)}")
            return []

    def analyze_symptoms(self, user_input: str) -> Dict:
        """Analyze user symptoms and provide recommendations."""
        try:
            # Check for emergencies first
            is_emergency, emergency_msg = self.check_emergency(user_input)
            if is_emergency:
                return {
                    "type": "emergency",
                    "message": emergency_msg,
                    "recommendations": ["Seek immediate medical attention", "Call emergency services"]
                }

            # Extract and analyze symptoms
            matched_symptoms = self.extract_symptoms(user_input)
            
            if not matched_symptoms:
                return {
                    "type": "unknown",
                    "message": "I'm not sure about these symptoms. Please provide more details or consult a healthcare professional.",
                    "recommendations": ["Consult a healthcare provider for proper diagnosis"]
                }

            return {
                "type": "analysis",
                "matched_symptoms": matched_symptoms,
                "recommendations": []
            }

        except Exception as e:
            print(f"Error in analyze_symptoms: {str(e)}")
            return {
                "type": "error",
                "message": "I encountered an error analyzing your symptoms. Please try again.",
                "error": str(e)
            }

    def get_response(self, user_input: str) -> str:
        """Generate a response based on user input."""
        try:
            if not user_input:
                return "Please describe your symptoms."

            analysis = self.analyze_symptoms(user_input)
            
            if analysis["type"] == "emergency":
                return analysis["message"]
            
            if analysis["type"] == "unknown":
                return analysis["message"]
            
            if analysis["type"] == "error":
                return analysis["message"]
            
            # Format response
            response = "Based on your description:\n\n"
            
            for symptom in analysis["matched_symptoms"]:
                response += f"Regarding {symptom['symptom']}:\n"
                response += f"• {symptom['info']['description']}\n"
                response += f"• Severity levels: {', '.join(symptom['info']['severity_levels'])}\n"
                response += "\nRecommendations:\n"
                for rec in symptom["info"]["recommendations"]:
                    response += f"• {rec}\n"
                response += "\n"
            
            response += "\nGeneral Advice:\n"
            response += "• Monitor your symptoms\n"
            response += "• If symptoms worsen, consult a healthcare provider\n"
            response += "• Keep track of how long you've had these symptoms\n"
            
            return response

        except Exception as e:
            print(f"Error in get_response: {str(e)}")
            return "I apologize, but I encountered an error processing your request. Please try again."
