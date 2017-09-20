# -*- coding: utf-8 -*-
import os
import graph as g
from flask import Flask, render_template, request, flash, jsonify, redirect
from flask_dropzone import Dropzone

app = Flask(__name__)
dropzone = Dropzone(app)
pair = None
app.config.update(
    UPLOADED_PATH=os.getcwd() + '/upload',
    DROPZONE_ALLOWED_FILE_TYPE='text',
    DROPZONE_MAX_FILE_SIZE=20,
    DROPZONE_INPUT_NAME='text',
    DROPZONE_MAX_FILES=30,
    SECRET_KEY='I have a dream'
)

@app.route('/index', methods=['POST', 'GET'])
@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        f = request.files.get('text')
        f.save(os.path.join(app.config['UPLOADED_PATH'], f.filename))
    return render_template('index.html')

@app.route('/manage')
def manage():
    files_list = os.listdir(app.config['UPLOADED_PATH'])
    return render_template('manage.html', files_list=files_list)
    
@app.route('/open/<filename>')
def open_file(filename):
    path = app.config['UPLOADED_PATH']+ "/" +filename
    # print(path)
    s = ''
    files_list = os.listdir(app.config['UPLOADED_PATH'])
    if os.path.exists(path):
        with open(path) as f:
            s = f.read()
    else:
        flash("File not exists.")
    return render_template('manage.html', files_list=files_list, overview=s)
@app.route('/delete/<filename>')
def delete_file(filename):
    path = app.config['UPLOADED_PATH'] + "/" + filename
    files_list = os.listdir(app.config['UPLOADED_PATH'])
    if os.path.exists(path):
       os.remove(path)
       flash("Del successfully!")
    else:
        flash("File not exists.")
    files_list = os.listdir(app.config['UPLOADED_PATH'])
    return render_template('manage.html',files_list=files_list)

@app.route('/matching', methods=['GET','POST'])
def matching():
    files_list = os.listdir(app.config['UPLOADED_PATH'])
    graphA = request.form.get("graphA")
    graphB = request.form.get("graphB")
    pair = (graphA, graphB)
    files_list = os.listdir(app.config['UPLOADED_PATH'])
    if(pair[0] in files_list and pair[1] in files_list):    #确认选定了两个文件

        return redirect("/result")
    return render_template("matching.html", files_list=files_list)

@app.route('/graph/<source>/<match>')
def general(source, match):
    elements = g.getNodePairs("./upload/"+ match +".txt", g.getGraph("./upload/"+ source +".txt"))
    return jsonify(elements=elements)
@app.route('/result')
def result():
    return render_template("result.html", pair = pair)
if __name__ == '__main__':
    app.run(debug=True)
