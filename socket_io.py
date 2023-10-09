from flask import Flask, session, copy_current_request_context
from flask_socketio import SocketIO, emit

app = Flask(__name__)
socketio = SocketIO(app, async_mode=None)

# socket functions
# Decorator to catch an event called "new inference":
@socketio.on('new_inference', namespace='/detect')
# updateInference() is the event callback function.
def updateInference(data):              
	# Trigger a new event called "update_inference"
	# that can be caught by another callback later in the program.
    emit('update_inference', data)      

@socketio.on('my_event', namespace='/test')
def test_message(message):
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my_response',
		{'data': message['data'], 'count': session['receive_count']})


@socketio.on('my_broadcast_event', namespace='/test')
def test_broadcast_message(message):
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my_response',
		{'data': message['data'], 'count': session['receive_count']},
		broadcast=True)


@socketio.on('disconnect_request', namespace='/test')
def disconnect_request():
    @copy_current_request_context
    def can_disconnect():
        disconnect()

    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my_response',
		{'data': 'Disconnected!', 'count': session['receive_count']},
		callback=can_disconnect)

@socketio.event
def connect():
    print("I'm connected!")

@socketio.event
def connect_error():
    print("The connection failed!")

@socketio.event
def disconnect():
    print("I'm disconnected!")
