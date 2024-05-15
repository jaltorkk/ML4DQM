from flask import Flask, render_template, request, send_file,redirect,url_for, Response, redirect

app = Flask(__name__)
#,static_folder="static", template_folder="templates")
#import sys
#import os

@app.route('/')
#, methods=['GET','POST'])
def index():
    return render_template('index.html')

@app.route('/result', methods=['POST'])
def result():
    training_data = request.form['training_data']
    testing_data = request.form['testing_data']
    # Process the data and generate images (replace this with your ML code)
    images = ['image1.jpg', 'image2.jpg', 'image3.jpg']
    return render_template('result.html', images=images)

if __name__ == '__main__':
    app.run(debug=True)
    




#def Menu_func():
#    import os
#    
#    return render_template('Frontpage.html')



#if __name__ == "__main__":
#    app.run(debug=True,host='localhost',port=8001)
