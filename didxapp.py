from flask import Flask, request, render_template, session, Blueprint
from didx import Didx_admin_bot
import json

didx_app = Blueprint('DIDxBot', __name__)
bot = Didx_admin_bot()

# Initialize message history list for each user session
def get_message_history():
    if 'message_history' not in session:
        session['message_history'] = []
    return session['message_history']

@didx_app.route('/')
def home():
    return render_template('DIDxBot.html', messages=get_message_history())

@didx_app.route('/chat')
def chat():
    # Get the message history from the URL parameter
    message_history_param = request.args.get('message_history')
    if message_history_param:
        # Decode the URL parameter and parse the JSON string to get the message history
        message_history = json.loads(message_history_param)
    else:
        # If no message history parameter is provided, initialize an empty list
        message_history = []

    # Render the chat template with the message history
    return render_template('DIDxBot.html', messages=message_history)
