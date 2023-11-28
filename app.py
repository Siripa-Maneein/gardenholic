import sys
import os

if not os.path.exists("config.py"):
    print("Configuration 'config.py' not found.  "
          "You may create one from 'config.py.example'.")
    sys.exit(1)

from config import OPENAPI_STUB_DIR

if not os.path.exists(OPENAPI_STUB_DIR):
    print(f"Folder '{OPENAPI_STUB_DIR}' not found.  "
          "Please create the folder and extract zip file "
          "generated by openapi-generator into it.")
    sys.exit(1)

sys.path.append(OPENAPI_STUB_DIR)

try:
    import connexion
    from flask_cors import CORS
except ModuleNotFoundError:
    print("Please install all required packages by running:"
          " pip install -r requirements.txt")
    sys.exit(1)

from swagger_server import encoder

def main():
    app = connexion.App(__name__, specification_dir='./openapi/')
    app.app.json_encoder = encoder.JSONEncoder
    app.add_api('gardenholic-api.yaml',
                arguments={'title': 'GardenHolic API'},
                pythonic_params=True)
    
    CORS(app.app)

    app.run(port=8080, debug=True)

if __name__ == '__main__':
    main()
