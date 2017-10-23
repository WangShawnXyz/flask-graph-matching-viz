# -*- coding: utf-8 -*-


import os
import graph as g
from flask import Flask, render_template, request, flash, jsonify
from flask import redirect, send_from_directory, make_response
from flask_dropzone import Dropzone
import datetime
import hashlib
import shutil
import random

app = Flask(__name__)
dropzone = Dropzone(app)
app.config.update(
    UPLOADED_PATH=os.getcwd() + '/upload',
    DROPZONE_ALLOWED_FILE_TYPE='text',
    DROPZONE_MAX_FILE_SIZE=20,
    DROPZONE_INPUT_NAME='text',
    DROPZONE_MAX_FILES=30,
    SECRET_KEY='This is a very SECRET key!',
    EXE_PATH=os.getcwd()+'/GMA',
    RESULT_DIR=os.getcwd()+'/RESULT'
)

def __gen_txt_md5(path):
    '''
        生成文件的md5
    '''
    md5 = str(random.randint(1000, 9999))
    try:
        content = open(path)
        content = open(path, "r", encoding="utf-8").read().encode("utf-8")
        md5 = hashlib.md5(content).hexdigest()
    except Exception as e:
        md5 = str(random.randint(1000, 9999))
        raise e

        
    return md5

    

def gen_dir_name(pathA, pathB):

     #根据文本md5值生成文件夹名
    md5s = []
    md5s.append(__gen_txt_md5(pathA))
    md5s.append(__gen_txt_md5(pathB))
    md5s.sort()
    dir_name = md5s[0] + md5s[1]
    return dir_name

def set_cookie(func): 
    '''
      #装饰器 如果请求没有文件随机码 生成一个存到cookie里面
    '''    
    def wrapper(*wargs, **kwargs):
        if request.cookies.get("file"):
            pass
        return func(*wargs, **kwargs)
    return wrapper


@app.route("/set_cookie")
def set_cookie():
    response = make_response(render_template(""))
    pass
@app.route('/index')
def index():
    return render_template("index.html", title="Index")


@app.route('/upload', methods=['POST', 'GET'])
@app.route('/', methods=['POST', 'GET'])
def upload():
    '''
    #文件上传
    '''
    if request.method == 'POST':
        f = request.files.get('text')
        f.save(os.path.join(app.config['UPLOADED_PATH'], f.filename))
    return render_template('upload.html')

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
        try:
            with open(path) as f:
                s = f.read()
        except Exception as e:
            s = '(This file seems cannot open)'
        
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
    '''
        #开始图匹配
    '''
    files_list = os.listdir(app.config['UPLOADED_PATH'])
    graphA = request.form.get("graphA")
    graphB = request.form.get("graphB")
    if not ( graphA and graphB):
        return render_template("matching.html", files_list=files_list)
    pathA = os.path.join(app.config['UPLOADED_PATH'], graphA)
    pathB = os.path.join(app.config['UPLOADED_PATH'], graphB)
    files_list = os.listdir(app.config['UPLOADED_PATH'])
    if(graphA in files_list and graphB in files_list):    #确认选定了两个文件
        # cmd = app.config["EXE_PATH"] + "/add.exe " + pathA \
        #     + " " + pathB + " " + app.config["EXE_PATH"] + "/result.txt"
        # os.popen(cmd)

        dir_name = gen_dir_name(pathA, pathB)
        #判断目录是否存在/如果说目录已经存在 那么曾经计算过,直接可视化， 否则进行图匹配
        # f = open("log.txt", "a")
        # f.write(app.config["RESULT_DIR"] + "/" + dir_name + "\n")
        # f.close()
        if os.path.isdir(app.config["RESULT_DIR"] + "/" + dir_name):

            return render_template("viz.html", graphA="", graphB="", result="")
        else:
            #在result目录下，创建新目录
            worked_dir = app.config["RESULT_DIR"] + "/" +dir_name
            os.mkdir(worked_dir)
            new_pathA = os.path.join(worked_dir, "graphA.txt")
            new_pathB = os.path.join(worked_dir, "graphB.txt")
            shutil.copy(pathA, new_pathA)
            shutil.copy(pathB, new_pathB)
            cmd = os.path.join(app.config["EXE_PATH"], "/add.exe") +" " + new_pathA \
            + " " + new_pathB + " " + worked_dir + "/result.txt"
            os.popen(cmd)
            #  # 测试
            # f = open("log.txt", "a")
            # f.write(cmd+"\n")
            # f.close()
            response = make_response(render_template("result.html"))
            response.set_cookie('worked_dir', worked_dir)
            return response

        return redirect("/result")
    return render_template("matching.html", files_list=files_list)

# @app.route('/set_cookie')  
# def set_cookie():  
#     response=make_response('Hello World');  
#     response.set_cookie('Name','Hyman')  
#     return response  

@app.route('/graph/<source>/<match>')#获取匹配数据
def general(source, match):
    elements = g.getNodePairs("./upload/"+ match +".txt", g.getGraph("./upload/"+ source +".txt"))
    return jsonify(elements=elements)
@app.route('/result')
def result():
    worked_dir = request.cookies.get("worked_dir")
    if worked_dir:
        files_list = os.listdir(worked_dir)
        return render_template('result.html', files_list=files_list)
    else:
        flash("Please marke sure you have uploaded your graph file and matched it.")
        return redirect("/upload")
def __stamp2datetime(timestamp):
    try:  
        d = datetime.datetime.fromtimestamp(timestamp)  
        str1 = d.strftime("%Y-%m-%d %H:%M:%S")  
        # 2015-08-28 16:43:37.283000'  
        return str1  
    except Exception as e:  
        print(e)
        return ''
def __convert_size(size):
    s = ''
    if size/1024>  1024:
        s = str(size/1024) + ' M '
    elif size/1024 >= 1:
        s = str(size/1024.0) + ' K '
    else:
        s = str(size) + ' B '
    return s
@app.route('/view/<filename>')
def view(filename):
    path = app.config['EXE_PATH']+ "/" +filename
    # print(path)
    detail = {}
    s = ""
    files_list = os.listdir(app.config['EXE_PATH'])
    if os.path.exists(path):

        detail['atime'] = __stamp2datetime(os.path.getatime(path))
        detail['ctime'] = __stamp2datetime(os.path.getctime(path))
        detail['mtime'] = __stamp2datetime(os.path.getmtime(path))
        size = os.path.getsize(path)
        detail['size'] = size
        try:
            with open(path) as f:
                s = f.read()
        except Exception as e:
            s = "(This file seems cannot open)"
    else:
        flash("File not exists.")
    return render_template('result.html', files_list=files_list, overview=s, detail=detail)
@app.route('/download/<filename>', methods=['GET'])
def download(filename):
    if request.method == "GET":
        if os.path.isfile(os.path.join(app.config['EXE_PATH'], filename)):
            return send_from_directory(app.config['EXE_PATH'], filename, as_attachment=True)
        # abort(404)

@app.route("/viz")
def viz():

    return render_template('viz.html')
@app.route("/gettest")
def gettest():
    elements = g.getFullGraph("")
    return jsonify(elements=elements)

if __name__ == '__main__':
    # print(os.getcwd())
    app.run(debug=True)
    # print(__convert_size(1024))
    # print(__convert_size(1024*1024*1024))
    # print(__convert_size(102))

