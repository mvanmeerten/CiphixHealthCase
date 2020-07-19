from flask import Flask, request, jsonify, flash, url_for, redirect, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os
import boto3
from werkzeug.utils import secure_filename
from tika import parser


client = boto3.client(service_name='comprehendmedical', region_name='eu-west-2')

# Init app
UPLOAD_FOLDER = 'C:/Users/Martijn/PycharmProjects/CiphixHealthCase/PredictAPI/docs'
ALLOWED_EXTENSIONS = {'txt', 'pdf'}
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
basedir = os.path.abspath(os.path.dirname(__file__))
# Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Init db
db = SQLAlchemy(app)
# Init marshmallow
ma = Marshmallow(app)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            text = parser.from_file(filepath)['content']
            result = client.detect_entities(Text=text)
            # return jsonify(result['Entities'])
            return text

            # return redirect(url_for('uploaded_file',
            #                         filename=filename))
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


# @app.route('/', methods=['POST'])
# def extract_entities():
#     data = request.get_json()
#     print(data)
#     # result = client.detect_entities(Text='cerealx 84 mg daily')
#     result = client.detect_entities(Text=data['text'])
#     entities = result['Entities']
#     for entity in entities:
#         print('Entity', entity)
#     return jsonify(entities)


# Run server
if __name__ == '__main__':
    app.run()
