from celery import Celery
from flask import Flask, render_template, request, url_for, redirect
import os
import time

app = Flask(__name__)
celery = Celery(app.name, broker='redis://localhost:6379/0')

@app.route('/')
def index():
    return render_template('index.html')

# Celery Task for processing runs
@celery.task(bind=True)
def process_runs_task(self, training_run_list_str, test_run_list_str):
    # Simulate a long process
    from run_locations import process_runs
    from ae_2d_phieta import run_analysis
    run_analysis(training_run_list_str, test_run_list_str)
    return 'Done'

@app.route('/submit', methods=['POST'])
def submit():
    # Get the run list inputs
    training_run_list = request.form['training_run_list']
    test_run_list = request.form['test_run_list']

    # Convert run lists to lists of integers
    training_run_list = [run.strip() for run in training_run_list.split(',')]
    test_run_list = [run.strip() for run in test_run_list.split(',')]

    # Trigger background task
    task = process_runs_task.apply_async(args=[','.join(training_run_list), ','.join(test_run_list)])
    
    # Redirect to the loading page with the task ID
    return redirect(url_for('loading', task_id=task.id))

@app.route('/loading/<task_id>')
def loading(task_id):
    return render_template('loading.html', task_id=task_id)

@app.route('/result/<task_id>')
def result(task_id):
    # Fetch the task status and return result page
    task = celery.AsyncResult(task_id)
    if task.state == 'SUCCESS':
        images = os.listdir('static')
        return render_template('result.html', images=images)
    else:
        return "Task still running or failed", 202

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8001)




