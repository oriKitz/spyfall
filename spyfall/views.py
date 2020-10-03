from flask import render_template, url_for, request, jsonify, redirect, flash
from spyfall import app, db, bcrypt
from flask_login import login_user, current_user, logout_user, login_required
from .forms import LoginForm
from .models import User, Room, RoomUser
from .utils import *
from .config import Config
import datetime


@app.route('/', methods=['GET', 'POST'])
def create_game():
    return render_template('home.html')


@app.route('/create_room')
@app.route('/<string:room_id>')
@app.route('/enter-name/<string:room_id>', methods=['GET', 'POST'])
def enter_name(room_id):
    if request.path == '/create-room':
        room_id = generate_room_id()
        room = Room(room_id=room_id)
        db.session.add(room)
        db.session.commit()
    else:
        room = None

    if current_user.is_authenticated:
        if not room:
            room = Room.query.get(room_id)

        if not room.users:
            room.admin = current_user.id

        room_user = RoomUser(user_id=current_user.id, room_id=room.id)
        db.session.add(room_user)
        db.session.commit()
        return redirect(f'/lobby')

    if request.form:
        user = User.query.filter_by(username=request.form['username']).first()
        if not user:
            user = User(username=request.form['username'])
            db.session.add(user)
            db.session.commit()
        # Should check if room exists
        room = Room.query.filter_by(room_id=room_id).first()

        if not room.users:
            room.admin = user.id

        room_user = RoomUser(user_id=user.id, room_id=room.id)
        db.session.add(room_user)
        db.session.commit()

        login_user(user, remember=True)
        return redirect(f'/lobby')

    return render_template('enter_name.html', room_id=room_id)


@app.route('/status', methods=['GET', 'POST'])
def status_update():
    room = get_user_current_room(current_user.id)
    # room = Room.query.get(room_id)
    game_started = room.game_status == 'started'
    room_users = [user.username for user in room.users]
    room_users.sort()

    user_room = RoomUser.query.filter_by(user_id=current_user.id, room_id=room.id).first()
    user_room.last_connected = datetime.datetime.now()
    db.session.commit()

    return jsonify(game_started=game_started, room_users=room_users, admin_user=room.admin, user_id=current_user.id)


@app.route('/lobby')
def lobby():
    return render_template('lobby.html')


@app.route('/game')
def game():
    room = get_user_current_room(current_user.id)
    return render_template('game.html', location=room.location, spy=room.spy == current_user.id, possible_locations=Config.LOCATIONS)


@app.route('/start-game')
def start_game():
    location = random.choice(Config.LOCATIONS)
    room = get_user_current_room(current_user.id)
    spy = random.choice(room.users)

    room.location = location
    room.spy = spy.id
    room.game_status = 'started'
    db.session.commit()

    return redirect('/game')


@app.route('/end-game')
def end_game():
    room = get_user_current_room(current_user.id)
    room.game_status = 'ended'
    db.session.commit()
    return redirect('/lobby')
