from flask import Flask, jsonify
from flask_swagger_ui import get_swaggerui_blueprint
import yaml
import os
import json


app = Flask('__name__') # Specify static folder explicitly
SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.json'

swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Spotifeel API"
    }
)
app.register_blueprint(swaggerui_blueprint,url_prefix = SWAGGER_URL)


yaml_file_path = os.path.join(os.getcwd(), 'static', 'swagger.yaml')
json_file_path = os.path.join(os.getcwd(), 'static', 'swagger.json')

with open(yaml_file_path, 'r') as yaml_file:
    SWAGGER_SPEC = yaml.safe_load(yaml_file)

with open(json_file_path, 'w') as json_file:
    json.dump(SWAGGER_SPEC, json_file, indent=2)


@app.route('/static/swagger.json')
def swagger_json():
    return jsonify(SWAGGER_SPEC)

if __name__ == '__main__':
    app.run(debug=True)
