from flask import Flask, render_template, request
import os
import numpy as np
from ae_2d_phieta import process_runs  # Import the process_runs function
from run_conditions import train_run_2023, test_run_2023

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/result', methods=['POST'])
def result():
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
    training_runs, test_runs, training_lists, test_lists, norm_list_phieta_train, norm_list_phieta_test = process_runs(training_run_list_str, test_run_list_str)

    
    # Normalize training and test runs
    max_train = max(norm_list_phieta_train) if norm_list_phieta_train else 1
    max_test = max(norm_list_phieta_test) if norm_list_phieta_test else 1

    training_list = np.array(training_lists)  
    test_list = np.array(test_lists)
    training_list = training_list / max_train 
    test_list = test_list / max_test

    n_train1 = training_list.shape[0]
    n_test1 = test_list.shape[0]

    # Collect results (assuming they are generated in the 'static' folder)
    images = os.listdir('static')

    return render_template('result.html', 
                           training_runs=training_runs,
                           test_runs=test_runs,
                           n_train1=n_train1, 
                           training_list_shape=training_list.shape,
                           n_test1=n_test1, 
                           test_list_shape=test_list.shape,
                           images=images,
                           warnings=all_warnings)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8001)




