from flask import Flask, render_template, request, jsonify, Blueprint, send_from_directory
import speech_recognition as sr
from openai import OpenAI
import os
from pathlib import Path
from playsound import playsound
import threading
from dotenv import load_dotenv

callannieapp = Blueprint('rehanaiv1', __name__ ,static_url_path='/static')

speech_file_path = Path("static") / "output.mp3"


# Load environment variables from .env
load_dotenv()

client = OpenAI(api_key=os.environ['openai_api_key'])

# Initialize the recognizer
r = sr.Recognizer()
sample_rate = 44100
duration = 5
r.energy_threshold = 4000
r.dynamic_energy_threshold = True
r.dynamic_energy_adjustment_damping = 0.15
r.dynamic_energy_ratio = 1.5





@callannieapp.route('/')
def home():
    return render_template('callannie.html')


def listen():
    try:    
            
            data = request.get_json()
            transcript = data['transcript']
        
            # Make API call to OpenAI for generating response
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system",
                     "content": "You are a helpful assistant of Rehan Ai. who helps everyone with their queries and gives the right answer "},
                    {"role": "user", "content": "Who are you?"},
                    {"role": "assistant", "content": "As an AI language model, I am programmed to assist you with your queries and concerns to the best of my abilities"},
                    {"role": "user", "content": "Where was it?"},
                    {"role": "user", "content": f"This is the transcribed text: {transcript}"}
                ]
            )

            # Get AI response content
            response_content = response.choices[0].message.content

            audio_response = client.audio.speech.create(
                model="tts-1",
                voice="nova",
                input=response_content
            )
            audio_response.stream_to_file(speech_file_path)

            res_choice = {
                'response_content': response_content,
                'transcript': transcript,
            }

            # Play the generated audio in a separate thread
            threading.Thread(target=playsound, args=(str(speech_file_path),)).start()

            return res_choice

    except sr.WaitTimeoutError:
        return 'No speech detected within the timeout period.'
    except sr.UnknownValueError:
        return 'Could not understand audio'
    except sr.RequestError as e:
        return f'Request to Google API failed: {e}'
    except Exception as e:
        return f'An unexpected error occurred: {e}'


@callannieapp.route('/process_audio', methods=['POST'])
def process_audio():
    try:
        response_content = listen()
        return jsonify(response_content)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    



@callannieapp.route('/static/<filename>')
def serve_static(filename):
    return send_from_directory(callannieapp.static_folder, filename)


