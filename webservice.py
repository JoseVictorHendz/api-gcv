from flask import Flask, jsonify, request
import random

import io
import os

from base64 import decodestring

from google.cloud import vision
from google.cloud.vision import types

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "apikey.json"

app = Flask(__name__)


def prepararImagemParaSalvar():
    imagem = request.json['img']

    imagem = imagem.encode("utf8")

    return imagem

def salvarImagem(imgBase64):

    hash = random.getrandbits(128)
    nomeArquivo = str(hash)

    print("----------------", type(imgBase64))
    # # In Python 2.7
    # fh = open("./imagens/" + nomeArquivo + ".png", "wb")
    # fh.write(imgBase64.decode('base64'))
    # fh.close()

    with open("./imagens/" + nomeArquivo + ".png", "wb") as f:
        f.write(decodestring(imgBase64))
   
    return nomeArquivo

def enviarApiGCV(idArquivo):
    client = vision.ImageAnnotatorClient()

    file_name = os.path.join(
        os.path.dirname(__file__),
        './imagens/' + idArquivo + '.png')

    with io.open(file_name, 'rb') as image_file:
        content = image_file.read()

    image = types.Image(content=content)

    response = client.label_detection(image=image)
    labels = response.label_annotations

    return recuperarRetornoApi(labels)

def recuperarRetornoApi(labels):
    retorno = []

    for label in labels:
        retorno.append(label.description)
        print(label.description)
    return retorno



@app.route("/retornoApiGoogleVision", methods=['POST'])
def index():
    imagem = prepararImagemParaSalvar()

    idArquivo = salvarImagem(imagem)

    labels = enviarApiGCV(idArquivo)

    return jsonify(labels)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
