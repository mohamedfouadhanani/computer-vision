from flask import Flask, redirect

# blueprints
from routes.encode import encode_blueprint
from routes.decode import decode_blueprint
from routes.preview import preview_blueprint

# settings
import settings

settings.init()

app = Flask(__name__)

app.register_blueprint(encode_blueprint, url_prefix="/encode")
app.register_blueprint(decode_blueprint, url_prefix="/decode")
app.register_blueprint(preview_blueprint, url_prefix="/preview")

@app.route("/", methods=["GET"])
def index():
    return redirect("/encode")

if __name__ == '__main__':
     app.run(debug=True)