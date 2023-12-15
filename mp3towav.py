from flask import Flask, render_template, request, send_file,Blueprint
from pydub import AudioSegment
import os

mp3towav_app = Blueprint('mp3towav',__name__)

def mp3_to_wav(input_file, output_file):
    audio = AudioSegment.from_mp3(input_file)
    audio.export(output_file, format="wav")

@mp3towav_app.route('/')
def index():
    return render_template('mp3.html')

@mp3towav_app.route('/', methods=['POST'])
def convert():
    try:
        uploaded_file = request.files['file']
        if uploaded_file.filename == '':
            raise ValueError("No file selected")
        
        input_file = "audio/audio.mp3"
        uploaded_file.save(input_file)
        
        output_file = "wav/converted.wav"
        mp3_to_wav(input_file, output_file)

        return send_file(output_file, as_attachment=True)

    except Exception as e:
        error_message = "An error occurred: " + str(e)
        return render_template('mp3.html', error=error_message)



