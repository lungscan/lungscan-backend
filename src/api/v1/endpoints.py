import datetime
import traceback
import os
import random

import pydicom
from flask import jsonify, current_app, request, send_file
from typing import Dict
from . import api_v1
from src.extensions import limiter
import numpy as np

@api_v1.route("/health")
def health():
    """Health check endpoint."""
    return jsonify(
        {
            "status": "healthy",
            "timestamp": datetime.datetime.utcnow().replace(microsecond=0).isoformat() + "Z"
        }
    )

@api_v1.route("/pathologies")
def get_pathologies():
    """Returns the list of supported pathologies."""
    try:
        lung_analyzer = current_app.lung_analyzer
        pathologies = lung_analyzer.get_pathologies()

        return jsonify({
            'success': True,
            'pathologies': pathologies,
            'count': len(pathologies)
        })

    except Exception as e:
        return jsonify({
            'error': 'Failed to retrieve pathologies',
            'message': str(e)
        }), 500

@api_v1.route('/analyze', methods=['POST'])
@limiter.limit("10 per minute")
def analyze_lung_scan():
    """
    Analyze lung X-ray image (including .dcm) for pathologies.

    Expects:
        - Image file in multipart form data with key 'image'
        - Accepted formats: png, jpg, jpeg, bmp, gif, tiff, dcm (DICOM)

    Returns:
        JSON response with pathology predictions and model metadata.
    """
    try:
        # Check if image file is present
        if 'image' not in request.files:
            return jsonify({
                'error': 'No image file provided',
                'message': 'Please upload an image file with key "image"'
            }), 400

        file = request.files['image']

        # Check if file is empty
        if file.filename == '':
            return jsonify({
                'error': 'No image file selected',
                'message': 'Please select an image file to upload'
            }), 400

        # Validate file type
        allowed_extensions = {'png', 'jpg', 'jpeg', 'gif', 'bmp', 'tiff', 'dcm'}
        if not _allowed_file(file.filename, allowed_extensions):
            return jsonify({
                'error': 'Invalid file type',
                'message': f'Allowed file types: {", ".join(allowed_extensions)}'
            }), 400

        extension = os.path.splitext(file.filename)[1].lower()

        if extension == '.dcm':
            try:
                dicom_data = pydicom.dcmread(file)
                image_array = dicom_data.pixel_array.astype(np.float32)
                image_array -= np.min(image_array)
                image_array /= np.max(image_array)
                image_array *= 255.0
                image_array = image_array.astype(np.uint8)
                image_data = image_array
            except Exception as e:
                return jsonify({
                    'error': 'DICOM processing error',
                    'message': str(e)
                }), 400
        else:
            image_data = file.read()

        # Get the lung analyzer from app context
        lung_analyzer = current_app.lung_analyzer

        # Analyze the image
        results = lung_analyzer.analyze(image_data)

        # Return results
        return jsonify({
            'success': True,
            'predictions': results,
            'pathologies_detected': _get_significant_pathologies(results),
            'model_info': {
                'model_name': lung_analyzer.model_name,
                'total_pathologies': len(results)
            }
        })

    except ValueError as e:
        return jsonify({
            'error': 'Image processing error',
            'message': str(e)
        }), 400

    except RuntimeError as e:
        return jsonify({
            'error': 'Model inference error',
            'message': str(e)
        }), 500

    except Exception as e:
        # Log the full traceback for debugging
        current_app.logger.error(f"Unexpected error in analyze_lung_scan: {traceback.format_exc()}")
        return jsonify({
            'error': 'Internal server error',
            'message': 'An unexpected error occurred during image analysis'
        }), 500

@api_v1.route('/random-image', methods=['GET'])
def get_random_image():
    try:
        current_file = os.path.abspath(__file__)
        project_root = os.path.dirname(os.path.dirname(os.path.dirname(current_file)))
        images_folder = os.path.join(project_root, 'images')
        
        if not os.path.exists(images_folder):
            return jsonify({'error': f'Images folder not found at: {images_folder}'}), 404
        
        supported_extensions = {'.png', '.jpg', '.jpeg', '.gif', '.bmp', '.webp', 'dcm'}
        
        image_files = [
            f for f in os.listdir(images_folder) 
            if os.path.splitext(f)[1].lower() in supported_extensions
        ]
        
        if not image_files:
            return jsonify({'error': 'No images available'}), 404

        random_image = random.choice(image_files)
        image_path = os.path.join(images_folder, random_image)
        
        ext = os.path.splitext(random_image)[1].lower()
        mimetype = {
            '.png': 'image/png',
            '.jpg': 'image/jpeg',
            '.jpeg': 'image/jpeg',
            '.gif': 'image/gif',
            '.bmp': 'image/bmp',
            '.webp': 'image/webp',
            '.dcm': 'application/dicom'
        }.get(ext, 'application/octet-stream')

        return send_file(image_path, mimetype=mimetype, as_attachment=False)

    except Exception as e:
        return jsonify({'error': str(e)}), 500

def _allowed_file(filename: str, allowed_extensions: set) -> bool:
    """Check if file has allowed extension."""
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in allowed_extensions


def _get_significant_pathologies(results: Dict[str, float], threshold: float = 0.5) -> Dict[str, float]:
    """
    Filter pathologies with confidence scores above threshold.

    Args:
        results: Dictionary of pathology predictions
        threshold: Minimum confidence threshold

    Returns:
        Dictionary of significant pathologies
    """
    return {k: v for k, v in results.items() if v >= threshold}