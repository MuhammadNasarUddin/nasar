from flask import Flask, render_template, request, redirect, url_for, send_file,Blueprint
from PIL import Image
import io

resizer_app = Blueprint('resizer',__name__)

@resizer_app.route('/')
def index():
    return render_template('resizer.html')

@resizer_app.route('/resize', methods=['POST'])
def resize():
    if 'file' not in request.files:
        return redirect(request.url)

    file = request.files['file']

    if file.filename == '':
        return redirect(request.url)

    try:
        img = Image.open(io.BytesIO(file.read()))
        width = int(request.form['width'])
        height = int(request.form['height'])

        resized_img = img.resize((width, height))
        output = io.BytesIO()
        resized_img.save(output, format='JPEG')  # Change format if desired (JPEG, PNG, etc.)

        output.seek(0)
        return send_file(
            output,
            mimetype='image/jpeg',
            as_attachment=True,  # Forces browser to download the file instead of displaying it
            download_name='resized_image.jpg'  # Change the filename as needed
        )

    except Exception as e:
        return f"An error occurred: {str(e)}"

