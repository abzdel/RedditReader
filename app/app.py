import sys
import os
import subprocess
from flask import Flask, request, render_template, redirect, url_for

# Add the src directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from data_handler import read_data, convert_json_to_df, get_title
from file_manager import save_title_and_comments, clean_df

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process_data():
    url = request.form['url']
    try:
        # Call your main.py script
        result = subprocess.run(['python', 'src/main.py', url], capture_output=True, text=True)
        if result.returncode == 0:
            return redirect(url_for('success'))
        else:
            return f"Error: {result.stderr}"
    except Exception as e:
        return f"An error occurred: {e}"

@app.route('/success')
def success():
    return "Processing complete! Check the outputs directory for the results."

if __name__ == "__main__":
    app.run(debug=True)
