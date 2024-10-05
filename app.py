from flask import Flask, request, jsonify, render_template, redirect, url_for
import sqlite3
import hashlib

app = Flask(__name__)

# Створення або підключення до бази даних
def init_db():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Хешування пароля
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Перевірка наявності користувача
def user_exists(username, password=None):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    if password:
        cursor.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, hash_password(password)))
    else:
        cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
    user = cursor.fetchone()
    conn.close()
    return user

# Реєстрація користувача
@app.route('/register', methods=['POST'])
def register():
    data = request.form
    username = data['username']
    email = data['email']
    password = data['password']
    confirm_password = data['confirm_password']

    if password != confirm_password:
        return jsonify({"message": "Паролі не збігаються"}), 400

    if user_exists(username):
        return jsonify({"message": "Користувач вже існує"}), 400

    hashed_password = hash_password(password)

    try:
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO users (email, username, password) VALUES (?, ?, ?)', (email, username, hashed_password))
        conn.commit()
        conn.close()
        return jsonify({"message": "Успішна реєстрація"}), 200
    except sqlite3.IntegrityError:
        return jsonify({"message": "Користувач з таким email вже існує"}), 400

# Вхід користувача
@app.route('/login', methods=['POST'])
def login():
    data = request.form
    username = data['username']
    password = data['password']

    user = user_exists(username, password)
    
    if user:
        return jsonify({"message": "Успішний вхід"}), 200
    else:
        return jsonify({"message": "Невірний логін або пароль"}), 400

# Рендеринг HTML
@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
