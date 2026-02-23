# ImageForge
ImageForge is a Flask-based AI image generation web application powered by Stability AI.

It includes user authentication, image generation, and basic image editing features.
## Requirements

- Python 3.11+
- Stability AI API Key

## Tech Stack
- Flask
- Stability AI SDK
- SQLite3
- Pillow
- Werkzeug (password hashing)
- Flask-Session
- Python-Dotenv

---

## Installation

Clone the repository(example only):

```bash
git clone (repository url)
cd ImageForge

How to run it:
#Create and activate virtual environment:
python -m venv venv
venv\Scripts\activate

#Install dependencies:
pip install flask flask-session stability-sdk pillow werkzeug requests python-dotenv blinker

#Create a .env file in the project root:
SESSION_SECRET=your_random_secret
STABILITY_API_KEY=your_stability_api_key

#Run the app:
python app.py
Open:
http://localhost:5000

Notes
.env, database files, and virtual environments are ignored via .gitignore.
For production, disable debug mode and use a proper WSGI server.
Author
Tushar Panchal
