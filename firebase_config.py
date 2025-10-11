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
        news_ref = db.collection('news').order_by('created_at', direction=firestore.Query.DESCENDING)
        docs = news_ref.stream()
        
        news_list = []
        for doc in docs:
            news_data = doc.to_dict()
            news_data['id'] = doc.id
            # Ensure order field exists
            if 'order' not in news_data:
                news_data['order'] = 999
            news_list.append(news_data)
        
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

