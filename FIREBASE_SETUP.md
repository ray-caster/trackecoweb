# Firebase Setup Guide for TrackEco Admin

## 🔥 Step-by-Step Firebase Configuration

### 1. Create Firebase Project

1. Go to [Firebase Console](https://console.firebase.google.com/)
2. Click "Add project"
3. Enter project name: `trackeco-admin`
4. Follow the setup wizard

### 2. Enable Firestore Database

1. In Firebase Console, go to "Build" → "Firestore Database"
2. Click "Create database"
3. Choose "Start in production mode"
4. Select your region (closest to Surabaya: `asia-southeast1`)
5. Click "Enable"

### 3. Set Up Firestore Security Rules

In Firestore Database → Rules tab, add:

```javascript
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    // News collection - read public, write admin only
    match /news/{newsId} {
      allow read: if true;
      allow write: if request.auth != null;
    }
  }
}
```

### 4. Get Service Account Key

1. Go to Project Settings (⚙️ icon) → "Service accounts"
2. Click "Generate new private key"
3. Click "Generate key"
4. Save the downloaded JSON file as `firebase-credentials.json` in your project root

**Important:** Add `firebase-credentials.json` to `.gitignore`!

### 5. Configure Environment Variables

1. Copy `.env.example` to `.env`:
   ```bash
   cp .env.example .env
   ```

2. Edit `.env` and set:
   ```env
   SECRET_KEY=your-random-secret-key-here
   ADMIN_USERNAME=admin
   ADMIN_PASSWORD=your-secure-password-here
   FIREBASE_CREDENTIALS_PATH=firebase-credentials.json
   ```

### 6. Install Dependencies

```bash
pip install -r requirements.txt
```

### 7. Run the Application

```bash
python main.py
```

## 🔐 Admin Access

### Login Credentials

- **URL:** `http://localhost:5000/admin/login`
- **Username:** Set in `.env` (default: `admin`)
- **Password:** Set in `.env` (default: change this!)

### Admin Routes

- `/admin/login` - Login page
- `/admin` - Dashboard (requires login)
- `/admin/news/add` - Add new article
- `/admin/news/edit/<id>` - Edit article
- `/admin/logout` - Logout

## 📊 Firestore Data Structure

### News Collection (`news`)

```json
{
  "title_en": "Article Title in English",
  "title_id": "Judul Artikel dalam Bahasa Indonesia",
  "description_en": "Article description in English...",
  "description_id": "Deskripsi artikel dalam Bahasa Indonesia...",
  "category": "partnership|event|impact|innovation",
  "image_url": "/static/images/background3.webp",
  "published": true,
  "created_at": "2024-10-11T10:30:00",
  "updated_at": "2024-10-11T10:30:00"
}
```

## 🛡️ Security Best Practices

1. **Change Default Password**
   - Update `ADMIN_PASSWORD` in `.env` immediately
   - Use a strong password (16+ characters)

2. **Secret Key**
   - Generate a secure random key:
     ```python
     import secrets
     print(secrets.token_hex(32))
     ```
   - Update `SECRET_KEY` in `.env`

3. **Firebase Credentials**
   - Never commit `firebase-credentials.json`
   - Add to `.gitignore`
   - Use environment-specific credentials for production

4. **Production Deployment**
   - Use environment variables instead of `.env` file
   - Enable HTTPS
   - Set up proper authentication (OAuth, etc.)

## 🎨 Categories

Available news categories:
- **partnership** - Partnership announcements
- **event** - Events and activities
- **impact** - Impact reports and achievements
- **innovation** - New technologies and innovations

## 📝 Usage Example

### Adding News via Admin Panel

1. Login at `/admin/login`
2. Click "Add New Article"
3. Fill in both English and Indonesian content
4. Select category
5. Add image URL (use existing images or upload new ones)
6. Check "Publish immediately" or save as draft
7. Click "Save Article"

### News Appears On

- Homepage (latest news preview)
- `/news` page (all published news)
- API endpoint `/api/news` (JSON format)

## 🔧 Troubleshooting

### "Firebase credentials file not found"
- Ensure `firebase-credentials.json` exists in project root
- Check `FIREBASE_CREDENTIALS_PATH` in `.env`

### "Login not working"
- Check username/password in `.env`
- Ensure SECRET_KEY is set
- Clear browser cookies/cache

### "No news showing"
- Check if articles are published (checkbox)
- Check Firestore security rules
- Verify Firebase is initialized

## 🚀 Next Steps

1. Set up Firebase credentials
2. Change admin password
3. Add your first news article
4. Test on news page
5. Deploy to production

## 📚 Additional Resources

- [Firebase Documentation](https://firebase.google.com/docs)
- [Firestore Guide](https://firebase.google.com/docs/firestore)
- [Flask-Login Documentation](https://flask-login.readthedocs.io/)

---

**Status:** Ready to use  
**Version:** 1.0  
**Last Updated:** October 11, 2024

