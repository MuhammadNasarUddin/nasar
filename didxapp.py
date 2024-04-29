from flask import Flask, request, render_template, redirect, url_for, flash, session, Blueprint
from didx import Didx_admin_bot

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

@didx_app.route('/chat', methods=['POST'])
def chat():
    if request.method == 'POST':
        user_input = request.form.get('user_input')
        if user_input:
            try:
                answer = bot.user_chat(user_input)
            except Exception as e:
                answer = "Apologies, I am unable to process your request at the moment."

            message_history = get_message_history()
            message_history.append({'type': 'user', 'content': user_input})
            message_history.append({'type': 'bot', 'content': answer})
            session['message_history'] = message_history

            return render_template('DIDxBot.html', messages=message_history)
        else:
            flash('Invalid input. Please try again.')
            return redirect(url_for('home'))

