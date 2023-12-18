from flask import Flask, render_template, request
from flask import Blueprint
from qrcode import qrcode_app
from password_generator import password_app
from mp3towav import mp3towav_app
from audiototext import audiototext_app
from mp4 import mp4_app




app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

app.register_blueprint(qrcode_app, url_prefix='/qrcode')
app.register_blueprint(password_app, url_prefix='/password')
app.register_blueprint(mp3towav_app, url_prefix='/mp3towav')
app.register_blueprint(audiototext_app, url_prefix='/wavtotext')
app.register_blueprint(mp4_app, url_prefix='/mp4')


if __name__ == "__main__":
    app.run(debug=True,port=8001)