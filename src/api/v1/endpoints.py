import datetime

from flask import jsonify, current_app

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
