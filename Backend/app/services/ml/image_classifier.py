import torch
import cv2
import numpy as np
from PIL import Image
import io
import os
from ultralytics import YOLO
import logging

class WasteImageClassifier:
    def __init__(self):
        self.model = None
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.classes = [
            'Rice Straw', 'Wheat Straw', 'Corn Stalks', 
            'Cotton Waste', 'Sugarcane Bagasse', 'Agricultural Waste'
        ]
        self.load_model()
    
    def load_model(self):
        """Load YOLOv8 model"""
        try:
            model_path = "app/models/best.pt"
            if os.path.exists(model_path):
                self.model = YOLO(model_path)
                print(f"✅ YOLO model loaded successfully from {model_path}")
            else:
                print(f"⚠️ Model file not found at {model_path}. Using fallback classification.")
                self.model = None
        except Exception as e:
            print(f"⚠️ Error loading YOLO model: {e}. Using fallback classification.")
            self.model = None
    
    def preprocess_image(self, image_bytes):
        """Preprocess image for model input"""
        try:
            # Convert bytes to PIL Image
            image = Image.open(io.BytesIO(image_bytes))
            
            # Convert to RGB if necessary
            if image.mode != 'RGB':
                image = image.convert('RGB')
            
            # Convert to numpy array for YOLO
            image_array = np.array(image)
            
            return image_array, image
            
        except Exception as e:
            print(f"Error preprocessing image: {e}")
            return None, None
    
    def estimate_quantity_from_image(self, image, waste_type, detection_results=None):
        """Estimate quantity from image analysis"""
        try:
            # Get image dimensions
            height, width = image.size[1], image.size[0]
            image_area = height * width
            
            # Estimate based on image area and waste type
            area_factor = min(1.0, image_area / (640 * 640))  # Normalize to 640x640
            
            # Base quantity estimates per waste type (kg)
            base_quantities = {
                'Rice Straw': 1200,
                'Wheat Straw': 1000,
                'Corn Stalks': 1500,
                'Cotton Waste': 800,
                'Sugarcane Bagasse': 2000,
                'Agricultural Waste': 1000
            }
            
            base_qty = base_quantities.get(waste_type, 1000)
            
            # If we have YOLO detection results, use them for better estimation
            if (detection_results and len(detection_results) > 0 and 
                hasattr(detection_results[0], 'boxes') and 
                detection_results[0].boxes is not None and 
                len(detection_results[0].boxes) > 0):
                # Calculate total detection area
                total_detection_area = 0
                for box in detection_results[0].boxes:
                    x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
                    detection_area = (x2 - x1) * (y2 - y1)
                    total_detection_area += detection_area
                
                # Estimate quantity based on detection coverage
                detection_ratio = total_detection_area / (width * height)
                estimated_qty = base_qty * detection_ratio * (1 + area_factor)
            else:
                # Fallback estimation based on image size
                estimated_qty = base_qty * area_factor
            
            # Add some randomness and bounds
            estimated_qty *= (0.8 + np.random.random() * 0.4)  # 80% to 120% variation
            estimated_qty = max(100, min(5000, estimated_qty))  # Bounds: 100kg to 5000kg
            
            return round(estimated_qty, 0)
            
        except Exception as e:
            print(f"Error estimating quantity: {e}")
            return 1000  # Default fallback
    
    def classify_image_fallback(self, image):
        """Fallback classification based on image properties"""
        try:
            # Convert PIL to numpy array
            img_array = np.array(image)
            
            # Simple color-based classification
            # Calculate average color values
            avg_color = np.mean(img_array, axis=(0, 1))
            
            # Simple heuristics based on color
            if avg_color[1] > avg_color[0] and avg_color[1] > avg_color[2]:  # More green
                return "Rice Straw", 0.7
            elif avg_color[0] > avg_color[1]:  # More red/brown
                return "Wheat Straw", 0.65
            elif np.mean(avg_color) < 100:  # Darker
                return "Cotton Waste", 0.6
            else:
                return "Agricultural Waste", 0.6
                
        except Exception as e:
            print(f"Error in fallback classification: {e}")
            return "Agricultural Waste", 0.5
    
    def predict(self, image_bytes):
        """Main prediction function"""
        try:
            # Preprocess image
            processed_image, pil_image = self.preprocess_image(image_bytes)
            
            if processed_image is None:
                return {
                    "wasteType": "Unknown",
                    "confidence": 0.5,
                    "quantity": 1000,
                    "error": "Image preprocessing failed"
                }
            
            if self.model:
                try:
                    # YOLO prediction
                    results = self.model(processed_image)
                    
                    if results and len(results) > 0 and hasattr(results[0], 'probs') and results[0].probs is not None:
                        # Classification results
                        top1_idx = results[0].probs.top1
                        confidence = float(results[0].probs.top1conf)
                        
                        # Get waste type from model classes
                        if hasattr(results[0], 'names') and top1_idx < len(results[0].names):
                            waste_type = results[0].names[top1_idx]
                        else:
                            waste_type = self.classes[min(top1_idx, len(self.classes) - 1)]
                        
                        # Estimate quantity
                        quantity = self.estimate_quantity_from_image(pil_image, waste_type, results)
                        
                    elif results and len(results) > 0 and hasattr(results[0], 'boxes') and len(results[0].boxes) > 0:
                        # Detection results
                        best_detection = results[0].boxes[0]  # Get first/best detection
                        class_id = int(best_detection.cls[0].cpu())
                        confidence = float(best_detection.conf[0].cpu())
                        
                        # Get waste type from detection
                        if hasattr(results[0], 'names') and class_id < len(results[0].names):
                            waste_type = results[0].names[class_id]
                        else:
                            waste_type = self.classes[min(class_id, len(self.classes) - 1)]
                        
                        # Estimate quantity
                        quantity = self.estimate_quantity_from_image(pil_image, waste_type, results)
                        
                    else:
                        # No valid predictions, use fallback
                        waste_type, confidence = self.classify_image_fallback(pil_image)
                        quantity = self.estimate_quantity_from_image(pil_image, waste_type)
                        
                except Exception as model_error:
                    print(f"YOLO model prediction error: {model_error}")
                    # Fallback to rule-based classification
                    waste_type, confidence = self.classify_image_fallback(pil_image)
                    quantity = self.estimate_quantity_from_image(pil_image, waste_type)
            else:
                # No model available, use fallback
                waste_type, confidence = self.classify_image_fallback(pil_image)
                quantity = self.estimate_quantity_from_image(pil_image, waste_type)
            
            return {
                "wasteType": waste_type,
                "confidence": confidence,
                "quantity": int(quantity),
                "processingRecommendation": self.get_processing_method(waste_type)
            }
            
        except Exception as e:
            print(f"Prediction error: {e}")
            return {
                "wasteType": "Agricultural Waste",
                "confidence": 0.5,
                "quantity": 1000,
                "error": str(e)
            }
    
    def get_processing_method(self, waste_type):
        """Get recommended processing method"""
        methods = {
            'Rice Straw': 'Anaerobic Digestion',
            'Wheat Straw': 'Gasification', 
            'Corn Stalks': 'Pyrolysis',
            'Cotton Waste': 'Composting',
            'Sugarcane Bagasse': 'Direct Combustion',
            'Agricultural Waste': 'Anaerobic Digestion'
        }
        return methods.get(waste_type, 'Anaerobic Digestion')

# Global instance
image_classifier = WasteImageClassifier()
