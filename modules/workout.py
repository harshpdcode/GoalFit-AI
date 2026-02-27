from flask import Blueprint, session, redirect, url_for, render_template
from database.db_connection import get_db_connection

workout_bp = Blueprint('workout', __name__)


@workout_bp.route('/workout-plan')
def workout_plan():

    # ---------- SESSION ----------
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    user_id = session['user_id']

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # ---------- USER HEALTH ----------
    cursor.execute("""
        SELECT goal_type, activity_level
        FROM user_health
        WHERE user_id=%s
    """, (user_id,))
    health = cursor.fetchone()

    # ---------- BMI ----------
    cursor.execute("""
        SELECT bmi_category
        FROM bmi_records
        WHERE user_id=%s
        ORDER BY recorded_date DESC
        LIMIT 1
    """, (user_id,))
    bmi_data = cursor.fetchone()

    if not health or not bmi_data:
        return "Health/BMI data missing"

    goal = health['goal_type']
    activity = health['activity_level']
    bmi = bmi_data['bmi_category']

    # ---------- DIFFICULTY FILTER ----------
    if bmi in ["Obese", "Overweight"]:
        difficulty_levels = ["Beginner", "Intermediate"]

    elif bmi == "Normal":
        difficulty_levels = ["Intermediate"]

    else:
        difficulty_levels = ["Intermediate", "Advanced"]

    format_strings = ','.join(['%s'] * len(difficulty_levels))

    query = f"""
        SELECT *
        FROM workout_exercises
        WHERE difficulty_level IN ({format_strings})
        ORDER BY muscle_id, option_group
    """

    cursor.execute(query, tuple(difficulty_levels))
    all_exercises = cursor.fetchall()

    # ---------- GROUP ----------
    grouped_workouts = {}

    for ex in all_exercises:
        muscle = ex['target_muscle']
        grouped_workouts.setdefault(muscle, []).append(ex)

    cursor.close()
    conn.close()

    return render_template(
        'workout/workout_plan.html',
        workouts=grouped_workouts,
        goal=goal,
        bmi=bmi,
        activity=activity,
        user_name=session.get('user_name'),
        email=session.get('email')
    )