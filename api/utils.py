import os
import numpy as np
import tensorflow as tf
import requests
from PIL import Image
from django.conf import settings
from .models import Medicine

# --- Optional: sensible defaults if not set in settings.py ---
DEFAULT_MODEL_PATH = getattr(settings, "MODEL_PATH", None) or os.path.join(
    getattr(settings, "BASE_DIR", "."), "models", "skin_disease_model_best.h5"
)
MED_API_BASE = getattr(settings, "MEDICINE_API_BASE_URL", "https://api.fda.gov/drug")

# Try to import cv2, but provide fallback if it fails
try:
    import cv2
    CV2_AVAILABLE = True
except ImportError:
    CV2_AVAILABLE = False
    print("Warning: OpenCV not available, using PIL for image processing")

# Cancer type mapping
CANCER_TYPES = {
    0: 'melanoma',
    1: 'basal_cell_carcinoma',
    2: 'squamous_cell_carcinoma',
    3: 'benign',
    4: 'actinic_keratosis',
    5: 'dermatofibroma',
    6: 'vascular_lesion'
}

# Cancer type descriptions
CANCER_DESCRIPTIONS = {
    'melanoma': 'Melanoma is a serious form of skin cancer that begins in cells known as melanocytes.',
    'basal_cell_carcinoma': 'Basal cell carcinoma is the most common type of skin cancer, usually slow-growing.',
    'squamous_cell_carcinoma': 'Squamous cell carcinoma is a common type of skin cancer that develops in squamous cells.',
    'benign': 'This appears to be a benign skin condition, but regular monitoring is recommended.',
    'actinic_keratosis': 'Actinic keratosis is a precancerous skin condition that can develop into squamous cell carcinoma.',
    'dermatofibroma': 'Dermatofibroma is a common benign skin growth that usually appears on the legs.',
    'vascular_lesion': 'Vascular lesions are abnormalities of blood vessels that can appear on the skin.'
}

# Symptoms for each cancer type
CANCER_SYMPTOMS = {
    'melanoma': 'Asymmetrical moles, irregular borders, multiple colors, diameter larger than 6mm, evolving appearance',
    'basal_cell_carcinoma': 'Pearly or waxy bump, flat flesh-colored or brown scar-like lesion, bleeding or scabbing sore',
    'squamous_cell_carcinoma': 'Firm red nodule, flat lesion with scaly crust, new sore or raised area on old scar',
    'benign': 'Usually no concerning symptoms, but monitor for changes in size, color, or texture',
    'actinic_keratosis': 'Rough, scaly patches, usually less than 2cm, may be pink or red',
    'dermatofibroma': 'Small, firm, raised growth, usually brown or pink, may itch or be tender',
    'vascular_lesion': 'Red, purple, or pink patches or bumps, may be present at birth or develop later'
}

# Recommendations for each cancer type
CANCER_RECOMMENDATIONS = {
    'melanoma': 'Immediate consultation with a dermatologist is recommended. Regular skin checks and sun protection are essential.',
    'basal_cell_carcinoma': 'Consult a dermatologist for proper diagnosis and treatment. Usually treatable with surgery.',
    'squamous_cell_carcinoma': 'Seek medical attention promptly. Treatment typically involves surgical removal.',
    'benign': 'Continue regular skin monitoring. Consult a doctor if changes are noticed.',
    'actinic_keratosis': 'Consult a dermatologist for treatment options. Regular skin checks recommended.',
    'dermatofibroma': 'Usually no treatment needed unless symptomatic. Monitor for changes.',
    'vascular_lesion': 'Consult a dermatologist for proper evaluation and treatment options.'
}

# --- Load the model lazily once (prevents reloading every request) ---
_MODEL = None
def _get_model():
    global _MODEL
    if _MODEL is None:
        model_path = DEFAULT_MODEL_PATH
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Model file not found at {model_path}")
        # compile=False avoids issues when the original compile context isn't present
        _MODEL = tf.keras.models.load_model(model_path, compile=False)
    return _MODEL

