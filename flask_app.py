from flask import Flask, render_template, request
import os
import subprocess

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/result', methods=['POST'])
def result():
    training_run_list = request.form['training_run_list']
    test_run_list = request.form['test_run_list']

    # Execute the run_locations.py script with the provided run lists
    training_run_list_str = training_run_list.replace(" ", "")
    test_run_list_str = test_run_list.replace(" ", "")
    
    result = subprocess.run(
        ["python3", "run_locations.py", training_run_list_str, test_run_list_str],
        capture_output=True, text=True
    )
    
    print(result.stdout)  # Print script output
    print(result.stderr)  # Print script error, if any

    # Collect results (assuming they are generated in the 'static' folder)
    images = os.listdir('static')

    return render_template('result.html', images=images)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8001)


