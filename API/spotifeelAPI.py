from flask import jsonify
import yaml, os, json

# Dictionary of emotions mapped to their respective IDs
# Set file paths for YAML and JSON API documentation files
yaml_file_path = os.path.join(os.getcwd(), 'static', 'swagger.yaml')
json_file_path = os.path.join(os.getcwd(), 'static', 'swagger.json')

