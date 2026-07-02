from typing import Dict

# Configuration map defining baseline threat factors per class
CLASS_THREAT_WEIGHTS: Dict[str, float] = {
    "fire": 1.0,
    "smoke": 0.8,
    "heavy_exhaust": 0.6,
    "dust": 0.3
}

def calculate_severity(
    class_name: str, 
    confidence: float, 
    bbox_area: float, 
    frame_area: float
) -> float:
    """Calculates an environmental severity metric between 0.0 and 1.0.
    
    Formula considers:
    1. Class weight (Fire vs Dust)
    2. Model confidence accuracy
    3. Spatial coverage (how much of the frame the pollution occupies)
    """
    weight = CLASS_THREAT_WEIGHTS.get(class_name.lower(), 0.2)
    
    # Calculate percentage of screen filled by the object
    spatial_coverage = bbox_area / frame_area if frame_area > 0 else 0.0
    
    # Normalize spatial impact: filling 15% or more of a CCTV field of view maxes out this factor
    spatial_factor = min(spatial_coverage / 0.15, 1.0)
    
    # Compose composite base score (40% confidence verification + 60% physical size impact)
    base_score = (0.4 * confidence) + (0.6 * spatial_factor)
    
    # Scale score against class specific severity weight and safely clamp bounds
    final_score = max(0.0, min(base_score * weight, 1.0))
    
    return round(final_score, 2)