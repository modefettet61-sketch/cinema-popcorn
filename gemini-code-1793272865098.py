from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import json
import os

app = Flask(__name__)
app.secret_key = 'cinema_popcorn_secret_key_2026'

DATA_FILE = 'data.json'

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []
    return []

def save_data(data):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

@app.route('/')
def index():
    data = load_data()
    return render_template('index.html', data=data)

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        password = request.form.get('password')
        if password == '123':
            session['logged_in'] = True
            return redirect(url_for('admin'))
        else:
            return render_template('admin_login.html', error='كلمة المرور غير صحيحة')
    
    if not session.get('logged_in'):
        return render_template('admin_login.html')
    
    data = load_data()
    return render_template('admin_dashboard.html', data=data)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)