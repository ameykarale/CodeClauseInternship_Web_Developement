import random
from flask import Flask, render_template, request
from flask_socketio import SocketIO

app = Flask(__name__)
socketio = SocketIO(app)

# Store user info (name and color)
user_info = {}

def generate_random_color():
    return "#{:06x}".format(random.randint(0, 0xFFFFFF))

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('connect')
def handle_connect():
    user_id = request.sid  # Use the unique socket ID as the user ID
    socketio.emit('request_name', {'user_id': user_id})

@socketio.on('disconnect')
def handle_disconnect():
    user_id = request.sid
    user_info.pop(user_id, None)
    socketio.emit('user_disconnected', {'user_id': user_id})

@socketio.on('submit_name')
def handle_submit_name(data):
    user_id = data['user_id']
    user_name = data['name']
    user_color = generate_random_color()
    
    user_info[user_id] = {'name': user_name, 'color': user_color}
    
    socketio.emit('color_assigned', {'user_id': user_id, 'color': user_color})
    socketio.emit('user_connected', {'user_id': user_id, 'name': user_name})

@socketio.on('message')
def handle_message(data):
    user_id = request.sid
    user_info_entry = user_info.get(user_id, {'name': 'Anonymous', 'color': '#000000'})
    message = {'user_id': user_id, 'name': user_info_entry['name'], 'color': user_info_entry['color'], 'text': data['text']}
    socketio.emit('message', message)

if __name__ == '__main__':
    socketio.run(app, debug=True)
