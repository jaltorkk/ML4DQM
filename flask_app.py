import shutil
import os
import uuid
import time
from flask import Flask, render_template, request
from celery import Celery  # Import Celery
import numpy as np
from ae_2d_phieta import *  # Import the process_runs function
from run_conditions import train_run_2023, test_run_2023
import run_locations

# Set up Flask app
app = Flask(__name__)

# Set up Celery
def make_celery(app):
    celery = Celery(app.import_name, backend=app.config['CELERY_RESULT_BACKEND'], broker=app.config['CELERY_BROKER_URL'])
    celery.conf.update(app.config)
    return celery

# Celery config for Redis
app.config.update(
    CELERY_BROKER_URL='redis://redis:6379/0',  # Example: using Redis as the broker
    CELERY_RESULT_BACKEND='redis://redis:6379/0',  # Store results in Redis
)

celery = make_celery(app)  # Initialize Celery with the Flask app

# Helper function to clear old folders
def clear_old_folders(folder='static', max_age_seconds=3600):
    now = time.time()
    for item in os.listdir(folder):
        path = os.path.join(folder, item)
        if os.path.isdir(path):
            creation_time = os.path.getctime(path)
            if now - creation_time > max_age_seconds:
                try:
                    shutil.rmtree(path)
                    print(f"Deleted old folder: {path}")
                except Exception as e:
                    print(f"Failed to delete {path}. Reason: {e}")

# Define the Celery task
@celery.task
def process_runs_async(training_run_list_str, test_run_list_str, session_folder):
    # Process the runs asynchronously
    training_runs, test_runs = run_locations.process_runs(training_run_list_str, test_run_list_str)
    run_analysis(training_run_list_str, test_run_list_str, output_dir=session_folder)

    # Filter out CMS logo
    images = [img for img in os.listdir(session_folder) if img.lower() not in ['cms_logo.png', 'cms_logo.jpg']]
    images = [f"{session_folder}/{img}" for img in images if img.lower().endswith(('.png', '.jpg', '.jpeg'))]

    return training_runs, test_runs, images

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/result', methods=['POST'])
def result():
    # Clear existing PNG files in the 'static' folder before generating new ones
    clear_old_folders()

    # Generate unique session ID and folder
    session_id = str(uuid.uuid4())
    session_folder = os.path.join('static', session_id)
    os.makedirs(session_folder, exist_ok=True)

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

    # Call the Celery task asynchronously
    task = process_runs_async.apply_async(args=[training_run_list_str, test_run_list_str, session_folder])

    # You can return a task ID or a page indicating the task is in progress
    return render_template('task_in_progress.html', task_id=task.id)

@app.route('/task_status/<task_id>')
def task_status(task_id):
    task = process_runs_async.AsyncResult(task_id)

    # Check task status and display the result when done
    if task.state == 'SUCCESS':
        training_runs, test_runs, images = task.result
        return render_template('result.html', training_runs=training_runs, test_runs=test_runs, images=images)
    elif task.state == 'PENDING':
        return f"Task {task_id} is pending. Please wait..."
    else:
        return f"Task {task_id} failed with state {task.state}"

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8001)
