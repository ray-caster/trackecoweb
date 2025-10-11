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
    categories = get_categories() if FIREBASE_AVAILABLE else []
    return render_template("admin/dashboard.html", news_articles=news_articles, categories=categories)

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
        
        # Handle publish date
        publish_date_str = request.form.get('publish_date')
        publish_date = None
        if publish_date_str:
            try:
                publish_date = datetime.fromisoformat(publish_date_str.replace('T', ' '))
            except:
                publish_date = datetime.now()
        else:
            publish_date = datetime.now()

        news_data = {
            'title_en': request.form.get('title_en'),
            'title_id': request.form.get('title_id'),
            'description_en': request.form.get('description_en'),
            'description_id': request.form.get('description_id'),
            'category': request.form.get('category'),
            'image_url': image_url,
            'published': request.form.get('published') == 'on',
            'featured': request.form.get('featured') == 'on',
            'publish_date': publish_date,
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
    
    categories = get_categories() if FIREBASE_AVAILABLE else []
    current_date = datetime.now().strftime('%Y-%m-%dT%H:%M')
    return render_template("admin/add_news.html", categories=categories, current_date=current_date)

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
        
        # Handle publish date
        publish_date_str = request.form.get('publish_date')
        publish_date = None
        if publish_date_str:
            try:
                publish_date = datetime.fromisoformat(publish_date_str.replace('T', ' '))
            except:
                publish_date = news.publish_date if hasattr(news, 'publish_date') else datetime.now()
        else:
            publish_date = news.publish_date if hasattr(news, 'publish_date') else datetime.now()

        news_data = {
            'title_en': request.form.get('title_en'),
            'title_id': request.form.get('title_id'),
            'description_en': request.form.get('description_en'),
            'description_id': request.form.get('description_id'),
            'category': request.form.get('category'),
            'image_url': image_url,
            'published': request.form.get('published') == 'on',
            'featured': request.form.get('featured') == 'on',
            'publish_date': publish_date,
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

@app.route("/api/news/featured", methods=['POST'])
@login_required
def api_toggle_featured():
    if not FIREBASE_AVAILABLE:
        return jsonify({'success': False, 'message': 'Firebase not configured'})
    
    data = request.get_json()
    news_id = data.get('news_id')
    featured = data.get('featured', False)
    
    try:
        db = get_firestore_client()
        if not db:
            return jsonify({'success': False, 'message': 'Database not available'})
        
        doc_ref = db.collection('news').document(news_id)
        doc_ref.update({'featured': featured})
        
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

# Category Management Routes
@app.route("/admin/categories")
@login_required
def admin_categories():
    if not FIREBASE_AVAILABLE:
        flash('Firebase is not configured.', 'error')
        return render_template("admin/categories.html", categories=[])
    
    categories = get_categories()
    return render_template("admin/categories.html", categories=categories)

@app.route("/admin/categories/add", methods=['POST'])
@login_required
def admin_add_category():
    if not FIREBASE_AVAILABLE:
        return jsonify({'success': False, 'message': 'Firebase not configured'})
    
    category_data = {
        'name': request.form.get('name'),
        'color': request.form.get('color'),
        'description': request.form.get('description', ''),
        'created_at': datetime.now()
    }
    
    category_id = add_category(category_data)
    if category_id:
        flash('Category added successfully!', 'success')
        return redirect(url_for('admin_categories'))
    else:
        flash('Failed to add category.', 'error')
        return redirect(url_for('admin_categories'))

@app.route("/admin/categories/edit/<category_id>", methods=['POST'])
@login_required
def admin_edit_category(category_id):
    if not FIREBASE_AVAILABLE:
        return jsonify({'success': False, 'message': 'Firebase not configured'})
    
    category_data = {
        'name': request.form.get('name'),
        'color': request.form.get('color'),
        'description': request.form.get('description', ''),
        'updated_at': datetime.now()
    }
    
    if update_category(category_id, category_data):
        flash('Category updated successfully!', 'success')
    else:
        flash('Failed to update category.', 'error')
    
    return redirect(url_for('admin_categories'))

@app.route("/admin/categories/delete/<category_id>", methods=['POST'])
@login_required
def admin_delete_category(category_id):
    if not FIREBASE_AVAILABLE:
        return jsonify({'success': False, 'message': 'Firebase not configured'})
    
    if delete_category(category_id):
        flash('Category deleted successfully!', 'success')
    else:
        flash('Failed to delete category.', 'error')
    
    return redirect(url_for('admin_categories'))

# Website Data Management Routes
@app.route("/admin/website-data")
@login_required
def admin_website_data():
    if not FIREBASE_AVAILABLE:
        flash('Firebase is not configured.', 'error')
        return render_template("admin/website_data.html", website_data={})
    
    website_data = get_website_data()
    return render_template("admin/website_data.html", website_data=website_data)

@app.route("/admin/website-data/update", methods=['POST'])
@login_required
def admin_update_website_data():
    if not FIREBASE_AVAILABLE:
        flash('Firebase is not configured.', 'error')
        return redirect(url_for('admin_website_data'))
    
    website_data = {
        'hero_title_en': request.form.get('hero_title_en'),
        'hero_title_id': request.form.get('hero_title_id'),
        'hero_subtitle_en': request.form.get('hero_subtitle_en'),
        'hero_subtitle_id': request.form.get('hero_subtitle_id'),
        'stats': {
            'plastic_collected': int(request.form.get('plastic_collected', 0)),
            'communities_reached': int(request.form.get('communities_reached', 0)),
            'recycling_rate': int(request.form.get('recycling_rate', 0)),
            'co2_reduced': int(request.form.get('co2_reduced', 0))
        },
        'mission_title_en': request.form.get('mission_title_en'),
        'mission_title_id': request.form.get('mission_title_id'),
        'mission_text_en': request.form.get('mission_text_en'),
        'mission_text_id': request.form.get('mission_text_id'),
        'updated_at': datetime.now()
    }
    
    if update_website_data(website_data):
        flash('Website data updated successfully!', 'success')
    else:
        flash('Failed to update website data.', 'error')
    
    return redirect(url_for('admin_website_data'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)