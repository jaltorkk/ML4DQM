import shutil
from flask import Flask, render_template, request
import os
import numpy as np
from ae_2d_phieta import *  # Import the process_runs function
from run_conditions import train_run_2023, test_run_2023
import run_locations

def clear_static_folder():
    folder = 'static'
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            # Check if the file is a PNG before deleting
            if filename.endswith('.png') and os.path.isfile(file_path):
                os.unlink(file_path)  # Remove the file
        except Exception as e:
            print(f"Failed to delete {file_path}. Reason: {e}")

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/result', methods=['POST'])
def result():
    # Clear existing PNG files in the 'static' folder before generating new ones
    clear_static_folder()
    
    training_run_list = request.form['training_run_list']
    test_run_list = request.form['test_run_list']

    # Convert run lists to lists of integers
    training_run_list = [run.strip() for run in training_run_list.split(',')]
    test_run_list = [run.strip() for run in test_run_list.split(',')]

    # Validate run lists
    valid_training_runs, training_warnings = train_run_2023(training_run_list)
    valid_test_runs, test_warnings = test_run_2023(test_run_list)

    # Handle errors or warnings in validation
    if isinstance(valid_training_runs, str):
        return f"Error in training run list: {valid_training_runs}"
    if isinstance(valid_test_runs, str):
        return f"Error in test run list: {valid_test_runs}"

    # Combine warnings
    all_warnings = training_warnings + test_warnings

    # Now you can use these valid runs in your function call
    training_run_list_str = ','.join(valid_training_runs)
    test_run_list_str = ','.join(valid_test_runs)

    # Process the runs using process_runs function
    training_runs, test_runs = run_locations.process_runs(training_run_list_str, test_run_list_str)

    # Collect results (assuming they are generated in the 'static' folder)
    run_analysis(training_run_list_str, test_run_list_str)
    images = os.listdir('static')

    # Filter out CMS logo
    images = [img for img in os.listdir('static') if img.lower() not in ['cms_logo.png']]  

    return render_template('result.html', 
                           training_runs=training_runs,
                           test_runs=test_runs,
                           images=images,
                           warnings=all_warnings)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8001)




