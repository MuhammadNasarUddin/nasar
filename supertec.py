from flask import Flask, render_template, request, redirect, url_for, flash, session,Blueprint
from bot import supertec_bot

supertec = supertec_bot()

supertec_app = Blueprint('bot',__name__)
message_history = []

@supertec_app.route('/')
def index():
    if 'logged_in' not in session or not session['logged_in']:
        return redirect(url_for('bot.login'))
    return render_template('supertec.html', messages=message_history)

@supertec_app.route('/chat', methods=['POST'])
def chat():
    if request.method == 'POST':
        # Check if 'user_input' is in the form data
        if 'user_input' in request.form:
            user_input = request.form['user_input']
            try:
                answer = supertec.user_chat(user_input)
            except Exception as e:
                # Handle the exception, you might want to log the error or take other actions
                error_message = f"Error: {e}"
                # For simplicity, let's display an error message instead of the bot's response
                answer = "Apologies, there was an error processing your request."

            # Append the user and bot messages to message_history
            message_history.append({'type': 'user', 'content': user_input})
            message_history.append({'type': 'bot', 'content': answer})

            return render_template('supertec.html', messages=message_history)

        else:
            # Handle the case where 'user_input' is not present in the form data
            flash('Invalid request. Please provide a valid input.', 'error')
            return redirect(url_for('index'))

@supertec_app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        if email == "admin@gmail.com" and password == "admin123":
            session['logged_in'] = True
            return redirect(url_for('bot.index'))
        else:
            flash('Invalid credentials. Please try again.', 'error')
            return redirect(url_for('bot.login'))
    return render_template('login.html')



