from flask import Blueprint, render_template, request, send_file
import numpy as np
import cv2

import settings
from utils.decode import decoding

decode_blueprint = Blueprint("decode", __name__)

@decode_blueprint.route("/", methods=["GET"])
def decode_get():
    return render_template("decode/index.html", title="Invisi-Ink | Decoding")


@decode_blueprint.route("/", methods=["POST"])
def decode_post():
    image_string = request.files["image"].read()
    image_bytes = np.fromstring(image_string, dtype=np.uint8)
    
    image = cv2.imdecode(image_bytes, cv2.IMREAD_UNCHANGED)

    text_image = decoding(image, settings.sh, settings.sw)

    cv2.imwrite(settings.file_name, text_image)
    
    response = send_file(settings.file_name, mimetype='image/png', as_attachment=True)

    return response