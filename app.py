from flask import Flask, render_template, request, jsonify, redirect, url_for, flash, session, send_from_directory
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import os
import json
import datetime
from functools import wraps

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-change-this-in-production'
app.config['UPLOAD_FOLDER'] = 'newsletters'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'admin_login'

# Simple user model for admin
class User(UserMixin):
    def __init__(self, id):
        self.id = id

@login_manager.user_loader
def load_user(user_id):
    return User(user_id)

# Admin credentials (in production, use a database)
ADMIN_USERNAME = 'Brilliance'
ADMIN_PASSWORD_HASH = generate_password_hash('Heisenb3rg@1')

# In-memory storage for Vercel (in production, use a database)
NEWSLETTERS_DATA = [
    {
        'id': 1,
        'title': 'Getting Started with AI',
        'description': 'An introduction to artificial intelligence and machine learning concepts.',
        'date': '2025-01-01',
        'filename': 'sample_1.pdf',
        'downloads': 0,
        'uploaded_at': '2025-01-01T00:00:00',
        'preview_image': 'preview_1.jpg'
    },
    {
        'id': 2,
        'title': 'Cloud Computing Fundamentals',
        'description': 'Understanding cloud computing, its benefits, and implementation strategies.',
        'date': '2025-01-15',
        'filename': 'sample_2.pdf',
        'downloads': 0,
        'uploaded_at': '2025-01-15T00:00:00',
        'preview_image': 'preview_2.jpg'
    }
]

def load_newsletters():
    """Load newsletters from memory"""
    return NEWSLETTERS_DATA

def save_newsletters(newsletters):
    """Save newsletters to memory"""
    global NEWSLETTERS_DATA
    NEWSLETTERS_DATA = newsletters

def allowed_file(filename, file_type='pdf'):
    """Check if file extension is allowed"""
    if file_type == 'pdf':
        return '.' in filename and filename.rsplit('.', 1)[1].lower() == 'pdf'
    elif file_type == 'image':
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg', 'gif', 'webp'}
    return False

# Routes
@app.route('/')
def index():
    """Main homepage"""
    return send_from_directory('.', 'index.html')

@app.route('/styles.css')
def styles():
    """Serve CSS file"""
    return send_from_directory('.', 'styles.css')

@app.route('/script.js')
def script():
    """Serve JavaScript file"""
    return send_from_directory('.', 'script.js')

@app.route('/newsletters/<filename>')
def serve_newsletter(filename):
    """Serve newsletter PDF files"""
    # For Vercel, we'll return a placeholder since file storage isn't available
    return jsonify({'error': 'File storage not available in serverless environment'}), 404

@app.route('/read/<filename>')
def read_newsletter(filename):
    """Read newsletter PDF in browser"""
    # For Vercel, we'll return a placeholder since file storage isn't available
    return jsonify({'error': 'File storage not available in serverless environment'}), 404

@app.route('/api/newsletters')
def api_newsletters():
    """API endpoint to get all newsletters"""
    newsletters = load_newsletters()
    return jsonify(newsletters)

# Admin routes
@app.route('/admin')
@login_required
def admin_dashboard():
    """Admin dashboard"""
    newsletters = load_newsletters()
    return render_template('admin_dashboard.html', newsletters=newsletters)

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    """Admin login page"""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if username == ADMIN_USERNAME and check_password_hash(ADMIN_PASSWORD_HASH, password):
            user = User(username)
            login_user(user)
            flash('Login successful!', 'success')
            return redirect(url_for('admin_dashboard'))
        else:
            flash('Invalid username or password', 'error')
    
    return render_template('admin_login.html')

@app.route('/admin/logout')
@login_required
def admin_logout():
    """Admin logout"""
    logout_user()
    flash('Logged out successfully', 'success')
    return redirect(url_for('admin_login'))

@app.route('/admin/upload', methods=['POST'])
@login_required
def upload_newsletter():
    """Upload new newsletter"""
    try:
        # Get form data
        title = request.form.get('title')
        description = request.form.get('description')
        date = request.form.get('date')
        
        if not all([title, description, date]):
            return jsonify({'error': 'All fields are required'}), 400
        
        # For Vercel, we'll create a newsletter entry without file upload
        newsletters = load_newsletters()
        new_newsletter = {
            'id': len(newsletters) + 1,
            'title': title,
            'description': description,
            'date': date,
            'filename': f'sample_{len(newsletters) + 1}.pdf',
            'downloads': 0,
            'uploaded_at': datetime.datetime.now().isoformat()
        }
        
        newsletters.append(new_newsletter)
        save_newsletters(newsletters)
        
        return jsonify({'success': True, 'newsletter': new_newsletter})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/admin/upload-preview/<int:newsletter_id>', methods=['POST'])
@login_required
def upload_preview_image(newsletter_id):
    """Upload preview image for newsletter"""
    try:
        newsletters = load_newsletters()
        newsletter = next((n for n in newsletters if n['id'] == newsletter_id), None)
        
        if not newsletter:
            return jsonify({'error': 'Newsletter not found'}), 404
        
        # For Vercel, we'll use a placeholder image
        newsletter['preview_image'] = f'preview_{newsletter_id}.jpg'
        save_newsletters(newsletters)
        
        return jsonify({'success': True, 'preview_image': newsletter['preview_image']})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/admin/delete/<int:newsletter_id>', methods=['DELETE'])
@login_required
def delete_newsletter(newsletter_id):
    """Delete a newsletter"""
    try:
        newsletters = load_newsletters()
        newsletter = next((n for n in newsletters if n['id'] == newsletter_id), None)
        
        if not newsletter:
            return jsonify({'error': 'Newsletter not found'}), 404
        
        # Remove from list
        newsletters = [n for n in newsletters if n['id'] != newsletter_id]
        save_newsletters(newsletters)
        
        return jsonify({'success': True})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/admin/edit/<int:newsletter_id>', methods=['PUT'])
@login_required
def edit_newsletter(newsletter_id):
    """Edit newsletter details"""
    try:
        data = request.get_json()
        newsletters = load_newsletters()
        
        newsletter = next((n for n in newsletters if n['id'] == newsletter_id), None)
        if not newsletter:
            return jsonify({'error': 'Newsletter not found'}), 404
        
        # Update fields
        newsletter['title'] = data.get('title', newsletter['title'])
        newsletter['description'] = data.get('description', newsletter['description'])
        newsletter['date'] = data.get('date', newsletter['date'])
        
        save_newsletters(newsletters)
        return jsonify({'success': True, 'newsletter': newsletter})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

# For Vercel deployment
app.debug = False 