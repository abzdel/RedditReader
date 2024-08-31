import sys
import os

# Add the src directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from flask import Flask, request, render_template, redirect, url_for
from file_manager import save_title_and_comments, clean_df
from data_handler import read_data, convert_json_to_df, get_title

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process_data():
    url = request.form['url']
    try:
        data = read_data(url)
        title = get_title(data)
        df = convert_json_to_df(data)
        df = clean_df(df)
        save_title_and_comments(title, df)
        return redirect(url_for('success'))
    except Exception as e:
        return f"An error occurred: {e}"

@app.route('/success')
def success():
    return "Processing complete! Check the outputs directory for the results."

if __name__ == "__main__":
    app.run(debug=True)
