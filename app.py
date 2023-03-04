from flask import Flask, render_template
from get_nasa_images import get_nasa_images
import os

app = Flask(__name__, template_folder='templates')

@app.route("/")
def home():
    image_list = os.listdir("static")
    return render_template("home.html", images=image_list)

if __name__ == "__main__":
    get_nasa_images()
    app.run(debug=True)
