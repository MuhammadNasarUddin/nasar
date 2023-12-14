from flask import Flask, render_template, request
import subprocess

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/runcode', methods=['POST'])
def run_code():
    code = request.form['code']
    language = request.form['language']

    # Mapping of file extensions to programming languages
    extensions = {
        'python': 'py',
        'javascript': 'js',
        # Add more languages here
    }

    # Get the file extension based on the selected language
    extension = extensions.get(language)

    if extension:
        # Write the code to a temporary file
        filename = f'temp.{extension}'
        with open(filename, 'w') as file:
            file.write(code)

        # Execute the code using subprocess
        try:
            result = subprocess.run([language, filename], capture_output=True, text=True, timeout=10)
            output = result.stdout
            error = result.stderr
        except subprocess.TimeoutExpired:
            output = "Execution timed out"
            error = ""
        
        # Remove the temporary file
        subprocess.run(['rm', filename])

        return output if not error else error
    else:
        return "Invalid language selected"

if __name__ == '__main__':
    app.run(debug=True)
