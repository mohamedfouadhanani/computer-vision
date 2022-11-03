import os
from flask import Blueprint, render_template, request, send_file
import numpy as np
import cv2

import settings
from utils.encode import encoding

encode_blueprint = Blueprint("encode", __name__)

@encode_blueprint.route("/", methods=["GET"])
def encode_get():
    return render_template("encode/index.html", title="Invisi-Ink | Encoding")


@encode_blueprint.route("/", methods=["POST"])
def encode_post():
    image_string = request.files["image"].read()
    image_bytes = np.fromstring(image_string, dtype=np.uint8)
    image = cv2.imdecode(image_bytes, cv2.IMREAD_COLOR)

    message = request.form["message"]
    font_scale = int(request.form["fontscale"])

    encoded_image, _ = encoding(image, message, font_scale, settings.sh, settings.sw)
    
    cv2.imwrite(settings.file_name, encoded_image)
    
    response = send_file(settings.file_name, mimetype='image/png', as_attachment=True)

    return response