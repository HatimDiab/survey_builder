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

@app.route('/objectives')
def objectives():
    """Objectives selection page (formerly category)"""
    return render_template('objectives.html')

@app.route('/question')
def question():
    """Question builder page"""
    return render_template('question.html')

@app.route('/review')
def review():
    """Review and export page"""
    return render_template('review.html')

# API endpoints for Data Vault backend integration

@app.route('/api/save-objectives', methods=['POST'])
def save_objectives():
    """API endpoint for saving objectives"""
    try:
        data = request.get_json()
        # Forward to backend API
        response = requests.post(f"{BACKEND_URL}/api/save-objectives", json=data, timeout=10)
        return jsonify(response.json()), response.status_code
    except requests.RequestException as e:
        return jsonify({'status': 'error', 'message': f'Backend connection failed: {str(e)}'}), 500

@app.route('/api/save-customization', methods=['POST'])
def save_customization():
    """API endpoint for saving client customization"""
    try:
        data = request.get_json()
        # Forward to backend API
        response = requests.post(f"{BACKEND_URL}/api/save-customization", json=data, timeout=10)
        return jsonify(response.json()), response.status_code
    except requests.RequestException as e:
        return jsonify({'status': 'error', 'message': f'Backend connection failed: {str(e)}'}), 500

@app.route('/api/save-questions', methods=['POST'])
def save_questions():
    """API endpoint for saving questions"""
    try:
        data = request.get_json()
        # Forward to backend API
        response = requests.post(f"{BACKEND_URL}/api/save-questions", json=data, timeout=10)
        return jsonify(response.json()), response.status_code
    except requests.RequestException as e:
        return jsonify({'status': 'error', 'message': f'Backend connection failed: {str(e)}'}), 500

@app.route('/api/survey-data/<company_name>/<survey_title>')
def get_survey_data(company_name, survey_title):
    """API endpoint for retrieving survey data"""
    try:
        # Forward to backend API
        response = requests.get(f"{BACKEND_URL}/api/survey-data/{company_name}/{survey_title}", timeout=10)
        return jsonify(response.json()), response.status_code
    except requests.RequestException as e:
        return jsonify({'status': 'error', 'message': f'Backend connection failed: {str(e)}'}), 500

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