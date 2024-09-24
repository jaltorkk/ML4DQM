import os
from flask import Flask, render_template, request, redirect, url_for, flash
from celery import Celery
import run_locations
from run_conditions import train_run_2023, test_run_2023

app = Flask(__name__)
app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'

celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)

@celery.task
def process_runs(training_runs, test_runs):
    # Perform the long-running task here
    training_runs, test_runs = run_locations.process_runs(training_runs, test_runs)
    return training_runs, test_runs

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/result', methods=['POST'])
def result():
    training_run_list = request.form['training_run_list']
    test_run_list = request.form['test_run_list']

    # Validate and process run lists
    valid_training_runs, training_warnings = train_run_2023(training_run_list.split(','))
    valid_test_runs, test_warnings = test_run_2023(test_run_list.split(','))

    if isinstance(valid_training_runs, str) or isinstance(valid_test_runs, str):
        return "Invalid runs provided."

    # Trigger the Celery task
    task = process_runs.apply_async(args=(valid_training_runs, valid_test_runs))
    
    return redirect(url_for('task_status', task_id=task.id))

@app.route('/status/<task_id>')
def task_status(task_id):
    task = process_runs.AsyncResult(task_id)
    if task.state == 'PENDING':
        response = {
            'state': task.state,
            'status': 'Pending...'
        }
    elif task.state != 'FAILURE':
        response = {
            'state': task.state,
            'result': task.result,
            'status': 'Processing...'
        }
    else:
        response = {
            'state': task.state,
            'status': str(task.info),  # this is the exception raised
        }
    return render_template('status.html', response=response)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8001)
