================================================================================
                    IMAGEFORGE - AI IMAGE GENERATION PLATFORM
                         VS CODE SETUP GUIDE
================================================================================

OVERVIEW
--------
ImageForge is a Flask-based AI image generation platform using Stability AI.
It includes user authentication, image generation, and editing features.

================================================================================
                        STEP-BY-STEP SETUP IN VS CODE
================================================================================

STEP 1: INSTALL PYTHON
-----------------------
1. Download Python 3.11 or higher from https://www.python.org/downloads/
2. During installation, CHECK the box "Add Python to PATH"
3. Verify installation by opening Command Prompt/Terminal and typing:
   python --version
   (Should show Python 3.11.x or higher)

STEP 2: COPY PROJECT FILES
---------------------------
1. Copy ALL files from this project to a folder on your computer
   Example: C:\Projects\ImageForge or ~/Projects/ImageForge

2. Files you should have:
   - app.py (main application)
   - database.py (database setup)
   - templates/ folder (HTML files)
   - static/ folder (images and assets)
   - .gitignore
   - README.txt (this file)

STEP 3: OPEN PROJECT IN VS CODE
--------------------------------
1. Open Visual Studio Code
2. Click "File" > "Open Folder"
3. Select your ImageForge folder
4. VS Code will load the project

STEP 4: INSTALL PYTHON DEPENDENCIES
------------------------------------
1. Open Terminal in VS Code (View > Terminal or Ctrl+`)

2. Create a virtual environment (RECOMMENDED):
   Windows:
      python -m venv venv
      venv\Scripts\activate
   
   Mac/Linux:
      python3 -m venv venv
      source venv/bin/activate

3. Install required packages:
   pip install flask flask-session stability-sdk pillow werkzeug requests

   Wait for all packages to install successfully.

STEP 5: SET UP ENVIRONMENT VARIABLES
-------------------------------------
1. Create a file named ".env" in your project root folder

2. Add these variables to the .env file:

   SESSION_SECRET=your-random-secret-key-here
   STABILITY_API_KEY=your-stability-ai-api-key-here

3. HOW TO GET STABILITY AI API KEY:
   a. Go to https://platform.stability.ai/
   b. Create an account or log in
   c. Navigate to "API Keys" section
   d. Click "Create API Key"
   e. Copy the key and paste it in your .env file

4. GENERATE A SESSION SECRET:
   - Use any random string (20+ characters)
   - Example: mySecretKey123456789!@#$%

5. Load environment variables in your code:
   - Add this to app.py if not already there:
     from dotenv import load_dotenv
     load_dotenv()
   
   - Install python-dotenv:
     pip install python-dotenv

STEP 6: INITIALIZE THE DATABASE
--------------------------------
1. The database will be created automatically when you first run the app
2. It creates a file named "imageforge.db" in your project folder
3. SQLite is used - no additional database installation needed!

STEP 7: RUN THE APPLICATION
----------------------------
1. Make sure your virtual environment is activated (you'll see (venv) in terminal)

2. Run the app:
   python app.py

3. You should see output like:
   Database initialized successfully!
   * Running on http://127.0.0.1:5000
   * Running on http://0.0.0.0:5000

4. Open your browser and go to:
   http://localhost:5000

STEP 8: TEST THE APPLICATION
-----------------------------
1. Click "Sign Up" to create an account
2. Fill in username, email, and password
3. Log in with your credentials
4. Go to "Generate" page
5. Enter a prompt like "a beautiful sunset over mountains"
6. Click "Generate Image"
7. View your image in the "History" page

================================================================================
                          EDITING FEATURES GUIDE
================================================================================

IMAGE EDITING OPTIONS:
1. Go to "History" page
2. Hover over any generated image
3. Click the EDIT button (blue pencil icon)

AVAILABLE EDITING TOOLS:
- Brightness: Adjust image brightness (0-200%)
- Contrast: Adjust image contrast (0-200%)
- Saturation: Adjust color intensity (0-200%)
- Rotate: Rotate image 90° clockwise or counter-clockwise
- Reset: Undo all changes
- Save: Apply changes and save the edited image

================================================================================
                          PROJECT STRUCTURE
================================================================================

ImageForge/
├── app.py                  # Main Flask application
├── database.py             # Database setup and connection
├── imageforge.db           # SQLite database (auto-created)
├── README.txt              # This file
├── .env                    # Environment variables (you create this)
├── .gitignore              # Git ignore rules
│
├── templates/              # HTML templates
│   ├── base.html
│   ├── index.html          # Homepage
│   ├── signup.html         # Sign up page
│   ├── login.html          # Login page
│   ├── generate.html       # Image generation page
│   ├── profile.html        # User profile
│   ├── edit_profile.html   # Edit profile page
│   ├── history.html        # Image history
│   └── edit_image.html     # Image editor
│
├── static/                 # Static files
│   └── generated_images/   # Saved AI-generated images
│
└── flask_session/          # Session data (auto-created)

================================================================================
                          TROUBLESHOOTING
================================================================================

PROBLEM: "Module not found" error
SOLUTION: Make sure you activated the virtual environment and installed all packages

PROBLEM: Database errors
SOLUTION: Delete imageforge.db and let the app recreate it

PROBLEM: Can't generate images
SOLUTION: Check your STABILITY_API_KEY in .env file is correct

PROBLEM: Port 5000 already in use
SOLUTION: Edit app.py and change port 5000 to another port like 8000:
          app.run(host='0.0.0.0', port=8000, debug=True)

PROBLEM: Images not saving
SOLUTION: Check that static/generated_images/ folder exists
          The app should create it automatically

================================================================================
                          ROUTES AVAILABLE
================================================================================

/               - Homepage
/signup         - User registration
/login          - User login
/logout         - Logout user
/generate       - Generate AI images (requires login)
/profile        - View profile (requires login)
/edit_profile   - Edit profile (requires login)
/history        - View image history (requires login)
/edit_image/<id> - Edit specific image (requires login)

================================================================================
                          FEATURES SUMMARY
================================================================================

✓ User Authentication (signup, login, logout)
✓ Password hashing for security
✓ AI Image Generation using Stability AI
✓ Personal image gallery/history
✓ Image editing (rotate, brightness, contrast, saturation)
✓ Download images
✓ Delete images
✓ User profile management
✓ SQLite database (portable, no server needed)
✓ Session management
✓ Flash messages for user feedback

================================================================================
                          DEPLOYMENT NOTES
================================================================================

FOR PRODUCTION:
1. Change debug=True to debug=False in app.py
2. Use a production WSGI server like Gunicorn:
   pip install gunicorn
   gunicorn -w 4 -b 0.0.0.0:5000 app:app

3. Set strong SESSION_SECRET in environment variables
4. Consider migrating from SQLite to PostgreSQL for better performance
5. Use a proper web server like Nginx as reverse proxy

================================================================================
                          SUPPORT & CREDITS
================================================================================

Technology Stack:
- Backend: Flask (Python)
- Database: SQLite3
- AI: Stability AI SDK
- Frontend: HTML, Tailwind CSS, JavaScript
- Image Processing: Pillow (PIL)

For questions or issues, refer to:
- Flask Documentation: https://flask.palletsprojects.com/
- Stability AI Docs: https://platform.stability.ai/docs

================================================================================
                          QUICK START COMMANDS
================================================================================

# Activate virtual environment
Windows: venv\Scripts\activate
Mac/Linux: source venv/bin/activate

# Install dependencies
pip install flask flask-session stability-sdk pillow werkzeug requests python-dotenv

# Run application
python app.py

# Access application
Open browser: http://localhost:5000

================================================================================
                                 END
================================================================================
