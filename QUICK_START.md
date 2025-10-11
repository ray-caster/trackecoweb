# 🚀 Quick Start Guide - TrackEco Admin System

## ⚡ Fast Setup (5 minutes)

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Create `.env` File
Create a file named `.env` in the project root with:
```env
SECRET_KEY=trackeco-secret-key-change-this
ADMIN_USERNAME=admin
ADMIN_PASSWORD=admin123
FIREBASE_CREDENTIALS_PATH=firebase-credentials.json
```

### Step 3: Setup Firebase (Optional - can skip for now)
1. Go to [Firebase Console](https://console.firebase.google.com/)
2. Create a project
3. Enable Firestore
4. Download service account key → save as `firebase-credentials.json`

**OR skip Firebase setup and test locally first!**

### Step 4: Run the Application
```bash
python main.py
```

## 🔑 Access Admin Panel

1. **Login:** http://localhost:5000/admin/login
   - Username: `admin`
   - Password: `admin123`

2. **Add News:** Click "Add New Article" button

3. **View News:** Visit http://localhost:5000/news

## 📝 Adding Your First News Article

1. Login to admin panel
2. Click "Add New Article"
3. Fill in:
   - **Title (English):** "Coastal Cleanup 2024"
   - **Title (Indonesian):** "Aksi Bersih Pantai 2024"
   - **Description (English):** Your content...
   - **Description (Indonesian):** Konten Anda...
   - **Category:** Select one (Partnership, Event, Impact, Innovation)
   - **Image URL:** Use `/static/images/Beach2.webp` or any image from static/images/
   - **Published:** Check to publish immediately

4. Click "Save Article"

## 🎨 Available Images

Use these existing images:
- `/static/images/Beach2.webp`
- `/static/images/Beach1.webp`
- `/static/images/UBS1.webp`
- `/static/images/background3.webp`
- `/static/images/background5.webp`

## 🔐 Security

**Important:** Change the default password!

Edit `.env`:
```env
ADMIN_PASSWORD=your-secure-password-here
```

## 🐛 Troubleshooting

### "Firebase not available"
- It's okay! The system works without Firebase
- News won't persist between restarts
- Set up Firebase later using `FIREBASE_SETUP.md`

### "Login not working"
- Check `.env` file exists
- Verify username/password
- Restart the server

### "ModuleNotFoundError"
- Run `pip install -r requirements.txt`

## 📚 Full Documentation

- **Firebase Setup:** See `FIREBASE_SETUP.md`
- **Recent Changes:** See `RECENT_CHANGES.md`

## 🎯 What You Get

✅ Admin login system  
✅ Add/Edit/Delete news articles  
✅ Bilingual content (English/Indonesian)  
✅ Category management  
✅ Publish/Draft status  
✅ Beautiful admin dashboard  
✅ Firestore integration (optional)  
✅ Automatic news display on website  

---

**Need help?** Check `FIREBASE_SETUP.md` for detailed instructions.