def preprocess_image(image_path, target_size=(224, 224)):
    """Preprocess image for model prediction. Returns np.ndarray of shape (1, H, W, 3) in [0,1]."""
    try:
        if CV2_AVAILABLE:
            img = cv2.imread(image_path)
            if img is None:
                raise ValueError(f"cv2.imread returned None. Bad path or unreadable image: {image_path}")
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            img = cv2.resize(img, target_size)
            img = img.astype(np.float32) / 255.0
        else:
            with Image.open(image_path) as pil_img:
                pil_img = pil_img.convert('RGB')
                pil_img = pil_img.resize(target_size)
                # Convert PIL Image -> NumPy BEFORE astype (this was the bug)
                img = np.array(pil_img, dtype=np.float32) / 255.0

        # Add batch dimension
        img = np.expand_dims(img, axis=0)
        return img
    except Exception as e:
        print(f"Error preprocessing image: {e}")
        return None

def predict_cancer_type(image_path):
    """Predict cancer type using the loaded model. Returns (cancer_type:str|None, confidence:float)."""
    try:
        img = preprocess_image(image_path)
        if img is None:
            return None, 0.0

        model = _get_model()
        preds = model.predict(img)
        if preds is None or len(preds) == 0:
            return None, 0.0

        predicted_class = int(np.argmax(preds[0]))
        confidence = float(np.max(preds[0]) * 100.0)
        cancer_type = CANCER_TYPES.get(predicted_class, 'unknown')
        return cancer_type, confidence
    except Exception as e:
        print(f"Error in prediction: {e}")
        return None, 0.0

def get_medicine_suggestions(cancer_type):
    """
    Get medicine suggestions from the FDA API based on cancer type.
    Uses 'indications_and_usage' instead of 'openfda.generic_name' so
    we can search by disease/condition terms.
    """
    suggestions = []
    try:
        # Map cancer_type to search terms
        search_terms = {
            'melanoma': ['melanoma'],
            'basal_cell_carcinoma': ['basal cell carcinoma', 'skin cancer'],
            'squamous_cell_carcinoma': ['squamous cell carcinoma', 'skin cancer'],
            'actinic_keratosis': ['actinic keratosis'],
            'benign': ['dermatological treatment'],
            'dermatofibroma': ['dermatofibroma'],
            'vascular_lesion': ['vascular lesion']
        }
        terms = search_terms.get(cancer_type, ['skin cancer'])

        for term in terms[:2]:  # keep it light
            url = f"{MED_API_BASE}/label.json"
            params = {
                # Query labels by indications text; this field exists more consistently for conditions
                'search': f'indications_and_usage:"{term}"',
                'limit': 5
            }
            resp = requests.get(url, params=params, timeout=10)
            if resp.status_code != 200:
                continue

            payload = resp.json()
            results = payload.get('results', [])

            for result in results:
                ofda = result.get('openfda', {}) or {}
                generic_name = (ofda.get('generic_name') or ['Unknown'])[0]
                brand_name = (ofda.get('brand_name') or ['Unknown'])[0]
                dosage_form = (ofda.get('dosage_form') or ['Unknown'])[0]
                manufacturer = (ofda.get('manufacturer_name') or ['Unknown'])[0]

                desc_list = result.get('description') or result.get('indications_and_usage') or ['No description available']
                description = desc_list[0] if isinstance(desc_list, list) and desc_list else str(desc_list)
                if description and len(description) > 500:
                    description = description[:500] + '...'

                suggestions.append({
                    'name': brand_name,
                    'generic_name': generic_name,
                    'dosage_form': dosage_form,
                    'manufacturer': manufacturer,
                    'description': description,
                    'side_effects': 'Consult your healthcare provider for complete information about side effects.'
                })

                if len(suggestions) >= 5:
                    break

            if len(suggestions) >= 5:
                break

    except Exception as e:
        print(f"Error fetching medicines: {e}")

    if not suggestions:
        # Fallback if API fails or returns nothing
        suggestions = [{
            'name': 'Consultation Required',
            'generic_name': 'Medical Consultation',
            'dosage_form': 'Consultation',
            'manufacturer': 'Healthcare Provider',
            'description': 'Please consult with a healthcare provider for proper diagnosis and treatment.',
            'side_effects': 'N/A'
        }]

    return suggestions

def get_cancer_info(cancer_type):
    """Get comprehensive information about a cancer type"""
    return {
        'description': CANCER_DESCRIPTIONS.get(cancer_type, 'Information not available'),
        'symptoms': CANCER_SYMPTOMS.get(cancer_type, 'Consult a healthcare provider for symptoms'),
        'recommendations': CANCER_RECOMMENDATIONS.get(cancer_type, 'Consult a healthcare provider for recommendations')
    }
