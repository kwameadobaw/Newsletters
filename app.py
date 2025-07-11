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

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

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

# Newsletter data file
NEWSLETTERS_FILE = 'newsletters_data.json'

def load_newsletters():
    """Load newsletters from JSON file"""
    if os.path.exists(NEWSLETTERS_FILE):
        with open(NEWSLETTERS_FILE, 'r') as f:
            return json.load(f)
    return []

def save_newsletters(newsletters):
    """Save newsletters to JSON file"""
    with open(NEWSLETTERS_FILE, 'w') as f:
        json.dump(newsletters, f, indent=2)

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
    response = send_from_directory(app.config['UPLOAD_FOLDER'], filename)
    # Set headers to display PDF in browser instead of downloading
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'inline; filename=' + filename
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response

@app.route('/read/<filename>')
def read_newsletter(filename):
    """Read newsletter PDF in browser"""
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    
    if not os.path.exists(file_path):
        return jsonify({'error': 'File not found'}), 404
    
    # Create an HTML page that embeds the PDF
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Reading: {filename}</title>
        <style>
            body {{
                margin: 0;
                padding: 0;
                background: #0f0f23;
                font-family: Arial, sans-serif;
            }}
            .pdf-container {{
                width: 100vw;
                height: 100vh;
                display: flex;
                flex-direction: column;
            }}
            .pdf-header {{
                background: #1a1a2e;
                color: white;
                padding: 1rem;
                border-bottom: 1px solid #2d2d4a;
                display: flex;
                justify-content: space-between;
                align-items: center;
            }}
            .pdf-header h1 {{
                margin: 0;
                font-size: 1.2rem;
            }}
            .pdf-header a {{
                color: #6366f1;
                text-decoration: none;
                padding: 0.5rem 1rem;
                border: 1px solid #6366f1;
                border-radius: 5px;
                transition: all 0.3s ease;
            }}
            .pdf-header a:hover {{
                background: #6366f1;
                color: white;
            }}
            .pdf-viewer {{
                flex: 1;
                width: 100%;
            }}
            .pdf-viewer embed {{
                width: 100%;
                height: 100%;
                border: none;
            }}
        </style>
    </head>
    <body>
        <div class="pdf-container">
            <div class="pdf-header">
                <h1>📄 {filename}</h1>
                <a href="/newsletters/{filename}" download>💾 Download PDF</a>
            </div>
            <div class="pdf-viewer">
                <embed src="/newsletters/{filename}" type="application/pdf" />
            </div>
        </div>
    </body>
    </html>
    """
    
    return html_content

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
        
        # Handle file upload
        if 'pdf_file' not in request.files:
            return jsonify({'error': 'No file uploaded'}), 400
        
        file = request.files['pdf_file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not allowed_file(file.filename, 'pdf'):
            return jsonify({'error': 'Only PDF files are allowed'}), 400
        
        # Generate secure filename
        filename = secure_filename(file.filename)
        timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{timestamp}_{filename}"
        
        # Save file
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        
        # Create newsletter entry
        newsletters = load_newsletters()
        new_newsletter = {
            'id': len(newsletters) + 1,
            'title': title,
            'description': description,
            'date': date,
            'filename': filename,
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
        
        # Handle image upload
        if 'preview_image' not in request.files:
            return jsonify({'error': 'No image uploaded'}), 400
        
        file = request.files['preview_image']
        if file.filename == '':
            return jsonify({'error': 'No image selected'}), 400
        
        if not allowed_file(file.filename, 'image'):
            return jsonify({'error': 'Only image files (PNG, JPG, JPEG, GIF, WEBP) are allowed'}), 400
        
        # Generate secure filename
        filename = secure_filename(file.filename)
        timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"preview_{newsletter_id}_{timestamp}_{filename}"
        
        # Save file
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        
        # Update newsletter with preview image
        newsletter['preview_image'] = filename
        save_newsletters(newsletters)
        
        return jsonify({'success': True, 'preview_image': filename})
    
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
        
        # Delete file
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], newsletter['filename'])
        if os.path.exists(file_path):
            os.remove(file_path)
        
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