from flask import Blueprint, request, jsonify
from didx import Didx_admin_bot

# Create a blueprint
didx_blueprint = Blueprint('didx_blueprint', __name__)

# Initialize DIDx admin bot
bot = Didx_admin_bot()

@didx_blueprint.route('/chat', methods=['POST'])
def chat():
    if request.method == 'POST':
        if 'user_input' in request.json:
            user_input = request.json['user_input']
            try:
                answer = bot.user_chat(user_input)
            except Exception as e:
                error_message = "An error occurred: " + str(e)
                answer = "Apologies, I am unable to process your request at the moment."

            response = {
                'user_input': user_input,
                'bot_response': answer
            }

            return jsonify(response), 200
        else:
            error_response = {'error': 'Invalid input. Please provide user_input in JSON format.'}
            return jsonify(error_response), 400

