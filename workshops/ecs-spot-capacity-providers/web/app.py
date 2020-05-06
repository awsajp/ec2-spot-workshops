from flask import Flask
import os
import requests
import json

app = Flask(__name__)

@app.route('/')
def index():
    
    response = ""
    response += "<h2>Environment Variables</h2> <hr/>"

    for env_var in os.environ:
        response += "<li>{}: {}</li>".format(env_var, os.environ.get(env_var))

    if 'AWS_EXECUTION_ENV' in os.environ:
        response += "<h2>Execution Environment: {}</h2> <hr/>".format(os.environ.get('AWS_EXECUTION_ENV'))
    else:
        response += "<h2>Execution Environment: {}</h2> <hr/>".format('LOCAL')

    if 'ECS_CONTAINER_METADATA_URI' in os.environ:
        metadata_uri = os.environ.get('ECS_CONTAINER_METADATA_URI')
        metadata = requests.get(metadata_uri)
        response += "<h2>Metadata</h2 <hr/> {}".format(json.dumps(metadata.text, indent=4, sort_keys=True))

    return response

if __name__ == '__main__':

    app.run(debug=True,host='0.0.0.0', port=80)