from flask import Flask, request, jsonify, make_response
from flask_socketio import SocketIO, emit
from flask_cors import CORS
from firebase import db
from agent import Agent
import threading

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='threading', max_http_buffer_size=10 * 1024 * 1024)

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

def agent_reply_handler(message, client_sid, project_id):
    """Callback function to handle agent replies"""
    if (message != ""):
        socketio.emit('agent_response', {"message": message, "project_id": project_id}, room=client_sid)

def style_callback(code, client_sid, project_id, html_code = None):
    # Get a reference to the specific document
    doc_ref = db.collection('projects').document(project_id)

    data = {
        "updated": True,
        'cssCode': code,
    }
    if html_code:
        data['htmlCode'] = html_code
        
    # Update the document
    doc_ref.update(data)

    toReturn = {
        "code": code,
        "project_id": project_id,
    }
    if html_code:
        toReturn['htmlCode'] = html_code
    
    socketio.emit('styled_code', toReturn, room=client_sid)

def screenshot_callback(client_sid, project_id):
    socketio.emit('screenshot', {"project_id": project_id}, room=client_sid)

def finish_callback(client_sid, project_id):
    socketio.emit('finish', {"project_id": project_id}, room=client_sid)

agent.reply_callback = agent_reply_handler
agent.style_callback = style_callback
agent.screenshot_callback = screenshot_callback
agent.finish_callback = finish_callback

@socketio.on('connect')
def handle_connect():
    print('Client connected')
    agent.set_client_connected()

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')
    agent.set_client_disconnected()

@socketio.on('style_code')
def handle_style_code(data):
    print("got it")
    html_code = data.get('htmlCode')
    css_code = data.get('cssCode')
    css_type = data.get('cssType')
    project_id = data.get('id')
    client_sid = request.sid
    
    edit_classes = data.get('editClasses')
    messages = data.get('messages', [])
    
    texts = []
    images = []
    
    # Process messages
    for message in messages:
        if message.get('text'):
            texts.append(message['text'])
        if message.get('images'):
            for image in message['images']:
                images.append({"image": image, "text": message.get('text', '')})

    agent.receive_input(html_code, css_code, texts=texts, images=images, css_type=css_type, edit_classes=edit_classes, client_sid=client_sid, project_id=project_id)
    socketio.emit('start', {"project_id": project_id}, room=client_sid)

@socketio.on('screenshot_response')
def handle_screenshot_response(data):
    screenshot = data.get('screenshot')
    project_id = data.get('project_id')
    if screenshot:
        agent.receive_screenshot(screenshot)

@socketio.on('screenshot_unavailable')
def handle_screenshot_unavailable(data):
    agent.working_memory.observations.append("Unable to access screenshots at the moment.") 
    if not agent.decision_loop_running:
        agent.decision_thread = threading.Thread(target=agent.make_decision)
        agent.decision_thread.start()

@socketio.on('reset')
def handle_reset():
    print("Reset received from client.")
    agent.reset()
    print("Agent reset.")

if __name__ == "__main__":
    print("Agent is ready. Starting SocketIO server...")
    socketio.run(app, debug=True, port=7777)
