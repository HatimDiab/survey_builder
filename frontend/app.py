from flask import Flask, render_template, request, jsonify, redirect, url_for
import os
import requests

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'dev-secret-key')

# Backend API URL
BACKEND_URL = os.environ.get('BACKEND_URL', 'http://backend:8000')

@app.route('/')
def splash():
    """Splash page - welcome screen"""
    return render_template('splash.html')

@app.route('/white-label')
def white_label():
    """White label configuration page"""
    return render_template('white_label.html')

@app.route('/category')
def category():
    """Category selection page"""
    return render_template('category.html')

@app.route('/question')
def question():
    """Question builder page"""
    return render_template('question.html')

@app.route('/review')
def review():
    """Review and export page"""
    return render_template('review.html')

@app.route('/api/export', methods=['POST'])
def export_survey():
    """API endpoint for exporting survey data"""
    try:
        data = request.get_json()
        # Forward to backend API
        response = requests.post(f"{BACKEND_URL}/api/export", json=data, timeout=10)
        return jsonify(response.json()), response.status_code
    except requests.RequestException as e:
        return jsonify({'status': 'error', 'message': f'Backend connection failed: {str(e)}'}), 500

@app.route('/api/save-progress', methods=['POST'])
def save_progress():
    """API endpoint for saving survey progress"""
    try:
        data = request.get_json()
        # Forward to backend API
        response = requests.post(f"{BACKEND_URL}/api/save-progress", json=data, timeout=10)
        return jsonify(response.json()), response.status_code
    except requests.RequestException as e:
        return jsonify({'status': 'error', 'message': f'Backend connection failed: {str(e)}'}), 500

@app.route('/health')
def health_check():
    """Health check endpoint"""
    try:
        # Check backend health
        backend_health = requests.get(f"{BACKEND_URL}/health", timeout=5)
        backend_status = "healthy" if backend_health.status_code == 200 else "unhealthy"
    except:
        backend_status = "unreachable"
    
    return jsonify({
        'frontend': 'healthy',
        'backend': backend_status
    })

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=3000) 