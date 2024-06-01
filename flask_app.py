from flask import Flask, render_template, request
import subprocess
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
    training_run_list = [int(run.strip()) for run in training_run_list.split(',')]
    test_run_list = [int(run.strip()) for run in test_run_list.split(',')]

    # Validate run lists
    valid_training_runs = train_run_2023(training_run_list)
    valid_test_runs = test_run_2023(test_run_list)

    # Handle errors or warnings in validation
    if isinstance(valid_training_runs, str):
        return f"Error in training run list: {valid_training_runs}"
    if isinstance(valid_test_runs, str):
        return f"Error in test run list: {valid_test_runs}"

    # Now you can use these valid runs in your subprocess call
    training_run_list_str = str(valid_training_runs)
    test_run_list_str = str(valid_test_runs)

    # Execute the run_locations.py script with the provided run lists
    result = subprocess.run(
        ["python3", "run_locations.py", training_run_list_str, test_run_list_str],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True
    )

    print(result.stdout)  # Print script output
    print(result.stderr)  # Print script error, if any

    # Collect results (assuming they are generated in the 'static' folder)
    images = os.listdir('static')

    return render_template('result.html', images=images)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8001)




