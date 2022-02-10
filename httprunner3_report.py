from flask import Flask
from flask import render_template
import os
from icecream import ic

# template_folder = "{}{}{}".format(os.path.dirname(__file__), os.path.sep, "report")
# template_folder = "{}{}{}".format(os.path.dirname(os.path.abspath(os.path.curdir)), os.path.sep, "report")
template_folder = os.environ.get("REPORT_DIR", "")

# template_folder = r"d:\temps"
ic(template_folder)

app = Flask(__name__, template_folder=template_folder)


@app.route("/")
def report():
    return render_template("report.html")
