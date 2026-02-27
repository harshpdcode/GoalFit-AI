from flask import Blueprint, render_template, request, session, redirect, url_for
from database.db_connection import get_db_connection
from datetime import date

progress_bp = Blueprint('progress', __name__)


@progress_bp.route('/progress', methods=['GET', 'POST'])
def progress():

    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    user_id = session['user_id']

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Insert new weight
    if request.method == 'POST':
        weight = request.form['weight']

        cursor.execute("""
            INSERT INTO progress_logs (user_id, weight_kg, log_date)
            VALUES (%s, %s, %s)
        """, (user_id, weight, date.today()))

        conn.commit()

    # Fetch weight history
    cursor.execute("""
        SELECT weight_kg, log_date
        FROM progress_logs
        WHERE user_id=%s
        ORDER BY log_date ASC
    """, (user_id,))

    logs = cursor.fetchall()

    # Fetch BMI data
    cursor.execute("""
        SELECT bmi_value, recorded_date
        FROM bmi_records
        WHERE user_id=%s
        ORDER BY recorded_date ASC
    """, (user_id,))

    bmi_logs = cursor.fetchall()

    # Fetch health data
    cursor.execute("""
        SELECT weight_kg, target_weight
        FROM user_health
        WHERE user_id=%s
    """, (user_id,))

    health = cursor.fetchone()

    cursor.close()
    conn.close()

    return render_template(
        'user/progress.html',
        logs=logs,
        bmi_logs=bmi_logs,
        health=health,
        user_name=session.get('user_name'),
        email=session.get('email')
    )