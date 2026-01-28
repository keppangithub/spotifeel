import os
import sys
import pytest

# Set dummy environment variables for testing BEFORE any imports
if not os.getenv('OPENAI_API_KEY'):
    os.environ['OPENAI_API_KEY'] = 'test-key-12345'
if not os.getenv('CLIENT_ID'):
    os.environ['CLIENT_ID'] = 'test-client-id'
if not os.getenv('CLIENT_SECRET'):
    os.environ['CLIENT_SECRET'] = 'test-client-secret'

# Add the project directories to the path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(project_root, 'API'))
sys.path.insert(0, os.path.join(project_root, 'Client'))
