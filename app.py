from flask import Flask, render_template
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)


@socketio.on('my_event', namespace='/')
def test_message(message):
    emit('my_response',
         {'data': "test"})

if __name__ == '__main__':
    socketio.run(app, "0.0.0.0", port=8000)
