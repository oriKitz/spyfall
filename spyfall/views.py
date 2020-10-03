from flask import render_template, url_for, request, jsonify, redirect, flash
from spyfall import app, db, bcrypt
from flask_login import login_user, current_user, logout_user, login_required


@app.route('/')
@app.route('/home')
def create_game():
    return render_template('home.html')


@app.route('/enter-name')
@app.route('/<string:room_id>')
def enter_name(room_id):
    return render_template('enter_name.html')


@app.route('/lobby/<string:room_id>/<string:username>')
def login(room_id, username):
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form, fields=['username', 'password'])


@app.route('/lobby/<string:room_id>')
def lobby(room_id):
    pass


@app.route('/game/<string:room_id>')
def game(room_id):
    pass


@app.route('/start-game/<string:room_id>')
def start_game(room_id):
    pass


@app.route('/end-game/<string:room_id>')
def end_game(room_id):
    pass
