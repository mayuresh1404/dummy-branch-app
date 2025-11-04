from flask import Blueprint, jsonify

bp = Blueprint('health', __name__)

@bp.route('/health')
def health():
    return jsonify({"status": "ok"})

# Add this root route
@bp.route('/')
def index():
    return jsonify({
        "message": "Welcome to Branch Loans API",
        "endpoints": {
            "health": "/health",
            "loans": "/api/loans",
            "stats": "/api/stats"
        }
    })
