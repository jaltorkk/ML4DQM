from flask import Flask, render_template, request, redirect, url_for
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
    
    # Convert comma-separated strings to lists
    training_run_list = training_run_list.split(',')
    test_run_list = test_run_list.split(',')

    # Write the run list files
    with open('runlist_2d_phieta.py', 'w') as f:
        f.write("trainingrunlist = " + str(training_run_list) + "\n")
        f.write("testrunlist = " + str(test_run_list) + "\n")
        f.write("test_MET_tail = False\n")
        f.write("test_2D_phivseta = True\n")

    # Execute the script
    subprocess.run(["python", "ae_2d_phieta.py"], check=True)

    # Collect results (assuming they are generated in the 'static' folder)
    images = os.listdir('static')

    return render_template('result.html', images=images)

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=8001)

