import re
import json
from typing import Dict, List, Tuple
import logging

class WasteTextClassifier:
    def __init__(self):
        self.model = None
        self.waste_keywords = self.load_waste_keywords()
        print("✅ Text classifier initialized with rule-based classification")
    
    def load_waste_keywords(self) -> Dict[str, List[str]]:
        """Load keywords for waste type classification"""
        return {
            'Rice Straw': [
                'rice', 'paddy', 'straw', 'chawal', 'dhan', 'धान', 'चावल', 
                'rice stubble', 'paddy straw', 'rice residue', 'rice waste'
            ],
            'Wheat Straw': [
                'wheat', 'gehun', 'straw', 'गेहूं', 'wheat stubble', 
                'wheat residue', 'wheat waste', 'गेहुँ'
            ],
            'Corn Stalks': [
                'corn', 'maize', 'makka', 'stalks', 'मक्का', 'भुट्टा',
                'corn residue', 'maize stalks', 'corn waste', 'makkai'
            ],
            'Cotton Waste': [
                'cotton', 'kapas', 'कपास', 'cotton waste', 'cotton residue',
                'cotton stalks', 'कॉटन'
            ],
            'Sugarcane Bagasse': [
                'sugarcane', 'bagasse', 'ganna', 'गन्ना', 'sugar cane',
                'cane waste', 'sugarcane residue', 'गन्ने', 'ikhu'
            ],
            'Agricultural Waste': [
                'farm waste', 'crop waste', 'agricultural', 'farming',
                'खेती', 'कृषि', 'फसल', 'किसान', 'agricultural residue'
            ]
        }
    
    def preprocess_text(self, text: str) -> str:
        """Clean and preprocess text"""
        if not text:
            return ""
        
        text = text.lower().strip()
        # Remove extra spaces and special characters
        text = re.sub(r'[^\w\s]', ' ', text)
        text = re.sub(r'\s+', ' ', text)
        return text
    
    def extract_quantity_from_text(self, text: str) -> float:
        """Extract quantity from text using regex patterns"""
        text = text.lower()
        
        # Patterns for quantity extraction
        patterns = [
            r'(\d+(?:\.\d+)?)\s*(?:kg|किलो|kilo)',
            r'(\d+(?:\.\d+)?)\s*(?:ton|tons|टन)',
            r'(\d+(?:\.\d+)?)\s*(?:quintal|quintals|क्विंटल)',
            r'(\d+(?:\.\d+)?)\s*(?:pound|pounds|lb)',
            r'(\d+(?:\.\d+)?)\s*(?:gram|grams|ग्राम|gm)',
            r'(\d+(?:\.\d+)?)\s*(?:sack|sacks|बोरी|bags)',
            r'(\d+(?:\.\d+)?)\s*(?:bundle|bundles|गट्ठर)',
            r'(\d+(?:\.\d+)?)\s*(?:acre|acres|एकड़)',
            r'(\d+(?:\.\d+)?)\s*(?:hectare|hectares|हेक्टेयर)',
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, text)
            if matches:
                quantity = float(matches[0])
                
                # Convert to kg based on unit
                if 'ton' in pattern or 'टन' in pattern:
                    quantity *= 1000
                elif 'quintal' in pattern or 'क्विंटल' in pattern:
                    quantity *= 100
                elif 'pound' in pattern or 'lb' in pattern:
                    quantity *= 0.453592
                elif 'gram' in pattern or 'ग्राम' in pattern or 'gm' in pattern:
                    quantity /= 1000
                elif 'sack' in pattern or 'बोरी' in pattern or 'bags' in pattern:
                    quantity *= 50  # Assuming 50kg per sack
                elif 'bundle' in pattern or 'गट्ठर' in pattern:
                    quantity *= 25  # Assuming 25kg per bundle
                elif 'acre' in pattern or 'एकड़' in pattern:
                    quantity *= 2000  # Assuming 2000kg waste per acre
                elif 'hectare' in pattern or 'हेक्टेयर' in pattern:
                    quantity *= 5000  # Assuming 5000kg waste per hectare
                
                return max(10, min(50000, quantity))  # Bounds: 10kg to 50000kg
        
        # If no quantity found, look for descriptive terms
        quantity_terms = {
            'small': 100, 'छोटा': 100, 'little': 100, 'few': 150,
            'medium': 500, 'मध्यम': 500, 'moderate': 500, 'some': 300,
            'large': 1500, 'बड़ा': 1500, 'big': 1500, 'huge': 2000,
            'massive': 3000, 'enormous': 3000, 'lots': 2000, 'many': 1000,
            'truck': 5000, 'ट्रक': 5000, 'tractor': 3000, 'ट्रैक्टर': 3000
        }
        
        for term, qty in quantity_terms.items():
            if term in text:
                return qty
        
        return 1000  # Default quantity
    
    def rule_based_classification(self, text: str) -> Tuple[str, float]:
        """Rule-based classification using keyword matching"""
        text = self.preprocess_text(text)
        
        # Score each waste type based on keyword matches
        scores = {}
        
        for waste_type, keywords in self.waste_keywords.items():
            score = 0
            for keyword in keywords:
                keyword_lower = keyword.lower()
                if keyword_lower in text:
                    # Give higher score for exact matches
                    if f" {keyword_lower} " in f" {text} ":
                        score += 2
                    else:
                        score += 1
            
            if score > 0:
                scores[waste_type] = score
        
        if scores:
            # Get the waste type with highest score
            best_waste_type = max(scores.keys(), key=lambda k: scores[k])
            max_score = scores[best_waste_type]
            
            # Calculate confidence based on score (return as percentage)
            confidence = min(95.0, 60.0 + (max_score * 10.0))
            
            return best_waste_type, confidence
        
        return "Agricultural Waste", 60.0
    
    def extract_location_info(self, text: str) -> str:
        """Extract location information from text"""
        text = text.lower()
        
        # Common Indian states and regions
        locations = [
            'punjab', 'haryana', 'uttar pradesh', 'up', 'bihar', 'rajasthan',
            'maharashtra', 'gujarat', 'karnataka', 'andhra pradesh', 'telangana',
            'tamil nadu', 'kerala', 'odisha', 'west bengal', 'jharkhand',
            'chhattisgarh', 'madhya pradesh', 'mp', 'assam', 'delhi',
            'पंजाब', 'हरियाणा', 'उत्तर प्रदेश', 'बिहार', 'राजस्थान'
        ]
        
        for location in locations:
            if location in text:
                return location.title()
        
        return "India"  # Default location
    
    def get_processing_method(self, waste_type: str) -> str:
        """Get processing recommendation"""
        methods = {
            'Rice Straw': 'Anaerobic Digestion',
            'Wheat Straw': 'Gasification',
            'Corn Stalks': 'Pyrolysis', 
            'Cotton Waste': 'Composting',
            'Sugarcane Bagasse': 'Direct Combustion',
            'Agricultural Waste': 'Anaerobic Digestion'
        }
        return methods.get(waste_type, 'Anaerobic Digestion')
    
    def get_waste_category(self, waste_type: str) -> str:
        """Get category for waste type"""
        category_map = {
            "rice_straw": "Crop Residue",
            "wheat_straw": "Crop Residue", 
            "corn_stalks": "Crop Residue",
            "cow_dung": "Animal Waste",
            "buffalo_dung": "Animal Waste",
            "chicken_manure": "Animal Waste",
            "vegetable_scraps": "Organic Waste",
            "fruit_peels": "Organic Waste",
            "sugarcane_bagasse": "Agricultural Byproduct"
        }
        return category_map.get(waste_type.lower().replace(" ", "_"), "Agricultural Waste")
    
    def get_similar_waste_types(self, waste_type: str) -> List[str]:
        """Get similar waste types for suggestions"""
        category = self.get_waste_category(waste_type)
        similar_by_category = {
            "Crop Residue": ["Rice Straw", "Wheat Straw", "Corn Stalks", "Cotton Stalks"],
            "Animal Waste": ["Cow Dung", "Buffalo Dung", "Chicken Manure", "Goat Manure"],
            "Organic Waste": ["Vegetable Scraps", "Fruit Peels", "Food Waste", "Kitchen Waste"],
            "Agricultural Byproduct": ["Sugarcane Bagasse", "Coconut Husk", "Rice Husk"]
        }
        return similar_by_category.get(category, ["Rice Straw", "Wheat Straw", "Corn Stalks"])
    
    def get_supported_categories(self) -> Dict:
        """Get all supported waste categories"""
        return {
            "Crop Residue": ["Rice Straw", "Wheat Straw", "Corn Stalks", "Cotton Stalks"],
            "Animal Waste": ["Cow Dung", "Buffalo Dung", "Chicken Manure", "Goat Manure"],
            "Organic Waste": ["Vegetable Scraps", "Fruit Peels", "Food Waste", "Kitchen Waste"],
            "Agricultural Byproduct": ["Sugarcane Bagasse", "Coconut Husk", "Rice Husk", "Corn Husks"]
        }
    
    def get_suggestions(self, query: str) -> List[str]:
        """Get search suggestions for partial queries"""
        all_types = []
        for category_types in self.get_supported_categories().values():
            all_types.extend(category_types)
        
        # Filter based on query
        suggestions = [t for t in all_types if query.lower() in t.lower()]
        return suggestions[:10]
    
    def predict(self, waste_description: str, quantity: float = None, location: str = None) -> Dict:
        """Main prediction function"""
        try:
            processed_text = self.preprocess_text(waste_description)
            
            if not processed_text:
                return {
                    "wasteType": "Agricultural Waste",
                    "confidence": 0.5,
                    "quantity": quantity or 1000,
                    "location": location or "India",
                    "error": "Empty or invalid input text"
                }
            
            # Classify waste type
            waste_type, confidence = self.rule_based_classification(processed_text)
            
            # Extract quantity if not provided
            if quantity is None:
                quantity = self.extract_quantity_from_text(processed_text)
            
            # Extract location if not provided
            if location is None:
                location = self.extract_location_info(processed_text)
            
            # Get processing recommendation
            processing_method = self.get_processing_method(waste_type)
            
            return {
                "waste_type": waste_type,
                "confidence": confidence,
                "quantity": quantity,
                "category": self.get_waste_category(waste_type),
                "location": location,
                "processing_recommendation": processing_method,
                "similar_types": self.get_similar_waste_types(waste_type),
                "extracted_info": {
                    "original_text": waste_description,
                    "processed_text": processed_text,
                    "extracted_quantity": quantity,
                    "extracted_location": location
                }
            }
            
        except Exception as e:
            logging.error(f"Text prediction error: {e}")
            return {
                "waste_type": "Agricultural Waste",
                "confidence": 50.0,
                "quantity": quantity or 1000,
                "category": "General",
                "location": location or "India",
                "similar_types": ["Rice Straw", "Wheat Straw", "Corn Stalks"],
                "error": str(e)
            }

# Global instance
text_classifier = WasteTextClassifier()
