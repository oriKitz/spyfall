import random
import string
from .models import User, Room, RoomUser


def generate_room_id():
    return ''.join([random.choice(string.ascii_letters) for _ in range(4)])


def get_user_current_room(user_id):
    user_rooms = RoomUser.query.filter_by(user_id=user_id)
    user_room = sorted(user_rooms, key=lambda user_room: user_room.last_connected, reverse=True)[0].room_id
    return Room.query.get(user_room)