from flask import Blueprint, request, redirect, url_for, render_template, flash, session
from database.db_connection import get_db_connection

auth_bp = Blueprint('auth', __name__)


# ================= REGISTER ================= #

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():

    if request.method == 'POST':

        name = request.form['name']
        email = request.form['email']
        password = request.form['password']

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        try:
            # Check duplicate email
            cursor.execute("SELECT id FROM users WHERE email=%s", (email,))
            existing = cursor.fetchone()

            if existing:
                flash("Email already registered!", "danger")
                return redirect(url_for('auth.register'))

            # Insert user
            cursor.execute("""
                INSERT INTO users (name, email, password)
                VALUES (%s, %s, %s)
            """, (name, email, password))

            flash("Registration Successful!", "success")
            return redirect(url_for('auth.login'))

        except Exception as e:
            print("REGISTER ERROR:", e)
            flash("Registration failed. Check console.", "danger")

        finally:
            cursor.close()
            conn.close()

    return render_template('auth/register.html')


# ================= LOGIN ================= #

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':

        email = request.form['email']
        password = request.form['password']

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
            SELECT * FROM users
            WHERE email=%s AND password=%s
        """, (email, password))

        user = cursor.fetchone()

        if user:

            session['user_id'] = user['id']
            session['user_name'] = user['name']
            session['email'] = user['email']

            # Check health profile
            cursor.execute("""
                SELECT * FROM user_health
                WHERE user_id=%s
            """, (user['id'],))

            health = cursor.fetchone()

            cursor.close()
            conn.close()

            if not health:
                session['first_time_login'] = True
                return redirect(url_for('health.health_profile'))

            session['first_time_login'] = False
            return redirect(url_for('dashboard.dashboard'))

        else:
            flash("Invalid Email or Password", "danger")

            cursor.close()
            conn.close()

    return render_template('auth/login.html')


# ================= LOGOUT ================= #

@auth_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))