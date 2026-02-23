import os
import io
import base64
import sqlite3
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_session import Session
from stability_sdk import client
import stability_sdk.interfaces.gooseai.generation.generation_pb2 as generation
from PIL import Image
from database import get_db_connection, init_db

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SESSION_SECRET', 'dev-secret-key-change-in-production')
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

init_db()

def login_required(f):
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to access this page.', 'error')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        if not username or not email or not password:
            flash('All fields are required!', 'error')
            return render_template('signup.html')
        
        if password != confirm_password:
            flash('Passwords do not match!', 'error')
            return render_template('signup.html')
        
        password_hash = generate_password_hash(password)
        
        conn = get_db_connection()
        try:
            conn.execute(
                'INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)',
                (username, email, password_hash)
            )
            conn.commit()
            flash('Account created successfully! Please log in.', 'success')
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            flash('Username or email already exists!', 'error')
        finally:
            conn.close()
    
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if not username or not password:
            flash('Please enter both username and password!', 'error')
            return render_template('login.html')
        
        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
        conn.close()
        
        if user is None:
            flash('Invalid username', 'error')
            return render_template('login.html')
        
        if not check_password_hash(user['password_hash'], password):
            flash('Incorrect password', 'error')
            return render_template('login.html')
        
        session['user_id'] = user['id']
        session['username'] = user['username']
        flash('Login successful!', 'success')
        return redirect(url_for('generate'))
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'success')
    return redirect(url_for('index'))

@app.route('/generate', methods=['GET', 'POST'])
@login_required
def generate():
    if request.method == 'POST':
        prompt = request.form.get('prompt')
        
        if not prompt:
            flash('Please enter a prompt!', 'error')
            return render_template('generate.html')
        
        try:
            api_key = os.environ.get('STABILITY_API_KEY')
            if not api_key:
                flash('Stability AI API key not configured. Please set STABILITY_API_KEY environment variable.', 'error')
                return render_template('generate.html')
            
            stability_api = client.StabilityInference(
                key=api_key,
                verbose=True,
            )
            
            answers = stability_api.generate(
                prompt=prompt,
                seed=42,
                steps=30,
                cfg_scale=8.0,
                width=512,
                height=512,
                samples=1,
                sampler=generation.SAMPLER_K_DPMPP_2M
            )
            
            for resp in answers:
                for artifact in resp.artifacts:
                    if artifact.finish_reason == generation.FILTER:
                        flash('Your request activated the API safety filters. Please modify your prompt.', 'warning')
                        return render_template('generate.html')
                    
                    if artifact.type == generation.ARTIFACT_IMAGE:
                        img = Image.open(io.BytesIO(artifact.binary))
                        
                        os.makedirs('static/generated_images', exist_ok=True)
                        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                        image_filename = f"img_{session['user_id']}_{timestamp}.png"
                        image_path = f"static/generated_images/{image_filename}"
                        img.save(image_path)
                        
                        conn = get_db_connection()
                        conn.execute(
                            'INSERT INTO image_history (user_id, prompt, image_path) VALUES (?, ?, ?)',
                            (session['user_id'], prompt, image_path)
                        )
                        conn.commit()
                        conn.close()
                        
                        flash('Image generated successfully!', 'success')
                        return redirect(url_for('history'))
        
        except Exception as e:
            flash(f'Error generating image: {str(e)}', 'error')
    
    return render_template('generate.html')

@app.route('/profile')
@login_required
def profile():
    conn = get_db_connection()
    user = conn.execute('SELECT * FROM users WHERE id = ?', (session['user_id'],)).fetchone()
    conn.close()
    return render_template('profile.html', user=user)

@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    if request.method == 'POST':
        email = request.form.get('email')
        new_password = request.form.get('new_password')
        
        conn = get_db_connection()
        
        if new_password:
            password_hash = generate_password_hash(new_password)
            conn.execute(
                'UPDATE users SET email = ?, password_hash = ? WHERE id = ?',
                (email, password_hash, session['user_id'])
            )
        else:
            conn.execute(
                'UPDATE users SET email = ? WHERE id = ?',
                (email, session['user_id'])
            )
        
        conn.commit()
        conn.close()
        flash('Profile updated successfully!', 'success')
        return redirect(url_for('profile'))
    
    conn = get_db_connection()
    user = conn.execute('SELECT * FROM users WHERE id = ?', (session['user_id'],)).fetchone()
    conn.close()
    return render_template('edit_profile.html', user=user)

@app.route('/history')
@login_required
def history():
    conn = get_db_connection()
    images = conn.execute(
        'SELECT * FROM image_history WHERE user_id = ? ORDER BY created_at DESC',
        (session['user_id'],)
    ).fetchall()
    conn.close()
    return render_template('history.html', images=images)

@app.route('/delete_image/<int:image_id>', methods=['POST'])
@login_required
def delete_image(image_id):
    conn = get_db_connection()
    image = conn.execute(
        'SELECT * FROM image_history WHERE id = ? AND user_id = ?',
        (image_id, session['user_id'])
    ).fetchone()
    
    if image:
        if os.path.exists(image['image_path']):
            os.remove(image['image_path'])
        
        conn.execute('DELETE FROM image_history WHERE id = ?', (image_id,))
        conn.commit()
        flash('Image deleted successfully!', 'success')
    else:
        flash('Image not found or you do not have permission to delete it.', 'error')
    
    conn.close()
    return redirect(url_for('history'))

@app.route('/edit_image/<int:image_id>')
@login_required
def edit_image(image_id):
    conn = get_db_connection()
    image = conn.execute(
        'SELECT * FROM image_history WHERE id = ? AND user_id = ?',
        (image_id, session['user_id'])
    ).fetchone()
    conn.close()
    
    if not image:
        flash('Image not found or you do not have permission to edit it.', 'error')
        return redirect(url_for('history'))
    
    return render_template('edit_image.html', image=image)

@app.route('/save_edited_image', methods=['POST'])
@login_required
def save_edited_image():
    temp_path = None
    conn = None
    try:
        image_id = request.form.get('image_id')
        
        conn = get_db_connection()
        image = conn.execute(
            'SELECT * FROM image_history WHERE id = ? AND user_id = ?',
            (image_id, session['user_id'])
        ).fetchone()
        
        if not image:
            return {'success': False, 'error': 'Image not found'}, 403
        
        if 'image' in request.files:
            edited_image = request.files['image']
            
            temp_path = image['image_path'] + '.tmp'
            edited_image.save(temp_path)
            
            if os.path.exists(temp_path):
                os.replace(temp_path, image['image_path'])
                temp_path = None
            else:
                return {'success': False, 'error': 'Failed to save temporary file'}, 500
        
        return {'success': True}
    
    except Exception as e:
        if temp_path and os.path.exists(temp_path):
            os.remove(temp_path)
        return {'success': False, 'error': str(e)}, 500
    
    finally:
        if conn:
            conn.close()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
