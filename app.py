from flask import Flask ,session, redirect, url_for, request
from modules.auth import auth_bp
from modules.health import health_bp
from modules.bmi import bmi_bp
from modules.prediction import prediction_bp
from modules.diet import diet_bp
from modules.workout import workout_bp
from modules.dashboard import dashboard_bp
from modules.progress import progress_bp


app = Flask(__name__)
app.secret_key = "goalfit_secret_key"

# Register Blueprint
app.register_blueprint(auth_bp)
app.register_blueprint(health_bp)
app.register_blueprint(bmi_bp)
app.register_blueprint(prediction_bp)
app.register_blueprint(diet_bp)
app.register_blueprint(workout_bp)
app.register_blueprint(dashboard_bp)
app.register_blueprint(progress_bp)


# First-time login protection
@app.before_request
def check_first_login():
    """Redirect first-time users to health profile"""
    if session.get('first_time_login'):
        # Allow only health form, auth routes, and static files
        allowed_routes = ['health.health_profile', 'auth.logout', 'static']
        if request.endpoint and request.endpoint not in allowed_routes:
            return redirect(url_for('health.health_profile'))


@app.route('/')
def home():

    if 'user_id' in session:
        return redirect(url_for('dashboard.dashboard'))

    return redirect(url_for('auth.login'))

@app.route('/check-session')
def check_session():
    return str(session)



if __name__ == '__main__':
    app.run(debug=True)