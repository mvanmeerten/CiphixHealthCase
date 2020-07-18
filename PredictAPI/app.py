from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os
import boto3

client = boto3.client(service_name='comprehendmedical', region_name='eu-west-2')

# Init app
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
# Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Init db
db = SQLAlchemy(app)
# Init marshmallow
ma = Marshmallow(app)

@app.route('/', methods=['POST'])
def extract_entities():
    data = request.get_json()
    print(data)
    result = client.detect_entities(Text='cerealx 84 mg daily')
    # result = client.detect_entities(Text=data['text'])
    entities = result['Entities']
    for entity in entities:
        print('Entity', entity)
    return jsonify(entities)


# Run server
if __name__ == '__main__':
    app.run()
