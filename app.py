from flask import Flask, render_template, request, Blueprint
from qrcode import qrcode_app
from password_generator import password_app
from mp3towav import mp3towav_app
from audiototext import audiototext_app
from mp4 import mp4_app
from resizer import resizer_app
from supertec import supertec_app
from flask import Flask
import solara.server.flask



app = Flask(__name__)
app.secret_key = 'nasar123'  # Set a secret key for session management
app.register_blueprint(solara.server.flask.blueprint, url_prefix="/solara/")
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # Allow up to 10 megabytes


@app.route('/')
def index():
    return render_template('index.html')

app.register_blueprint(qrcode_app, url_prefix='/qrcode')
app.register_blueprint(password_app, url_prefix='/password')
app.register_blueprint(mp3towav_app, url_prefix='/mp3towav')
app.register_blueprint(audiototext_app, url_prefix='/wavtotext')
app.register_blueprint(mp4_app, url_prefix='/mp4')
app.register_blueprint(resizer_app, url_prefix='/resizer')
app.register_blueprint(supertec_app, url_prefix='/bot')



if __name__ == "__main__":
    app.run(debug=True, port=8001)
