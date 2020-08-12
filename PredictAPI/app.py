import os

import boto3
from flask import Flask, request, flash, redirect, render_template, send_from_directory, url_for, jsonify
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from tika import parser
from werkzeug.utils import secure_filename
from wtforms import SubmitField

client = boto3.client(service_name='comprehendmedical', region_name='eu-west-2')

# Init app
UPLOAD_FOLDER = 'C:/Users/Martijn/PycharmProjects/CiphixHealthCase/PredictAPI/docs'
ALLOWED_EXTENSIONS = {'txt', 'pdf'}
app = Flask(__name__)
app.config["SECRET_KEY"] = "secret"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def parse_entities(entity_list):
    result = ""
    print(entity_list)
    for entity in entity_list:
        print(type(entity))
        result += entity['Text'] + ", category: " + entity['Category'] + ', type: ' + entity['Type'] + '\n'
        if entity['Attributes']:
            for attribute in entity['Attributes']:
                result += '- ' + attribute['Text'] + ', type: ' + attribute['Type'] + os.linesep

    print(result)
    return result


@app.route('/', methods=['get', 'POST'])
def index():
    form = UploadForm()
    if request.method == "POST":
        if form.validate_on_submit():
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
                # print(jsonify(result['Entities']).content)

                # return jsonify(result['Entities'])
                print(type(result['Entities']))
                # entities = parse_entities(result['Entities'])
                return render_template('index.html', form=form, entities=result['Entities'], text=text)
                # return redirect(url_for('uploaded_file', filename=filename))
    text = 'Pt is 87 yo woman, highschool teacher with past medical history that includes - status post cardiac catheterization in April 2019. She presents today with palpitations and chest pressure. HPI : Sleeping trouble on present dosage of Clonidine. Severe Rash on face and leg, slightly itchy Meds : Vyvanse 50 mgs po at breakfast daily, Clonidine 0.2 mgs -- 1 and 1 / 2 tabs po qhs HEENT : Boggy inferior turbinates, No oropharyngeal lesion Lungs : clear Heart : Regular rhythm Skin : Mild erythematous eruption to hairline Follow-up as scheduled'
    result = client.detect_entities(Text=text)
    return render_template('index.html', form=form, entities=result['Entities'], text=text)


@app.route('/display/<filename>')
def display_doc(filename):
    return redirect(url_for('uploaded_file', filename='docs/' + filename), code=301)


class UploadForm(FlaskForm):
    file = FileField(validators=[
        FileRequired(),
        FileAllowed(ALLOWED_EXTENSIONS, 'Only txt and pdf files are allowed.')
    ])
    submit = SubmitField("submit")


# def upload_file():
#     if request.method == 'POST':
#         # check if the post request has the file part
#         if 'file' not in request.files:
#             flash('No file part')
#             return redirect(request.url)
#         file = request.files['file']
#         # if user does not select file, browser also
#         # submit an empty part without filename
#         if file.filename == '':
#             flash('No selected file')
#             return redirect(request.url)
#         if file and allowed_file(file.filename):
#             filename = secure_filename(file.filename)
#             filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
#             file.save(filepath)
#             text = parser.from_file(filepath)['content']
#             result = client.detect_entities(Text=text)
#             # return jsonify(result['Entities'])
#             return result
#
#             # return redirect(url_for('uploaded_file',
#             #                         filename=filename))
#     return '''
#     <!doctype html>
#     <title>Upload new File</title>
#     <h1>Upload new File</h1>
#     <form method=post enctype=multipart/form-data>
#       <input type=file name=file>
#       <input type=submit value=Upload>
#     </form>
#     '''
#
#
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
    app.run(debug=True)
