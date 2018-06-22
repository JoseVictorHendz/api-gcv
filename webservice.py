from flask import Flask, jsonify

import io
import os

from google.cloud import vision
from google.cloud.vision import types
from google.protobuf.json_format import MessageToJson

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "apikey.json"
# print("--------------------",os.environ["GOOGLE_APPLICATION_CREDENTIALS"] )
# Imports the Google Cloud client library


app = Flask(__name__)
print("teste")




@app.route("/retornoApiGoogleVision")
def index():
    retorno = []

    # Instantiates a client
    client = vision.ImageAnnotatorClient()

    # The name of the image file to annotate
    file_name = os.path.join(
        os.path.dirname(__file__),
        './urso.jpg')

    # Loads the image into memory
    with io.open(file_name, 'rb') as image_file:
        content = image_file.read()

    image = types.Image(content=content)

    # Performs label detection on the image file
    response = client.label_detection(image=image)
    labels = response.label_annotations

    for label in labels:
        retorno.append(label.description)
        print(label.description)

    return jsonify(retorno)


# if __name__ == '__main__':
#     app.run(debug=True)
#
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
