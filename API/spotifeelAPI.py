from flask import jsonify
import yaml, os, json
import playlists # Om playlists är i samma mapp (API)

# Dictionary of emotions mapped to their respective IDs
# Set file paths for YAML and JSON API documentation files
yaml_file_path = os.path.join(os.getcwd(), 'static', 'swagger.yaml')
json_file_path = os.path.join(os.getcwd(), 'static', 'swagger.json')

# Read the YAML file containing API documentation
'''with open(yaml_file_path, 'r') as yaml_file:
    SWAGGER_SPEC = yaml.safe_load(yaml_file)

# Write the API documentation to a JSON file for serving as static content
with open(json_file_path, 'w') as json_file:
    json.dump(SWAGGER_SPEC, json_file, indent=2)'''

def get_loaded_playlist() ->list:
    '''
    Call the function get_loaded_playlist()
    
    Returns:
        list: A list of dictionaries, each representing a playlist with a playlist 'id' and 'uri'.
        If an error occurs an empty list is returned.
    '''
    return playlists.get_loaded_playlist()

def get_playlists() -> list:
    '''
    Call the function get_playlists().
    
    Returns:
        A list of dictionaries, each representing a playlist with a playlist 'id' and 'uri'.
    '''
    return playlists.get_playlists()

def get_playlists_by_id(id) -> str:
    '''
    Call the function get_playlists_by_id.
    
    Args:
        id (str): playlist id.
        
    Returns:
        str: The URI of the playlist, or a message saying 'No playlist found' if not found.
    '''
    return playlists.get_playlists_by_id(id)
