from flask import Blueprint, render_template, request
import numpy as np
import cv2

import settings

preview_blueprint = Blueprint("preview", __name__)

@preview_blueprint.route("/", methods=["POST"])
def preview():
    print("here")
    image_string = request.files["image"].read()
    image_bytes = np.fromstring(image_string, dtype=np.uint8)
    image = cv2.imdecode(image_bytes, cv2.IMREAD_UNCHANGED)

    message = request.form["message"]    
    font_scale = int(request.form["fontscale"])

    x0 = 50
    y0 = 50 * font_scale
    thickness = 2
    font_face = cv2.FONT_HERSHEY_SIMPLEX
    color = (255, 255, 255)

    # create preview image
    h, w, _ = image.shape
    h_b = int(h / settings.sh)
    w_b = int(w / settings.sw)

    text_image = np.zeros(image.shape, dtype=np.uint8)

    distance = 50
    sentences = message.splitlines()
    for index, sentence in enumerate(sentences):
        y = y0 + index * distance * font_scale
        text_image = cv2.putText(text_image, sentence, (x0, y), font_face, font_scale, color, thickness)


    text_image = cv2.resize(text_image, dsize=(h_b, w_b))

    cv2.imwrite("./static/images/preview.jpg", text_image)

    return render_template("preview/index.html", title="Invisi-Ink | Preview")