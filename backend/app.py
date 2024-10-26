from flask import Flask, request, jsonify, make_response
from flask_socketio import SocketIO, emit
from flask_cors import CORS
from agent import Agent

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='threading')

agent = Agent()

def _build_cors_preflight_response():
    response = make_response()
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add("Access-Control-Allow-Headers", "*")
    response.headers.add("Access-Control-Allow-Methods", "*")
    return response

@app.route('/send_message', methods=['POST', 'OPTIONS'])
def send_message():
    if request.method == 'OPTIONS':
        response = _build_cors_preflight_response();
        return response, 200
    
    data = request.json
    if 'message' not in data:
        return jsonify({"error": "No message provided"}), 400

    user_input = data['message']
    agent.receive_input(user_input)

    response = jsonify({"status": "Message received"})
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add("Access-Control-Allow-Headers", "*")
    response.headers.add("Access-Control-Allow-Methods", "*")
    return response, 200

def agent_reply_handler(message, client_sid):
    """Callback function to handle agent replies"""
    print("AGENT REPLY HANDLER", message, client_sid)
    socketio.emit('agent_response', {"message": message}, room=client_sid)
    print(f"Message emitted: {message}")

def style_callback(code, client_sid):
    socketio.emit('styled_code', {"code": code}, room=client_sid)

def screenshot_callback(screenshot, client_sid):
    socketio.emit('screenshot', {"screenshot": screenshot}, room=client_sid)

agent.reply_callback = agent_reply_handler
agent.style_callback = style_callback
agent.screenshot_callback = screenshot_callback
@socketio.on('connect')
def handle_connect():
    print('Client connected')

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

@socketio.on('user_message')
def handle_message(data):
    message = data.get('message')
    if message:
        client_sid = request.sid
        agent.receive_input(message, client_sid)
    else:
        emit('error', {'message': 'No message provided'})

@socketio.on('style_code')
def handle_style_code(data):
    html_code = data.get('htmlCode')
    css_code = data.get('cssCode')
    css_type = data.get('cssType')
    user_input = data.get('messages')
    client_sid = request.sid
    edit_classes = data.get('editClasses')

    print("STYLING CODE", html_code, css_code, css_type, edit_classes)
    
    styled_code = agent.receive_input(html_code, css_code, user_input, client_sid)
    
    emit('styled_code', styled_code)

@socketio.on('reset')
def handle_reset():
    print("Reset received from client.")
    agent.reset()
    print("Agent reset.")

if __name__ == "__main__":
    print("Agent is ready. Starting SocketIO server...")
    socketio.run(app, debug=True, port=7777)
