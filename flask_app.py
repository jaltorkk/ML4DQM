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

    # Write the run list files
    #with open('runlist_2d_phieta.py', 'w') as f:
    #    f.write("trainingrunlist = " + str(training_run_list) + "\n")
    #    f.write("testrunlist = " + str(test_run_list) + "\n")
     #   f.write("test_MET_tail = False\n")
     #   f.write("test_2D_phivseta = True\n")
    
    try:
        with open('static/runlist_2d_phieta.py', 'w') as f:
            f.write("trainingrunlist = " + str(training_run_list) + "\n")
            f.write("testrunlist = " + str(test_run_list) + "\n")
            f.write("test_MET_tail = False\n")
            f.write("test_2D_phivseta = True\n")
    except Exception as e:
        app.logger.error(f"Error writing run list files: {e}")
        return "An error occurred while writing run list files.", 500

    # Execute the script
    subprocess.run(["python", "ae_2d_phieta.py"], check=True)

    # Collect results (assuming they are generated in the 'static' folder)
    images = os.listdir('static')

    return render_template('result.html', images=images)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8001)

