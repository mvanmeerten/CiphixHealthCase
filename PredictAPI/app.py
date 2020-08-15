import os

import boto3
from flask import Flask, request, flash, redirect, render_template, send_from_directory, url_for, jsonify
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from pdfminer.high_level import extract_text
from werkzeug.utils import secure_filename
from wtforms import SubmitField

client = boto3.client(service_name='comprehendmedical', region_name='eu-west-2')

# Init app
UPLOAD_FOLDER = 'C:/Users/Martijn/PycharmProjects/CiphixHealthCase/PredictAPI/docs'
ALLOWED_EXTENSIONS = {'pdf'}
app = Flask(__name__)
app.config["SECRET_KEY"] = "secret"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    """
    Only allow files with extensions from ALLOWED_EXTENSIONS
    :param filename: The filename of the uploaded file
    :return If allowed, True, else, False
    """
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def choose_color(category):
    COLOR_CATEGORIES = {
        "ANATOMY": "cyan",
        "MEDICAL_CONDITION": "lightgreen",
        "MEDICATION": "yellow",
        "PROTECTED_HEALTH_INFORMATION": "orange",
        "TEST_TREATMENT_PROCEDURE": "pink"
    }

    return "<span style=\"background-color:" + COLOR_CATEGORIES[category] + "\">"


def highlight_entities(text, entities):
    """
    Highlight entities found in original text.
    :param text: The text to highlight in
    :param entities: The entities found by the NER system
    :return: The original text with entities highlighted
    """
    last_index = 0
    for entity in entities:
        # index throws an exception if entity is not found in the text.
        try:
            entity_index = text.index(entity['Text'], last_index)
            last_index = entity_index
            # Mark the found entity
            text = text[:entity_index] + choose_color(entity['Category']) + text[entity_index:entity_index+len(entity['Text'])] + "</span>" + text[entity_index+len(entity['Text']):]
            # Mark potential attributes as well
            if 'Attributes' in entity:
                for attribute in entity['Attributes']:
                    attribute_index = text.index(attribute['Text'], last_index)
                    last_index = attribute_index
                    text = text[:attribute_index] + "<mark>" + text[attribute_index:attribute_index + len(attribute['Text'])] + "</mark>" + text[attribute_index + len(attribute['Text']):]
        except ValueError:
            pass

    return text


@app.route('/', methods=['get', 'POST'])
def index():
    """
    Load the page.
    :return:
    """
    form = UploadForm()
    # If the user uploaded a file, save, parse, and extract entities from text.
    if request.method == "POST":
        if form.validate_on_submit():
            if 'file' not in request.files:
                return redirect(request.url)
            file = request.files['file']
            # if user does not select file, browser also
            # submit an empty part without filename
            if file.filename == '':
                return redirect(request.url)
            if file and allowed_file(file.filename):
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(file.filename))
                file.save(file_path)
                text = extract_text(file)
                result = client.detect_entities(Text=text)
                text = highlight_entities(text, result['Entities'])
                return render_template('index.html', form=form, entities=result['Entities'], text=text[:-1])

    return render_template('index.html', form=form)


class UploadForm(FlaskForm):
    """
    Flask_wtf form for uploading files.
    """
    file = FileField(validators=[
        FileRequired(),
        FileAllowed(ALLOWED_EXTENSIONS, 'Only pdf files are allowed.')
    ])
    submit = SubmitField("submit")


# Run server
if __name__ == '__main__':
    app.run(debug=False)
