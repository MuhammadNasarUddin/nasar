from flask import Flask, render_template, request,Blueprint
import pyqrcode
import io
import base64

qrcode_app = Blueprint('qrcode',__name__)

def generate_qr_code(link, file_type, scale):
    try:
        qr = pyqrcode.create(link)
        img = io.BytesIO()

        if file_type == 'SVG':
            qr.svg(img, scale=scale)
        elif file_type == 'PNG':
            qr.png(img, scale=scale)    

        img.seek(0)
        return img
    except Exception as e:
        return str(e)

@qrcode_app.route('/')
def index():
    return render_template('qrcode.html')

@qrcode_app.route('/', methods=['POST'])
def generate():
    link = request.form['link']
    file_type = request.form['file_type']
    scale = int(request.form['scale'])

    img = generate_qr_code(link, file_type, scale)

    if isinstance(img, str):  # Check if img is an error message
        return render_template('qrcode.html', error_message=img)
    else:
        if file_type == 'SVG':
            encoded_svg = base64.b64encode(img.getvalue()).decode('utf-8')
            svg_data = 'data:image/svg+xml;base64,' + encoded_svg
            return render_template('qrcode.html', svg_data=svg_data)
        elif file_type == 'PNG':
            encoded_png = base64.b64encode(img.getvalue()).decode('utf-8')
            png_data = 'data:image/png;base64,' + encoded_png
            return render_template('qrcode.html', png_data=png_data)
