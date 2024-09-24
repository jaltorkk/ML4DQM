from flask import Flask, render_template, request
from celery import Celery
import os
import numpy as np
from ae_2d_phieta import *  # Import the process_runs function
from run_conditions import train_run_2023, test_run_2023
import run_locations

app = Flask(__name__)

# Configure Celery
app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'
celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)

# Long-running task to process runs
@celery.task
def process_runs_task(training_run_list_str, test_run_list_str):
    # Validate run lists
    valid_training_runs, training_warnings = train_run_2023(training_run_list_str.split(','))
    valid_test_runs, test_warnings = test_run_2023(test_run_list_str.split(','))

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

    return {
        'training_runs': training_runs,
        'test_runs': test_runs,
        'images': images,
        'warnings': all_warnings
    }

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/result', methods=['POST'])
def result():
    training_run_list = request.form['training_run_list']
    test_run_list = request.form['test_run_list']

    # Convert run lists to strings
    training_run_list_str = ','.join(run.strip() for run in training_run_list.split(','))
    test_run_list_str = ','.join(run.strip() for run in test_run_list.split(','))

    # Start the Celery task
    task = process_runs_task.apply_async(args=[training_run_list_str, test_run_list_str])

    # Return a message to the user indicating that the task has started
    return f"Task started! Check back later for results. Task ID: {task.id}"

@app.route('/result/<task_id>')
def get_result(task_id):
    task = process_runs_task.AsyncResult(task_id)

    if task.state == 'PENDING':
        return "Task is still processing..."
    elif task.state != 'FAILURE':
        result = task.result
        return render_template('result.html', 
                               training_runs=result['training_runs'],
                               test_runs=result['test_runs'],
                               images=result['images'],
                               warnings=result['warnings'])
    else:
        return f"Task failed: {task.info}"

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8001)
