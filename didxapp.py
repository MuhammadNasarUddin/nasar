from flask import Flask, request, render_template, redirect, url_for, flash,Blueprint
from didx import Didx_admin_bot

didx_app = Blueprint('DIDxBot',__name__)
bot = Didx_admin_bot()

# Initialize message history list
message_history = []

@didx_app.route('/')
def home():
    return render_template('DIDxBot.html', messages=message_history)

@didx_app.route('/chat', methods=['POST'])
def chat():
    if request.method == 'POST':
        if 'user_input' in request.form:
            user_input = request.form['user_input']
            try:
                answer = bot.user_chat(user_input)
            except Exception as e:
                error_message = "An error occurred: " + str(e)
                answer = "Apologies, I am unable to process your request at the moment."

            message_history.append({'type': 'user', 'content':user_input})
            message_history.append({'type': 'bot', 'content':answer})

            return render_template('DIDxBot.html', messages=message_history)
        else:
            flash('Invalid input. Please try again.')
            return redirect(url_for('home'))

