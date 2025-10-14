"""
Firebase Configuration and Initialization
"""
import firebase_admin
from firebase_admin import credentials, firestore
import os
from dotenv import load_dotenv

load_dotenv()

# Initialize Firebase Admin SDK
def initialize_firebase():
    """Initialize Firebase Admin SDK if not already initialized"""
    if not firebase_admin._apps:
        # Get credentials path from environment variable
        cred_path = os.getenv('FIREBASE_CREDENTIALS_PATH', 'firebase-credentials.json')
        
        # Check if credentials file exists
        if not os.path.exists(cred_path):
            print(f"Warning: Firebase credentials file not found at {cred_path}")
            print("Please download your Firebase service account key and save it as firebase-credentials.json")
            return None
        
        try:
            cred = credentials.Certificate(cred_path)
            firebase_admin.initialize_app(cred)
            print("Firebase initialized successfully!")
            return firestore.client()
        except Exception as e:
            print(f"Error initializing Firebase: {e}")
            return None
    else:
        return firestore.client()

# Get Firestore client
def get_firestore_client():
    """Get or create Firestore client"""
    try:
        return firestore.client()
    except:
        return initialize_firebase()

# News collection helpers
def add_news_article(data):
    """Add a new news article to Firestore"""
    db = get_firestore_client()
    if not db:
        return None
    
    try:
        # Ensure order field exists
        if 'order' not in data:
            data['order'] = 999
        
        doc_ref = db.collection('news').document()
        doc_ref.set(data)
        return doc_ref.id
    except Exception as e:
        print(f"Error adding news article: {e}")
        return None

def get_all_news():
    """Get all news articles from Firestore"""
    db = get_firestore_client()
    if not db:
        return []
    
    try:
        # Get all news articles first, then sort by order in Python
        news_ref = db.collection('news')
        docs = news_ref.stream()
        
        news_list = []
        for doc in docs:
            news_data = doc.to_dict()
            news_data['id'] = doc.id
            # Ensure order field exists
            if 'order' not in news_data:
                news_data['order'] = 999
            news_list.append(news_data)
        
        # Sort by order field (lower numbers first)
        news_list.sort(key=lambda x: x.get('order', 999))
        
        return news_list
    except Exception as e:
        print(f"Error getting all news: {e}")
        return []

def get_news_by_id(news_id):
    """Get a specific news article by ID"""
    db = get_firestore_client()
    if not db:
        return None
    
    try:
        doc_ref = db.collection('news').document(news_id)
        doc = doc_ref.get()
        
        if doc.exists:
            news_data = doc.to_dict()
            news_data['id'] = doc.id
            # Ensure order field exists
            if 'order' not in news_data:
                news_data['order'] = 999
            return news_data
        return None
    except Exception as e:
        print(f"Error getting news by ID: {e}")
        return None

def update_news_article(news_id, data):
    """Update a news article"""
    db = get_firestore_client()
    if not db:
        return False
    
    try:
        doc_ref = db.collection('news').document(news_id)
        doc_ref.update(data)
        return True
    except Exception as e:
        print(f"Error updating news article: {e}")
        return False

def delete_news_article(news_id):
    """Delete a news article"""
    db = get_firestore_client()
    if not db:
        return False
    
    try:
        db.collection('news').document(news_id).delete()
        return True
    except Exception as e:
        print(f"Error deleting news article: {e}")
        return False

def get_published_news(limit=None):
    """Get only published news articles"""
    db = get_firestore_client()
    if not db:
        # Return empty list so template knows there's no data
        return []
    
    try:
        # First get all published articles, then sort in Python
        query = db.collection('news').where(filter=firestore.FieldFilter('published', '==', True))
        
        docs = query.stream()
        
        news_list = []
        for doc in docs:
            news_data = doc.to_dict()
            news_data['id'] = doc.id
            # Ensure order field exists
            if 'order' not in news_data:
                news_data['order'] = 999
            news_list.append(news_data)
        
        # Sort by order field in Python
        news_list.sort(key=lambda x: x.get('order', 999))
        
        if limit:
            news_list = news_list[:limit]
        
        return news_list
    except Exception as e:
        print(f"Error getting published news: {e}")
        return []

def update_news_order(news_id, new_order):
    """Update the order of a news article"""
    db = get_firestore_client()
    if not db:
        return False
    
    try:
        doc_ref = db.collection('news').document(news_id)
        doc_ref.update({'order': new_order})
        return True
    except Exception as e:
        print(f"Error updating news order: {e}")
        return False

# Category Management Functions
def get_categories():
    """Get all categories"""
    db = get_firestore_client()
    if not db:
        return []
    
    try:
        docs = db.collection('categories').stream()
        categories = []
        for doc in docs:
            category_data = doc.to_dict()
            category_data['id'] = doc.id
            categories.append(category_data)
        return categories
    except Exception as e:
        print(f"Error getting categories: {e}")
        return []

def add_category(category_data):
    """Add a new category"""
    db = get_firestore_client()
    if not db:
        return False
    
    try:
        doc_ref = db.collection('categories').add(category_data)
        return doc_ref[1].id
    except Exception as e:
        print(f"Error adding category: {e}")
        return False

def update_category(category_id, category_data):
    """Update a category"""
    db = get_firestore_client()
    if not db:
        return False
    
    try:
        doc_ref = db.collection('categories').document(category_id)
        doc_ref.update(category_data)
        return True
    except Exception as e:
        print(f"Error updating category: {e}")
        return False

def delete_category(category_id):
    """Delete a category"""
    db = get_firestore_client()
    if not db:
        return False
    
    try:
        doc_ref = db.collection('categories').document(category_id)
        doc_ref.delete()
        return True
    except Exception as e:
        print(f"Error deleting category: {e}")
        return False

# Website Data Management Functions
def get_website_data():
    """Get website data and statistics"""
    db = get_firestore_client()
    if not db:
        return {}
    
    try:
        doc = db.collection('website_data').document('main').get()
        if doc.exists:
            return doc.to_dict()
        else:
            # Return default data
            return {
                'hero_title_en': 'TrackEco - Plastic Waste Management',
                'hero_title_id': 'TrackEco - Pengelolaan Sampah Plastik',
                'hero_subtitle_en': 'Transforming plastic waste into valuable resources',
                'hero_subtitle_id': 'Mengubah sampah plastik menjadi sumber daya berharga',
                'stats': {
                    'plastic_collected': 5000,
                    'communities_reached': 25,
                    'recycling_rate': 85,
                    'co2_reduced': 1200,
                    'member_count': 74,
                    'bottles_collected': 35000,
                    'sme_partners': 8,
                    'impact_plastic_collected': 3000,
                    'volunteers_cleanup': 100,
                    'plastic_cleanup_kg': 500,
                    'co2_emissions_prevented': 42,
                    'ocean_plastic_prevented': 2000,
                    'craft_support_percentage': 85,
                    'people_educated': 500
                },
                'mission_title_en': 'Our Mission',
                'mission_title_id': 'Misi Kami',
                'mission_text_en': 'To create a sustainable future by transforming plastic waste into valuable resources.',
                'mission_text_id': 'Menciptakan masa depan yang berkelanjutan dengan mengubah sampah plastik menjadi sumber daya berharga.'
            }
    except Exception as e:
        print(f"Error getting website data: {e}")
        return {}

def update_website_data(data):
    """Update website data"""
    db = get_firestore_client()
    if not db:
        return False
    
    try:
        doc_ref = db.collection('website_data').document('main')
        doc_ref.set(data, merge=True)
        return True
    except Exception as e:
        print(f"Error updating website data: {e}")
        return False

