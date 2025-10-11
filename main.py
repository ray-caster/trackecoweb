from flask import Flask, render_template, request, jsonify, send_from_directory, redirect, url_for, flash, session
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename
from dotenv import load_dotenv
from datetime import datetime
import os
import uuid

# Load environment variables
load_dotenv()

# Import Firebase configuration
try:
    from firebase_config import (
        initialize_firebase, 
        add_news_article, 
        get_all_news, 
        get_news_by_id,
        update_news_article,
        delete_news_article,
        get_published_news,
        update_news_order
    )
    FIREBASE_AVAILABLE = True
    # Initialize Firebase on startup
    initialize_firebase()
except Exception as e:
    print(f"Firebase not available: {e}")
    FIREBASE_AVAILABLE = False

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'change-this-to-something-secret')

# Upload configuration
UPLOAD_FOLDER = 'static/images/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Create upload directory if it doesn't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Flask-Login setup
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'admin_login'

# Simple User class for admin
class User(UserMixin):
    def __init__(self, id):
        self.id = id

@login_manager.user_loader
def load_user(user_id):
    if user_id == 'admin':
        return User(user_id)
    return None

# Public routes
@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')
                               
@app.route("/")
def index():
    # Get latest 5 news for carousel
    if FIREBASE_AVAILABLE:
        latest_news = get_published_news(limit=5)
    else:
        latest_news = []
    return render_template("index.html", latest_news=latest_news)

@app.route("/news")
def news():
    if FIREBASE_AVAILABLE:
        news_articles = get_published_news()
    else:
        news_articles = []
    return render_template("news.html", news_articles=news_articles)

@app.route("/timeline")
def timeline():
    return render_template("timeline.html")

@app.route("/calculator")
def calculator():
    return render_template("calculator.html")

# Admin routes
@app.route("/admin/login", methods=['GET', 'POST'])
def admin_login():
    if current_user.is_authenticated:
        return redirect(url_for('admin_dashboard'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        admin_username = os.getenv('ADMIN_USERNAME', 'admin')
        admin_password = os.getenv('ADMIN_PASSWORD', 'admin123')
        
        if username == admin_username and password == admin_password:
            user = User('admin')
            login_user(user)
            flash('Login successful!', 'success')
            return redirect(url_for('admin_dashboard'))
        else:
            flash('Invalid credentials. Please try again.', 'error')
    
    return render_template("admin/login.html")

@app.route("/admin/logout")
@login_required
def admin_logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('admin_login'))

@app.route("/admin")
@login_required
def admin_dashboard():
    if not FIREBASE_AVAILABLE:
        flash('Firebase is not configured. Please set up Firebase credentials.', 'error')
    
    news_articles = get_all_news() if FIREBASE_AVAILABLE else []
    return render_template("admin/dashboard.html", news_articles=news_articles)

@app.route("/admin/news/add", methods=['GET', 'POST'])
@login_required
def admin_add_news():
    if request.method == 'POST':
        if not FIREBASE_AVAILABLE:
            flash('Firebase is not configured.', 'error')
            return redirect(url_for('admin_dashboard'))
        
        # Handle image upload
        image_url = request.form.get('image_url', '/static/images/background3.webp')
        if 'image_file' in request.files:
            file = request.files['image_file']
            if file and file.filename and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                unique_filename = f"{uuid.uuid4().hex}_{filename}"
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
                file.save(filepath)
                image_url = f'/static/images/uploads/{unique_filename}'
        
        news_data = {
            'title_en': request.form.get('title_en'),
            'title_id': request.form.get('title_id'),
            'description_en': request.form.get('description_en'),
            'description_id': request.form.get('description_id'),
            'category': request.form.get('category'),
            'image_url': image_url,
            'published': request.form.get('published') == 'on',
            'order': int(request.form.get('order', 999)),
            'created_at': datetime.now(),
            'updated_at': datetime.now()
        }
        
        news_id = add_news_article(news_data)
        if news_id:
            flash('News article added successfully!', 'success')
            return redirect(url_for('admin_dashboard'))
        else:
            flash('Failed to add news article.', 'error')
    
    return render_template("admin/add_news.html")

@app.route("/admin/news/edit/<news_id>", methods=['GET', 'POST'])
@login_required
def admin_edit_news(news_id):
    if not FIREBASE_AVAILABLE:
        flash('Firebase is not configured.', 'error')
        return redirect(url_for('admin_dashboard'))
    
    if request.method == 'POST':
        # Handle image upload
        image_url = request.form.get('image_url')
        if 'image_file' in request.files:
            file = request.files['image_file']
            if file and file.filename and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                unique_filename = f"{uuid.uuid4().hex}_{filename}"
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
                file.save(filepath)
                image_url = f'/static/images/uploads/{unique_filename}'
        
        news_data = {
            'title_en': request.form.get('title_en'),
            'title_id': request.form.get('title_id'),
            'description_en': request.form.get('description_en'),
            'description_id': request.form.get('description_id'),
            'category': request.form.get('category'),
            'image_url': image_url,
            'published': request.form.get('published') == 'on',
            'order': int(request.form.get('order', 999)),
            'updated_at': datetime.now()
        }
        
        if update_news_article(news_id, news_data):
            flash('News article updated successfully!', 'success')
            return redirect(url_for('admin_dashboard'))
        else:
            flash('Failed to update news article.', 'error')
    
    news_article = get_news_by_id(news_id)
    if not news_article:
        flash('News article not found.', 'error')
        return redirect(url_for('admin_dashboard'))
    
    return render_template("admin/edit_news.html", news=news_article)

@app.route("/admin/news/delete/<news_id>", methods=['POST'])
@login_required
def admin_delete_news(news_id):
    if not FIREBASE_AVAILABLE:
        flash('Firebase is not configured.', 'error')
        return redirect(url_for('admin_dashboard'))
    
    if delete_news_article(news_id):
        flash('News article deleted successfully!', 'success')
    else:
        flash('Failed to delete news article.', 'error')
    
    return redirect(url_for('admin_dashboard'))

# API endpoint for getting news (for frontend)
@app.route("/api/news")
def api_get_news():
    if not FIREBASE_AVAILABLE:
        return jsonify([])
    
    news_articles = get_published_news()
    return jsonify(news_articles)

# Debug route to check news status
@app.route("/debug/news")
def debug_news():
    debug_info = {
        "firebase_available": FIREBASE_AVAILABLE,
        "published_news": get_published_news() if FIREBASE_AVAILABLE else "Firebase not available",
        "all_news": get_all_news() if FIREBASE_AVAILABLE else "Firebase not available"
    }
    return jsonify(debug_info)

@app.route("/api/news/reorder", methods=['POST'])
@login_required
def api_reorder_news():
    if not FIREBASE_AVAILABLE:
        return jsonify({'success': False, 'message': 'Firebase not configured'})
    
    data = request.get_json()
    news_order = data.get('order', [])
    
    try:
        for index, news_id in enumerate(news_order):
            update_news_order(news_id, index)
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)