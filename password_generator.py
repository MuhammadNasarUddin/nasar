from flask import Flask, render_template, request,Blueprint
import string
import random

password_app = Blueprint('passowrd',__name__)

def generate_password(length=12, use_symbols=True):
    try:
        characters = string.ascii_letters + string.digits
        if use_symbols:
            characters += string.punctuation

        password = ''.join(random.choice(characters) for _ in range(length))
        return password
    except Exception as e:
        return f"Error generating password: {str(e)}"

@password_app.route('/', methods=['GET', 'POST'])
def index():
    generated_password = ''
    error_message = ''

    if request.method == 'POST':
        try:
            password_length = int(request.form['password_length'])
            include_symbols = 'include_symbols' in request.form
            generated_password = generate_password(password_length, include_symbols)
        except ValueError:
            error_message = 'Invalid password length entered'
        except Exception as e:
            error_message = f"Error generating password: {str(e)}"

    return render_template('password_generator.html', generated_password=generated_password, error_message=error_message)
