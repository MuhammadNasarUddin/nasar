from flask import Flask, render_template, request, jsonify,Blueprint
import speech_recognition as sr
from openai import OpenAI
import os
from pathlib import Path
from playsound import playsound
import threading
from dotenv import load_dotenv
from pydub import AudioSegment
from pydub.playback import play

callannieapp = Blueprint('callannie',__name__)

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
        with sr.Microphone() as source:
            audio_data = r.listen(source, timeout=duration, phrase_time_limit=duration)

        audio_path = 'audio.wav'
        with open(audio_path, 'wb') as audio_file:
            audio_file.write(audio_data.get_wav_data())

        with sr.AudioFile(audio_path) as source:
            audio_data = r.record(source)
            text = r.recognize_google(audio_data, key=None, language="en-US", show_all=False)
            print("you said:", text)

            # Recognize speech using Google's speech recognition
            transcripted = r.recognize_google(audio_data)

            # Make API call to OpenAI for generating response
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system",
                     "content": "You are a helpful assistant of Rehan Ai. who helps everyone with their queries and gives the right answer "},
                    {"role": "user", "content": "Who are you?"},
                    {"role": "assistant", "content": "As an AI language model, I am programmed to assist you with your queries and concerns to the best of my abilities"},
                    {"role": "user", "content": "Where was it?"},
                    {"role": "user", "content": f"This is the transcribed text: {transcripted}"}
                ]
            )

            # Get AI response content
            response_content = response.choices[0].message.content

            speech_file_path = Path(__file__).parent / "output.mp3"
            audio_response = client.audio.speech.create(
                model="tts-1",
                voice="echo",
                input=response_content
            )
            audio_response.stream_to_file(speech_file_path)

            res_choice = {
                'response_content': response_content,
                'transcripted': transcripted,
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
    response_content = listen()
    return jsonify({'response': response_content})