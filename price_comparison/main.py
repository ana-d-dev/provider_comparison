from os import error

from price_comparison.db.db_access import get_all_data, get_provider_data, get_user_by_id, get_user_by_api_key
from flask import Flask, render_template, jsonify, redirect, url_for, session, request
from price_comparison.forms import RegistrationForm, LoginForm
from price_comparison.auth import register_user, auth_user
from price_comparison.logger_config import setup_logger
from flask_limiter.util import get_remote_address
from price_comparison.utils import last_update
from flask_limiter import Limiter
from dotenv import load_dotenv
import time
import os



logger = setup_logger('main')
app = Flask(__name__)

current_time = time.localtime()
date = time.strftime('%d.%m.%Y.', current_time)

load_dotenv()
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

# app.config['SESSION_COOKIE_HTTPONLY'] = True
# app.config['SESSION_COOKIE_SECURE'] = True
# app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
limiter = Limiter(get_remote_address, app=app)


@app.context_processor
def inject():
    return {"logged_in": "user_id" in session}


@app.route('/')
def home():
    circle_images = ['a1.png', 'bon-bon.png', 'tcom.png', 'telemach.jpeg', 'tomato.png', 'compare.png', 'api.png']
    paths = ['a1', 'bon_bon', 'tcom', 'telemach', 'tomato', 'compare', 'api']
    tariff_names = ['A1', 'Bon-Bon', 'T-Com', 'Telemach', 'Tomato', 'Compare', 'API']
    return render_template('home.html', circle_images=circle_images, paths=paths, tariff_names=tariff_names, date=date, active_page='home')


@app.route('/a1')
def a1():
    rows = get_provider_data('A1')
    return render_template('a1.html', rows=rows, date=date, last_update=last_update(), active_page='a1')


@app.route('/bon_bon')
def bon_bon():
    rows = get_provider_data('BONBON')
    return render_template('bon_bon.html', rows=rows, date=date, last_update=last_update(), active_page='bon_bon')


@app.route('/tcom')
def tcom():
    rows = get_provider_data('T-COM')
    return render_template('tcom.html', rows=rows, date=date, last_update=last_update(), active_page='tcom')


@app.route('/telemach')
def telemach():
    rows = get_provider_data('TELEMACH')
    if rows:
        return render_template('telemach.html', rows=rows, date=date, last_update=last_update(), active_page='telemach')
    else:
        return render_template('unavailable.html', active_page='telemach')


@app.route('/tomato')
def tomato():
    rows = get_provider_data('TOMATO')
    return render_template('tomato.html', rows=rows, date=date, last_update=last_update(), active_page='tomato')


@app.route('/compare')
def compare():
    data = get_all_data()
    return render_template('compare.html', rows=data, last_update=last_update(), active_page='compare')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/contact')
def contact():
    return render_template('contact.html')


@app.route('/privacy')
def privacy():
    return render_template('privacy.html')


@app.get('/register')
def register():
    form = RegistrationForm()
    return render_template('register.html', form=form)


@app.post('/register')
# @limiter.limit("5 per minute")
# @limiter.limit("20 per hour")
# @limiter.limit("200 per week")
def register_post():
    register_form = RegistrationForm()


    if register_form.validate_on_submit():
        username = register_form.username.data.strip().lower()
        password = register_form.password.data


        success, message = register_user(username, password)
        if success:
            return render_template("login.html", form=LoginForm(), message=message)

        return render_template("register.html", form=register_form, message=message)

    username_message = register_form.username.errors
    password_message = register_form.password.errors

    return render_template("register.html", form=register_form, username_message=username_message, password_message=password_message)


@app.get('/login')
def login():
    form = LoginForm()
    return render_template('login.html', form=form)


@app.post('/login')
# @limiter.limit("5 per minute")
# @limiter.limit("20 per hour")
# @limiter.limit("200 per week")
def login_post():
    form = LoginForm()

    if not form.validate_on_submit():
        return render_template("login.html", form=form, error_message='Invalid credentials.')

    username = form.username.data.strip()
    password = form.password.data
    user = auth_user(username, password)
    if not user:
        return render_template("login.html", form=form, error_message='Invalid credentials.')

    session["user_id"] = user["id"]

    return redirect(url_for("profile"))



@app.route('/profile')
def profile():
    user_id = session.get('user_id')

    if not user_id:
        session.clear()
        return redirect(url_for('login'))

    # logged_in = True
    user = get_user_by_id(user_id)
    return render_template('profile.html', username=user['username'], api_key=user['api_key'])


@app.post("/logout")
def logout_post():
    session.clear()
    return redirect(url_for("home"))


@app.route('/api')
def api():
    return render_template('api.html', active_page='API')


@app.route('/api/tariffs')
def api_tariffs():
    api_key = request.headers.get('X-API-Key')

    user = get_user_by_api_key(api_key)
    if not user:
        return jsonify({"error": "invalid or missing API key"}), 401

    data = get_all_data()
    return jsonify(data)



if __name__ == '__main__':
    app.run(debug=True)





