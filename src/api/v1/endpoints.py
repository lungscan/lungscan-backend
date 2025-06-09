import datetime

from flask import jsonify

from . import api_v1

@api_v1.route("/health")
def health():
    """Health check endpoint."""
    return jsonify(
        {
            "status": "healthy",
            "timestamp": datetime.datetime.utcnow().replace(microsecond=0).isoformat() + "Z",
        }
    )

@api_v1.route("/pathologies")
def get_pathologies():
    """Returns the list of supported pathologies."""
    pathologies = [
        "Atelectasis", "Cardiomegaly", "Effusion", "Infiltration", "Mass",
        "Nodule", "Pneumonia", "Pneumothorax", "Consolidation", "Edema",
        "Emphysema", "Fibrosis", "Pleural Thickening", "Hernia"
    ]
    return jsonify({"pathologies": pathologies})