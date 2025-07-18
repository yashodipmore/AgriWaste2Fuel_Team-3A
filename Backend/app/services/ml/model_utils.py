import logging
import time
import json
from datetime import datetime
from typing import Dict, Any, List, List

def log_prediction(model_type: str, input_data: Dict, prediction: Dict, processing_time: float):
    """Log model predictions for monitoring"""
    log_data = {
        "timestamp": datetime.now().isoformat(),
        "model_type": model_type,
        "prediction": prediction,
        "processing_time": processing_time,
        "confidence": prediction.get("confidence", 0),
        "waste_type": prediction.get("wasteType", "unknown"),
        "quantity": prediction.get("quantity", 0)
    }
    
    logging.info(f"ML_PREDICTION: {json.dumps(log_data)}")

def validate_image_input(image_bytes: bytes) -> Dict[str, Any]:
    """Validate image input"""
    if not image_bytes:
        return {"valid": False, "error": "Empty image data"}
    
    if len(image_bytes) > 10 * 1024 * 1024:  # 10MB limit
        return {"valid": False, "error": "Image too large (max 10MB)"}
    
    # Check for basic image headers
    image_headers = [
        b'\xff\xd8\xff',  # JPEG
        b'\x89PNG\r\n\x1a\n',  # PNG
        b'GIF87a',  # GIF87a
        b'GIF89a',  # GIF89a
        b'RIFF',  # WebP (partial)
    ]
    
    is_valid_image = any(image_bytes.startswith(header) for header in image_headers)
    
    if not is_valid_image:
        return {"valid": False, "error": "Invalid image format"}
    
    return {"valid": True}

def validate_text_input(text: str) -> Dict[str, Any]:
    """Validate text input"""
    if not text or not text.strip():
        return {"valid": False, "error": "Empty text input"}
    
    if len(text) > 1000:  # 1000 character limit
        return {"valid": False, "error": "Text too long (max 1000 characters)"}
    
    # Check for minimum meaningful content
    if len(text.strip()) < 3:
        return {"valid": False, "error": "Text too short (minimum 3 characters)"}
    
    return {"valid": True}

def format_prediction_response(prediction: Dict, processing_time: float) -> Dict:
    """Format prediction response consistently"""
    return {
        "status": "success",
        "data": prediction,
        "metadata": {
            "processing_time": round(processing_time, 3),
            "timestamp": datetime.now().isoformat(),
            "model_version": "1.0.0"
        }
    }

def handle_prediction_error(error: Exception, model_type: str) -> Dict:
    """Handle prediction errors consistently"""
    error_message = str(error)
    logging.error(f"{model_type} prediction error: {error_message}")
    
    return {
        "status": "error",
        "error": error_message,
        "data": {
            "wasteType": "Unknown",
            "confidence": 0.0,
            "quantity": 1000,
            "fallback": True
        },
        "metadata": {
            "timestamp": datetime.now().isoformat(),
            "model_type": model_type,
            "error_handled": True
        }
    }

class PerformanceMonitor:
    """Monitor ML model performance"""
    
    def __init__(self):
        self.predictions = []
        self.max_history = 1000
    
    def record_prediction(self, model_type: str, processing_time: float, confidence: float):
        """Record prediction metrics"""
        record = {
            "timestamp": datetime.now().isoformat(),
            "model_type": model_type,
            "processing_time": processing_time,
            "confidence": confidence
        }
        
        self.predictions.append(record)
        
        # Keep only recent predictions
        if len(self.predictions) > self.max_history:
            self.predictions = self.predictions[-self.max_history:]
    
    def get_performance_stats(self) -> Dict:
        """Get performance statistics"""
        if not self.predictions:
            return {"error": "No predictions recorded"}
        
        processing_times = [p["processing_time"] for p in self.predictions]
        confidences = [p["confidence"] for p in self.predictions]
        
        return {
            "total_predictions": len(self.predictions),
            "avg_processing_time": sum(processing_times) / len(processing_times),
            "max_processing_time": max(processing_times),
            "min_processing_time": min(processing_times),
            "avg_confidence": sum(confidences) / len(confidences),
            "recent_predictions": self.predictions[-10:]  # Last 10
        }

class ModelManager:
    """Manages ML model lifecycle and utilities"""
    
    def __init__(self):
        self.models = {}
        self.load_times = {}
        
    def register_model(self, name: str, model_instance: Any):
        """Register a model instance"""
        self.models[name] = model_instance
        self.load_times[name] = datetime.now()
        logging.info(f"Model '{name}' registered successfully")
        
    def get_model(self, name: str):
        """Get a registered model"""
        return self.models.get(name)
        
    def get_model_info(self, name: str) -> Dict:
        """Get model information"""
        if name in self.models:
            return {
                "name": name,
                "loaded": True,
                "load_time": self.load_times[name].isoformat(),
                "type": type(self.models[name]).__name__
            }
        return {"name": name, "loaded": False}
        
    def list_models(self) -> List[Dict]:
        """List all registered models"""
        return [self.get_model_info(name) for name in self.models.keys()]
        
    def unload_model(self, name: str):
        """Unload a model to free memory"""
        if name in self.models:
            del self.models[name]
            del self.load_times[name]
            logging.info(f"Model '{name}' unloaded")
            
    def get_memory_usage(self) -> Dict:
        """Get memory usage statistics"""
        try:
            import psutil
            process = psutil.Process()
            return {
                "memory_mb": round(process.memory_info().rss / 1024 / 1024, 2),
                "cpu_percent": process.cpu_percent(),
                "models_loaded": len(self.models)
            }
        except ImportError:
            return {"error": "psutil not available"}

# Global performance monitor
performance_monitor = PerformanceMonitor()

# Global model manager instance
model_manager = ModelManager()
